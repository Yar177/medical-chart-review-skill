# COL-E — Colorectal Cancer Screening

**Reporting path:** ECDS (COL-E); admin/hybrid variant historically called COL
**Population focus:** Adults 45-75 (lowered from 50-75 in recent MY - verify)

## Denominator

- Members 45-75 as of end of MY
- Continuous enrollment through MY

## Numerator (any one of the following look-backs)

- **FOBT / FIT (fecal blood test):** during MY (annual)
- **FIT-DNA (Cologuard):** during MY or 2 years prior (every 3 years)
- **Flexible sigmoidoscopy:** during MY or 4 years prior (every 5 years)
- **CT colonography:** during MY or 4 years prior (every 5 years)
- **Colonoscopy:** during MY or 9 years prior (every 10 years)

## Exclusions

- Colorectal cancer at any time on or before end of MY
- Total colectomy at any time on or before end of MY
- Hospice
- Advanced illness / frailty exclusion for members 66+
- Palliative care

## NLP signal phrases

**Section hints:** Results (endoscopy, pathology, imaging), Past Surgical Hx, problem list, Plan, scanned outside procedure reports

**Positive signals**
- "colonoscopy" / "screening colonoscopy"
- "sigmoidoscopy" / "flexible sigmoidoscopy" / "flex sig"
- "FIT" / "fecal immunochemical test" / "FOBT" / "guaiac"
- "FIT-DNA" / "Cologuard" / "stool DNA test"
- "CT colonography" / "virtual colonoscopy"
- Endoscopy findings: "to cecum" / "ileocecal valve visualized" / "complete colonoscopy"
- "polypectomy" / "biopsy" (implies colonoscopy occurred)

**Negative / exclusion signals**
- "colon cancer" / "colorectal cancer" / "rectal cancer" / "history of CRC"
- "total colectomy" / "subtotal colectomy with no residual colon"
- "ostomy for CRC"
- "hospice" / "comfort care"
- "metastatic"

**False positives to filter**
- "colonoscopy recommended" / "referred for colonoscopy" - intent
- "incomplete colonoscopy" without rescheduled completion - may not count
- "diagnostic colonoscopy for GI bleed" - typically still counts as evidence of completion, verify spec
- "patient declined colonoscopy"
- "partial colectomy" alone (segmental) does NOT trigger exclusion - total colectomy required

## Common documentation gaps

- FIT kit sent home, returned, processed at outside lab - result never reaches EHR
- Cologuard ordered through pharmacy benefit; result in lab data but not endoscopy-tab
- Colonoscopy done years ago at another health system; report scanned but not in structured Results
- Surgical history says "colon resection" without total colectomy detail - exclusion ambiguous

## Notes

- Age lower bound changed from 50 to 45 (USPSTF 2021 guideline; HEDIS aligned in subsequent MY) - verify current spec
- Multiple modalities at different intervals - the patient closes the gap by satisfying any one within its lookback
- ECDS direction: structured procedure / observation via FHIR

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
- USPSTF colorectal cancer screening guideline
