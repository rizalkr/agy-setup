#!/usr/bin/env python3
"""PreInvocation Context Guardian hook for Antigravity CLI, App, and IDE."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

DEFAULT_THRESHOLDS = {
    "preset": "neon-balanced",
    "yellow_steps": 75,
    "yellow_cooldown": 35,
    "yellow_tokens": 85_000,
    "red_steps": 120,
    "red_cooldown": 25,
    "red_tokens": 135_000,
}

MIN_PEAK_FOR_COMPACT_DROP = 40_000
COMPACT_DROP_RATIO = 0.75
MAX_STATE_ENTRIES = 50


def load_thresholds(home_dir: Path) -> dict:
    """Load active preset thresholds from ~/.gemini/config/hooks/preset.json."""
    thresholds = dict(DEFAULT_THRESHOLDS)
    preset_path = home_dir / ".gemini/config/hooks/preset.json"
    if not preset_path.is_file():
        return thresholds
    try:
        data = json.loads(preset_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in DEFAULT_THRESHOLDS:
                if key in data and (
                    isinstance(data[key], int) or (key == "preset" and isinstance(data[key], str))
                ):
                    thresholds[key] = data[key]
    except Exception:
        pass
    return thresholds


def resolve_transcript(payload: dict, home_dir: Path) -> Path | None:
    """Resolve transcript.jsonl from payload or conversationId brain directory."""
    raw_path = payload.get("transcriptPath")
    if isinstance(raw_path, str) and raw_path:
        candidate = Path(raw_path).expanduser()
        if candidate.is_file():
            return candidate

    conv_id = payload.get("conversationId")
    if isinstance(conv_id, str) and conv_id:
        for product in ("antigravity-cli", "antigravity", "antigravity-ide"):
            candidate = (
                home_dir
                / ".gemini"
                / product
                / "brain"
                / conv_id
                / ".system_generated"
                / "logs"
                / "transcript.jsonl"
            )
            if candidate.is_file():
                return candidate
    return None


def inspect_transcript(transcript_path: Path | None, fallback_steps: int) -> tuple[int, int, int]:
    """Return (total_steps, last_compact_step, latest_tokens) from transcript.jsonl."""
    if not transcript_path or not transcript_path.is_file():
        return fallback_steps, 0, 0

    total_steps = fallback_steps
    last_compact_step = 0
    latest_tokens = 0
    peak_tokens = 0
    line_count = 0

    with transcript_path.open("r", encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            line_count += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            step_idx = entry.get("step_index")
            if not isinstance(step_idx, int):
                step_idx = line_count - 1
            if step_idx + 1 > total_steps:
                total_steps = step_idx + 1

            if entry.get("source") == "USER_EXPLICIT":
                content = str(entry.get("content", ""))
                if "<USER_REQUEST>" in content:
                    after_tag = content.split("<USER_REQUEST>", 1)[1].lstrip()
                else:
                    after_tag = content.lstrip()
                if after_tag.startswith("/compact"):
                    last_compact_step = step_idx
                    peak_tokens = 0

            if entry.get("source") == "MODEL":
                inp = entry.get("input_tokens")
                cache = entry.get("cache_read_tokens")
                if isinstance(inp, int) or isinstance(cache, int):
                    tokens = (inp if isinstance(inp, int) else 0) + (
                        cache if isinstance(cache, int) else 0
                    )
                    if tokens > 0:
                        if (
                            peak_tokens >= MIN_PEAK_FOR_COMPACT_DROP
                            and tokens <= int(peak_tokens * COMPACT_DROP_RATIO)
                        ):
                            last_compact_step = step_idx
                            peak_tokens = tokens
                        elif tokens > peak_tokens:
                            peak_tokens = tokens
                        latest_tokens = tokens

    if line_count > total_steps:
        total_steps = line_count
    return total_steps, last_compact_step, latest_tokens


def load_state(state_path: Path) -> dict:
    """Load persisted cooldown state safely."""
    if not state_path.is_file():
        return {}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_state(state_path: Path, state: dict) -> None:
    """Persist up to MAX_STATE_ENTRIES recent conversation states."""
    if len(state) > MAX_STATE_ENTRIES:
        sorted_items = sorted(
            state.items(),
            key=lambda kv: kv[1].get("updated_at", 0) if isinstance(kv[1], dict) else 0,
            reverse=True,
        )[:MAX_STATE_ENTRIES]
        state = dict(sorted_items)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def evaluate_zone(steps_since_compact: int, latest_tokens: int, thresholds: dict) -> str:
    """Determine GREEN, YELLOW, or RED zone."""
    if (
        steps_since_compact >= thresholds["red_steps"]
        or latest_tokens >= thresholds["red_tokens"]
    ):
        return "RED"
    if (
        steps_since_compact >= thresholds["yellow_steps"]
        or latest_tokens >= thresholds["yellow_tokens"]
    ):
        return "YELLOW"
    return "GREEN"


def should_notify(
    zone: str,
    total_steps: int,
    last_compact_step: int,
    conv_state: dict | None,
    thresholds: dict,
) -> bool:
    """Apply cooldown and zone-escalation rules."""
    if zone == "GREEN":
        return False
    if not isinstance(conv_state, dict):
        return True
    if conv_state.get("last_compact_step") != last_compact_step:
        return True

    prev_zone = conv_state.get("zone", "GREEN")
    if prev_zone == "GREEN":
        return True
    if prev_zone == "YELLOW" and zone == "RED":
        return True

    last_warn_step = conv_state.get("last_warn_step", 0)
    cooldown = thresholds["red_cooldown"] if zone == "RED" else thresholds["yellow_cooldown"]
    return (total_steps - last_warn_step) >= cooldown


def run_guardian() -> dict:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    if not isinstance(payload, dict):
        return {}

    home_dir = Path.home()
    thresholds = load_thresholds(home_dir)
    fallback_steps = payload.get("initialNumSteps")
    if not isinstance(fallback_steps, int):
        fallback_steps = 0

    transcript_path = resolve_transcript(payload, home_dir)
    total_steps, last_compact_step, latest_tokens = inspect_transcript(
        transcript_path, fallback_steps
    )
    steps_since_compact = max(0, total_steps - last_compact_step)
    zone = evaluate_zone(steps_since_compact, latest_tokens, thresholds)

    if zone == "GREEN":
        return {}

    conv_id = str(payload.get("conversationId") or "default")
    state_path = home_dir / ".gemini/cache/context_guardian_state.json"
    all_state = load_state(state_path)
    conv_state = all_state.get(conv_id)

    if not should_notify(zone, total_steps, last_compact_step, conv_state, thresholds):
        return {}

    all_state[conv_id] = {
        "zone": zone,
        "last_warn_step": total_steps,
        "last_compact_step": last_compact_step,
        "updated_at": time.time(),
    }
    save_state(state_path, all_state)

    preset_name = thresholds["preset"]
    token_label = f"~{round(latest_tokens / 1000)}k" if latest_tokens > 0 else "unknown"
    if zone == "YELLOW":
        msg = (
            f"[CONTEXT_GUARDIAN: ZONA KUNING | preset={preset_name} | "
            f"{steps_since_compact} steps since last compact | {token_label} active tokens] "
            "Follow the Context Compaction & Session Handoff Pakem in GEMINI.md: do NOT "
            "recommend /compact if a bug fix or multi-step edit is still unfinished; if a "
            "milestone just completed or all tasks are done, append the Zona Kuning "
            "recommendation block at the end of your response."
        )
    else:
        msg = (
            f"[CONTEXT_GUARDIAN: ZONA MERAH | preset={preset_name} | "
            f"{steps_since_compact} steps since last compact | {token_label} active tokens] "
            "Follow the Context Compaction & Session Handoff Pakem in GEMINI.md: append the "
            "Zona Merah warning block at the end of your response with a ready-to-copy "
            "'/compact <context + next step>' command (if tasks remain) or a '/clear' + "
            "New Session Handoff Prompt (if all tasks are complete or switching topics)."
        )

    return {"injectSteps": [{"systemMessage": {"systemMessage": msg}}]}


def main() -> None:
    try:
        output = run_guardian()
    except Exception:
        output = {}
    sys.stdout.write(json.dumps(output) + "\n")


if __name__ == "__main__":
    main()
