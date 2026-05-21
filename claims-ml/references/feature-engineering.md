# Feature Engineering for Claims-Based ML

Healthcare claims features look simple ("ED visits in last 90 days") and hide claim-lag, code-set, missingness, and stability traps. This file is the agent's reference for reviewing feature construction.

## §1. Rolling windows with claim-lag math

Naive window: `[T - W, T]` for window size W.

Lag-aware window: `[T - W - L, T - L]` where L is the claim-lag cushion. For typical professional + facility claims, `L = 90-120 days` is conservative.

**Example `[synthetic]`.**

```
Naive feature:    ED_VISITS_LAST_90D using service_date in [T - 90d, T].
Lag-aware:        ED_VISITS_90D_BUFFERED using service_date in [T - 180d, T - 90d].
Training look:    similar values (training has full run-out).
Production look:  lag-aware version is stable; naive version is sparse.
```

**Window-size choice.** Bigger window = more signal but slower to react to changes. Smaller window = sensitive to noise.

| Use case | Typical window |
|---|---|
| Short-horizon admit prediction | 90-180 days |
| Annual cost prediction | 12-24 months |
| Long-term risk stratification | 24-36 months |
| Onset detection | minimum 12 months for lookback exclusion |

---

## §2. Comorbidity rollups

Three standard rollup families. Pick one as the primary; the others can be supplementary.

| Family | Source | Typical N features | Good for |
|---|---|---|---|
| Charlson Comorbidity Index | Charlson 1987 / Quan 2005 (claims) | ~17 conditions + 1 score | Mortality, IP cost |
| Elixhauser | Elixhauser 1998 / van Walraven 2009 | ~30 conditions + 1 score | Readmit, hospital outcomes |
| CMS-HCC | CMS-HCC V28 / V24 | ~80-120 HCC categories + RAF | Cost prediction, risk adjustment |

**Trade-offs.**

- HCC categories are coding-policy artifacts; they drift with V24 → V28.
- Charlson / Elixhauser are research-derived and more stable across years.
- Using all three families together creates collinearity; pick a primary and use others only for documented reasons.

**Cross-link.** Defer to the sibling `hcc-nlp` skill for HCC mapping mechanics. Charlson and Elixhauser have well-documented ICD-10 mappings (Quan 2005 for Charlson, AHRQ for Elixhauser).

---

## §3. Episode grouping

For features that summarize a care episode (sepsis bundle, surgical episode, oncology treatment episode, behavioral-health crisis episode), use a published episode grouper:

- ETG (Episode Treatment Group, Optum)
- MEG (Medical Episode Grouper, Truven)
- ECR (Episodes of Care, Symmetry)
- Custom rules-based (acceptable for narrow use cases)

**Pitfall.** Different groupers produce different episode boundaries. A model that uses ETG for training and a different grouper for scoring is broken. Pin the grouper version like a code set.

---

## §4. Care-pattern features

Features that describe how a member uses the system, not just what they have. These are often the strongest non-obvious predictors.

| Feature pattern | Example | Predicts |
|---|---|---|
| PCP visit count + recency | `pcp_visits_12mo` | Engagement; lower-cost trajectory |
| Specialist visit count | `specialist_visits_12mo` | Disease burden; higher cost |
| ED-to-PCP ratio | `ed_visits / max(1, pcp_visits)` in 12mo | Inappropriate utilization; care-management opportunity |
| Polypharmacy count | distinct active drugs in last 90d | Adverse events; admit risk |
| Adherence proxy | PDC (proportion of days covered) by class | Outcome risk |
| Fragmented care indicator | distinct PCPs seen in 12mo | Care coordination gap |
| No-show / cancel rate | claim sequence patterns | Engagement risk |

These features are often more predictive than diagnosis lists for behavior-driven outcomes (admit, ED, adherence-related cost spikes).

---

## §5. Missingness semantics

In claims data, "missing" can mean very different things:

| What's missing | What it actually means |
|---|---|
| No claims in window | Member is healthy AND insured AND not utilizing OR member is dead AND feed has not caught up OR member disenrolled OR data pipeline issue |
| Missing race / ethnicity | Not collected, member declined, or recorded as "Unknown" |
| Missing PCP attribution | Member is new OR attribution table not refreshed |
| Missing lab values | Lab not ordered OR ordered but no result yet OR ordered at out-of-network lab |
| Missing pharmacy data | No prescriptions OR carve-out pharmacy benefit not in feed |

**Rule.** Never let `NULL` mean "zero utilization" without confirming the missingness regime. Build a `data_quality_flag` per member per scoring run.

**Example `[synthetic]`.**

```
Member 99001 [synthetic]
  Eligibility: continuous CY2024
  Claims in CY2024: 0
  Pharmacy in CY2024: 0
  Race: Unknown

Naive feature: HIGH_UTILIZER_FLAG = 0 (no claims, "low utilization")
Reality: this is one of three cases
  (a) healthy + insured + not utilizing
  (b) recently deceased, feed not caught up
  (c) carve-out behavioral health not in our data

Treat as: a separate "no-claim regime" rather than imputed zero.
```

---

## §6. Feature stability over time

A feature whose distribution shifts year-over-year for non-clinical reasons is unstable. Common causes:

- Coding intensity changes (provider education campaigns, audit response).
- Code set updates (ICD-10 annual, HCC version changes).
- Network changes (new ACO assignment, plan-product changes).
- Benefit changes (formulary, copay tier).
- Population mix changes (open enrollment, dual-status transitions).

**Recommendation.** Plot the feature distribution by month for the last 24 months at minimum. Flag features with > 25% month-over-month percentile drift. Either:

- Re-derive in a stable form (e.g., binarize at a stable threshold).
- Remove if instability cannot be explained.
- Document if the instability is the signal you want (e.g., a market-disruption indicator).

---

## §7. Derived features from sibling models

Common pattern: use HCC extractor outputs (from sibling `hcc-nlp`), HEDIS gap-closure flags (from `hedis-nlp`), or NLP-derived features as inputs.

**Risks.**

- Version drift: HCC extractor v3.1 vs v3.2 produces slightly different outputs.
- Calibration: extractor precision / recall directly shapes feature distribution.
- Coverage: if the extractor only runs on a subset of charts, the feature is biased.

**Required.** Pin the producing model's version in the scoring spec. When the upstream model is retrained, the downstream model needs a calibration check.

---

## §8. Member-month vs member-year aggregation

For cost and utilization features, two common units:

| Unit | When to use | Tradeoff |
|---|---|---|
| Member-month | Short-horizon prediction, monthly scoring | Smaller sample size per row; more rows |
| Member-year | Annual cost prediction, MY-bound models | Confounded by partial enrollment |

For member-year features with partial enrollment, normalize to a per-month rate, then optionally annualize. Document the normalization method.

---

## §9. Provider-level rollups

Provider-attributed features (PCP risk score, specialist mix, hospital quality) can be powerful but introduce a new identifier:

- Provider-level features inherit the attribution-staleness problem (see [`target-leakage.md`](target-leakage.md) L5).
- Multi-provider members need an aggregation policy (primary PCP only, weighted by visit count, etc.).
- Provider features may correlate with race / geography in ways that complicate fairness analysis.

---

## §10. Categorical-feature handling

ICD-10 codes, HCC categories, NDC codes, place-of-service codes are all categorical with thousands of levels.

**Recommendations.**

- One-hot encoding is fine for tree models, expensive for linear / NN.
- Target encoding is leaky unless done with cross-validation folds.
- Embeddings work for very-high-cardinality codes (NDC level).
- Roll up to a stable grouping (HCC, ATC class, CCSR) when possible before encoding.

---

## §11. Feature-engineering audit checklist

```yaml
feature_engineering_audit:
  rolling_windows_lag_aware:           PASS | FAIL
  comorbidity_family_pinned:           PASS | FAIL
  episode_grouper_version_pinned:      PASS | FAIL | N/A
  care_pattern_features_present:       PASS | FAIL | N/A
  missingness_regimes_distinguished:   PASS | FAIL
  feature_stability_validated:         PASS | FAIL
  upstream_model_versions_pinned:      PASS | FAIL | N/A
  aggregation_unit_documented:         PASS | FAIL
  high_cardinality_encoding_documented: PASS | FAIL | N/A
overall: PASS | FAIL
```

FAILs on `rolling_windows_lag_aware` or `missingness_regimes_distinguished` are Critical.
