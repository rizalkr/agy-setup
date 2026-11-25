#!/usr/bin/env python3
"""Cross-platform sync script to copy ~/.gemini customizations back into this repo."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


CORE_SKILLS = (
    "find-skills",
    "graphify",
    "lean-code",
    "read-only-agent",
    "security-audit",
    "skill-router",
)

PORTABLE_GUARDIAN_CMD = "python3 ~/.gemini/config/hooks/context-guardian.py"


def replace_dir_contents(
    src_root: Path,
    dst_root: Path,
    only_names: tuple[str, ...] | None = None,
) -> None:
    """Clean dst_root and copy src_root contents without Python cache files."""
    if dst_root.exists():
        shutil.rmtree(dst_root)
    dst_root.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    for item in src_root.iterdir():
        if only_names is not None and item.name not in only_names:
            continue
        target = dst_root / item.name
        if item.is_dir():
            shutil.copytree(item, target, ignore=ignore)
        else:
            shutil.copy2(item, target)


def sync_hooks_json(hooks_json_src: Path, hooks_json_dst: Path) -> None:
    """Sync only the context-guardian hook with a portable POSIX command."""
    if not hooks_json_src.is_file():
        return
    data = json.loads(hooks_json_src.read_text(encoding="utf-8"))
    guardian = data.get("context-guardian")
    if not isinstance(guardian, dict):
        return
    pre_inv = guardian.get("PreInvocation")
    if isinstance(pre_inv, list) and pre_inv and isinstance(pre_inv[0], dict):
        pre_inv[0]["command"] = PORTABLE_GUARDIAN_CMD
    hooks_json_dst.write_text(
        json.dumps({"context-guardian": guardian}, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_setup(home_dir: Path | None = None, repo_dir: Path | None = None) -> None:
    resolved_repo = repo_dir or Path(__file__).resolve().parent
    resolved_home = home_dir or Path.home()
    gemini_dir = resolved_home / ".gemini"

    (resolved_repo / "rules").mkdir(parents=True, exist_ok=True)
    (resolved_repo / "hooks").mkdir(parents=True, exist_ok=True)
    shutil.copy2(gemini_dir / "GEMINI.md", resolved_repo / "rules/global-GEMINI.md")
    shutil.copy2(resolved_home / "GEMINI.md", resolved_repo / "rules/workspace-GEMINI.md")

    core_skills_src = gemini_dir / "config/skills"
    replace_dir_contents(core_skills_src, resolved_repo / "core-skills", only_names=CORE_SKILLS)
    replace_dir_contents(gemini_dir / "skill-library", resolved_repo / "skill-library")

    hook_src = gemini_dir / "config/hooks/context-guardian.py"
    if hook_src.is_file():
        shutil.copy2(hook_src, resolved_repo / "hooks/context-guardian.py")
    sync_hooks_json(gemini_dir / "config/hooks.json", resolved_repo / "hooks/hooks.json")

    subprocess.run([sys.executable, str(resolved_repo / "skill-library/rebuild-index.py")], check=True)
    print(f"Synced rules, hooks, core-skills, and skill-library into {resolved_repo}.")


def main() -> None:
    sync_setup()


if __name__ == "__main__":
    main()
