# Antigravity (AGY) Token-Optimized CLI & IDE Setup

A portable, token-disciplined configuration for **Google Antigravity (CLI, App, and IDE)** featuring Orchestrator Mode (Plan-Execute), pruned MCP tool schemas, Progressive Disclosure skills, and a **Global Skill Router** backed by a categorized **18-skill library**.

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

## Installation

```bash
git clone https://github.com/rizalkr/agy-setup.git
cd agy-setup
./install.sh
```

Ensure `~/.local/bin` is in your `PATH` so `agy-index-skills` works globally.

### Optional Settings & Templates
Review and merge the sanitized templates under `settings/` manually if setting up a fresh machine:
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
   ```bash
   ./sync.sh
   git add -A && git commit -m "chore: update skills" && git push
   ```
