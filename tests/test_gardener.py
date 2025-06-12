"""Test garderner tools."""

from speechtree.gardener import extract_accent_position
from speechtree.tree import AccentPhrase, Mora, Phoneme, Word


def test_extract_accent_position() -> None:
    # Inputs
    # fmt: off
    ap = AccentPhrase(
        words=[
            Word(moras=[
                    Mora(phonemes=(
                            Phoneme(symbol="k", unvoicing=False),
                            Phoneme(symbol="o", unvoicing=False),
                        ), pronunciation="コ", tone_high=False),
                    Mora(phonemes=(
                            Phoneme(symbol="N", unvoicing=False),
                        ), pronunciation="ン", tone_high=True),
                    Mora(phonemes=(
                            Phoneme(symbol="n", unvoicing=False),
                            Phoneme(symbol="i", unvoicing=False),
                        ), pronunciation="ニ", tone_high=True),
                    Mora(phonemes=(
                            Phoneme(symbol="ch", unvoicing=False),
                            Phoneme(symbol="i", unvoicing=False),
                        ), pronunciation="チ", tone_high=True),
                    Mora(phonemes=(
                            Phoneme(symbol="w", unvoicing=False),
                            Phoneme(symbol="a", unvoicing=False),
                        ), pronunciation="ワ", tone_high=True),
                    Mora(phonemes=(
                            Phoneme(symbol="d", unvoicing=False),
                            Phoneme(symbol="e", unvoicing=False),
                        ), pronunciation="デ", tone_high=False),
                    Mora(phonemes=(
                            Phoneme(symbol="s", unvoicing=False),
                            Phoneme(symbol="U", unvoicing=False),
                        ), pronunciation="ス", tone_high=False),
                ], text="こんにちはです"),
        ]
    )
    # fmt: on
    # Outputs
    accent = extract_accent_position(ap)
    # Expects
    true_accent = 5

    # Tests
    assert accent == true_accent
