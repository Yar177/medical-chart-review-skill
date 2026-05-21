# Fairness & Equity for Claims-Based ML

Healthcare ML models touch people's access to care, insurance pricing, and clinical recommendations. Fairness is not optional, and "we dropped race from the features" is not fairness. This file gives the technical methods, the regulatory landscape, and the deferral boundary.

> This file is engineering guidance, not legal advice. Any fairness finding that drives a deployment decision, a member-facing communication, or a regulatory submission requires sign-off from compliance counsel.

## §1. What "fair" means here

There is no single technical definition of fairness. The common operationalizations:

| Definition | One-line | Where it matters |
|---|---|---|
| **Calibration parity** | Predicted = realized within each subgroup at every decile | Cost / risk-score models |
| **Demographic parity** | Selection rate is equal across subgroups | Rare in healthcare; usually inappropriate |
| **Equal opportunity** | TPR (recall) is equal across subgroups | Outreach / care-management eligibility |
| **Equalized odds** | TPR and FPR are equal across subgroups | High-stakes binary decisions |
| **Counterfactual fairness** | Decision would not change if the member's subgroup attribute were different | Causal-modeling extension |

For most claims-ML use cases, the agent should require:

- **Calibration parity** at the population subgroup level, AND
- **Equal opportunity** (recall parity) when the model drives access to a beneficial intervention.

These are the two definitions that map most cleanly to "the model is not systematically harming a subgroup."

---

## §2. Required subgroup splits

At minimum, the agent should require subgroup analysis on:

- Age band (18-44, 45-64, 65-74, 75-84, 85+)
- Sex
- Dual-eligibility status
- Race / ethnicity (self-reported where available; BISG-imputed where not, with documented method)
- Language preference (when collected)
- Geography (CBSA-level or state-level)
- Plan product (HMO vs PPO vs DSNP)

Imputed race / ethnicity (via Bayesian Improved Surname Geocoding or similar) is acceptable as a stopgap but the imputation method itself has accuracy disparities that have to be documented.

---

## §3. The Obermeyer 2019 case (required reading)

Obermeyer et al. (2019), Science, "Dissecting racial bias in an algorithm used to manage the health of populations."

**Summary.** A widely-deployed risk-prediction tool used cost as a proxy for clinical need. Because Black patients historically had lower per-capita care costs (due to differential access to care, not differential disease burden), the tool systematically under-flagged Black patients with equivalent disease for care management. At equivalent cost levels, Black patients had ~26.3% more chronic conditions than White patients.

**Lessons.**

- Cost is not a neutral proxy for need.
- Equalizing predicted cost across subgroups would have masked the access disparity.
- The fix was to predict avoidable harm (active chronic conditions) rather than cost.

**Generalizable principle.** When picking a target, ask: "Does this target itself encode an access disparity?" If yes, the model will replicate the disparity at scale.

---

## §4. Proxy variables - dropping race does not work

Common claim: "We removed race from the features, so the model cannot be discriminatory."

Proxy variables that correlate with race / ethnicity:

- ZIP code (highly correlated)
- Plan product (DSNP membership correlates with race / income)
- Specific provider attribution
- Specific procedure codes (e.g., procedures more commonly performed in certain settings)
- Pharmacy formulary patterns
- Insurance type history

A model trained on "everything except race" can produce as much racial disparity in outputs as one trained with race. The only way to know is to **measure** outputs by race / ethnicity after training.

**Recommendation.** Include race / ethnicity (or imputation) as a *measurement* variable in evaluation, even if it is not used as a *training* feature.

---

## §5. The technical fairness audit

For any claims-ML model, the agent should require:

1. **Subgroup calibration plots.** Calibration plot per subgroup, overlaid on population calibration.
2. **Subgroup decile lift.** Decile lift table per subgroup.
3. **Subgroup AUROC / Brier.** With bootstrap CIs.
4. **Selection-rate analysis.** If the model drives a binary action at a threshold, the selection rate by subgroup.
5. **Recall (equal opportunity) by subgroup.** Especially for beneficial interventions.
6. **Counterfactual sensitivity (optional but recommended).** What happens to a member's prediction if we change only their subgroup attribute, holding other features constant?

**Acceptable thresholds (default; tighter required for high-stakes models).**

| Metric | Maximum acceptable subgroup disparity |
|---|---|
| Calibration ratio (predicted/realized) | ± 15% from population baseline within each decile |
| Selection rate ratio | 80/120 rule (smallest subgroup / largest > 0.80) |
| Recall (TPR) ratio | > 0.85 across all subgroups |
| AUROC | within 0.03 of population AUROC, all subgroups |

Failures on calibration parity are Critical. Failures on selection / recall parity are High and require a documented business decision.

---

## §6. The regulatory landscape (overview, not legal advice)

Defer to compliance counsel on all of the below; this section is for engineering awareness.

| Regulator | Scope | Relevant pointer |
|---|---|---|
| **CMS** | Medicare Advantage, Medicaid managed care | Final Rule 2024 on prior authorization, equity-focused metrics in Star Ratings |
| **NAIC** | State insurance regulators (collective) | NAIC Model Bulletin on Use of AI Systems by Insurers (2023) |
| **State DOIs** | Insurance regulation (e.g., CO, CA, NY) | Colorado SB21-169 (Restrictions on Insurers' Use of External Consumer Data and Algorithms) |
| **FTC** | Unfair / deceptive practices | FTC AI guidance (2023+); applies broadly to commercial insurers |
| **HHS OCR** | Section 1557 (non-discrimination in health programs) | 2024 Final Rule includes algorithm-related provisions |
| **CFPB** | When ML touches insurance pricing / credit-adjacent decisions | Limited but emerging |

**Key obligations that commonly apply.**

- Document the model's training data, intended use, and known limitations.
- Disclose use of algorithms in coverage / care decisions to affected members.
- Perform impact analysis by protected class for any algorithm used in coverage / eligibility decisions.
- Retain records of model decisions for the regulator's record-retention period.

**Strict deferral.** Any question of "is this legal" or "does this meet the requirements of X regulation" goes to counsel. The agent does not interpret law.

---

## §7. The "we cannot fix this with technical changes" boundary

Some unfairness in a model cannot be fixed by retraining:

- The underlying access disparity in the training data.
- The target itself encoding a disparity (Obermeyer cost-as-proxy).
- The action driven by the model being structurally unequal.

In these cases, the model card must say so. A technical fairness section cannot launder a structural inequity. The recommendation in the model card is to escalate to the program owner (medical director, actuary, compliance) for an action-level decision, not to claim the model is "fair" because the disparity is upstream.

---

## §8. Fairness mitigation techniques (with cautions)

| Technique | What it does | Caution |
|---|---|---|
| Subgroup-stratified threshold | Different action thresholds per subgroup | Often legally problematic; requires counsel |
| Calibration refinement per subgroup | Isotonic / Platt scaling per subgroup | Helps calibration parity; does not change rank-order |
| Reweighting training data | Up-weights underrepresented subgroups | Can hurt calibration on dominant subgroup |
| Adversarial debiasing | Trains a head that cannot distinguish subgroup | Often degrades primary task performance |
| Target redefinition | Replace cost-as-need with active-chronic-condition-count | The Obermeyer fix; usually the strongest option |

Mitigation techniques are *not* a substitute for measurement. Always measure first.

---

## §9. Fairness-spec YAML (canonical)

```yaml
fairness_spec:
  model_name: ma_hospitalization_90d_v3
  subgroups_evaluated:
    - {dimension: age_band,         categories: [18-44, 45-64, 65-74, 75-84, 85+]}
    - {dimension: sex,              categories: [F, M, X/Unknown]}
    - {dimension: dual_eligibility, categories: [yes, no]}
    - {dimension: race_ethnicity,   categories: [non-Hispanic White, non-Hispanic Black, Hispanic, Asian, AIAN, Other, Unknown]}
    - {dimension: language,         categories: [English, Spanish, Other, Unknown]}
    - {dimension: geography,        categories: [CBSA 1, CBSA 2, ..., Rural]}
  evaluation_metrics:
    - calibration_plot_per_subgroup
    - decile_lift_per_subgroup
    - auroc_brier_per_subgroup
    - selection_rate_per_subgroup
    - recall_per_subgroup
  thresholds:
    calibration_disparity_max_pct:    15
    selection_rate_ratio_min:         0.80
    recall_ratio_min:                 0.85
    auroc_max_delta:                  0.03
  imputation_method_for_race: BISG (Bayesian Improved Surname Geocoding)
  imputation_method_caveat: "BISG accuracy varies by subgroup; document residual error"
  legal_review_required: yes
  legal_review_status: pending | complete | not-required (with justification)
```

---

## §10. Fairness-audit checklist

```yaml
fairness_audit:
  subgroups_documented:                       PASS | FAIL
  calibration_parity_within_threshold:        PASS | FAIL
  selection_rate_parity_within_threshold:     PASS | FAIL | N/A
  recall_parity_within_threshold:             PASS | FAIL | N/A
  auroc_parity_within_threshold:              PASS | FAIL
  proxy_variables_examined:                   PASS | FAIL
  target_definition_does_not_encode_disparity: PASS | FAIL
  imputation_method_documented:               PASS | FAIL | N/A
  legal_counsel_review_status:                COMPLETE | PENDING | DEFERRED
overall: PASS | FAIL
```

`calibration_parity` and `target_definition_does_not_encode_disparity` failures are Critical.

---

## §11. Deferral guidance (when to stop and escalate)

Stop the engineering audit and escalate when:

- The proposed model targets coverage / eligibility / pricing decisions for individual members.
- A subgroup disparity is identified that cannot be explained by clinical / population factors.
- The model touches a regulated decision (Medicare Advantage Star Rating, prior auth, payment).
- The team proposes a subgroup-stratified threshold or a mitigation that changes outcomes by protected class.
- The model is intended for sale or licensing to another organization.

In every case above, escalate to:

- Compliance counsel (legal review).
- Medical director (clinical / patient-safety review).
- Actuary (financial / pricing review).
- Privacy officer if PHI scope changes (see sibling `hipaa-compliance` skill).
