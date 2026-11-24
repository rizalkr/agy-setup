- Do not use any emoticons.
- Use English instead of Indonesian for projects, code, comments, and documentation; use Indonesian only for conversation.

## Token Efficiency & Context Discipline
- Read targeted line ranges (`StartLine`/`EndLine`) rather than entire large files once relevant lines are identified.
- Batch all independent file reads, searches, and edits in a single turn to avoid re-sending conversation history across extra turns.
- Delegate broad codebase exploration, multi-file searches, or noisy log analysis to the `research` subagent so intermediate search output stays out of the main context window.
- Never read raw large `.ipynb` files directly with `read_file` (base64/output bloat); inspect source cells via a one-line Python filter or load `colab-jupyter-notebooks` first.
- Keep responses concise and direct; do not repeat full code blocks in chat responses after applying edits.
- Before implementing domain-specific tasks (backend, frontend, database, testing, devops, data-ai, docs-office), check ~/.gemini/skill-library/INDEX.md (run ~/.gemini/skill-library/rebuild-index.py if newly added skills are not listed) and load only the relevant SKILL.md.

## Context Compaction & Session Handoff Pakem
When `[CONTEXT_GUARDIAN: ZONA KUNING ...]` or `[CONTEXT_GUARDIAN: ZONA MERAH ...]` appears in the context (or after completing a major milestone in a long session), evaluate task state and append a concise status block at the very end of your response (in the user's conversation language):
- **Rule 1 (Never Compact Mid-Task)**: Never recommend `/compact` in the middle of an unresolved bug, failing test, or half-applied edit.
- **ZONA KUNING (75-119 steps or ~85k-135k tokens)**:
  - *If mid-task (unfinished fix/edit)*: State `[Zona Kuning - <steps> steps / ~<tokens>k tokens | Status: Belum Aman Compact]` and advise finishing the active sub-task first before compacting.
  - *If a sub-task/milestone just finished and more work remains*: State `[Zona Kuning - <steps> steps / ~<tokens>k tokens | Status: Aman untuk Compact]` and provide a ready-to-copy command block:
    `/compact Pertahankan konteks: <key files, decisions, and verified state>. Selanjutnya: <exact next task>.`
  - *If all requested tasks are finished*: Advise starting a fresh session (`/clear` or New Conversation) for the next unrelated task.
- **ZONA MERAH (>=120 steps or >=135k tokens)**:
  - *If all tasks are finished*: State `[Zona Merah - <steps> steps / ~<tokens>k tokens | Semua Tugas Selesai]`, recommend moving to a new session (`/clear`), and provide a short **New Session Handoff Prompt** block if follow-up work in a new session may be needed.
  - *If tasks remain unfinished*: State `[Zona Merah - <steps> steps / ~<tokens>k tokens | Konteks Berat]`, advise compacting immediately (or finishing the current atomic step first if mid-edit), and provide BOTH:
    1. **Same-Session Compact Prompt**:
       `/compact Pertahankan konteks: <key files, decisions, and current progress>. Lanjutkan: <exact next step>.`
    2. **New-Session Handoff Prompt (Alternative via `/clear`)**:
       A self-contained 3-5 line prompt the user can paste into a brand-new session if they prefer resetting context to zero.
