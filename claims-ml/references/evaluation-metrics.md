# Evaluation Metrics for Claims-Based ML

Two audiences disagree about what "good" means. Actuaries want decile lift, Lorenz, calibration. ML teams want AUROC, AUPRC, F1. Both can be wrong on their own. This file gives the dual lens and a per-target metric guide.

## §1. The two lenses

### Actuary lens

The actuary's question: "If I act on the top decile, how much of the action (cost, admits, gap closures) do I capture, and is my predicted total close to the realized total?"

| Metric | What it measures | Why actuaries care |
|---|---|---|
| Decile lift @ K | Mean target in top-K decile / mean target in population | Translates directly to ROI on intervention budget |
| Lorenz curve / Gini | Inequality of predicted vs realized | Visualizes concentration of cost / risk |
| Calibration plot (deciles or quantiles) | Predicted vs realized within each decile | Required for any model that drives financial decisions |
| Captured-target-in-top-K% | Sum of target in top-K / total target | "If we work the top 5%, what fraction of cost do we touch?" |
| MAPE on positives | Mean absolute percentage error among non-zero | Cost-prediction accuracy for the population that matters |
| Total predicted vs total realized | Sum agreement | Pricing / reserving sanity check |

### ML lens

The ML team's question: "How well does the model rank, classify, or score relative to a baseline?"

| Metric | What it measures | Where it misleads |
|---|---|---|
| AUROC | Probability a random positive ranks above a random negative | Insensitive to calibration; rewards rank-order even when probabilities are nonsense |
| AUPRC | Precision over recall curve | Sensitive to prevalence; good for imbalanced classification |
| F1 | Harmonic mean of precision and recall at a threshold | Hides threshold dependence; not useful for ranking targets |
| Brier score | Squared error of probability prediction | Good calibration proxy; penalizes confidence on errors |
| Log loss | Average negative log probability of the truth | Penalizes confident wrong answers more |
| Accuracy | Fraction correct | Useless at low prevalence (predict "no admit" = 92% accuracy) |
| R² (cost regression) | Variance explained | Overstates fit on heavy-tailed targets; sensitive to outliers |
| MAE / RMSE | Absolute / squared regression error | RMSE on PMPM dominated by tail; MAE more interpretable for cost |

### When each lens is sufficient on its own

Almost never. A claims-ML model report should always include both an actuary-lens metric set and an ML-lens metric set. A model that beats baseline AUROC but flatlines calibration is not ready to ship. A model that has perfect deciles but no AUROC improvement over the baseline is not learning anything new.

---

## §2. The per-target metric guide

For each target, the agent should require the model report to include the metrics in the "required" column and refuse to bless the model if it relies solely on a metric in the "forbidden as sole" column.

| Target | Required | Forbidden as sole | Highly recommended |
|---|---|---|---|
| Cost (PMPM, regression) | Calibration plot by decile, Lorenz / Gini, MAPE on positives, total predicted vs realized | R², AUROC | Stratified calibration by age band, dual-eligibility, race / ethnicity |
| Hospitalization (binary, 90d) | AUROC, AUPRC, calibration plot, decile lift @ top decile | Accuracy, F1 alone | Subgroup AUROC, captured-admits @ top decile |
| Readmit (30d) | AUROC, AUPRC, calibration, sensitivity to threshold | Accuracy | Cause-specific hazard performance if competing risks modeled |
| ED utilization (count) | Calibration of mean prediction by decile, Poisson deviance, top-decile captured-visits | R² | Per-utilization-band performance |
| Disease onset | AUROC, AUPRC at very low prevalence, top-percentile precision | F1 | Time-to-event ROC if survival framing |
| Mortality | Brier score, calibration plot, AUROC, sensitivity by subgroup | AUROC alone | Stratified by age band, dual status |
| Eligibility scoring | Precision @ K (top recommendations), reviewer-confirmation rate | AUROC vs reviewer label | Downstream outcome impact metrics |
| Anomaly detection | Precision @ K (audit budget K), recall of validated cases | AUROC | Per-specialty performance |
| Composite | Per-component metrics from above | Composite-only metric | Each component independently |

---

## §3. What AUROC hides (worked examples)

### Two models with the same AUROC, different calibration `[synthetic]`

```
Population: 100,000 members. True admit rate: 8.5%.

Model A:
  AUROC: 0.78
  Top decile: predicted rate 18%, realized rate 26%   <-- under-predicts
  Brier: 0.061

Model B:
  AUROC: 0.78
  Top decile: predicted rate 24%, realized rate 25%   <-- well-calibrated
  Brier: 0.052
```

Model A and Model B rank identically. Model A's predicted probabilities are off by 30%. If the action is "any member with predicted probability > 0.20 gets care management", Model A flags ~35% fewer members than Model B. AUROC missed it.

### Cost model `[synthetic]`

```
Population: 50,000 MA members.

Model X (XGBoost on 200 features):
  R²:                          0.42
  Top decile captured cost:    47%
  Calibration in top decile:   predicted $4,200; realized $5,650  <-- 26% under
  Total predicted PMPM:        $830 vs realized $890  <-- 7% under overall

Model Y (regression on 4 features):
  R²:                          0.31
  Top decile captured cost:    44%
  Calibration in top decile:   predicted $5,500; realized $5,650  <-- 3% under
  Total predicted PMPM:        $885 vs realized $890  <-- well-calibrated
```

Model X has better R². Model Y is more useful for budgeting. The actuary uses Model Y. The ML team is celebrating Model X. Both are reading the same training results.

---

## §4. Calibration: required for any model that drives a dollar decision

A calibration plot is required for: cost prediction, ED count, mortality, eligibility scoring, any model whose output is consumed as a probability or a dollar value.

**How to build one.**

1. Rank members by predicted score.
2. Bin into deciles (or 20-quantiles for larger test sets).
3. Within each bin: compute mean predicted value and mean realized value.
4. Plot mean predicted vs mean realized. The 45-degree line is perfect calibration.

**Acceptable calibration.** Mean predicted within ±10% of mean realized in every decile. Stricter for the top deciles (those drive the action).

**Common failures.**

- "Hockey stick": well-calibrated middle deciles, top decile under-predicted by 20-40%. Tail-collapse pattern from log-cost regression or truncation.
- "Pancake": all deciles predict roughly the same value (model not learning). Often signals broken feature pipeline.
- "Inverted in low deciles": low predicted bin has higher realized rate. Usually missingness handled wrong (no-claim members coded as low-risk).

---

## §5. Subgroup calibration

Population-level calibration can hide subgroup failure. Required subgroup splits at minimum:

- Age band (18-44, 45-64, 65-74, 75-84, 85+)
- Sex
- Dual-eligibility status
- Race / ethnicity (if available; if not, imputed via BISG with documented caveat)
- Geographic region (CBSA-level or state-level)

If calibration differs by more than 15% between two subgroups in the same decile, that is a Fairness finding. Cross-link [`fairness-and-equity.md`](fairness-and-equity.md).

---

## §6. Threshold-based metric reporting

For any model that drives action at a threshold (e.g., "members with predicted probability > 0.20 enroll in care management"), report:

- Confusion matrix at the production threshold.
- Precision and recall at the production threshold.
- Volume implications: predicted number of members above threshold per month.
- Capacity check: does the volume match the program's capacity?

A model that flags 5,000 members per month for a program that has capacity for 300 is not deployable as-is.

---

## §7. Bootstrap confidence intervals

Any reported metric should include a 95% bootstrap CI when the test set has < 5,000 positives. Without intervals, a 0.78 AUROC and a 0.74 AUROC look meaningfully different and may not be.

```
Bootstrap procedure (pseudocode):
  for b in 1..1000:
    sample test set with replacement
    compute metric on sample
  report 2.5th, 50th, 97.5th percentiles
```

---

## §8. Metric-set audit checklist

```yaml
metric_audit:
  actuary_lens_metrics_present:   PASS | FAIL
  ml_lens_metrics_present:        PASS | FAIL
  calibration_plot_present:       PASS | FAIL | N/A_classification_only
  subgroup_calibration_present:   PASS | FAIL
  ci_or_bootstrap_present:        PASS | FAIL
  forbidden_sole_metric_avoided:  PASS | FAIL
  threshold_volume_documented:    PASS | FAIL | N/A
  beats_baseline_on_actuary:      PASS | FAIL
  beats_baseline_on_ml:           PASS | FAIL
overall: PASS | FAIL
```

A FAIL on `beats_baseline_on_actuary` or `beats_baseline_on_ml` is Critical. The baseline is defined in [`baselines-and-benchmarks.md`](baselines-and-benchmarks.md).

---

## §9. Reporting template (required minimum)

Every model-card metric block should answer:

1. What is the target, and what action does it drive?
2. What is the baseline, and how much does this model beat it?
3. Calibration plot at population level and for the named subgroups.
4. Decile lift table.
5. Captured-target-in-top-K% at the K that matches program capacity.
6. AUROC and AUPRC with bootstrap CI.
7. Threshold-based confusion matrix at the production threshold.
8. Per-subgroup performance summary.

Anything less is incomplete.
