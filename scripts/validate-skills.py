#!/usr/bin/env python3
"""Validate skill structure across the monorepo.

Hard checks (exit 1 on failure):
- every top-level dir with SKILL.md is a skill
- SKILL.md frontmatter parses, name matches folder, description non-empty
- references/ and templates/ exist per skill
- every relative [text](path.md) link inside a skill resolves
- CITATION.cff parses and has version
- CHANGELOG.md first version header is [Unreleased] or [X.Y.Z] - YYYY-MM-DD

Soft warnings (no exit):
- mismatched "N reference files" / "N template files" claims vs actual file counts

Runnable locally: `python3 scripts/validate-skills.py`
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []
warnings: list[str] = []

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.S)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
COUNT_RE = re.compile(r"\b(\d+)\s+(reference|template)\s+files?\b", re.IGNORECASE)
VERSION_HEADER_RE = re.compile(
    r"^##\s+\[([^\]]+)\](?:\s+-\s+(\d{4}-\d{2}-\d{2}))?", re.M
)


def find_skills() -> list[Path]:
    return sorted(p.parent for p in ROOT.glob("*/SKILL.md"))


def parse_frontmatter(skill_md: Path) -> dict | None:
    text = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{skill_md.relative_to(ROOT)}: YAML parse error: {exc}")
        return None
    return data if isinstance(data, dict) else None


def check_skill(skill_dir: Path) -> None:
    name = skill_dir.name
    fm = parse_frontmatter(skill_dir / "SKILL.md")
    if fm is None:
        errors.append(f"{name}: SKILL.md has no valid YAML frontmatter")
        return

    if fm.get("name") != name:
        errors.append(
            f"{name}: frontmatter name={fm.get('name')!r} does not match folder"
        )

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{name}: frontmatter description missing or empty")

    for sub in ("references", "templates"):
        if not (skill_dir / sub).is_dir():
            errors.append(f"{name}: missing {sub}/ directory")

    check_links(skill_dir)
    check_counts(skill_dir)


def check_links(skill_dir: Path) -> None:
    for md in skill_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                rel = md.relative_to(ROOT)
                errors.append(f"{rel}: broken link -> {target}")


def check_counts(skill_dir: Path) -> None:
    refs = skill_dir / "references"
    tmpls = skill_dir / "templates"
    ref_count = sum(
        1 for p in refs.glob("*.md") if p.name != "README.md"
    ) if refs.exists() else 0
    tmpl_count = sum(
        1 for p in tmpls.glob("*.md") if p.name != "README.md"
    ) if tmpls.exists() else 0
    expected = {"reference": ref_count, "template": tmpl_count}

    candidates = [
        skill_dir / "SKILL.md",
        skill_dir / "README.md",
        refs / "README.md",
        tmpls / "README.md",
    ]
    for md in candidates:
        if not md.exists():
            continue
        text = md.read_text(encoding="utf-8")
        for match in COUNT_RE.finditer(text):
            n = int(match.group(1))
            kind = match.group(2).lower()
            if n != expected[kind]:
                rel = md.relative_to(ROOT)
                warnings.append(
                    f"{rel}: claims {n} {kind} files, actual {expected[kind]}"
                )


def check_root() -> None:
    cff = ROOT / "CITATION.cff"
    if not cff.exists():
        errors.append("CITATION.cff: not found")
    else:
        try:
            data = yaml.safe_load(cff.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"CITATION.cff: YAML parse error: {exc}")
            data = None
        if isinstance(data, dict) and not data.get("version"):
            errors.append("CITATION.cff: missing version field")

    chg = ROOT / "CHANGELOG.md"
    if not chg.exists():
        errors.append("CHANGELOG.md: not found")
        return
    text = chg.read_text(encoding="utf-8")
    m = VERSION_HEADER_RE.search(text)
    if not m:
        errors.append("CHANGELOG.md: no version header found")
        return
    ver, date = m.group(1), m.group(2)
    if ver != "Unreleased" and not re.match(r"^\d+\.\d+\.\d+$", ver):
        errors.append(
            f"CHANGELOG.md: first header [{ver}] not 'Unreleased' or X.Y.Z"
        )
    if ver != "Unreleased" and not date:
        errors.append(f"CHANGELOG.md: version {ver} missing date (YYYY-MM-DD)")


def main() -> int:
    skills = find_skills()
    if not skills:
        errors.append("no skills found (no */SKILL.md at repo root)")

    for s in skills:
        check_skill(s)
    check_root()

    print(
        f"Validated {len(skills)} skill(s): "
        f"{', '.join(s.name for s in skills)}"
    )

    for w in warnings:
        print(f"WARN  {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)

    if errors:
        print(
            f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1
    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
