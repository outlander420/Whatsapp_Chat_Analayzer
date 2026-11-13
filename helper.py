from collections import Counter
from pathlib import Path

import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud

from preprocessor import is_media_marker

extract = URLExtract()
_STOP_WORDS_PATH = Path(__file__).parent / "stop_hinglish.txt"


def _filter_user(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df


def _content_messages(df):
    """Messages excluding system notifications and media placeholders."""
    temp = df[df["user"] != "group_notification"]
    return temp[~temp["message"].apply(is_media_marker)]


def fetch_stats(selected_user, df):
    df = _filter_user(selected_user, df)

    num_messages = df.shape[0]

    words = []
    for message in df["message"]:
        words.extend(message.split())

    num_media_messages = df["message"].apply(is_media_marker).sum()

    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), int(num_media_messages), len(links)


def most_busy_users(df):
    x = df["user"].value_counts().head()
    percent = round((df["user"].value_counts() / df.shape[0]) * 100, 2)
    new_df = percent.reset_index()
    new_df.columns = ["name", "percent"]
    return x, new_df


def _load_stop_words():
    return set(_STOP_WORDS_PATH.read_text(encoding="utf-8").split())


def create_wordcloud(selected_user, df):
    stop_words = _load_stop_words()
    df = _filter_user(selected_user, df)

    temp = _content_messages(df).copy()
    temp["message"] = temp["message"].apply(
        lambda m: " ".join(w for w in m.lower().split() if w not in stop_words)
    )

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    return wc.generate(temp["message"].str.cat(sep=" "))


def most_common_words(selected_user, df):
    stop_words = _load_stop_words()
    df = _filter_user(selected_user, df)

    words = []
    for message in _content_messages(df)["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):
    df = _filter_user(selected_user, df)

    emojis = []
    for message in df["message"]:
        emojis.extend(item["emoji"] for item in emoji.emoji_list(message))

    counts = Counter(emojis)
    return pd.DataFrame(counts.most_common(len(counts)))


def monthly_timeline(selected_user, df):
    df = _filter_user(selected_user, df)

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    timeline["time"] = timeline["month"] + "-" + timeline["year"].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    df = _filter_user(selected_user, df)
    return df.groupby("only_date").count()["message"].reset_index()


def week_activity_map(selected_user, df):
    df = _filter_user(selected_user, df)
    return df["day_name"].value_counts()


def month_activity_map(selected_user, df):
    df = _filter_user(selected_user, df)
    return df["month"].value_counts()


def activity_heatmap(selected_user, df):
    df = _filter_user(selected_user, df)
    return df.pivot_table(
        index="day_name", columns="period", values="message", aggfunc="count"
    ).fillna(0)
