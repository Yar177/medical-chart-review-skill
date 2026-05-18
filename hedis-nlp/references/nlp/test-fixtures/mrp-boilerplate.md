# mrp-boilerplate

## Synthetic note

```
Encounter date: 05/02/2025
Provider: Chen, K. MD (Internal Medicine)
Visit type: Hospital follow-up

CC: f/u after hospital discharge 04/22/2025 for CHF exacerbation.

HPI:
68F with HFrEF s/p CHF exacerbation. Discharged on additional torsemide and
new metolazone PRN. Tolerating well, no SOB at rest.

PMH:
- HFrEF (EF 30%)
- CKD stage 3
- T2DM
- HTN

Medications: reviewed.

A/P:
1. CHF - stable. Continue torsemide 40 mg daily; hold metolazone unless weight gain.
2. CKD - watching renal function. BMP today.
3. DM - A1c last 6.8 (02/2025). Continue current regimen.
4. RTC 4 weeks or sooner for s/sx fluid overload.
```

## Expected extraction

```yaml
satisfies_numerator: false   # "Medications: reviewed" alone does NOT satisfy MRP
evidence: []
mrp_failure_reason: |
  "Medications: reviewed" is boilerplate. MRP requires explicit reconciliation
  of the discharge medication list against the pre-admission/current outpatient
  list, documented by an eligible provider. The note shows:
  - Discharge-meds context (torsemide additional, metolazone new)
  - Current-meds discussion in A/P
  - No explicit reconciliation statement linking the two lists
notes_for_reviewer: |
  This is the most common MRP false positive. Pipelines that match the
  phrase "medications reviewed" without requiring reconciliation-specific
  language will over-close MRP.
  Contrast: "Reconciled discharge medications against current outpatient
  regimen: continuing torsemide 40 mg daily, holding metolazone PRN, no
  changes to remaining regimen." would satisfy.
```

## Notes for reviewers

- This is the #1 MRP anti-pattern.
- Require reconciliation-specific language, not generic "meds reviewed."
- Provider role here (MD) is eligible, so role is not the failure - documentation depth is.
- Same encounter date counts for TRC-Med if reconciliation is documented.
