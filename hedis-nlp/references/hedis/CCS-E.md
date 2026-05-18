# CCS-E — Cervical Cancer Screening

**Reporting path:** ECDS (CCS-E); admin/hybrid variant historically called CCS
**Population focus:** Women 21-64

## Denominator

- Women 21-64 as of end of MY
- Continuous enrollment through MY

## Numerator (any of the following)

- **Ages 21-64:** Cervical cytology (Pap) within the past **3 years**
- **Ages 30-64:** Cytology + high-risk HPV co-test within the past **5 years**
- **Ages 30-64:** Primary high-risk HPV testing within the past **5 years**

(Verify exact look-back windows in current MY spec - may shift by a year.)

## Exclusions

- Hysterectomy with no residual cervix at any time on or before end of MY
- Total / complete hysterectomy
- Congenital absence of cervix
- Hospice
- Palliative care

> "Hysterectomy" alone (without "total" / "no residual cervix") does NOT qualify - supracervical hysterectomy leaves the cervix.

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - rolling look-back by age band and modality |
| **Compliance window** | Pap cytology within 3 years (ages 21-64); OR Pap+hrHPV co-test or primary hrHPV within 5 years (ages 30-64) |
| **Date types that COUNT** | Specimen collection date (cytology and/or HPV) |
| **Date types that do NOT count** | Result-posting date alone, order date, prior cervical biopsy date (biopsy is diagnostic, not screening), patient-reported date without provider documentation |
| **"Most recent" disambiguation** | Any qualifying specimen in the applicable look-back satisfies |
| **Look-back / look-forward** | 3 years (cytology) or 5 years (co-test / primary hrHPV); no look-forward |

**Common date confusions for this measure**

- Pap done at OB-GYN outside plan network - capture specimen date from outside report, not the EHR import date
- Co-test result: cytology and HPV often share a specimen date but may have separate posting dates - use the (shared) specimen date
- Patient reports Pap "last year" without documentation - cannot anchor a date; not directly scoreable
- Reflex HPV after ASC-US - diagnostic workup; may not satisfy screening look-back on its own

## NLP signal phrases

**Section hints:** Results (cytology, pathology), Past Surgical Hx, problem list, Plan, scanned outside pathology reports

**Positive signals**
- "Pap smear" / "Pap test" / "cervical cytology"
- "ThinPrep" / "liquid-based cytology"
- "HPV test" / "hrHPV" / "high-risk HPV"
- "co-test" / "Pap and HPV"
- "primary HPV screening"
- Cytology result phrases: "NILM" / "negative for intraepithelial lesion or malignancy" / "ASC-US" / "LSIL"

**Negative / exclusion signals**
- "total hysterectomy" / "TAH" / "TAH-BSO"
- "hysterectomy with cervix removed"
- "no cervix" / "absent cervix" / "s/p hysterectomy with no residual cervix"
- "congenital absence of uterus / cervix"
- "hospice"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Pap negative" / "NILM" / "HPV negative"** - negative = normal result = POSITIVE evidence; do NOT let NegEx flip it
- **"Hysterectomy"** alone without "total" / "complete" / "cervix removed" - may be supracervical; exclusion not confirmed
- **"Cervical biopsy"** alone - diagnostic, not screening; may not satisfy on its own
- **"Pap recommended" / "due for Pap" / "will schedule Pap next visit"** - temporality: future intent
- **"Patient declined Pap"** - refusal; does NOT close measure
- **"Reflex HPV done after ASC-US"** - diagnostic workup; check spec for screening-look-back qualification
- **"FH of cervical cancer"** - experiencer = family
- **"Pap done elsewhere"** without date - hedged; cannot place in look-back
- **"NILM, recommend routine screening interval"** - the NILM result IS evidence; the routine-interval phrase is just guidance
- **"Cervical cytology unsatisfactory"** - inadequate sample; spec-dependent whether it counts
- **"S/p hysterectomy"** without cervix-status detail - exclusion unclear; flag for review

## Common documentation gaps

- Pap done at OB-GYN outside of plan network; results not in EHR
- Hysterectomy in surgical history without "total" qualifier - exclusion can't be confirmed
- HPV test ordered but result not posted to structured Results
- Outside cytology report scanned but not parsed into Results

## Notes

- The 30-64 age band has multiple pathways (cytology alone q3y, co-test q5y, primary HPV q5y) - the patient closes the gap by satisfying any one
- "Reflex HPV" after ASC-US is diagnostic; it may not satisfy screening alone - check current spec
- ECDS direction: structured cytology and HPV results via FHIR `Observation` / `DiagnosticReport`

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
