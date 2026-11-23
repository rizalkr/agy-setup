#!/usr/bin/env python3
"""Cross-platform sync script to copy ~/.gemini customizations back into this repo."""

import shutil
import subprocess
import sys
from pathlib import Path


def replace_dir_contents(src_root: Path, dst_root: Path) -> None:
    """Clean dst_root and copy src_root contents without Python cache files."""
    if dst_root.exists():
        shutil.rmtree(dst_root)
    dst_root.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    for item in src_root.iterdir():
        target = dst_root / item.name
        if item.is_dir():
            shutil.copytree(item, target, ignore=ignore)
        else:
            shutil.copy2(item, target)


def main() -> None:
    repo_dir = Path(__file__).resolve().parent
    home_dir = Path.home()
    gemini_dir = home_dir / ".gemini"

    (repo_dir / "rules").mkdir(parents=True, exist_ok=True)
    (repo_dir / "hooks").mkdir(parents=True, exist_ok=True)
    shutil.copy2(gemini_dir / "GEMINI.md", repo_dir / "rules/global-GEMINI.md")
    shutil.copy2(home_dir / "GEMINI.md", repo_dir / "rules/workspace-GEMINI.md")

    replace_dir_contents(gemini_dir / "config/skills", repo_dir / "core-skills")
    replace_dir_contents(gemini_dir / "skill-library", repo_dir / "skill-library")

    hook_src = gemini_dir / "config/hooks/context-guardian.py"
    if hook_src.is_file():
        shutil.copy2(hook_src, repo_dir / "hooks/context-guardian.py")
    hooks_json_src = gemini_dir / "config/hooks.json"
    if hooks_json_src.is_file():
        shutil.copy2(hooks_json_src, repo_dir / "hooks/hooks.json")

    subprocess.run([sys.executable, str(repo_dir / "skill-library/rebuild-index.py")], check=True)
    print(f"Synced rules, hooks, core-skills, and skill-library into {repo_dir}.")


if __name__ == "__main__":
    main()
