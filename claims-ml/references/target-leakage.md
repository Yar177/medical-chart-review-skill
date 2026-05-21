# Target Leakage in Claims-Based ML

> *"Your AUROC is 0.92 in validation and 0.61 in production."* Almost always leakage. Almost always claim lag.

This file catalogs the leakage modes that are specific to healthcare claims data. Generic ML reviews catch row-level leakage (e.g., duplicate IDs across split). They miss everything below.

For every finding the agent surfaces, cite the leakage class from this file.

## Classes of leakage (taxonomy)

| Class | One-line definition | Example feature / setup |
|---|---|---|
| **L1. Claim-lag leakage** | Training data reflects months of run-out that production data does not | Counts of services from `[T-3m, T]` for predictions at time `T` |
| **L2. Lab / result-date leakage** | Collection date in window, result date out of window | "Most recent A1c value as of T" using result date |
| **L3. RAF / risk-score circularity** | Using a derived risk score as a feature for a target the score itself helps explain | Prior-year RAF as feature for prior-year-period cost |
| **L4. Look-ahead in label** | Label uses information observable only at or after outcome time, but feature window does not | Discharge disposition for a model run at admission |
| **L5. Retroactive attribution** | Member-to-program assignment that gets backfilled after the fact | "PCP attribution as of T" using attribution table refreshed at T+90d |
| **L6. Mortality-feed lag** | Death date arrives weeks to months late; absence != alive | Treating no-claims period as healthy, when member is deceased |
| **L7. Hospice-election lag** | Hospice / palliative-care election flag arrives delayed | Cost prediction that misses hospice-electing members |
| **L8. Authorization / referral leakage** | Pre-auth or referral status reflects intent of a future event | Inpatient pre-auth as a feature in a 30-day admit predictor |
| **L9. Cohort-selection leakage** | The cohort eligibility criterion itself depends on the outcome | "Adults with 12 months continuous enrollment in the prediction window" |
| **L10. Code-set leakage** | ICD-10 / HCC codes valid only in the test period, not the train period | Using V28 HCCs in train data that was extracted before V28 was released |

---

## L1. Claim-lag leakage (the most common)

**Mechanism.** Claims arrive at the data warehouse on a lag. Typical lag distribution (commercial / MA, professional + facility combined):

| Days after DoS | Cumulative % of claims received |
|---|---|
| 30 days | ~55-70% |
| 60 days | ~75-85% |
| 90 days | ~85-92% |
| 180 days | ~95-98% |
| 365 days | ~99%+ |

Training data extracted in March 2026 against a prediction date of `T = 2025-11-01` sees ~90%+ of claims from Aug-Oct 2025. Production scoring on `2026-01-01` against `T = 2025-11-01` sees ~70%.

**Example `[synthetic]`.**

```
Feature: ED_VISIT_COUNT_LAST_90D
  Training extraction date: 2026-03-15
  Production scoring date:  2026-01-01
  Prediction date T:        each scored month-end

  In training, feature for Nov-2025 has ~92% run-out.
  In production, feature for Nov-2025 has ~70% run-out.

  Validation AUROC: 0.84
  Production AUROC: 0.66
```

**Fix.** Train against the data-as-of state that production will see. Either:
- Build training snapshots that mimic the lag (extract `[T-Xd, T]` claims using `received_date <= T + scoring_lag_days`, not `service_date <= T`), or
- Push the feature window further back (`[T-7m, T-4m]` instead of `[T-3m, T]`) so run-out is stable in both train and production.

**Cross-link.** See [`production-scoring-constraints.md`](production-scoring-constraints.md) for the scoring-time feature-availability YAML.

---

## L2. Lab-result-date leakage

**Mechanism.** Lab claims carry two dates: collection date (DoS) and result date (when the result becomes available in the warehouse). A "most recent A1c as of T" feature that filters on collection date can use results that did not exist as of T.

**Example `[synthetic]`.**

```
Member 12345 [synthetic]
  A1c collected 2025-10-28, resulted 2025-11-05
  Prediction date T = 2025-11-01

  Filter on collection_date <= T: feature includes the A1c = 9.1 result.
  Reality at T = 2025-11-01:       result not in warehouse yet.

  Training data: feature populated.
  Production:    feature null.
```

**Fix.** Filter lab features on `result_date <= T - lab_lag_days`, never on `collection_date <= T`. Apply a conservative lag of 14 days for routine labs, 7 days for inpatient labs.

---

## L3. RAF / risk-score circularity

**Mechanism.** RAF (Risk Adjustment Factor) and similar risk scores are derived from diagnoses and demographics over a measurement period. Using `RAF_2025` as a feature to predict `COST_2025` is circular: RAF is partly built from cost-correlated diagnosis intensity in the same window.

**Worked example `[synthetic]`.**

```
Model: predict CY2025 PMPM cost.
Feature: RAF_2025 (computed from CY2024 diagnoses for PY2025).

Apparent R^2: 0.42
True signal:  RAF_2025 includes diagnosis intensity that itself correlates with
              CY2025 utilization patterns (sicker members get more dx and more cost).

The model is partly memorizing the RAF formula, not learning a new signal.
```

**Fix options.**
- Predict `next-year cost` and use `RAF_prior-year` as a feature (legal; RAF is fully realized before the prediction window).
- Predict `current-year cost` and use `RAF_2-years-back` as a feature.
- Decompose RAF into its component HCC features and audit each for leakage individually.

**Pitfall.** Concurrent RAF (`RAF_2025` for `CY2025` cost) is leaky even though it is technically computed from prior-period diagnoses, because the diagnosis intensity used to build it correlates with the same care patterns driving the cost target.

---

## L4. Look-ahead in label

**Mechanism.** The label uses information available only at outcome time, but features stop earlier.

**Examples `[synthetic]`.**

| Model | Bad label | Why |
|---|---|---|
| Predict 30-day readmit at admission | Includes discharge disposition (SNF, hospice, expired) in label logic | Discharge disposition is unknown at admission |
| Predict ED visit in next 90 days | Includes "ED visit was avoidable" classification | Avoidability is reviewer-judged after the visit |
| Predict mortality in next year | Includes hospice election in window | Hospice election is a near-perfect mortality predictor and arrives after the prediction date |

**Fix.** Label-generation logic must run only on facts that will be observable at the outcome assessment time, not at any earlier moment. Document the label-generation function with a `feature_freeze_date` parameter; the label must not depend on any field with a `realized_date > feature_freeze_date`.

---

## L5. Retroactive attribution

**Mechanism.** PCP-to-member attribution, ACO assignment, care-management program enrollment - all of these get reassigned retroactively. The attribution table you queried in March 2026 for `T = 2025-11-01` is not the table that existed on `2025-11-01`.

**Example `[synthetic]`.**

```
Feature: PCP_NPI as of T = 2025-11-01
Source:  attribution_v3 table, last refreshed 2026-02-15.

Member 67890 [synthetic]:
  attribution_v3 at 2026-02-15: PCP = Dr. A (effective 2025-07-01)
  attribution_v1 at 2025-11-01: PCP = Dr. B (effective 2025-03-01)

In training, you get Dr. A.
In production scoring on 2025-11-01, you would have gotten Dr. B.
```

**Fix.** Use point-in-time attribution tables (`attribution AS OF <date>`) if the warehouse supports them. If not, freeze attribution at `T - 90d` and document the staleness.

---

## L6. Mortality-feed lag

**Mechanism.** SSA Death Master File arrives monthly with 30-90 day lag. State vital records vary. Claim absence is interpreted as "healthy member with no utilization" when in reality the member is deceased and the feed has not caught up.

**Example `[synthetic]`.**

```
Member 11223 [synthetic] died 2025-10-15.
SSA DMF update received 2026-01-10.

Snapshot extracted 2025-12-01 for prediction date T = 2025-11-30:
  member appears in "no admits, no ED, no PCP" cohort
  cost prediction = $48 / month (low-utilizer pattern)

Reality: member was already deceased.
```

**Fix.** Apply a death-feed-lag cushion: censor any "no recent claims" inference where last claim is > 90 days ago. Cross-reference state vital records where licensed.

---

## L7. Hospice-election lag

**Mechanism.** Hospice election flag arrives via Medicare claims with 30-60 day lag. Hospice-electing members have a very different cost / utilization profile than the population at large.

**Fix.** Same pattern as L6: apply a hospice-lag cushion of 60 days; flag `hospice_status = UNKNOWN_RECENT` for members whose last claim is recent enough that election could exist but not yet posted.

---

## L8. Authorization / referral leakage

**Mechanism.** Pre-authorizations and referrals are predictive because the event they authorize is already planned. Using "elective IP pre-auth in window" as a feature to predict "IP admit in next 30 days" is near-perfect for elective admits and near-zero for unplanned admits.

**Fix.** Decide whether the model should predict planned-and-unplanned admits combined or only unplanned. If only unplanned, drop pre-auth features. If combined, expect a degenerate model that does well on planned admits and badly on the population that matters for ED-to-IP avoidance.

---

## L9. Cohort-selection leakage

**Mechanism.** "Members with 12 months continuous enrollment in the prediction window" is a common cohort filter. It is leaky for any model that predicts disenrollment, mortality, or program-eligibility loss, because the cohort definition itself excludes the outcome you are trying to predict.

**Example `[synthetic]`.**

```
Model: predict 12-month mortality.
Cohort: members with 12 months continuous enrollment in the outcome window.

Effect: anyone who died in months 1-11 is silently excluded.
Apparent mortality rate: 0.4%.
True mortality rate:     2.1%.
```

**Fix.** Define cohorts on data observable at `T`. Use survival / time-to-event framing for outcomes that censor enrollment.

---

## L10. Code-set leakage

**Mechanism.** ICD-10 codes are updated annually (Oct 1). CMS-HCC versions change (V24 → V28). HEDIS specs change yearly. Using a code in train data that did not exist in the test period (or vice versa) creates a feature whose meaning silently shifted.

**Example `[synthetic]`.**

```
Feature: HCC_85_CHF flag from V28 mapping.
Train extraction: V28 mappings applied to CY2022-2024 claims.
Test extraction:  V28 mappings applied to CY2025 claims.

Issue: some ICD-10 codes that mapped to V24 HCC 85 do not map to V28 HCC 85.
       Train prevalence and test prevalence diverge for reasons unrelated to disease.
```

**Fix.** Apply the production code-set version to all train / test / production data uniformly. Document `code_set_version` as a pinned input. Cross-link: defer to the sibling `hcc-nlp` skill for V28 / V24 mapping mechanics.

---

## Leakage audit checklist

For every feature in the spec, the agent must answer:

```yaml
feature_name: ED_VISIT_COUNT_LAST_90D
leakage_audit:
  L1_claim_lag:          checked   # what claim-lag policy applies?
  L2_lab_result_lag:     n/a       # not a lab feature
  L3_raf_circularity:    n/a       # not a derived risk score
  L4_label_lookahead:    checked   # feature window strictly before label window
  L5_retroactive_attr:   n/a       # not an attribution feature
  L6_mortality_lag:      checked   # death-feed cushion applied at cohort level
  L7_hospice_lag:        checked   # hospice cushion applied
  L8_auth_referral:      n/a       # not an authorization feature
  L9_cohort_selection:   checked   # cohort defined on T-observable data
  L10_code_set:          checked   # V28 applied uniformly
status: PASS
notes: rolling 90-day window uses received_date <= T + 30d
```

Findings that come back as anything other than `n/a` or `PASS` populate [`templates/leakage-audit-report.md`](../templates/leakage-audit-report.md).

---

## Common interview question: "We held out the last 6 months as a test set. Are we good?"

No. Temporal holdout is necessary but not sufficient. You also need:
- Claim-lag matching (L1) between train extraction and production scoring.
- Code-set version matching (L10) across train, test, production.
- Cohort definition observable at `T` (L9).
- Label-generation function that does not see post-`T` data (L4).
- Attribution and risk-score features pinned to point-in-time (L3, L5).

A clean temporal holdout with leaky features just makes the leakage harder to spot.
