"""Test e2e Open Jtalk to VOICEVOX conversion."""

import pyopenjtalk  # type: ignore # noqa: PGH003, because of external library's type missing

from speechtree.e2e import ojt_raw_features_to_vv_accent_phrases
from speechtree.voicevox.domain import AccentPhrase as VVAccentPhrase
from speechtree.voicevox.domain import Mora as VVMora


def test_ojt_raw_features_to_vv_accent_phrases_valid_text() -> None:
    # NOTE:
    # 以下の要素を正しい形で含む:
    #   - 複数種類の pau 要素。「、」「。」「？」「 」「末尾の『。』」
    #   - 無声化。「です de sU」
    #   - 長音。「ー」
    #   - アルファベット。「SpeechTree」
    text = "あぁ、どうもこんにちはです。おや？今日は綺麗な鞄をお持ちですね、SpeechTreeの ブランド品 ですかー。"
    raw_features = pyopenjtalk.run_frontend(text)
    # vv_aps
    vv_aps = ojt_raw_features_to_vv_accent_phrases(raw_features)

    # Expects
    # NOTE: Generated at VOICEVOX ENGINE at VOICEVOX ENGINE bb42ad73e337872c81514f7f6cd80e195384e96d. Code is below:
    # ```python
    # from voicevox_engine.tts_pipeline.njd_feature_processor import text_to_full_context_labels
    # from voicevox_engine.tts_pipeline.text_analyzer import full_context_labels_to_accent_phrases
    #
    # def test_ap() -> None:
    #     text = "あぁ、どうもこんにちはです。おや？今日は綺麗な鞄をお持ちですね、SpeechTreeの ブランド品 ですかー。"
    #     full_context_labels = text_to_full_context_labels(text, enable_e2k=False)
    #     accent_phrases = full_context_labels_to_accent_phrases(full_context_labels)
    #
    #     print(accent_phrases)
    #     assert False
    # ```
    true_vv_aps = [
        VVAccentPhrase(
            moras=[
                VVMora("ア", None, None, "a", 0.0, 0.0),
                VVMora("ア", None, None, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("ド", "d", 0.0, "o", 0.0, 0.0),
                VVMora("オ", None, None, "o", 0.0, 0.0),
                VVMora("モ", "m", 0.0, "o", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("コ", "k", 0.0, "o", 0.0, 0.0),
                VVMora("ン", None, None, "N", 0.0, 0.0),
                VVMora("ニ", "n", 0.0, "i", 0.0, 0.0),
                VVMora("チ", "ch", 0.0, "i", 0.0, 0.0),
                VVMora("ワ", "w", 0.0, "a", 0.0, 0.0),
                VVMora("デ", "d", 0.0, "e", 0.0, 0.0),
                VVMora("ス", "s", 0.0, "U", 0.0, 0.0),
            ],
            accent=7,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("オ", None, None, "o", 0.0, 0.0),
                VVMora("ヤ", "y", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=True,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("キョ", "ky", 0.0, "o", 0.0, 0.0),
                VVMora("オ", None, None, "o", 0.0, 0.0),
                VVMora("ワ", "w", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("キ", "k", 0.0, "i", 0.0, 0.0),
                VVMora("レ", "r", 0.0, "e", 0.0, 0.0),
                VVMora("エ", None, None, "e", 0.0, 0.0),
                VVMora("ナ", "n", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("カ", "k", 0.0, "a", 0.0, 0.0),
                VVMora("バ", "b", 0.0, "a", 0.0, 0.0),
                VVMora("ン", None, None, "N", 0.0, 0.0),
                VVMora("オ", None, None, "o", 0.0, 0.0),
            ],
            accent=4,
            pause_mora=None,
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("オ", None, None, "o", 0.0, 0.0),
                VVMora("モ", "m", 0.0, "o", 0.0, 0.0),
                VVMora("チ", "ch", 0.0, "i", 0.0, 0.0),
                VVMora("デ", "d", 0.0, "e", 0.0, 0.0),
                VVMora("ス", "s", 0.0, "U", 0.0, 0.0),
                VVMora("ネ", "n", 0.0, "e", 0.0, 0.0),
            ],
            accent=6,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("エ", None, None, "e", 0.0, 0.0),
                VVMora("ス", "s", 0.0, "u", 0.0, 0.0),
                VVMora("ピ", "p", 0.0, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("シ", "sh", 0.0, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("エ", None, None, "e", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("チ", "ch", 0.0, "i", 0.0, 0.0),
                VVMora("ティ", "t", 0.0, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("ア", None, None, "a", 0.0, 0.0),
                VVMora("ア", None, None, "a", 0.0, 0.0),
                VVMora("ル", "r", 0.0, "u", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("イ", None, None, "i", 0.0, 0.0),
                VVMora("ノ", "n", 0.0, "o", 0.0, 0.0),
            ],
            accent=23,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("ブ", "b", 0.0, "u", 0.0, 0.0),
                VVMora("ラ", "r", 0.0, "a", 0.0, 0.0),
                VVMora("ン", None, None, "N", 0.0, 0.0),
                VVMora("ド", "d", 0.0, "o", 0.0, 0.0),
                VVMora("ヒ", "h", 0.0, "i", 0.0, 0.0),
                VVMora("ン", None, None, "N", 0.0, 0.0),
            ],
            accent=4,
            pause_mora=VVMora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        VVAccentPhrase(
            moras=[
                VVMora("デ", "d", 0.0, "e", 0.0, 0.0),
                VVMora("ス", "s", 0.0, "U", 0.0, 0.0),
                VVMora("カ", "k", 0.0, "a", 0.0, 0.0),
                VVMora("ア", None, None, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
    ]

    assert vv_aps == true_vv_aps
