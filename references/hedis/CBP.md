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

**False positives to filter**
- Single elevated BP without re-check or follow-up reading
- BP from urgent care during acute pain - use the most recent qualifying reading
- "white coat hypertension" without controlled reading
- "secondary hypertension" - check whether spec accepts (denominator includes essential HTN primarily)

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
