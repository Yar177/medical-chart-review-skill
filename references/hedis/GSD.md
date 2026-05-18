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

**False positives to filter**
- "A1c ordered" / "A1c pending" - no result
- "A1c done at outside lab" without result reaching EHR
- Random glucose or fasting glucose values - NOT a glycemic status assessment for this measure
- "patient declined A1c"

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
