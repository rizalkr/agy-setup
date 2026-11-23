---
name: drizzle-orm-postgres
description: Schema design, query optimization, transactions, and migration workflows for Drizzle ORM with PostgreSQL (including Neon and pgvector). Use when editing Drizzle schemas, writing complex queries, or managing migrations.
---

# Drizzle ORM & PostgreSQL

## 1. Schema & Indexing Conventions
- Define explicit `index()` and `uniqueIndex()` directly inside the table's third argument callback for foreign keys, tenant/status filters, and unique business keys.
- Use `timestamp('...', { withTimezone: true }).defaultNow().notNull()` consistently and `numeric` (or integer minor units) for currency—never `real`/`doublePrecision`.
- For vector search (`pgvector`), use `vector('embedding', { dimensions: ... })` with an HNSW or IVFFlat index matching the distance operator (`vector_cosine_ops`).

## 2. Query Performance & Safety
- Prefer targeted `db.select({ id: ..., name: ... })` over `SELECT *` on wide tables or embedding columns.
- Use `.prepare('query_name')` for hot-path lookups and `Promise.all` for independent reads.
- Wrap multi-step writes in `await db.transaction(async (tx) => { ... })`; inside the callback, use `tx` exclusively, never `db`.
- Always use Drizzle query builders (`eq`, `and`, `inArray`) or `sql` tagged templates—never string interpolation in `sql.raw()`.

## 3. Migration Discipline
- Check `package.json` scripts for environment-specific commands (`db:generate`, `db:migrate`, `db:push:test`, `db:migrate:prod`).
- Use `drizzle-kit generate` + `drizzle-kit migrate` for tracked environments; reserve `drizzle-kit push` for local/disposable test prototyping only.
- Review generated SQL in `drizzle/` before applying to staging or production to avoid accidental column drops or table locks.

## Verification
Run `npm run typecheck` and test migrations against the `.env.test` database before running integration tests.
