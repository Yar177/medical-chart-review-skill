# Baselines & Benchmarks for Claims-Based ML

A model that does not beat a strong baseline is not a model worth deploying. This file defines the required baselines per target and discusses where industry benchmarks are stable enough to use as reference.

## §1. The "did you beat the dumb model" test

Every claims-ML model must beat a target-specific baseline. If it does not, the team has not learned anything new and should not deploy.

| Target | Required baseline |
|---|---|
| Cost (PMPM) | Prior-year PMPM, applied as-is |
| Cost (PMPM, sophisticated) | Prior-year PMPM + age band + sex + RAF |
| Hospitalization (90-day) | Prior-12mo admit count > 0 → flag |
| Hospitalization (sophisticated) | Logistic regression on age + RAF + prior-12mo admit count + prior-12mo ED count |
| Readmit (30-day) | LACE+ or HOSPITAL score |
| Mortality (12-month) | Age + dual-eligibility + Charlson |
| ED utilization | Prior-12mo ED count |
| Onset (e.g., new diabetes) | Prior-year prediabetes flag + BMI > 30 + age |
| Anomaly detection | Median absolute deviation from specialty norm |

**Rule of thumb.** A complex ensemble that beats the sophisticated baseline by < 3% on the actuary-lens metric and < 5% on the ML-lens metric is not worth the operational overhead. The simpler model is often more defensible.

---

## §2. Why prior-year cost is the toughest baseline for cost models

Prior-year PMPM is a strong predictor of next-year PMPM. Persistence of cost is high:

```
[synthetic] Cost-persistence matrix (CY2023 decile → CY2024 decile):
  Top decile in CY2023 → top decile in CY2024:   ~52%
  Top decile in CY2023 → top 3 deciles in CY2024: ~78%
  Bottom 5 deciles in CY2023 → bottom 5 in CY2024: ~71%
```

A model that uses prior-year cost as its only feature already captures most of the rank-order signal. The marginal value of adding 200 more features is small.

The actuary's test: "Does your model beat prior-year-cost-by-decile on the top-decile captured-cost metric?" If not, the model is not adding value over a SQL query.

---

## §3. The 3-feature linear-regression benchmark

Often, a linear / logistic regression on 3-4 carefully chosen features beats a black-box ensemble. Examples:

| Target | 3-feature benchmark | Common ensemble lift |
|---|---|---|
| Hospitalization (90d) | age + prior-12mo admits + RAF | ~3-5% AUROC improvement |
| Cost (PMPM) | age + sex + RAF | ~10-15% R² improvement |
| Mortality (12mo) | age + Charlson + prior-IP-days | ~5-8% Brier improvement |

A model that does not beat the 3-feature benchmark by a clear margin is not deployable. A model that beats it by a thin margin on a complex pipeline should be reviewed for operational cost vs marginal benefit.

---

## §4. The recency-only baseline (for time-to-event targets)

For onset / progression / mortality models, "most recent claim in the relevant category" is a surprisingly strong baseline:

- Most recent A1c > 7 → diabetes progression
- Most recent eGFR < 60 → CKD progression
- Most recent IP discharge with HF → mortality 12mo

These baselines are not great predictors in absolute terms (AUROC 0.65-0.72), but they set a floor that more complex models must clear.

---

## §5. Industry benchmark ranges (cite-with-caveat)

Industry benchmarks are useful to set expectation ranges, but they should be cited with the caveat that population, target definition, and evaluation methodology vary widely. The agent should not present a benchmark number as a target without surfacing what study produced it.

**Cost prediction.** Published R² ranges for PMPM cost models on Medicare Advantage:
- Demographics + RAF only: ~0.15-0.20 R²
- + claims utilization: ~0.20-0.28 R²
- ML models with 100+ features: ~0.25-0.35 R²

Above 0.40 R² on PMPM cost: highly suspicious; check for leakage (especially L3 RAF circularity).

**Hospitalization (90-day, MA / commercial).**
- Sophisticated baselines: AUROC 0.72-0.78
- ML models with extensive features: AUROC 0.78-0.84
- Above 0.88: highly suspicious; check for leakage (L4 label look-ahead, L8 auth features).

**30-day all-cause readmit.**
- LACE+: AUROC 0.55-0.65 (notoriously hard target)
- ML models: AUROC 0.65-0.72
- Above 0.78: suspicious; check for L4 / L8.

**12-month mortality.**
- Age + Charlson: AUROC 0.72-0.78
- ML models: AUROC 0.80-0.86
- Above 0.92: check for L6 mortality-feed leakage or L7 hospice leakage.

These ranges are guideposts, not targets. A model in the suspicious range is not necessarily wrong, but it requires an explicit leakage audit.

---

## §6. The "two models, same AUROC" problem

If a new model has the same AUROC as the baseline but different calibration, the better-calibrated model wins. If a new model has higher AUROC but worse calibration, it usually does NOT win for a financial use case (it ranks better but predicts worse).

The agent should always require both lenses (see [`evaluation-metrics.md`](evaluation-metrics.md)).

---

## §7. The "ensemble of mediocre models" trap

Stacking, bagging, and complex ensembles often gain 1-3% AUROC over a single well-tuned model. Operational cost:

- More features in production → more failure modes.
- More model artifacts → more version management.
- Less interpretable to actuaries / clinicians.
- Harder to recalibrate at MY boundary.

The agent should flag any "X% better than baseline" claim that exceeds the operational cost. A 0.5% AUROC gain from a 5-model ensemble is rarely worth it.

---

## §8. Baseline-spec YAML (required for any audit)

```yaml
baseline_spec:
  target: ma_hospitalization_90d
  primary_baseline:
    name: logistic_on_age_raf_prior_admits_prior_ed
    features: [age, raf_prior_year, admit_count_prior_12mo, ed_count_prior_12mo]
    auroc_test: 0.745 [synthetic]
    calibration_top_decile_pred_vs_realized: 0.18 vs 0.21 [synthetic]
    captured_admits_top_decile_pct: 38 [synthetic]
  challenger_model:
    name: xgboost_v3
    auroc_test: 0.781 [synthetic]
    calibration_top_decile_pred_vs_realized: 0.22 vs 0.23 [synthetic]
    captured_admits_top_decile_pct: 44 [synthetic]
  delta:
    auroc: +0.036
    calibration_top_decile_abs_error: -0.02
    captured_admits_top_decile_pp: +6
  worth_deployment: yes / no
  reasoning: |
    AUROC gain modest. Calibration meaningfully better. Captured-admits +6pp
    translates to ~280 additional admits identified annually at population scale.
    Operational cost (5x more features, monthly retrain) is justified.
```

---

## §9. Baseline-audit checklist

```yaml
baseline_audit:
  required_baseline_for_target_present:    PASS | FAIL
  three_feature_benchmark_present:         PASS | FAIL
  baseline_evaluated_on_same_test_set:     PASS | FAIL
  challenger_beats_baseline_on_actuary:    PASS | FAIL
  challenger_beats_baseline_on_ml:         PASS | FAIL
  delta_in_suspicious_range_flagged:       PASS | FAIL | N/A
  operational_cost_justified_by_gain:      PASS | FAIL
overall: PASS | FAIL
```

A FAIL on either `challenger_beats_baseline` row is Critical.
