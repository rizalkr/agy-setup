#!/usr/bin/env python3
"""Cross-platform installer for Antigravity (Windows, macOS, and Linux)."""

from __future__ import annotations

import argparse
import json
import os
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


def prune_non_core_skills(skills_dir: Path, prune_all: bool = False) -> None:
    """Remove DataCloud auto-injected skills, and optionally non-core entries."""
    if not skills_dir.is_dir():
        return
    manifest = skills_dir / ".datacloud_skills_manifest"
    if manifest.is_file():
        try:
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
            skills = manifest_data.get("skills", {}) if isinstance(manifest_data, dict) else {}
            if isinstance(skills, (dict, list)):
                for name in skills:
                    if (
                        not isinstance(name, str)
                        or name in CORE_SKILLS
                        or Path(name).name != name
                    ):
                        continue
                    target = skills_dir / name
                    if target.is_dir() and not target.is_symlink():
                        shutil.rmtree(target)
                    elif target.exists() or target.is_symlink():
                        target.unlink()
        except (OSError, json.JSONDecodeError):
            pass
        try:
            manifest.unlink()
        except OSError:
            pass
    if not prune_all:
        return
    for item in skills_dir.iterdir():
        if item.name in CORE_SKILLS:
            continue
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()


def backup_if_different(src: Path, dst: Path) -> Path | None:
    """Create a .bak copy of dst before overwriting if its contents differ from src."""
    if not dst.is_file():
        return None
    if dst.read_bytes() == src.read_bytes():
        return None
    backup_path = dst.with_name(f"{dst.name}.bak")
    shutil.copy2(dst, backup_path)
    print(f"Backed up existing {dst} -> {backup_path}")
    return backup_path


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
    """Create an empty mcpServers config if missing or empty/whitespace-only."""
    needs_write = not path.exists()
    if not needs_write:
        needs_write = not path.read_text(encoding="utf-8", errors="replace").strip()
    if needs_write:
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


def resolve_preset(presets_cfg: dict, raw_choice: str | None, interactive: bool) -> tuple[str, dict]:
    """Resolve preset name from CLI argument or interactive prompt."""
    aliases = presets_cfg.get("aliases", {})
    presets = presets_cfg["presets"]
    default_name = presets_cfg.get("default", "neon-balanced")
    default_id = presets[default_name]["id"]

    if interactive:
        print("\nSelect Antigravity Token & Quality Preset:")
        ordered_keys = sorted(presets.keys(), key=lambda k: int(presets[k]["id"]))
        current_family = None
        for key in ordered_keys:
            item = presets[key]
            family = item.get("family")
            if family and family != current_family:
                current_family = family
                print(f"\n  --- {family} Series ---")
            orch = item["orchestrator"]
            cg = item["context_guardian"]
            print(
                f"  [{item['id']}] {item['label']} ({key})\n"
                f"      Planner: {orch['planner']} | Executor: {orch['executor']}\n"
                f"      Compact zones: Yellow {cg['yellow_steps']} steps / Red {cg['red_steps']} steps\n"
                f"      {item['description']}"
            )
        choice = (
            input(f"\nEnter choice [1-{len(ordered_keys)} or preset name] (default {default_id}): ")
            .strip()
            .lower()
            or default_id
        )
        raw_choice = choice

    if not raw_choice:
        return default_name, presets[default_name]

    normalized = raw_choice.strip().lower()
    name = aliases.get(normalized, normalized)
    if name not in presets:
        valid = ", ".join(list(aliases.keys()) + list(presets.keys()))
        raise SystemExit(f"Unknown preset '{raw_choice}'. Valid options: {valid}")
    return name, presets[name]


def write_preset_config(home_dir: Path, preset_name: str, preset_data: dict) -> None:
    """Write active Context Guardian preset thresholds."""
    preset_target = home_dir / ".gemini/config/hooks/preset.json"
    preset_target.parent.mkdir(parents=True, exist_ok=True)
    preset_payload = {"preset": preset_name, **preset_data["context_guardian"]}
    preset_target.write_text(json.dumps(preset_payload, indent=2) + "\n", encoding="utf-8")


def apply_settings_merge(
    repo_dir: Path,
    home_dir: Path,
    local_bin: Path,
    with_hooks: bool,
    preset_name: str,
    preset_data: dict,
    no_orchestrator: bool = False,
) -> None:
    """Safely merge preset Orchestrator settings, hooks, and plugin flags."""
    cli_example = json.loads(
        (repo_dir / "settings/cli-settings.example.json").read_text(encoding="utf-8")
    )
    cli_example["model"] = preset_data["model"]
    cli_example["orchestrator"] = preset_data["orchestrator"]

    cli_target = home_dir / ".gemini/antigravity-cli/settings.json"
    orchestrator_keys = ("model", "orchestrator")
    preference_keys = (
        "agentMode",
        "artifactReviewPolicy",
        "colorScheme",
        "vimInsertFirst",
        "showThinking",
    )

    if cli_target.exists():
        cli_data = json.loads(cli_target.read_text(encoding="utf-8"))
        if not no_orchestrator:
            for key in orchestrator_keys:
                if key in cli_example:
                    cli_data[key] = cli_example[key]
        for key in preference_keys:
            if key in cli_example:
                cli_data.setdefault(key, cli_example[key])
    else:
        cli_data = dict(cli_example)
        if no_orchestrator:
            for key in orchestrator_keys:
                cli_data.pop(key, None)
    cli_target.write_text(json.dumps(cli_data, indent=2) + "\n", encoding="utf-8")

    write_preset_config(home_dir, preset_name, preset_data)

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

        before_tool = settings_data.setdefault("hooks", {}).setdefault("BeforeTool", [])
        already_configured = any(
            isinstance(hook.get("command"), str)
            and "graphify" in hook["command"]
            and "hook-guard" in hook["command"]
            for entry in before_tool
            if isinstance(entry, dict)
            for hook in entry.get("hooks", [])
            if isinstance(hook, dict)
        )
        if not already_configured:
            example_entries = hooks_example.get("hooks", {}).get("BeforeTool", [])
            if graphify_bin:
                quoted_bin = f'"{graphify_bin}"' if " " in graphify_bin else graphify_bin
                for entry in example_entries:
                    for hook in entry.get("hooks", []):
                        cmd = hook.get("command")
                        if isinstance(cmd, str) and "graphify hook-guard" in cmd:
                            hook["command"] = f"{quoted_bin} hook-guard gemini"
            before_tool.extend(example_entries)
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


def install_setup(
    argv: list[str] | None = None,
    home_dir: Path | None = None,
    repo_dir: Path | None = None,
) -> None:
    parser = argparse.ArgumentParser(description="Install Antigravity token-optimized setup.")
    parser.add_argument(
        "--full",
        "--apply-settings",
        dest="apply_settings",
        action="store_true",
        help="Safely merge Orchestrator CLI settings, hooks, and plugin preferences.",
    )
    parser.add_argument(
        "--preset",
        type=str,
        default=None,
        help=(
            "Preset profile: 1/balanced (Argon), 2/ultra-saver (Argon Saver), 3/max-quality "
            "(Argon Max), 4/neon-balanced (default), 5/neon-saver, 6/neon-max, "
            "7/carbon-balanced, 8/carbon-saver, or 9/carbon-max. Implies --full."
        ),
    )
    parser.add_argument(
        "--choose",
        action="store_true",
        help="Interactively choose a preset profile (1-9: Argon, Neon, or Carbon series). Implies --full.",
    )
    parser.add_argument(
        "--no-orchestrator",
        action="store_true",
        help="Keep existing model/orchestrator settings untouched while applying Context Guardian presets and hooks.",
    )
    parser.add_argument(
        "--prune-skills",
        action="store_true",
        help="Remove non-core skills from ~/.gemini/config/skills/ (by default only DataCloud-injected skills are pruned).",
    )
    parser.add_argument(
        "--with-hooks",
        action="store_true",
        help="Install graphify BeforeTool hook even if graphify is not on PATH yet.",
    )
    args = parser.parse_args(argv)

    if args.preset is not None or args.choose:
        args.apply_settings = True

    resolved_repo = repo_dir or Path(__file__).resolve().parent
    resolved_home = home_dir or Path.home()
    gemini_dir = resolved_home / ".gemini"
    local_bin = resolved_home / ".local/bin"

    presets_cfg = json.loads((resolved_repo / "settings/presets.json").read_text(encoding="utf-8"))
    preset_name, preset_data = resolve_preset(presets_cfg, args.preset, args.choose)

    for folder in (
        gemini_dir / "config/skills",
        gemini_dir / "config/hooks",
        gemini_dir / "antigravity",
        gemini_dir / "antigravity-cli",
        gemini_dir / "skill-library",
        local_bin,
    ):
        folder.mkdir(parents=True, exist_ok=True)

    global_rule_src = resolved_repo / "rules/global-GEMINI.md"
    global_rule_dst = gemini_dir / "GEMINI.md"
    backup_if_different(global_rule_src, global_rule_dst)
    shutil.copy2(global_rule_src, global_rule_dst)

    workspace_rule_src = resolved_repo / "rules/workspace-GEMINI.md"
    workspace_rule_dst = resolved_home / "GEMINI.md"
    backup_if_different(workspace_rule_src, workspace_rule_dst)
    shutil.copy2(workspace_rule_src, workspace_rule_dst)

    copy_dir_contents(resolved_repo / "core-skills", gemini_dir / "config/skills")
    prune_non_core_skills(gemini_dir / "config/skills", prune_all=args.prune_skills)
    copy_dir_contents(resolved_repo / "skill-library", gemini_dir / "skill-library")

    hook_script = gemini_dir / "config/hooks/context-guardian.py"
    shutil.copy2(resolved_repo / "hooks/context-guardian.py", hook_script)
    if os.name != "nt":
        hook_script.chmod(0o755)

    hooks_json_target = gemini_dir / "config/hooks.json"
    hooks_repo_data = json.loads((resolved_repo / "hooks/hooks.json").read_text(encoding="utf-8"))
    raw_hooks = (
        hooks_json_target.read_text(encoding="utf-8").strip()
        if hooks_json_target.exists()
        else ""
    )
    existing_hooks = json.loads(raw_hooks) if raw_hooks else {}
    guardian_hook = hooks_repo_data["context-guardian"]
    if os.name == "nt" or not shutil.which("python3"):
        guardian_hook["PreInvocation"][0]["command"] = f'"{sys.executable}" "{hook_script}"'
    existing_hooks["context-guardian"] = guardian_hook
    hooks_json_target.write_text(json.dumps(existing_hooks, indent=2) + "\n", encoding="utf-8")

    write_preset_config(resolved_home, preset_name, preset_data)

    ensure_empty_mcp(gemini_dir / "config/mcp_config.json")
    ensure_empty_mcp(gemini_dir / "antigravity/mcp_config.json")

    rebuild_script = gemini_dir / "skill-library/rebuild-index.py"
    install_indexer_command(local_bin, rebuild_script)

    if args.apply_settings:
        apply_settings_merge(
            resolved_repo,
            resolved_home,
            local_bin,
            args.with_hooks,
            preset_name,
            preset_data,
            no_orchestrator=args.no_orchestrator,
        )

    subprocess.run([sys.executable, str(rebuild_script)], check=True)

    print(
        f"Antigravity setup installed successfully "
        f"(apply_settings={args.apply_settings}, preset={preset_name}, "
        f"no_orchestrator={args.no_orchestrator})."
    )
    print(f"Templates remain available in: {resolved_repo / 'settings'}")


def main() -> None:
    install_setup()


if __name__ == "__main__":
    main()
