# OSW — Osteoporosis Screening in Older Women

**Reporting path:** Admin / ECDS
**Population focus:** Women 65-75

> **Distinct from OMW** (covered in the sibling `medical-chart-review` skill's `references/quality-measures.md`)**:** OSW is **screening** in asymptomatic older women. OMW (Osteoporosis Management in Women who had a Fracture) is **secondary prevention** after a fracture. Don't conflate them.

## Denominator

- Women 65-75 as of end of MY
- Continuous enrollment through MY (with allowed enrollment gap per spec)

## Numerator

- Documented **bone density / osteoporosis screening** on or before end of MY (typically lifetime look-back through MY - verify current spec)
- Acceptable evidence:
  - DXA (dual-energy X-ray absorptiometry) bone density scan
  - Other accepted osteoporosis screening modality per current spec
  - Existing diagnosis of osteoporosis or osteopenia (implies prior screening occurred)
  - Active treatment with osteoporosis medication (implies prior diagnosis and screening)

## Exclusions

- Hospice
- Palliative care
- Advanced illness / frailty exclusion for members 66+
- Per current spec - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - lifetime/look-back through end of MY |
| **Compliance window** | Lifetime through end of MY (verify current spec - some accept 2-year look-back, some lifetime) |
| **Date types that COUNT** | DXA scan date, date osteoporosis/osteopenia diagnosis was first established, date osteoporosis medication was prescribed (implies prior diagnosis) |
| **Date types that do NOT count** | DXA referral date (without scan completed), "DXA recommended" date, "patient declined DXA" date, spine X-ray with incidental "osteopenia" comment (not DXA), calcium/vitamin D supplementation date (does NOT imply prior screening) |
| **"Most recent" disambiguation** | Most recent DXA, or earliest qualifying diagnosis/medication on file by end of MY |
| **Look-back / look-forward** | Lifetime through end of MY typically; verify spec |

**Common date confusions for this measure**

- DXA done at outside imaging center years ago; scanned report exists - the scan date counts if the report is on file
- Osteoporosis on problem list with no DXA in EHR - the diagnosis on file may satisfy (implies prior screening); spec-dependent
- Bisphosphonate use for non-osteoporosis indication (Paget's, malignancy hypercalcemia) - does NOT imply osteoporosis screening; the prescription date does NOT count
- DXA done at age 64, member now 67 - lifetime evidence typically counts; verify spec
- Spine X-ray with incidental "osteopenia" comment - NOT a DXA; do NOT use that date
- DXA scheduled but not completed - referral date does NOT count

## NLP signal phrases

**Section hints:** Results (imaging, DXA reports), Past Medical Hx, Problem List, Medications, Plan, scanned outside DXA reports

**Positive signals - screening completed**
- "DXA scan" / "DEXA scan" / "bone density scan" / "bone densitometry"
- "BMD: T-score ___" / "T-score -1.5 at L-spine"
- "Z-score ___"
- "FRAX score: ___" (often calculated with DXA result)
- "osteoporosis screening completed"
- "bone density within normal limits"
- "osteopenia of femoral neck"
- "results: normal / osteopenia / osteoporosis"

**Positive signals - diagnosis implies prior screening**
- "osteoporosis" on problem list
- "osteopenia" on problem list
- "M81.0" / "M85.80" referenced

**Positive signals - active osteoporosis treatment**
- Bisphosphonates: "alendronate" / "Fosamax" / "risedronate" / "Actonel" / "ibandronate" / "Boniva" / "zoledronic acid" / "Reclast"
- "denosumab" / "Prolia"
- "teriparatide" / "Forteo"
- "abaloparatide" / "Tymlos"
- "romosozumab" / "Evenity"
- "raloxifene" / "Evista"
- "calcitonin" (less common now)

**Negative / exclusion signals**
- "hospice"
- "comfort care"
- "metastatic" / "advanced illness" / "frailty"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"DXA recommended" / "DXA referral pending"** - intent, not done
- **"Patient declined DXA"** - refusal; does NOT close measure
- **"Spine X-ray"** alone is NOT DXA - modality mismatch
- **"Calcium / vitamin D supplementation"** alone does NOT imply prior screening - commonly recommended for prevention without screening
- **"Fall risk discussion"** without bone density screen - unrelated measure context
- **Bisphosphonate use for non-osteoporosis indication** (Paget's, malignancy hypercalcemia) - lexical collision; verify context
- **"Hx of fractures"** in PMH - history; OSW is screening, not fracture-driven (that's OMW); do NOT conflate
- **"FH of osteoporosis"** - experiencer = family
- **"BMD low"** without numeric T-score - hedged
- **"Osteopenia per imaging"** without confirming modality is DXA - modality ambiguity
- **"Started Fosamax for prophylaxis"** without osteoporosis/osteopenia diagnosis - prophylaxis may not imply prior screening; verify
- **"DXA scheduled"** - future intent
- **"Patient on calcium"** alone - supplementation, not screening
- **"Bone health discussed"** - hedged; not screening

## Common documentation gaps

- DXA done at outside imaging center; report scanned but not in structured Results
- Osteoporosis on problem list but no DXA evidence in current EHR (assume historical)
- Patient on osteoporosis medication but diagnosis missing from problem list - link breaks
- DXA done > spec look-back period (verify current spec - some accept 2 years, some lifetime)
- Spine X-ray with incidental "osteopenia" comment misread as DXA evidence

## Notes

- **OSW is newer than OMW** - verify your reporting program includes OSW in the current MY
- Lifetime evidence typically counts (a DXA at age 64 still satisfies for a 67-year-old member - verify spec)
- USPSTF recommends bone density screening for women 65+ - OSW aligns with that guideline
- ECDS direction: structured DXA result via FHIR `DiagnosticReport` / `Observation` with LOINC for T-score

## See also

- OMW (Osteoporosis Management in Women who had a Fracture) - see the sibling `medical-chart-review` skill's `references/quality-measures.md`
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- USPSTF osteoporosis screening recommendation
- NCQA HEDIS Technical Specifications, Volume 2
