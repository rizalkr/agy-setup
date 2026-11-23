#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$REPO_DIR/rules" "$REPO_DIR/core-skills" "$REPO_DIR/skill-library"

cp "$HOME/.gemini/GEMINI.md" "$REPO_DIR/rules/global-GEMINI.md"
cp "$HOME/GEMINI.md" "$REPO_DIR/rules/workspace-GEMINI.md"

rm -rf "$REPO_DIR/core-skills/"*
cp -R "$HOME/.gemini/config/skills/"* "$REPO_DIR/core-skills/"

rm -rf "$REPO_DIR/skill-library/"*
cp -R "$HOME/.gemini/skill-library/"* "$REPO_DIR/skill-library/"

python3 "$REPO_DIR/skill-library/rebuild-index.py"
find "$REPO_DIR" -name "__pycache__" -type d -exec rm -rf {} +

echo "Synced rules, core-skills, and skill-library into $REPO_DIR."
