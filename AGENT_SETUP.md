# Automated Agent CLI Setup Runbook

This file is written for an AI Agent CLI (`agy`, Gemini CLI, Claude Code, Codex, or equivalent) to install and verify this Antigravity token-optimized setup non-interactively on **Windows, macOS, or Linux**.

## Execution Steps

Detect the host OS and run the corresponding steps in order without prompting the user unless a command fails:

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

### Step 2: Run Full Non-Destructive Installer

Running the full installer will:
- Install global rules (`~/.gemini/GEMINI.md`) and workspace graphify rule (`~/GEMINI.md`).
- Install Context Guardian (`~/.gemini/config/hooks.json` + `~/.gemini/config/hooks/context-guardian.py`) for automatic Green/Yellow/Red context zone monitoring and `/compact` recommendations.
- Install `core-skills` (`skill-router`, `graphify` fast-path, `find-skills`, `read-only-agent`, `security-audit`) into `~/.gemini/config/skills/`.
- Install the 18 categorized domain skills into `~/.gemini/skill-library/` and register `agy-index-skills` (`~/.local/bin/agy-index-skills` on POSIX, or `.cmd`/`.ps1` wrappers on Windows).
- Safely merge Orchestrator Mode (`model` + `orchestrator` planner/executor) into `~/.gemini/antigravity-cli/settings.json` while preserving existing `permissions` and `trustedWorkspaces`.
- Configure the `graphify` BeforeTool hook if `graphify` is installed, disable `datacloud_telemetry` in `~/.gemini/config/config.json` if present, and remove duplicate legacy skill folders.

**Linux / macOS:**
```bash
cd "$HOME/Projects/agy-setup" && ./install.sh --full
```

**Windows (PowerShell):**
```powershell
cd "$env:USERPROFILE\Projects\agy-setup"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --full
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
1. Confirmation that rules, `skill-router`, 18 categorized skills, and Orchestrator Mode were installed.
2. Output of `INDEX.md` skill count and JSON validation checks.
3. Reminder that project-specific MCP servers (such as Supabase) should be placed in `<project>/.agents/mcp_config.json` using `settings/mcp_templates.example.json` as a reference.
