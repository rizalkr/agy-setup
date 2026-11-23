---
name: docker-compose-cicd-cloud
description: Production-grade Dockerfiles, Docker Compose stacks, GitHub Actions CI/CD pipelines, and VPS/cloud reverse-proxy deployment. Use when containerizing Next.js/Python/Laravel apps, configuring compose profiles, or automating CI/CD.
---

# Docker, Compose, CI/CD & Cloud Deployment

## 1. Multi-Stage Dockerfiles
- Keep images small and secure:
  - **Next.js**: Enable `output: 'standalone'` in `next.config.*`; copy only `.next/standalone`, `.next/static`, and `public` into a minimal `node:22-alpine` runner stage.
  - **Python/FastAPI**: Use `python:3.12-slim` with `uv` or wheels in a builder stage; run as a non-root user.
  - **Laravel/PHP**: Multi-stage Composer build + PHP-FPM/Nginx (or FrankenPHP) with opcache enabled in production.
- Maintain `.dockerignore` (`.git`, `node_modules`, `.next`, `vendor`, `.env*`, `__pycache__`) to prevent bloated build contexts and leaked secrets.

## 2. Docker Compose & Profiles
- Separate `docker-compose.yml` (local dev/test) from `docker-compose.prod.yml` (resource limits, `restart: unless-stopped`, pinned image tags).
- Add explicit `healthcheck` directives on Postgres, Redis, and AI services, and gate dependent services with `depends_on: { service: { condition: service_healthy } }`.
- Use `profiles: ["test"]` for ephemeral `db_test` containers so daily `docker compose up` stays lean.

## 3. GitHub Actions CI/CD & Production
- Order CI jobs fast-fail first: `typecheck` & `lint` -> `unit tests` -> `integration/E2E tests` -> `docker build/push`.
- Cache package stores (`actions/cache` or `setup-node`/`setup-python` built-in cache) and Docker layer cache (`type=gha`).
- Terminate TLS at Nginx/Caddy/Cloudflare in front of app containers, keep DB ports unbound from public interfaces, and validate `.env` secrets outside VCS.
