#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

bash ./install.sh
. ".venv/bin/activate"

echo
echo "Program inditasa..."
python main.py
