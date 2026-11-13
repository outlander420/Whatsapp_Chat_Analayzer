import re

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.\-]+")
_URL = re.compile(r"(?:https?://|www\.)\S+")
_PHONE = re.compile(r"\+?\d[\d\s\-()]{6,}\d")


def redact_pii(text):
    """Mask emails, URLs, and phone numbers in a message body."""
    text = _URL.sub("[url]", text)
    text = _EMAIL.sub("[email]", text)
    text = _PHONE.sub("[phone]", text)
    return text


def redact_dataframe(df):
    """Return a copy of df with PII masked in the message column."""
    df = df.copy()
    df["message"] = df["message"].apply(redact_pii)
    return df
