#!/usr/bin/env bash
# Idempotent setup + baseline verification for WhatsApp Chat Analyzer.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    echo "[init] creating .venv"
    python3 -m venv .venv
    .venv/bin/pip install --quiet --upgrade pip
fi

echo "[init] installing pinned dependencies"
.venv/bin/pip install --quiet -r requirements.txt

echo "[init] baseline verification: pytest"
.venv/bin/pytest -q

echo "[init] OK — start the app with: .venv/bin/streamlit run app.py"
