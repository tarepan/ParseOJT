"""SpeechTree tree and its elements."""

from typing import Literal, TypedDict


class Phoneme(TypedDict):
    """
    音素。

    種類を表すシンボルと、無声化の有無を表すフラグからなる。
    """

    # NOTE: abbreviated as "PN/pn"

    symbol: str
    unvoicing: bool


class Mora(TypedDict):
    """
    モーラ。

    モーラを構成する音素列と、モーラの音をカタカナ表記した発音からなる。
    発音はカタカナ列・全角長音・全角空白で表現される。
    発音の一例として、「ア」「キャ」「ー」「　」が挙げられる。
    """

    # NOTE: abbreviated as "MR/mr"

    phonemes: tuple[Phoneme, Phoneme] | tuple[Phoneme]  # CV | V
    pronunciation: str
    tone_high: bool


class Word(TypedDict):
    """
    ワード。

    単体で意味を持つ言葉。
    ワードを構成するモーラ列と、ワードを表現する自然言語のテキストからなる。
    """

    # NOTE: abbreviated as "WD/wd"

    moras: list[Mora]
    text: str


class AccentPhrase(TypedDict):
    """
    アクセント句。

    単一のアクセントを持つひと続きのワード。
    アクセント句を構成するワード列と、句内でのアクセント位置からなる。
    """

    # NOTE: abbreviated as "AP/ap"

    words: list[Word]


class BreathGroup(TypedDict):
    """
    ブレスグループ。

    一息で発声されるひと続きのアクセント句。
    一例として、「今日はいい天気ですね。」のうち「今日はいい天気ですね」が1つのブレスグループに属する。
    """

    # NOTE: abbreviated as "BG/bg"

    accent_phrases: list[AccentPhrase]
    type: Literal["BreathGroup"]


class MarkGroup(TypedDict):
    """
    マークグループ。

    発声されないひと続きのアクセント句。
    一例として、「それホント！？　うゎマジか」のうち「！？　」が1つのマークグループに属する。
    """

    # NOTE: abbreviated as "MG/mg"

    accent_phrases: list[AccentPhrase]
    type: Literal["MarkGroup"]


# フレーズグループ。ひと続きのアクセント句。グループを構成するアクセント句の列 `accent_phrases` と、グループの種類を表現するタイプ `type` からなる。
type PhraseGroup = BreathGroup | MarkGroup
"""
フレーズグループ。

ひと続きのアクセント句。
グループを構成するアクセント句の列 `accent_phrases` と、グループの種類を表現するタイプ `type` からなる。
"""
# NOTE: abbreviated as "PG/pg"


type Tree = list[PhraseGroup]
"""
ツリー。

ブレスグループとマークグループが必ず交互に配置された列。先頭と末尾にグループ種別の制限は無い。
"""
