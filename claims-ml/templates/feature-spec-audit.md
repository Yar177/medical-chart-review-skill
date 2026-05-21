# Feature Spec Audit

> Use this template when the user provides a feature spec, feature list, or feature pipeline for review.

The primary deliverable. Produces a per-feature audit table plus summary findings.

---

## Header

```yaml
audit_metadata:
  model_name: <name>
  target: <cost | hospitalization | readmit | ED | onset | mortality | eligibility | anomaly>
  prediction_horizon: <days / months>
  scoring_cadence: <daily | weekly | monthly | quarterly | annual>
  population: <MA | ACA | Medicaid | commercial; subgroup if any>
  reviewer: claims-ml skill
  review_date: <date>
  references_consulted: [target-leakage, train-test-splits, production-scoring-constraints, feature-engineering]
```

## §1. Per-feature audit table

For each feature in the spec:

| # | Feature name | Source | Refresh latency (d) | Scoring availability | Leakage classes flagged | Severity | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | `AGE_AT_T` | eligibility | 0 | always | none | OK | none |
| 2 | `ED_VISIT_COUNT_LAST_90D` | facility claims | 90 | only with buffer | L1 | High | Shift window to [T-180d, T-90d] |
| 3 | `PRIOR_YEAR_RAF` | derived RAF | within MY | post-MY only | L3 if target overlaps RAF window | Medium | Confirm RAF window does not overlap target window |
| 4 | `HOSPICE_FLAG_LAST_60D` | CMS DUA | 60 | stale by design | L7 | Medium | Document; window already accounts for lag |
| 5 | `PCP_NPI` | attribution_v3 | 90 retroactive | freeze at T-90d | L5 | Medium | Use point-in-time attribution snapshot |
| ... | ... | ... | ... | ... | ... | ... | ... |

Severity legend: **Critical** (blocks deployment), **High** (blocks production promotion), **Medium** (track and fix in next iteration), **Low** (note for future).

## §2. Leakage class coverage summary

| Class | Reference | Features affected | Critical | High | Medium |
|---|---|---|---|---|---|
| L1 claim-lag | [`references/target-leakage.md`](../references/target-leakage.md) §L1 | N | n | n | n |
| L2 lab-result-date | §L2 | N | n | n | n |
| L3 RAF circularity | §L3 | N | n | n | n |
| L4 look-ahead label | §L4 | N | n | n | n |
| L5 retroactive attribution | §L5 | N | n | n | n |
| L6 mortality-feed lag | §L6 | N | n | n | n |
| L7 hospice-election lag | §L7 | N | n | n | n |
| L8 auth / referral | §L8 | N | n | n | n |
| L9 cohort selection | §L9 | N | n | n | n |
| L10 code-set leakage | §L10 | N | n | n | n |

## §3. Split design summary

Reproduce the split-spec YAML from [`references/train-test-splits.md`](../references/train-test-splits.md) §10 or flag missing fields.

```yaml
split_spec_supplied: yes | no | partial
findings:
  - unit_of_independence: PASS | FAIL  (notes)
  - temporal_holdout:     PASS | FAIL
  - my_boundary_documented: PASS | FAIL
  - code_set_pinned:        PASS | FAIL
  - cohort_observable_at_T: PASS | FAIL
overall: PASS | FAIL
```

## §4. Production-fitness summary

```yaml
production_audit:
  scoring_feature_spec_complete:   PASS | FAIL
  every_feature_has_latency:       PASS | FAIL
  scoring_cadence_matches_action:  PASS | FAIL
  compute_cost_fits_budget:        PASS | FAIL
  upstream_model_deps_pinned:      PASS | FAIL | N/A
critical_blockers: [list features with scoring_availability = never or only_in_training]
```

## §5. Findings summary

Group findings by severity. Cite the reference section for each.

### Critical (n)

1. **Feature `X`** - [L4 label look-ahead](../references/target-leakage.md#l4-look-ahead-in-label). Feature window includes data realized after `T`. Block deployment until fixed.
2. ...

### High (n)

1. **Feature `Y`** - [L1 claim-lag](../references/target-leakage.md#l1-claim-lag-leakage-the-most-common). Production-scoring availability ≠ training availability. Recommend window shift.
2. ...

### Medium (n)

1. ...

### Low (n)

1. ...

## §6. Required follow-ups before re-audit

- [ ] Address all Critical findings.
- [ ] Provide updated feature spec.
- [ ] Provide split-spec YAML if missing.
- [ ] Provide scoring-time feature spec if missing.

## §7. Deferrals

- Any clinical-validity questions on feature selection → defer to medical director.
- Any actuarial-validity questions on financial impact → defer to credentialed actuary.
- Any HCC mapping / V28 questions → defer to sibling `hcc-nlp` skill.
- Any HEDIS-measure mechanics → defer to sibling `hedis-nlp` skill.
- Any PHI handling / de-identification questions → defer to sibling `hipaa-compliance` skill.
