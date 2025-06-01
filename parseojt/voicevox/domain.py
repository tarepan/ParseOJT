"""VOICEVOX structures."""

from dataclasses import dataclass


@dataclass
class AccentPhrase:
    """VOICEVOX AccentPharase."""

    moras: list[str]
