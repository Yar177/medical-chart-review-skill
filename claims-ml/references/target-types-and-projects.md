# Target Types and Projects - Per-Project Playbook

A catalog of common claims-ML projects with their target definition, common leakage modes, recommended baseline, recommended metrics, and target-specific pitfalls. The agent uses this when the user describes a project type to route to the right starting reference.

For each project: target spec, baseline, metrics, top leakage risks, top pitfalls.

---

## §1. Cost prediction (PMPM forecast)

**Target.** Per-member-per-month allowed cost in a future window (next quarter, next CY).

**Baseline (required to beat).** Prior-year PMPM, optionally plus age band + sex + RAF.

**Recommended specification.** Tweedie regression (power ~1.5) or two-part model (logistic for `cost > 0`, gamma GLM for severity). See [`target-definitions.md`](target-definitions.md) §1.

**Required metrics.** Calibration plot by decile; Lorenz / Gini; MAPE on positives; total predicted vs realized; captured-cost in top decile. See [`evaluation-metrics.md`](evaluation-metrics.md) §2.

**Top leakage risks.**
- L3: RAF circularity (prior-year RAF for prior-year-window cost).
- L1: claim-lag in utilization features.
- L10: V28 transition shifts HCC-derived features.

**Top pitfalls.**
- Truncating tail at P99 to "stabilize" model; results in systematic top-decile under-prediction.
- OLS on raw dollars; fails on heavy-tailed distribution.
- Not normalizing for partial-year enrollment.
- AUROC as a metric (this is regression, not classification).

**Action.** Drives care management enrollment, budget planning, ACO performance benchmarking, capitation pricing.

---

## §2. Hospitalization prediction (90-day, 180-day)

**Target.** Binary IP admit (default unplanned) in `[T+1, T+H]`.

**Baseline.** Logistic regression on age + RAF + prior-12mo admit count + prior-12mo ED count.

**Recommended specification.** Gradient-boosted trees or logistic regression. Avoid neural networks unless feature count > 500.

**Required metrics.** AUROC + AUPRC with CI; calibration plot; decile lift; subgroup calibration; threshold-volume vs program capacity.

**Top leakage risks.**
- L4: label look-ahead if discharge disposition leaks in.
- L8: pre-authorization features for elective admits.
- L1: short-window features without claim-lag buffer.

**Top pitfalls.**
- Including planned admits in label without separating them; degenerate "elective predictor" results.
- Threshold set without checking program capacity.
- Imbalanced classes treated with naive resampling; calibration breaks.
- Treating obs stays inconsistently (decide once: include or exclude).

**Action.** Care management, transitions-of-care programs, network-management decisions.

---

## §3. 30-day all-cause unplanned readmit

**Target.** Unplanned IP admit within 30 days of index discharge. Use CMS HRRP planned-admit algorithm to exclude planned readmits.

**Baseline.** LACE+ score or HOSPITAL score (published, validated, publicly available).

**Recommended specification.** Logistic regression with index-discharge features, OR competing-risks model (Fine-Gray subdistribution) for cleaner death handling.

**Required metrics.** AUROC + AUPRC; calibration; subgroup; threshold-based PPV / sensitivity for program triage.

**Top leakage risks.**
- L4: discharge disposition / discharge summary features that leak from post-discharge.
- L8: post-discharge auth features.
- L1: claim-lag in measuring the readmit event.

**Top pitfalls.**
- Including planned readmits in label.
- Ignoring death as a competing risk; under-predicts in highest-risk subgroups.
- Combining all-cause and condition-specific readmit; usually one or the other.
- Hard population definition (index discharge for what condition? CMS HRRP defines six conditions).

**Action.** Post-discharge follow-up program enrollment, transition-of-care call prioritization.

---

## §4. ED utilization prediction

**Target.** Count of ED visits in `[T+1, T+H]`, or binary `≥ N visits`.

**Baseline.** Prior-12mo ED count (linear regression for count target, threshold for binary).

**Recommended specification.** Negative binomial regression (count target) or logistic regression (binary).

**Required metrics.** Per-utilization-band performance; calibration by decile; captured-visits-in-top-K%.

**Top leakage risks.**
- L1: claim-lag in ED feature.
- L9: cohort selection on recent ED visits (the very signal you want to predict).

**Top pitfalls.**
- Predicting ≥ 1 ED visit (too common to action).
- Treating 1-visit and 8-visit members the same in a binary target.
- ED visit definition varies (urgent care vs ED; observation-converted-to-IP).

**Action.** ED diversion programs, intensive-care-coordination outreach.

---

## §5. Disease onset / progression

**Target.** First claim with target diagnosis in `[T+1, T+H]`, where member had no such claim in `[T-24m, T]` and ≥ 12 months continuous prior enrollment.

**Baseline.** Single recent claim or lab value in adjacent category (e.g., prediabetes flag + obesity for new diabetes).

**Recommended specification.** Logistic regression at low prevalence; consider survival framing for time-to-event.

**Required metrics.** AUROC + AUPRC (AUPRC critical at low prevalence); top-percentile precision; time-to-event ROC if applicable.

**Top leakage risks.**
- L4: lookahead in label (rule-out codes leaking into incident definition).
- L10: code-set transitions shift which codes count as incident.
- L1: lab-result-date lag.

**Top pitfalls.**
- First claim != true onset (left-censoring).
- Including newly-enrolled members; predicts enrollment rather than incidence.
- Combining true onset with prevalence-now-coded.
- Lab progression often precedes claim coding by months; claim-only model lags clinically.

**Action.** Early intervention, disease-management program enrollment, payer-provider gainsharing programs.

---

## §6. Mortality / end-of-life prediction

**Target.** Death within `[T+1, T+H]` (typically 6-month, 12-month).

**Baseline.** Age band + Charlson + prior IP days.

**Recommended specification.** Logistic regression or survival framing (Cox proportional hazards); high attention to calibration over discrimination.

**Required metrics.** Brier score; calibration plot; subgroup calibration; AUROC with CI; PPV at action threshold.

**Top leakage risks.**
- L6: mortality-feed lag (no-claim members assumed alive).
- L7: hospice election lag.
- L4: end-of-life codes used at time of death leaking into features.

**Top pitfalls.**
- Disenrollment censoring not handled.
- Action sensitivity: false-positives can inappropriately push members toward hospice; calibration is the metric that matters.
- Subgroup calibration: mortality model errors concentrate in specific subgroups (age, dual status).

**Action.** Palliative care enrollment, end-of-life care planning, advance-directive outreach. **Highest sensitivity to misuse.**

---

## §7. Program-eligibility scoring (CM, DM, complex care)

**Target.** Eligibility flag for an internal program. Often defined by clinician review of high-risk members.

**Baseline.** Composite risk score (commonly prior-year cost percentile + admit count + chronic-condition count).

**Recommended specification.**
- If targeting clinician-judged eligibility: precision @ K with reviewer-confirmation; high deferral risk.
- Better: target the downstream outcome the program is supposed to prevent (admits, ED, cost) and use as a recommendation system.

**Required metrics.** Precision @ K (top recommendations); reviewer-confirmation rate; downstream outcome impact (long-term).

**Top leakage risks.**
- Model learns reviewer heuristic, not eligibility.
- Outcomes used as features.

**Top pitfalls.**
- "Eligibility" itself is fuzzy and reviewer-dependent.
- No clear ground truth; bootstrapped labels reflect historical biases in program access.
- Capacity-constrained: model output should be calibrated to program throughput.

**Action.** Care-management triage, complex-care navigator assignment.

---

## §8. ICD-10 anomaly detection (FWA, upcoding, profiling)

**Target.** Anomalous coding pattern at provider, member, or claim level. Often unsupervised.

**Baseline.** Distance from specialty-norm coding distribution; MAD-based outlier flag.

**Recommended specification.**
- Supervised when labeled examples (validated FWA) exist; rare and biased.
- Semi-supervised on known-clean baseline.
- Unsupervised: isolation forest, autoencoder, density estimation - per specialty.

**Required metrics.** Precision @ K (audit budget); recall on validated cases (when available); per-specialty performance.

**Top leakage risks.**
- Specialty mix (oncology, palliative, transplant) inherently anomalous; pre-filter.
- Provider-volume effects: low-volume providers look outlying for trivial reasons.

**Top pitfalls.**
- Labels biased toward what auditors caught.
- Anomaly = "rare" not "wrong"; surfaced cases need human review before action.
- High-cost specialty patterns flagged as "anomaly" when actually appropriate care.

**Action.** Audit queue prioritization, FWA investigation, provider-profiling reports.

---

## §9. Risk stratification (general-purpose)

**Target.** Member-level composite risk score for population segmentation. Often a sub-component of cost prediction or hospitalization prediction.

**Baseline.** Prior-year cost decile + RAF + chronic-condition count.

**Recommended specification.** Either a component model (cost or hospitalization) used as the score, or a rule-based stratification using component model outputs.

**Required metrics.** Decile assignment stability month-over-month; rank correlation with prior period; downstream-action segmentation effectiveness.

**Top pitfalls.**
- "Stratification" without a defined action is decoration; require an action per tier.
- Composite scores collapsing multiple targets often have ambiguous calibration.
- Tier boundaries set without capacity/program alignment.

**Action.** Population segmentation, care-tier assignment, member outreach prioritization.

---

## §10. HEDIS-engine consumer models

**Target.** Predictive models built on HEDIS-engine outputs (gap-closure flags, measure-level rates). E.g., "predict which open gaps will close without intervention."

**Baseline.** Historical gap-closure rate by measure and member-engagement segment.

**Recommended specification.** Logistic regression per measure family; do not pool across measures with different mechanics (GSD diabetes care vs CCS-E vs FUH have totally different dynamics).

**Required metrics.** Per-measure precision @ K; member-level outreach efficiency.

**Top leakage risks.**
- Upstream HEDIS-engine version drift.
- Annual HEDIS spec changes shift target definitions.
- Member-engagement features that themselves correlate with the closure outcome.

**Top pitfalls.**
- Treating HEDIS-engine output as ground truth without auditing the engine's precision.
- Pooling measures with different mechanics in one model.

**Action.** Gap-closure outreach prioritization, vendor-team workload assignment.

**Cross-link.** Defer to sibling `hedis-nlp` skill for HEDIS engine internals and per-measure specifications.

---

## §11. Project-selection guidance for the agent

When a user describes a new project, the agent should:

1. Map the project to one of the categories above (or flag if it does not fit).
2. State the required baseline from this file.
3. State the required metric set.
4. State the top 2-3 leakage risks specific to the project type.
5. State the action sensitivity (low: planning; medium: outreach prioritization; high: care decisions; **highest**: mortality / end-of-life / coverage / eligibility / pricing).
6. Recommend the matching reference deep-dives for the user to read before designing the spec.

The catalog is the entry point. The other references in this skill provide the depth.
