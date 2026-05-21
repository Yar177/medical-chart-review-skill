# medical-chart-review-skill

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20278242.svg)](https://doi.org/10.5281/zenodo.20278242)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill Spec](https://img.shields.io/badge/spec-agentskills.io-blue)](https://agentskills.io/)

A monorepo of **7 healthcare AI agent skills** - chart review, HEDIS NLP, HCC NLP, HIPAA compliance, claims-ML failure-mode auditing, healthcare code systems / crosswalks / value sets, and FHIR R4 implementation (US Core, CARIN BB, Da Vinci, SMART, Bulk Data). Each subdirectory is an independently installable [Agent Skill](https://agentskills.io/) packaged for a distinct audience and works with Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, Gemini, and [40+ other agents](https://www.skills.sh/agent).

## Quickstart

Pick one (or use `--skill '*'` to install all seven):

```bash
npx skills add Yar177/medical-chart-review-skill --skill medical-chart-review
npx skills add Yar177/medical-chart-review-skill --skill hedis-nlp
npx skills add Yar177/medical-chart-review-skill --skill hcc-nlp
npx skills add Yar177/medical-chart-review-skill --skill hipaa-compliance
npx skills add Yar177/medical-chart-review-skill --skill claims-ml
npx skills add Yar177/medical-chart-review-skill --skill healthcare-code-systems
npx skills add Yar177/medical-chart-review-skill --skill fhir-r4-implementation

# All seven at once
npx skills add Yar177/medical-chart-review-skill --skill '*'
```

> ⚠️ Every skill in this repo produces documentation, engineering, or compliance analysis. None of them provide medical advice. Final clinical, coding, regulatory, and compliance decisions require credentialed humans.

## Skills in this repo

| Skill | Audience | What it does |
|---|---|---|
| [`medical-chart-review/`](medical-chart-review/) | Clinicians, CRC/CCS coders, CDI specialists, quality auditors | Reads charts, classifies care setting + payer program, validates documentation against coding and quality standards, produces auditable findings and provider queries |
| [`hedis-nlp/`](hedis-nlp/) | Data-science / NLP engineering teams | Per-measure HEDIS extractor design, DoS attribution, assertion handling, evaluation, annotation, model-card documentation, MRRV-ready pipelines |
| [`hcc-nlp/`](hcc-nlp/) | Data-science / NLP engineering teams | HCC / risk-adjustment extractor design (suspect + validate engines), CMS-HCC V28 / V24 / HHS-HCC versioning, MEAT, hierarchies, RADV readiness, per-HCC model cards |
| [`hipaa-compliance/`](hipaa-compliance/) | Builders / compliance officers / privacy + security teams for any healthcare app | HIPAA Privacy + Security + Breach Notification Rules, BAA review, de-identification methodology, OCR audit prep, breach response, technical safeguards for web / mobile / cloud / AI services handling PHI |
| [`claims-ml/`](claims-ml/) | Data-science / ML engineering teams building supervised models on claims | Healthcare-ML failure-mode auditor: target leakage (10 classes), splits, target definitions, evaluation (actuary + ML lens), calibration / drift, production-scoring fitness, baselines, fairness; pre-deployment checklist + model card |
| [`healthcare-code-systems/`](healthcare-code-systems/) | Data engineering, analytics, data-science, and platform teams | Authoritative reference + working templates for the code systems that healthcare data runs on: ICD-10-CM / PCS, ICD-9 + GEMs, CPT + modifiers, HCPCS Level II, NDC, RxNorm, SNOMED CT, LOINC + UCUM, CVX, NUCC, NPI, revenue / TOB / POS / DRG / APC, CCSR / Elixhauser / Charlson / BETOS, value sets (VSAC, NCQA HEDIS, eCQM), crosswalks (GEMs, NDC↔RxNorm, SNOMED↔ICD, LOINC↔CPT, ICD-10→HCC), versioning / drift, sources / licensing |
| [`fhir-r4-implementation/`](fhir-r4-implementation/) | Health-IT / interop engineering, platform, integration, and FHIR app-dev teams | FHIR R4 (4.0.1) implementation reference for US payer / provider interop: resource taxonomy, identity + versioning, search, bundles + transactions, FHIRPath, profiles + conformance, terminology services, operations (incl. R4 Subscription vs R5 SubscriptionTopic), SMART App Launch + Backend Services, Bulk Data export, US Core 6.1.0, CARIN BB 2.1.0, Da Vinci PDex / HRex / Plan-Net, conformance testing (HAPI / `$validate` / Inferno), CMS-9115-F + CMS-0057-F alignment |

## Which skill should I install?

- **Reviewing charts, auditing records, doing CDI / coding / HEDIS / HCC audits as a human or AI-assisted human** → install [`medical-chart-review/`](medical-chart-review/)
- **Building per-measure HEDIS extractors (GSD, BCS-E, FUH, MRP, TRC, etc.)** → install [`hedis-nlp/`](hedis-nlp/)
- **Building HCC extractors, suspect engines, validate engines, RAF pipelines, RADV-ready workflows** → install [`hcc-nlp/`](hcc-nlp/)
- **Designing / reviewing HIPAA compliance for an app: BAAs, breach response, OCR audit prep, de-id strategy, technical safeguards, cloud + AI service boundaries** → install [`hipaa-compliance/`](hipaa-compliance/)
- **Building or auditing supervised ML on claims (cost, hospitalization, readmit, ED, onset, mortality, eligibility, anomaly): leakage audit, split design, calibration / drift, production-scoring fitness, fairness** → install [`claims-ml/`](claims-ml/)
- **Working with healthcare code systems and crosswalks: ICD-10, CPT, HCPCS, NDC, RxNorm, SNOMED, LOINC, value sets, GEMs, ICD↔HCC, NDC↔RxNorm; versioning / drift monitoring; provider / institutional codes; grouper selection** → install [`healthcare-code-systems/`](healthcare-code-systems/)
- **Implementing FHIR R4 endpoints / clients / IGs: US Core, CARIN BB, Da Vinci PDex / HRex / Plan-Net, SMART App Launch + Backend Services, Bulk Data; profiles, must-support, search, conformance testing (HAPI / `$validate` / Inferno); CMS-9115-F and CMS-0057-F (Jan 2027) alignment** → install [`fhir-r4-implementation/`](fhir-r4-implementation/)
- **Building all of the above as a unified platform** → install all seven

The skills are designed to coexist. Cross-references between them are written as prose pointers (e.g., "see the `medical-chart-review` skill's `references/coding-icd10-hcc.md`") rather than clickable links so each skill works standalone.

## Routing matrix (for agents with all skills loaded)

If you've installed multiple skills and want fast disambiguation:

| If the user says... | Load skill |
|---|---|
| "review this chart", "audit this record", "abstract this note", "chart review", "CDI review", "coding audit", "med rec", "quality gap chase" | `medical-chart-review` |
| "build a HEDIS extractor", "GSD / BCS-E / FUH / MRP / TRC NLP", "per-measure NLP", "MRRV-ready pipeline", "HEDIS model card" | `hedis-nlp` |
| "build an HCC extractor", "suspect engine", "validate engine", "RAF NLP", "MEAT validation", "CMS-HCC V28 / V24 NLP", "RADV readiness" | `hcc-nlp` |
| "review our BAA", "breach 4-factor assessment", "OCR audit prep", "HIPAA risk analysis", "de-identify dataset", "Safe Harbor vs Expert Determination", "HIPAA technical safeguards" | `hipaa-compliance` |
| "audit my feature spec", "target leakage check", "claims ML model card", "pre-deployment review", "split design for member-year data", "calibration / drift", "claims ML fairness audit" | `claims-ml` |
| "ICD-10 / CPT / HCPCS / NDC / RxNorm / SNOMED / LOINC question", "value set lookup", "GEMs crosswalk", "ICD↔HCC mapping", "NDC↔RxNorm", "code-system version / drift", "grouper / DRG / APC selection" | `healthcare-code-systems` |
| "FHIR R4 implementation", "US Core / CARIN BB / Da Vinci profile", "SMART App Launch / Backend Services", "Bulk Data `$export`", "`$validate` / HAPI / Inferno", "CapabilityStatement", "CMS-9115-F / CMS-0057-F Patient Access / Payer-to-Payer / Provider Directory API", "R4 Subscription vs R5 SubscriptionTopic" | `fhir-r4-implementation` |

## Install

Each skill is independently installable via [`skills.sh`](https://www.skills.sh) or by cloning into the appropriate directory for your agent. Use the `--skill <name>` flag to pick a specific skill from this monorepo.

### Recommended: `skills.sh` one-liner

```bash
# Install one
npx skills add Yar177/medical-chart-review-skill --skill medical-chart-review
npx skills add Yar177/medical-chart-review-skill --skill hedis-nlp
npx skills add Yar177/medical-chart-review-skill --skill hcc-nlp
npx skills add Yar177/medical-chart-review-skill --skill hipaa-compliance
npx skills add Yar177/medical-chart-review-skill --skill claims-ml
npx skills add Yar177/medical-chart-review-skill --skill healthcare-code-systems
npx skills add Yar177/medical-chart-review-skill --skill fhir-r4-implementation

# Or all seven
npx skills add Yar177/medical-chart-review-skill --skill '*'

# Target a specific agent (e.g. claude-code, cursor, codex, github-copilot)
npx skills add Yar177/medical-chart-review-skill --skill medical-chart-review -a claude-code

# Install globally instead of per-project
npx skills add Yar177/medical-chart-review-skill --skill '*' -g
```

List what's available without installing:

```bash
npx skills add Yar177/medical-chart-review-skill --list
```

> If your `skills.sh` CLI is older and `--skill` is unavailable, use the manual install below.

### Manual install (Claude Code)

Personal (available in all projects):

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review ~/.claude/skills/
cp -R /tmp/mcr-skills/hedis-nlp           ~/.claude/skills/
cp -R /tmp/mcr-skills/hcc-nlp             ~/.claude/skills/
cp -R /tmp/mcr-skills/hipaa-compliance    ~/.claude/skills/
cp -R /tmp/mcr-skills/claims-ml           ~/.claude/skills/
cp -R /tmp/mcr-skills/healthcare-code-systems ~/.claude/skills/
cp -R /tmp/mcr-skills/fhir-r4-implementation ~/.claude/skills/
rm -rf /tmp/mcr-skills
```

Project-only (commit alongside your repo):

```bash
mkdir -p .claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review .claude/skills/
cp -R /tmp/mcr-skills/hedis-nlp           .claude/skills/
cp -R /tmp/mcr-skills/hcc-nlp             .claude/skills/
cp -R /tmp/mcr-skills/hipaa-compliance    .claude/skills/
cp -R /tmp/mcr-skills/claims-ml           .claude/skills/
cp -R /tmp/mcr-skills/healthcare-code-systems .claude/skills/
cp -R /tmp/mcr-skills/fhir-r4-implementation .claude/skills/
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
cp -R /tmp/mcr-skills/hipaa-compliance    ~/.copilot/skills/
cp -R /tmp/mcr-skills/claims-ml           ~/.copilot/skills/
cp -R /tmp/mcr-skills/healthcare-code-systems ~/.copilot/skills/
cp -R /tmp/mcr-skills/fhir-r4-implementation ~/.copilot/skills/
rm -rf /tmp/mcr-skills
```

Project-only:

```bash
mkdir -p .github/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git /tmp/mcr-skills
cp -R /tmp/mcr-skills/medical-chart-review .github/skills/
cp -R /tmp/mcr-skills/hedis-nlp           .github/skills/
cp -R /tmp/mcr-skills/hcc-nlp             .github/skills/
cp -R /tmp/mcr-skills/hipaa-compliance    .github/skills/
cp -R /tmp/mcr-skills/claims-ml           .github/skills/
cp -R /tmp/mcr-skills/healthcare-code-systems .github/skills/
cp -R /tmp/mcr-skills/fhir-r4-implementation .github/skills/
rm -rf /tmp/mcr-skills
```

The skill folder names must remain `medical-chart-review`, `hedis-nlp`, `hcc-nlp`, `hipaa-compliance`, `claims-ml`, `healthcare-code-systems`, and `fhir-r4-implementation` - they must match the `name` field in each `SKILL.md`.

### Verify it loaded

- **Claude Code**: ask *"What skills do you have available?"* or type `/medical-chart-review`, `/hedis-nlp`, `/hcc-nlp`, `/hipaa-compliance`, `/claims-ml`, `/healthcare-code-systems`, `/fhir-r4-implementation`.
- **VS Code Copilot**: Chat → Configure Chat (gear icon) → Skills tab. Or type `/` in chat and look for the seven skills.

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
│   ├── references/            (14 files, incl. chart-types.md and date-of-service.md)
│   └── templates/             (9 files, incl. chart-triage.md and the auditor HCC audit)
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
├── hcc-nlp/                   (HCC engineering skill)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            (12 files + cards/ + test-fixtures/)
│   │   ├── cards/             (HCC 18, 22, 85, 96, 108, 111 exemplars)
│   │   └── test-fixtures/     (synthetic regression fixtures)
│   └── templates/
│       ├── hcc-model-card.md
│       └── hcc-audit-nlp.md
│
├── hipaa-compliance/          (HIPAA builder / compliance-officer skill)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            (12 files - Three Rules, BAA, de-id, technical safeguards, OCR audit, IR, state-law boundaries)
│   └── templates/             (5 files - BAA review, breach 4-factor, risk analysis, IR playbook, OCR audit binder)
│
├── claims-ml/                 (claims-ML failure-mode auditor for data-science / ML teams)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            (10 files - target-leakage, splits, target-definitions, evaluation, calibration-and-drift, production-scoring, feature-engineering, baselines, fairness, target-types-and-projects)
│   └── templates/             (5 files - feature-spec audit, leakage audit, model card, pre-deployment checklist, recalibration plan)
│
├── healthcare-code-systems/   (code-systems / crosswalks / value-sets reference for data + analytics teams)
│   ├── SKILL.md
│   ├── README.md
│   ├── references/            (17 files - icd10-cm, icd10-pcs, icd9-and-legacy, cpt-and-modifiers, hcpcs-level-ii, institutional-billing-codes, snomed-ct, loinc-and-ucum, rxnorm-ndc-and-drugs, immunizations-and-other, provider-identifiers, crosswalks, value-sets-and-vsac, code-groupers, versioning-and-drift, sources-and-licensing, common-pitfalls)
│   └── templates/             (5 files - code-system-inventory, crosswalk-spec, value-set-manifest, code-drift-monitoring, grouper-evaluation)
│
└── fhir-r4-implementation/   (FHIR R4 implementation reference for health-IT / interop / FHIR app-dev teams)
    ├── SKILL.md
    ├── README.md
    ├── references/            (13 files - resource-taxonomy, resource-identity-and-versioning, search-parameters, bundles-and-transactions, fhirpath, profiles-and-conformance, terminology-services, operations, smart-on-fhir, bulk-data-export, us-core-ig, carin-bb-ig, da-vinci-overview, conformance-testing, common-pitfalls)
    └── templates/             (5 files - resource-design-spec, capability-statement-skeleton, claims-to-eob-mapping, smart-app-launch-checklist, fhir-conformance-audit)
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
