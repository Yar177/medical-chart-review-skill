# medical-chart-review

An AI agent skill for expert-level review of medical charts, EMRs, and EHRs. Designed for clinicians, CRC/CCS coders, CDI specialists, and quality auditors doing documentation review, coding/quality auditing, and clinical data abstraction - **not** for direct patient care.

> ⚠️ This skill produces documentation analysis, not medical advice. Final clinical, coding, and compliance decisions require credentialed humans (physicians, CCS/CPC/CRC coders, CCDS specialists).

This is one of three skills in this monorepo. For NLP engineering work, see the sibling `hedis-nlp` and `hcc-nlp` skills.

## Install

See the [root README](../README.md) for install instructions. This skill installs as `medical-chart-review`.

## Quick start

Once installed, try one of these prompts:

> *"I want to do an HCC audit on a synthetic patient chart. Walk me through the safety gate first."*

> *"/medical-chart-review summarize this discharge summary"* *(paste de-identified or synthetic chart text)*

The agent will run the PHI/scope check from `SKILL.md` §0, then route to the appropriate template under [templates/](templates/).

## When the agent loads it

Triggered by requests like:

- "review this chart" / "summarize this patient's history"
- "audit these records for HCC capture" / "validate ICD-10 coding"
- "perform a CDI review" / "write a provider query"
- "do a HEDIS gap analysis"
- "reconcile these medications"
- "extract structured data from this note"

**Not** triggered for: live patient care, prescribing, diagnosis of real patients, handling identifiable PHI in non-compliant environments, or NLP engineering (use the sibling `hedis-nlp` / `hcc-nlp` skills).

## What it does

1. **Safety gate** - confirms PHI status, scope, and disclaimers before reading anything.
2. **Selects a review type** - clinical summary, CDI, HCC audit, HEDIS gap, med rec, utilization review, coding audit, or data abstraction.
3. **Runs a standard workflow** - orient → index → read → cross-reference → apply domain rules → surface findings with citations.
4. **Outputs** a structured report using the matching template.

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, routing |
| [references/](references/) | Deep domain knowledge, loaded on demand |
| [templates/](templates/) | Output formats, one per review type |

### References (loaded only when needed)

- [chart-structure.md](references/chart-structure.md) - EHR systems (Epic, Cerner, Athena, Meditech) and universal chart sections
- [note-types.md](references/note-types.md) - SOAP, H&P, OLDCARTS/OPQRST, note taxonomy
- [administrative-insurance.md](references/administrative-insurance.md) - face sheet, insurance verification, eligibility on DOS, COB, prior auth, referrals, payer policy basics, denial categories
- [coding-icd10-hcc.md](references/coding-icd10-hcc.md) - ICD-10-CM, MEAT criteria, CMS-HCC, RAF (auditor-oriented; complementary NLP engineering view lives in the sibling `hcc-nlp` skill)
- [coding-cpt-drg.md](references/coding-cpt-drg.md) - CPT modifiers, E&M 2021+ leveling, MS-DRG
- [quality-measures.md](references/quality-measures.md) - HEDIS, CMS Stars, MIPS overview (NLP engineering view lives in the sibling `hedis-nlp` skill)
- [medications.md](references/medications.md) - Beers, interactions, polypharmacy, controlled substances
- [labs-imaging.md](references/labs-imaging.md) - Reference ranges, critical values, CKD staging
- [red-flags.md](references/red-flags.md) - Must-not-miss patient-safety findings
- [abbreviations.md](references/abbreviations.md) - Clinical shorthand + JCAHO Do-Not-Use list
- [hipaa-privacy.md](references/hipaa-privacy.md) - 18 Safe Harbor identifiers, 42 CFR Part 2
- [provider-queries.md](references/provider-queries.md) - Compliant ACDIS/AHIMA query templates

### Templates

[clinical-summary.md](templates/clinical-summary.md) · [hcc-audit.md](templates/hcc-audit.md) · [cdi-review.md](templates/cdi-review.md) · [quality-gap.md](templates/quality-gap.md) · [med-rec.md](templates/med-rec.md) · [utilization-review.md](templates/utilization-review.md) · [coding-audit.md](templates/coding-audit.md) · [data-abstraction.md](templates/data-abstraction.md)

## Related skills in this repo

- [`hedis-nlp`](../hedis-nlp/) - per-measure HEDIS extractor design (DoS, assertion, evaluation, model cards)
- [`hcc-nlp`](../hcc-nlp/) - HCC / risk-adjustment extractor design (V28 / V24 / HHS-HCC, MEAT, hierarchies, RADV readiness)
- [`hipaa-compliance`](../hipaa-compliance/) - HIPAA Privacy + Security + Breach Notification, BAA review, OCR audit prep, de-identification methodology. This skill's `references/hipaa-privacy.md` is the reviewer-facing 18-identifier checklist; the sibling is the broader builder / compliance-officer view.

## Compliance & safety guardrails

The skill enforces:

- **PHI verification** before reading any chart content (Safe Harbor de-identified, synthetic, or BAA-covered environment)
- **No diagnosis / prescribing** for real patients
- **No upcoding** - coding suggestions must be supported by documentation (MEAT)
- **Non-leading provider queries** per ACDIS/AHIMA 2022 Practice Brief
- **No PHI written to agent memory** (session, repo, or user scope)
- **Explicit deferral** to credentialed humans for ambiguous coding, fraud signals, and CMS/RAC/legal submissions

## Customization tips

- Add `references/specialty-<X>.md` for domain-specific deep dives (e.g., cardiology, oncology, behavioral health)
- Add `examples/` with 1-2 walked-through synthetic reviews to anchor the agent's voice
- For organization-specific coding rules or payer policies, add `references/local-policy.md` and reference it in `SKILL.md`
- Update annually - ICD-10-CM guidelines, HEDIS measure set, and Beers Criteria all change yearly

## Out of scope

- Real-time clinical decision support
- Prescribing or order entry
- Anything requiring a licensed clinician's signature on the legal record
- Handling identifiable PHI without a confirmed HIPAA-compliant environment
- HEDIS / HCC NLP engineering (use sibling skills)

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans before being used for billing, compliance, regulatory submission, or patient care decisions.
