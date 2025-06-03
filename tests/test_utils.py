"""Test utilities."""

from typing import Final, Literal

from parseojt.utils import get_args


def test_get_args_literal_alias() -> None:
    """`get_args()` can extract literal's type arguments."""
    # Inputs
    type VowelSymbol = Literal["a", "A", "i", "I", "u", "pau"]
    # Outputs
    vowel_symbols: Final[tuple[VowelSymbol, ...]] = get_args(VowelSymbol)
    # Expects
    true__vowel_symbols = ("a", "A", "i", "I", "u", "pau")

    # Tests
    assert vowel_symbols == true__vowel_symbols
