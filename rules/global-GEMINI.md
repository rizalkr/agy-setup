## Communication & Language
- Write code, comments, commit messages, and technical documentation in English; respond in the user's conversation language.

## Token Efficiency & Context Discipline
- Read targeted line ranges (`StartLine`/`EndLine`) rather than entire large files once relevant lines are identified.
- Batch all independent file reads, searches, and edits in a single turn to avoid re-sending conversation history across extra turns.
- Delegate broad codebase exploration, multi-file searches, or noisy log analysis to the `research` subagent so intermediate search output stays out of the main context window.
- Never read raw large `.ipynb` files directly with `read_file` (base64/output bloat); inspect source cells via a one-line Python filter or load `colab-jupyter-notebooks` first.
- Keep responses concise and direct; do not repeat full code blocks in chat responses after applying edits.
- Before implementing domain-specific tasks (backend, frontend, database, testing, devops, data-ai, docs-office), check ~/.gemini/skill-library/INDEX.md (run ~/.gemini/skill-library/rebuild-index.py if newly added skills are not listed) and load only the relevant SKILL.md.

## Lean Code Discipline
- Follow the reuse ladder before writing new code: existing repo utilities/patterns -> standard library/platform features -> installed dependencies -> minimal readable new code (never add dependencies for trivial helpers).
- Keep changes surgical and YAGNI: avoid single-use abstractions, speculative configurability, or unrelated refactors; respect framework/repo file conventions while keeping implementations lean and explicit (boring over clever).
- Never cut trust-boundary validation, error handling that prevents data loss, security, accessibility, or readability; load the `lean-code` skill for non-trivial coding, refactoring, or bloat/diff audits.

## Context Compaction & Session Handoff
When `[CONTEXT_GUARDIAN: YELLOW ZONE ...]` or `[CONTEXT_GUARDIAN: RED ZONE ...]` appears in the context (or after completing a major milestone in a long session), evaluate task state and append a concise status block at the very end of your response in the user's conversation language:
- **Rule 1 (Never Compact Mid-Task)**: Never recommend `/compact` in the middle of an unresolved bug, failing test, or half-applied edit.
- **YELLOW ZONE**:
  - *If mid-task (unfinished fix/edit)*: State `[Yellow Zone - <steps> steps / ~<tokens>k tokens | Status: Not Safe to Compact]` and advise finishing the active sub-task first before compacting.
  - *If a sub-task/milestone just finished and more work remains*: State `[Yellow Zone - <steps> steps / ~<tokens>k tokens | Status: Safe to Compact]` and provide a ready-to-copy command block:
    `/compact Keep context: <key files, decisions, and verified state>. Next: <exact next task>.`
  - *If all requested tasks are finished*: Advise starting a fresh session (`/clear` or New Conversation) for the next unrelated task.
- **RED ZONE**:
  - *If all tasks are finished*: State `[Red Zone - <steps> steps / ~<tokens>k tokens | All Tasks Complete]`, recommend moving to a new session (`/clear`), and provide a short **New Session Handoff Prompt** block if follow-up work in a new session may be needed.
  - *If tasks remain unfinished*: State `[Red Zone - <steps> steps / ~<tokens>k tokens | Heavy Context]`, advise compacting immediately (or finishing the current atomic step first if mid-edit), and provide BOTH:
    1. **Same-Session Compact Prompt**:
       `/compact Keep context: <key files, decisions, and current progress>. Next: <exact next step>.`
    2. **New-Session Handoff Prompt (Alternative via `/clear`)**:
       A self-contained 3-5 line prompt the user can paste into a brand-new session if they prefer resetting context to zero.
