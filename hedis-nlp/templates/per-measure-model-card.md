# Per-measure model card template

Canonical documentation for a HEDIS extraction model. **The YAML block is authoritative**; the Markdown narrative below it is human-readable elaboration. On conflict, the YAML wins for automated systems and audit purposes.

Use one card per measure (or per sub-indicator if the sub-indicators have meaningfully different models). Store cards in version control next to the model artifacts.

---

## YAML schema (canonical)

```yaml
# ---------------------------------------------------------------
# CANONICAL MODEL CARD - YAML wins on conflict with narrative.
# ---------------------------------------------------------------

model_card:
  schema_version: "1.0"

  model:
    name: <string>                       # e.g., gsd-a1c-extractor
    version: <semver string>             # e.g., 1.4.2
    artifact_uri: <string>               # e.g., s3://.../model-v1.4.2.tar.gz
    framework: <string>                  # e.g., spacy-3.7, transformers-4.x, custom
    created_date: <ISO date>
    created_by: <team or individual>

  measure:
    code: <string>                       # e.g., GSD
    name: <string>                       # full measure name
    sub_indicator: <string|null>         # e.g., TRC-Patient, or null
    measurement_year: <integer>          # e.g., 2025
    spec_source: <string>                # e.g., "NCQA HEDIS Volume 2 MY2025"
    spec_version_snapshot_date: <ISO date>

  scope:
    intent: <string>                     # what the model claims to extract
    in_scope:                            # populations / cases / document types in scope
      - <string>
    out_of_scope:
      - <string>
    eligible_provider_roles:
      - <string>
    accepted_document_types:
      - <string>
    accepted_modalities:                 # for telehealth-relevant measures
      - <string>

  data:
    training_corpus:
      description: <string>
      n_documents: <integer>
      n_patients: <integer>
      source: <string>                   # real-deidentified | synthetic | mixed
      date_range: <string>               # e.g., 2022-01-01 to 2024-12-31
    evaluation_corpus:
      description: <string>
      n_documents: <integer>
      n_patients: <integer>
      gold_standard_source: <string>     # adjudicated human annotation
      annotator_kappa: <float>           # IAA on the eval gold
      cohort_strata:                     # what the cohort is stratified by
        - <string>

  metrics:
    span_level:
      precision: <float>
      recall: <float>
      f1: <float>
    document_level:
      precision: <float>
      recall: <float>
      f1: <float>
    patient_level:
      precision: <float>
      recall: <float>
      f1: <float>
    date_attribution_accuracy: <float>
    assertion_attribution_accuracy: <float>
    provider_role_attribution_accuracy: <float>
    downstream_measure_rate_delta_pp: <float>  # vs admin-only baseline
    measured_on: <ISO date>

  failure_modes:                         # link to failure-mode catalog entries
    - id: <string>
      summary: <string>
      mitigation_status: <string>

  dependencies:
    upstream_pipelines:
      - <string>                         # e.g., OCR, doc-type classifier
    code_systems:
      icd10_year: <integer>
      cpt_year: <integer>
      rxnorm_snapshot: <ISO date>
      loinc_release: <string>
      snomed_edition: <string>
    value_set_source: <string>           # e.g., NCQA-licensed snapshot date
    libraries:
      - name: <string>
        version: <string>

  deployment:
    environment: <string>                # e.g., production, shadow, eval-only
    monitored: <boolean>
    monitoring_dashboard_uri: <string>
    alert_thresholds:
      closure_rate_drop_pct: <float>
      override_rate_max_pct: <float>
      ocr_confidence_drop_pct: <float>
    rollback_plan: <string>

  governance:
    owners:
      technical: <string>                # individual or team
      clinical_sme: <string>
      product: <string>
    review_cadence: <string>             # e.g., quarterly + annual MY revalidation
    last_review_date: <ISO date>
    next_review_due: <ISO date>
    sign_off:
      clinical: <string>                 # name + date
      technical: <string>
      product: <string>

  compliance:
    hipaa_assessed: <boolean>
    de_identification_method: <string>   # safe-harbor | expert-determination | n/a
    mrrv_simulation_passed: <boolean>
    mrrv_simulation_date: <ISO date>
    mrrv_simulation_findings: <string>

  changelog:
    - version: <semver>
      date: <ISO date>
      change: <string>
      author: <string>

  references:
    measure_card: <relative path>        # e.g., references/hedis/GSD.md
    extraction_patterns: <relative path> # references/nlp/extraction-patterns.md
    dos_guidance: <relative path>        # references/nlp/date-of-service.md
    assertion_guidance: <relative path>  # references/nlp/negation-and-assertion.md
    terminology_mapping: <relative path>
    annotation_guidelines: <relative path>
    evaluation_methodology: <relative path>
```

---

## Markdown narrative (human-readable elaboration)

Use the sections below to elaborate on the YAML for humans. **If the narrative and YAML conflict, the YAML is authoritative.** Update both together.

### Model

Brief plain-language description of what the model does and what it is not.

### Measure context

What HEDIS measure the model serves, what counts as numerator-satisfying evidence, what the spec MY context is. Cross-link the per-measure card.

### Scope and limitations

- Populations and document types in scope
- Explicit out-of-scope populations (e.g., pediatric for an adult-only model)
- Known edge cases the model handles poorly
- Spec-MY boundary - model behavior for adjacent MYs

### Training data

- Corpus composition (real de-identified, synthetic, mixed)
- Volume and stratification
- Annotation provenance (single annotator, multi-annotator with adjudication)
- Known data biases (geography, EHR vendor mix, payer mix)

### Evaluation

- Methodology summary (see [`../references/nlp/evaluation-and-validation.md`](../references/nlp/evaluation-and-validation.md))
- Headline metrics with context (what good looks like)
- Downstream measure-rate impact vs admin-only baseline
- Subgroup performance (provider type, source-document type, demographic where appropriate)
- Known performance gaps

### Failure modes

Reference the per-measure failure-mode catalog entries. Summarize the top 3-5 known failure modes and their mitigation status.

### Deployment

- Where the model runs (production, shadow, eval-only)
- Upstream and downstream dependencies (OCR, doc-type classifier, measure scorer)
- Monitoring strategy (which signals, which thresholds, who gets alerted)
- Rollback procedure

### Governance

- Who owns the model (technical, clinical, product)
- Review cadence
- Sign-off history
- Last and next review dates

### Compliance

- HIPAA assessment status
- De-identification methodology if real data was used
- MRRV simulation results
- Known compliance gaps and remediation status

### Changelog

Newest-first list of meaningful changes. Tie each entry to a version, date, and the failure-mode or business driver behind the change.

### Cross-references

- Per-measure card in `references/hedis/`
- Date-of-service guidance
- Assertion / negation guidance
- Extraction patterns
- Terminology mapping
- Annotation guidelines
- Evaluation methodology
- Failure-mode catalog entries
- Test fixtures used for regression

---

## Card-versioning conventions

- Bump the `model.version` semver field for every code or weight change
- Bump `model_card.schema_version` only when the YAML schema itself changes (backward-incompatible)
- Keep the prior card version in git history; do not overwrite history
- New review date = today; next review due = today + review cadence

---

## See also

- [`hedis-abstraction.md`](hedis-abstraction.md) - abstraction worksheet that pairs with this model card at runtime
- [`../references/nlp/README.md`](../references/nlp/README.md) - NLP enablement directory
- [`../references/nlp/evaluation-and-validation.md`](../references/nlp/evaluation-and-validation.md) - evaluation methodology
- [`../references/nlp/annotation-guidelines.md`](../references/nlp/annotation-guidelines.md) - gold-standard production
- [`../references/hedis/`](../references/hedis/) - per-measure cards
