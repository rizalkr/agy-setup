#!/usr/bin/env python3
"""Cross-platform installer for Antigravity (Windows, macOS, and Linux)."""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def copy_dir_contents(src_root: Path, dst_root: Path) -> None:
    """Recursively copy subdirectories and files from src_root into dst_root."""
    dst_root.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    for item in src_root.iterdir():
        target = dst_root / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True, ignore=ignore)
        else:
            shutil.copy2(item, target)


def ensure_empty_mcp(path: Path) -> None:
    """Create an empty mcpServers config if none exists."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"mcpServers": {}}, indent=2) + "\n", encoding="utf-8")


def install_indexer_command(local_bin: Path, rebuild_script: Path) -> None:
    """Install agy-index-skills command for POSIX (symlink) or Windows (.cmd/.ps1)."""
    local_bin.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        cmd_wrapper = local_bin / "agy-index-skills.cmd"
        ps1_wrapper = local_bin / "agy-index-skills.ps1"
        cmd_wrapper.write_text(
            f'@echo off\r\n"{sys.executable}" "{rebuild_script}" %*\r\n',
            encoding="utf-8",
        )
        ps1_wrapper.write_text(
            f'& "{sys.executable}" "{rebuild_script}" @args\r\n',
            encoding="utf-8",
        )
    else:
        rebuild_script.chmod(0o755)
        link_path = local_bin / "agy-index-skills"
        if link_path.is_symlink() or link_path.exists():
            link_path.unlink()
        link_path.symlink_to(rebuild_script)


def find_graphify_binary(home_dir: Path, local_bin: Path) -> str | None:
    """Locate graphify executable across POSIX and Windows."""
    found = shutil.which("graphify")
    if found:
        return found
    for candidate in (
        local_bin / "graphify",
        local_bin / "graphify.exe",
        home_dir / ".local/bin/graphify",
        home_dir / ".local/bin/graphify.exe",
    ):
        if candidate.is_file():
            return str(candidate)
    return None


def apply_settings_merge(repo_dir: Path, home_dir: Path, local_bin: Path, with_hooks: bool) -> None:
    """Safely merge CLI Orchestrator settings, graphify hooks, and plugin flags."""
    cli_example = json.loads(
        (repo_dir / "settings/cli-settings.example.json").read_text(encoding="utf-8")
    )
    cli_target = home_dir / ".gemini/antigravity-cli/settings.json"
    merge_keys = (
        "model",
        "orchestrator",
        "agentMode",
        "artifactReviewPolicy",
        "colorScheme",
        "vimInsertFirst",
    )

    if cli_target.exists():
        cli_data = json.loads(cli_target.read_text(encoding="utf-8"))
        for key in merge_keys:
            if key in cli_example:
                cli_data[key] = cli_example[key]
    else:
        cli_data = cli_example
    cli_target.write_text(json.dumps(cli_data, indent=2) + "\n", encoding="utf-8")

    graphify_bin = find_graphify_binary(home_dir, local_bin)
    if graphify_bin or with_hooks:
        hooks_example = json.loads(
            (repo_dir / "settings/hooks-settings.example.json").read_text(encoding="utf-8")
        )
        settings_target = home_dir / ".gemini/settings.json"
        if settings_target.exists():
            settings_data = json.loads(settings_target.read_text(encoding="utf-8"))
        else:
            settings_data = {}
        if "hooks" not in settings_data:
            settings_data["hooks"] = hooks_example["hooks"]
            if graphify_bin:
                for entry in settings_data["hooks"].get("BeforeTool", []):
                    for hook in entry.get("hooks", []):
                        cmd = hook.get("command")
                        if isinstance(cmd, str) and "graphify hook-guard" in cmd:
                            hook["command"] = f"{graphify_bin} hook-guard gemini"
        settings_target.write_text(json.dumps(settings_data, indent=2) + "\n", encoding="utf-8")

    config_target = home_dir / ".gemini/config/config.json"
    if config_target.exists():
        config_data = json.loads(config_target.read_text(encoding="utf-8"))
        plugins = config_data.setdefault("plugins", {})
        if isinstance(plugins.get("googlecloudtools.datacloud_telemetry"), dict):
            plugins["googlecloudtools.datacloud_telemetry"]["enabled"] = False
            config_target.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")

    canonical_skills = home_dir / ".gemini/config/skills"
    duplicates = [
        home_dir / ".gemini/skills/graphify",
        home_dir / ".gemini/skills/security-audit",
        home_dir / ".agents/skills/find-skills",
        home_dir / ".agents/skills/security-audit",
    ]
    for dup in duplicates:
        if dup.is_dir() and (canonical_skills / dup.name).is_dir():
            shutil.rmtree(dup)

    legacy_skills_dir = home_dir / ".gemini/skills"
    if legacy_skills_dir.is_dir():
        try:
            legacy_skills_dir.rmdir()
        except OSError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Install Antigravity token-optimized setup.")
    parser.add_argument(
        "--full",
        "--apply-settings",
        dest="apply_settings",
        action="store_true",
        help="Safely merge Orchestrator CLI settings, hooks, and plugin preferences.",
    )
    parser.add_argument(
        "--with-hooks",
        action="store_true",
        help="Install graphify BeforeTool hook even if graphify is not on PATH yet.",
    )
    args = parser.parse_args()

    repo_dir = Path(__file__).resolve().parent
    home_dir = Path.home()
    gemini_dir = home_dir / ".gemini"
    local_bin = home_dir / ".local/bin"

    for folder in (
        gemini_dir / "config/skills",
        gemini_dir / "antigravity",
        gemini_dir / "antigravity-cli",
        gemini_dir / "skill-library",
        local_bin,
    ):
        folder.mkdir(parents=True, exist_ok=True)

    shutil.copy2(repo_dir / "rules/global-GEMINI.md", gemini_dir / "GEMINI.md")
    shutil.copy2(repo_dir / "rules/workspace-GEMINI.md", home_dir / "GEMINI.md")

    copy_dir_contents(repo_dir / "core-skills", gemini_dir / "config/skills")
    copy_dir_contents(repo_dir / "skill-library", gemini_dir / "skill-library")

    ensure_empty_mcp(gemini_dir / "config/mcp_config.json")
    ensure_empty_mcp(gemini_dir / "antigravity/mcp_config.json")

    rebuild_script = gemini_dir / "skill-library/rebuild-index.py"
    install_indexer_command(local_bin, rebuild_script)

    if args.apply_settings:
        apply_settings_merge(repo_dir, home_dir, local_bin, args.with_hooks)

    subprocess.run([sys.executable, str(rebuild_script)], check=True)

    print(f"Antigravity setup installed successfully (apply_settings={args.apply_settings}).")
    print(f"Templates remain available in: {repo_dir / 'settings'}")


if __name__ == "__main__":
    main()
