# DBM — Documented Assessment After Mammogram

**Reporting path:** Verify with program source (admin claims, hybrid, or ECDS depending on owner)
**Population focus:** Members with a recent mammogram (typically aligns with BCS-E age band - verify)
**Domain:** Cancer screening / closed-loop screening follow-up

> **Spec verification required:** "DBM - Documented Assessment After Mammogram" is **not a standard NCQA HEDIS measure I can independently verify** under that exact code/name. It may originate from a payer-internal quality program, a state Medicaid program, a newer NCQA pilot, or an aggregator's custom measure set. The content below is built from the literal measure name plus reasonable clinical inference about closed-loop screening follow-up. **Validate against the originating program's technical specification before using for reporting.**

## Intent (inferred from measure name)

The measure appears to address the **closed-loop screening problem**: a mammogram is completed, but is there documented clinical assessment / action taken in response to the result? This addresses well-documented gaps where:
- Normal results are filed without provider review or patient notification
- Abnormal results (BI-RADS 0, 4, 5) lack documented follow-up plans
- BI-RADS 3 (probably benign, short-interval follow-up) recommendations are not tracked

This is distinct from [BCS-E](BCS-E.md), which measures **whether** the mammogram occurred. DBM measures **what happened after**.

## Denominator (likely structure - verify)

- Members who had a screening or diagnostic mammogram during the measurement window
- Age band probably aligns with the underlying screening population (BCS-E range 50-74; some programs broader, e.g., 40-74)
- Continuous enrollment through the assessment window (likely 30-90 days after mammogram - verify)

## Numerator (likely structure - verify)

Documented clinical assessment / action after the mammogram result within the spec-defined window. Likely-acceptable evidence:

- Documented review of the mammogram result by the ordering provider or PCP
- Documented communication of the result to the patient (normal or abnormal)
- For **abnormal results (BI-RADS 0, 4, 5)**:
  - Documented follow-up plan: diagnostic mammogram, ultrasound, MRI, biopsy, surgical referral
  - Documented referral to breast specialist / surgical oncology
- For **BI-RADS 3 (probably benign)**:
  - Documented short-interval follow-up plan (typically 6-month follow-up imaging)
- For **BI-RADS 1 or 2 (normal / benign)**:
  - Documented review and patient notification

## Exclusions (likely - verify)

- Hospice
- Death within assessment window
- Mammogram not yet resulted at end of window
- Per program spec - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

> **Spec verification required** for the exact window length and event-definition; values below are inferred from the closed-loop-screening intent and standard radiology practice.

| Field | Value |
|---|---|
| **Anchor event** | Index mammogram result (often abnormal: BI-RADS 0, 3, 4, 5) |
| **Compliance window** | Documented assessment / follow-up action within the spec-defined window after the index mammogram (commonly 30-90 days; **verify**) |
| **Date types that COUNT** | Date of follow-up imaging procedure (diagnostic mammogram, US, MRI); biopsy procedure date; documented result-review and patient-notification date; specialist consult date |
| **Date types that do NOT count** | Imaging report-signing date when delayed from procedure (use procedure date); referral order date alone; "will discuss at next visit" without a follow-up date |
| **"Most recent" disambiguation** | First qualifying follow-up action within window closes the measure |
| **Look-back / look-forward** | None look-back; look-forward = the post-mammogram window |

**Common date confusions for this measure**

- Diagnostic mammogram procedure date vs report-signing date - use procedure date
- Biopsy scheduled date vs biopsy completion date - completion date is the evidence date
- Patient-notification via portal message - the message-sent date is the documentation date
- BI-RADS 3 short-interval follow-up imaging in 6 months - the follow-up imaging date counts when it occurs, not the recommendation date

## NLP signal phrases

**Section hints:** Results (imaging, pathology), Plan, problem list, Patient Communication / Letters, scanned outside reports, message inbox / result-review documentation

**Positive signals - result review and assessment**
- "mammogram result reviewed"
- "results reviewed with patient"
- "patient notified of normal mammogram"
- "letter sent regarding normal mammogram results"
- "BI-RADS 1 - return to routine annual screening"
- "BI-RADS 2 - benign, routine screening interval"

**Positive signals - abnormal result follow-up**
- "BI-RADS 0 - additional imaging needed"
- "BI-RADS 3 - 6-month short-interval follow-up imaging recommended"
- "BI-RADS 4 - biopsy recommended"
- "BI-RADS 5 - highly suggestive of malignancy, biopsy"
- "diagnostic mammogram ordered" / "additional views"
- "breast ultrasound ordered"
- "breast MRI ordered"
- "core needle biopsy" / "stereotactic biopsy" / "ultrasound-guided biopsy"
- "referred to breast surgeon" / "breast specialist referral"
- "referred to surgical oncology"
- "patient educated on need for follow-up imaging"

**Positive signals - documentation of patient communication**
- "results communicated via MyChart"
- "patient called regarding results"
- "result letter sent on [date]"
- "patient acknowledged understanding of follow-up plan"

**Negative / exclusion signals**
- "hospice"
- "patient declined further evaluation despite abnormal findings"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Recommended diagnostic mammogram" / "diagnostic mammogram ordered" / "biopsy recommended"** - temporality: future intent / order; not the follow-up action itself
- **"Will discuss results at next visit"** without a documented follow-up tracking - vague future plan
- **"Results: normal"** pasted from prior visit (copy-forward) without provider review attestation - not evidence of THIS-event review
- **"BI-RADS 4, awaiting patient response"** - acknowledged but action not completed
- **"Patient declined further evaluation despite abnormal findings"** - refusal documented; may not close measure but documents the chain
- **"Referral made"** without documentation of why or link to the mammogram result - cannot tie to the index event
- **"Mammogram result reviewed"** with no patient-notification or plan documentation (boilerplate) - thin evidence; assertion = hedged on whether substantive review occurred
- **"FH of breast cancer"** - experiencer = family; relevant context, not the follow-up action
- **"Hx of breast biopsy"** - historical; does not satisfy this-event follow-up
- **"BI-RADS 1 / BI-RADS 2 - return to routine screening"** - normal result; "return to routine" IS the documented assessment for normal
- **"Lost to follow-up"** - documented gap; does not close measure

## Common documentation gaps

- Normal mammogram result auto-filed into Results without provider review attestation
- Abnormal result acknowledged in inbox but no documented Plan entry
- Follow-up imaging ordered but not linked back to the index mammogram
- Patient communication occurred verbally / via portal but not documented in the chart
- BI-RADS 3 short-interval follow-up not tracked - patient lost to follow-up
- Outside mammogram (different facility) result reviewed but PCP documentation thin

## Notes

- **The closed-loop screening problem** this measure addresses is well-documented in patient safety literature: abnormal results that go un-actioned are a recurring source of diagnostic-delay harm
- Related but distinct measures:
  - [BCS-E](BCS-E.md) — Breast Cancer Screening (was the mammogram done?)
  - Possible adjacent measures in some programs: "Diagnostic Mammogram Follow-Up", "Time to Biopsy After Abnormal Mammogram"
- For NLP extraction:
  - **Link the mammogram result to the follow-up action** by date proximity and patient identifier
  - Distinguish **routine recommendation** ("return to routine screening") from **active follow-up plan** ("biopsy scheduled")
  - **Patient communication is hard to extract** - may live in portal messages, telephone encounters, or scanned letters
- ECDS direction (if applicable): structured `DiagnosticReport` for mammogram + linked `CarePlan` / `ServiceRequest` for follow-up

## See also

- [`BCS-E.md`](BCS-E.md) — the underlying screening measure
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- [`../red-flags.md`](../red-flags.md) — closed-loop / diagnostic delay safety patterns
- **Program-specific technical specification** for the authoritative DBM definition (not yet linked - please add)
