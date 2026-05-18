# EED — Eye Exam for Patients with Diabetes

**Reporting path:** Admin / Hybrid; ECDS direction
**Population focus:** Adults 18-75 with diabetes

## Denominator

- Members 18-75 as of end of MY
- Continuous enrollment through MY
- Diabetes diagnosis identification (typically two outpatient or one inpatient diagnosis during MY or prior year, OR a dispensed antihyperglycemic medication)

## Numerator (any of the following)

- **Retinal or dilated eye exam by an eye care professional (ophthalmologist or optometrist) during MY** (with or without retinopathy finding)
- **Negative retinal exam by an eye care professional in the year prior to MY** (no diabetic retinopathy result extends to current MY)
- **Bilateral eye enucleation** (anytime - patient is excluded from need but reported as numerator-positive in some specs - verify)

## Exclusions

- Hospice
- Palliative care
- Bilateral eye enucleation may be a numerator-positive depending on spec

## NLP signal phrases

**Section hints:** Results (eye exam reports), Plan, problem list, scanned outside ophthalmology reports

**Positive signals**
- "dilated fundus exam" / "dilated retinal exam" / "DFE"
- "fundoscopy" / "ophthalmoscopy"
- "retinal photography" / "fundus photography" / "retinal imaging"
- "no diabetic retinopathy" / "no DR" / "no signs of diabetic retinopathy" (especially in prior-year exam - extends compliance)
- "ophthalmology consult note"
- "optometry exam"
- "background DR" / "NPDR" / "PDR" / "diabetic macular edema" (implies exam occurred and DR was found)

**Negative / exclusion signals**
- "hospice"
- "comfort care"
- "bilateral enucleation"

**False positives to filter**
- "vision screening" by primary care (Snellen alone) is NOT a retinal exam
- "eye exam recommended" / "due for ophthalmology referral" - intent
- "patient declined ophthalmology referral"
- "glasses prescription updated" - refraction is not a retinal exam

## Common documentation gaps

- Eye exam done by outside ophthalmologist; report mailed/faxed but not in structured Results
- Result noted in narrative ("ophthalmology report received - no DR") but not parsed into structured eye-exam field
- Prior-year negative retinopathy exam not surfaced to current MY compliance check
- Patient seen by optometrist at retail clinic - claim exists but report doesn't

## Notes

- Retinal imaging programs (point-of-care fundus cameras with remote reading) typically count - confirm reading by qualified eye care professional
- "No DR in prior year" rule extends compliance by one MY - this is one of the rare HEDIS lookback extensions
- ECDS direction: structured eye exam result via FHIR `Observation` / `DiagnosticReport`

## See also

- [`GSD.md`](GSD.md)
- [`KED.md`](KED.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
