# FLOW — WhatsApp Chat Analyzer

## Module Map

```
app.py (Streamlit UI)
  ├── load_chat(raw)            @st.cache_data wrapper
  │     └── preprocessor.preprocess(raw)   → DataFrame
  ├── redaction.redact_dataframe(df)       → PII-masked copy (toggle, default ON)
  └── helper.*                  analytics on the (possibly redacted) df
        ├── fetch_stats / most_busy_users / monthly_timeline / daily_timeline
        ├── week_activity_map / activity_heatmap
        ├── create_wordcloud / most_common_words
        └── emoji_helper         (emoji v2: emoji.emoji_list)
```

## preprocessor.py
- `_ANDROID_LINE` / `_IOS_LINE` regexes → `_parse_timestamp` (day-first;
  `%I:%M` + am/pm for 12h, `%H:%M:%S` for iOS) → `_split_messages`
  (multi-line continuation) → `_USER_SPLIT` (long lines → `group_notification`).
- `is_media_marker(msg)`: `_MEDIA_MARKERS` set + `_MEDIA_PREFIXES`
  (`<Media omitted>`, `image omitted`, `video omitted`, missed-call events).
- Derived columns: only_date, year, month_num, month, day, day_name,
  hour, minute, period.
- Empty input → `ValueError`.

## redaction.py
- `redact_pii(text)`: URL → `[url]`, email → `[email]`, phone → `[phone]`.
- `redact_dataframe(df)`: returns a redacted copy; original untouched.

## helper.py
- `_filter_user(selected, df)` → `_content_messages(df)` excludes
  `group_notification` rows and `is_media_marker` rows.
- Stop words: `stop_hinglish.txt` loaded via `pathlib` relative to module.
- `most_busy_users` returns `(x, percent_df)` with explicit
  `percent_df.columns = ["name", "percent"]`.

## Data flow
1. Upload `.txt` → bytes decoded → `load_chat` (cached).
2. `preprocess` → DataFrame.
3. If redaction ON → `redact_dataframe`.
4. Sidebar user selection → helper analytics → charts.

## Change Ledger
- 2026-11-13: Initial rebuild (parser, redaction module, emoji v2, cache,
  fixtures/tests, Heroku removal). See DECISIONS.md.
