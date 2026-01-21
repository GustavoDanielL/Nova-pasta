#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Building backend binary using PyInstaller..."

ROOT_DIR=$(dirname "$0")
cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  echo "Using virtualenv"
  PYINSTALLER=.venv/bin/pyinstaller
else
  PYINSTALLER=pyinstaller
fi

if ! command -v "$PYINSTALLER" >/dev/null 2>&1; then
  echo "PyInstaller not found. Install it in the project's virtualenv: pip install pyinstaller" >&2
  exit 1
fi

rm -rf dist build __pycache__

"$PYINSTALLER" --clean --noconfirm --name financepro-backend --onefile backend/run_backend.py

# Create resources dir for Electron integration
mkdir -p frontend/resources/backend
cp dist/financepro-backend frontend/resources/backend/

echo "✅ Backend binary built and copied to frontend/resources/backend/"
