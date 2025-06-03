"""Utterance-To-VOICEVOX converter."""

from typing import Final

from parseojt.domain import Utterance, Word
from parseojt.voicevox.domain import AccentPhrase, Mora

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
        for mora in word.moras:
            phonemes = mora.phonemes
            consonant = None if len(phonemes) == 1 else phonemes[0].symbol
            consonant_length = None if len(phonemes) == 1 else 0.0
            vowel = phonemes[-1].symbol
            pron = mora.pronunciation
            if pron[-1] == "’":  # noqa: RUF001, because of Japanese.
                mora_text = pron[:-1]
            elif pron == "ー":
                # NOTE: VOICEVOX losts prolonged sound mark. Only realized phonemes remain.
                mora_text = _aiueo_to_mora_pron(vowel)
            else:
                mora_text = pron
            vv_moras.append(
                Mora(
                    text=_replace_mora_pron(mora_text),
                    consonant=consonant,
                    consonant_length=consonant_length,
                    vowel=vowel,
                )
            )
    return vv_moras


def convert_utterance_to_voicevox_accent_phrases(
    utterance: Utterance,
) -> list[AccentPhrase]:
    """Convert utterance into VOICEVOX accent phrases."""
    vv_aps: list[AccentPhrase] = []
    for bc in utterance:
        is_tail_bc = bc == utterance[-1]
        for ap in bc.accent_phrases:
            is_tail_ap = ap == bc.accent_phrases[-1]
            # NOTE: VOICEVOX delete utterance tail pause.
            with_pau = is_tail_ap and not is_tail_bc
            vv_aps.append(
                AccentPhrase(
                    _convert_words_to_voicevox_moras(ap.words),
                    accent=ap.accent,
                    pause_mora=_gen_pau_mora() if with_pau else None,
                    is_interrogative=ap.interrogative,
                )
            )
    return vv_aps
