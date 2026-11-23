# Antigravity Categorized Skill Library

Store downloaded domain skills here organized by category so the global `skill-router` can discover and load them on demand without bloating every conversation's system prompt.

## Structure

```text
~/.gemini/skill-library/
├── backend/       # Laravel, PHP, Node.js, Go, Python APIs
├── frontend/      # React, Next.js, Vue, Tailwind, UI/UX
├── database/      # MySQL, PostgreSQL, Supabase, migrations, indexing
├── testing/       # Playwright, Pest, PHPUnit, Jest, Vitest, E2E
├── devops/        # Docker, CI/CD, Linux, Nginx, deployment
├── data-ai/       # Scraping, ETL, ML, analytics, prompts
└── docs-office/   # Word, PDF, Excel, technical writing, copywriting
```

Place each skill inside its category folder as:

```text
~/.gemini/skill-library/<category>/<skill-name>/SKILL.md
```

## Refreshing the Index

After adding, removing, or editing skills, run:

```bash
agy-index-skills
```

This regenerates `INDEX.md`, which `skill-router` reads to find and load only the skill needed for your current task.
