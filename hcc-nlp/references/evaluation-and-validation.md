# Evaluation and validation for HCC NLP

> **Why this file exists:** Standard NLP metrics (token F1, span F1) substantially understate the operational and audit risk of HCC pipelines. HCC needs hierarchy-aware, dollar-weighted, encounter-scoped, MEAT-conditioned metrics. This file gives you the metric set and the gold-standard construction process.

The HEDIS NLP evaluation reference lives in the sibling `hedis-nlp` skill's `references/nlp/evaluation-and-validation.md` (in this same repo). The general structure (span / document / patient-level, IAA, drift) carries over; HCC-specific extensions are below.

---

## 1. The unit-of-analysis question

Pick the unit explicitly. Mixing them produces meaningless aggregate numbers.

| Unit | Definition | When useful |
|---|---|---|
| **Span-level** | Each diagnosis mention is a unit | Annotator IAA, error analysis, candidate-generation quality |
| **Encounter-HCC** | One unit per (encounter, HCC) pair | Validate-engine quality, MEAT and assertion quality |
| **Member-year-HCC** | One unit per (member, year, HCC) | Suspect-engine quality, RAF-impact estimation |
| **Member-year-RAF** | Member's total RAF for the year | Business-level summary, board-level reporting |

Report at the relevant unit for the audience. RAF-level summaries hide hierarchy and assertion bugs; span-level reports hide business impact.

## 2. Required metrics for a validate engine

For each HCC, compute on a labeled encounter-level set:

- **Precision** = validated HCC predictions that are truly correct / all validated predictions
- **Recall** = validated HCC predictions that are truly correct / all true HCCs in the set
- **F1** = harmonic mean
- **Precision @ confidence threshold** = precision at the threshold used for auto-validation
- **Recall @ confidence threshold** = recall at the same threshold
- **AUPRC** = area under precision-recall curve (better than ROC for imbalanced HCC distributions)
- **MEAT-conditioned precision** = of validated HCCs, the fraction with verifiable MEAT linkage
- **Assertion-conditioned precision** = of validated HCCs, the fraction with correct assertion class

For audit posture, precision targets are typically much higher than recall targets. A common framing: a validated HCC submitted to claims should have precision above 0.95 on a held-out gold set; recall is whatever it is at that precision.

## 3. Required metrics for a suspect engine

For each HCC, compute on a labeled member-level set:

- **Precision @ K** = of top K suspects, how many actually have the HCC
- **Recall @ K** = of all true HCC members, how many appear in top K
- **Mean reciprocal rank** = how high up the worklist real positives appear
- **Lift over claims-only baseline** = how many more true positives surfaced vs the prior-year claims list

Suspect engines tolerate lower precision (the cost of a false positive is a wasted reviewer minute) but reward higher recall (the cost of a false negative is missed RAF dollars).

## 4. Hierarchy-aware metric computation

Apply hierarchies to both predictions and gold standard before computing metrics. Failing to do this misattributes errors.

Example:

```
Gold:        {HCC 18}                     (HCC 19 was suppressed by hierarchy)
Prediction:  {HCC 18, HCC 19}
Naive metric: 1 TP (18), 1 FP (19)        precision 0.5
Hierarchy-aware: prediction collapses to {HCC 18}, perfect match
```

The naive metric punishes the pipeline for a hierarchy bug it did not have. Conversely:

```
Gold:        {HCC 18}
Prediction:  {HCC 19}
Naive metric: 0 TP, 1 FP, 1 FN            precision 0, recall 0
Hierarchy-aware: prediction is in the same family but wrong specificity; report as a specificity error separately
```

The naive metric also hides specificity errors, which have different operational meaning than category errors.

Recommended: report both naive and hierarchy-aware versions, plus a "within-family specificity error" rate as a separate signal.

## 5. Dollar-weighted metrics

Weight by HCC coefficient (or normalized RAF contribution):

- **RAF precision** = sum of true-positive RAF dollars / sum of all predicted RAF dollars
- **RAF recall** = sum of true-positive RAF dollars / sum of all gold RAF dollars
- **RAF dollars missed** = sum of false-negative RAF dollars
- **RAF dollars over-claimed** = sum of false-positive RAF dollars

These are the metrics that operations leadership wants. They are also the metrics that translate most directly to audit risk: RAF dollars over-claimed is a direct estimate of refund exposure if every false positive were detected by RADV.

Pair with the model-version, payment year, and county base rate to translate into actual dollars when needed.

## 6. Per-HCC vs averaged metrics

- **Per-HCC**: F1, precision, recall for each HCC. Surfaces specific HCCs where the model is weak.
- **Macro-averaged**: simple mean across HCCs. Treats every HCC equally; downweights the impact of common HCCs.
- **Micro-averaged**: pooled true positives / false positives / false negatives. Dominated by common HCCs.
- **RAF-weighted average**: weighted by HCC coefficient. Most business-relevant.

Always report per-HCC. Macro is misleading. Micro and RAF-weighted are both useful summaries; pick based on audience.

## 7. MEAT and assertion as separable subtasks

Decompose validation errors:

- **Candidate generation error**: HCC was not surfaced at pass 1
- **Assertion classification error**: HCC was surfaced but assertion (history-of, family, hypothetical, hedging) was wrong
- **MEAT detection error**: HCC was surfaced with correct assertion but MEAT was missed (or wrong evidence credited)
- **Hierarchy application error**: HCC was correctly extracted but not deduplicated
- **DoS / setting error**: HCC was correctly extracted but attributed to wrong DOS or wrong setting

Compute confusion matrices for each error type. They drive different fixes:

- Candidate errors → retrain or extend the pass-1 extractor / crosswalk
- Assertion errors → improve assertion classifier or add rules
- MEAT errors → improve MEAT linkage logic
- Hierarchy errors → fix the post-roll-up code
- DoS errors → fix the metadata propagation

A single accuracy number hides which of these is broken.

## 8. Gold-standard construction

Quality of gold standard caps the quality of every metric above. HCC gold standards are expensive because they require coder-level judgment, not just clinician annotation.

Process:

1. **Sample selection.** Stratify by HCC and by encounter type to avoid common-HCC overrepresentation. Include known difficult cases (history-of, hierarchy collisions, AWV templates, scanned PDFs).
2. **Annotation guidelines.** Use [`annotation-guidelines.md`](annotation-guidelines.md). Include MEAT linkage rules, assertion taxonomy, hierarchy convention (annotate at extracted-code level OR at post-hierarchy level - pick one and document).
3. **Double-coding for IAA.** Two independent coders per encounter. Aim for Cohen's kappa above 0.7 per assertion dimension. HCC annotation IAA is harder than HEDIS; budget for it.
4. **Adjudication.** Disagreements adjudicated by a senior coder. Adjudication notes feed back into the guidelines.
5. **Per-HCC volume targets.** Common HCCs (diabetes, CHF, COPD) need hundreds of positive examples each. Long-tail HCCs may have to rely on synthetic supplementation, with caveats.
6. **Versioning.** Gold standard versions track guideline versions. Re-evaluate prior pipeline runs only against the gold version they were tested on.

## 9. RADV-style audit as an internal eval pattern

Run a periodic internal RADV simulation:

1. Sample a stratified subset of member-years from claims data.
2. For each member-year, pull the supporting documentation (charts that should support the claimed HCCs).
3. Coder reviews the chart against each claimed HCC and verdicts (validated / invalid / needs more info).
4. Compare coder verdict to pipeline output. Compute validation rate and the per-HCC breakdown of failures.
5. Investigate the top failure categories. Use them to drive pipeline fixes and provider documentation feedback.

This is the closest internal proxy for what CMS RADV actually measures. It is also a defensible posture if the plan is later audited - having an internal program is a mitigating factor.

## 10. Drift monitoring

HCC models, terminologies, clinical practice, and templates all drift. Track over time:

- Per-HCC capture rate, by month
- Per-HCC validation rate, by month
- Per-HCC suspect-engine precision and recall (against a held-out periodic gold)
- Assertion-class distribution (sudden shift in "history-of" rate often signals an upstream template change)
- MEAT-linkage rate
- Average confidence by HCC
- Hierarchy collision rate (how often pass 2 emits two HCCs in the same family)

Sudden changes signal something upstream changed (EHR template update, new specialty starting to contribute charts, new outside-record feed). Investigate before assuming the model is broken.

## 11. Comparison to claims as a sanity check

Almost every HCC pipeline should sanity-check against historical claims:

- **HCCs you find that claims also had:** validate baseline; should be high
- **HCCs you find that claims did NOT have:** recapture opportunities (or false positives - need review)
- **HCCs claims had that you did NOT find:** miss; investigate why (chart not in feed? extraction miss? assertion bug?)

A pipeline that disagrees with claims in unexpected directions deserves a careful look before deployment.

## 12. Failure-mode catalog

Maintain a living catalog of observed failure modes. Each entry:

- Description and minimal reproducer (link to a test fixture in [`test-fixtures/`](test-fixtures/) when possible)
- Root cause (which pipeline stage)
- Fix applied
- Regression test added
- Dollar impact estimate at scale

This catalog is the team's institutional memory. New team members read it before making changes. It also makes audit-defense narratives much easier to write.

## 13. Reporting cadence

- **Pipeline runs**: per-HCC precision, recall, RAF dollars by run
- **Weekly**: drift dashboard, top failure modes
- **Monthly**: per-HCC breakdown vs prior month, comparison to claims
- **Quarterly**: internal RADV simulation results, gold-standard refresh stats
- **Annually**: model-version change impact analysis (when CMS publishes new model)

## See also

- [`annotation-guidelines.md`](annotation-guidelines.md) - gold-standard construction details
- [`compliance-and-enforcement.md`](compliance-and-enforcement.md) - audit context for precision targets
- [`hierarchies.md`](hierarchies.md) - hierarchy-aware metrics
- [`raf-calculation.md`](raf-calculation.md) - RAF-weighted metric basis
- Sibling `hedis-nlp` skill, `references/nlp/evaluation-and-validation.md` - shared HEDIS evaluation framework
