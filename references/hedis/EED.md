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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-only with 1-year look-back extension |
| **Compliance window** | Eye exam by eye care professional during MY; OR negative-retinopathy exam in the year prior to MY |
| **Date types that COUNT** | Procedure date of retinal/dilated exam; for teleophthalmology, the imaging date |
| **Date types that do NOT count** | Note signing date alone, order/referral date, scheduled future exam, vision screening (Snellen) date |
| **"Most recent" disambiguation** | Any qualifying exam in the window; if a prior-year negative exam carries forward, the original exam date is the evidence date |
| **Look-back / look-forward** | 1 prior year extension if the prior exam was **negative for diabetic retinopathy** |

**Common date confusions for this measure**

- Outside ophthalmology report received during MY but the exam itself was in a prior year - the **exam date** is the evidence date, not the receipt or scan date
- Teleophthalmology / point-of-care retinal imaging: the imaging acquisition date is the evidence date, not the remote-read date if delayed
- Annual PCP "vision screening" date confused with retinal exam date - they are not equivalent regardless of date
- Cataract surgery date confused with retinal exam - the surgery does not satisfy the eye-exam requirement on its own

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

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Vision screening" by PCP (Snellen alone)** - NOT a retinal exam regardless of context
- **"Will refer to ophthalmology" / "due for eye exam"** - temporality: future intent
- **"Patient declined ophthalmology referral"** - refusal, not compliance; tracked separately
- **"Glasses prescription updated" / "refraction stable"** - refraction is not a retinal exam
- **"Family hx of diabetic retinopathy"** - experiencer = family
- **"No DR noted"** without provider type or exam date - hedged; need eye-care-professional attribution and date
- **"Eye exam done elsewhere"** without date or provider type - hedged; cannot anchor a date or qualify the provider
- **"PMH: diabetic retinopathy"** - historical dx; does not prove an eye exam this MY
- **"S/p cataract surgery"** - cataract surgery alone does not satisfy the retinal exam requirement
- **"Eye exam negative for DR"** in a prior-year note - POSITIVE evidence (extends one MY); do not let "negative" flip it

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
