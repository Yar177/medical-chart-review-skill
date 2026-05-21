# Leakage Audit Report

> Use this template when the feature spec audit surfaces multiple leakage findings or when the user requests a standalone leakage deep-dive.

A focused, single-purpose report. Where the feature-spec audit is a broad table, this is a deep dive on one or a few leakage classes affecting one or a few features.

---

## Header

```yaml
report_metadata:
  model_name: <name>
  target: <target>
  scope: <feature(s) or model section under review>
  notebook_or_pipeline_reference: <path or commit>
  reviewer: claims-ml skill
  review_date: <date>
  references_consulted: [target-leakage]
```

## §1. Executive summary

One paragraph. State which leakage class(es) are present, which feature(s) are affected, and the recommended fix path. Keep this under 200 words.

## §2. Reproduction of the leakage

For each affected feature:

### Feature: `<FEATURE_NAME>`

**Class flagged.** Lx. <name>. Reference: [`references/target-leakage.md`](../references/target-leakage.md#lx-...).

**Mechanism in this model.**

```
<concise description of why the leakage applies in this specific feature>
```

**Numerical evidence (synthetic illustrative or actual if provided).**

```
[synthetic]
Training extract date: <date>
Production scoring date: <date>
Prediction date T: <date>

In training:
  <feature value pattern>

In production:
  <feature value pattern>

Resulting metric inflation:
  Validation AUROC: <x>
  Expected production AUROC: <y>
  Delta: <z>
```

**Severity.** Critical | High | Medium | Low. With justification.

## §3. Cross-checks against other leakage classes

For each affected feature, run the leakage audit checklist from [`references/target-leakage.md`](../references/target-leakage.md#leakage-audit-checklist):

```yaml
feature_name: <FEATURE>
leakage_audit:
  L1_claim_lag:          PASS | FAIL | N/A
  L2_lab_result_lag:     PASS | FAIL | N/A
  L3_raf_circularity:    PASS | FAIL | N/A
  L4_label_lookahead:    PASS | FAIL | N/A
  L5_retroactive_attr:   PASS | FAIL | N/A
  L6_mortality_lag:      PASS | FAIL | N/A
  L7_hospice_lag:        PASS | FAIL | N/A
  L8_auth_referral:      PASS | FAIL | N/A
  L9_cohort_selection:   PASS | FAIL | N/A
  L10_code_set:          PASS | FAIL | N/A
```

## §4. Recommended fixes (per feature)

For each finding above:

| Feature | Fix option | Pros | Cons | Recommended |
|---|---|---|---|---|
| `X` | Shift feature window back N days | Simple; preserves feature | Loses recent signal | Yes |
| `X` | Use received_date instead of service_date filter | Mimics production exactly | More complex query | Acceptable |
| `X` | Drop feature | Eliminates leakage | Loses signal | Only if other options fail |
| ... | ... | ... | ... | ... |

## §5. Re-validation plan

Once fixes are applied, the team should re-run:

1. **Same train/test split** with corrected features.
2. **Compare metrics** pre-fix vs post-fix. The expected pattern: validation metrics drop modestly (the leakage was inflating them); production-mimicking metrics improve (training now matches production).
3. **If validation metrics drop dramatically (> 30% AUROC reduction):** the model was depending entirely on leakage. Reconsider feature set.
4. **If validation metrics do not change:** verify the fix was actually applied; the leakage may not have been the only signal source.

## §6. Sign-off

This is an engineering audit, not actuarial certification. Before deployment:

- [ ] All Critical findings closed.
- [ ] Re-validation results documented.
- [ ] Model card updated with leakage-audit notes.
- [ ] Actuary / medical director / compliance review where the model touches financial / clinical / regulatory decisions.
