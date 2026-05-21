# hedis-nlp

A skill for data-science / NLP engineering teams building per-measure HEDIS extraction pipelines. **Not for clinical chart review** (use the [`medical-chart-review`](../medical-chart-review/) skill in this repo). **Not for HCC / risk-adjustment NLP** (use the [`hcc-nlp`](../hcc-nlp/) skill).

> ⚠️ Outputs are NLP engineering guidance, not certified HEDIS reporting. Model decisions affecting reported rates require sign-off from NCQA-certified auditors and credentialed coders.

## What this skill provides

For teams building per-measure HEDIS extractors (GSD, BCS-E, FUH, MRP, TRC, COA, CBP, and 17+ other measures), this skill packages the chart-review knowledge in the parallel `medical-chart-review` skill into model-friendly form:

- **Cross-cutting NLP enablement** in [`references/nlp/`](references/nlp/): date-of-service taxonomy and per-measure rule grid (now with strategy cascade S0a-S7, per-measure `dos_policy` schema, copy-forward detection algorithm, provenance column contract, and M1-M12 capability punch list), assertion / negation framework with ConText 4 dimensions, extraction patterns (sections, abbreviations, copy-forward, telehealth, outside records / OCR, provider attribution, doc-type classification), terminology mapping (LOINC / SNOMED / RxNorm / NDC / CVX / CPT / HCPCS / ICD-10), evaluation methodology (span / document / patient-level, IAA, MRRV simulation, drift monitoring), annotation guidelines, synthetic test fixtures.
- **Per-measure deep dives** in [`references/hedis/`](references/hedis/): 24 measure cards covering denominator, numerator, exclusions, NLP signal phrases, **date-of-service rule**, and **assertion / negation pitfalls** per measure.
- **Supplemental data / hybrid sampling** in [`references/hedis-supplemental-data.md`](references/hedis-supplemental-data.md).
- **Canonical model-card template** in [`templates/per-measure-model-card.md`](templates/per-measure-model-card.md): YAML schema + Markdown narrative, YAML is authoritative on conflict.
- **HEDIS abstraction worksheet** in [`templates/hedis-abstraction.md`](templates/hedis-abstraction.md): auditable per-measure abstraction with provenance, pairs with the model card at runtime.

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill hedis-nlp
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## When the agent loads it

Triggered by requests like:

- "Build a HEDIS extractor for [measure]"
- "Set up date-of-service attribution for [measure]"
- "Design assertion / negation handling for HEDIS NLP"
- "Evaluate a HEDIS NLP model"
- "Write annotation guidelines for [measure]"
- "Write a model card for [measure]"
- "Set up MRRV simulation"
- "Handle supplemental data / hybrid sampling provenance"

Not triggered for: clinical chart review (`medical-chart-review`), HCC NLP (`hcc-nlp`), or PHI handling in non-compliant environments.

## Quick start

```text
I'm building a GSD A1c extractor. What's the canonical date-of-service rule
and what assertion pitfalls should I plan for?
```

The agent will run the PHI/scope gate from `SKILL.md` §0, then load the GSD measure card from [`references/hedis/GSD.md`](references/hedis/GSD.md), the DoS grid from [`references/nlp/date-of-service.md`](references/nlp/date-of-service.md), and the assertion grid from [`references/nlp/negation-and-assertion.md`](references/nlp/negation-and-assertion.md).

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, task routing |
| [references/nlp/](references/nlp/) | Cross-cutting NLP enablement (DoS, assertion, extraction, terminology, evaluation, annotation, fixtures) |
| [references/hedis/](references/hedis/) | 24 per-measure cards |
| [references/hedis-supplemental-data.md](references/hedis-supplemental-data.md) | Supplemental data and hybrid sampling provenance |
| [templates/per-measure-model-card.md](templates/per-measure-model-card.md) | Canonical per-measure model card (YAML + Markdown) |
| [templates/hedis-abstraction.md](templates/hedis-abstraction.md) | Auditable abstraction worksheet |

## Related skills in this repo

- [`medical-chart-review`](../medical-chart-review/) - clinical chart review for clinicians, coders, CDI / quality auditors. Read its `references/coding-icd10-hcc.md`, `quality-measures.md`, and `note-types.md` for the auditor-oriented complement to this skill's NLP-oriented files.
- [`hcc-nlp`](../hcc-nlp/) - HCC / risk-adjustment NLP. HEDIS and HCC are different products; do not conflate.
- [`hipaa-compliance`](../hipaa-compliance/) - HIPAA compliance for the platform hosting this pipeline: BAA review with EHR / annotation / cloud vendors, breach response for extraction-pipeline incidents, OCR audit prep, de-identification methodology if the pipeline produces de-id outputs.
- [`claims-ml`](../claims-ml/) - healthcare-ML failure-mode auditor. Use when this skill's outputs feed a supervised ML model (HEDIS-engine-consumer models, gap-closure prediction); claims-ml audits leakage / calibration / drift / fairness on those downstream models.
- [`healthcare-code-systems`](../healthcare-code-systems/) - foundational code-system reference. Its `references/value-sets-and-vsac.md` (VSAC, OIDs, NCQA HEDIS MY versioning, intensional vs expansion), `references/loinc-and-ucum.md`, and `references/rxnorm-ndc-and-drugs.md` are the data-engineering layer beneath HEDIS measure logic.

## Compliance & safety guardrails

- PHI verification before reading any chart content
- No auto-closure of care gaps without provenance
- No fabricated denominator / numerator / exclusion logic
- Model card YAML authoritative; required fields enforced
- Explicit deferral to NCQA-certified auditors for MRRV-bound work

## Out of scope

- Clinical chart review by humans
- HCC / risk-adjustment NLP
- BI / analytics layer (this skill produces extraction outputs; rollups live elsewhere)
- Handling identifiable PHI without a confirmed HIPAA-compliant environment

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans before being used for HEDIS reporting, MRRV submission, or any reported quality metric.
