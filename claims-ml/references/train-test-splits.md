# Train / Test Splits for Claims-Based ML

Generic ML splits do not work on claims data. The unit of independence is the **member-year** (or member-episode), not the row. The time axis matters because code sets change, policy changes, and population utilization shifts.

This file is the agent's reference when auditing a split design.

## The non-negotiables

1. **Never random row-level split.** Members appear in many rows; random splits leak across train and test.
2. **Member-year is the default unit.** Each (member, year) tuple is one observation.
3. **Temporal holdout for forward-looking models.** Train on `[T-K, T-1]`, test on `[T]`. Random over time is not acceptable for any model that will run on future data.
4. **MY-boundary discipline.** A measurement year boundary forces a re-evaluation: code sets, policy, fee schedules, network composition all shift.
5. **Code-set version pinned.** Apply the production code-set version (V28, ICD-10-CM 2025, HEDIS MY2025) uniformly across train / test / production.
6. **Document the split function.** A reviewer must be able to reproduce the exact split from a function signature.

---

## Split kinds (when to use which)

| Split | When to use | What it does NOT defend against |
|---|---|---|
| **Random member-level** | Cross-sectional model with no time component (rare in claims) | Temporal drift, code-set transitions |
| **Temporal holdout** | Forward-looking prediction at horizon `H` | Population shift, MY-boundary regime change |
| **Rolling-origin (walk-forward)** | Production-mimicking validation | Computational cost, sample size at each origin |
| **MY-boundary holdout** | Models that will be rebuilt at every MY boundary | Sample size; usually 1 year of test data only |
| **Episode-level** | Episode-of-care predictions (sepsis bundle, surgical episode) | Member-level dependence across episodes |
| **Geo / plan holdout** | Generalization to new geographies / plans | Within-population drift |
| **Stratified by subgroup** | Fairness analysis on a subgroup that is rare | Same as base split |

---

## §1. Member-year split (the default)

**Unit.** `(member_id, measurement_year)` tuple.

**Rule.** A member's records for a given year must not be split across train and test for that year. Either all of `(member, 2024)` is in train or all of it is in test.

**Allowed.** `(member 12345, 2023) -> train` and `(member 12345, 2024) -> test`. The years are independent observations of the same member as long as features for 2024 do not include 2024 outcomes (see [`target-leakage.md`](target-leakage.md) L4).

**Forbidden.** Splitting `(member 12345, 2024)` rows at the claim level between train and test.

**Pseudocode `[synthetic]`.**

```
splits:
  - name: train
    member_years:
      - {member_id_hash: deterministic_hash(member_id) % 10 < 7, year: in [2022, 2023]}
  - name: test
    member_years:
      - {member_id_hash: deterministic_hash(member_id) % 10 >= 7, year: in [2022, 2023]}
unit_of_independence: (member_id, year)
```

---

## §2. Temporal holdout

**Pattern.** Train on `[T_start, T_holdout)`, test on `[T_holdout, T_end]`.

**Worked example `[synthetic]`.**

```
Target: 90-day hospitalization at end of each month T.
Training window:   T in [2022-01-31, 2024-12-31]
Holdout window:    T in [2025-01-31, 2025-12-31]
Feature window:    [T - 12m, T - 4m]   (4-month buffer for claim lag, see L1)
Label window:      [T + 1d, T + 90d]
```

**Common error.** Train on `[T - 12m, T]` and label `[T + 1d, T + 90d]`, then test on randomly sampled `T` values across all years. This is not temporal holdout, it is randomized `T`-stratified sampling, and it cross-contaminates time.

**Stronger pattern: rolling-origin / walk-forward.** Multiple `T_holdout` boundaries, retrain at each, evaluate at the next. Mimics production retrain cadence. Recommended whenever compute allows.

---

## §3. MY-boundary discipline

**Why it matters.** At every measurement-year boundary, healthcare data has a regime shift:

- ICD-10-CM updates (Oct 1 each year)
- CMS-HCC model coefficients (Jan 1)
- HEDIS spec updates (mid-year publication, Jan 1 application)
- Fee schedule updates (Jan 1)
- Plan benefit changes (Jan 1)
- Open-enrollment-driven population changes (Jan 1)

A model trained on `[2022, 2023]` and tested on `2024` crosses one MY boundary. A model trained on `[2022, 2023, 2024]` and tested on `2025` crosses one boundary that includes the V24→V28 transition for MA - a regime shift big enough that test-set calibration will collapse on its own.

**Rule.** Document every MY boundary crossed by the split. For each, declare whether the affected feature (HCC, HEDIS, fee schedule, plan mix) is normalized, re-derived, or accepted as a confound.

---

## §4. The V24 → V28 transition (worked case)

CMS-HCC V28 was phased in for PY2024-PY2026. A model trained on V24-labeled data and scored against V28-labeled data sees:

- ~2,200 fewer ICD-10 codes mapping to any HCC under V28
- Different HCC structure for diabetes, vascular disease, depression
- Different RAF coefficients

**Wrong setup.**

```
Train: CY2021-2023 with V24 HCCs.
Test:  CY2024 with V28 HCCs.
Result: features are not comparable; prevalence shifts on every diabetes/vascular HCC.
        Model degradation looks like drift; it is actually re-coding.
```

**Right setup.**

```
Train: CY2021-2023 with V28 mappings re-applied to historical claims.
Test:  CY2024 with V28 (native).
Result: features comparable; remaining drift is real drift.
```

**Cross-link.** Defer to the sibling `hcc-nlp` skill for V28 / V24 mapping mechanics.

---

## §5. COVID utilization shock (worked case)

CY2020 utilization patterns are unlike any year before or after. Recommendations:

- Exclude CY2020 from training when the model serves a non-pandemic-future.
- Include CY2020 with a year-indicator feature when the model serves long-horizon actuarial work that needs to learn shock patterns.
- Never test on CY2020 unless the model is specifically a pandemic-response model.

A test set that bridges 2019-2021 will show calibration anomalies that are real and unexplainable without context.

---

## §6. Episode-vs-member splits

For episode-of-care predictions (e.g., 30-day post-discharge readmit, sepsis-bundle outcome), the unit of independence becomes the episode. But members can have multiple episodes:

- Same member can appear in 4 separate sepsis episodes.
- Episode-level random split leaks member-level confounders across train and test.

**Recommendation.** Default to member-stratified episode split: all of `member X`'s episodes go to one side. Use episode-level random split only when membership-level features are explicitly excluded from the model.

---

## §7. Geo / plan holdout (generalization tests)

For models intended to deploy in a new market, geography, or plan: split-by-geo or split-by-plan reveals generalization weakness that within-geo cross-validation hides. Common findings:

- Cost models trained on FL Medicaid massively miscalibrate on TX Medicaid (different network composition, different fee schedules, different population mix).
- HEDIS-engine features (gap closure rates) shift by plan-product (HMO vs PPO).

This is supplementary to (not a replacement for) member-year + temporal split.

---

## §8. Stratified splits for fairness analysis

If a subgroup is small (e.g., dual-eligible members under 65), random member-year split may produce a test set with no members in the subgroup. Stratify the split on the subgroup column to guarantee representation. Document the stratification.

See [`fairness-and-equity.md`](fairness-and-equity.md) for subgroup-calibration analysis.

---

## §9. Sample-size sanity

For rare outcomes (e.g., 30-day all-cause readmit at population level ~12%, but for a CHF cohort ~22%; for a behavioral-health cohort ~18%), test sets need enough positives to estimate calibration deciles. Rule of thumb:

| Use case | Minimum positives in test |
|---|---|
| Single AUROC point estimate | 50 |
| AUROC with confidence interval | 200 |
| Calibration plot (10 deciles) | 500 |
| Subgroup calibration (per subgroup) | 200 per subgroup |
| Decile lift at top decile | 100 in top decile |

If the test set does not meet the requirement for the audience's preferred metric, escalate before reporting.

---

## §10. Split-spec YAML (canonical)

The agent should require this YAML for any split it audits.

```yaml
split_spec:
  unit_of_independence: member_year   # or episode, episode_member, geo, plan
  split_method: temporal              # random_member | temporal | rolling_origin | my_boundary | geo | plan
  train_window:
    start: 2022-01-01
    end:   2024-12-31
  test_window:
    start: 2025-01-01
    end:   2025-12-31
  feature_window_relative_to_T: [T-12m, T-4m]
  label_window_relative_to_T:   [T+1d,  T+90d]
  my_boundaries_crossed:
    - 2023-01-01   # ICD-10 update, no major regime
    - 2024-01-01   # V28 phase-in begins for MA
    - 2025-01-01   # V28 phase-in 67%
  code_set_versions:
    icd10:    2025
    cms_hcc:  V28
    hedis:    MY2025
  population_shock_exclusions:
    - 2020-03 to 2021-06   # COVID
  cohort_inclusion_criteria: ...
  stratification: [dual_eligible_flag, age_band, race_ethnicity_imputed]
  random_seed: 42
  reproducibility_script: ./splits/build_splits.py
```

If any field is missing, that itself is a Critical finding.

---

## §11. Split-audit checklist

For any split presented for audit:

```yaml
split_audit:
  unit_correctly_member_year:        PASS | FAIL | N/A
  temporal_holdout_for_forward_pred: PASS | FAIL | N/A
  no_random_row_split:               PASS | FAIL
  my_boundaries_documented:          PASS | FAIL
  code_set_version_uniform:          PASS | FAIL
  cohort_observable_at_T:            PASS | FAIL
  label_does_not_see_post_T:         PASS | FAIL
  test_size_meets_metric_needs:      PASS | FAIL
  stratification_documented:         PASS | FAIL | N/A
  reproducible_from_script:          PASS | FAIL
overall: PASS | FAIL
```

Any FAIL on the first 7 rows is Critical. Failures on the last 3 are High.
