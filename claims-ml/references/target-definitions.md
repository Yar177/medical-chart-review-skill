# Target Definitions for Claims-Based ML

The target is the most under-reviewed part of a healthcare ML pipeline. Teams pick "cost" or "admit" and move on. The agent's job is to slow them down: what does the target *mean*, what distribution does it have, what action does it drive, and what mis-specifications quietly produce bad models.

## Per-target catalog

| Target | Default specification | Common mis-specifications |
|---|---|---|
| Cost | Per-member-per-month allowed amount, log or Tweedie | Raw dollar, OLS regression, no PMPM normalization |
| Hospitalization | Any IP admit in `[T+1, T+90]` | Combining planned + unplanned; ignoring obs-vs-IP |
| Readmit | Unplanned IP admit within 30 days of index discharge | Including planned readmits; ignoring competing risk of death |
| ED utilization | ED visit count in window | Treating high-utilizer 8-visits same as 1-visit |
| Disease onset | First claim with target dx in window | Treating first claim as true onset; ignoring left-censoring |
| Mortality | Death within window | No censoring for disenrollment; missing death-feed lag |
| Eligibility scoring | Program-eligible flag at T | Reviewer-judged target leaks judgment criteria |
| Composite | Cost + admit + ED, weighted | Components disagree; weights are arbitrary |

---

## §1. Cost prediction

### The distribution problem

PMPM cost is zero-inflated and heavy-tailed. A typical MA population `[synthetic]`:

```
Members:                         50,000
Median PMPM:                     ~$310
Mean PMPM:                       ~$890
P95 PMPM:                        ~$3,200
P99 PMPM:                        ~$11,500
Top 1% share of total cost:      ~28%
Zero-cost months (no claims):    ~22% of member-months
```

OLS on raw dollars fits the mean and misses the tail. The agent should refuse to bless a cost model fit with OLS on raw dollars.

### Acceptable specifications

| Specification | When to use | Notes |
|---|---|---|
| Tweedie regression (power ~1.5) | Default for PMPM cost | Handles zero-inflation + heavy tail |
| Two-part model (P(cost>0) + E[cost\|cost>0]) | When zero-cost is a meaningful regime | Interpretable; two model artifacts |
| Log(1 + cost) regression | When tail is not the primary concern | Predictions on raw scale require correction (smearing) |
| Quantile regression at P90 | When the action targets the tail | Single quantile only; no full distribution |
| Gamma GLM (cost > 0 only) | Severity in a two-part setup | Combine with logistic for occurrence |

### Common pitfalls

- **Per-member-year cost without normalization for partial-year membership.** A member with 4 months of enrollment cannot be compared at face value to a 12-month member. Normalize to PMPM and weight by member-months.
- **Allowed vs paid amount.** Allowed includes member cost-share; paid does not. The action drives the choice. Care management cares about allowed (total burden); plan financial planning cares about paid. Document the choice.
- **Risk-score circularity.** See [`target-leakage.md`](target-leakage.md) L3.
- **Log-transform back-transformation.** `exp(predict(log(1+y)))` is biased; needs smearing or Duan correction.
- **Truncation of high-cost outliers.** Common practice is to truncate at the 99th percentile. This systematically under-predicts the tail that drives the action.

---

## §2. Hospitalization / readmit prediction

### Hospitalization (90-day, 180-day)

**Default target.** Any unplanned IP admit in `[T+1, T+H]` where H is the horizon.

**Confusions to resolve up front.**

| Question | Action |
|---|---|
| Planned admits included? | Default no; planned admits are predicted by pre-auth |
| Observation stays count as admits? | Default yes for clinical action; no for financial action |
| Transfers from ED to IP count as ED or IP? | The IP admit counts; the ED visit is a separate event |
| LTCH / IRF / SNF count as IP? | Generally no; require explicit IP-acute filter |
| Behavioral-health IP separate? | Often modeled separately; depends on benefit carve-out |

### Readmit (30-day, all-cause vs cause-specific)

**The competing-risk problem.** Death after index discharge censors readmit. A model that ignores death will:

- Treat dead members as "no readmit" (correctly, in a sense).
- But the action target ("members at risk of readmit") implicitly assumes the member is alive to be readmitted.
- Members at highest readmit risk also have highest death risk; the competing risk creates a downward bias in the predicted probability.

**Recommended framings.**

- Cause-specific hazard model: `Pr(readmit | alive at t)` and `Pr(death | no readmit at t)` as separate models, combined via subdistribution.
- Fine-Gray subdistribution hazard for direct prediction.
- Simple workaround: exclude members who died in `[T+1d, T+30d]` from the test set and document.

**Planned-vs-unplanned distinction.** CMS HRRP defines planned readmits via a published algorithm (procedure-list + diagnosis-list). Use it explicitly; do not invent a heuristic.

### Worked example `[synthetic]`

```
Model: 30-day all-cause unplanned readmit at index discharge.
Index population: 8,200 IP discharges in 2024 [synthetic].

Outcomes in [discharge_date+1d, discharge_date+30d]:
  unplanned readmit:   1,025  (12.5%)
  planned readmit:       148   (1.8%)
  death (no readmit):    198   (2.4%)
  none of above:       6,829  (83.3%)

Bad target: any readmit (includes planned)
Better target: unplanned readmit
Best target: unplanned readmit with death modeled as competing risk
```

---

## §3. ED utilization

**Default target.** ED visit count in `[T+1, T+H]`, or binary `≥ N ED visits`.

**The intensity question.** A model that predicts ≥1 ED visit captures most of the population (~25-30% of MA members visit ED in a year). The action probably targets high-utilizers (≥4 visits / year). Pick the threshold based on the action, not the distribution.

**Count regression options.**
- Poisson: assumes mean = variance; violated for ED data.
- Negative binomial: handles over-dispersion.
- Zero-inflated negative binomial: handles excess zeros (most members have 0 ED visits in any given month).

---

## §4. Disease onset / progression

### Onset semantics

**First claim != true onset.** A claim with `dx = E11.9` (Type 2 diabetes) might be:

- True onset (member newly diagnosed).
- Newly enrolled member with longstanding condition (left-censored).
- Coding change (provider added the code; condition existed prior).
- Rule-out documentation (provider was investigating, condition not confirmed).

**Recommended definitions.**

- Incident case: first claim with target dx in window AND no claim with target dx in `[T - 24m, T]` lookback AND ≥ 12 months continuous enrollment before T.
- The lookback requirement is critical. Without it, the model predicts newly-enrolled-and-coded members, not true incidence.

### Left-censoring

For any member without 12+ months of prior enrollment, target value is unknown (could be prevalent, could be incident). Default: exclude from training and clearly flag in production scoring as `incident_status = UNKNOWN`.

### Progression

For disease progression (e.g., CKD stage 3 to stage 4, diabetes to diabetes-with-complications), the same first-claim-vs-true-progression problem applies. Add: progression often shows in labs before it shows in claims, so claim-only progression models lag clinical progression by months.

---

## §5. Mortality / end-of-life

**Default target.** Death within `[T+1, T+H]`.

**Censoring requirements.**

- Disenrollment from plan censors the outcome (member could die after disenrollment and you would not know).
- Switch to dual coverage / Medicaid / a different payer is a censoring event.
- See [`target-leakage.md`](target-leakage.md) L6 for death-feed lag.

**Action sensitivity.** Mortality models that drive end-of-life-care enrollment have high downside risk: falsely-flagged members can be inappropriately steered toward hospice; falsely-unflagged members miss the program. Calibration matters more than discrimination. See [`evaluation-metrics.md`](evaluation-metrics.md).

---

## §6. Program-eligibility scoring (CM, DM, complex care)

**The label-leakage problem.** "Eligible for our complex-care program" is often defined by clinician review of high-risk members. The features that the clinician uses (recent admits, polypharmacy, ED count) are then used to train a model to predict the clinician's label. The model learns the clinician's heuristic, not eligibility.

**Recommended framings.**

- Predict the downstream outcome the program is supposed to prevent (admits, ED, cost), not the eligibility label itself.
- If the eligibility label is the target, isolate which features the clinician actually used and audit each as a leaky proxy.
- Treat program-eligibility scoring as a recommendation system, with a human-in-loop confirmation step.

---

## §7. ICD-10 anomaly detection

**What "anomaly" means here.** Unusual coding patterns at the provider, member, or claim level. Common applications: FWA (fraud / waste / abuse), upcoding detection, provider-profiling outliers, member-level rare-condition signal.

**Target options.**

- Supervised: requires labeled examples (validated upcoding, validated FWA). Labels are scarce and biased toward what auditors caught.
- Semi-supervised: known-normal cases as positive class.
- Unsupervised: density / isolation / autoencoder on coding distributions. The "anomaly" is the artifact you choose to measure.

**Pitfall.** Unsupervised anomaly scores often surface unusual specialties (e.g., oncology, palliative care, transplant medicine) because their coding distributions are unusual. Filter by specialty before applying population-level anomaly detection, or build per-specialty models.

---

## §8. Composite endpoints

**The disagreement problem.** A composite of cost + admits + ED-visits weighted as a single score will:

- Drive different model behavior than three separate models because component disagreements are masked.
- Be hard to interpret post-hoc when one component dominates.
- Make calibration impossible to assess at the component level.

**Recommendation.** Build the three component models, then compose at the action layer (rule-based weighting, threshold combination). Calibrate each component independently.

---

## §9. Target-spec YAML (canonical)

Required for any model under audit.

```yaml
target_spec:
  name: 90d_unplanned_hospitalization
  type: binary                          # binary | count | continuous | survival | competing_risks
  definition: >
    Any IP admission with claim_type = IP_ACUTE
    AND admission_date in [T+1, T+90]
    AND CMS HRRP planned-admit algorithm = false
    AND member alive at admission_date
  population: MA membership, age 18+, ≥12mo continuous enrollment as of T
  action_driven: high-risk care management outreach
  rate_in_population: 0.085 [synthetic]   # to calibrate metric expectations
  competing_risks:
    - death_in_window: handled via cause-specific hazard
    - disenrollment_in_window: censored at disenrollment
  truncation_or_winsorization: none
  units: binary
  authoritative_source: CMS HRRP 2025 spec (cite document version)
```

If any field is missing the agent flags it.

---

## §10. Target-audit checklist

```yaml
target_audit:
  type_matches_action:                  PASS | FAIL
  distribution_documented:              PASS | FAIL
  zero_inflation_handled_if_present:    PASS | FAIL | N/A
  competing_risks_handled_if_present:   PASS | FAIL | N/A
  left_censoring_handled_if_present:    PASS | FAIL | N/A
  partial_enrollment_normalized:        PASS | FAIL | N/A
  planned_vs_unplanned_resolved:        PASS | FAIL | N/A
  composite_components_separated:       PASS | FAIL | N/A
  spec_yaml_complete:                   PASS | FAIL
overall: PASS | FAIL
```

Any FAIL on the first 5 rows is Critical.
