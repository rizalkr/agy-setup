#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p \
  "$HOME/.gemini/config/skills" \
  "$HOME/.gemini/antigravity" \
  "$HOME/.gemini/antigravity-cli" \
  "$HOME/.gemini/skill-library" \
  "$HOME/.local/bin"

cp "$REPO_DIR/rules/global-GEMINI.md" "$HOME/.gemini/GEMINI.md"
cp "$REPO_DIR/rules/workspace-GEMINI.md" "$HOME/GEMINI.md"

cp -R "$REPO_DIR/core-skills/"* "$HOME/.gemini/config/skills/"
cp -R "$REPO_DIR/skill-library/"* "$HOME/.gemini/skill-library/"

chmod +x "$HOME/.gemini/skill-library/rebuild-index.py"
ln -sf "$HOME/.gemini/skill-library/rebuild-index.py" "$HOME/.local/bin/agy-index-skills"

if [ ! -f "$HOME/.gemini/config/mcp_config.json" ]; then
  printf '{\n  "mcpServers": {}\n}\n' > "$HOME/.gemini/config/mcp_config.json"
fi

if [ ! -f "$HOME/.gemini/antigravity/mcp_config.json" ]; then
  printf '{\n  "mcpServers": {}\n}\n' > "$HOME/.gemini/antigravity/mcp_config.json"
fi

"$HOME/.local/bin/agy-index-skills"

echo "Antigravity setup installed successfully."
echo "Optional templates are available in: $REPO_DIR/settings/"
