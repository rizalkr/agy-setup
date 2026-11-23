---
name: saas-multitenant-highperf-api
description: Design and implementation patterns for multi-tenant SaaS architectures and high-performance backend APIs (RBAC, tenant isolation, idempotency, caching, queues, and microservices). Use when architecting SaaS backends or scaling APIs.
---

# Multi-Tenant SaaS & High-Performance API Architecture

## 1. Tenant Isolation & RBAC
- Enforce tenant isolation at every boundary: API middleware, service layer, DB queries/RLS, background jobs, and object-storage key prefixes (`tenants/{tenant_id}/...`).
- Derive `tenant_id` from verified session/JWT/subdomain context—never accept arbitrary tenant overrides unless the caller holds a verified `super_admin` role.
- Model RBAC with explicit permission checks per action (resource + tenant scope), not just UI hiding.

## 2. Idempotency & Data Integrity
- Require idempotency keys (or unique constraint guards) on payment, webhook, invoice, and order-creation endpoints to prevent duplicate writes on retries.
- Perform state transitions atomically in DB transactions with optimistic/pessimistic locking (`version` column or `SELECT ... FOR UPDATE`).

## 3. Latency, Caching & Async Offloading
- Cache read-heavy tenant config and permission lookups in Redis with explicit TTLs and event-driven invalidation on role/plan updates.
- Offload slow work (PDF generation, email, bulk imports, embedding indexing, webhooks) to idempotent background queue workers with dead-letter retry policies.
- Apply cursor/keyset pagination on large tables instead of deep `OFFSET` queries.

## 4. Service Resilience & Observability
- Set explicit timeouts, bounded retries with exponential backoff + jitter, and circuit breakers on downstream HTTP/AI-service calls.
- Propagate `X-Request-ID` / correlation IDs and structured JSON logs (`tenant_id`, `user_id`, `latency_ms`, `status`) across services.
- Enforce per-tenant and per-IP rate limiting at the API gateway or middleware layer.
