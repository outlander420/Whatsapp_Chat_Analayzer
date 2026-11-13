from pathlib import Path

import pytest

import preprocessor

FIXTURES = Path(__file__).parent / "fixtures"


def test_android_24h_parses(android_24h):
    df = preprocessor.preprocess(android_24h)
    assert len(df) == 12
    assert set(df["user"]) == {"Alice", "Bob", "Carol", "group_notification"}
    alice = df[df["user"] == "Alice"]
    assert alice.iloc[0]["message"] == "Good morning team! Meeting at 10."
    assert alice.iloc[0]["hour"] == 9


def test_android_12h_parses(android_12h):
    df = preprocessor.preprocess(android_12h)
    assert len(df) == 12
    carol = df[df["user"] == "Carol"]
    assert carol.iloc[0]["hour"] == 12
    assert carol.iloc[1]["hour"] == 13
    assert carol.iloc[1]["message"].startswith("🔥")


def test_ios_parses(ios_export):
    df = preprocessor.preprocess(ios_export)
    assert len(df) == 9
    assert set(df["user"]) == {"Alice", "Bob", "Carol"}
    alice = df[df["user"] == "Alice"]
    assert alice.iloc[0]["hour"] == 9
    assert alice.iloc[0]["minute"] == 15


def test_multiline_message_joins(android_24h):
    data = android_24h + "24/02/2023, 11:10 - Alice: line one\nline two\nline three\n"
    df = preprocessor.preprocess(data)
    last = df.iloc[-1]
    assert last["message"] == "line one\nline two\nline three"


def test_empty_input_raises():
    with pytest.raises(ValueError):
        preprocessor.preprocess("")


def test_media_markers_across_formats():
    assert preprocessor.is_media_marker("<Media omitted>")
    assert preprocessor.is_media_marker("image omitted")
    assert preprocessor.is_media_marker("video omitted")
    assert preprocessor.is_media_marker("Missed voice call")
    assert not preprocessor.is_media_marker("ok")
    assert not preprocessor.is_media_marker("")


def test_derived_columns(android_24h):
    df = preprocessor.preprocess(android_24h)
    for col in ("only_date", "year", "month_num", "month", "day",
                "day_name", "hour", "minute", "period"):
        assert col in df.columns
    assert df.iloc[0]["period"] == "9-10"
