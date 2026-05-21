# Recalibration Plan

> Use this template when a drift-monitor threshold has been breached. Forces an explicit decision: recalibrate, retrain, or deprecate.

---

## Header

```yaml
plan_metadata:
  model_name: <name>
  version_in_production: <semver>
  trigger_date: <date>
  trigger_alert: <feature_PSI | prediction_drift | realized_calibration | subgroup_calibration | scheduled_MY_boundary | shock_detected>
  owner: <name>
  reviewer: claims-ml skill
```

## §1. Trigger summary

Describe what tripped the alert. Quote the monitor output.

```yaml
trigger:
  monitor:    <feature_PSI | prediction_drift | realized | subgroup | scheduled | shock>
  metric:     <PSI value, calibration delta, etc.>
  threshold:  <warn | action>
  duration:   <single cohort | n consecutive cohorts>
  scope:      <population-wide | subgroup-specific | feature-specific>
  details: |
    <quote the monitor output: which features / subgroups / cohorts breached, by how much>
```

## §2. Root-cause analysis

Distinguish four root causes. Pick one (or document if mixed).

| Root cause | Signals | Implication |
|---|---|---|
| **Slow population drift** | PSI 0.10-0.25 across many features; gradual prediction shift | Recalibrate or retrain on recent data |
| **Code-set / regime change** | Sharp prediction shift around MY boundary; PSI jumps on derived features | Re-derive features in production code set; retrain |
| **Pipeline / data-quality issue** | Sudden prediction shift; PSI spikes on a single feature | Fix pipeline; do not retrain until fixed |
| **Shock / external event** | Population-wide utilization shift in a short window (pandemic, policy change, network disruption) | Freeze; do not auto-retrain |

```yaml
root_cause:
  category:   <slow_drift | code_set_change | pipeline_issue | shock>
  evidence:   |
    <what you observed that points to this cause>
  ruled_out:  |
    <other causes considered and why they were ruled out>
```

## §3. Decision

Choose ONE of three responses.

### Option A: Recalibrate

When: model rank-order still good (AUROC stable), but predicted probabilities / values drifted from realized.

```yaml
decision: recalibrate
method: <isotonic | Platt | quantile_mapping>
recalibration_data:
  window: <date range>
  size: <N members / cohorts>
artifacts_changed: [calibration_layer]
artifacts_unchanged: [feature_pipeline, model_weights]
expected_outcome: predicted vs realized within 5% across deciles
re-evaluation_required: yes; full evaluation suite on next held-out cohort
sign_offs_required: [ml_lead, actuary]
```

### Option B: Retrain

When: underlying relationships changed; rank-order degraded; new code-set / new population.

```yaml
decision: retrain
training_data:
  window: <date range; usually last 24-36 months>
  size: <N member-years>
features:
  changed: [list any features added / removed / redefined]
  unchanged: [list]
split_design:
  match_previous: yes | no (notes)
code_set_version: <V28 | V24 | latest>
expected_outcome:
  auroc_delta_from_prior: <expected range>
  calibration_delta_from_prior: <expected range>
re-evaluation_required: full evaluation suite + leakage re-audit + subgroup analysis
sign_offs_required: [ml_lead, actuary, medical_director, compliance]
deployment_window: <date range>
rollback_plan: keep prior version warm for N days; auto-rollback on production calibration delta > X
```

### Option C: Deprecate

When: target itself has changed (action is no longer relevant); data source has been retired; structural change makes the model fundamentally wrong.

```yaml
decision: deprecate
reason: |
  <full explanation>
downstream_consumers_notified: [list teams / systems]
replacement_plan:
  build_new_model: yes | no
  new_target: <if different>
  timeline: <date range>
transition_plan: |
  <how downstream consumers operate during the gap>
sunset_date: <date>
sign_offs_required: [ml_lead, actuary, medical_director, compliance, downstream_consumer_owners]
```

## §4. Risk assessment

For the chosen option, document:

```yaml
risk_assessment:
  population_at_risk_during_response: <N members affected by stale / wrong predictions during the response window>
  intervention_continuity_plan: |
    <do downstream programs keep enrolling members from the old scores? freeze and wait? manual review?>
  data_quality_safeguards: |
    <pipeline checks added to prevent recurrence>
  monitoring_changes: |
    <new monitors added or thresholds adjusted post-response>
```

## §5. Validation plan post-response

```yaml
validation_post_response:
  metrics_to_compare: [actuary lens + ML lens + calibration + subgroup calibration]
  cohorts_to_evaluate: <next n cohorts post-recalibrate/retrain>
  pass_criteria:
    population_calibration_delta_pct:   < 10
    top_decile_calibration_delta_pct:   < 15
    subgroup_calibration_delta_pct:     < 15
    auroc_no_regression_within:         0.01
  fail_action: |
    <what happens if validation fails: rollback, repeat response, escalate>
```

## §6. Communication plan

Who needs to know what, and when.

- [ ] ML team: notified of trigger; notified of decision; notified of post-response result.
- [ ] Downstream consumers (care management, actuary, financial planning): notified of decision; notified of any prediction-volume shifts.
- [ ] Compliance / legal: notified if subgroup calibration was the trigger or if fairness implications are present.
- [ ] Members / providers: notified only if response materially changes who gets actioned (usually no, but document the call).

## §7. Sign-offs

| Role | Name | Date | Sign-off |
|---|---|---|---|
| ML team lead | | | |
| Actuary (credentialed) | | | |
| Medical director | | | |
| Compliance | | | |
| MLOps / production owner | | | |
| Downstream consumer owner | | | |

## §8. Outcome (filled after response)

```yaml
outcome:
  response_completed: <date>
  validation_pass: yes | no (notes)
  rolled_back: yes | no (reason)
  follow_up_actions: [list]
  lessons_learned: |
    <documented for next cycle>
```
