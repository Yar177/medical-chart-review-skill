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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - modality-specific rolling look-back |
| **Compliance window** | FIT/FOBT in MY (annual); FIT-DNA in MY or 2 yr prior; sigmoidoscopy or CT colonography in MY or 4 yr prior; colonoscopy in MY or 9 yr prior |
| **Date types that COUNT** | Procedure date (endoscopy, imaging); specimen collection date (stool tests) |
| **Date types that do NOT count** | Order date, kit-distribution date, result-posting date alone, incomplete procedure date (unless rescheduled completion counted), patient-reported date without documentation |
| **"Most recent" disambiguation** | Any qualifying procedure or test in the applicable look-back satisfies |
| **Look-back / look-forward** | Modality-specific (1, 3, 5, or 10 years); no look-forward |

**Common date confusions for this measure**

- FIT kit sent home and returned weeks later - the specimen collection date (or processing date) is the evidence date, not the kit-distribution date
- Cologuard ordered through pharmacy benefit - dispense date is NOT the specimen date; need the actual stool collection / result date
- Outside-system colonoscopy report scanned into current chart - the procedure date in the report is the evidence date, not the scan date
- Modality-specific window failures: colonoscopy 8 years ago is in window (10-yr); FIT 2 years ago is out (1-yr); applying wrong window is a common silent miss

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

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"FIT negative" / "Cologuard negative" / "colonoscopy: no polyps"** - negative = normal result = POSITIVE evidence; do NOT let NegEx flip it
- **"Colonoscopy recommended" / "referred for colonoscopy" / "Cologuard ordered"** - temporality: future intent or distribution; not completion
- **"Cologuard kit given to patient" / "FIT kit sent home"** - distribution, not completion; need result
- **"Patient declined colonoscopy"** - refusal; does NOT close measure
- **"Incomplete colonoscopy"** without rescheduled completion - may not count
- **"Partial colectomy" / "segmental colectomy" / "hemicolectomy"** alone - does NOT trigger total-colectomy exclusion
- **"Hx of colon polyps"** - implies prior colonoscopy but does not satisfy without dated procedure
- **"FH of colon cancer"** - experiencer = family; relevant for risk stratification (earlier screening), not patient evidence
- **"Diagnostic colonoscopy for GI bleed"** - typically still counts as evidence of completion; verify spec
- **"S/p ostomy" without CRC context** - ostomy alone does not trigger CRC exclusion
- **"Polyps removed" / "polypectomy"** - implies colonoscopy occurred; positive evidence if dated

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
