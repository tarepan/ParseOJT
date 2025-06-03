"""OJT-to-domain parser."""

from itertools import batched, groupby
from typing import TypeGuard
from warnings import warn

from parseojt.characters import (
    MORA_MATCH_PATTERN,
    MORA_PRONUNCIATION,
    MR_CV,
    MoraPronunciation,
)

from .domain import (
    VOWEL_SYMBOLS,
    AccentPhrase,
    BreathClause,
    Consonant,
    Mora,
    Utterance,
    Vowel,
    VowelSymbol,
    Word,
)
from .ojt.domain import OjtFeature


def _split_pron_into_mora_prons(pron: str) -> list[tuple[str, bool]]:
    mora_prons: list[tuple[str, bool]] = []
    while len(pron):
        match = MORA_MATCH_PATTERN.match(pron)
        if match is None:
            msg = "not match"
            raise RuntimeError(msg)
        mora_pron = match[0]
        if mora_pron[-1] == "’":  # noqa: RUF001, because of Japanese.
            mora_prons.append((mora_pron[:-1], True))
        else:
            mora_prons.append((mora_pron, False))
        pron = pron[match.end() :]
    return mora_prons


class ParseError(Exception):
    """Parse failed."""


def _is_vowel_symbol(symbol: str) -> TypeGuard[VowelSymbol]:
    return symbol in VOWEL_SYMBOLS


def _is_mora_pronunciation(pron: str) -> TypeGuard[MoraPronunciation]:
    return pron in MORA_PRONUNCIATION


def _parse_as_phonemes(
    mora_pron_unvoice: tuple[str, bool],
) -> tuple[Consonant, Vowel] | tuple[Vowel]:
    mora_pron = mora_pron_unvoice[0]
    if not _is_mora_pronunciation(mora_pron):
        raise RuntimeError
    consonant_symbol, vowel_symbol = MR_CV[mora_pron]
    if mora_pron_unvoice[1]:
        if vowel_symbol in ["a", "i", "u", "e", "o"]:
            _vowel_symbol = vowel_symbol.upper()
            if not _is_vowel_symbol(_vowel_symbol):
                msg = "Never"
                raise RuntimeError(msg)
            vowel_symbol = _vowel_symbol
        else:
            msg = "無声化は /-a/ /-i/ /-u/ /-e/ /-o/ でのみ可能です。{vowel_symbol} には適用できないため無視されます。"
            warn(msg, stacklevel=2)
    v = Vowel(vowel_symbol)
    return (Consonant(consonant_symbol), v) if consonant_symbol else (v,)


def _parse_as_moras(feat: OjtFeature) -> list[Mora]:
    """Parse an Open JTalk feature into moras."""
    # NOTE:
    #   Mora-list-matching divide pronunciation into moras.
    #   [division example]
    #                  MR#0   MR#1  MR#2
    #   "ギョウザ" -> ["ギョ", "ウ", "ザ"]
    if feat.pron == "":
        return []

    mr_prons = _split_pron_into_mora_prons(feat.pron)

    # Validate
    if mr_prons[0][0] == "ー":
        msg = "長音（`ー`）はワードの先頭に置けません。この長音は無視されます。"  # noqa: RUF001, because of Japanese.
        warn(msg, stacklevel=2)
        if len(mr_prons) == 1:
            # No not-ignored mora remains.
            return []
        mr_prons = mr_prons[1:]

    # Convert mr-wise pronunciation into Mora.
    moras: list[Mora] = []
    for mr_pron in mr_prons:
        if mr_pron[0] == "ー":
            moras.append(Mora((Vowel(moras[-1].phonemes[-1].symbol),), mr_pron[0]))
        else:
            moras.append(Mora(_parse_as_phonemes(mr_pron), mr_pron[0]))

    return moras


def _is_chaining(feat: OjtFeature) -> bool:
    """Whether the feature is chaining or not."""
    return feat.chain_flag == 1


def _parse_as_ap(feats: list[OjtFeature], *, interrogative: bool) -> AccentPhrase:
    """Parse Open JTalk features into an accent phrase."""
    # NOTE: length of `feats` is not zero (contract)
    n_mora: int = 0
    words: list[Word] = []
    for feat in feats:
        moras = _parse_as_moras(feat)
        words.append(Word(moras, feat.string))
        n_mora += len(moras)
    # NOTE: OJT records the phrase accent type in ap-head feature
    acc = feats[0].acc
    # NOTE: Convert accent type into accent (アクセント核) position. Type 0 has 核 at last.
    acc = acc if acc > 0 else n_mora
    return AccentPhrase(words, acc, interrogative=interrogative)


def _parse_as_aps(
    feats: list[OjtFeature], *, last_interrogative: bool
) -> list[AccentPhrase]:
    """Parse Open JTalk features into accent phrases."""
    # NOTE:
    #   Chain flag divide features into accent phrases.
    #   [division example]
    #     n: chain-False feature, c: chain-True feature
    #                              AP#0     AP#1  AP#2  AP#3
    #   [n,c,c,n,c,c,c,n,n,c] -> [n,c,c,| n,c,c,c,| n,| n,c]

    # Split features into ap-wises.
    #   [n,c,c,n,c,c,c,n,n,c] -> [n,c,c,| n,c,c,c,| n,| n,c]
    ap_wises: list[list[OjtFeature]] = []
    ap_wise: list[OjtFeature] = []
    for feat in feats:
        if _is_chaining(feat):
            if len(ap_wises) == 0 and len(ap_wise) == 0:
                msg = f"ワードの連結はブレス節内でのみ発生します。ワード `{feat.string}` は句頭であるため、連結フラグは無視されます。"
                warn(msg, stacklevel=2)
            ap_wise.append(feat)
        else:
            # Next ap
            if len(ap_wise) > 0:
                ap_wises.append(ap_wise)
            ap_wise = [feat]
    if len(ap_wise) > 0:
        ap_wises.append(ap_wise)

    if len(ap_wises) == 0:
        return []

    # Convert ap-wise features into AccentPhrase.
    #   [n,c,c,| n,c,c,c,| n,| n,c] -> [AP#0, AP#1, AP#2, AP#3]
    tail_ap = [_parse_as_ap(ap_wises[-1], interrogative=last_interrogative)]
    return [
        _parse_as_ap(ap_wise, interrogative=False) for ap_wise in ap_wises[:-1]
    ] + tail_ap


def _is_pau(word: OjtFeature) -> bool:
    """Whether the word is pause or not."""
    return word.pron in ["、", "？"]  # noqa: RUF001, because of Japanese.


def _is_interrogative(word: OjtFeature) -> bool:
    """Whether the word is interrogative or not."""
    return word.pron == "？"  # noqa: RUF001, because of Japanese.


class NonBreathError(ParseError):
    """The feature is not a breath feature."""


def _parse_as_breath_word(breath_features: list[OjtFeature]) -> Word | None:
    """Parse breath features as a breath word."""
    # NOTE: interpreted as no breath
    if len(breath_features) == 0:
        return None

    # Validate
    if not all(map(_is_pau, breath_features)):
        msg = "Non-breath feature comes to `parse_breaths()`."
        raise NonBreathError(msg)

    # Parse
    phonemes = (Vowel(symbol="pau"),)
    text = "".join([feat.string for feat in breath_features])

    return Word([Mora(phonemes, "、")], text)


def _parse_as_bcs(feats: list[OjtFeature]) -> list[BreathClause]:
    """Parse Open JTalk features into breath clauses."""
    # NOTE:
    #   PAUs divide features into breath clauses.
    #   [division example]
    #     v: voice feature, p: pause feature
    #                                  BC#0     BC#1      BC#2  BC#3
    #   [v,v,p,v,v,v,p,p,v,p,v,v] -> [v,v,p,| v,v,v,p,p,| v,p,| v,v]

    if len(feats) == 0:
        return []

    # Group successive voices and successive pauses.
    #   [v,v,p,v,v,v,p,p,v,p,v,v] -> [v,v,| p,| v,v,v,| p,p,| v,| p,| v,v]
    groups = [list(group) for _, group in groupby(feats, _is_pau)]

    # Remove ut-head pauses.
    #   [p,p,p,| v,v,| p,| ...] -> [v,v,| p,| ...]
    if _is_pau(groups[0][0]):
        texts = "".join([w.string for w in groups[0]])
        msg = f"「{texts}」は音がないワードです。文頭に来れないため、無視されます。"
        warn(msg, stacklevel=2)
        if len(groups) == 1:
            # No not-ignored feature remains.
            return []
        groups = groups[1:]

    # Convert bc-wise voices/pauses into BreathClause.
    #   [v,v,| p,| v,v,v,| p,p,| v,| p,| v,v] -> [BC#0, BC#1, BC#2, BC#3]
    bcs: list[BreathClause] = []
    for bc_wise_vs_ps in batched(groups, 2):
        bc_wise_voices = bc_wise_vs_ps[0]
        # NOTE: 'No-end-period text' is converted to 'No-end-pau features' by OJT.
        bc_wise_pauses = bc_wise_vs_ps[1] if len(bc_wise_vs_ps) > 1 else []
        is_interrogative_pause = any(map(_is_interrogative, bc_wise_pauses))
        bc = BreathClause(
            _parse_as_aps(bc_wise_voices, last_interrogative=is_interrogative_pause),
            _parse_as_breath_word(bc_wise_pauses),
        )
        bcs.append(bc)

    return bcs


def parse_ojt_features(ojt_feats: list[OjtFeature]) -> Utterance:
    """Parse Open JTalk feature series into a hierarchical utterance."""
    return _parse_as_bcs(ojt_feats)
