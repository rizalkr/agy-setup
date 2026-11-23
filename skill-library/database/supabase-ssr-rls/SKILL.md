---
name: supabase-ssr-rls
description: Secure Supabase integration with @supabase/ssr in Next.js App Router and high-performance PostgreSQL Row Level Security (RLS) policies. Use when configuring Supabase auth, middleware, RLS policies, or storage access.
---

# Supabase SSR & PostgreSQL RLS

## 1. @supabase/ssr Client & Auth Rules
- Maintain separate client factories:
  - Browser (`createBrowserClient`) for Client Components only.
  - Server (`createServerClient` using `await cookies()`) for Server Components, Server Actions, and Route Handlers.
  - Middleware helper that refreshes auth tokens and copies updated cookies onto `NextResponse`.
- Always call `supabase.auth.getUser()` on the server to verify JWT authenticity—never trust `getSession()` on the server.
- Never expose `SUPABASE_SERVICE_ROLE_KEY` in client bundles or `NEXT_PUBLIC_*` variables.

## 2. RLS Policy Design & Performance
- Enable RLS (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`) on every public schema table before adding data.
- Wrap auth helpers in subselects so Postgres evaluates them once per statement instead of per row:
  - Prefer `(select auth.uid()) = user_id` over `auth.uid() = user_id`.
- Create B-tree indexes on every column referenced in RLS policies (`user_id`, `tenant_id`, `org_id`).
- Specify explicit roles (`TO authenticated`) and keep separate policies for `SELECT`, `INSERT` (`WITH CHECK`), `UPDATE` (`USING` + `WITH CHECK`), and `DELETE`.

## 3. Storage & Edge Safety
- Scope Storage bucket policies using `storage.foldername(name)` against `(select auth.uid()::text)` or verified tenant membership.
- Validate all payloads at the DB or Server Action layer even when RLS is enabled.

## Verification
Test RLS boundaries with distinct user/anon sessions (not only service role) to verify cross-tenant and anonymous access are denied.
