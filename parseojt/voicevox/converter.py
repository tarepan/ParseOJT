"""Utterance-To-VOICEVOX converter."""

from parseojt.domain import Utterance
from parseojt.voicevox.domain import AccentPhrase


def convert_utterance_to_accent_phrases(utterance: Utterance) -> list[AccentPhrase]:
    """VV parser."""
    _ = utterance
    return [AccentPhrase(["mora1"])]
