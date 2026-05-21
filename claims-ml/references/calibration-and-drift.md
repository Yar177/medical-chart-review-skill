# Calibration & Drift for Claims-Based ML

A model that passes pre-deployment is not done. Healthcare ML drifts on a predictable cadence: every measurement-year boundary, every code-set update, every policy / regulatory change, every utilization shock. Drift monitoring is not optional. This file is the agent's reference when reviewing a drift / monitoring spec or a recalibration plan.

## §1. The two questions drift monitoring must answer

1. **Are inputs changing?** Feature distributions, prevalence, coding patterns.
2. **Are predictions still right?** Predicted vs realized agreement.

A monitor that only watches inputs (PSI on features) will miss "all my features look normal but the model is now wrong by 30%." A monitor that only watches realized-vs-predicted is too late: the realized signal arrives months after the prediction.

The required pattern: watch both, alert on either.

---

## §2. Population Stability Index (PSI) on features

PSI is the standard input-drift metric.

```
PSI = Σ over bins ((actual_pct - expected_pct) * ln(actual_pct / expected_pct))
```

Thresholds (industry convention):

| PSI | Interpretation | Default action |
|---|---|---|
| < 0.10 | No meaningful shift | No action |
| 0.10 - 0.25 | Modest shift | Investigate; document |
| > 0.25 | Significant shift | Investigate root cause; flag for retrain consideration |

**What to PSI-monitor.**

- Every feature in the production scoring pipeline, monthly.
- Demographic distribution (age band, sex, dual status, geography).
- Outcome prevalence (when realized).
- Subgroup composition.

**What PSI misses.**

- Joint distributions (each feature stable, their interaction shifted).
- Feature *meaning* changes (V28 replaces V24 - prevalence shifts but the change is structural, not population).

---

## §3. Prediction-distribution drift

Watch the model's output distribution monthly:

- Mean predicted probability / value.
- 25th, 50th, 75th, 95th, 99th percentile.
- Volume above the production threshold.

**Acceptable shifts.** < 5% movement in any percentile from the prior month, < 10% from the baseline (frozen at deployment).

**Alarms.**

- Mean prediction shifts > 10% from baseline: a real population change OR a feature-pipeline bug.
- Volume above threshold doubles in a month: feature scaling broke OR a benefit change altered population utilization.

---

## §4. Realized-vs-predicted calibration (the only ground-truth signal)

For every model, define a `realization_window` after `T` when the outcome can be measured. Examples:

| Target | Realization window |
|---|---|
| 90-day hospitalization | T + 90 days + 30 days claim-lag cushion = T + 120 days |
| 30-day readmit | T + 30 days + 60 days claim-lag cushion = T + 90 days |
| CY cost | end of CY + 90 days run-out cushion |
| Mortality | T + horizon + 90 days death-feed lag cushion |

Monthly calibration tracking:

```
For each cohort of predictions made at T:
  wait until T + realization_window
  compute realized outcome
  compute predicted vs realized at population and per-decile
  report delta to baseline calibration from deployment
```

**Alarms.**

- Population-level realized rate diverges from predicted rate by > 10% for two consecutive cohorts.
- Top-decile calibration shifts by > 15% from baseline.
- Subgroup calibration delta exceeds 15% (fairness drift).

---

## §5. The V28 / V24 transition (worked case)

CMS-HCC V28 phase-in (2024: 33%; 2025: 67%; 2026: 100% blended). A risk-adjustment or cost model built on V24 features will see:

- HCC prevalence shifts on every restructured HCC category.
- RAF distribution drift downward (V28 is generally less generous on some categories).
- Apparent calibration breakdown that is actually a coefficient artifact.

**Required response.**

- Re-derive all HCC features under the production-applicable model version.
- Recalibrate the model on data labeled with the production version.
- Do NOT recalibrate on a blend; pick the version that production scoring will use.

Cross-link: defer to the sibling `hcc-nlp` skill for V28 / V24 mapping mechanics.

---

## §6. The COVID utilization shock (worked case)

CY2020 + early CY2021: utilization patterns inverted (deferred care, telehealth surge, ED visit collapse, behavioral health spike). A cost or admit model trained on pre-COVID data and scored in 2020-2021 saw 30-50% calibration breakdown.

**Generalizable lesson.** A drift monitor must distinguish:

- **Slow drift** (changing demographics, gradual coding intensity creep): recalibrate.
- **Shock** (pandemic, policy change, formulary disruption): freeze and reassess; do not auto-recalibrate against a transient regime.

The recalibration playbook should have explicit "shock detected, manual review required" branch.

---

## §7. The MY-boundary forced retrain

At every MY boundary (Jan 1 for CY plans), the model has to be reconsidered, even if no drift has triggered:

- ICD-10-CM annual update (Oct 1 prior year).
- CMS-HCC coefficient update.
- HEDIS spec annual update.
- Fee schedule updates.
- Benefit / formulary changes.
- Open-enrollment population turnover.

**Recommended cadence.** Annual scheduled retrain at MY boundary. Drift triggers in between are exceptions.

---

## §8. Drift-monitoring spec YAML (canonical)

```yaml
drift_monitor_spec:
  model_name: ma_hospitalization_90d_v3
  monitoring_cadence: monthly
  baseline_snapshot:
    date: 2025-01-15
    population_size: 412000
    metrics_frozen: [calibration_plot, decile_lift, subgroup_calibration]

  feature_drift:
    method: PSI
    thresholds:
      warn:    0.10
      action:  0.25
    features_monitored: [all production features]
    subgroup_PSI: [age_band, dual_status, geography]

  prediction_drift:
    metrics: [mean, p25, p50, p75, p95, p99, count_above_threshold]
    warn_delta_from_baseline_pct: 5
    action_delta_from_baseline_pct: 10

  realized_drift:
    realization_window_days: 120
    metrics: [population_calibration, decile_calibration, subgroup_calibration]
    warn_calibration_delta_pct: 10
    action_calibration_delta_pct: 15
    consecutive_cohorts_required_for_action: 2

  scheduled_retrain:
    cadence: annual
    trigger_date: 2026-01-15
    reason: MY-boundary

  alerts:
    on_warn: [ml_team_slack]
    on_action: [ml_team_slack, actuary_review, mlops_oncall]

  freeze_conditions:
    - covid_like_shock_detected: manual review required, no auto-recalibrate
    - code_set_version_change: re-derive features before recalibrate
```

---

## §9. Recalibration vs retrain vs deprecate

When the action threshold is breached, the team has three options.

| Response | When to choose | Mechanics |
|---|---|---|
| **Recalibrate** | Model rank-order is still good; only the probability mapping drifted | Isotonic or Platt scaling on recent data; keep the underlying model |
| **Retrain** | Underlying relationships changed; rank-order has degraded | Retrain on recent data; keep architecture |
| **Deprecate** | The action target itself has changed; model is fundamentally wrong | Retire model; build replacement; notify downstream consumers |

The choice goes into [`templates/recalibration-plan.md`](../templates/recalibration-plan.md).

---

## §10. Calibration-and-drift audit checklist

```yaml
drift_audit:
  feature_PSI_monitor_present:                PASS | FAIL
  prediction_distribution_monitor_present:    PASS | FAIL
  realized_vs_predicted_monitor_present:      PASS | FAIL
  subgroup_calibration_monitor_present:       PASS | FAIL
  thresholds_and_actions_documented:          PASS | FAIL
  baseline_snapshot_frozen:                   PASS | FAIL
  realization_window_correct_for_target:      PASS | FAIL
  scheduled_retrain_cadence_defined:          PASS | FAIL
  shock_handling_branch_defined:              PASS | FAIL
  recalibration_plan_template_present:        PASS | FAIL
overall: PASS | FAIL
```

The third row is the most-frequently-missed. A monitor that watches only inputs and predictions but not realized outcomes is a half-monitor; flag Critical.
