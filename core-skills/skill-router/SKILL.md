---
name: skill-router
description: >-
  Automatically routes tasks to specialized domain skills stored in
  ~/.gemini/skill-library/ across categories (backend, frontend, database,
  testing, devops, data-ai, docs-office). Activate this skill or read
  ~/.gemini/skill-library/INDEX.md whenever a task involves framework-specific
  coding, testing, database work, DevOps, data processing, or document
  generation.
---

# Global Skill Router

Use this skill to discover and load specialized skills from `~/.gemini/skill-library/` on demand without keeping all skills loaded in every conversation.

## Steps

1. Read `~/.gemini/skill-library/INDEX.md`.
2. If the user mentions newly downloaded skills or `INDEX.md` does not list a recently added skill, run `~/.gemini/skill-library/rebuild-index.py` first and then re-read `INDEX.md`.
3. Identify only the skill(s) relevant to the current task based on category and description.
4. Read only the matching `SKILL.md` file(s) from the path listed in `INDEX.md`, and follow their instructions. Do not read unrelated skills.
