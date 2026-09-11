#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

venv_python=".venv/bin/python"
if [[ ! -x "$venv_python" ]] || ! "$venv_python" -m pip --version >/dev/null 2>&1; then
    rm -rf .venv
    python3 -m venv .venv
fi

if ! "$venv_python" -c 'import fastapi, pymysql, sqlalchemy, uvicorn' 2>/dev/null; then
    "$venv_python" -m pip install -r requirements.txt
fi

exec "$venv_python" -m uvicorn app:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"