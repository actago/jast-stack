"""Validate portable skill folders without touching an agent installation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


def validate(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        return 0, ["No skills found"]
    for entry in skills:
        folder = entry.parent.resolve()
        prefix = folder.name
        content = entry.read_text(encoding="utf-8-sig")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.S)
        if not match:
            errors.append(f"{prefix}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"{prefix}: invalid YAML: {exc}")
            continue
        if not isinstance(meta, dict):
            errors.append(f"{prefix}: frontmatter must be a mapping")
            continue
        name = meta.get("name")
        if name != prefix or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(name)):
            errors.append(f"{prefix}: name must match the folder in hyphen-case")
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{prefix}: missing or oversized description")
        for required in ("references/sources.md", "evaluation.md"):
            if not (folder / required).is_file():
                errors.append(f"{prefix}: missing {required}")
        for doc in folder.rglob("*.md"):
            text = doc.read_text(encoding="utf-8-sig")
            # Remove fenced examples so placeholder links are not treated as resources.
            text = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                target = target.strip().strip("<>")
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                dest = (doc.parent / target.split("#", 1)[0]).resolve()
                if not dest.is_relative_to(folder):
                    errors.append(f"{prefix}: non-portable relative link in {doc.name}: {target}")
                elif not dest.exists():
                    errors.append(f"{prefix}: broken link in {doc.name}: {target}")
    return len(skills), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    count, errors = validate(args.root.resolve())
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{count} skills checked; {len(errors)} errors")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
