from redaction import redact_dataframe, redact_pii


def test_email_masked():
    assert redact_pii("mail me at alice@example.com now") == "mail me at [email] now"


def test_url_masked():
    assert redact_pii("doc at https://example.com/doc/x?y=1 end") == "doc at [url] end"


def test_phone_masked():
    assert redact_pii("call +91 98765 43210 today") == "call [phone] today"


def test_plain_text_untouched():
    assert redact_pii("Meeting at 10, ship it!") == "Meeting at 10, ship it!"


def test_dataframe_redaction(android_24h):
    import preprocessor

    df = preprocessor.preprocess(android_24h)
    redacted = redact_dataframe(df)
    joined = "\n".join(redacted["message"])
    assert "alice@example.com" not in joined
    assert "https://example.com" not in joined
    assert "98765" not in joined
    assert "[email]" in joined and "[url]" in joined and "[phone]" in joined
    # original untouched
    assert "alice@example.com" in "\n".join(df["message"])
