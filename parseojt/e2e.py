"""End-to-End converter."""
# NOTE: Should not implement conversion algorithms here.

from typing import Any

from .domain import Tree
from .ojt.loader import as_ojt_features
from .parser import parse_ojt_as_tree
from .voicevox.converter import convert_tree_to_voicevox_accent_phrases
from .voicevox.domain import AccentPhrase


def ojt_raw_features_to_tree(raw_features: Any) -> Tree:  # noqa: ANN401, because this function works as validator
    """Convert raw Open JTalk text-processing features into a hierarchical utterance."""
    ojt_feats = as_ojt_features(raw_features)
    return parse_ojt_as_tree(ojt_feats)


def ojt_raw_features_to_vv_accent_phrases(raw_features: Any) -> list[AccentPhrase]:  # noqa: ANN401, because this function works as validator
    """Convert raw Open JTalk text-processing features into VOICEVOX accent phrases."""
    tree = ojt_raw_features_to_tree(raw_features)
    return convert_tree_to_voicevox_accent_phrases(tree)
