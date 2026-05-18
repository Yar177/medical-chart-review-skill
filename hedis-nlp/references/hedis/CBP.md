# CBP — Controlling High Blood Pressure

**Reporting path:** Hybrid historically; ECDS direction
**Population focus:** Adults 18-85 with hypertension
**Stars:** Triple-weighted in Medicare Advantage Stars (verify current MY)

## Denominator

- Members 18-85 as of end of MY
- Continuous enrollment through MY
- Hypertension diagnosis identification: outpatient HTN diagnosis in the first 6 months of MY, OR HTN diagnosis in the year prior to MY
- "Event" date is the first HTN diagnosis in that window

## Numerator

- **Most recent BP reading during MY < 140/90 mmHg**
- Reading must be on or after the HTN-event date
- Both systolic AND diastolic must meet threshold

## Exclusions

- ESRD, dialysis, kidney transplant
- Pregnancy during MY
- Non-acute inpatient stay during MY
- Hospice
- Advanced illness / frailty exclusion for members 66+
- Palliative care

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | First qualifying HTN diagnosis (in first 6 months of MY or in year prior) |
| **Compliance window** | Most recent qualifying BP during MY, **on or after the HTN-event date** |
| **Date types that COUNT** | Encounter date of the visit where BP was recorded by clinician |
| **Date types that do NOT count** | Note signing date when BP is copy-forward, BP recorded before the HTN-event date in MY, BPs in unstructured narrative without encounter context, prior-year BP |
| **"Most recent" disambiguation** | Latest qualifying BP by encounter date; if multiple same-day, follow current spec (often lowest of the day or last recorded) |
| **Look-back / look-forward** | None for numerator; HTN diagnosis identification looks back into prior year |

**Common date confusions for this measure**

- HTN diagnosis on problem list with no encounter dx in qualifying window - denominator failure, not numerator
- BP recorded before the HTN event-date in MY - does NOT count for numerator even if value is at goal
- Home BP reported in a telehealth visit - the documentation date in the clinician's note is the evidence date; verify spec acceptance
- Single elevated BP with same-day re-check - the qualifying value per spec is usually the lowest of the day or last recorded

## NLP signal phrases

**Section hints:** Vitals, Assessment, Plan, Results, flowsheet

**Positive signals**
- BP value patterns: "BP 122/78" / "blood pressure 130/82"
- "hypertension controlled" / "HTN at goal" / "BP at goal"
- "normotensive on current regimen"

**HTN diagnosis confirmation (for denominator)**
- "essential hypertension" / "HTN" / "primary hypertension"
- "I10" referenced
- "on antihypertensive therapy"

**Negative / exclusion signals**
- "ESRD" / "on hemodialysis" / "HD" / "PD" / "renal transplant"
- "pregnant" / "EDC" / "G_P_ active pregnancy"
- "hospice" / "comfort care"
- "frailty" / "advanced illness" / "metastatic cancer"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"BP at goal" / "HTN controlled" / "normotensive"** without numeric value - hedged; needs the actual reading to score
- **Single elevated BP from urgent care during acute pain or anxiety** - use the most recent qualifying reading per spec
- **"BP elevated, will recheck next visit"** - first reading is the data; "will recheck" is future
- **"PMH: HTN, BP runs 120s/70s at home"** - historical narrative; not encounter-recorded data
- **"Patient denies HTN symptoms"** - symptom negation; does not affect BP value
- **"Mother / spouse with HTN"** - experiencer = family
- **"Stable on current regimen"** alone - hedged, no numeric value
- **"Secondary hypertension" / "renovascular HTN"** - check whether spec includes; primary essential HTN is the typical denominator
- **"White coat hypertension"** - context modifier; doesn't auto-qualify a normal value
- **"If BP elevated next visit, will add lisinopril"** - hypothetical
- **BP recorded in nurse-triage flowsheet only** - verify spec acceptance vs requirement for clinician attestation

## Common documentation gaps

- HTN diagnosis on problem list but no encounter-level dx code (some specs require encounter dx)
- BP readings only in nurse triage without provider attestation
- Multiple readings same visit - need clear handling per spec
- BP readings outside MY (member with only prior-year visits)

## Notes

- CBP threshold is currently <140/90 across populations (older specs split by age/diabetes); verify current MY
- ECDS direction: structured BP via FHIR `Observation` with LOINC codes for systolic / diastolic; date and provenance must be captured
- Telehealth BP: home readings reported during a telehealth visit and documented by the clinician typically count per current spec - verify

## See also

- [`BPD.md`](BPD.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
