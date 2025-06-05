"""Test Open JTalk feature parser."""

from speechtree.ojt.domain import OjtFeature
from speechtree.ojt.parser import parse_ojt_as_tree


def _gen_ft(
    string: str = "text",
    pron: str = "ハツオン",
    acc: int = 0,
    *,
    chain_flag: bool = True,
) -> OjtFeature:
    return OjtFeature(
        string=string,
        pos="*",
        pos_group1="*",
        pos_group2="*",
        pos_group3="*",
        ctype="*",
        cform="*",
        orig="*",
        read="*",
        pron=pron,
        acc=acc,
        mora_size=3,
        chain_rule="*",
        chain_flag=chain_flag,
    )


def test_parse_ojt_features() -> None:
    # Inputs
    # fmt: off
    ojt_feats = [
        #       string       pron:        acc chain_flag
        _gen_ft("こんにちは", "コンニチワ",  2, chain_flag=False),
        _gen_ft("、",        "、",          0, chain_flag=False),
        _gen_ft("今日は",    "キョウワ",     1, chain_flag=False),
        _gen_ft("暖かーい",  "アタタカーイ", 2,  chain_flag=True),
        _gen_ft("です",      "デス’",       0,  chain_flag=True),
        _gen_ft("？",        "？",          0, chain_flag=False),
    ]
    # fmt: on

    _ = parse_ojt_as_tree(ojt_feats)
    assert True
