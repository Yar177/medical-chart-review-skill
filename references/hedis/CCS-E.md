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

**False positives to filter**
- "hysterectomy" alone - may be supracervical; confirm "total" or "cervix removed"
- "cervical biopsy" alone is NOT screening - it's diagnostic; may or may not count
- "Pap recommended" / "due for Pap" - intent
- "patient declined Pap"

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
