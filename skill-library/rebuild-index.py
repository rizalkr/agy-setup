#!/usr/bin/env python3
"""Rebuild ~/.gemini/skill-library/INDEX.md from categorized SKILL.md files."""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "INDEX.md"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", re.DOTALL)


def parse_frontmatter(skill_md: Path) -> tuple[str, str]:
    """Extract name and description from SKILL.md YAML frontmatter."""
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    default_name = skill_md.parent.name
    if not match:
        return default_name, "No description provided."

    lines = match.group(1).splitlines()
    data: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        key_match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not key_match:
            i += 1
            continue

        key = key_match.group(1).strip()
        raw_val = key_match.group(2).strip()
        if raw_val in {">", ">-", "|", "|-"}:
            block_lines: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == "":
                    block_lines.append("")
                    i += 1
                elif next_line.startswith((" ", "\t")):
                    block_lines.append(next_line.strip())
                    i += 1
                else:
                    break
            data[key] = " ".join(part for part in block_lines if part).strip()
            continue

        if (raw_val.startswith('"') and raw_val.endswith('"')) or (
            raw_val.startswith("'") and raw_val.endswith("'")
        ):
            raw_val = raw_val[1:-1]
        data[key] = raw_val
        i += 1

    name = data.get("name") or default_name
    desc = re.sub(r"\s+", " ", data.get("description") or "No description provided.").strip()
    return name, desc


def build_index() -> str:
    """Scan category directories and render a compact Markdown index."""
    categories = sorted(
        p for p in BASE_DIR.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))
    )

    sections: list[str] = []
    total_skills = 0

    for cat_dir in categories:
        skill_files = sorted(cat_dir.glob("*/SKILL.md"))
        lines = [f"## {cat_dir.name} ({len(skill_files)})"]
        if not skill_files:
            lines.append("_No skills installed yet._")
        else:
            lines.append("| Skill | Description | Path |")
            lines.append("| :--- | :--- | :--- |")
            for skill_md in skill_files:
                name, desc = parse_frontmatter(skill_md)
                safe_desc = desc.replace("|", "\\|")
                portable_path = f"~/.gemini/skill-library/{cat_dir.name}/{skill_md.parent.name}/SKILL.md"
                lines.append(f"| `{name}` | {safe_desc} | `{portable_path}` |")
                total_skills += 1
        sections.append("\n".join(lines))

    header = [
        "# Skill Library Index",
        "",
        f"Total indexed skills: {total_skills}. Run `agy-index-skills` after adding or updating skills.",
        "",
    ]
    return "\n".join(header) + "\n\n".join(sections) + "\n"


def main() -> None:
    INDEX_PATH.write_text(build_index(), encoding="utf-8")


if __name__ == "__main__":
    main()
