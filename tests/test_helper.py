import helper
import preprocessor


def test_fetch_stats_counts_media_across_formats(android_24h, ios_export):
    df = preprocessor.preprocess(android_24h)
    num_messages, words, media, links = helper.fetch_stats("Overall", df)
    assert num_messages == 12
    assert media == 3  # two <Media omitted> + one missed call

    df_ios = preprocessor.preprocess(ios_export)
    _, _, media_ios, _ = helper.fetch_stats("Overall", df_ios)
    assert media_ios == 3  # <Media omitted> + image omitted + video omitted


def test_fetch_stats_per_user(android_24h):
    df = preprocessor.preprocess(android_24h)
    _, words, _, _ = helper.fetch_stats("Alice", df)
    assert words > 0


def test_emoji_helper_v2(android_24h):
    df = preprocessor.preprocess(android_24h)
    emoji_df = helper.emoji_helper("Overall", df)
    emojis = emoji_df[0].tolist()
    assert "🔥" in emojis
    assert "👋" in emojis


def test_most_common_words_excludes_media(android_24h):
    df = preprocessor.preprocess(android_24h)
    common = helper.most_common_words("Overall", df)
    words = common[0].tolist()
    assert "omitted" not in words
    assert len(common) > 0


def test_wordcloud(android_24h):
    df = preprocessor.preprocess(android_24h)
    wc = helper.create_wordcloud("Overall", df)
    assert wc is not None


def test_timelines_and_heatmap(android_24h):
    df = preprocessor.preprocess(android_24h)
    monthly = helper.monthly_timeline("Overall", df)
    assert monthly.iloc[0]["time"] == "February-2023"
    daily = helper.daily_timeline("Overall", df)
    assert len(daily) == 1
    heatmap = helper.activity_heatmap("Overall", df)
    assert heatmap.values.sum() == 12


def test_most_busy_users(android_24h):
    df = preprocessor.preprocess(android_24h)
    x, percent_df = helper.most_busy_users(df)
    assert list(percent_df.columns) == ["name", "percent"]
    assert percent_df["percent"].sum() <= 100.01
