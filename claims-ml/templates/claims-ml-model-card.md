# Claims ML Model Card

> Healthcare-tuned model card. Use for any claims-ML model going to production. The YAML block at the bottom is authoritative on conflict with the narrative.

A peer of [`hcc-nlp/templates/hcc-model-card.md`](../../hcc-nlp/templates/hcc-model-card.md) and [`hedis-nlp/templates/per-measure-model-card.md`](../../hedis-nlp/templates/per-measure-model-card.md), focused on supervised ML on claims data rather than on extractor pipelines.

---

## 1. Model identity

- **Model name:** `<name>`
- **Version:** `<semver>`
- **Trained on:** `<date>`
- **Owner:** `<team / individual>`
- **Code-set versions pinned:**
  - ICD-10-CM: `<version>`
  - CMS-HCC: `<V24 | V28>`
  - HEDIS (if used): `<MYYYYY>`
  - Episode grouper (if used): `<name + version>`

## 2. Intended use

- **Target:** `<cost | hospitalization | readmit | ED | onset | mortality | eligibility | anomaly>`
- **Prediction horizon:** `<days / months>`
- **Population:** `<MA | ACA | Medicaid | commercial; subgroup>`
- **Action driven:** `<care management enrollment | financial planning | outreach prioritization | etc.>`
- **Scoring cadence:** `<daily | weekly | monthly | quarterly | annual>`
- **Production threshold (if classification):** `<probability cutoff>`

## 3. Contraindications (out-of-scope uses)

- Not for: `<list>`
- Not validated for: `<subgroups / populations excluded from training>`
- Not for use in: `<settings where the action would be inappropriate>`

Explicit non-uses (defaults that should be in every claims-ML card unless deliberately overridden):

- Direct clinical decision-making for individual patients.
- Coverage / eligibility / pricing decisions without compliance counsel review.
- Real-time scoring (if model is batch-trained).
- Populations outside the training cohort.

## 4. Training cohort

- **Cohort definition:** `<inclusion / exclusion criteria>`
- **Cohort size:** `<N members; N member-years>`
- **Cohort date range:** `<start> to <end>`
- **Demographics:**

| Dimension | Distribution |
|---|---|
| Age band | 18-44: x%; 45-64: y%; 65-74: z%; 75-84: a%; 85+: b% |
| Sex | F: x%; M: y%; X/Unknown: z% |
| Dual-eligibility | yes: x%; no: y% |
| Race / ethnicity (self-reported or imputed via BISG) | <distribution> |
| Geography | <CBSA mix or state mix> |

## 5. Target definition

Reproduce the target-spec YAML from [`references/target-definitions.md`](../references/target-definitions.md#9-target-spec-yaml-canonical).

```yaml
target_spec:
  ...
```

## 6. Split design

Reproduce the split-spec YAML from [`references/train-test-splits.md`](../references/train-test-splits.md#10-split-spec-yaml-canonical).

```yaml
split_spec:
  ...
```

## 7. Features

- **Feature count:** `<n>`
- **Top features by importance:** `<list top 10 with brief description>`
- **Feature families:** `<demographics, claims utilization, comorbidities, care patterns, derived risk scores>`
- **Scoring-time feature spec:** Reproduce or link to scoring spec YAML from [`references/production-scoring-constraints.md`](../references/production-scoring-constraints.md#2-the-scoring-time-feature-availability-required-artifact).
- **Leakage audit results:** Summary from [`templates/feature-spec-audit.md`](feature-spec-audit.md). All Critical findings resolved; remaining High and Medium documented.

## 8. Baseline

Reproduce the baseline-spec YAML from [`references/baselines-and-benchmarks.md`](../references/baselines-and-benchmarks.md#8-baseline-spec-yaml-required-for-any-audit).

```yaml
baseline_spec:
  ...
```

## 9. Evaluation

Both lenses required. See [`references/evaluation-metrics.md`](../references/evaluation-metrics.md).

### Actuary lens

| Metric | Value | CI |
|---|---|---|
| Decile lift @ top decile | x | (a, b) |
| Lorenz / Gini | x | (a, b) |
| Captured-target-in-top-10% | x | (a, b) |
| MAPE on positives (cost models) | x | (a, b) |
| Total predicted vs realized | x vs y | |

### ML lens

| Metric | Value | CI |
|---|---|---|
| AUROC | x | (a, b) |
| AUPRC | x | (a, b) |
| Brier score | x | (a, b) |
| Log loss | x | (a, b) |
| Calibration (population, top decile) | predicted x vs realized y | |

### Calibration

- **Population calibration plot:** Required. Embed or link.
- **Subgroup calibration plots:** Required for at minimum age band, sex, dual-eligibility, race / ethnicity. Embed or link.

### Threshold-based metrics (classification only)

| Metric @ production threshold | Value |
|---|---|
| Threshold | <p> |
| Confusion matrix | TP / FP / FN / TN |
| Precision / Recall | <p> / <r> |
| Predicted volume above threshold per scoring run | <n> |
| Program capacity match | yes / no (notes) |

## 10. Fairness assessment

Reproduce the fairness-spec YAML and audit checklist from [`references/fairness-and-equity.md`](../references/fairness-and-equity.md).

```yaml
fairness_spec:
  ...
fairness_audit:
  ...
```

Subgroup performance summary:

| Subgroup | N test | AUROC (CI) | Calibration delta vs population | Selection rate | Recall |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

**Disparities flagged:** `<list, with severity>`.

**Mitigation applied:** `<technique + rationale, or "none">`.

**Legal review status:** `<complete | pending | not-required-with-justification>`.

## 11. Production scoring

- **Scoring-time feature spec:** Complete and audited. See §7 link.
- **Scoring cadence:** `<>`
- **Scoring environment:** `<>` (matches training environment? yes / no)
- **Upstream model dependencies pinned:** `<list with versions>`

## 12. Drift monitoring and recalibration

Reproduce the drift-monitor-spec YAML from [`references/calibration-and-drift.md`](../references/calibration-and-drift.md#8-drift-monitoring-spec-yaml-canonical).

```yaml
drift_monitor_spec:
  ...
```

Recalibration plan: see [`templates/recalibration-plan.md`](recalibration-plan.md) for the playbook to apply when thresholds breach.

## 13. Known limitations

- `<>` (e.g., calibrated for MA only; behavior on Medicaid not validated)
- `<>` (e.g., assumes V28 code set; V24 production scoring requires retrain)
- `<>` (e.g., death-feed lag of 60 days; mortality predictions in the most recent 60 days are systematically low)

## 14. Approval sign-offs

| Role | Name | Date | Sign-off |
|---|---|---|---|
| ML team lead | | | |
| Actuary (credentialed) | | | |
| Medical director | | | |
| Compliance | | | |
| MLOps / production owner | | | |

## 15. Change log

| Version | Date | Change | Approver |
|---|---|---|---|
| `<>` | `<>` | `<>` | `<>` |

---

## Canonical YAML block (authoritative on conflict)

```yaml
model_card:
  name: <name>
  version: <semver>
  trained_on: <date>
  target: <target>
  population: <population>
  code_set_versions:
    icd10: <v>
    cms_hcc: <v>
    hedis: <v>
    episode_grouper: <name+v>
  baselines_beaten:
    actuary_lens: yes | no (notes)
    ml_lens: yes | no (notes)
  leakage_audit_passed: yes | no (notes)
  calibration_passed: yes | no (notes)
  subgroup_calibration_passed: yes | no (notes)
  fairness_review_passed: yes | no | deferred-to-counsel
  scoring_feature_spec_audited: yes | no
  drift_monitor_in_place: yes | no
  recalibration_plan_in_place: yes | no
  approvals:
    ml_lead: signed | pending
    actuary: signed | pending
    medical_director: signed | pending | n/a
    compliance: signed | pending | n/a
    mlops: signed | pending
  ready_for_production: yes | no
```
