"""SpeechTree tree elements."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Phoneme:
    """音素。"""

    # NOTE: abbreviated as "PN/pn"

    symbol: str
    unvoicing: bool = False


@dataclass(frozen=True)
class Mora:
    """モーラ。"""

    # NOTE: abbreviated as "MR/mr"

    phonemes: tuple[Phoneme, Phoneme] | tuple[Phoneme]  # CV | V
    pronunciation: str


@dataclass(frozen=True)
class Word:
    """ワード。"""

    # NOTE: abbreviated as "WD/wd"

    moras: list[Mora]
    text: str


@dataclass(frozen=True)
class AccentPhrase:
    """アクセント句。"""

    # NOTE: abbreviated as "AP/ap"

    words: list[Word]
    accent: int


# PhraseGroup
@dataclass(frozen=True)
class Group:
    """グループ。"""

    # NOTE: abbreviated as "Gp/gp"

    accent_phrases: list[AccentPhrase]


@dataclass(frozen=True)
class BreathGroup(Group):
    """ブレスグループ。"""

    # NOTE: abbreviated as "BG/bg"


@dataclass(frozen=True)
class MarkGroup(Group):
    """マークグループ。"""

    # NOTE: abbreviated as "MG/mg"


type Tree = list[BreathGroup | MarkGroup]
