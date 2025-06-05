"""Test Open JTalk feature loader."""

import pyopenjtalk  # type: ignore # noqa: PGH003, because of external library's type missing

from speechtree.ojt.loader import as_ojt_features


def test_as_ojt_features() -> None:
    """`as_ojt_features()` can parse `pyopenjtalk.run_frontend()` output."""
    # Inputs
    text = "こんにちは、OpenJTalk のパーサーです。"
    raw_features = pyopenjtalk.run_frontend(text)
    # Expects
    true_n_feat = 8
    # Outputs & Tests
    ojt_feats = as_ojt_features(raw_features)
    n_feat = len(ojt_feats)
    assert n_feat == true_n_feat
