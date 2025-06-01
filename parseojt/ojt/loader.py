"""Open JTalk raw feature parser."""

from typing import Any

from pydantic import TypeAdapter

from .domain import OjtFeature

_feat_adapter = TypeAdapter(OjtFeature)


def as_ojt_features(features: Any) -> list[OjtFeature]:  # noqa: ANN401, because this is validator
    """Type and validate raw Open JTalk NJD features."""
    return list(map(_feat_adapter.validate_python, features))
