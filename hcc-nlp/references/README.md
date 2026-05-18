# CMS-HCC / risk-adjustment NLP enablement

This directory is for **data-science / NLP teams** building extractors for CMS-HCC, V24 legacy, and HHS-HCC (ACA marketplace) risk-adjustment models. It packages the chart-review knowledge in the rest of this skill into model-friendly form: shared rules, pitfalls, exemplar HCC cards, test fixtures, and evaluation patterns.

The auditor-facing summary lives in the sibling `medical-chart-review` skill's `references/coding-icd10-hcc.md` (in this same repo). The files here tell you **how to extract HCCs reliably** at scale, including the failure modes that drive RADV findings and FCA enforcement.

## Audience

- NLP / ML engineers building HCC suspect, validate, or end-to-end risk-adjustment extractors
- Clinical informaticists annotating training and eval data for HCC tasks
- Coding-QA leads spec'ing model evaluation against RADV-style audits
- Compliance / risk teams reviewing model behavior before deployment

## Files

| File | Purpose |
|---|---|
| [`model-versions.md`](model-versions.md) | CMS-HCC V28 vs V24 vs HHS-HCC: phase-in schedule, scope differences, when to use each |
| [`raf-calculation.md`](raf-calculation.md) | RAF formula, demographic + disease + interaction components, normalization, annual reset |
| [`meat-criteria.md`](meat-criteria.md) | Monitor / Evaluate / Assess / Treat with NLP-detectable patterns and per-category extraction signals |
| [`hierarchies.md`](hierarchies.md) | HCC trumping rules, condition categories, deduplication logic for pipelines that emit multiple HCCs in the same family |
| [`date-of-service.md`](date-of-service.md) | Calendar-year reset, face-to-face requirement, telehealth eligibility post-COVID, acceptable provider types |
| [`negation-and-assertion.md`](negation-and-assertion.md) | History-of vs active (the #1 RADV finding), status codes, inpatient vs outpatient probable/likely rule, family-history confounds |
| [`extraction-patterns.md`](extraction-patterns.md) | Suspect vs validate pipelines, problem-list-only invalidity, provenance requirements, two-pass architectures |
| [`terminology-mapping.md`](terminology-mapping.md) | ICD-10 → HCC V28 / V24 / HHS-HCC crosswalks, where to source the CMS files, mapping gotchas |
| [`evaluation-and-validation.md`](evaluation-and-validation.md) | RADV-style audit methodology, per-HCC precision / recall, gold-standard construction, drift monitoring |
| [`annotation-guidelines.md`](annotation-guidelines.md) | Span / attribute schema for HCC labeling, adjudication workflow, IAA targets |
| [`compliance-and-enforcement.md`](compliance-and-enforcement.md) | RADV mechanics, FCA / OIG enforcement context, why over-coding is existential risk for an MA plan |
| [`cards/`](cards/) | Exemplar per-HCC cards covering the major NLP failure modes; schema for team to build the rest |
| [`test-fixtures/`](test-fixtures/) | Synthetic note snippets with expected HCC outputs covering the worst failure modes |
| [`../templates/hcc-model-card.md`](../templates/hcc-model-card.md) | Canonical YAML + Markdown model card template per HCC |
| [`../templates/hcc-audit-nlp.md`](../templates/hcc-audit-nlp.md) | NLP-assisted auditor worksheet |

## How to use this directory

1. Read [`model-versions.md`](model-versions.md) first. Almost every other decision depends on which model you are targeting (V28, V24, or HHS-HCC) and the current phase-in blend.
2. Read [`meat-criteria.md`](meat-criteria.md), [`negation-and-assertion.md`](negation-and-assertion.md), and [`hierarchies.md`](hierarchies.md) before writing any extraction code. These are the three places where most HCC NLP pipelines silently fail.
3. Use the [exemplar HCC cards](cards/) as templates. The six cards we provide were chosen to exercise every major failure mode (hierarchy, status codes, history-of, MEAT, chronicity, Z-code conflations). Build your remaining HCC inventory by mirroring the 9-section card schema.
4. Document your model using [`../templates/hcc-model-card.md`](../templates/hcc-model-card.md). One card per HCC, or per HCC family with hierarchy notes.
5. Build regression coverage from [`test-fixtures/`](test-fixtures/) early, then expand to internal corpora.

## Core principles

1. **MEAT is the contract, not the ICD code.** A code without MEAT in a face-to-face encounter from an acceptable provider is not a valid HCC, regardless of how confident the extractor is.
2. **History-of and status are first-class assertion classes.** They are not "negation". They require explicit handling separate from negation / family / hypothetical.
3. **Hierarchies are not optional.** Pipelines that emit both HCC 18 (Diabetes w/ Chronic Complications) and HCC 19 (Diabetes w/o Complications) for the same member inflate RAF and fail audit.
4. **Calendar-year reset is unforgiving.** December documentation does not carry to January. Pipelines must be time-aware.
5. **Suspect ≠ validate.** Suspecting an HCC ("this member may have HCC X") and validating an HCC ("this DOS supports HCC X") are different tasks with different precision / recall targets. Most teams should build both.
6. **Over-coding is the existential failure mode.** False positives in HCC extraction map directly to FCA / RADV exposure for the MA plan. Precision targets are typically much higher than recall targets. See [`compliance-and-enforcement.md`](compliance-and-enforcement.md).

## Library landscape (clinical NLP for HCC)

Named without version pins on purpose; **verify currency before adoption**:

- **medspaCy** - clinical spaCy components, ConText implementation, useful for assertion and target-rule matching
- **negspacy** - lightweight NegEx for spaCy; usually insufficient on its own for HCC (does not handle history-of / status well)
- **pyConTextNLP** - reference ConText implementation; handles historical, hypothetical, experiencer, negation
- **scispaCy** - biomedical NER + UMLS linking; useful for ICD-10 candidate generation
- **Apache cTAKES** - end-to-end clinical NLP, includes dictionary lookup against UMLS and CUI assertion
- **CLAMP** - clinical NLP toolkit with GUI; good for annotation projects
- **MedCAT** - SNOMED / UMLS concept annotation; useful for HCC candidate generation when paired with a crosswalk

LLM-based approaches (zero-shot, instruction-tuned models on clinical text) can supplement rule-based extraction but should never auto-submit HCCs without human review. See [`evaluation-and-validation.md`](evaluation-and-validation.md) and [`compliance-and-enforcement.md`](compliance-and-enforcement.md).

## Out of scope here

- Actual model code, training scripts, or hosted inference
- CMS HCC crosswalk files themselves (proprietary distribution, change annually; we link to source)
- FHIR or X12 transformation code
- PHI handling, de-identification, or compliance controls (out of skill scope)
- LLM prompt templates (model-dependent and fast-changing)
- Internal-only payer rules (each MA plan has supplemental edits; out of scope)

## See also

- Sibling `medical-chart-review` skill, `references/coding-icd10-hcc.md` - auditor-facing HCC reference
- Sibling `hedis-nlp` skill, `references/nlp/` and `references/hedis/` - parallel structure for HEDIS NLP
- [`../templates/hcc-audit-nlp.md`](../templates/hcc-audit-nlp.md) - NLP-assisted human-audit worksheet
- [`../templates/hcc-model-card.md`](../templates/hcc-model-card.md) - model card template
