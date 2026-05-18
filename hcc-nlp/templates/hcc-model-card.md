# Per-HCC model card template

Canonical documentation for an HCC extraction model. **The YAML block is authoritative**; the Markdown narrative below it is human-readable elaboration. On conflict, the YAML wins for automated systems and audit purposes.

Use one card per HCC (or per HCC family where the model truly shares architecture, scope, and metrics across multiple HCCs in the family - rare). Store cards in version control next to the model artifacts.

Parallel to the sibling `hedis-nlp` skill's `templates/per-measure-model-card.md` (HEDIS). Same philosophy, HCC-specific fields.

---

## YAML schema (canonical)

```yaml
# ---------------------------------------------------------------
# CANONICAL HCC MODEL CARD - YAML wins on conflict with narrative.
# ---------------------------------------------------------------

hcc_model_card:
  schema_version: "1.0"

  model:
    name: <string>                       # e.g., hcc-18-validate-extractor
    version: <semver string>             # e.g., 2.1.0
    artifact_uri: <string>
    framework: <string>                  # e.g., spacy-3.7 + medspaCy + transformers
    pipeline_mode: <string>              # suspect | validate | both
    created_date: <ISO date>
    created_by: <team or individual>

  hcc:
    primary_hcc:
      model_version: <string>            # CMS-HCC V28 | V24 | HHS-HCC
      hcc_number: <integer>              # e.g., 18
      hcc_name: <string>                 # e.g., Diabetes with Chronic Complications
      payment_year: <integer>            # e.g., 2026
      crosswalk_snapshot_date: <ISO date>
    related_hcc_numbers:                 # if the model also covers within-family hierarchy
      - <integer>
    hierarchy_aware: <boolean>           # does the model apply the family hierarchy?
    icd10_in_scope:                      # ICD-10 codes the model emits as candidates
      - <string>

  scope:
    intent: <string>                     # what the model claims to extract
    in_scope:
      - <string>
    out_of_scope:
      - <string>
    eligible_provider_roles:             # acceptable signing providers
      - <string>
    accepted_encounter_settings:
      - <string>                         # outpatient | inpatient | telehealth | awv | etc.
    accepted_document_types:
      - <string>                         # progress note | consult | H&P | discharge summary

  meat:
    enforces_meat: <boolean>
    meat_categories_required:            # minimum subset required for validation
      - <string>                         # monitor | evaluate | assess | treat
    meat_linkage_method: <string>        # e.g., section-aware + sentence-window heuristic + model
    rejects_problem_list_only: <boolean>
    rejects_medication_list_only: <boolean>

  data:
    training_corpus:
      description: <string>
      n_encounters: <integer>
      n_members: <integer>
      source: <string>                   # real-deidentified | synthetic | mixed
      date_range: <string>
    evaluation_corpus:
      description: <string>
      n_encounters: <integer>
      n_members: <integer>
      gold_standard_source: <string>     # adjudicated human annotation
      annotator_iaa_assertion: <float>
      annotator_iaa_meat: <float>
      annotator_iaa_hcc: <float>
      cohort_strata:
        - <string>

  metrics:
    span_level:
      precision: <float>
      recall: <float>
      f1: <float>
    encounter_hcc_level:
      precision: <float>
      recall: <float>
      f1: <float>
    member_year_hcc_level:
      precision: <float>
      recall: <float>
      f1: <float>
    after_hierarchy_application:         # repeat above metrics post-hierarchy
      precision: <float>
      recall: <float>
      f1: <float>
    raf_precision_recall:
      dollar_weighted_precision: <float>
      dollar_weighted_recall: <float>
    decomposed_error_rates:              # see references/hcc/evaluation-and-validation.md
      candidate_generation_miss: <float>
      assertion_error: <float>
      meat_error: <float>
      hierarchy_error: <float>
      dos_attribution_error: <float>
    radv_simulation:
      simulated_one_way_review: <boolean>
      simulated_two_way_review: <boolean>
      auto_validation_precision: <float> # must be high; see compliance-and-enforcement.md
      simulation_date: <ISO date>
    measured_on: <ISO date>

  failure_modes:
    - id: <string>
      summary: <string>
      regression_fixture_uri: <string>   # link to test fixture covering it
      mitigation_status: <string>

  dependencies:
    upstream_pipelines:
      - <string>                         # OCR, section segmenter, doc-type classifier, etc.
    code_systems:
      icd10_year: <integer>
      hcc_crosswalk_version: <string>    # MUST be pinned; see model-versions.md
      hcc_crosswalk_snapshot_date: <ISO date>
      hcc_hierarchy_file_uri: <string>
      raf_coefficients_file_uri: <string>
      rxnorm_snapshot: <ISO date>
      loinc_release: <string>
      snomed_edition: <string>
    libraries:
      - name: <string>
        version: <string>

  deployment:
    environment: <string>                # production | shadow | eval-only
    auto_validate: <boolean>             # does this model auto-validate to claims?
    auto_validate_precision_floor: <float>  # threshold required before auto-validation
    suspect_to_outreach: <boolean>       # does suspect output drive member / provider outreach?
    monitored: <boolean>
    monitoring_dashboard_uri: <string>
    alert_thresholds:
      precision_drop_pct: <float>
      recall_drop_pct: <float>
      override_rate_max_pct: <float>
      raf_per_member_drift_pct: <float>
    rollback_plan: <string>

  governance:
    owners:
      technical: <string>
      clinical_sme: <string>             # often coding lead (CRC/CCS) for HCC models
      product: <string>
      compliance: <string>               # required for HCC models
    review_cadence: <string>             # quarterly + annual model-version revalidation
    last_review_date: <ISO date>
    next_review_due: <ISO date>
    sign_off:
      clinical: <string>
      coding_lead: <string>
      technical: <string>
      compliance: <string>

  compliance:
    hipaa_assessed: <boolean>
    de_identification_method: <string>   # safe-harbor | expert-determination | n/a
    radv_readiness:
      two_way_review_capable: <boolean>  # can flag invalid HCCs already submitted?
      provenance_recorded: <boolean>     # full audit trail per emission?
      candidate_log_retained: <boolean>  # "considered but not emitted" logged?
    cdi_query_workflow_integrated: <boolean>
    last_compliance_review_date: <ISO date>
    last_compliance_review_findings: <string>

  changelog:
    - version: <semver>
      date: <ISO date>
      change: <string>
      author: <string>
      driver: <string>                   # failure mode id, regulatory change, etc.

  references:
    hcc_card: <relative path>            # e.g., references/hcc/cards/hcc-18-diabetes-with-complications.md
    extraction_patterns: <relative path> # references/hcc/extraction-patterns.md
    meat_criteria: <relative path>       # references/hcc/meat-criteria.md
    hierarchies: <relative path>
    dos_guidance: <relative path>
    assertion_guidance: <relative path>
    terminology_mapping: <relative path>
    annotation_guidelines: <relative path>
    evaluation_methodology: <relative path>
    compliance_guidance: <relative path>
    model_versions: <relative path>
    raf_calculation: <relative path>
```

---

## Markdown narrative (human-readable elaboration)

Use the sections below to elaborate on the YAML for humans. **If the narrative and YAML conflict, the YAML is authoritative.** Update both together.

### Model

Brief plain-language description: what the model does, what HCC it serves, suspect or validate or both, and what it deliberately does NOT do.

### HCC context

- Which CMS model version (V28 / V24 / HHS-HCC) and payment year the model targets
- The crosswalk snapshot date the candidate-generation layer uses
- The hierarchy file used and whether the model applies it (or relies on a downstream step)
- The RAF coefficients file used for any RAF impact metric reported

### Scope and limitations

- Populations and document types in scope
- Acceptable provider roles per [`../references/date-of-service.md`](../references/date-of-service.md)
- Acceptable encounter settings (outpatient, AWV, inpatient, telehealth boundaries)
- Out-of-scope populations (pediatric, hospice, etc.)
- Known edge cases the model handles poorly

### MEAT enforcement

- Whether the model enforces MEAT and how
- Which MEAT categories the model requires for validation
- Linkage method (section-aware, sentence-window, model-scored)
- How problem-list-only and medication-list-only items are handled

### Training data

- Corpus composition (real de-identified, synthetic, mixed)
- Volume and stratification
- Annotation provenance and IAA per dimension (assertion, MEAT, HCC)
- Known data biases (specialty mix, EHR vendor mix, geography, payer mix)

### Evaluation

- Methodology summary (see [`../references/evaluation-and-validation.md`](../references/evaluation-and-validation.md))
- Metrics at each unit of analysis (span, encounter-HCC, member-year-HCC, pre- and post-hierarchy)
- Decomposed error rates (candidate, assertion, MEAT, hierarchy, DoS)
- RAF dollar-weighted precision and recall
- RADV simulation findings (one-way and two-way)
- Subgroup performance (specialty, encounter setting, document type)

### Failure modes

Reference the failure-mode catalog. Summarize the top 3-5 known failure modes, the regression fixtures that cover them (see [`../references/test-fixtures/`](../references/test-fixtures/)), and mitigation status.

### Deployment

- Where the model runs (production, shadow, eval-only)
- Whether outputs auto-validate to claims and what precision floor is required
- Whether suspect outputs drive outreach
- Upstream and downstream dependencies
- Monitoring signals and thresholds (precision, recall, override rate, RAF drift)
- Rollback procedure

### Governance

- Owners across technical, clinical SME, product, and compliance
- Review cadence: at minimum quarterly + annual model-version revalidation when CMS releases the new HCC year
- Sign-off history including coding lead and compliance

### Compliance

- HIPAA assessment status
- De-identification methodology if real data was used
- RADV readiness: two-way review capability, full provenance, candidate log retention
- CDI / provider query workflow integration
- Last compliance review findings and remediation status

See [`../references/compliance-and-enforcement.md`](../references/compliance-and-enforcement.md).

### Changelog

Newest-first list of meaningful changes. Tie each entry to a version, date, and the failure-mode, regulatory change, or model-year update behind the change.

### Cross-references

Per-HCC card, extraction patterns, MEAT criteria, hierarchies, DoS guidance, assertion guidance, terminology mapping, annotation guidelines, evaluation methodology, compliance guidance, model versions, RAF calculation.

---

## Card-versioning conventions

- Bump `model.version` semver for every code or weight change.
- Bump `hcc_model_card.schema_version` only on backward-incompatible YAML schema changes.
- Bump `hcc.crosswalk_snapshot_date` and `hcc.payment_year` when CMS releases a new HCC year; re-run training and evaluation against the new crosswalk before changing these fields.
- Keep prior card versions in git history; do not overwrite.

## Required field discipline for HCC models (stricter than HEDIS)

These fields are non-negotiable for HCC models due to RADV exposure:

- `hcc.model_version` (V28 / V24 / HHS-HCC) MUST be pinned per artifact
- `hcc.crosswalk_snapshot_date` MUST be recorded
- `dependencies.hcc_hierarchy_file_uri` MUST resolve to a versioned artifact
- `compliance.radv_readiness.provenance_recorded` MUST be true for any production model
- `metrics.radv_simulation` MUST be run before any auto-validation deployment

A model card missing any of the above is incomplete and the model should not be considered ready for production.

## See also

- Sibling `hedis-nlp` skill, `templates/per-measure-model-card.md` - parallel HEDIS template
- [`hcc-audit-nlp.md`](hcc-audit-nlp.md) - chart-level audit worksheet that pairs with this model card at runtime
- [`../references/README.md`](../references/README.md) - HCC NLP enablement directory
- [`../references/compliance-and-enforcement.md`](../references/compliance-and-enforcement.md) - regulatory context
- [`../references/evaluation-and-validation.md`](../references/evaluation-and-validation.md) - evaluation methodology
- [`../references/model-versions.md`](../references/model-versions.md) - V28 / V24 / HHS-HCC pinning
- [`../references/cards/`](../references/cards/) - per-HCC cards
