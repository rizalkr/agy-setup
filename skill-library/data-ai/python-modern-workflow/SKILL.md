---
name: python-modern-workflow
description: Modern Python virtual environment management, dependency detection (uv/Poetry/.venv), one-line pre-flight probes, ruff linting, pytest, and typing. Use before installing packages, initializing Python projects, or running Python scripts.
---

# Modern Python Workflow & Dependency Management

## 1. Dependency Manager Detection (Priority Order)
Before installing any package or running scripts, check workspace lock/config files in a single command (`ls uv.lock poetry.lock Pipfile environment.yml requirements.txt pyproject.toml 2>/dev/null`):

1. `uv.lock` or `pyproject.toml` with `[tool.uv]` -> **uv** (`uv add <pkg>`, `uv sync`, `uv run <cmd>`)
2. `pyproject.toml` with `[tool.poetry]` -> **Poetry** (`poetry add <pkg>`, `poetry install`, `poetry run <cmd>`)
3. `Pipfile` -> **Pipenv** (`pipenv install <pkg>`, `pipenv run <cmd>`)
4. `environment.yml` -> **Conda** (`conda install <pkg>`, `conda env create -f environment.yml`)
5. `requirements.txt` or none of the above -> **uv** (for greenfield projects) or **`.venv` + pip** (`python3 -m venv .venv`, `.venv/bin/pip install <pkg>`, `.venv/bin/pip freeze > requirements.txt`).

**Strict Rules:**
- **NEVER** run global `pip install` outside an isolated virtual environment.
- **NEVER** override an existing project's dependency manager with a different one.

## 2. Composite Pre-Flight Environment Probe
Combine Python version, active interpreter, and package availability checks into a single composite command instead of sequential shell calls:
```bash
python3 -c "import sys, importlib.util; print(sys.executable, sys.version.split()[0]); [print(p, importlib.util.find_spec(p) is not None) for p in ['numpy', 'pandas', 'polars', 'pytest']]"
```

## 3. Modern Python Engineering Defaults
- **Project Layout**: Prefer `pyproject.toml` over legacy `setup.py`; pin minimum Python version and separate `[dependency-groups]` / optional dev dependencies.
- **Linting & Formatting**: Run `ruff check --fix .` and `ruff format .` instead of legacy flake8/black/isort chains.
- **Testing**: Use `pytest` with deterministic fixtures, `tmp_path`, and `monkeypatch`; run targeted tests first (`pytest tests/test_target.py -q`).
- **Typing**: Add `from __future__ import annotations` for Python 3.9+ compatibility with `X | None` union syntax and `list[str]` / `dict[str, Any]` generics.
