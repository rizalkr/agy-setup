---
name: fastapi-pydantic-v2
description: Best practices for FastAPI services and Pydantic v2 schemas, including async/sync execution, ML model lifespan loading, and Uvicorn configuration. Use when building or optimizing Python FastAPI APIs or AI inference endpoints.
---

# FastAPI & Pydantic v2 Specialist

## 1. Async vs Sync Route Execution
- Use `async def` ONLY when awaiting non-blocking async I/O (`httpx.AsyncClient`, `asyncpg`, async Redis).
- Use plain `def` (so FastAPI dispatches to AnyIO's threadpool) or `run_in_threadpool` for blocking CPU/ML work (`sentence-transformers`, `torch`, `pandas`, sync `requests`) so the event loop is never blocked.

## 2. Lifespan & Heavy Model Initialization
- Load ML models, tokenizers, and HTTP client pools once inside FastAPI's `@asynccontextmanager async def lifespan(app: FastAPI):` and store on `app.state`.
- Never load models at module import time (breaks test isolation) or inside per-request handlers.
- Expose lightweight `/health` (liveness) and `/ready` (model loaded) endpoints.

## 3. Pydantic v2 Patterns
- Use Pydantic v2 APIs: `model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)`, `@field_validator`, `@model_validator(mode="after")`, and `model_dump()` / `model_validate()`.
- Define strict request/response schemas with `Field(..., min_length=..., le=...)` bounds (e.g., cap batch sizes for embedding endpoints).

## 4. Error Handling & Production Serving
- Raise structured `HTTPException` or custom exception handlers returning consistent JSON `{ "detail": ..., "code": ... }` without leaking stack traces.
- For ML services, size Uvicorn workers conservatively (`--workers 1` or `2` per GPU/CPU budget) to avoid duplicating large model weights in RAM.

## Verification
Run `pytest` (with `TestClient` / `httpx.AsyncClient`) and check `ruff` / `mypy` if configured.
