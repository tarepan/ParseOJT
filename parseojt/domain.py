"""SpeechTree tree elements."""

from dataclasses import dataclass
from typing import Final, Literal

from .utils import get_args

# fmt: off
# NOTE: Same as Open JTalk. ref: https://github.com/r9y9/open_jtalk/blob/462fc38e7520aa89e4d32b2611749208528c901e/src/jpcommon/jpcommon_rule_utf_8.h#L63-L236
type ConsonantSymbol = Literal["k", "ky", "kw", "g", "gy", "gw", "s", "sh", "z", "j", "t", "ch", "ts", "ty", "d", "dy", "n", "ny", "h", "hy", "f", "b", "by", "p", "py", "m", "my", "y", "r", "ry", "w", "v"]
type VowelSymbol = Literal["a", "A", "i", "I", "u", "U", "e", "E", "o", "O", "N", "cl", "pau"]  # NOTE: "A/I/U/E/O" is 無声化母音, "N" is 撥音, "cl" is 促音, "pau" is 無音.
type PhonemeSymbol = ConsonantSymbol | VowelSymbol
CONSONANT_SYMBOLS: Final[tuple[ConsonantSymbol, ...]] = get_args(ConsonantSymbol)
VOWEL_SYMBOLS: Final[tuple[VowelSymbol, ...]] = get_args(VowelSymbol)
PHONEME_SYMBOLS: Final[tuple[PhonemeSymbol, ...]] = CONSONANT_SYMBOLS + VOWEL_SYMBOLS
# fmt: on


@dataclass(frozen=True)
class Phoneme:
    """音素。"""

    # NOTE: abbreviated as "PN/pn"

    symbol: PhonemeSymbol


@dataclass(frozen=True)
class Consonant(Phoneme):
    """子音の音素。"""

    # NOTE: abbreviated as "C/c"

    symbol: ConsonantSymbol


@dataclass(frozen=True)
class Vowel(Phoneme):
    """母音の音素。"""

    # NOTE: abbreviated as "V/v"

    symbol: VowelSymbol


@dataclass(frozen=True)
class Mora:
    """モーラ。"""

    # NOTE: abbreviated as "MR/mr"

    phonemes: tuple[Consonant, Vowel] | tuple[Vowel]
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
    interrogative: bool


@dataclass(frozen=True)
class BreathClause:
    """ブレス節。"""

    # NOTE: abbreviated as "BC/bc"

    accent_phrases: list[AccentPhrase]
    breath: Word | None  # `None` means sentence end.


type Tree = list[BreathClause]
