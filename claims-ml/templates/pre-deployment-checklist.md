# Pre-Deployment Checklist

> Yes/no gate. Every item must be PASS or explicitly documented N/A before a model goes to production.

A model with any UNRESOLVED Critical finding cannot be deployed. A model with any FAIL on a non-N/A item is not production-ready.

---

## Header

```yaml
checklist_metadata:
  model_name: <name>
  version: <semver>
  target: <target>
  reviewer: claims-ml skill
  review_date: <date>
```

## §0. Safety gate

- [ ] PHI status confirmed (Safe Harbor / synthetic / BAA-covered environment).
- [ ] Scope confirmed; not silently broadened beyond stated target.
- [ ] Disclaimer stated.
- [ ] No real member IDs, NPIs, claim numbers, or provider names in any artifact reviewed.

## §1. Target & population

- [ ] Target definition documented in canonical YAML (see [`references/target-definitions.md`](../references/target-definitions.md#9-target-spec-yaml-canonical)).
- [ ] Target type matches the downstream action.
- [ ] Population definition observable at `T` (not back-filtered by outcome).
- [ ] Partial-enrollment handling documented.
- [ ] Competing risks handled (if applicable: readmit + death, etc.).
- [ ] Left-censoring handled (if applicable: onset models).
- [ ] Planned-vs-unplanned resolved (if applicable: admit / readmit models).
- [ ] Composite-endpoint components separated (if applicable).

## §2. Split

- [ ] Split-spec YAML complete (see [`references/train-test-splits.md`](../references/train-test-splits.md#10-split-spec-yaml-canonical)).
- [ ] Unit of independence = member-year (or documented alternative).
- [ ] Temporal holdout for forward-looking prediction.
- [ ] No random row-level split.
- [ ] MY boundaries crossed by split documented.
- [ ] Code-set version applied uniformly to train / test.
- [ ] Cohort criteria observable at `T`.
- [ ] Label generation does not see post-`T` data.
- [ ] Test set sized for the audience's preferred metrics (see [`references/train-test-splits.md`](../references/train-test-splits.md#9-sample-size-sanity)).
- [ ] Split reproducible from a script.

## §3. Leakage audit

- [ ] Per-feature leakage audit complete using [`templates/feature-spec-audit.md`](feature-spec-audit.md).
- [ ] All Critical leakage findings closed.
- [ ] All High leakage findings closed or explicitly accepted with sign-off.
- [ ] L1 claim-lag mitigated for every utilization feature.
- [ ] L3 RAF circularity does not apply OR is handled.
- [ ] L4 label look-ahead does not occur.
- [ ] L9 cohort-selection leakage does not occur.
- [ ] L10 code-set drift not present across train / test.

## §4. Features

- [ ] Feature count, families, and top-importance list documented.
- [ ] Rolling windows are claim-lag aware.
- [ ] Comorbidity family pinned to a single primary (Charlson / Elixhauser / HCC).
- [ ] Episode grouper version pinned (if used).
- [ ] Missingness regimes distinguished (no-claim vs missing-data).
- [ ] Feature stability validated over 24+ months.
- [ ] Upstream model dependencies pinned (HCC extractor, HEDIS engine, NLP outputs).
- [ ] High-cardinality encoding documented.

## §5. Baseline

- [ ] Required baseline for target present (see [`references/baselines-and-benchmarks.md`](../references/baselines-and-benchmarks.md#1-the-did-you-beat-the-dumb-model-test)).
- [ ] Three-feature linear / logistic benchmark present.
- [ ] Baseline evaluated on the same test set as the challenger.
- [ ] Challenger beats baseline on the actuary-lens metric.
- [ ] Challenger beats baseline on the ML-lens metric.
- [ ] Delta in "suspicious" range flagged for leakage re-audit (if applicable).
- [ ] Operational cost of challenger justified by gain over baseline.

## §6. Evaluation metrics

- [ ] Actuary-lens metrics present (calibration plot, decile lift, Lorenz / Gini, captured-target).
- [ ] ML-lens metrics present (AUROC + AUPRC for binary; Brier for probability; full regression diagnostics for cost).
- [ ] Bootstrap CIs reported for primary metrics.
- [ ] Population-level calibration plot included.
- [ ] No forbidden sole-metric (see [`references/evaluation-metrics.md`](../references/evaluation-metrics.md#2-the-per-target-metric-guide)).
- [ ] Threshold-based confusion matrix at production threshold (classification only).
- [ ] Predicted volume above threshold documented.

## §7. Calibration & subgroup

- [ ] Calibration plot per subgroup: age band, sex, dual-eligibility, race / ethnicity (self-reported or imputed).
- [ ] No subgroup calibration disparity > 15% in any decile.
- [ ] Subgroup AUROC within 0.03 of population AUROC for all subgroups.
- [ ] Subgroup recall ratio > 0.85 (for beneficial-intervention models).
- [ ] Subgroup selection-rate ratio > 0.80 (for binary-action models).

## §8. Fairness

- [ ] Fairness-spec YAML complete (see [`references/fairness-and-equity.md`](../references/fairness-and-equity.md#9-fairness-spec-yaml-canonical)).
- [ ] Target definition does not encode an access disparity (Obermeyer test).
- [ ] Proxy variables for protected classes examined.
- [ ] Imputation method documented (where race / ethnicity is imputed).
- [ ] Mitigation applied OR documented as not-required.
- [ ] Legal counsel review status: complete OR not-required with justification.

## §9. Production scoring

- [ ] Scoring-time feature spec complete (see [`references/production-scoring-constraints.md`](../references/production-scoring-constraints.md#2-the-scoring-time-feature-availability-required-artifact)).
- [ ] Every feature has documented refresh latency.
- [ ] No feature unavailable at scoring time.
- [ ] Scoring cadence matches downstream action.
- [ ] Compute cost fits the runtime budget.
- [ ] Predicted volume at production threshold matches program capacity.
- [ ] Scoring environment matches training environment (libraries, code sets).

## §10. Drift monitoring

- [ ] Drift-monitor spec YAML complete (see [`references/calibration-and-drift.md`](../references/calibration-and-drift.md#8-drift-monitoring-spec-yaml-canonical)).
- [ ] Feature PSI monitor configured.
- [ ] Prediction-distribution monitor configured.
- [ ] Realized-vs-predicted monitor configured (with realization window).
- [ ] Subgroup calibration monitor configured.
- [ ] Thresholds and alert routing documented.
- [ ] Baseline snapshot frozen at deployment.
- [ ] Scheduled annual MY-boundary retrain on the calendar.
- [ ] Shock-handling branch defined.

## §11. Recalibration plan

- [ ] [`templates/recalibration-plan.md`](recalibration-plan.md) populated as a stub ready to use.
- [ ] Recalibrate vs retrain vs deprecate decision tree documented.
- [ ] Owner for recalibration response assigned.

## §12. Model card

- [ ] [`templates/claims-ml-model-card.md`](claims-ml-model-card.md) complete.
- [ ] Canonical YAML block populated.
- [ ] Sign-offs collected from ML lead, actuary, medical director (where applicable), compliance (where applicable), MLOps.

---

## Outcome

```yaml
checklist_outcome:
  all_critical_resolved:     PASS | FAIL
  all_high_resolved_or_signed_off: PASS | FAIL
  any_section_below_PASS:    [list sections, or "none"]
  production_ready:          yes | no
  decision_date:             <date>
  decision_owner:            <name>
```

If `production_ready: no`, document the gap, the owner, and the target re-review date.
