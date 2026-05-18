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

**False positives to filter**
- "mammogram recommended" / "due for mammogram" - intent, not done
- "patient declined mammogram" - not compliant
- "diagnostic mammogram for palpable mass" - may count depending on spec; ECDS focuses on screening intent
- "lumpectomy" alone is NOT mastectomy exclusion

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
