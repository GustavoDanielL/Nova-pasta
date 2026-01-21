#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Building Electron frontend (Linux)..."

cd $(dirname "$0")

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Install Node.js and npm first." >&2
  exit 1
fi

echo "Installing dependencies..."
npm install

echo "Running electron-builder..."
npx electron-builder --linux --x64 --arm64

echo "✅ Electron build finished. Check the 'dist' folder in frontend/."
