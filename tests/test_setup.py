#!/usr/bin/env python3
"""Stdlib unit tests for agy-setup installer, sync, Context Guardian, and skill indexer."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, rel_path: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


install_mod = load_module("agy_install", "install.py")
sync_mod = load_module("agy_sync", "sync.py")
guardian_mod = load_module("agy_guardian", "hooks/context-guardian.py")
indexer_mod = load_module("agy_indexer", "skill-library/rebuild-index.py")


class InstallTests(unittest.TestCase):
    def test_zero_byte_mcp_is_populated_and_non_empty_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg_mcp = home / ".gemini/config/mcp_config.json"
            agy_mcp = home / ".gemini/antigravity/mcp_config.json"
            cfg_mcp.parent.mkdir(parents=True, exist_ok=True)
            agy_mcp.parent.mkdir(parents=True, exist_ok=True)
            cfg_mcp.write_text("", encoding="utf-8")
            custom_mcp = {"mcpServers": {"custom": {"command": "echo"}}}
            agy_mcp.write_text(json.dumps(custom_mcp), encoding="utf-8")

            install_mod.install_setup(argv=[], home_dir=home, repo_dir=REPO_ROOT)

            self.assertEqual(json.loads(cfg_mcp.read_text(encoding="utf-8")), {"mcpServers": {}})
            self.assertEqual(json.loads(agy_mcp.read_text(encoding="utf-8")), custom_mcp)

    def test_gemini_rules_backup_before_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            global_rule = home / ".gemini/GEMINI.md"
            workspace_rule = home / "GEMINI.md"
            global_rule.parent.mkdir(parents=True, exist_ok=True)
            global_rule.write_text("# My custom global rules\n", encoding="utf-8")
            workspace_rule.write_text("# My custom workspace rules\n", encoding="utf-8")

            install_mod.install_setup(argv=[], home_dir=home, repo_dir=REPO_ROOT)

            self.assertEqual(
                (home / ".gemini/GEMINI.md.bak").read_text(encoding="utf-8"),
                "# My custom global rules\n",
            )
            self.assertEqual(
                (home / "GEMINI.md.bak").read_text(encoding="utf-8"),
                "# My custom workspace rules\n",
            )

            # Re-running when files already match repo must not overwrite .bak
            install_mod.install_setup(argv=[], home_dir=home, repo_dir=REPO_ROOT)
            self.assertEqual(
                (home / ".gemini/GEMINI.md.bak").read_text(encoding="utf-8"),
                "# My custom global rules\n",
            )

    def test_prune_preserves_custom_and_agents_skills_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            skills_dir = home / ".gemini/config/skills"
            custom_skill = skills_dir / "my-custom-skill"
            datacloud_skill = skills_dir / "datacloud-bloat"
            escape_dir = home / ".gemini/config/escape-dir"
            agents_skill = home / ".agents/skills/find-skills"
            for d in (custom_skill, datacloud_skill, escape_dir, agents_skill):
                d.mkdir(parents=True, exist_ok=True)
                (d / "SKILL.md").write_text("# skill\n", encoding="utf-8")
            (skills_dir / ".datacloud_skills_manifest").write_text(
                json.dumps({"skills": {"datacloud-bloat": {}, "../escape-dir": {}}}),
                encoding="utf-8",
            )

            install_mod.install_setup(argv=["--preset", "4"], home_dir=home, repo_dir=REPO_ROOT)

            self.assertTrue(custom_skill.is_dir())
            self.assertFalse(datacloud_skill.exists())
            self.assertTrue(escape_dir.is_dir())
            self.assertFalse((skills_dir / ".datacloud_skills_manifest").exists())
            self.assertTrue(agents_skill.is_dir())

            # Explicit --prune-skills removes non-core skills in ~/.gemini/config/skills
            install_mod.install_setup(argv=["--prune-skills"], home_dir=home, repo_dir=REPO_ROOT)
            self.assertFalse(custom_skill.exists())
            self.assertTrue((skills_dir / "lean-code").is_dir())

    def test_no_orchestrator_preserves_model_and_ux_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cli_settings = home / ".gemini/antigravity-cli/settings.json"
            cli_settings.parent.mkdir(parents=True, exist_ok=True)
            existing = {
                "model": "My Custom Model",
                "orchestrator": {"planner": "Custom P", "executor": "Custom E"},
                "colorScheme": "light",
                "vimInsertFirst": False,
                "agentMode": "plan",
                "showThinking": True,
            }
            cli_settings.write_text(json.dumps(existing), encoding="utf-8")

            install_mod.install_setup(
                argv=["--preset", "2", "--no-orchestrator"], home_dir=home, repo_dir=REPO_ROOT
            )

            updated = json.loads(cli_settings.read_text(encoding="utf-8"))
            self.assertEqual(updated["model"], "My Custom Model")
            self.assertEqual(updated["orchestrator"], existing["orchestrator"])
            self.assertEqual(updated["colorScheme"], "light")
            self.assertFalse(updated["vimInsertFirst"])
            self.assertEqual(updated["agentMode"], "plan")
            self.assertTrue(updated["showThinking"])
            self.assertEqual(updated["artifactReviewPolicy"], "always-proceed")

            preset_data = json.loads(
                (home / ".gemini/config/hooks/preset.json").read_text(encoding="utf-8")
            )
            self.assertEqual(preset_data["preset"], "ultra-saver")

    def test_preset_updates_orchestrator_without_overwriting_ux(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cli_settings = home / ".gemini/antigravity-cli/settings.json"
            cli_settings.parent.mkdir(parents=True, exist_ok=True)
            cli_settings.write_text(
                json.dumps({"colorScheme": "light", "vimInsertFirst": False}),
                encoding="utf-8",
            )

            install_mod.install_setup(argv=["--preset", "1"], home_dir=home, repo_dir=REPO_ROOT)

            updated = json.loads(cli_settings.read_text(encoding="utf-8"))
            self.assertEqual(updated["model"], "Orchestrator (Argon)")
            self.assertEqual(updated["orchestrator"]["planner"], "Gemini 4 Argon (Medium)")
            self.assertEqual(updated["colorScheme"], "light")
            self.assertFalse(updated["vimInsertFirst"])

    def test_minimal_install_writes_default_preset_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_mod.install_setup(argv=[], home_dir=home, repo_dir=REPO_ROOT)
            preset_path = home / ".gemini/config/hooks/preset.json"
            self.assertTrue(preset_path.is_file())
            self.assertEqual(json.loads(preset_path.read_text(encoding="utf-8"))["preset"], "neon-balanced")

    def test_graphify_hook_merges_and_quotes_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            spaced_bin = home / "bin with spaces/graphify"
            spaced_bin.parent.mkdir(parents=True, exist_ok=True)
            spaced_bin.write_text("#!/bin/sh\n", encoding="utf-8")

            settings_path = home / ".gemini/settings.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(
                json.dumps({"hooks": {"AfterTool": [{"matcher": "write_file", "hooks": []}]}}),
                encoding="utf-8",
            )

            with patch.object(install_mod.shutil, "which", return_value=str(spaced_bin)):
                install_mod.install_setup(
                    argv=["--preset", "4", "--with-hooks"], home_dir=home, repo_dir=REPO_ROOT
                )
                # Re-run to ensure idempotency
                install_mod.install_setup(
                    argv=["--preset", "4", "--with-hooks"], home_dir=home, repo_dir=REPO_ROOT
                )

            settings_data = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertIn("AfterTool", settings_data["hooks"])
            before_tool = settings_data["hooks"]["BeforeTool"]
            self.assertEqual(len(before_tool), 1)
            self.assertEqual(
                before_tool[0]["hooks"][0]["command"], f'"{spaced_bin}" hook-guard gemini'
            )


class SyncTests(unittest.TestCase):
    def test_sync_normalizes_hooks_json_and_preserves_custom_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            repo = root / "repo"

            (home / ".gemini/config/skills/my-local-skill").mkdir(parents=True, exist_ok=True)
            (home / ".gemini/config/skills/lean-code").mkdir(parents=True, exist_ok=True)
            (home / ".gemini/config/skills/lean-code/SKILL.md").write_text("# lean\n", encoding="utf-8")
            (home / ".gemini/config/hooks").mkdir(parents=True, exist_ok=True)
            (home / ".gemini/skill-library").mkdir(parents=True, exist_ok=True)
            (home / ".gemini/skill-library/rebuild-index.py").write_text(
                (REPO_ROOT / "skill-library/rebuild-index.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (home / ".gemini/GEMINI.md").write_text("# global\n", encoding="utf-8")
            (home / "GEMINI.md").write_text("# workspace\n", encoding="utf-8")
            (home / ".gemini/config/hooks/context-guardian.py").write_text("# hook\n", encoding="utf-8")
            (home / ".gemini/config/hooks.json").write_text(
                json.dumps(
                    {
                        "context-guardian": {
                            "PreInvocation": [
                                {
                                    "type": "command",
                                    "command": '"C:\\Python312\\python.exe" "C:\\Users\\Test\\context-guardian.py"',
                                    "timeout": 5,
                                }
                            ]
                        },
                        "personal-hook": {"PreInvocation": []},
                    }
                ),
                encoding="utf-8",
            )

            (repo / "skill-library").mkdir(parents=True, exist_ok=True)
            (repo / "skill-library/rebuild-index.py").write_text(
                (REPO_ROOT / "skill-library/rebuild-index.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            sync_mod.sync_setup(home_dir=home, repo_dir=repo)

            # Live custom skill was not deleted
            self.assertTrue((home / ".gemini/config/skills/my-local-skill").is_dir())
            self.assertFalse((repo / "core-skills/my-local-skill").exists())

            synced_hooks = json.loads((repo / "hooks/hooks.json").read_text(encoding="utf-8"))
            self.assertEqual(list(synced_hooks.keys()), ["context-guardian"])
            self.assertEqual(
                synced_hooks["context-guardian"]["PreInvocation"][0]["command"],
                "python3 ~/.gemini/config/hooks/context-guardian.py",
            )


class GuardianAndIndexerTests(unittest.TestCase):
    def test_evaluate_zone_and_cooldown(self) -> None:
        thresholds = guardian_mod.DEFAULT_THRESHOLDS
        self.assertEqual(guardian_mod.evaluate_zone(10, 10_000, thresholds), "GREEN")
        self.assertEqual(guardian_mod.evaluate_zone(75, 10_000, thresholds), "YELLOW")
        self.assertEqual(guardian_mod.evaluate_zone(10, 85_000, thresholds), "YELLOW")
        self.assertEqual(guardian_mod.evaluate_zone(120, 10_000, thresholds), "RED")
        self.assertEqual(guardian_mod.evaluate_zone(10, 135_000, thresholds), "RED")

        self.assertTrue(guardian_mod.should_notify("YELLOW", 75, 0, None, thresholds))
        state = {"zone": "YELLOW", "last_warn_step": 75, "last_compact_step": 0}
        self.assertFalse(guardian_mod.should_notify("YELLOW", 90, 0, state, thresholds))
        self.assertTrue(guardian_mod.should_notify("YELLOW", 110, 0, state, thresholds))
        self.assertTrue(guardian_mod.should_notify("RED", 80, 0, state, thresholds))

    def test_inspect_transcript_compact_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            transcript = Path(tmp) / "transcript.jsonl"
            entries = [
                {"step_index": 0, "source": "MODEL", "input_tokens": 50_000, "cache_read_tokens": 0},
                # 20% drop should NOT trigger compact reset (ratio=0.55)
                {"step_index": 1, "source": "MODEL", "input_tokens": 40_000, "cache_read_tokens": 0},
                # Explicit /compact command
                {"step_index": 2, "source": "USER_EXPLICIT", "content": "<USER_REQUEST>\n/compact\n</USER_REQUEST>"},
                {"step_index": 3, "source": "MODEL", "input_tokens": 12_000, "cache_read_tokens": 0},
            ]
            transcript.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")

            total, last_compact, latest_tokens = guardian_mod.inspect_transcript(transcript, 0)
            self.assertEqual(total, 4)
            self.assertEqual(last_compact, 2)
            self.assertEqual(latest_tokens, 12_000)

    def test_rebuild_index_renders_all_21_skills(self) -> None:
        rendered = indexer_mod.build_index()
        self.assertIn("Total indexed skills: 21.", rendered)
        self.assertIn("`fastapi-pydantic-v2`", rendered)
        self.assertIn("`laravel13-specialist`", rendered)


if __name__ == "__main__":
    unittest.main()
