---
name: rag-llm-agents-embeddings
description: Designing RAG pipelines, sentence-transformer embedding services, hybrid vector search, and reliable LLM agent workflows. Use when building AI search, embedding indexers, chunking pipelines, or structured LLM outputs.
---

# RAG, Embeddings & LLM Agents

## 1. Chunking & Metadata Discipline
- Chunk documents by semantic boundaries (headings, paragraphs, code symbols) with modest overlap (10-15%), preserving metadata (`source_id`, `tenant_id`, `section`, `updated_at`) for pre-filtering.
- Never mix tenants inside vector retrieval: apply mandatory `tenant_id` / `visibility` metadata filters before ranking similarity.

## 2. Embedding Services & Indexing
- Batch embedding inference (`model.encode(texts, batch_size=32, normalize_embeddings=True)`) and cache embeddings by content hash so unchanged records are never re-embedded.
- Keep model dimensions aligned strictly between the Python `sentence-transformers` service and the Postgres `pgvector` schema.
- Build idempotent re-indexing scripts (`ai:index`) supporting incremental updates.

## 3. Hybrid Retrieval & Evaluation
- Combine dense vector similarity with lexical search (Postgres `tsvector` / BM25) via Reciprocal Rank Fusion (RRF) for exact identifiers, codes, and names.
- Evaluate retrieval quality separately from generation using a small golden query set (Recall@K / MRR) before tuning prompts.

## 4. Structured & Safe LLM Outputs
- Enforce JSON Schema / Pydantic validation on agent tool outputs and structured extractions, with bounded retries on schema mismatch.
- Sanitize retrieved external documents as untrusted data to mitigate indirect prompt injection, and cap max context tokens per retrieval call.
