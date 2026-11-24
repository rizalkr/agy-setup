---
name: python-data-ml-scraping
description: Python data engineering, Scikit-Learn ML pipelines (fraud/anomaly detection), resilient web scraping, and PDF-to-Markdown extraction. Use when working with Pandas, Scikit-Learn, scraping scripts, or document extraction tools.
---

# Python Data, ML & Scraping

## 1. Pandas, Polars & Scikit-Learn Discipline
- Prefer vectorized NumPy/Pandas operations over `.iterrows()`; for large tabular datasets (>500 MB), prefer `polars`, `duckdb`, or `pyarrow` + Parquet over CSV/Pandas.
- Validate schema, nulls, and dtypes immediately on ingestion, and downcast numeric/categorical columns when memory is constrained.
- Prevent data leakage: fit scalers, encoders, and SMOTE/resamplers strictly inside `sklearn.pipeline.Pipeline` on training folds only (`StratifiedKFold` or time-based splits).
- For imbalanced tasks (e.g., fraud detection), evaluate with Precision-Recall AUC (`average_precision_score`), F1, and confusion matrices at tuned thresholds rather than raw accuracy.

> For `.ipynb` / Google Colab workflows, load `colab-jupyter-notebooks`. For virtual environments and dependency management, load `python-modern-workflow`.

## 2. Resilient Web Scraping
- Reuse `requests.Session()` (or `httpx`) with explicit timeouts, realistic headers, exponential backoff retries on `429`/`5xx`, and polite jittered delays.
- Save progress incrementally (JSONL/SQLite checkpoints) keyed by item ID so interrupted scrapes resume cleanly without duplicate requests.
- Validate parsed fields defensively (`.get()`, regex/schema checks) and separate raw HTML/JSON capture from normalization transforms.

## 3. PDF & Document Extraction
- Keep large PDF/OCR workflows (`marker`, `pypdf`, Whisper) batched and isolated in virtual environments (`uv`/`.venv`) with explicit output directories outside source trees.

## Verification
Verify ML scripts on a deterministic seed and small sample slice before running full dataset training or scraping batches.
