# Antigravity (AGY) Token-Optimized CLI & IDE Setup

A portable, token-disciplined configuration for **Google Antigravity (CLI, App, and IDE)** across **Windows, macOS, and Linux** featuring Orchestrator Mode (Plan-Execute), pruned MCP tool schemas, Progressive Disclosure skills, and a **Global Skill Router** backed by a categorized **18-skill library**.

## Architecture Highlights

1. **Orchestrator Mode (Plan-Execute)**:
   - Uses a balanced reasoning model (`Gemini 4 Argon (Medium)`) for planning and a fast execution model (`Gemini 4 Hydrogen (High)`) for implementation, reducing wasted tokens from unguided trial-and-error.
2. **Zero Global MCP Context Bloat**:
   - Keeps global `mcp_config.json` empty (`{"mcpServers": {}}`) so unused MCP tool schemas are never injected into every turn.
   - Project-specific MCP servers (such as Supabase) belong inside `<project>/.agents/mcp_config.json` (see `settings/mcp_templates.example.json`).
3. **Global Rules (`GEMINI.md`)**:
   - Enforces targeted line-range reads (`StartLine`/`EndLine`), batched parallel tool calls, subagent delegation (`research`) for noisy exploration, concise responses, and automatic skill routing.
   - Integrates `graphify` (`~/GEMINI.md`) to query codebase knowledge graphs before raw file reads.
4. **Global Skill Router + Categorized Skill Library (18 Skills)**:
   - Instead of loading dozens of skill descriptions into every prompt, only `skill-router` (plus 4 core skills) is registered globally in `~/.gemini/config/skills/`.
   - Domain skills live in `~/.gemini/skill-library/<category>/<skill>/SKILL.md`, indexed into `INDEX.md` via `agy-index-skills`.
   - `graphify/SKILL.md` is refactored via Progressive Disclosure (2.2 KB fast-path + `references/full-pipeline.md`).
5. **Context Guardian (`PreInvocation` Auto-Compact Advisor)**:
   - Monitors step count since last compaction (`75` Yellow / `120` Red) and real active tokens (`input_tokens + cache_read_tokens`, `85k` Yellow / `135k` Red) via `hooks/context-guardian.py` with cooldown and automatic reset after `/compact`.
   - Enforces the **Never Compact Mid-Task** rule: advises finishing active fixes first, generates copy-paste `/compact <context + next step>` commands after milestones, and provides New Session Handoff prompts when all tasks finish or context reaches the Red Zone.

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

Run `agy` (or any AI coding CLI) on a new machine (Windows, macOS, or Linux) and paste this single prompt:

```text
Clone https://github.com/rizalkr/agy-setup.git to ~/Projects/agy-setup (or pull latest if it exists), then read and execute every step in AGENT_SETUP.md to install the full token-optimized setup.
```

The agent will follow [AGENT_SETUP.md](./AGENT_SETUP.md), run the cross-platform installer (`--full`), build the skill index, and verify all JSON configs automatically.

## Manual Installation

### Linux / macOS (Bash/Zsh)

Full setup (rules, skills + non-destructive CLI settings merge):
```bash
git clone https://github.com/rizalkr/agy-setup.git ~/Projects/agy-setup
cd ~/Projects/agy-setup
./install.sh --full
```

Minimal setup (rules & skills only):
```bash
./install.sh
```

Ensure `~/.local/bin` is in your `PATH` so `agy-index-skills` works globally.

### Windows (PowerShell)

Requires Python 3 (`py` or `python`) installed on PATH.

Full setup (rules, skills, `.cmd`/`.ps1` `agy-index-skills` wrappers, User PATH update + non-destructive CLI settings merge):
```powershell
git clone https://github.com/rizalkr/agy-setup.git "$env:USERPROFILE\Projects\agy-setup"
cd "$env:USERPROFILE\Projects\agy-setup"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --full
```

Minimal setup (rules & skills only):
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Or cross-platform directly via Python on any OS:
```bash
python3 install.py --full   # or: py -3 install.py --full
```

### Optional Settings & Templates
Review and merge the sanitized templates under `settings/` manually if needed:
- `settings/cli-settings.example.json` -> `~/.gemini/antigravity-cli/settings.json`
- `settings/hooks-settings.example.json` -> `~/.gemini/settings.json`
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
