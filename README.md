# medical-chart-review-skill

A monorepo of healthcare AI agent skills. Each subdirectory is an independently installable [Agent Skill](https://agentskills.io/) packaged for a distinct audience.

> ⚠️ Every skill in this repo produces documentation, engineering, or compliance analysis. None of them provide medical advice. Final clinical, coding, regulatory, and compliance decisions require credentialed humans.

## Skills in this repo

| Skill | Audience | What it does |
|---|---|---|
| [`medical-chart-review/`](medical-chart-review/) | Clinicians, CRC/CCS coders, CDI specialists, quality auditors | Reads charts, validates documentation against coding and quality standards, produces auditable findings and provider queries |
| [`hedis-nlp/`](hedis-nlp/) | Data-science / NLP engineering teams | Per-measure HEDIS extractor design, DoS attribution, assertion handling, evaluation, annotation, model-card documentation, MRRV-ready pipelines |
| [`hcc-nlp/`](hcc-nlp/) | Data-science / NLP engineering teams | HCC / risk-adjustment extractor design (suspect + validate engines), CMS-HCC V28 / V24 / HHS-HCC versioning, MEAT, hierarchies, RADV readiness, per-HCC model cards |

Planned future skills (not yet built): `hipaa-compliance/` (BAA review, breach response, OCR audit prep, de-identification methodology, HIPAA technical safeguards for any healthcare app - intended audience is broader than chart review; useful for web / mobile / SaaS teams handling PHI).

## Which skill should I install?

- **Reviewing charts, auditing records, doing CDI / coding / HEDIS / HCC audits as a human or AI-assisted human** → install [`medical-chart-review/`](medical-chart-review/)
- **Building per-measure HEDIS extractors (GSD, BCS-E, FUH, MRP, TRC, etc.)** → install [`hedis-nlp/`](hedis-nlp/)
- **Building HCC extractors, suspect engines, validate engines, RAF pipelines, RADV-ready workflows** → install [`hcc-nlp/`](hcc-nlp/)
- **Building all of the above as a unified platform** → install all three

The skills are designed to coexist. Cross-references between them are written as prose pointers (e.g., "see the `medical-chart-review` skill's `references/coding-icd10-hcc.md`") rather than clickable links so each skill works standalone.

## Install

Each skill is independently installable via [`skills.sh`](https://skills.sh) or by cloning into the appropriate directory for your agent. The path format `<repo>/<skill>` selects a specific skill from this monorepo.

### Recommended: `skills.sh` one-liner

```bash
# Install one
npx skills add Yar177/medical-chart-review-skill/medical-chart-review
npx skills add Yar177/medical-chart-review-skill/hedis-nlp
npx skills add Yar177/medical-chart-review-skill/hcc-nlp

# Or all three
npx skills add Yar177/medical-chart-review-skill/medical-chart-review \
                Yar177/medical-chart-review-skill/hedis-nlp \
                Yar177/medical-chart-review-skill/hcc-nlp
```

> If your version of `skills.sh` does not support subpath install, use the manual install below.

### Manual install (Claude Code)

Personal (available in all projects):

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review ~/.claude/skills/
cp -R /tmp/mcr-skills/hedis-nlp           ~/.claude/skills/
cp -R /tmp/mcr-skills/hcc-nlp             ~/.claude/skills/
rm -rf /tmp/mcr-skills
```

Project-only (commit alongside your repo):

```bash
mkdir -p .claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review .claude/skills/
cp -R /tmp/mcr-skills/hedis-nlp           .claude/skills/
cp -R /tmp/mcr-skills/hcc-nlp             .claude/skills/
rm -rf /tmp/mcr-skills
```

### Manual install (GitHub Copilot - VS Code, CLI, cloud agent)

Personal:

```bash
mkdir -p ~/.copilot/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review ~/.copilot/skills/
cp -R /tmp/mcr-skills/hedis-nlp           ~/.copilot/skills/
cp -R /tmp/mcr-skills/hcc-nlp             ~/.copilot/skills/
rm -rf /tmp/mcr-skills
```

Project-only:

```bash
mkdir -p .github/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review .github/skills/
cp -R /tmp/mcr-skills/hedis-nlp           .github/skills/
cp -R /tmp/mcr-skills/hcc-nlp             .github/skills/
rm -rf /tmp/mcr-skills
```

The skill folder names must remain `medical-chart-review`, `hedis-nlp`, and `hcc-nlp` - they must match the `name` field in each `SKILL.md`.

### Verify it loaded

- **Claude Code**: ask *"What skills do you have available?"* or type `/medical-chart-review`, `/hedis-nlp`, `/hcc-nlp`.
- **VS Code Copilot**: Chat → Configure Chat (gear icon) → Skills tab. Or type `/` in chat and look for the three skills.

## Repository structure

```
medical-chart-review-skill/    (this repo)
├── README.md                  (this file - umbrella)
├── CHANGELOG.md               (umbrella changelog, sections per skill)
├── CONTRIBUTING.md
├── LICENSE
├── SECURITY.md
│
├── medical-chart-review/      (auditor skill)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            (12 files)
│   └── templates/             (8 files including auditor HCC audit)
│
├── hedis-nlp/                 (HEDIS engineering skill)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   │   ├── nlp/               (cross-cutting NLP)
│   │   ├── hedis/             (24 per-measure cards)
│   │   └── hedis-supplemental-data.md
│   └── templates/
│       ├── per-measure-model-card.md
│       └── hedis-abstraction.md
│
└── hcc-nlp/                   (HCC engineering skill)
    ├── SKILL.md
    ├── README.md
    ├── references/            (12 files + cards/ + test-fixtures/)
    │   ├── cards/             (HCC 18, 22, 85, 96, 108, 111 exemplars)
    │   └── test-fixtures/     (synthetic regression fixtures)
    └── templates/
        ├── hcc-model-card.md
        └── hcc-audit-nlp.md
```

## Versioning

Each skill is versioned independently in [CHANGELOG.md](CHANGELOG.md). HEDIS measure updates bump `hedis-nlp` only; CMS-HCC model updates bump `hcc-nlp` only; clinical reference updates (Beers, ICD-10, abbreviations) bump `medical-chart-review` only. Cross-skill changes (the periodic monorepo restructure, shared install instructions) bump the umbrella.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Per-skill conventions:

- Every skill must run its `SKILL.md` §0 PHI / safety gate before reading chart content
- Synthetic data only in `test-fixtures/` directories; never commit real or de-identified PHI
- Model card YAML is authoritative on conflict with the narrative
- Internal links inside one skill use relative paths; cross-skill references are prose pointers
- Updates that affect submitted HEDIS / HCC outputs require named coder / auditor / compliance sign-off in the changelog entry

## Compliance & safety guardrails (apply to every skill)

- **PHI verification** before reading any chart content (Safe Harbor de-identified, synthetic, or BAA-covered environment)
- **No diagnosis / prescribing** for real patients
- **No upcoding / silent gap closure / auto-validation without provenance**
- **Non-leading provider queries** per ACDIS/AHIMA 2022 Practice Brief (chart-review skill)
- **No PHI written to agent memory** (session, repo, or user scope)
- **Explicit deferral to credentialed humans** (CRC/CCS, CCDS, NCQA-certified auditors, compliance) for any change affecting reported metrics or submitted claims

## License / disclaimer

Use at your own risk. Outputs from any skill in this repo are advisory and must be reviewed by appropriately credentialed humans before being used for billing, compliance, regulatory submission, quality reporting, or patient care decisions.
