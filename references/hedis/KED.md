# KED — Kidney Health Evaluation for Patients with Diabetes

**Reporting path:** Admin
**Population focus:** Adults 18-85 with diabetes

## Denominator

- Members 18-85 as of end of MY
- Continuous enrollment through MY
- Diabetes diagnosis identification (typically two outpatient or one inpatient diagnosis during MY or prior year, OR a dispensed antihyperglycemic medication)

## Numerator

- **Both** of the following during MY:
  - Estimated glomerular filtration rate (**eGFR**) lab result
  - Urine albumin-creatinine ratio (**uACR**) lab result

Both tests must be in the same MY - missing either fails the measure.

## Exclusions

- Hospice
- Palliative care
- ESRD / dialysis / kidney transplant
- Advanced illness / frailty exclusion for members 66+

## NLP signal phrases

**Section hints:** Results (labs), Assessment, Plan

**Positive signals - eGFR**
- "eGFR" with numeric value
- "estimated GFR"
- "GFR ___ mL/min/1.73m²"
- "creatinine" with calculated eGFR
- "CKD-EPI" / "MDRD" (calculation methods)

**Positive signals - uACR**
- "uACR" / "urine ACR"
- "urine albumin-to-creatinine ratio"
- "urine microalbumin / creatinine"
- "microalbumin"
- "spot urine microalbumin"
- "albuminuria screen"
- Numeric result in mg/g or mg/mmol

**Negative / exclusion signals**
- "ESRD" / "on hemodialysis" / "HD" / "PD" / "renal transplant" / "s/p kidney transplant"
- "hospice"
- "metastatic" / "advanced illness" / "frailty"

**False positives to filter**
- "urinalysis with protein" alone is NOT uACR
- "BUN" without eGFR
- "creatinine" without an eGFR calculation in result (most modern labs auto-calculate; older results may not)
- Urine dipstick protein - NOT acceptable substitute for uACR

## Common documentation gaps

- eGFR done routinely (BMP) but uACR never ordered
- uACR ordered but specimen never collected / result never returned
- Lab done at outside facility; result not in structured Results
- Patient with CKD followed by nephrology - tests done but results not flowing back to PCP system

## Notes

- KED is one of the **easier-to-miss diabetes measures** because it requires **two distinct lab tests in the same MY** - PCP workflows often miss uACR
- ESRD and kidney transplant patients are excluded - they don't need screening
- eGFR alone OR uACR alone does NOT satisfy - both required
- ECDS direction: structured lab results via FHIR `Observation` with LOINC for eGFR and uACR

## See also

- [`GSD.md`](GSD.md)
- [`EED.md`](EED.md)
- [`BPD.md`](BPD.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
