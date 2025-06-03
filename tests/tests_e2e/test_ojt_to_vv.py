"""Test e2e Open Jtalk to VOICEVOX conversion."""

import pyopenjtalk  # type: ignore # noqa: PGH003, because of external library's type missing

from parseojt.e2e import ojt_raw_features_to_vv_accent_phrases
from parseojt.voicevox.domain import AccentPhrase, Mora


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
        AccentPhrase(
            moras=[
                Mora("ア", None, None, "a", 0.0, 0.0),
                Mora("ア", None, None, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("ド", "d", 0.0, "o", 0.0, 0.0),
                Mora("オ", None, None, "o", 0.0, 0.0),
                Mora("モ", "m", 0.0, "o", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("コ", "k", 0.0, "o", 0.0, 0.0),
                Mora("ン", None, None, "N", 0.0, 0.0),
                Mora("ニ", "n", 0.0, "i", 0.0, 0.0),
                Mora("チ", "ch", 0.0, "i", 0.0, 0.0),
                Mora("ワ", "w", 0.0, "a", 0.0, 0.0),
                Mora("デ", "d", 0.0, "e", 0.0, 0.0),
                Mora("ス", "s", 0.0, "U", 0.0, 0.0),
            ],
            accent=7,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("オ", None, None, "o", 0.0, 0.0),
                Mora("ヤ", "y", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=True,
        ),
        AccentPhrase(
            moras=[
                Mora("キョ", "ky", 0.0, "o", 0.0, 0.0),
                Mora("オ", None, None, "o", 0.0, 0.0),
                Mora("ワ", "w", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("キ", "k", 0.0, "i", 0.0, 0.0),
                Mora("レ", "r", 0.0, "e", 0.0, 0.0),
                Mora("エ", None, None, "e", 0.0, 0.0),
                Mora("ナ", "n", 0.0, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("カ", "k", 0.0, "a", 0.0, 0.0),
                Mora("バ", "b", 0.0, "a", 0.0, 0.0),
                Mora("ン", None, None, "N", 0.0, 0.0),
                Mora("オ", None, None, "o", 0.0, 0.0),
            ],
            accent=4,
            pause_mora=None,
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("オ", None, None, "o", 0.0, 0.0),
                Mora("モ", "m", 0.0, "o", 0.0, 0.0),
                Mora("チ", "ch", 0.0, "i", 0.0, 0.0),
                Mora("デ", "d", 0.0, "e", 0.0, 0.0),
                Mora("ス", "s", 0.0, "U", 0.0, 0.0),
                Mora("ネ", "n", 0.0, "e", 0.0, 0.0),
            ],
            accent=6,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("エ", None, None, "e", 0.0, 0.0),
                Mora("ス", "s", 0.0, "u", 0.0, 0.0),
                Mora("ピ", "p", 0.0, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("シ", "sh", 0.0, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("エ", None, None, "e", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("チ", "ch", 0.0, "i", 0.0, 0.0),
                Mora("ティ", "t", 0.0, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("ア", None, None, "a", 0.0, 0.0),
                Mora("ア", None, None, "a", 0.0, 0.0),
                Mora("ル", "r", 0.0, "u", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("イ", None, None, "i", 0.0, 0.0),
                Mora("ノ", "n", 0.0, "o", 0.0, 0.0),
            ],
            accent=23,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("ブ", "b", 0.0, "u", 0.0, 0.0),
                Mora("ラ", "r", 0.0, "a", 0.0, 0.0),
                Mora("ン", None, None, "N", 0.0, 0.0),
                Mora("ド", "d", 0.0, "o", 0.0, 0.0),
                Mora("ヒ", "h", 0.0, "i", 0.0, 0.0),
                Mora("ン", None, None, "N", 0.0, 0.0),
            ],
            accent=4,
            pause_mora=Mora("、", None, None, "pau", 0.0, 0.0),
            is_interrogative=False,
        ),
        AccentPhrase(
            moras=[
                Mora("デ", "d", 0.0, "e", 0.0, 0.0),
                Mora("ス", "s", 0.0, "U", 0.0, 0.0),
                Mora("カ", "k", 0.0, "a", 0.0, 0.0),
                Mora("ア", None, None, "a", 0.0, 0.0),
            ],
            accent=1,
            pause_mora=None,
            is_interrogative=False,
        ),
    ]

    assert vv_aps == true_vv_aps
