"""Tests Open JTalk structures."""

import pyopenjtalk  # type: ignore # noqa: PGH003

from parseojt.ojt import as_ojt_words


def test_ojt_word() -> None:
    """`OjtWord` can be initialized with `pyopenjtalk.run_frontend()` output."""
    # Inputs
    text = "こんにちは、OpenJTalk のパーサーです。"
    features = pyopenjtalk.run_frontend(text)
    # Expects
    true_n_word = 8
    # Outputs & Tests
    ojt_words = as_ojt_words(features)
    n_word = len(ojt_words)
    assert n_word == true_n_word
