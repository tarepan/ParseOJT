"""Characters."""

import re
from itertools import groupby
from typing import Final, Literal

from speechtree.utils import get_args

# fmt: off
# NOTE: Same as Open JTalk. ref: https://github.com/r9y9/open_jtalk/blob/462fc38e7520aa89e4d32b2611749208528c901e/src/jpcommon/jpcommon_rule_utf_8.h#L63-L236
type ConsonantSymbol = Literal["k", "ky", "kw", "g", "gy", "gw", "s", "sh", "z", "j", "t", "ch", "ts", "ty", "d", "dy", "n", "ny", "h", "hy", "f", "b", "by", "p", "py", "m", "my", "y", "r", "ry", "w", "v"]
type VowelSymbol = Literal["a", "A", "i", "I", "u", "U", "e", "E", "o", "O", "N", "cl", "pau"]  # NOTE: "A/I/U/E/O" is 無声化母音, "N" is 撥音, "cl" is 促音, "pau" is 無音.
type PhonemeSymbol = ConsonantSymbol | VowelSymbol
CONSONANT_SYMBOLS: Final[tuple[ConsonantSymbol, ...]] = get_args(ConsonantSymbol)
VOWEL_SYMBOLS: Final[tuple[VowelSymbol, ...]] = get_args(VowelSymbol)
PHONEME_SYMBOLS: Final[tuple[PhonemeSymbol, ...]] = CONSONANT_SYMBOLS + VOWEL_SYMBOLS

# missing phonemes:
#     /hu/, /yi/, /tye/ /dye/
#     /-i/                 of  /ky-/ /gy-/ /ty-/ /dy-/ /ny-/ /hy-/ /by-/ /py-/ /my-/ /ry-/
#     /-i/ /-u/ /-e/ /-o/  of  /kw-/ /gw-/
type MoraPronunciation = Literal[
                                                                                                                           # standard        specials
    "ア", "イ", "ウ", "エ", "オ",                                                             "ァ", "ィ", "ゥ", "ェ", "ォ",  # /∅-/
    "カ", "キ", "ク", "ケ", "コ",  "ガ", "ギ", "グ", "ゲ", "ゴ",                                                 "ヶ",       # /k-/ /g-/
    "サ", "シ", "ス", "セ", "ソ",  "ザ", "ジ", "ズ", "ゼ", "ゾ",                                                             # /s-/ /z-/       シ=/shi/, ジ=/ji/
    "タ", "チ", "ツ", "テ", "ト",  "ダ", "ヂ", "ヅ", "デ", "ド",                                           "ッ",             # /t-/ /d-/       チ=/chi/, ツ=/tsu/, ヂ=/ji/, ヅ=/zu/, ッ=/∅cl/
    "ナ", "ニ", "ヌ", "ネ", "ノ",                                                                                           # /n-/                                                            # noqa: RUF001
    "ハ", "ヒ", "フ", "ヘ", "ホ",  "バ", "ビ", "ブ", "ベ", "ボ", "パ", "ピ", "プ", "ペ", "ポ",                                # /h-/ /b-/ /p-/  フ=/fu/, /hu/ missing
    "マ", "ミ", "ム", "メ", "モ",                                                                                           # /m-/
    "ヤ",       "ユ",       "ヨ",                                                             "ャ",       "ュ",       "ョ", # /y-/            /yi/ missing, /ye/ no single character
    "ラ", "リ", "ル", "レ", "ロ",                                                                                           # /r-/
    "ワ", "ヰ",       "ヱ", "ヲ",                                                             "ヮ",                         # /w-/            ヰ=/∅i/, /wu/ missing, ヱ=/∅e/, ヲ=/∅o/
    "ン",                                                                                                                  # /∅N/

            "スィ",                                  "ズィ",                                                                # /si/, /zi/,             compensatation of サ行・ザ行 specials
            "ティ", "トゥ",                          "ディ", "ドゥ",                                                        #  /ti/, /tu/, /di/, /du/, compensatation of タ行・ダ行 specials
                            "イェ",                                                                                        #  /ye/                    compensatation of ヤ行      specials
            "ウィ",         "ウェ", "ウォ",                                                                                 # /wi/, /we/, /wo/,       compensatation of ワ行      specials

                                                                                                                           # standard          specials
    "キャ",         "キュ", "キェ", "キョ",  "ギャ",         "ギュ", "ギェ", "ギョ",                                          # /ky-/ /gy-/
    "テャ",         "テュ",         "テョ",  "デャ",         "デュ",         "デョ",                                         # /ty-/ /dy-/        /tye/ missing, /dye/ missing
    "ニャ",         "ニュ", "ニェ", "ニョ",                                                                                 # /ny-/
    "ヒャ",         "ヒュ", "ヒェ", "ヒョ",  "ビャ",         "ビュ", "ビェ", "ビョ",  "ピャ",         "ピュ", "ピェ", "ピョ",  # /hy-/ /by-/ /py-/
                                            "ヴャ",        "ヴュ",         "ヴョ",                                          #                    alternative /bya/ /byu/ /byo/ expression
    "ミャ",         "ミュ", "ミェ", "ミョ",                                                                                 # /my-/
    "リャ",         "リュ", "リェ", "リョ",                                                                                 # /ry-/

    "シャ",         "シュ", "シェ", "ショ",  "ジャ",         "ジュ", "ジェ", "ジョ",                                          # /sh-/ /j-/        /shi/=シ, /ji/=ジ
    "チャ",         "チュ", "チェ", "チョ",                                                                                 # /ch-/              /chi/=チ

    "ツァ", "ツィ",         "ツェ", "ツォ",                                                                                 #  /ts-/             /tsu/=ツ
    "ファ", "フィ",         "フェ", "フォ",                                                                                 #  /f-/              /fu/=フ
    "ヴァ", "ヴィ", "ヴ",   "ヴェ", "ヴォ",                                                                                 #  /v-/
    "クヮ",                                "グヮ",                                                                         #  /kw-/ /gw-/       only /kwa/ /gwa/ exist

]


MORA_PRONUNCIATION: Final[tuple[MoraPronunciation, ...]] = get_args(MoraPronunciation)
FULL_MORA_PRONUNCIATION: Final[tuple[MoraPronunciation | Literal["ー"], ...]] = MORA_PRONUNCIATION + ("ー",)   # noqa: RUF005, because of Japanese.

# Mora-Consonant/Vowel mapping
# NOTE: Character order should be kept for mora search (longest match).
MR_CV: Final[dict[MoraPronunciation, tuple[ConsonantSymbol | None, VowelSymbol]]] = {
    "ヴョ": ("by", "o"), # NOTE: same phonemes as `ビョ`
    "ヴュ": ("by", "u"), # NOTE: same phonemes as `ビュ`
    "ヴャ": ("by", "a"), # NOTE: same phonemes as `ビャ`
    "ヴォ": ("v",  "o"),
    "ヴェ": ("v",  "e"),
    "ヴィ": ("v",  "i"),
    "ヴァ": ("v",  "a"),
    "ヴ":   ("v",  "u"),
    "ン":   (None, "N"),
    "ヲ":   (None, "o"), # NOTE: same phonemes as `オ`
    "ヱ":   (None, "e"), # NOTE: same phonemes as `エ`
    "ヰ":   (None, "i"), # NOTE: same phonemes as `イ`
    "ワ":   ("w",  "a"),
    "ヮ":   ("w",  "a"), # NOTE: same phonemes as `ワ`
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
    "ョ":   ("y",  "o"), # NOTE: same phonemes as `ヨ`
    "ユ":   ("y",  "u"),
    "ュ":   ("y",  "u"), # NOTE: same phonemes as `ユ`
    "ヤ":   ("y",  "a"),
    "ャ":   ("y",  "a"), # NOTE: same phonemes as `ヤ`
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
    "ノ":   ("n",  "o"),  # noqa: RUF001, because this is Japanese.
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
    "ヅ":   ("z",  "u"), # NOTE: same phonemes as `ズ`
    "ツォ": ("ts", "o"),
    "ツェ": ("ts", "e"),
    "ツィ": ("ts", "i"),
    "ツァ": ("ts", "a"),
    "ツ":   ("ts", "u"),
    "ッ":   (None, "cl"),
    "ヂ":   ("j",  "i"), # NOTE: same phonemes as `ジ`
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
    "ヶ":   ("k",  "e"), # NOTE: same phonemes as `ケ`
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
    "ォ":   (None, "o"), # NOTE: same phonemes as `オ`
    "エ":   (None, "e"),
    "ェ":   (None, "e"), # NOTE: same phonemes as `エ`
    "ウォ": ("w",  "o"),
    "ウェ": ("w",  "e"),
    "ウィ": ("w",  "i"),
    "ウ":   (None, "u"),
    "ゥ":   (None, "u"), # NOTE: same phonemes as `ウ`
    "イェ": ("y",  "e"),
    "イ":   (None, "i"),
    "ィ":   (None, "i"), # NOTE: same phonemes as `イ`
    "ア":   (None, "a"),
    "ァ":   (None, "a"), # NOTE: same phonemes as `ア`
}
# fmt: on


def _generate_mora_match_pattern(mora_simbols: tuple[str, ...]) -> re.Pattern[str]:
    """Generate a mora-match pattern."""
    _size_ordered_simbols = sorted(mora_simbols, key=len, reverse=True)
    _n_length_groups = [list(group) for _, group in groupby(_size_ordered_simbols, len)]
    _pattern = "、|？|ー"  # noqa: RUF001, because of Japanese.
    for i_length_group in _n_length_groups:
        for simbol in [m + "’" for m in i_length_group] + i_length_group:  # noqa: RUF001, because of Japanese.
            _pattern += f"|{simbol}"
    return re.compile(_pattern)


MORA_MATCH_PATTERN: Final = _generate_mora_match_pattern(MORA_PRONUNCIATION)
