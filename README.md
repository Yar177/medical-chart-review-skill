# medical-chart-review

An AI agent skill for expert-level review of medical charts, EMRs, and EHRs. Designed for documentation review, coding/quality auditing, and clinical data abstraction — **not** for direct patient care.

> ⚠️ This skill produces documentation analysis, not medical advice. Final clinical, coding, and compliance decisions require credentialed humans (physicians, CCS/CPC/CRC coders, CCDS specialists).

## Install

Drop the folder into your agent's skills directory:

- **Claude / generic agents**: `~/.agents/skills/medical-chart-review/`
- **GitHub Copilot (VS Code)**: also expose as `.github/instructions/medical-chart-review.instructions.md` if you want it auto-applied

The agent discovers the skill via `SKILL.md`'s frontmatter `description`.

## When the agent loads it

Triggered by requests like:
- "review this chart" / "summarize this patient's history"
- "audit these records for HCC capture" / "validate ICD-10 coding"
- "perform a CDI review" / "write a provider query"
- "do a HEDIS gap analysis"
- "reconcile these medications"
- "extract structured data from this note"

**Not** triggered for: live patient care, prescribing, diagnosis of real patients, handling identifiable PHI in non-compliant environments.

## What it does

1. **Safety gate** — confirms PHI status, scope, and disclaimers before reading anything.
2. **Selects a review type** — clinical summary, CDI, HCC audit, HEDIS gap, med rec, utilization review, coding audit, or data abstraction.
3. **Runs a standard workflow** — orient → index → read → cross-reference → apply domain rules → surface findings with citations.
4. **Outputs** a structured report using the matching template.

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point — workflow, safety gates, routing |
| [references/](references/) | Deep domain knowledge, loaded on demand |
| [templates/](templates/) | Output formats, one per review type |

### References (loaded only when needed)

- [chart-structure.md](references/chart-structure.md) — EHR systems (Epic, Cerner, Athena, Meditech) and universal chart sections
- [note-types.md](references/note-types.md) — SOAP, H&P, OLDCARTS/OPQRST, note taxonomy
- [coding-icd10-hcc.md](references/coding-icd10-hcc.md) — ICD-10-CM, MEAT criteria, CMS-HCC, RAF
- [coding-cpt-drg.md](references/coding-cpt-drg.md) — CPT modifiers, E&M 2021+ leveling, MS-DRG
- [quality-measures.md](references/quality-measures.md) — HEDIS, CMS Stars, MIPS
- [medications.md](references/medications.md) — Beers, interactions, polypharmacy, controlled substances
- [labs-imaging.md](references/labs-imaging.md) — Reference ranges, critical values, CKD staging
- [red-flags.md](references/red-flags.md) — Must-not-miss patient-safety findings
- [abbreviations.md](references/abbreviations.md) — Clinical shorthand + JCAHO Do-Not-Use list
- [hipaa-privacy.md](references/hipaa-privacy.md) — 18 Safe Harbor identifiers, 42 CFR Part 2
- [provider-queries.md](references/provider-queries.md) — Compliant ACDIS/AHIMA query templates

### Templates

[clinical-summary.md](templates/clinical-summary.md) · [hcc-audit.md](templates/hcc-audit.md) · [cdi-review.md](templates/cdi-review.md) · [quality-gap.md](templates/quality-gap.md) · [med-rec.md](templates/med-rec.md) · [utilization-review.md](templates/utilization-review.md) · [coding-audit.md](templates/coding-audit.md) · [data-abstraction.md](templates/data-abstraction.md)

## Compliance & safety guardrails

The skill enforces:

- **PHI verification** before reading any chart content (Safe Harbor de-identified, synthetic, or BAA-covered environment)
- **No diagnosis / prescribing** for real patients
- **No upcoding** — coding suggestions must be supported by documentation (MEAT)
- **Non-leading provider queries** per ACDIS/AHIMA 2022 Practice Brief
- **No PHI written to agent memory** (session, repo, or user scope)
- **Explicit deferral** to credentialed humans for ambiguous coding, fraud signals, and CMS/RAC/legal submissions

## Customization tips

- Add `references/medicare-advantage.md` or `references/specialty-<X>.md` for domain-specific deep dives
- Add `examples/` with 1–2 walked-through synthetic reviews to anchor the agent's voice
- For organization-specific coding rules or payer policies, add `references/local-policy.md` and reference it in `SKILL.md`
- Update annually — ICD-10-CM guidelines, HCC model versions (v24 → v28 transition), HEDIS measure set, and Beers Criteria all change yearly

## Out of scope

- Real-time clinical decision support
- Prescribing or order entry
- Anything requiring a licensed clinician's signature on the legal record
- Handling identifiable PHI without a confirmed HIPAA-compliant environment

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans before being used for billing, compliance, regulatory submission, or patient care decisions.
