#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

find_python() {
    for cmd in python3 python; do
        if command -v "$cmd" >/dev/null 2>&1 && "$cmd" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 9) else 1)
PY
        then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

PYTHON_CMD="$(find_python)" || {
    echo "Python 3.9 vagy ujabb verzio nem talalhato."
    echo "Toltsd le innen: https://www.python.org/downloads/"
    exit 1
}

if [ ! -d ".venv" ]; then
    echo "Virtualis kornyezet letrehozasa..."
    "$PYTHON_CMD" -m venv .venv
fi

. ".venv/bin/activate"

echo "Fuggosegek telepitese..."
PIP_DISABLE_PIP_VERSION_CHECK=1 python -m pip install -r requirements.txt

echo "Telepites kesz."
