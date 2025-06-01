"""Open JTalk structures."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OjtFeature:
    """Open JTalk text-processing feature."""

    # NOTE:
    #   Defined as `NJDNode` by openjtalk, in https://github.com/r9y9/open_jtalk/blob/462fc38e7520aa89e4d32b2611749208528c901e/src/njd/njd.h#L56-L73.
    #   Defined as Python-style by pyopenjtalk, in https://github.com/r9y9/pyopenjtalk/blob/0f0fc44e782a8134cd9a51d80b57b48a7c95bb80/pyopenjtalk/openjtalk.pyx#L68-L84.
    #   Outputted by `pyopenjtalk.run_frontend()`.

    # fmt: off
    string: str      # 文字列                       : 表層形に相当。全角表記。例として「学校」「です」「、」「　」
    pos: str         # 品詞        part of speech   :
    pos_group1: str  # 品詞細分類1                  :
    pos_group2: str  # 品詞細分類2                  :
    pos_group3: str  # 品詞細分類3                  :
    ctype: str       # 活用型      conjugation type :
    cform: str       # 活用形      conjugation form :
    orig: str        # 原形        original form    :
    read: str        # 読み        reading          : 書き文字のカタカナ表記。例として「ガッコウ」「デス」「、」「、」
    pron: str        # 発音        pronunciation    : 読む音声の特殊カタカナ表記。例として「ガッコー」「デス’」「、」「、」 # noqa: RUF003
    acc: int         # アクセント   accent          :
    mora_size: int   # モーラ数                     :
    chain_rule: str  # 連結規則                     : 前のワードと連結してアクセント句をつくる際に句アクセントを移動する規則。
    chain_flag: int  # 連結フラグ                   : 前のワードと連結してアクセント句をつくるか否かのフラグ。-1: 未判定 / 0: 連結しない / 1: 連結する
    # fmt: on
