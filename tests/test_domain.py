from parseojt.domain import AccentPhrase, BreathClause, Consonant, Mora, Utterance, Vowel, Word


def test_utterance_init() -> None:
    """Utterance can be initialized."""
    # Outputs & Tests
    # NOTE: text is `あら？どうもこんにちは、パンダ先生`
    uttr: Utterance = [
        BreathClause(
            [
                AccentPhrase(
                    [
                        Word(
                            [
                                Mora((Vowel("a"),), "ア"),
                                Mora((Consonant("r"), Vowel("a"),), "ラ"),
                            ],
                            "あら",
                        )
                    ],
                    accent=0,
                    interrogative=True,
                ),
            ],
            breath=Word(
                moras=[
                    Mora(
                        phonemes=(Vowel(symbol="pau"),),
                        pronunciation="、",
                    )
                ],
                text="？",
            ),
        ),
        BreathClause(
            accent_phrases=[
                AccentPhrase(
                    [
                        Word(
                            [
                                Mora((Consonant("d"), Vowel("o"),), "ド"),
                                Mora((Vowel("o"),), "ー"),
                                Mora((Consonant("m"), Vowel("o"),), "モ"),
                            ],
                            "どうも",
                        )
                    ],
                    accent=1,
                    interrogative=False,
                ),
                AccentPhrase(
                    [
                        Word(
                            [
                                Mora((Consonant("k"), Vowel("o"),), "コ"),
                                Mora((Vowel("N"),), "ン"),
                                Mora((Consonant("n"), Vowel("i"),), "ニ"),
                                Mora((Consonant("ch"), Vowel("i"),), "チ"),
                                Mora((Consonant("w"), Vowel("A"),), "ワ"),
                            ],
                            "こんにちは",
                        )
                    ],
                    accent=0,
                    interrogative=False,
                ),
            ],
            breath=Word(
                moras=[
                    Mora(
                        phonemes=(Vowel(symbol="pau"),),
                        pronunciation="、",
                    )
                ],
                text="、",
            ),
        ),
        BreathClause(
            accent_phrases=[
                AccentPhrase(
                    [
                        Word(
                            [
                                Mora((Consonant("p"), Vowel("a"),), "パ"),
                                Mora((Vowel("N"),), "ン"),
                                Mora((Consonant("d"), Vowel("a"),), "ダ"),
                            ],
                            "パンダ",
                        ),
                        Word(
                            [
                                Mora((Consonant("s"), Vowel("e"),), "セ"),
                                Mora((Vowel("N"),), "ン"),
                                Mora((Consonant("s"), Vowel("e"),), "セ"),
                                Mora((Vowel("i"),), "ー"),
                            ],
                            "先生",
                        )
                    ],
                    accent=6,
                    interrogative=False,
                ),
            ],
            breath=None,
        ),
    ]
    assert True
