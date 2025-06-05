"""SpeechTree tree and its elements."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Phoneme:
    """
    音素。

    種類を表すシンボルと、無声化の有無を表すフラグからなる。
    """

    # NOTE: abbreviated as "PN/pn"

    symbol: str
    unvoicing: bool = False


@dataclass
class Mora:
    """
    モーラ。

    モーラを構成する音素列と、モーラの音をカタカナ表記した発音からなる。
    発音はカタカナ列・全角長音・全角空白で表現される。
    発音の一例として、「ア」「キャ」「ー」「　」が挙げられる。
    """

    # NOTE: abbreviated as "MR/mr"

    phonemes: tuple[Phoneme, Phoneme] | tuple[Phoneme]  # CV | V
    pronunciation: str


@dataclass
class Word:
    """
    ワード。

    単体で意味を持つ言葉。
    ワードを構成するモーラ列と、ワードを表現する自然言語のテキストからなる。
    """

    # NOTE: abbreviated as "WD/wd"

    moras: list[Mora]
    text: str


@dataclass
class AccentPhrase:
    """
    アクセント句。

    単一のアクセントを持つひと続きのワード。
    アクセント句を構成するワード列と、句内でのアクセント位置からなる。
    """

    # NOTE: abbreviated as "AP/ap"

    words: list[Word]
    accent: int


@dataclass
class PhraseGroup:
    """
    フレーズグループ。

    ひと続きのアクセント句。
    グループを構成するアクセント句の列と、グループの種類を表現するタイプからなる。
    """

    # NOTE: abbreviated as "PG/pg"
    # NOTE: Intended to be used as inheritance super class. Not intended to be instantiated directly.

    accent_phrases: list[AccentPhrase]
    type: Literal["BreathGroup", "MarkGroup"]


@dataclass
class BreathGroup(PhraseGroup):
    """
    ブレスグループ。

    一息で発声されるひと続きのアクセント句。
    一例として、「今日はいい天気ですね。」のうち「今日はいい天気ですね」が1つのブレスグループに属する。
    """

    # NOTE: abbreviated as "BG/bg"

    type: Literal["BreathGroup"] = "BreathGroup"


@dataclass
class MarkGroup(PhraseGroup):
    """
    マークグループ。

    発声されないひと続きのアクセント句。
    一例として、「それホント！？　うゎマジか」のうち「！？　」が1つのマークグループに属する。
    """

    # NOTE: abbreviated as "MG/mg"

    type: Literal["MarkGroup"] = "MarkGroup"


type Tree = list[BreathGroup | MarkGroup]
