# Antigravity (AGY) Token-Optimized CLI & IDE Setup

A portable, token-disciplined configuration for **Google Antigravity (CLI, App, and IDE)** across **Windows, macOS, and Linux** featuring configurable Orchestrator Mode presets, pruned MCP tool schemas, Progressive Disclosure skills, Context Guardian auto-compact advisor, and a **Global Skill Router** backed by a categorized **18-skill library**.

## Setup Presets (Choose Your Token vs. Quality Combo)

Pick the profile that matches your task and credit budget (defined in `settings/presets.json`):

| Preset | Flag / Alias | Planner Model | Executor Model | Context Guardian (Yellow / Red) | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Setup 1: Balanced (Recommended)** | `--preset 1` or `balanced` | `Gemini 4 Argon (Medium)` | `Gemini 4 Hydrogen (High)` | `75 / 120` steps (`85k / 135k` tokens) | Daily full-stack coding: best balance of quality and token efficiency |
| **Setup 2: Ultra Saver** | `--preset 2` or `ultra-saver` | `Gemini 4 Hydrogen (XHigh)` | `Gemini 4 Hydrogen (High)` | `50 / 85` steps (`60k / 95k` tokens) | Tight token/credit budgets, repetitive edits, quick scripts |
| **Setup 3: Max Quality** | `--preset 3` or `max-quality` | `Gemini 4 Argon (High)` | `Gemini 4 Hydrogen (XHigh)` | `100 / 150` steps (`110k / 160k` tokens) | Complex system architecture, deep debugging, multi-service refactors |

## Architecture Highlights

1. **Orchestrator Mode (Plan-Execute)**:
   - Separates planning and execution models according to your selected preset (`balanced`, `ultra-saver`, or `max-quality`), avoiding wasted tokens from trial-and-error loops.
2. **Zero Global MCP Context Bloat**:
   - Keeps global `mcp_config.json` empty (`{"mcpServers": {}}`) so unused MCP tool schemas are never injected into every turn.
   - Project-specific MCP servers (such as Supabase) belong inside `<project>/.agents/mcp_config.json` (see `settings/mcp_templates.example.json`).
3. **Global Rules (`GEMINI.md`)**:
   - Enforces targeted line-range reads (`StartLine`/`EndLine`), batched parallel tool calls, subagent delegation (`research`) for noisy exploration, concise responses, and automatic skill routing.
   - Integrates `graphify` (`~/GEMINI.md`) to query codebase knowledge graphs before raw file reads.
4. **Global Skill Router + Categorized Skill Library (18 Skills)**:
   - Only `skill-router` (plus 4 core skills) is registered globally in `~/.gemini/config/skills/`.
   - Domain skills live in `~/.gemini/skill-library/<category>/<skill>/SKILL.md`, indexed into `INDEX.md` via `agy-index-skills`.
   - `graphify/SKILL.md` uses Progressive Disclosure (2.2 KB fast-path + `references/full-pipeline.md`).
5. **Context Guardian (`PreInvocation` Auto-Compact Advisor)**:
   - Monitors step count and active tokens (`input_tokens + cache_read_tokens`) using your selected preset thresholds in `~/.gemini/config/hooks/preset.json`, with cooldown and automatic reset after `/compact`.
   - Enforces **Never Compact Mid-Task**: warns against compacting mid-fix, generates copy-paste `/compact <context + next step>` commands after milestones, and provides New Session Handoff prompts when tasks finish or reach the Red Zone.

## Skill Library Catalog (18 Skills Across 7 Categories)

| Category | Skills |
| :--- | :--- |
| `backend` | `fastapi-pydantic-v2`, `laravel13-specialist`, `saas-multitenant-highperf-api` |
| `frontend` | `nextjs-react19-best-practices`, `tailwind-v4-shadcn-ui`, `high-end-visual-taste`, `saas-dashboard-ux`, `design-system-microinteractions` |
| `database` | `drizzle-orm-postgres`, `supabase-ssr-rls` |
| `testing` | `playwright-e2e-rbac`, `vitest-rtl-testing`, `laravel-phpunit-tdd` |
| `devops` | `docker-compose-cicd-cloud` |
| `data-ai` | `rag-llm-agents-embeddings`, `python-data-ml-scraping`, `reverse-engineering-appsec` |
| `docs-office` | `office-docs-guidebook-automation` |

## Quick Setup with Agent CLI (Zero Manual Config)

Run `agy` (or any AI coding CLI) on a new machine (Windows, macOS, or Linux) and paste this single prompt (optionally specify `preset 1`, `2`, or `3`—if omitted, the agent will ask you to choose):

```text
Clone https://github.com/rizalkr/agy-setup.git to ~/Projects/agy-setup (or pull latest if it exists), then read and execute AGENT_SETUP.md to install the setup. Ask me which preset I want (1 Balanced [Recommended], 2 Ultra Saver, or 3 Max Quality) before running the installer.
```

Or specify your preset directly in one shot:

```text
Clone https://github.com/rizalkr/agy-setup.git to ~/Projects/agy-setup (or pull latest if it exists), then read and execute AGENT_SETUP.md with preset 1 (balanced).
```

## Manual Installation

### Linux / macOS (Bash/Zsh)

Interactive preset menu (choose 1, 2, or 3):
```bash
git clone https://github.com/rizalkr/agy-setup.git ~/Projects/agy-setup
cd ~/Projects/agy-setup
./install.sh --choose
```

Or install a specific preset non-interactively (`--full` defaults to Preset 1 `balanced`):
```bash
./install.sh --preset 1   # or: --preset balanced | ultra-saver | max-quality
```

Minimal setup (rules & skills only, without merging CLI settings):
```bash
./install.sh
```

Ensure `~/.local/bin` is in your `PATH` so `agy-index-skills` works globally.

### Windows (PowerShell)

Requires Python 3 (`py` or `python`) installed on PATH.

Interactive preset menu (choose 1, 2, or 3):
```powershell
git clone https://github.com/rizalkr/agy-setup.git "$env:USERPROFILE\Projects\agy-setup"
cd "$env:USERPROFILE\Projects\agy-setup"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --choose
```

Or install a specific preset directly (`--full` defaults to Preset 1 `balanced`):
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 --preset 1
```

Minimal setup (rules & skills only):
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### Switching Presets Later
You can switch presets anytime without losing permissions or workspaces:
```bash
./install.sh --preset 2      # Linux/macOS
.\install.ps1 --preset 2     # Windows PowerShell
```

### Optional Templates
- `settings/mcp_templates.example.json` -> copy individual servers into `<project>/.agents/mcp_config.json`

## Adding New Skills & Syncing

1. Drop any new skill into `~/.gemini/skill-library/<category>/<skill-name>/SKILL.md`.
2. Refresh the index:
   ```bash
   agy-index-skills
   ```
3. Sync local changes back into this repository and push:
   - Linux / macOS:
     ```bash
     ./sync.sh && git add -A && git commit -m "chore: update skills" && git push
     ```
   - Windows (PowerShell):
     ```powershell
     .\sync.ps1; git add -A; git commit -m "chore: update skills"; git push
     ```
