# BCS-E — Breast Cancer Screening

**Reporting path:** ECDS (BCS-E); admin variant historically called BCS
**Population focus:** Women 50-74
**Stars:** Often star-rated in Medicare Advantage

## Denominator

- Women aged 50-74 as of end of MY (verify current spec - some sub-bands)
- Continuously enrolled through MY (with allowed gap per spec)
- Qualifying outpatient encounter requirements may apply for ECDS variant

## Numerator

- Mammogram (any modality: 2D, tomosynthesis, MRI in qualifying contexts) within the **27-month look-back** ending on the last day of MY
  - Look-back covers MY plus prior year - so a mammogram done early in the prior year still counts

## Exclusions

- Bilateral mastectomy at any time on or before end of MY (or two unilateral mastectomies)
- Hospice during MY
- Advanced illness / frailty exclusion for members 66+
- Palliative care during MY

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - rolling look-back |
| **Compliance window** | Mammogram within the **27-month look-back** ending on the last day of MY (covers MY + prior year) |
| **Date types that COUNT** | Mammogram procedure date |
| **Date types that do NOT count** | Order date, scheduled/future date, imaging report date when delayed from procedure (use procedure date), self-reported mammogram without dated documentation |
| **"Most recent" disambiguation** | Any qualifying mammogram in the 27-month window satisfies |
| **Look-back / look-forward** | 27 months look-back from end of MY; no look-forward |

**Common date confusions for this measure**

- Mobile screening unit mammogram - the on-site exam date is the evidence date; receipt-by-EHR date can lag months
- Outside-imaging report scanned in current MY for an exam done 2 years ago - use the exam date; falls outside 27-month window if too old
- BI-RADS 0 (additional imaging needed) - the screening date still counts as evidence the screening occurred; do not require BI-RADS resolution date
- Patient-reported "had mammogram last year" without a dated outside report - cannot anchor a date; not directly scoreable

## NLP signal phrases

**Section hints:** Results (imaging), Past Surgical Hx, Plan, problem list, scanned outside imaging reports

**Positive signals**
- "mammogram" / "mammography"
- "screening mammogram bilateral"
- "tomosynthesis" / "3D mammogram" / "DBT"
- "breast MRI" (only counts in some contexts - high-risk screening)
- "BI-RADS 1" / "BI-RADS 2" / "BI-RADS 0 - additional imaging" (any BI-RADS implies imaging occurred)
- "results sent to patient: normal mammogram"

**Negative / exclusion signals**
- "bilateral mastectomy" / "s/p bilateral mastectomy" / "history of bilateral mastectomy"
- "right mastectomy" + "left mastectomy" (two unilaterals satisfy exclusion)
- "hospice"
- "metastatic cancer" / "stage IV" (may trigger advanced illness exclusion at 66+)

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Negative mammogram" / "mammogram negative" / "Pap negative"-style phrasing** - in screening, "negative" = normal result = POSITIVE evidence; do NOT let NegEx flip it
- **"Mammogram recommended" / "due for mammogram" / "referred for screening"** - temporality: future intent; not evidence of completion
- **"Patient declined mammogram"** - refusal; does NOT close measure
- **"Diagnostic mammogram for palpable mass"** - spec-dependent whether it counts; ECDS focuses on screening intent
- **"Lumpectomy" alone** - lumpectomy is NOT mastectomy; does not trigger exclusion
- **"Hx of breast cancer"** without bilateral mastectomy - history alone does not exclude; the surgical procedure does
- **"FH of breast cancer in mother"** - experiencer = family; relevant for risk stratification, not patient exclusion or numerator
- **"Mammogram done elsewhere"** without date - hedged; cannot place in 27-month window
- **"BI-RADS 0" / "additional imaging needed"** - the screening DID occur; this is still evidence of completion
- **"Patient at average risk, screening discussed"** - discussion is not screening; need actual mammogram

## Common documentation gaps

- Outside imaging reports scanned but not entered as structured Results
- Mammogram done at mobile screening unit; report never reached EHR
- Mastectomy in surgical history but not in problem list (so exclusion isn't triggered)
- Member moved within 27-month window; prior plan's mammogram not in current data

## Notes

- BCS-E (ECDS) and historical BCS use the same clinical intent but different reporting mechanics
- Hybrid sampling may apply for non-ECDS variants
- Mastectomy date can be lifetime - prior medical history counts

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
