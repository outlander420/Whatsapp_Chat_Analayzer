# DECISIONS — WhatsApp Chat Analyzer (append-only)

## 2026-11-13 — Full rebuild of parser/analytics stack
- **What**: Rewrote `preprocessor.py`, `helper.py`, `app.py`; added `redaction.py`.
- **Why**: Original code only parsed one Android format, used the removed
  emoji v1 API (`UNICODE_EMOJI`), had a broken `most_busy_users` rename,
  hardcoded media markers, and shipped Heroku artifacts.
- **Alternatives**: Incremental patches — rejected; the parser core was
  single-format and the emoji API was dead, so a clean rewrite with fixtures
  was safer and testable.

## 2026-11-13 — PII redaction as UI toggle, default ON
- **What**: Sidebar checkbox "Redact personal info (recommended)" defaults to
  True; `redact_dataframe` masks phones/emails/URLs before analysis.
- **Why**: User owns PII-leakage prevention; chat exports contain real PII.
- **Alternatives**: Always-on redaction — rejected (user asked for a toggle);
  default OFF — rejected (privacy-first requirement).

## 2026-11-13 — Synthetic fixtures committed to repo
- **What**: `tests/fixtures/{android_24h,android_12h,ios_export}.txt` are
  synthetic (Alice/Bob/Carol), committed.
- **Why**: Parser regressions need executable evidence; real exports must
  never be committed (hard constraint 7).
- **Alternatives**: Generating fixtures in test code — rejected; file fixtures
  are easier to extend per format.

## 2026-11-13 — Media markers centralized in `preprocessor.is_media_marker`
- **What**: Single set + prefix list covers `<Media omitted>`, `image omitted`,
  `video omitted`, missed-call/system events; helper consumes it.
- **Why**: Format-aware detection (hard constraint 2); avoids hardcoding one
  marker string in analytics.

## 2026-11-13 — Derived column names unchanged
- **What**: Parser emits the same columns as the original app
  (only_date, year, month_num, month, day, day_name, hour, minute, period).
- **Why**: Keeps `helper.py`/`app.py` call sites stable; analytics code did
  not need a rewrite of its DataFrame contract.

## 2026-11-13 — Heroku artifacts removed, deps pinned exactly
- **What**: Deleted `Procfile`/`setup.sh`; `requirements.txt` pins 8 exact
  versions; `.gitignore` covers `.venv/`, caches.
- **Why**: User deploys elsewhere; reproducible env (hard constraints 4–5).

## 2026-11-13 — pytest config: `pytest.ini` with `pythonpath = .`
- **What**: Root added to sys.path via pytest ini instead of packaging.
- **Why**: Flat script layout (app.py imports helper/preprocessor directly);
  packaging the app as a package was out of scope for this rebuild.
