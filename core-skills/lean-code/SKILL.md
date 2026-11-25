---
name: lean-code
description: >-
  Pragmatic minimal-code and anti-overengineering guide combining YAGNI,
  reuse-first decision ladder, surgical diffs, readability, and safety
  guardrails. Use on non-trivial coding, feature implementation, bug fixes,
  refactoring, or when auditing a git diff or codebase for bloat and
  over-engineering.
---

# Lean Code

Write the smallest, clearest change that completely solves the task without over-engineering or sacrificing readability and safety.

## 1. Before Writing Code

- State non-obvious assumptions explicitly; if requirements are ambiguous and materially change scope, ask before coding.
- Trace what your change touches: callers, types, config, exports, and tests. Fix bugs once at the shared root cause after checking callers.
- Respect established repo and framework conventions (e.g., FormRequests, schemas, server/client boundaries, layered directories). Apply minimalism inside those layers rather than fighting project architecture.

## 2. Reuse Ladder (First Viable Option Wins)

1. **Skip what is not needed**: Do not add unrequested features, flags, fallbacks, or "for later" hooks (YAGNI).
2. **Reuse the codebase**: Match existing helpers, components, queries, and patterns.
3. **Use standard library or platform features**: Prefer built-in language, runtime, or framework primitives unless the repo already wraps them.
4. **Use installed dependencies**: Never add a new package for a small helper.
5. **Write minimal, readable code**: Straightforward, explicit code beats clever one-liners that require decoding.

## 3. Coding & Surgical Diff Rules

- **No premature abstraction**: Avoid wrappers, factories, indirection layers, or new files for single-use logic unless required by framework structure.
- **Surgical edits**: Touch only code directly tied to the task. Do not reformat, rename, or refactor unrelated adjacent code.
- **Clean your own orphans**: Remove imports, variables, or helpers made unused by your edit; report pre-existing dead code instead of deleting it unasked.
- **Comments**: Explain non-obvious *why* or constraints in one short line; never narrate *what* the code does.
- **Verification**: For non-trivial new logic (branching, parsing, state transitions, auth/billing), run existing checks and add a focused test if the repo has a test suite.

## 4. Never Cut

- Validation at trust boundaries (user input, external APIs, auth/RBAC, file/DB boundaries).
- Error handling that prevents silent failure or data loss.
- Security controls, accessibility, and explicit readability.
- Existing invariants and anything the user explicitly asked for.

## 5. Bloat & Diff Review Mode

When asked to review a diff, PR, or module for over-engineering (e.g., `git diff`), inspect only the changed scope and report concrete findings:
1. **Unnecessary code or features**: Speculative options, unused parameters, or dead paths.
2. **Premature abstractions**: Single-use wrappers, redundant DTO/type conversions, or gratuitous new files.
3. **Reinvented wheels**: Custom logic that duplicates a repo helper, stdlib feature, or installed library.
4. **Readability vs. cleverness**: Dense one-liners, unclear nesting, or missing boundary checks.
5. **Diff hygiene**: Unrelated edits or leftover unused imports/code.

Propose the concrete smaller replacement (or file/line deletion) for each finding while preserving safety and readability.
