# WhatsApp Chat Analyzer — AGENTS.md

## Overview
Streamlit web app that parses exported WhatsApp chat logs (Android 24h,
Android 12h AM/PM, and iOS formats) into a normalized DataFrame and renders
analytics: stats, timelines, activity maps, wordcloud, common words, emoji
analysis. Privacy-first: PII redaction (phones, emails, URLs) is a UI toggle
defaulted ON.

## Tech Stack
- Python 3.14 (`.venv/`), pandas 3.x, Streamlit 1.67
- matplotlib, seaborn, wordcloud, urlextract, emoji 2.x
- pytest for verification

## Quick Start
```bash
./init.sh                                  # create env if missing + verify
.venv/bin/pytest                           # run tests
.venv/bin/ruff check .                     # lint (if ruff installed)
.venv/bin/streamlit run app.py             # run the app
```

## Hard Constraints
1. Parser must handle all three export formats; never regress a format once
   a fixture exists for it.
2. Media-marker detection must be format-aware (Android `<Media omitted>`,
   iOS variants) — never hardcode a single marker string.
3. PII redaction toggle defaults to ON; redaction happens before analysis.
4. No Heroku artifacts (Procfile/setup.sh removed; do not reintroduce).
5. All dependencies pinned exactly in requirements.txt.
6. New parser behavior requires a fixture + test before merge.
7. Do not commit real chat exports or PII fixtures — synthetic data only.
8. emoji API must be emoji v2 (`emoji.emoji_list`), not `UNICODE_EMOJI`.

## Topic Docs
- `FLOW.md` — module map and call chains
- `DECISIONS.md` — decision log (append-only)
- `feature_list.json` — feature states (behavior, verification, state)

## Definition of Done
- `.venv/bin/pytest` passes
- `./init.sh` baseline verification passes
- Feature evidence recorded in `feature_list.json` / `progress.md`
