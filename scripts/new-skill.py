#!/usr/bin/env python3
"""Scaffold a new skill in the monorepo.

Usage:
    scripts/new-skill.py <name> "<one-line description>"

Example:
    scripts/new-skill.py fhir-resources "FHIR R4 resource modeling and US Core profiles"

What it does:
    1. Validates args + preconditions (clean tree, validator passes, no clash)
    2. Creates <name>/{SKILL.md, README.md, references/README.md, templates/README.md}
    3. Updates umbrella README.md: tagline, both npx blocks, skills table,
       routing matrix, "Which skill should I install?" list
    4. Updates every existing sibling README's "Related skills" section
       and "one of N skills" prose
    5. Adds an Added bullet to CHANGELOG.md [Unreleased] (creates section if missing)
    6. Runs validator. Prints next-step TODO checklist.

Leaves changes UNSTAGED so you can review with `git diff` before committing.
If anything goes wrong mid-flight, `git checkout -- . && git clean -fd <name>/`
reverts cleanly (precondition: clean tree).
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAME_RE = re.compile(r"^[a-z][a-z0-9-]+$")
NUM_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
}


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def existing_skills() -> list[str]:
    return sorted(p.parent.name for p in ROOT.glob("*/SKILL.md"))


def replace_once(text: str, old: str, new: str, file_label: str) -> str:
    count = text.count(old)
    if count == 0:
        die(f"{file_label}: marker not found: {old!r}")
    if count > 1:
        die(f"{file_label}: marker not unique ({count} matches): {old!r}")
    return text.replace(old, new)


# ---------- skeleton templates ----------

def skill_md(name: str, desc: str, siblings: list[str]) -> str:
    sib_prose = "; ".join(f"for {s.replace('-', ' ')} work see `{s}`" for s in siblings)
    return f"""---
name: {name}
description: '{desc} TODO: pack this description with trigger phrases users will actually type, plus explicit DO NOT USE FOR clauses that defer to sibling skills.'
---

# {name}

You are an expert at TODO. TODO one-paragraph positioning: who you are, what
problem you solve, what you are NOT.

This is one of {NUM_WORDS[len(siblings) + 1]} skills in this monorepo. {sib_prose.capitalize()}.

## 0. Safety & Compliance Gate (run FIRST, every time)

Before doing anything:

1. **PHI check.** TODO: state the PHI / data-sensitivity gate appropriate for this skill.
2. **Scope check.** Confirm the task (see §1). Do not silently broaden into sibling-skill territory.
3. **Disclaimer.** State once per session: *"TODO scope-appropriate disclaimer."*
4. **Never invent.** TODO: anti-fabrication rule for whatever authoritative source this skill cites.
5. **No real PHI in examples.** All examples synthetic, tagged `[synthetic]`.
6. **No clinical / legal / regulatory advice.** TODO: list the deferral classes.

If any gate fails, stop and report back.

## 1. When to Use This Skill

TODO: list trigger phrases users will type. Mirror the `description` field.

- "TODO trigger 1"
- "TODO trigger 2"

**Not** triggered for:

- TODO out-of-scope class 1 (defer to `sibling-skill`)
- TODO out-of-scope class 2

## 2. Workflow

TODO: numbered steps. Reference templates by file.

1. **Safety gate.**
2. **Orient.** TODO.
3. **Produce output.** Use the matching template from `templates/`.

## 3. References

TODO: pointer table to references/.

## 4. Anti-patterns

TODO: what NOT to do.
"""


def readme_md(name: str, desc: str, siblings: list[str]) -> str:
    n = len(siblings) + 1
    sib_prose = "; ".join(f"for {s.replace('-', ' ')} see `{s}`" for s in siblings)
    rel_bullets = "\n".join(
        f"- [`{s}`](../{s}/) - TODO one-line summary of how {name} relates to {s}"
        for s in siblings
    )
    return f"""# {name}

{desc} TODO: 2-3 sentence expansion of the audience and the problem this skill solves.

> ⚠️ TODO: scope-appropriate disclaimer.

This is one of {NUM_WORDS[n]} skills in this monorepo. {sib_prose.capitalize()}.

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill {name}
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## Quick start

> *"TODO example user prompt 1"*

> *"TODO example user prompt 2"*

The agent runs the safety gate from `SKILL.md` §0, then TODO describe workflow, citing references and producing findings using [templates/](templates/).

## When the agent loads it

Triggered by requests like:

- TODO trigger phrase
- TODO trigger phrase

**Not** triggered for: TODO out-of-scope list.

## What it does

1. **Safety gate** - TODO.
2. **TODO step.**
3. **Outputs** a structured result using the matching template.

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, routing |
| [references/](references/) | Deep domain knowledge, loaded on demand |
| [templates/](templates/) | Output formats |

### References (loaded only when needed)

TODO: list once you add reference files.

### Templates

TODO: list once you add template files.

## Related skills in this repo

{rel_bullets}

## Compliance & safety guardrails

The skill enforces:

- TODO guardrail 1
- TODO guardrail 2
"""


def references_readme(name: str) -> str:
    return f"""# {name} references

Deep domain knowledge loaded on demand by `SKILL.md`.

TODO: list each `*.md` here with a one-line description of when it's needed.
"""


def templates_readme(name: str) -> str:
    return f"""# {name} templates

Output formats. The skill picks the matching template based on the requested
audit / artifact type.

TODO: list each `*.md` here with a one-line description of when to use it.
"""


# ---------- repo-wide updaters ----------

def update_umbrella_readme(name: str, desc: str, siblings: list[str]) -> None:
    p = ROOT / "README.md"
    t = p.read_text()
    old_n = len(siblings)
    new_n = old_n + 1

    # 1. Tagline digit bump
    tagline_old = f"**{old_n} healthcare AI agent skills**"
    tagline_new = f"**{new_n} healthcare AI agent skills**"
    t = replace_once(t, tagline_old, tagline_new, "README.md tagline")

    # 2. Quickstart npx block: ends with comment `# All N at once`
    new_npx_line = f"npx skills add Yar177/medical-chart-review-skill --skill {name}"
    quickstart_old = f"# All {NUM_WORDS[old_n]} at once"
    quickstart_new = f"# All {NUM_WORDS[new_n]} at once"
    t = replace_once(
        t,
        f"\n\n{quickstart_old}\n",
        f"\n{new_npx_line}\n\n{quickstart_new}\n",
        "README.md quickstart npx block",
    )

    # 3. Install-section npx block: ends with comment `# Or all N`
    install_old = f"# Or all {NUM_WORDS[old_n]}"
    install_new = f"# Or all {NUM_WORDS[new_n]}"
    t = replace_once(
        t,
        f"\n\n{install_old}\n",
        f"\n{new_npx_line}\n\n{install_new}\n",
        "README.md install npx block",
    )

    # 4. "(or use `--skill '*'` to install all N)" line in Quickstart
    pick_old = f"Pick one (or use `--skill '*'` to install all {NUM_WORDS[old_n]})"
    pick_new = f"Pick one (or use `--skill '*'` to install all {NUM_WORDS[new_n]})"
    if pick_old in t:
        t = t.replace(pick_old, pick_new, 1)

    # 5. Skills table: append a row at the positional end of the table
    # (table is in chronological-add order, not alpha — so we scan for the last
    # `| [` row that occurs after the table header).
    table_header = "| Skill | Audience | What it does |"
    if table_header not in t:
        die("README.md: skills-table header not found")
    lines = t.split("\n")
    in_table = False
    last_table_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == table_header.strip():
            in_table = True
            continue
        if in_table:
            if line.startswith("| ["):
                last_table_idx = i
            elif line.strip() == "" and last_table_idx >= 0:
                break
    if last_table_idx < 0:
        die("README.md: no skills-table rows found")
    new_table_row = (
        f"| [`{name}/`]({name}/) | TODO audience | {desc} TODO expand |"
    )
    lines.insert(last_table_idx + 1, new_table_row)
    t = "\n".join(lines)

    # 6. Routing matrix: append new row before the closing of the matrix.
    # Matrix ends with the healthcare-code-systems row. Use the last sibling row as anchor.
    matrix_anchor_prefix = f"| \"ICD-10"  # heuristic - the last row of the seeded matrix
    # Safer: find the routing-matrix table header and append after the last `|` row.
    matrix_header = "| If the user says... | Load skill |"
    if matrix_header not in t:
        die("README.md: routing matrix header not found")
    # Find matrix bounds
    lines = t.split("\n")
    out = []
    in_matrix = False
    matrix_done = False
    last_matrix_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == matrix_header.strip():
            in_matrix = True
        if in_matrix and not matrix_done:
            if line.startswith("|"):
                last_matrix_idx = i
            elif line.strip() == "" and last_matrix_idx >= 0:
                matrix_done = True
    if last_matrix_idx < 0:
        die("README.md: routing matrix rows not found")
    new_row = f'| "TODO trigger phrase for {name}" | `{name}` |'
    lines.insert(last_matrix_idx + 1, new_row)
    t = "\n".join(lines)

    # 7. "Which skill should I install?" bullet list: insert before the "Building all" bullet
    all_bullet = "- **Building all of the above as a unified platform**"
    if all_bullet not in t:
        die("README.md: 'Building all of the above' bullet not found")
    new_bullet = (
        f"- **TODO use case for {name}** → install [`{name}/`]({name}/)\n"
    )
    t = t.replace(all_bullet, new_bullet + all_bullet, 1)
    # Also update the "install all N" suffix on that bullet
    install_all_old = f"install all {NUM_WORDS[old_n]}"
    install_all_new = f"install all {NUM_WORDS[new_n]}"
    if install_all_old in t:
        t = t.replace(install_all_old, install_all_new, 1)

    p.write_text(t)


def update_sibling_readme(sibling: str, new_name: str, new_desc: str, total_siblings: int) -> None:
    """Update one sibling README: add new skill to 'Related skills' list and bump 'N skills' prose."""
    p = ROOT / sibling / "README.md"
    t = p.read_text()
    new_total = total_siblings + 1  # total skills after the new one is added

    # Bump "one of N skills" / "five skills" / "six skills" etc.
    old_phrase = f"one of {NUM_WORDS[total_siblings]} skills"
    new_phrase = f"one of {NUM_WORDS[new_total]} skills"
    if old_phrase in t:
        t = t.replace(old_phrase, new_phrase)

    # Append bullet to "Related skills in this repo" section
    header = "## Related skills in this repo"
    if header not in t:
        die(f"{sibling}/README.md: '{header}' not found")
    lines = t.split("\n")
    out: list[str] = []
    in_section = False
    last_bullet_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == header:
            in_section = True
        elif in_section and line.startswith("## "):
            in_section = False
        if in_section and line.startswith("- ["):
            last_bullet_idx = i
    if last_bullet_idx < 0:
        die(f"{sibling}/README.md: no bullets found in '{header}' section")
    new_bullet = f"- [`{new_name}`](../{new_name}/) - {new_desc} TODO refine cross-skill summary"
    lines.insert(last_bullet_idx + 1, new_bullet)
    p.write_text("\n".join(lines))


def update_changelog(name: str, desc: str) -> None:
    p = ROOT / "CHANGELOG.md"
    t = p.read_text()
    bullet = f"- New skill: `{name}/` - {desc}"

    if "## [Unreleased]" in t:
        # Insert bullet under existing [Unreleased]. Add ### Added if missing.
        lines = t.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == "## [Unreleased]":
                # Find next non-blank line
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines) and lines[j].startswith("### Added"):
                    # Insert bullet after the ### Added header
                    lines.insert(j + 1, "")
                    lines.insert(j + 2, bullet)
                else:
                    # Insert new ### Added block right after [Unreleased]
                    lines.insert(i + 1, "")
                    lines.insert(i + 2, "### Added")
                    lines.insert(i + 3, "")
                    lines.insert(i + 4, bullet)
                break
        t = "\n".join(lines)
    else:
        # No [Unreleased] section. Insert one above the first version header.
        m = re.search(r"^## \[\d+\.\d+\.\d+\]", t, re.M)
        if not m:
            die("CHANGELOG.md: no version headers found; cannot insert [Unreleased]")
        insertion = (
            "## [Unreleased]\n"
            "\n"
            "### Added\n"
            "\n"
            f"{bullet}\n"
            "\n"
        )
        t = t[: m.start()] + insertion + t[m.start() :]

    p.write_text(t)


# ---------- main ----------

def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)

    name, desc = sys.argv[1], sys.argv[2].strip()

    if not NAME_RE.match(name):
        die(f"name {name!r} must match {NAME_RE.pattern}")
    if not desc:
        die("description must not be empty")
    if not desc.endswith("."):
        desc += "."

    target = ROOT / name
    if target.exists():
        die(f"{name}/ already exists")

    # Precondition: clean working tree
    r = run(["git", "status", "--porcelain"])
    if r.stdout.strip():
        die("working tree not clean. Commit or stash first.")

    # Precondition: validator passes
    r = run(["python3", "scripts/validate-skills.py"])
    if r.returncode != 0:
        die(f"validator currently failing; fix that first:\n{r.stderr}")

    siblings = existing_skills()
    if not siblings:
        die("no existing skills found")
    if name in siblings:
        die(f"{name!r} is already a sibling skill")

    print(f">> scaffolding {name} (siblings: {', '.join(siblings)})")

    # Create skill dir + files
    target.mkdir()
    (target / "references").mkdir()
    (target / "templates").mkdir()
    (target / "SKILL.md").write_text(skill_md(name, desc, siblings))
    (target / "README.md").write_text(readme_md(name, desc, siblings))
    (target / "references" / "README.md").write_text(references_readme(name))
    (target / "templates" / "README.md").write_text(templates_readme(name))
    print(f"   created {name}/{{SKILL.md, README.md, references/README.md, templates/README.md}}")

    # Update repo-wide files
    update_umbrella_readme(name, desc, siblings)
    print("   updated README.md (tagline, npx blocks, table, routing matrix, install list)")

    for s in siblings:
        update_sibling_readme(s, name, desc, len(siblings))
    print(f"   updated {len(siblings)} sibling README(s)")

    update_changelog(name, desc)
    print("   updated CHANGELOG.md [Unreleased]")

    # Smoke-test
    print("\n>> running validator...")
    r = run(["python3", "scripts/validate-skills.py"])
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        die("validator failed after scaffold; inspect with `git status`, then `git checkout -- . && git clean -fd " + name + "/` to revert")

    print(f"""
>> scaffold complete. NEXT:

   1. Fill {name}/SKILL.md: pack §0 safety gate, §1 triggers, §2 workflow
   2. Fill {name}/README.md: quick-start prompts, audience prose, layout table
   3. Add real *.md content to {name}/references/ and {name}/templates/
   4. Fill the TODOs in:
      - README.md (skills-table row, routing-matrix row, install-list bullet)
      - {len(siblings)} sibling READMEs ("Related skills" bullets)
      - CHANGELOG.md [Unreleased] entry
   5. Re-run: python3 scripts/validate-skills.py
   6. Commit: git add -A && git commit -m "feat: scaffold {name} skill"

   To revert this scaffold:
      git checkout -- . && git clean -fd {name}/
""")


if __name__ == "__main__":
    main()
