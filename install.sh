#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$REPO_DIR/install.py" "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$REPO_DIR/install.py" "$@"
else
  echo "Python 3 is required to run this installer." >&2
  exit 1
fi
