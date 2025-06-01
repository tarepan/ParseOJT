"""
parseOJT structures.

OJT から取り込む情報とその根拠:
  - string: 読み上げたい書き文字テキストであり、原文の情報として必要。
  - pron: 読み上げるときの音の種類であり、主要な音声情報として必要。なお、string から簡単にはわからない。
  - acc: 読み上げるときの音の高さであり、主要な音声情報として必要。なお、string から簡単にはわからない。
  - chain_flag: アクセント句化の指示であり、アクセント句への構造化に必要。なお、最終的にはフラグ値としては不要。
"""

from dataclasses import dataclass
from typing import Final, Literal

from .utils import get_args

# fmt: off

# NOTE: Same as Open JTalk. ref: https://github.com/tarepan/analysis_open_jtalk/blob/9584d4271dd8af213da687b30f327593d979246b/src/jpcommon/jpcommon_rule_utf_8.h#L63-L236
# NOTE: "N" is 撥音, "cl" is 促音.
type ConsonantSymbol = Literal["k", "ky", "kw", "g", "gy", "gw", "s", "sh", "z", "j", "t", "ch", "ts", "ty", "d", "dy", "n", "ny", "h", "hy", "f", "b", "by", "p", "py", "m", "my", "y", "r", "ry", "w", "v"]
type VowelSymbol = Literal["a", "A", "i", "I", "u", "U", "e", "E", "o", "O", "N", "cl", "pau"]
type PhonemeSymbol = ConsonantSymbol | VowelSymbol
CONSONANT_SYMBOLS: Final[tuple[ConsonantSymbol, ...]] = get_args(ConsonantSymbol)
VOWEL_SYMBOLS: Final[tuple[VowelSymbol, ...]] = get_args(VowelSymbol)

type MoraPronunciation = Literal["ヴョ", "ヴュ", "ヴャ", "ヴォ", "ヴェ", "ヴィ", "ヴァ", "ヴ", "ン", "ヲ", "ヱ", "ヰ", "ワ", "ヮ", "ロ", "レ", "ル", "リョ", "リュ", "リャ", "リェ", "リ", "ラ", "ヨ", "ョ", "ユ", "ュ", "ヤ", "ャ", "モ", "メ", "ム", "ミョ", "ミュ", "ミャ", "ミェ", "ミ", "マ", "ポ", "ボ", "ホ", "ペ", "ベ", "ヘ", "プ", "ブ", "フォ", "フェ", "フィ", "ファ", "フ", "ピョ", "ピュ", "ピャ", "ピェ", "ピ", "ビョ", "ビュ", "ビャ", "ビェ", "ビ", "ヒョ", "ヒュ", "ヒャ", "ヒェ", "ヒ", "パ", "バ", "ハ", "ノ", "ネ", "ヌ", "ニョ", "ニュ", "ニャ", "ニェ", "ニ", "ナ", "ドゥ", "ド", "トゥ", "ト", "デョ", "デュ", "デャ", "ディ", "デ", "テョ", "テュ", "テャ", "ティ", "テ", "ヅ", "ツォ", "ツェ", "ツィ", "ツァ", "ツ", "ッ", "ヂ", "チョ", "チュ", "チャ", "チェ", "チ", "ダ", "タ", "ゾ", "ソ", "ゼ", "セ", "ズィ", "ズ", "スィ", "ス", "ジョ", "ジュ", "ジャ", "ジェ", "ジ", "ショ", "シュ", "シャ", "シェ", "シ", "ザ", "サ", "ゴ", "コ", "ゲ", "ケ", "ヶ", "グヮ", "グ", "クヮ", "ク", "ギョ", "ギュ", "ギャ", "ギェ", "ギ", "キョ", "キュ", "キャ", "キェ", "キ", "ガ", "カ", "オ", "ォ", "エ", "ェ", "ウォ", "ウェ", "ウィ", "ウ", "ゥ", "イェ", "イ", "ィ", "ア", "ァ"]
# type  = MoraSymbol | Literal["ー"]

# Mora-Consonant/Vowel mapping
MR_CV: Final[dict[MoraPronunciation, tuple[ConsonantSymbol | None, VowelSymbol]]] = {
    "ヴョ": ("by", "o"),
    "ヴュ": ("by", "u"),
    "ヴャ": ("by", "a"),
    "ヴォ": ("v",  "o"),
    "ヴェ": ("v",  "e"),
    "ヴィ": ("v",  "i"),
    "ヴァ": ("v",  "a"),
    "ヴ":   ("v",  "u"),
    "ン":   (None, "N"),
    "ヲ":   (None, "o"),
    "ヱ":   (None, "e"),
    "ヰ":   (None, "i"),
    "ワ":   ("w",  "a"),
    "ヮ":   ("w",  "a"),
    "ロ":   ("r",  "o"),
    "レ":   ("r",  "e"),
    "ル":   ("r",  "u"),
    "リョ": ("ry", "o"),
    "リュ": ("ry", "u"),
    "リャ": ("ry", "a"),
    "リェ": ("ry", "e"),
    "リ":   ("r",  "i"),
    "ラ":   ("r",  "a"),
    "ヨ":   ("y",  "o"),
    "ョ":   ("y",  "o"),
    "ユ":   ("y",  "u"),
    "ュ":   ("y",  "u"),
    "ヤ":   ("y",  "a"),
    "ャ":   ("y",  "a"),
    "モ":   ("m",  "o"),
    "メ":   ("m",  "e"),
    "ム":   ("m",  "u"),
    "ミョ": ("my", "o"),
    "ミュ": ("my", "u"),
    "ミャ": ("my", "a"),
    "ミェ": ("my", "e"),
    "ミ":   ("m",  "i"),
    "マ":   ("m",  "a"),
    "ポ":   ("p",  "o"),
    "ボ":   ("b",  "o"),
    "ホ":   ("h",  "o"),
    "ペ":   ("p",  "e"),
    "ベ":   ("b",  "e"),
    "ヘ":   ("h",  "e"),
    "プ":   ("p",  "u"),
    "ブ":   ("b",  "u"),
    "フォ": ("f",  "o"),
    "フェ": ("f",  "e"),
    "フィ": ("f",  "i"),
    "ファ": ("f",  "a"),
    "フ":   ("f",  "u"),
    "ピョ": ("py", "o"),
    "ピュ": ("py", "u"),
    "ピャ": ("py", "a"),
    "ピェ": ("py", "e"),
    "ピ":   ("p",  "i"),
    "ビョ": ("by", "o"),
    "ビュ": ("by", "u"),
    "ビャ": ("by", "a"),
    "ビェ": ("by", "e"),
    "ビ":   ("b",  "i"),
    "ヒョ": ("hy", "o"),
    "ヒュ": ("hy", "u"),
    "ヒャ": ("hy", "a"),
    "ヒェ": ("hy", "e"),
    "ヒ":   ("h",  "i"),
    "パ":   ("p",  "a"),
    "バ":   ("b",  "a"),
    "ハ":   ("h",  "a"),
    "ノ":   ("n",  "o"),
    "ネ":   ("n",  "e"),
    "ヌ":   ("n",  "u"),
    "ニョ": ("ny", "o"),
    "ニュ": ("ny", "u"),
    "ニャ": ("ny", "a"),
    "ニェ": ("ny", "e"),
    "ニ":   ("n",  "i"),
    "ナ":   ("n",  "a"),
    "ドゥ": ("d",  "u"),
    "ド":   ("d",  "o"),
    "トゥ": ("t",  "u"),
    "ト":   ("t",  "o"),
    "デョ": ("dy", "o"),
    "デュ": ("dy", "u"),
    "デャ": ("dy", "a"),
    "ディ": ("d",  "i"),
    "デ":   ("d",  "e"),
    "テョ": ("ty", "o"),
    "テュ": ("ty", "u"),
    "テャ": ("ty", "a"),
    "ティ": ("t",  "i"),
    "テ":   ("t",  "e"),
    "ヅ":   ("z",  "u"),
    "ツォ": ("ts", "o"),
    "ツェ": ("ts", "e"),
    "ツィ": ("ts", "i"),
    "ツァ": ("ts", "a"),
    "ツ":   ("ts", "u"),
    "ッ":   (None, "cl"),
    "ヂ":   ("j",  "i"),
    "チョ": ("ch", "o"),
    "チュ": ("ch", "u"),
    "チャ": ("ch", "a"),
    "チェ": ("ch", "e"),
    "チ":   ("ch", "i"),
    "ダ":   ("d",  "a"),
    "タ":   ("t",  "a"),
    "ゾ":   ("z",  "o"),
    "ソ":   ("s",  "o"),
    "ゼ":   ("z",  "e"),
    "セ":   ("s",  "e"),
    "ズィ": ("z",  "i"),
    "ズ":   ("z",  "u"),
    "スィ": ("s",  "i"),
    "ス":   ("s",  "u"),
    "ジョ": ("j",  "o"),
    "ジュ": ("j",  "u"),
    "ジャ": ("j",  "a"),
    "ジェ": ("j",  "e"),
    "ジ":   ("j",  "i"),
    "ショ": ("sh", "o"),
    "シュ": ("sh", "u"),
    "シャ": ("sh", "a"),
    "シェ": ("sh", "e"),
    "シ":   ("sh", "i"),
    "ザ":   ("z",  "a"),
    "サ":   ("s",  "a"),
    "ゴ":   ("g",  "o"),
    "コ":   ("k",  "o"),
    "ゲ":   ("g",  "e"),
    "ケ":   ("k",  "e"),
    "ヶ":   ("k",  "e"),
    "グヮ": ("gw", "a"),
    "グ":   ("g",  "u"),
    "クヮ": ("kw", "a"),
    "ク":   ("k",  "u"),
    "ギョ": ("gy", "o"),
    "ギュ": ("gy", "u"),
    "ギャ": ("gy", "a"),
    "ギェ": ("gy", "e"),
    "ギ":   ("g",  "i"),
    "キョ": ("ky", "o"),
    "キュ": ("ky", "u"),
    "キャ": ("ky", "a"),
    "キェ": ("ky", "e"),
    "キ":   ("k",  "i"),
    "ガ":   ("g",  "a"),
    "カ":   ("k",  "a"),
    "オ":   (None, "o"),
    "ォ":   (None, "o"),
    "エ":   (None, "e"),
    "ェ":   (None, "e"),
    "ウォ": ("w",  "o"),
    "ウェ": ("w",  "e"),
    "ウィ": ("w",  "i"),
    "ウ":   (None, "u"),
    "ゥ":   (None, "u"),
    "イェ": ("y",  "e"),
    "イ":   (None, "i"),
    "ィ":   (None, "i"),
    "ア":   (None, "a"),
    "ァ":   (None, "a"),
}
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


type Utterance = list[BreathClause]
