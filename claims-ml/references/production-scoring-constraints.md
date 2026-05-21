# Production Scoring Constraints

A model that performs in validation can still fail in production for a single reason: a feature that was available at training time is not available at scoring time. This file is the agent's reference for the production-fitness audit.

## §1. The scoring-time feature-availability problem

At training, you query the warehouse and get back whatever exists. At scoring, you have a fixed time budget and a fixed feature pipeline that has to compute every feature from sources that themselves have refresh cadences.

**Example `[synthetic]`.**

```
Feature: PRIOR_HOSPICE_ELECTION_FLAG
  Source: CMS hospice election claims, monthly DUA delivery.
  Latency: 30-60 days after election.

  At training, you have 18 months of data and full election history.
  At daily scoring on 2026-01-15:
    elections from Dec 2025: ~40% in warehouse
    elections from Nov 2025: ~80% in warehouse
    elections from Oct 2025: ~95% in warehouse

  A model that scores daily and uses this feature is under-flagging recent hospice electors
  every day for 60 days after their election.
```

The mitigation is not "make the feed faster." The mitigation is to declare the latency at training time and use only data that will be available at scoring time.

---

## §2. The scoring-time feature spec (required artifact)

Every model going to production needs a scoring-time feature spec. Format:

```yaml
scoring_feature_spec:
  model_name: ma_hospitalization_90d_v3
  scoring_cadence: monthly                # daily | weekly | monthly | quarterly
  scoring_run_time_minutes_target: 30     # for whole population
  prediction_volume: ~410000 members
  features:
    - name: AGE_AT_T
      source: eligibility_table
      refresh_cadence: daily
      latency_days: 0
      scoring_availability: always
      compute_cost: trivial
    - name: ED_VISIT_COUNT_6MO_TO_4MO
      source: facility_claims
      refresh_cadence: nightly batch
      latency_days: 90                    # using claims received 90+ days after DoS
      scoring_availability: always_with_4mo_buffer
      compute_cost: aggregate over ~70M rows
    - name: PRIOR_YEAR_RAF
      source: derived_raf_table
      refresh_cadence: annual at MY boundary + quarterly refresh
      latency_days: 0 (within MY)
      scoring_availability: always_post_MY_boundary
      compute_cost: lookup
    - name: HOSPICE_ELECTION_PRIOR_60D
      source: CMS hospice claims
      refresh_cadence: monthly DUA
      latency_days: 60
      scoring_availability: stale_by_design
      compute_cost: lookup
      note: |
        Feature window deliberately set to [T-150d, T-60d] to avoid
        claim-lag undercount. Documented as L1 mitigation.
```

Every feature line that says `scoring_availability: never` or `scoring_availability: only_in_training` is a Critical finding.

---

## §3. Latency budget by source (typical, used as default if unspecified)

| Source | Typical warehouse latency | Notes |
|---|---|---|
| Eligibility / membership | Daily | Refresh nightly in most warehouses |
| Pharmacy claims | 1-3 days | Real-time adjudication; near-current |
| Professional claims | 30-90 days | Lag distribution: see [`target-leakage.md`](target-leakage.md) L1 |
| Facility / IP claims | 60-120 days | Slower than professional |
| Lab claims | 14-30 days | Variable; depends on lab vendor |
| Lab results (HEDIS supplemental) | 7-90 days | Depends on supplemental data agreements |
| Hospice election (Medicare) | 30-60 days | Monthly DUA |
| Death (SSA DMF) | 30-90 days | Monthly DUA |
| Provider attribution | 30-90 days | Often retroactive; see L5 |
| HCC features (derived) | Quarterly during MY, then frozen | Bound to MY |
| HEDIS engine outputs | Annual at minimum, often quarterly | Spec-bound |

When the team specifies a different latency, use theirs. When they do not specify, the agent uses these defaults and flags the assumption.

---

## §4. Scoring cadence and feature freshness

| Scoring cadence | Acceptable latency for feature | Notes |
|---|---|---|
| Daily | ≤ 7 days (or feature window pushed back enough) | Most features will need a `[T-180d, T-90d]`-style window |
| Weekly | ≤ 30 days | Most features OK with 60-day push-back |
| Monthly | ≤ 60 days | Default for risk-stratification / cost models |
| Quarterly | ≤ 90 days | Most permissive |
| Annual (PY-bound) | All features available at MY boundary | RAF, HEDIS engine outputs |

The scoring cadence is a hard constraint set by the downstream action, not by the ML team. A care-management program that needs members enrolled within 7 days of risk identification cannot use a monthly-scored model.

---

## §5. Compute cost and population size

Per-member features have different scoring costs:

| Feature complexity | Compute time per member (rough) |
|---|---|
| Lookup from eligibility | < 1 ms |
| Aggregation over recent claims (≤ 1k rows) | 1-10 ms |
| Aggregation over historical claims (10k+ rows) | 10-100 ms |
| Cross-source join (member + provider + claims) | 50-500 ms |
| Derived feature requiring re-extraction (HCC, episode grouper) | 1-10 s |
| Free-text NLP feature (notes, claims narrative) | 1-30 s |

For a 500k-member monthly scoring run, a 100 ms / member feature is 14 hours. A 1 s / member NLP feature is 6 days. Either find a precomputed pipeline or accept the cadence implication.

---

## §6. Real-time scoring constraints

If the model has to score in real time (member-portal call, provider-side decision support):

- Single-member latency budget typically < 500 ms end-to-end.
- Pre-computed feature store recommended (Redis, materialized views).
- No on-demand cross-source aggregation in the request path.
- Feature staleness becomes a per-feature contract, not a batch property.

Most claims-ML use cases do not need real-time. Daily or monthly batch is the default. Real-time should be justified by the action, not the technology preference.

---

## §7. Feature dependency on other models

Feature-of-a-feature dependencies are common and dangerous.

```
Model A: predicts cost.
  Feature: predicted_admit_probability from Model B.
Model B: predicts hospitalization.
  Feature: predicted_cost from Model A.
```

Circular dependencies break scoring. Even non-circular dependencies create version-compatibility risk: Model B is retrained with new architecture; Model A's predictions drift.

**Rule.** Document every model-as-feature dependency in the scoring spec. Each dependent feature carries the producing model's version and last-trained date. Recalibrating Model B triggers a Model A recalibration check.

---

## §8. The volume-and-capacity audit

Every model that drives a downstream action has a capacity constraint:

```
Care management program:
  Capacity: 300 new enrollments / month
  Model output above threshold: 1,200 members / month
  Resolution: pick the top 300 by score, OR raise the threshold
```

If the predicted volume at the production threshold exceeds program capacity by > 3x, the threshold is wrong and the model card must say so. If the volume is < 30% of capacity, the threshold is too high and members who would benefit are excluded.

---

## §9. Scoring-fitness audit checklist

```yaml
scoring_audit:
  scoring_feature_spec_complete:           PASS | FAIL
  every_feature_has_latency_documented:    PASS | FAIL
  no_feature_unavailable_at_scoring:       PASS | FAIL
  scoring_cadence_matches_action:          PASS | FAIL
  compute_cost_fits_runtime_budget:        PASS | FAIL
  model_dependencies_documented:           PASS | FAIL | N/A
  threshold_volume_matches_capacity:       PASS | FAIL
  feature_window_accommodates_lag:         PASS | FAIL
  scoring_environment_matches_training:    PASS | FAIL
overall: PASS | FAIL
```

A FAIL on `no_feature_unavailable_at_scoring` is always Critical.
