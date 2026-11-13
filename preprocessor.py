import re
from datetime import datetime

import pandas as pd

# Android: "24/02/2023, 09:15 - " or "24/02/2023, 9:15 am - "
_ANDROID_LINE = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s*"
    r"(?P<ampm>[AaPp][Mm])?\s*-\s"
)
# iOS: "[24/02/2023, 09:15:34] "
_IOS_LINE = re.compile(
    r"^\[(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s*"
    r"(?P<ampm>[AaPp][Mm])?\]\s*"
)
_USER_SPLIT = re.compile(r"^(?P<user>[^\n:]{1,64}?):\s(?P<body>.*)", re.DOTALL)

# Messages that are media placeholders or system events, per format.
_MEDIA_MARKERS = {
    "<media omitted>",
    "image omitted",
    "video omitted",
    "audio omitted",
    "sticker omitted",
    "gif omitted",
    "document omitted",
    "contact card omitted",
    "missed voice call",
    "missed video call",
    "you deleted this message",
    "this message was deleted",
    "live location shared",
    "location: https://maps.google.com",
}
_MEDIA_PREFIXES = ("location:", "live location", "shared location")


def is_media_marker(message):
    """True when a message body is a media placeholder or call/system event."""
    text = str(message).strip().lower()
    if not text:
        return False
    return text in _MEDIA_MARKERS or text.startswith(_MEDIA_PREFIXES)


def _parse_timestamp(date_str, time_str, ampm):
    day_first = date_str.split("/")
    if len(day_first[2]) == 2:
        date_fmt = "%d/%m/%y"
    else:
        date_fmt = "%d/%m/%Y"
    if time_str.count(":") == 2:
        time_fmt = "%H:%M:%S"
    else:
        time_fmt = "%I:%M" if ampm else "%H:%M"
    stamp = f"{date_str} {time_str}"
    fmt = f"{date_fmt} {time_fmt}"
    if ampm:
        stamp = f"{stamp} {ampm.upper()}"
        fmt = f"{fmt} %p"
    return datetime.strptime(stamp, fmt)


def _split_messages(data):
    """Yield (datetime, raw_message) pairs; continuation lines join the previous message."""
    entries = []
    current = None
    for line in data.splitlines():
        android = _ANDROID_LINE.match(line)
        ios = None if android else _IOS_LINE.match(line)
        match = android or ios
        if match:
            if current is not None:
                entries.append(current)
            stamp = _parse_timestamp(
                match.group("date"), match.group("time"), match.group("ampm")
            )
            body = line[match.end():]
            current = [stamp, body]
        elif current is not None and line.strip():
            current[1] += "\n" + line
    if current is not None:
        entries.append(current)
    return entries


def preprocess(data):
    entries = _split_messages(data)
    if not entries:
        raise ValueError("No WhatsApp messages recognized in the provided text.")

    users, messages = [], []
    for _, raw in entries:
        match = _USER_SPLIT.match(raw)
        if match:
            users.append(match.group("user").strip())
            messages.append(match.group("body"))
        else:
            users.append("group_notification")
            messages.append(raw)

    df = pd.DataFrame(
        {
            "date": [stamp for stamp, _ in entries],
            "user": users,
            "message": messages,
        }
    )

    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df["hour"]:
        if hour == 23:
            period.append("23-00")
        else:
            period.append(f"{hour}-{hour + 1}")
    df["period"] = period

    return df
