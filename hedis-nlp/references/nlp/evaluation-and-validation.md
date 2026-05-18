# Evaluation and validation for HEDIS chart-review NLP

How to evaluate per-measure HEDIS extractors so that performance numbers reflect downstream measure-rate impact. Pairs with [`annotation-guidelines.md`](annotation-guidelines.md) (gold standard production) and the per-measure cards in [`../hedis/`](../hedis/).

## Audience

NLP / ML engineers, evaluation leads, clinical informaticists, and analytics teams who need to know if a model is good enough to ship into HEDIS workflows.

## Scope

- Span-level vs document-level vs patient-level metrics
- Inter-annotator agreement (IAA)
- MRRV simulation (defending evidence against NCQA validation)
- Downstream measure-rate sensitivity
- Failure-mode catalog (template + worked examples)
- Drift monitoring in production

Not in scope: model training, hyperparameter search, infrastructure.

---

## 1. Metrics that matter

### Span-level (intrinsic)

For each measure's extraction task:

| Metric | Definition | When it matters |
|---|---|---|
| Precision | TP / (TP + FP) | False positives drive provider abrasion (false closure) and audit failures |
| Recall | TP / (TP + FN) | False negatives drive missed measure closure and revenue / Star impact |
| F1 | Harmonic mean | Single-number summary; useful for tracking deltas |
| Exact-match vs partial-match span | Counting style for entity spans | Date and value extractions usually need exact-match; concept spans tolerate partial |
| Per-attribute accuracy | Date correct? Assertion correct? Provider role correct? | HEDIS evidence is multi-field; per-field metrics surface where pipelines fail |

### Document-level (per-note)

- Does the note contain qualifying evidence for measure M? (binary classification per note)
- Precision/recall at the note level; useful for prioritizing reviewer queues

### Patient-level (extrinsic, business-relevant)

- For patient P and measure M: did the extractor produce evidence that closes the gap, and is that closure correct?
- **This is what plans care about.** Span-level F1 means little if the patient-level decision is wrong.

### Patient-level confusion matrix

|  | True compliant | True non-compliant |
|---|---|---|
| Model: compliant | True closure (TP) | False closure (FP) - audit risk |
| Model: non-compliant | Missed closure (FN) - revenue/Star impact | True open (TN) |

Compute precision and recall at the patient level for the most operationally meaningful numbers.

### Date-of-service-aware metrics

For DoS-sensitive measures (most of them), a "correct" closure requires:
- Correct concept extraction
- Correct date attribution
- Correct assertion qualification

A model that extracts the right concept with the wrong date is **not correct** for HEDIS purposes. Track these as separate failure categories.

---

## 2. Inter-annotator agreement (IAA)

You cannot evaluate against a gold standard without trust in the gold standard. IAA quantifies that trust.

### When to compute IAA

- Before scaling annotation: pilot with 2-3 annotators on a shared sample
- Periodically during annotation: drift check
- After annotation guideline changes: re-baseline

### Recommended approach

| Task | Metric | Rationale |
|---|---|---|
| Binary measure-level compliance | Cohen's kappa | Two-rater categorical; chance-corrected |
| Multi-rater compliance | Fleiss' kappa | Generalizes Cohen for >2 raters |
| Span boundaries | F1 between annotators | Boundary disagreement is common; F1 captures it cleanly |
| Categorical attributes (assertion, date type) | Cohen's / Fleiss' kappa | Attribute-by-attribute |
| Date extraction | Exact match accuracy | Dates are atomic; partial credit is misleading |

### Interpreting kappa

| Kappa range | Interpretation |
|---|---|
| < 0.40 | Poor; revise guidelines |
| 0.40-0.60 | Moderate; investigate disagreements |
| 0.60-0.75 | Substantial; usually acceptable for production gold |
| > 0.75 | Excellent |

For HEDIS work, target ≥ 0.70 on compliance-level kappa before relying on the gold for model selection.

### Adjudication

When annotators disagree:

- Track every disagreement with its source snippet
- Have a clinical adjudicator (RN / coder / measure SME) resolve
- Update guidelines to address the disagreement pattern
- Re-annotate any cases affected by the guideline change

---

## 3. MRRV simulation

NCQA Medical Record Review Validation (MRRV) is the auditor process that validates a sample of plan-submitted evidence. For NLP-driven submissions, simulate MRRV against your own model output before it leaves your org.

### MRRV-style sampling

- Stratified sample across measures, providers, source-document types
- Disproportionate sampling on high-risk categories (OCR'd outside records, telehealth, copy-forward-prone notes)
- Sample size per measure: 30-50 cases is a reasonable starting point for internal validation; NCQA's actual sample sizes are larger

### What to validate per case

1. Does the source snippet exist in the cited document?
2. Does the snippet say what the model claims it says?
3. Is the date correct?
4. Is the provider role correct?
5. Is the assertion correct (not negated, not historical-only, not future-intent)?
6. Does the evidence satisfy the measure's numerator criteria per current spec?
7. Are exclusions correctly applied?

### Failure rate thresholds

NCQA tolerates very few errors in MRRV. Internal targets should be stricter:

- 0% wrong-patient errors (catastrophic)
- < 1% wrong-date errors
- < 2% wrong-concept errors
- < 5% wrong-attribute (assertion, provider role) errors

If you exceed these internally, do not submit; remediate first.

### Re-findability

Every NLP-driven evidence record must be re-findable. Capture:

- Document ID and version
- Page number (for paginated documents)
- Bounding box or character offset (for layout-aware extraction)
- Verbatim snippet (not paraphrase)

See [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) for the broader provenance picture.

---

## 4. Downstream measure-rate sensitivity

Span-level metric deltas can be small while the downstream measure rate moves significantly (or vice versa). Always compute measure-rate impact alongside intrinsic metrics.

### Sensitivity analysis approach

For each model candidate:

1. Apply to a population sample (held-out evaluation cohort, ideally with adjudicated gold for that population)
2. Compute the measure rate the model would produce (numerator / denominator using model's evidence)
3. Compute the measure rate using gold-standard evidence on the same cohort
4. Report the delta in percentage points and as a relative delta

A 0.01 F1 improvement that closes 200 additional patients (real evidence) is far more valuable than a 0.05 F1 improvement that comes from cleaning up easy-to-find cases.

### Cohort considerations

- Stratify by provider, geography, source-document mix, demographic, age band
- Watch for cohort-level bias: a model that's accurate on average but poor for a specific subgroup creates fairness and operational risk
- Compare to the no-NLP baseline (admin-only measure rate) to quantify NLP lift

---

## 5. Failure-mode catalog (template)

Maintain a per-measure catalog of failure modes observed during evaluation. This becomes the regression test suite, the guideline-revision trigger list, and the model-improvement backlog.

### Catalog entry template

```yaml
failure_id: GSD-FM-001
measure: GSD
discovered_date: 2025-XX-XX
discovered_by: <annotator/reviewer id>
category: date-of-service  # or: negation, copy-forward, abbreviation, OCR, provider-role, etc.
description: >
  Model extracted A1c value from a copy-forwarded HPI line, attributed
  to current note date instead of original measurement date 4 months prior.
example_snippet: "Last A1c 7.1 in Mar 2024" appearing in a note dated Jul 2024
patient_impact: Incorrect closure for current MY
root_cause: >
  Extractor uses note-date as fallback when no explicit result-date is parsed
  in the same sentence; missed the embedded date.
mitigation: >
  Extend date-extraction regex to capture "in <month> <year>" trailing patterns;
  add to regression fixtures.
status: open  # or: triaged, in-progress, fixed, verified
related_fixtures:
  - test-fixtures/gsd-copy-forward-001.txt
linked_card_section: "GSD.md - Date of service rule"
```

### Sample categories to track

- Date-of-service errors (wrong anchor, wrong window, copy-forward, OCR-mangled date)
- Negation / assertion errors (missed negation, scope error, false-positive negation flip)
- Temporality errors (historical referenced as current, future intent counted as event)
- Experiencer errors (family history mistaken for patient)
- Lexical collisions (BPD ambiguity, SI ambiguity, MR ambiguity)
- Provider attribution errors (eligible role mismatch)
- Modality errors (telehealth modality acceptance)
- Outside-record / OCR errors
- Copy-forward errors
- Sub-indicator confusion (e.g., COA-Med Review vs MRP)
- Spec-MY drift (model trained on prior MY)

---

## 6. Drift monitoring in production

Once a model ships, performance degrades. Monitor continuously.

### What to monitor

| Signal | What it tells you |
|---|---|
| Closure rate over time | Sudden drops suggest pipeline breakage; sudden spikes suggest false positives |
| Source-document mix shifts | New HIE feed or OCR vendor can change extraction quality silently |
| OCR confidence distribution | Drift indicates upstream OCR / scanner changes |
| Doc-type classifier distribution | New note templates or vendor upgrades change the input mix |
| Provider-attribution success rate | Credentialing-roster drift |
| Date-extraction missingness | Pipeline regression on date capture |
| Reviewer override rate | Human reviewers correcting model output - rising rate = degradation |
| Spec-MY transitions | Annual MY change must trigger re-validation |

### Cadence

- Weekly: pipeline health metrics, closure-rate trends, override rates
- Monthly: source-document mix, OCR drift, attribution accuracy on a small audit sample
- Quarterly: full re-evaluation against gold cohort
- Annually: full spec-MY revalidation before HEDIS reporting cycle

### Drift response playbook

1. Detect: monitoring alert or audit finding
2. Triage: identify scope (single provider? single source? measure-wide? cohort-wide?)
3. Hypothesize: what upstream change correlates with the drift?
4. Validate: pull representative samples, manually review
5. Remediate: code fix, retraining, guideline update, or both
6. Backfill: re-run on affected period if HEDIS reporting window is open
7. Document: failure-catalog entry, regression fixture, postmortem

---

## 7. Cross-references

- [`date-of-service.md`](date-of-service.md) - DoS test cases (use as starter regression fixtures)
- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion test cases (use as starter regression fixtures)
- [`annotation-guidelines.md`](annotation-guidelines.md) - producing the gold standard
- [`extraction-patterns.md`](extraction-patterns.md) - upstream pipeline that this evaluates
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - MRRV and provenance
- [`../../templates/per-measure-model-card.md`](../../templates/per-measure-model-card.md) - canonical model documentation that ties extraction, evaluation, and deployment together
- [`test-fixtures/README.md`](test-fixtures/README.md) - synthetic notes for regression testing
