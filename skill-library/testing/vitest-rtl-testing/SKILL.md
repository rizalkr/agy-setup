---
name: vitest-rtl-testing
description: Unit and integration testing with Vitest 3, React Testing Library, and user-event. Use when writing TypeScript/React unit tests, mocking modules, testing hooks/components, or running DB-backed integration tests.
---

# Vitest 3 & React Testing Library

## 1. Unit vs Integration Separation
- Keep pure logic and component tests fast under `tests/unit/` (mocking network/DB boundaries; e.g., `SKIP_DB_RESET=1 vitest run tests/unit/`).
- Put DB-backed API/service tests under `tests/integration/` against a dedicated `.env.test` database with clean per-test or per-file state isolation.
- Always run non-interactive `vitest run` (never watch mode) from agents.

## 2. React Testing Library Discipline
- Query elements by accessible roles and labels (`screen.getByRole`, `screen.getByLabelText`) rather than DOM structure or `container.querySelector`.
- Use `const user = userEvent.setup()` and `await user.click(...)` / `await user.type(...)` instead of `fireEvent` for realistic event sequences.
- Use `findBy*` or `waitFor` for async UI updates; avoid testing internal component state or implementation details.

## 3. Mocking & Isolation
- Declare `vi.mock(...)` at module top-level with `vi.hoisted(...)` when factory functions reference local variables.
- Restore mocks/spies cleanly (`vi.restoreAllMocks()` / `vi.clearAllMocks()`) in `afterEach` so tests never leak state across files.

## Verification
Run targeted test files first (`npx vitest run path/to/file.test.ts`), then the full CI check (`npm run typecheck && npm run test`).
