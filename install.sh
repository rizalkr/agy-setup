#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APPLY_SETTINGS=false
WITH_HOOKS=false

for arg in "$@"; do
  case "$arg" in
    --full|--apply-settings)
      APPLY_SETTINGS=true
      ;;
    --with-hooks)
      WITH_HOOKS=true
      ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: ./install.sh [--full] [--apply-settings] [--with-hooks]" >&2
      exit 1
      ;;
  esac
done

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

if [ "$APPLY_SETTINGS" = true ]; then
  python3 - "$REPO_DIR" "$HOME" "$WITH_HOOKS" <<'PYEOF'
import json
import os
import shutil
import sys
from pathlib import Path

repo_dir = Path(sys.argv[1])
home_dir = Path(sys.argv[2])
with_hooks = sys.argv[3].lower() == "true"

# 1. Non-destructive merge into ~/.gemini/antigravity-cli/settings.json
cli_example = json.loads((repo_dir / "settings/cli-settings.example.json").read_text(encoding="utf-8"))
cli_target = home_dir / ".gemini/antigravity-cli/settings.json"
merge_keys = ("model", "orchestrator", "agentMode", "artifactReviewPolicy", "colorScheme", "vimInsertFirst")

if cli_target.exists():
    cli_data = json.loads(cli_target.read_text(encoding="utf-8"))
    for key in merge_keys:
        if key in cli_example:
            cli_data[key] = cli_example[key]
else:
    cli_data = cli_example

cli_target.write_text(json.dumps(cli_data, indent=2) + "\n", encoding="utf-8")

# 2. Merge graphify BeforeTool hook into ~/.gemini/settings.json if graphify exists or --with-hooks
graphify_bin = shutil.which("graphify") or (
    str(home_dir / ".local/bin/graphify") if (home_dir / ".local/bin/graphify").is_file() else None
)
if graphify_bin or with_hooks:
    hooks_example = json.loads((repo_dir / "settings/hooks-settings.example.json").read_text(encoding="utf-8"))
    settings_target = home_dir / ".gemini/settings.json"
    if settings_target.exists():
        settings_data = json.loads(settings_target.read_text(encoding="utf-8"))
    else:
        settings_data = {}
    if "hooks" not in settings_data:
        settings_data["hooks"] = hooks_example["hooks"]
        if graphify_bin:
            for entry in settings_data["hooks"].get("BeforeTool", []):
                for hook in entry.get("hooks", []):
                    if isinstance(hook.get("command"), str) and "graphify hook-guard" in hook["command"]:
                        hook["command"] = f"{graphify_bin} hook-guard gemini"
    settings_target.write_text(json.dumps(settings_data, indent=2) + "\n", encoding="utf-8")

# 3. Disable datacloud_telemetry plugin in ~/.gemini/config/config.json if present
config_target = home_dir / ".gemini/config/config.json"
if config_target.exists():
    config_data = json.loads(config_target.read_text(encoding="utf-8"))
    plugins = config_data.setdefault("plugins", {})
    if isinstance(plugins.get("googlecloudtools.datacloud_telemetry"), dict):
        plugins["googlecloudtools.datacloud_telemetry"]["enabled"] = False
        config_target.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")
PYEOF

  # 4. Clean legacy duplicate skill directories when canonical copies exist
  for dup in \
    "$HOME/.gemini/skills/graphify" \
    "$HOME/.gemini/skills/security-audit" \
    "$HOME/.agents/skills/find-skills" \
    "$HOME/.agents/skills/security-audit"; do
    skill_name="$(basename "$dup")"
    if [ -d "$dup" ] && [ -d "$HOME/.gemini/config/skills/$skill_name" ]; then
      rm -rf "$dup"
    fi
  done
  rmdir "$HOME/.gemini/skills" 2>/dev/null || true
fi

"$HOME/.local/bin/agy-index-skills"

echo "Antigravity setup installed successfully (apply_settings=$APPLY_SETTINGS)."
echo "Templates remain available in: $REPO_DIR/settings/"
