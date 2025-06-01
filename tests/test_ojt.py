"""Tests Open JTalk structures."""

import pyopenjtalk  # type: ignore # noqa: PGH003, because of external library's type missing

from parseojt.ojt import as_ojt_feats


def test_as_ojt_feats() -> None:
    """`as_ojt_feats()` can parse `pyopenjtalk.run_frontend()` output."""
    # Inputs
    text = "こんにちは、OpenJTalk のパーサーです。"
    raw_features = pyopenjtalk.run_frontend(text)
    # Expects
    true_n_feat = 8
    # Outputs & Tests
    ojt_feats = as_ojt_feats(raw_features)
    n_feat = len(ojt_feats)
    assert n_feat == true_n_feat
