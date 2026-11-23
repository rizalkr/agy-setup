---
name: playwright-e2e-rbac
description: End-to-end, multi-role, and RBAC security testing with Playwright. Use when writing or debugging Playwright specs, auth storageState setups, role-based access tests, or flow assertions.
---

# Playwright E2E & RBAC Testing

## 1. Multi-Role Project & Fixture Architecture
- Separate role authentication setup from test specs using `storageState` files per role (e.g., `guest`, `buyer`, `principal`, `super-user`) so tests do not re-login on every spec.
- Organize projects cleanly in `playwright.config.*` (`setup`, `guest`, `rbac`, `security`, `flows`) with tag filters (`@smoke`, `@functional`) for fast targeted runs.

## 2. Reliable Locators & Assertions
- Prefer user-facing locators (`getByRole`, `getByLabel`, `getByText`, `getByTestId`) over brittle CSS/XPath chains.
- Rely on web-first auto-retrying assertions (`await expect(locator).toBeVisible()`, `toHaveURL()`, `toHaveText()`).
- Never use arbitrary `page.waitForTimeout(...)`; wait for specific network responses (`waitForResponse`), URL transitions, or element states.

## 3. RBAC & Security Test Patterns
- Verify both UI and direct URL/API access: test that unauthorized roles receive `403`/`401` or redirect when navigating directly to restricted routes or calling protected endpoints.
- Ensure test data created during flows is isolated or cleaned up via dedicated teardown/cleanup scripts so repeated runs stay deterministic.

## 4. Token-Efficient Execution
- Run targeted projects or single spec files with concise reporters during debugging:
  - `npx playwright test tests/rbac/rbac.spec.ts --reporter=line`
- Inspect failure traces/screenshots only on failing specs rather than dumping full HTML reports.
