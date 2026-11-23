---
name: reverse-engineering-appsec
description: Defensive reverse engineering, API/protocol discovery, client bundle inspection, and authorization security verification. Use when analyzing undocumented APIs, inspecting JS/web bundles, or auditing auth/RBAC/IDOR flaws.
---

# Reverse Engineering & Application Security

## 1. Scope & Safety Boundary
- Operate strictly on authorized local workspaces, owned targets, or explicit staging environments—never probe unauthorized third-party infrastructure or bypass anti-bot/CAPTCHA controls.
- Keep analysis read-only by default; document findings with exact file paths, endpoints, and reproduction evidence.

## 2. API & Bundle Reconnaissance
- Map client-server surfaces systematically:
  - Inspect route tables, OpenAPI specs, and client network wrappers (`fetch`/`axios`/RPC clients) to list endpoints, parameters, and auth headers.
  - Decode source-mapped or bundled JS cleanly (`rg` for `/api/`, `graphql`, token headers, feature flags) rather than reading minified blobs whole.
- Trace token lifecycles (login, refresh, CSRF `_token`, cookie flags `HttpOnly`/`SameSite`/`Secure`).

## 3. Authorization & Logic Verification
- Check every sensitive endpoint for:
  - **BOLA/IDOR**: Can Role A access/modify Resource ID belonging to Role B or another tenant?
  - **BFLA**: Can a lower-privilege user invoke admin/super-user endpoints directly?
  - **Mass Assignment & State Bypass**: Can client payloads overwrite `role`, `status`, `tenant_id`, or `price`?
- Record concrete evidence (request, role, expected vs actual status/body) and minimal remediation.
