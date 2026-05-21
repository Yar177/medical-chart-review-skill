# hcc-nlp

A skill for data-science / NLP engineering teams building HCC / risk-adjustment extraction pipelines (suspect engines, validate engines, RAF estimation, RADV preparation). Covers CMS-HCC V28, V24, and HHS-HCC. **Not for clinical chart review** (use [`medical-chart-review`](../medical-chart-review/)). **Not for HEDIS NLP** (use [`hedis-nlp`](../hedis-nlp/)).

> ⚠️ Outputs are NLP engineering guidance, not certified risk-adjustment coding. HCC decisions affecting submitted claims require sign-off from a credentialed coder (CRC/CCS) and compliance review. Auto-validation requires extremely high precision and full provenance.

## What this skill provides

- **Cross-cutting NLP enablement** in [`references/`](references/) covering the highest-impact failure modes that drive RADV findings, OIG investigations, and FCA exposure:
  - Model versions (V28 / V24 / HHS-HCC), phase-in schedule, version pinning
  - RAF calculation with disease-disease interactions, calendar reset, dollar-weighted metrics
  - MEAT as a separate NLP task (two-pass architecture, linkage problem)
  - Hierarchies as a post-extraction step (within-family trumping)
  - Date of service (5-part contract, calendar-year reset, provider-type whitelist, telehealth boundaries, AWV recapture trap; cascade alignment with HEDIS NLP plus HCC-specific `hcc_dos_policy` and provenance columns `MATCH_FACE_TO_FACE_VERIFIED` / `MATCH_ENCOUNTER_SETTING`)
  - Assertion / negation (9-dimension taxonomy, history-of as #1 RADV finding, Z-code family disambiguation, family-history confusion, hedging asymmetry, section-aware priors)
  - Extraction patterns (suspect vs validate engine split, two-pass architecture, provenance requirements)
  - Terminology / crosswalk handling
  - Evaluation (span / encounter-HCC / member-year-HCC / RAF dollar-weighted, hierarchy-aware metrics, decomposed errors, RADV simulation, drift monitoring)
  - Annotation guidelines and IAA targets
  - Compliance / enforcement (RADV / OIG / FCA, two-way review obligation, auto-validation precision floor, CDI / provider-query workflow)
- **Per-HCC exemplar cards** in [`references/cards/`](references/cards/): 9-section schema cards for HCC 18 (diabetes w/ complications), 22 (morbid obesity), 85 (CHF), 96 (specified arrhythmias), 108 (vascular disease), 111 (COPD). Use these as the template for building your own HCC cards.
- **Synthetic regression fixtures** in [`references/test-fixtures/`](references/test-fixtures/): history-of trap, hierarchy collapse, status-code amputation, MEAT gap, problem-list-only.
- **Canonical per-HCC model card** in [`templates/hcc-model-card.md`](templates/hcc-model-card.md): YAML + Markdown, YAML authoritative, stricter required-field discipline than HEDIS due to RADV exposure.
- **NLP-assisted HCC audit template** in [`templates/hcc-audit-nlp.md`](templates/hcc-audit-nlp.md): expanded version of the auditor's HCC audit with model version, MEAT evidence, hierarchy application, and reviewer-override feedback loop.

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill hcc-nlp
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## When the agent loads it

Triggered by requests like:

- "Build an HCC extractor" / "build a suspect engine" / "build a validate engine"
- "V28 vs V24 migration for NLP"
- "Apply HCC hierarchies"
- "MEAT as NLP"
- "RADV simulation" / "RADV readiness"
- "Z-code disambiguation for HCC"
- "History-of trap" / "problem-list-only invalid"
- "Date of service for HCC" / "AWV recapture"
- "Write a model card for HCC [n]"
- "HHS-HCC NLP" / "ACA risk adjustment NLP"

Not triggered for: clinical chart review (`medical-chart-review`), HEDIS NLP (`hedis-nlp`), or PHI handling in non-compliant environments.

## Quick start

```text
I'm building a validate engine for HCC 18. What's the MEAT contract, how do I
apply the hierarchy, and what's the most common over-coding pattern I need to
regress against?
```

The agent will run the PHI/scope gate from `SKILL.md` §0, then load [`references/cards/hcc-18-diabetes-with-complications.md`](references/cards/hcc-18-diabetes-with-complications.md), [`references/meat-criteria.md`](references/meat-criteria.md), [`references/hierarchies.md`](references/hierarchies.md), and [`references/test-fixtures/hierarchy-collapse.md`](references/test-fixtures/hierarchy-collapse.md).

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, task routing |
| [references/](references/) | All HCC NLP enablement (12 files + cards/ + test-fixtures/) |
| [references/cards/](references/cards/) | Per-HCC exemplar cards (9-section schema) |
| [references/test-fixtures/](references/test-fixtures/) | Synthetic note + expected-extraction regression pairs |
| [templates/hcc-model-card.md](templates/hcc-model-card.md) | Canonical per-HCC model card |
| [templates/hcc-audit-nlp.md](templates/hcc-audit-nlp.md) | NLP-assisted audit template |

## Related skills in this repo

- [`medical-chart-review`](../medical-chart-review/) - clinical chart review for clinicians, coders, CDI / quality auditors. Its `references/coding-icd10-hcc.md` is the auditor-oriented complement to this skill's NLP-oriented files. Its `templates/hcc-audit.md` is the human-auditor version of this skill's `hcc-audit-nlp.md`.
- [`hedis-nlp`](../hedis-nlp/) - HEDIS NLP. HEDIS and HCC are different products; do not conflate.
- [`hipaa-compliance`](../hipaa-compliance/) - HIPAA compliance for the platform hosting this pipeline: BAA review, breach response, OCR audit prep, de-identification methodology, technical safeguards. RADV exposure makes audit-evidence retention especially relevant.
- [`claims-ml`](../claims-ml/) - healthcare-ML failure-mode auditor. Claims-ML models commonly consume HCC outputs (HCC-rollup features, prior-year RAF); claims-ml's `references/target-leakage.md` §L3 (RAF circularity) and `references/feature-engineering.md` §2 cover the downstream pitfalls.

## Compliance & safety guardrails

- PHI verification before reading any chart content
- No auto-validation without internal RADV simulation passing precision floor
- Hierarchy enforcement required before metric computation
- Problem-list-only and med-list-only rejected as MEAT
- Status-code per-family logic enforced (Z85/86/87 generally not HCCs; Z89/93/94/99 subset ARE; Z95.x cardiac implants do not imply current disease)
- Model card YAML authoritative; stricter required-field discipline than HEDIS
- Two-way review capability required for any auto-validation deployment
- Explicit deferral to credentialed coders (CRC/CCS) and compliance for any change affecting submitted claims

## Out of scope

- Clinical chart review by humans
- HEDIS NLP
- BI / analytics dashboards for RAF reporting (this skill produces extractions; reporting layer is separate)
- Handling identifiable PHI without a confirmed HIPAA-compliant environment

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans before being used for HCC submission, RAF reporting, RADV response, or any compliance / regulatory work.
