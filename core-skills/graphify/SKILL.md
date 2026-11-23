---
name: graphify
description: "Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, where the question should be treated as a graphify query first. Turns any input (code, docs, papers, images, videos) into a persistent knowledge graph with god nodes, community detection, and query/path/explain tools."
---

# /graphify (Fast-Path Reference)

Turn code, docs, papers, images, or video into a queryable knowledge graph (`graphify-out/`).

## 1. Fast Path: When `graphify-out/graph.json` Exists

Before grepping or reading raw files for a codebase question, query the existing graph first:

```bash
graphify query "<question>"              # BFS traversal (broad context)
graphify query "<question>" --dfs        # DFS traversal (trace a specific flow)
graphify query "<question>" --budget 1500
graphify path "<NodeA>" "<NodeB>"        # Shortest path between two concepts
graphify explain "<Node>"                # Plain-language explanation of a node
```

- If `graphify-out/wiki/index.md` exists, read it for broad navigation instead of scanning raw source directories.
- Read raw source files only for lines located by the graph or an earlier targeted read.
- Read `graphify-out/GRAPH_REPORT.md` only for high-level architecture reviews or when `query`/`path`/`explain` lack context.

## 2. Keeping the Graph Current (Zero LLM Cost)

After modifying code in a project that has `graphify-out/`, run an incremental AST-only update:

```bash
graphify update .
```

## 3. When to Read Full Pipeline Instructions

Do NOT load the full pipeline manual for normal graph queries or `graphify update .`.
Only read `~/.gemini/config/skills/graphify/references/full-pipeline.md` when:
- Building a brand-new knowledge graph from scratch (`/graphify` or `/graphify <path>`)
- Running deep semantic extraction on docs, images, PDFs, or videos (`--mode deep`)
- Cloning or merging GitHub repositories (also see `references/github-and-merge.md`)
- Exporting to Neo4j, FalkorDB, Obsidian, GraphML, or SVG, or starting `--watch` / `--mcp`
- Installing or troubleshooting the `graphify` CLI
