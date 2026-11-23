# Automated Agent CLI Setup Runbook

This file is written for an AI Agent CLI (`agy`, Gemini CLI, Claude Code, Codex, or equivalent) to install and verify this Antigravity token-optimized setup non-interactively on any Linux/macOS machine.

## Execution Steps

Run the following steps in order without prompting the user unless a command fails:

### Step 1: Clone or Update Repository

```bash
mkdir -p "$HOME/Projects"
if [ -d "$HOME/Projects/agy-setup/.git" ]; then
  git -C "$HOME/Projects/agy-setup" pull --ff-only
else
  git clone https://github.com/rizalkr/agy-setup.git "$HOME/Projects/agy-setup"
fi
```

### Step 2: Run Full Non-Destructive Installer

Execute `./install.sh --full` to:
- Install global rules (`~/.gemini/GEMINI.md`) and workspace graphify rule (`~/GEMINI.md`).
- Install `core-skills` (`skill-router`, `graphify` fast-path, `find-skills`, `read-only-agent`, `security-audit`) into `~/.gemini/config/skills/`.
- Install the 18 categorized domain skills into `~/.gemini/skill-library/` and symlink `~/.local/bin/agy-index-skills`.
- Safely merge Orchestrator Mode (`model` + `orchestrator` planner/executor) into `~/.gemini/antigravity-cli/settings.json` while preserving existing `permissions` and `trustedWorkspaces`.
- Configure the `graphify` BeforeTool hook if `graphify` is installed, disable `datacloud_telemetry` in `~/.gemini/config/config.json` if present, and remove duplicate legacy skill folders.

```bash
cd "$HOME/Projects/agy-setup" && ./install.sh --full
```

### Step 3: Ensure `~/.local/bin` Is on PATH (If Missing)

Check if `~/.local/bin` is already in `PATH`. If not, append it to `~/.bashrc` and `~/.zshrc` only when missing:

```bash
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *)
    for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
      if [ -f "$rc" ] && ! grep -q '\.local/bin' "$rc"; then
        printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$rc"
      fi
    done
    ;;
esac
```

### Step 4: Verify Installation

Run this single verification command and confirm every check passes:

```bash
"$HOME/.local/bin/agy-index-skills" && \
for f in \
  "$HOME/.gemini/antigravity-cli/settings.json" \
  "$HOME/.gemini/config/mcp_config.json" \
  "$HOME/.gemini/antigravity/mcp_config.json"; do
  python3 -m json.tool "$f" >/dev/null && echo "OK: $f"
done && \
head -n 5 "$HOME/.gemini/skill-library/INDEX.md" && \
ls -1 "$HOME/.gemini/config/skills"
```

### Step 5: Report to User

Report back concisely with:
1. Confirmation that rules, `skill-router`, 18 categorized skills, and Orchestrator Mode were installed.
2. Output of `INDEX.md` skill count and JSON validation checks.
3. Reminder that project-specific MCP servers (such as Supabase) should be placed in `<project>/.agents/mcp_config.json` using `settings/mcp_templates.example.json` as a reference.
