"""OJT-to-domain parser."""

from itertools import groupby
from typing import TypeGuard
from warnings import warn

from speechtree.characters import (
    MORA_MATCH_PATTERN,
    MORA_PRONUNCIATION,
    MR_CV,
    MoraPronunciation,
)
from speechtree.tree import (
    AccentPhrase,
    BreathGroup,
    MarkGroup,
    Mora,
    Phoneme,
    Tree,
    Word,
)

from .domain import OjtFeature


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


def _is_mora_pronunciation(pron: str) -> TypeGuard[MoraPronunciation]:
    return pron in MORA_PRONUNCIATION


def _parse_as_phonemes(
    mora_pron_unvoice: tuple[str, bool],
) -> tuple[Phoneme, Phoneme] | tuple[Phoneme]:
    mora_pron, mora_unvoicing = mora_pron_unvoice
    if not _is_mora_pronunciation(mora_pron):
        raise RuntimeError
    consonant_symbol, vowel_symbol = MR_CV[mora_pron]
    v = Phoneme(symbol=vowel_symbol, unvoicing=mora_unvoicing)

    if consonant_symbol:
        # NOTE: consonant is never unvoiced/無声化 because consonant is always unvoice/無声音.
        return (Phoneme(symbol=consonant_symbol, unvoicing=False), v)
    return (v,)


def _parse_as_moras(feat: OjtFeature) -> list[Mora]:
    """Parse an Open JTalk feature into moras."""
    # NOTE:
    #   Mora-list-matching divide pronunciation into moras.
    #   [division example]
    #                  MR#0   MR#1  MR#2
    #   "ギョウザ" -> ["ギョ", "ウ", "ザ"]
    if feat.pron == "":
        return []

    pron_unvoice_pairs = _split_pron_into_mora_prons(feat.pron)

    # Validate
    if pron_unvoice_pairs[0][0] == "ー":
        msg = "長音（`ー`）はワードの先頭に置けません。この長音は無視されます。"  # noqa: RUF001, because of Japanese.
        warn(msg, stacklevel=2)
        if len(pron_unvoice_pairs) == 1:
            # No not-ignored mora remains.
            return []
        pron_unvoice_pairs = pron_unvoice_pairs[1:]

    # Convert mr-wise pronunciation into Mora.
    # NOTE: `tone_high` is fixed to False. Need update after.
    moras: list[Mora] = []
    for pron, unvoicing in pron_unvoice_pairs:
        match pron:
            case "ー":
                symbol = moras[-1]["phonemes"][-1]["symbol"]
                v = Phoneme(symbol=symbol, unvoicing=unvoicing)
                moras.append(Mora(phonemes=(v,), pronunciation=pron, tone_high=False))
            case "、" | "？":  # noqa: RUF001, because of Japanese.
                pau = Phoneme(symbol="pau", unvoicing=False)
                moras.append(Mora(phonemes=(pau,), pronunciation="　", tone_high=False))
            case _:
                pns = _parse_as_phonemes((pron, unvoicing))
                moras.append(Mora(phonemes=pns, pronunciation=pron, tone_high=False))

    return moras


def _is_chaining(feat: OjtFeature) -> bool:
    """Whether the feature is chaining or not."""
    return feat.chain_flag == 1


def _parse_as_ap(feats: list[OjtFeature]) -> AccentPhrase:
    """Parse Open JTalk features into an accent phrase."""
    # NOTE: length of `feats` is not zero (contract)
    ap_moras: list[Mora] = []
    words: list[Word] = []
    for feat in feats:
        wd_moras = _parse_as_moras(feat)
        words.append(Word(moras=wd_moras, text=feat.string))
        ap_moras += wd_moras

    # Update tone based on 東京式アクセント rule.
    # NOTE: OJT records the phrase accent type in ap-head feature.
    # Convert accent type into accent position.
    acc_pos = feats[0].acc if feats[0].acc > 0 else len(ap_moras)
    # Switch tone to high until accent position
    for i, mora in enumerate(ap_moras):
        if i < acc_pos:
            mora["tone_high"] = True
    # Switch tone to low at head if not type1.
    if acc_pos > 1:
        ap_moras[0]["tone_high"] = False

    return AccentPhrase(words=words)


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


def parse_ojt_as_tree(feats: list[OjtFeature]) -> Tree:
    """Open JTalk のテキスト処理結果を Tree としてパースする。"""
    if len(feats) == 0:
        return []

    tree: Tree = []
    # Divide features into successive voices (BreathGroup) and successive marks (MarkGroup).
    for is_marks, successive_feats in groupby(feats, _is_mark):
        aps = _parse_as_aps(list(successive_feats))
        tree += [
            MarkGroup(accent_phrases=aps, type="MarkGroup")
            if is_marks
            else BreathGroup(accent_phrases=aps, type="BreathGroup")
        ]
    return tree
