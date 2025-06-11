"""Tree-To-VOICEVOX converter."""

from itertools import batched
from typing import Final
from warnings import warn

from speechtree.gardener import extract_text
from speechtree.tree import PhraseGroup, Tree, Word
from speechtree.voicevox.domain import AccentPhrase, Mora

_NON_VV_MORA_MAPPING = {
    "ヲ": "オ",
    "ヱ": "エ",
    "ヰ": "イ",
    "ヮ": "ワ",
    "ョ": "ヨ",
    "ュ": "ユ",
    "ヅ": "ズ",
    "ヴョ": "ビョ",
    "ヴュ": "ビュ",
    "ヴャ": "ビャ",
    "ヂョ": "ジョ",
    "ヂュ": "ジュ",
    "ヂャ": "ジャ",
    "ヂェ": "ジェ",
    "ヂ": "ジ",
    "グァ": "グヮ",
    "クァ": "クヮ",
    "ヶ": "ケ",
    "ャ": "ヤ",
    "ォ": "オ",
    "ェ": "エ",
    "ゥ": "ウ",
    "ィ": "イ",
    "ァ": "ア",
}
_NON_VV_MORA_PRONS: Final = list(_NON_VV_MORA_MAPPING.keys())


def _gen_pau_mora() -> Mora:
    """Generate VOICEVOX pause mora."""
    # NOTE: ref: https://github.com/VOICEVOX/voicevox_engine/blob/c95bb9e387043e7f7a2eb4fd3e46692fea28716a/voicevox_engine/tts_pipeline/text_analyzer.py#L383-L391
    return Mora(
        text="、",
        consonant=None,
        consonant_length=None,
        vowel="pau",
        vowel_length=0.0,
        pitch=0.0,
    )


def _unvoiced_symbol(symbol: str) -> str:
    """Convert the symbol into unvoiced phoneme symbol."""
    return symbol.upper()


def _aiueo_to_mora_pron(phoneme: str) -> str:
    match phoneme:
        case "a" | "A":
            return "ア"
        case "i" | "I":
            return "イ"
        case "u" | "U":
            return "ウ"
        case "e" | "E":
            return "エ"
        case "o" | "O":
            return "オ"
        case _:
            msg = f"音素 `{phoneme}` は長音に変換できません。"
            raise RuntimeError(msg)


def _replace_mora_pron(mora_pron: str) -> str:
    if mora_pron in _NON_VV_MORA_PRONS:
        mora_pron = _NON_VV_MORA_MAPPING[mora_pron]
    return mora_pron


def _convert_words_to_voicevox_moras(words: list[Word]) -> list[Mora]:
    """Convert words into VOICEVOX moras."""
    vv_moras: list[Mora] = []
    for word in words:
        for mora in word["moras"]:
            phonemes = mora["phonemes"]

            consonant_symbol = None if len(phonemes) == 1 else phonemes[0]["symbol"]
            consonant_length = None if len(phonemes) == 1 else 0.0

            vowel = phonemes[-1]
            _v_symbol = vowel["symbol"]
            v_symbol = _unvoiced_symbol(_v_symbol) if vowel["unvoicing"] else _v_symbol
            vowel_length = 0.0

            pron = mora["pronunciation"]
            if pron[-1] == "’":  # noqa: RUF001, because of Japanese.
                mora_text = pron[:-1]
            elif pron == "ー":
                # NOTE: VOICEVOX losts prolonged sound mark. Only realized phonemes remain.
                mora_text = _aiueo_to_mora_pron(v_symbol)
            else:
                mora_text = pron
            vv_moras.append(
                Mora(
                    text=_replace_mora_pron(mora_text),
                    consonant=consonant_symbol,
                    consonant_length=consonant_length,
                    vowel=v_symbol,
                    vowel_length=vowel_length,
                )
            )
    return vv_moras


def _contain_interrogative(pg: PhraseGroup) -> bool:
    """Whether the group contains interrogative or not."""
    text = ""
    for ap in pg["accent_phrases"]:
        for wd in ap["words"]:
            text += wd["text"]
    return "？" in text  # noqa: RUF001, because of Japanese.


def convert_tree_to_voicevox_accent_phrases(
    tree: Tree,
) -> list[AccentPhrase]:
    """Convert tree into VOICEVOX accent phrases."""
    # Validation on VOICEVOX standards
    # unvoicing check ["a", "i", "u", "e", "o"]
    # "無声化は /-a/ /-i/ /-u/ /-e/ /-o/ でのみ可能です。{vowel_symbol} には適用できないため無視されます。

    # Remove tree-head MarkGroup.
    if tree[0]["type"] == "MarkGroup":
        texts = extract_text(tree[0:1])
        msg = f"「{texts}」には音がありません。文頭に来れないため無視されます。"
        warn(msg, stacklevel=2)
        tree = tree[1:]

    # Divide groups into BG-MG pairs
    bg_mg_pairs = list(batched(tree, 2))

    # Generate accent phrases
    vv_aps: list[AccentPhrase] = []
    for i, bg_mg in enumerate(bg_mg_pairs):
        # Last pair can be not pair, just BG 1-tuple.
        bg = bg_mg[0]
        mg = bg_mg[1] if len(bg_mg) == 2 else None  # noqa: PLR2004, because length of pair equal to 2 is apparent.

        is_tail_bg = i == len(bg_mg_pairs) - 1
        is_interrogative_bg = _contain_interrogative(mg) if mg else False

        for ap in bg["accent_phrases"]:
            is_tail_ap = ap == bg["accent_phrases"][-1]
            # NOTE: VOICEVOX delete utterance tail pause.
            with_pau = is_tail_ap and not is_tail_bg
            interrogative = is_tail_ap and is_interrogative_bg
            vv_aps.append(
                AccentPhrase(
                    _convert_words_to_voicevox_moras(ap["words"]),
                    accent=ap["accent"],
                    pause_mora=_gen_pau_mora() if with_pau else None,
                    is_interrogative=interrogative,
                )
            )

    return vv_aps
