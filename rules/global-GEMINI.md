- Do not use any emoticons.
- Use English instead of Indonesian for projects, code, comments, and documentation; use Indonesian only for conversation.

## Token Efficiency & Context Discipline
- Read targeted line ranges (`StartLine`/`EndLine`) rather than entire large files once relevant lines are identified.
- Batch all independent file reads, searches, and edits in a single turn to avoid re-sending conversation history across extra turns.
- Delegate broad codebase exploration, multi-file searches, or noisy log analysis to the `research` subagent so intermediate search output stays out of the main context window.
- Keep responses concise and direct; do not repeat full code blocks in chat responses after applying edits.
- Before implementing domain-specific tasks (backend, frontend, database, testing, devops, data-ai, docs-office), check ~/.gemini/skill-library/INDEX.md (run ~/.gemini/skill-library/rebuild-index.py if newly added skills are not listed) and load only the relevant SKILL.md.
