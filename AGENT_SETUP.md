# Automated Agent CLI Setup Runbook

This file is written for an AI Agent CLI (`agy`, Gemini CLI, Claude Code, Codex, or equivalent) to install and verify this Antigravity token-optimized setup on **Windows, macOS, or Linux**.

## Step 0: Select Setup Preset

Check whether the user already specified a preset in their prompt (`1`–`3` Argon series or `4`–`6` Neon series):

| Series | Preset / Aliases | Planner | Executor | Context Guardian (Yellow / Red) |
| :--- | :--- | :--- | :--- | :--- |
| **Argon** | `1` / `balanced` / `argon-balanced` (**Recommended**) | `Gemini 4 Argon (Medium)` | `Gemini 4 Hydrogen (High)` | `75 / 120` steps (`85k / 135k` tokens) |
| **Argon** | `2` / `ultra-saver` / `argon-saver` | `Gemini 4 Hydrogen (XHigh)` | `Gemini 4 Hydrogen (High)` | `50 / 85` steps (`60k / 95k` tokens) |
| **Argon** | `3` / `max-quality` / `argon-max` | `Gemini 4 Argon (High)` | `Gemini 4 Hydrogen (XHigh)` | `100 / 150` steps (`110k / 160k` tokens) |
| **Neon** | `4` / `neon-balanced` / `neon` | `Gemini 4 Neon (High)` | `Gemini 4 Hydrogen (High)` | `75 / 120` steps (`85k / 135k` tokens) |
| **Neon** | `5` / `neon-saver` / `neon-ultra-saver` | `Gemini 4 Neon (Medium)` | `Gemini 4 Hydrogen (High)` | `55 / 90` steps (`65k / 100k` tokens) |
| **Neon** | `6` / `neon-max` / `neon-max-quality` | `Gemini 4 Neon (XHigh)` | `Gemini 4 Hydrogen (XHigh)` | `100 / 150` steps (`110k / 160k` tokens) |

- If the user did **not** specify a preset and interactive questions are available, ask them to choose between Argon Series (`1` `balanced` — Recommended, `2` `ultra-saver`, `3` `max-quality`) or Neon Series (`4` `neon-balanced`, `5` `neon-saver`, `6` `neon-max`) before running Step 2.
- If running strictly headless/non-interactive without user input, default to `--preset balanced`.

## Execution Steps

Detect the host OS and run the steps below in order:

### Step 1: Clone or Update Repository

**Linux / macOS (Bash/Zsh):**
```bash
mkdir -p "$HOME/Projects"
if [ -d "$HOME/Projects/agy-setup/.git" ]; then
  git -C "$HOME/Projects/agy-setup" pull --ff-only
else
  git clone https://github.com/rizalkr/agy-setup.git "$HOME/Projects/agy-setup"
fi
```

**Windows (PowerShell):**
```powershell
$Target = Join-Path $env:USERPROFILE "Projects\agy-setup"
New-Item -ItemType Directory -Force -Path (Split-Path $Target) | Out-Null
if (Test-Path (Join-Path $Target ".git")) {
  git -C $Target pull --ff-only
} else {
  git clone https://github.com/rizalkr/agy-setup.git $Target
}
```

### Step 2: Run Installer with Chosen Preset (`<PRESET>` = `balanced` | `ultra-saver` | `max-quality` | `neon-balanced` | `neon-saver` | `neon-max`)

Running with `--preset <PRESET>` will:
- Install global rules (`~/.gemini/GEMINI.md`) and workspace graphify rule (`~/GEMINI.md`).
- Install Context Guardian (`~/.gemini/config/hooks.json`, `context-guardian.py`, and `preset.json`) configured for `<PRESET>`.
- Install `core-skills` (`skill-router`, `graphify` fast-path, `find-skills`, `read-only-agent`, `security-audit`) into `~/.gemini/config/skills/`.
- Install the 18 categorized domain skills into `~/.gemini/skill-library/` and register `agy-index-skills`.
- Safely merge `<PRESET>`'s Orchestrator model combo into `~/.gemini/antigravity-cli/settings.json` while preserving existing `permissions` and `trustedWorkspaces`.
- Configure the `graphify` BeforeTool hook if `graphify` is installed, disable `datacloud_telemetry` in `~/.gemini/config/config.json` if present, and remove duplicate legacy skill folders.

**Linux / macOS:**
```bash
cd "$HOME/Projects/agy-setup" && ./install.sh --preset <PRESET>
```

**Windows (PowerShell):**
```powershell
cd "$env:USERPROFILE\Projects\agy-setup"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --preset <PRESET>
```

### Step 3: Ensure `~/.local/bin` Is on PATH (If Missing)

**Linux / macOS:**
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

**Windows:** `install.ps1` automatically appends `%USERPROFILE%\.local\bin` to the Windows User `PATH` if missing.

### Step 4: Verify Installation

**Linux / macOS:**
```bash
"$HOME/.local/bin/agy-index-skills" && \
for f in \
  "$HOME/.gemini/antigravity-cli/settings.json" \
  "$HOME/.gemini/config/hooks.json" \
  "$HOME/.gemini/config/hooks/preset.json" \
  "$HOME/.gemini/config/mcp_config.json" \
  "$HOME/.gemini/antigravity/mcp_config.json"; do
  python3 -m json.tool "$f" >/dev/null && echo "OK: $f"
done && \
head -n 5 "$HOME/.gemini/skill-library/INDEX.md" && \
ls -1 "$HOME/.gemini/config/skills"
```

**Windows (PowerShell):**
```powershell
& "$env:USERPROFILE\.local\bin\agy-index-skills.cmd"
$Py = if (Get-Command py -ErrorAction SilentlyContinue) { "py -3" } else { "python" }
foreach ($f in @(
  "$env:USERPROFILE\.gemini\antigravity-cli\settings.json",
  "$env:USERPROFILE\.gemini\config\hooks.json",
  "$env:USERPROFILE\.gemini\config\hooks\preset.json",
  "$env:USERPROFILE\.gemini\config\mcp_config.json",
  "$env:USERPROFILE\.gemini\antigravity\mcp_config.json"
)) {
  Invoke-Expression "$Py -m json.tool `"$f`" > `$null"
  Write-Host "OK: $f"
}
Get-Content "$env:USERPROFILE\.gemini\skill-library\INDEX.md" -TotalCount 5
Get-ChildItem -Name "$env:USERPROFILE\.gemini\config\skills"
```

### Step 5: Report to User

Report back concisely with:
1. Active preset installed (`balanced`, `ultra-saver`, `max-quality`, `neon-balanced`, `neon-saver`, or `neon-max`) and its Planner/Executor model combo.
2. Output of `INDEX.md` skill count and JSON validation checks.
3. Reminder that project-specific MCP servers (such as Supabase) should be placed in `<project>/.agents/mcp_config.json` using `settings/mcp_templates.example.json` as a reference.
