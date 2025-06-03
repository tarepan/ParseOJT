"""Utterance-To-VOICEVOX converter."""

from parseojt.domain import Utterance, Word
from parseojt.voicevox.domain import AccentPhrase, Mora


def _gen_pau_mora() -> Mora:
    """Generate VOICEVOX pause mora."""
    # NOTE: ref: https://github.com/VOICEVOX/voicevox_engine/blob/c95bb9e387043e7f7a2eb4fd3e46692fea28716a/voicevox_engine/tts_pipeline/text_analyzer.py#L383-L391
    return Mora(
        text="、",
        consonant=None,
        consonant_length=None,
        vowel="pau",
        vowel_length=0,
        pitch=0,
    )


def _convert_words_to_voicevox_moras(words: list[Word]) -> list[Mora]:
    """Convert words into VOICEVOX moras."""
    vv_moras: list[Mora] = []
    for word in words:
        for mora in word.moras:
            phonemes = mora.phonemes
            consonant = None if len(phonemes) == 1 else phonemes[0].symbol
            consonant_length = None if len(phonemes) == 1 else 0
            vowel = phonemes[0].symbol if len(phonemes) == 1 else phonemes[1].symbol
            pron = mora.pronunciation
            if pron[-1] == "’":  # noqa: RUF001, because of Japanese.
                mora_text = pron[:-1]
            elif pron == "ー":
                mora_text = "a"
            else:
                mora_text = pron
            vv_moras.append(
                Mora(
                    text=mora_text,
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
        for ap in bc.accent_phrases:
            is_tail_ap = ap == bc.accent_phrases[-1]
            vv_aps.append(
                AccentPhrase(
                    _convert_words_to_voicevox_moras(ap.words),
                    accent=ap.accent,
                    pause_mora=_gen_pau_mora() if is_tail_ap else None,
                    is_interrogative=ap.interrogative,
                )
            )
    return vv_aps
