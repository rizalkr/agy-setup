---
name: office-docs-guidebook-automation
description: Automated creation of DOCX guidebooks, XLSX spreadsheets, PDF exports via LibreOffice, and deterministic headless Chrome CDP screenshot pipelines. Use when generating user manuals, reports, or visual documentation.
---

# Office Docs & Guidebook Automation

## 1. Deterministic Screenshot Pipelines (Headless Chrome / Playwright)
- Seed deterministic demo data first (e.g., via seeder/artisan command) and verify DB record IDs exist before capturing pages.
- Reuse an authenticated session cookie/CSRF flow and wait for network idle plus key UI selectors before capturing PNGs.
- Use consistent viewport dimensions (e.g., `1440x900` for desktop, `390x844` for mobile) and avoid overlapping sticky headers or leftover debug banners.
- Inspect generated screenshots visually only on representative samples or failed pages to save tokens.

## 2. Programmatic DOCX Generation (`python-docx`)
- Build documents via a reusable script in an isolated `.venv` using consistent heading hierarchy (`Heading 1..3`), custom table cell padding/borders, and explicit `Inches(...)` image widths that fit page margins.
- Keep Markdown source as the single source of truth (`00_*.md .. NN_*.md`) and compile `.docx` cleanly from Markdown so edits remain diffable in Git.
- Insert page breaks intentionally before major sections and prevent table rows from splitting awkwardly (`cantSplit`).

## 3. PDF & Spreadsheet Conversion
- Convert `.docx` -> `.pdf` deterministically via headless LibreOffice:
  - `libreoffice --headless --convert-to pdf --outdir <out_dir> <file.docx>`
- Use `openpyxl` for styled `.xlsx` reports (frozen header rows, auto-fitted column widths, explicit number/currency formats).
