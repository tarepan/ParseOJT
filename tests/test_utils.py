
from typing import Final, Literal

from parseojt.utils import get_args


def test_get_args_literal_alias() -> None:
    """`get_args()` can extract literal's type arguments."""
    # Inputs
    type VowelSymbol = Literal["a", "A", "i", "I", "u", "pau"]
    # Outputs
    VOWEL_SYMBOLS: Final[tuple[VowelSymbol, ...]] = get_args(VowelSymbol)
    # Expects
    TRUE_VOWEL_SYMBOLS = ("a", "A", "i", "I", "u", "pau")

    # Tests
    assert VOWEL_SYMBOLS == TRUE_VOWEL_SYMBOLS
