"""VOICEVOX structures."""

from dataclasses import dataclass


@dataclass
class Mora:
    """VOICEVOX モーラ。"""

    text: str
    consonant: str | None
    consonant_length: float | None
    vowel: str
    vowel_length: float = 0
    pitch: float = 0


@dataclass
class AccentPhrase:
    """VOICEVOX アクセント句。"""

    moras: list[Mora]
    accent: int
    pause_mora: Mora | None
    is_interrogative: bool
