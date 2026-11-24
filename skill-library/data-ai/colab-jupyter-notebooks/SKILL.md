---
name: colab-jupyter-notebooks
description: Google Colab runtime management, Jupyter Notebook performance optimization, and token-safe .ipynb Git hygiene. Use when creating, editing, optimizing, or debugging .ipynb notebooks or Colab workflows.
---

# Google Colab & Jupyter Notebook Optimization

## 1. Google Colab Runtime & Persistence
- Guard Colab-only imports for local portability:
  ```python
  try:
      import google.colab  # noqa: F401
      IN_COLAB = True
  except ImportError:
      IN_COLAB = False
  ```
- Inspect hardware/VRAM early (`!nvidia-smi` or `torch.cuda.get_device_properties(0)`), prefer `torch.amp.autocast("cuda", dtype=torch.bfloat16)` (or `fp16` on T4), and call `torch.cuda.empty_cache()` after heavy phases.
- Mount Google Drive only when `IN_COLAB` is `True` and save training/ETL checkpoints periodically to Drive to survive idle disconnects.
- Store API keys in `google.colab.userdata.get("KEY_NAME")` (or `.env` locally); never hardcode secrets in notebook cells.
- Keep package installs quiet and pinned (`%pip install -q ...`) in a dedicated top setup cell.

## 2. Jupyter Performance & Architecture
- Keep notebooks thin: extract reusable functions/classes into `src/*.py` and enable hot-reloading at the top of the notebook:
  ```python
  %load_ext autoreload
  %autoreload 2
  ```
- For large datasets, prefer Parquet + `polars`/`duckdb`/`pyarrow` over raw CSV + Pandas, and downcast numeric/categorical dtypes early.
- Release large intermediate DataFrames/tensors explicitly (`del df; gc.collect()`).
- **Execution & Validation Discipline**:
  - If a notebook cell-execution tool/MCP is available, follow incremental **generate cell -> execute cell -> validate output** before moving on.
  - Otherwise, write the complete notebook cleanly and validate top-to-bottom in a fresh kernel (`jupyter nbconvert --to notebook --execute --inplace <nb>.ipynb` or `papermill`) to eliminate hidden out-of-order state.
- Ensure the final notebook has zero failed cells and clear markdown section headers.

## 3. Token & Git Hygiene for `.ipynb`
- **Never** read raw large `.ipynb` files directly with `read_file` (base64 images and long cell outputs waste tens of thousands of tokens).
- Inspect notebook code/markdown cells via a one-line Python filter stripping `outputs` (e.g., `python3 -c "import json; nb=json.load(open('nb.ipynb')); [print(f'--- [{i}] {c[\"cell_type\"]} ---\n' + ''.join(c['source'])) for i,c in enumerate(nb['cells'])]"`) or pair with `jupytext` (`.py` percent format).
- Strip outputs before committing to Git using `nbstripout` or `jupyter nbconvert --clear-output --inplace <nb>.ipynb`.
