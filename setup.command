#!/bin/bash
# ===================================================================
#  ONE-TIME SETUP (Mac). Double-click this once.
#  (First time, macOS may say "unidentified developer" — right-click
#   the file, choose Open, then Open again.)
# ===================================================================
cd "$(dirname "$0")" || exit 1

echo "Checking Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 not found. Install it from https://www.python.org/downloads/ and re-run."
  read -r -p "Press Enter to close..."
  exit 1
fi
python3 --version

echo "Creating virtual environment (.venv)..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing libraries (needs internet ONCE, only for the libraries -"
echo " your client PDFs are never uploaded anywhere)..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ""
echo "Setup complete. You can now double-click run_watcher.command"
read -r -p "Press Enter to close..."
