"""OJT-to-domain parser."""

from itertools import groupby
from typing import TypeGuard
from warnings import warn

from parseojt.characters import (
    MORA_MATCH_PATTERN,
    MORA_PRONUNCIATION,
    MR_CV,
    VOWEL_SYMBOLS,
    MoraPronunciation,
    VowelSymbol,
)

from .domain import (
    AccentPhrase,
    BreathGroup,
    MarkGroup,
    Mora,
    Phoneme,
    Tree,
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
) -> tuple[Phoneme, Phoneme] | tuple[Phoneme]:
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
    v = Phoneme(vowel_symbol, unvoicing=mora_pron_unvoice[1])
    return (Phoneme(consonant_symbol), v) if consonant_symbol else (v,)


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
        match mr_pron[0]:
            case "ー":
                # NOTE: needs unvoicing check?
                moras.append(
                    Mora((Phoneme(moras[-1].phonemes[-1].symbol),), mr_pron[0])
                )
            case "、" | "？":  # noqa: RUF001, because of Japanese.
                moras.append(Mora((Phoneme("pau"),), mr_pron[0]))
            case _:
                moras.append(Mora(_parse_as_phonemes(mr_pron), mr_pron[0]))

    return moras


def _is_chaining(feat: OjtFeature) -> bool:
    """Whether the feature is chaining or not."""
    return feat.chain_flag == 1


def _parse_as_ap(feats: list[OjtFeature]) -> AccentPhrase:
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
    return AccentPhrase(words, acc)


def _parse_as_aps(feats: list[OjtFeature]) -> list[AccentPhrase]:
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

    return [_parse_as_ap(ap_wise) for ap_wise in ap_wises]


def _is_mark(word: OjtFeature) -> bool:
    """Whether the word is mark or not."""
    return word.pron in ["、", "？"]  # noqa: RUF001, because of Japanese.


# def parse_ojt_as_tree(feats: list[OjtFeature]) -> Tree:
def parse_ojt_features(feats: list[OjtFeature]) -> Tree:
    """Open JTalk のテキスト処理結果を Tree としてパースする。"""
    if len(feats) == 0:
        return []

    tree: Tree = []
    # Divide features into successive voices (BreathGroup) and successive marks (MarkGroup).
    for is_marks, successive_feats in groupby(feats, _is_mark):
        aps = _parse_as_aps(list(successive_feats))
        tree += [MarkGroup(aps) if is_marks else BreathGroup(aps)]
    return tree
