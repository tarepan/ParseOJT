"""End-to-End converter."""
# NOTE: Should not implement conversion algorithms here.

from typing import Any

from .domain import Utterance
from .ojt.loader import as_ojt_features
from .parser import parse_ojt_features
from .voicevox.converter import convert_utterance_to_voicevox_accent_phrases
from .voicevox.domain import AccentPhrase


def ojt_raw_features_to_utterance(raw_features: Any) -> Utterance:  # noqa: ANN401, because this function works as validator
    """Convert raw Open JTalk text-processing features into a hierarchical utterance."""
    ojt_feats = as_ojt_features(raw_features)
    return parse_ojt_features(ojt_feats)


def ojt_raw_features_to_vv_accent_phrases(raw_features: Any) -> list[AccentPhrase]:  # noqa: ANN401, because this function works as validator
    """Convert raw Open JTalk text-processing features into VOICEVOX accent phrases."""
    utterance = ojt_raw_features_to_utterance(raw_features)
    return convert_utterance_to_voicevox_accent_phrases(utterance)
