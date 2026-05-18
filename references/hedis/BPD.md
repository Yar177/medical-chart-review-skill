# BPD — Blood Pressure Control for Patients with Diabetes

**Reporting path:** Admin / Hybrid (varies by MY); ECDS direction
**Population focus:** Adults 18-75 with diabetes

## Denominator

- Members 18-75 as of end of MY
- Continuous enrollment through MY
- Diabetes diagnosis identification (typically two outpatient diagnoses or one inpatient diagnosis during MY or prior year, OR a dispensed antihyperglycemic medication)

## Numerator

- **Most recent BP reading during MY < 140/90 mmHg**
- Both systolic AND diastolic must meet the threshold
- The BP must be recorded by a clinician (or self-reported home BP captured by clinician, per current spec - verify)

## Exclusions

- Hospice during MY
- ESRD / dialysis
- Pregnancy during MY (any time)
- Non-acute inpatient stay during MY
- Advanced illness / frailty exclusion for members 66+
- Gestational or steroid-induced diabetes (denominator exclusion if it's the only diabetes evidence)

## NLP signal phrases

**Section hints:** Vitals, Plan ("BP at goal"), Assessment ("HTN controlled"), Results, flowsheet

**Positive signals**
- BP value patterns like "BP 128/78" / "B/P 132/84" / "blood pressure 130/80"
- "BP at goal"
- "hypertension controlled"
- "normotensive today"

**Negative / exclusion signals**
- "ESRD" / "on dialysis" / "HD" / "PD" / "renal transplant"
- "pregnant" / "G_P_ with active pregnancy" / "EDC"
- "hospice" / "comfort care"
- "metastatic" / "advanced illness"

**False positives to filter**
- BP from triage taken before pain treatment / panic (often re-checked - use most recent during MY per spec)
- "BP elevated, re-check" without follow-up reading (use the re-check value if same date)
- BP from non-clinician source (e.g., patient-reported without clinician documentation) - verify current spec
- "white coat hypertension" without confirmed reading at goal

## Common documentation gaps

- Multiple BPs in same visit - need clear "most recent" or "lowest of the day" handling per spec
- Home BP readings dictated into note but not captured as structured vitals
- BP at goal but no diabetes diagnosis on the same encounter chain (denominator failure, not numerator)

## Notes

- **BPD vs CBP**: BPD is diabetic-population BP control; [CBP](CBP.md) is the broader hypertension control measure
- Both share BP <140/90 threshold today; older specs used different thresholds for some populations
- ECDS direction: structured BP (FHIR `Observation` with LOINC for systolic + diastolic) is preferred

## See also

- [`CBP.md`](CBP.md)
- [`GSD.md`](GSD.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
