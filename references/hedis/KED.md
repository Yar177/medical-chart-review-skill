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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-only |
| **Compliance window** | BOTH eGFR AND uACR results within the same MY |
| **Date types that COUNT** | Lab specimen collection date for each test independently |
| **Date types that do NOT count** | Result-posting date alone, order date, prior-year test (does NOT extend), one component in MY with the other component in a different MY |
| **"Most recent" disambiguation** | Latest qualifying specimen for each component if multiple in MY |
| **Look-back / look-forward** | None - both components must be in the same MY |

**Common date confusions for this measure**

- eGFR routinely on BMP (in MY) + uACR last year - NOT compliant for current MY; both must be in MY
- uACR ordered late in MY, specimen actually collected next MY - does not count for current MY
- Nephrology labs outside the system - capture the specimen date from the outside report, not the import date
- One MY's eGFR carried forward into a current note - the evidence date is the original specimen date, which may be outside current MY

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

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"uACR ordered" / "microalbumin pending" / "will check renal function"** - temporality: future / order; not evidence
- **"Urinalysis: protein negative" or "UA dipstick"** - urine dipstick is NOT a uACR; do not substitute
- **"BUN/Cr normal"** without an explicit calculated eGFR - need the eGFR value; modern labs auto-calc, older or outside labs may not
- **"PMH: CKD stage 3"** - historical dx; does not satisfy this MY's screening
- **"Patient declined uACR" / "refused urine sample"** - refusal, not compliance
- **"Will recheck kidney function in 6 months"** - future
- **"Hx of microalbuminuria, on ACEi"** - historical, does not replace MY testing
- **"FH of ESRD" / "FH of polycystic kidney disease"** - experiencer = family
- **"Spot urine: 30 mg/g"** without explicit uACR labeling - ambiguous unit context; need explicit albumin-to-creatinine ratio
- **"Renal function stable" / "kidneys WNL"** - hedged; no numeric values; needs both eGFR and uACR with values
- **"Creatinine 0.9"** alone with no eGFR calculation - need the calculated eGFR result

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
