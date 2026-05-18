# MRP — Medication Reconciliation Post-Discharge

**Reporting path:** Hybrid historically; ECDS direction
**Population focus:** Members 18+ discharged from inpatient

## Denominator

- Members 18 years and older as of end of MY
- Discharged alive from an acute or non-acute inpatient stay during MY (typically Jan 1 through Dec 1 to allow 30-day window within MY)
- Continuous enrollment from discharge through 30 days after

## Numerator

- Medication reconciliation conducted by a **prescribing practitioner, clinical pharmacist, or registered nurse** within **30 days of discharge** (day of discharge does NOT count - day 1 is the next calendar day)
- Documentation must explicitly demonstrate reconciliation, not just review

## Exclusions

- Hospice
- Death within 30 days post-discharge
- Transfers between inpatient settings handled as single stay per spec

## NLP signal phrases

**Section hints:** Medications, Plan, dedicated "Medication Reconciliation" tab/field, post-discharge visit note

**Positive signals - explicit reconciliation**
- "medication reconciliation completed"
- "med rec done"
- "reconciled home medications with discharge medications"
- "discharge medications reconciled"
- "compared home med list to discharge list"
- "no discrepancies between home and discharge meds"
- "discrepancies identified: ___, resolved by ___"
- "discharge med list reviewed and updated in EHR"

**Provider attribution signals**
- "MD reconciled meds"
- "Pharm.D. completed med rec"
- "RN performed medication reconciliation"
- "NP/PA reconciled"

**Negative signals (insufficient evidence)**
- "medications reviewed" alone (without "reconciled")
- "current meds listed" alone
- "no changes to medications" alone (does not demonstrate reconciliation)

**False positives to filter**
- "med rec" used in a different context (e.g., medication-assisted recovery)
- Med list refreshed at visit without reference to discharge meds
- Discharge med list printed for patient (intent, not reconciliation)

## Common documentation gaps

- Med rec done verbally in visit; documentation says "meds reviewed" not "reconciled"
- Reconciliation done by MA / non-eligible provider; doesn't satisfy spec
- Discharge med list not available in the post-discharge visit (outside hospital, no HIE feed)
- Reconciliation done > 30 days post-discharge
- Visit on day of discharge - typically does NOT count (day 0)

## Notes

- **MRP ↔ TRC-Med overlap:** MRP is a standalone measure; TRC has a Medication Reconciliation sub-indicator with the same intent and 30-day window. Different reporting programs use one or both - verify
- **Explicit "reconciliation" language is the documentation differentiator** - templated phrasing helps
- Eligible providers: prescribing practitioner (MD/DO/NP/PA), clinical pharmacist, RN
- ECDS direction: structured `Procedure` or specific reconciliation `Observation` via FHIR

## See also

- [`TRC.md`](TRC.md) (TRC-Med sub-indicator)
- [`FUH.md`](FUH.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
