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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | Inpatient discharge (acute or non-acute) |
| **Compliance window** | Med rec within **30 days** of discharge; day of discharge does NOT count - day 1 is the next calendar day |
| **Date types that COUNT** | Date the med-rec documentation was entered by an eligible provider |
| **Date types that do NOT count** | Discharge summary signing date alone, day-of-discharge med-list refresh, med rec by non-eligible role (MA, scribe), reconciliation > 30 days post-discharge |
| **"Most recent" disambiguation** | First qualifying med-rec in the window closes the measure |
| **Look-back / look-forward** | Look-forward 30 calendar days from discharge |

**Common date confusions for this measure**

- Day-of-discharge med rec at the hospital - typically does NOT count for outpatient MRP; day 1 is the next calendar day
- Med rec note dated the day of the outpatient visit but signed days later - the visit / reconciliation date is the evidence date, not the signing date
- Discharge date split across midnight - use the spec-defined discharge date
- Med rec done at follow-up visit but documented in a separate addendum days later - use the visit date as the reconciliation event date

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

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Medications reviewed" alone** - boilerplate; does NOT demonstrate reconciliation; this is the #1 MRP false positive
- **"Current meds listed"** alone - listing is not reconciliation
- **"No changes to medications"** alone - statement of stability is not reconciliation evidence
- **"Med rec" used in a different context** (e.g., medication-assisted recovery, medical record) - lexical collision; require reconciliation-specific phrasing
- **"Discharge med list printed for patient"** - distribution / intent, not reconciliation
- **"Med list reconciled by MA / scribe"** - eligible roles are prescribing practitioner, clinical pharmacist, or RN; other roles do NOT satisfy
- **"Med rec to be done at next visit"** - future intent
- **"Patient refused to review meds"** - refusal documented; does NOT close measure
- **Day-0 med rec at hospital discharge** - day of discharge does NOT count for outpatient MRP
- **"Reconciled with patient verbally"** without documentation of the reconciliation itself - assertion = hedged on substantive content
- **"Outside hospital discharge meds not available"** - barrier to substantive reconciliation; documentation alone of the barrier is not reconciliation

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
