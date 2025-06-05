"""Utilities."""

from typing import Any, TypeAliasType
from typing import get_args as built_in_get_args


def get_args(literal_type_obj: TypeAliasType) -> tuple[Any, ...]:
    """Get type arguments."""
    # NOTE: Tests guarantees type-tuple exact matching.
    return built_in_get_args(literal_type_obj.__value__)
