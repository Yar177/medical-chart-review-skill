# GSD — Glycemic Status Assessment for Patients with Diabetes

**Reporting path:** Admin / Hybrid; ECDS direction
**Population focus:** Adults 18-75 with diabetes
**Note:** GSD **replaced HBD (Hemoglobin A1c Control for Patients with Diabetes)** starting MY 2024. GSD broadens evidence to include Glucose Management Indicator (GMI) from continuous glucose monitoring, not just HbA1c.

## Denominator

- Members 18-75 as of end of MY
- Continuous enrollment through MY
- Diabetes diagnosis identification (typically two outpatient or one inpatient diagnosis during MY or prior year, OR a dispensed antihyperglycemic medication)

## Numerator (reported as two separate rates - inverse logic)

- **GSD Good Control:** most recent glycemic status assessment during MY shows result < 8.0%
- **GSD Poor Control (inverse - lower is better):** most recent glycemic status assessment during MY shows result > 9.0% (or missing)

Evidence types:
- HbA1c lab result
- Glucose Management Indicator (GMI) from CGM device (new under GSD)

## Exclusions

- Hospice
- Palliative care
- Advanced illness / frailty exclusion for members 66+
- Gestational diabetes only (not type 1 or type 2)
- Steroid-induced diabetes (denominator exclusion if it's the only diabetes evidence)

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md) (added in Phase 1). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-based, no event anchor |
| **Compliance window** | Most recent qualifying assessment during MY (Jan 1 - Dec 31) |
| **Date types that COUNT** | Lab specimen collection date (HbA1c); CGM analysis window end-date (GMI) |
| **Date types that do NOT count** | Lab result/report date alone, order date, note signing date alone, prior-year result, future-scheduled order |
| **"Most recent" disambiguation** | If multiple A1cs in MY, use latest by **specimen collection date** (not result-posting date) |
| **Look-back / look-forward** | None - MY-only |

**Common date confusions for this measure**

- Prior-year A1c referenced in a current-MY note via copy-forward - the evidence date is the *original* collection date, which is outside MY
- A1c collected late in MY at outside retail clinic; result reaches EHR in following year - collection date is in MY, so it counts; do not use result-posting date
- CGM "estimated A1c" / GMI - the evidence date is the *analysis window end* (last day of the 14-day or 90-day GMI window), not the device upload date or the visit date when the report was reviewed
- Note dated Jan 5 of next year referencing "A1c done last month" - resolve to specific date; if that date falls in MY, it counts

## NLP signal phrases

**Section hints:** Results (labs), Assessment, Plan, flowsheet, CGM device data

**Positive signals**
- "HbA1c" / "A1c" / "hemoglobin A1c" with numeric value
- "GMI" / "glucose management indicator"
- "CGM data: GMI 6.8%"
- "estimated A1c from CGM"
- "Dexcom G7 report" / "Libre 3 report" (implies GMI available)

**Result interpretation phrases**
- "A1c at goal" / "good control"
- "A1c above goal" / "uncontrolled"

**Exclusion signals**
- "hospice" / "comfort care"
- "gestational diabetes" (when sole diabetes evidence)
- "metastatic" / "frailty"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md) (added in Phase 1). This block captures measure-specific pitfalls.

- **"HbA1c result: 6.8%" near the word "negative"** (e.g., "negative for diabetic retinopathy; HbA1c 6.8%") - the A1c is POSITIVE evidence; do not let nearby negation triggers scope onto the result
- **"HbA1c not done this visit" / "A1c deferred"** - negation of the action; this visit does not contribute evidence
- **"Patient declined A1c"** - refusal, not negation of the measure concept; track separately, does not close measure
- **"A1c ordered" / "A1c pending" / "will check A1c next visit"** - temporality: future intent, not evidence
- **"Hx of poorly controlled DM, A1c was 11% last year"** - temporality: historical; do NOT attribute to current MY
- **"FH of T2DM"** - experiencer = family; relevant for risk counseling but not the patient's GSD numerator
- **"Random glucose 180" / "fasting glucose 110" / "FPG"** - NOT A1c or GMI; do not count as glycemic status assessment for this measure
- **"A1c not interpretable due to hemoglobinopathy / hemolysis / pregnancy"** - assessment was performed but result is invalid; verify spec handling (may require alternative evidence or exclusion)
- **"A1c at goal" without a numeric value** - hedging; needs the actual value to be scored
- **"Continue current diabetes regimen, A1c stable"** - implies prior A1c result; not new evidence unless paired with a current numeric value and date

## Common documentation gaps

- A1c done at retail clinic / point-of-care; result in narrative but not structured Results
- CGM GMI shown in device report (PDF) but not pulled into structured observations
- Lab result outside MY (only prior-year result)
- Diabetes diagnosis on problem list but no qualifying encounter or prescription

## Notes

- **GSD vs HBD:** GSD broadens acceptable evidence to include GMI - reflects real-world CGM adoption. NLP pipelines targeting older charts should still handle HBD-era data
- "Most recent" rule applies - if multiple A1cs in MY, use the last one
- Poor control rate is **inverse** (lower is better) - reporting and dashboards must handle direction correctly
- ECDS direction: structured lab result via FHIR `Observation` with LOINC for HbA1c / GMI

## See also

- [`BPD.md`](BPD.md)
- [`EED.md`](EED.md)
- [`KED.md`](KED.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2 (note MY 2024+ for GSD definition)
