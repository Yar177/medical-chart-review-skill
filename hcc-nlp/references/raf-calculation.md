# RAF (Risk Adjustment Factor) calculation

> **Why this file exists:** NLP teams often build HCC extractors without understanding how outputs flow into the RAF score. That leads to two common errors: (1) treating all HCCs as equally valuable (they are not - coefficients vary 10x+) and (2) ignoring interactions (some HCC combinations add a third coefficient).

This file is conceptual. We do not redistribute CMS coefficient tables; source them from the official CMS-HCC or HHS-HCC software packages described in [`model-versions.md`](model-versions.md).

---

## 1. RAF formula (CMS-HCC, simplified)

For a given member in a given calendar year:

```
RAF = demographic_component
    + sum(HCC_coefficient_i for each HCC the member has)
    + sum(interaction_coefficient_j for each qualifying interaction)
    + community / institutional / new-enrollee adjustment
```

Then normalized:

```
Normalized RAF = RAF / CMS normalization factor (annual)
```

CMS publishes the normalization factor and any coding-pattern adjustment each year. Plans receive capitation proportional to the normalized RAF, multiplied by the county base rate and adjusted for Star ratings and other factors.

**NLP implication:** A "+0.105" HCC coefficient is not "small." Multiplied across thousands of members and the county base rate, a recall miss on a common HCC can be a seven-figure shortfall. Conversely, a false positive on a high-coefficient HCC creates audit risk proportionally larger than the immediate dollar value (see [`compliance-and-enforcement.md`](compliance-and-enforcement.md)).

## 2. The four input categories

### Demographic component

Driven by claims and enrollment data, not chart text:

- Age band (typically 5-year buckets)
- Sex
- Medicaid dual-eligibility status
- Originally-disabled status (entered Medicare under age 65 via disability)
- Community / institutional / new-enrollee segment

NLP does not produce this. But the **segment** (community vs institutional vs new-enrollee) selects which CMS-HCC coefficient table applies, so the segment is required context when scoring RAF.

### HCC coefficients

One per HCC the member has in the calendar year. These come directly from extractor output (or claims). The 6 cards in [`cards/`](cards/) show how to think about extraction targets per HCC.

### Disease-disease interactions

CMS-HCC has a small number of named interactions that add an extra coefficient when two specific HCCs co-occur. Examples (illustrative, verify against current model):

- DM + CHF
- CHF + COPD
- DM + Renal
- Cancer + Immune

**NLP implication:** Your pipeline must check post-extraction whether interaction-eligible pairs are present and surface them. Some teams handle this in the scoring layer, not the extraction layer; either is fine, but it must happen somewhere.

### Disabled / institutional interactions

Separate set of interactions for the disabled-under-65 segment and institutional segment. Same logic: post-extraction check.

## 3. HHS-HCC differences

HHS-HCC's calculation is structurally similar (demographic + HCC + interactions) but uses:

- Separate models for adult / child / infant
- Metal-tier-specific induced demand factors
- An infant model that includes maturity and severity HCCs not present in CMS-HCC
- Different interaction terms

If you serve ACA marketplace, your pipeline runs the same kind of post-extraction roll-up but against the HHS-HCC coefficient files for the benefit year.

## 4. Annual reset

Every chronic condition resets January 1 in the calendar year:

- A diagnosis documented in December 2025 does not carry to 2026.
- Each chronic HCC must be re-documented at least once in a qualifying face-to-face encounter in 2026 to count for PY 2027 (CMS-HCC uses prior-year claims for current-year payment).
- Status conditions (amputation, ostomy, transplant) require annual recapture even though they are permanent.

**NLP implication:**

- Your suspect engine should highlight prior-year HCCs not yet recaptured this year (the "open HCC" list).
- Your validate engine must enforce that the supporting evidence is dated in the correct calendar year.
- "Carry-forward" of HCCs from prior year is never valid for current-year RAF.

See [`date-of-service.md`](date-of-service.md) for the full date-handling framework.

## 5. Payment-year vs service-year terminology

This trips up new NLP teams.

- **Service year** = the calendar year the diagnosis is documented (also called dates-of-service year, claims year, encounter year).
- **Payment year** = the year CMS pays the plan using those diagnoses. For CMS-HCC, payment year typically uses prior-year service-year diagnoses.

So for payment year 2026, CMS-HCC uses calendar-year 2025 dates of service. Your extractor outputs should be tagged with the service year. The plan's risk-adjustment submission process maps service years to payment years.

## 6. Coding pattern adjustment / coding intensity

CMS applies an annual downward adjustment to MA risk scores to account for documented coding intensity differences vs fee-for-service Medicare. This is a flat multiplicative haircut and does not change per-member.

**NLP implication:** Your RAF estimates are pre-adjustment. The plan's actuarial team applies the haircut downstream. Do not double-apply.

## 7. RAF as an evaluation signal

When measuring extractor quality, dollar-weighted metrics are often more useful than equal-weighted metrics. Examples:

- **RAF recall**: sum of RAF dollars captured / sum of true RAF dollars present
- **RAF precision**: sum of RAF dollars validated / sum of RAF dollars claimed
- **Per-HCC dollar-weighted F1**: F1 weighted by HCC coefficient

These are not replacements for per-HCC precision / recall (which you also need). They give business-meaningful summaries. See [`evaluation-and-validation.md`](evaluation-and-validation.md).

## 8. Common RAF mistakes in NLP pipelines

- **Equal-weighting all HCCs in loss functions.** A model tuned this way under-prioritizes the high-coefficient HCCs that drive the most dollars and audit risk.
- **Forgetting the interaction layer.** Captures all the right HCCs but misses the interaction lift.
- **Not respecting hierarchies before scoring.** Sums coefficients for HCC 18 and HCC 19 when only HCC 18 should apply (see [`hierarchies.md`](hierarchies.md)).
- **Mixing service-year and payment-year RAFs.** RAF estimates not tagged with service year cannot be reconciled with downstream actuarial work.
- **Comparing RAF across model versions naively.** A member's V24 RAF is not directly comparable to V28 RAF; the models differ.

## See also

- [`model-versions.md`](model-versions.md) - which coefficient tables apply
- [`hierarchies.md`](hierarchies.md) - apply hierarchies BEFORE summing coefficients
- [`date-of-service.md`](date-of-service.md) - calendar-year and recapture rules
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - dollar-weighted metrics
