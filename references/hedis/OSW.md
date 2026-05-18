# OSW — Osteoporosis Screening in Older Women

**Reporting path:** Admin / ECDS
**Population focus:** Women 65-75

> **Distinct from [OMW](../quality-measures.md):** OSW is **screening** in asymptomatic older women. OMW (Osteoporosis Management in Women who had a Fracture) is **secondary prevention** after a fracture. Don't conflate them.

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

**False positives to filter**
- "DXA recommended" / "DXA referral pending" - intent, not done
- "patient declined DXA"
- "spine X-ray" alone is NOT DXA
- "calcium / vitamin D supplementation" alone does NOT imply prior screening (commonly recommended for prevention without screening)
- "fall risk discussion" without bone density screen
- Bisphosphonate use for **non-osteoporosis indication** (e.g., Paget disease, malignancy-related hypercalcemia) - verify context

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

- OMW (Osteoporosis Management in Women who had a Fracture) - see [`../quality-measures.md`](../quality-measures.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- USPSTF osteoporosis screening recommendation
- NCQA HEDIS Technical Specifications, Volume 2
