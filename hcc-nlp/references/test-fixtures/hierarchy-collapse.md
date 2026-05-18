# hierarchy-collapse

## Synthetic note

```
Encounter date: 06/10/2025
Provider: Nguyen, T. MD (Endocrinology)
Visit type: Diabetes follow-up

Subjective:
58 y/o M with T2DM x 12 years. Reports increasing numbness and tingling in both feet
over the last 6 months, worse at night. Adherent to metformin and recently started
semaglutide. No hypoglycemia. Last podiatry visit 3 months ago.

PE:
Feet: dry skin, mild fissures. Monofilament: reduced sensation bilateral plantar surfaces.
Pulses 2+ DP and PT bilateral.

Results:
- A1c 7.8% (today)
- eGFR 68 (today)
- Microalbumin/Cr 18 (today, normal)

Assessment/Plan:
1. Type 2 diabetes mellitus with peripheral neuropathy
   - A1c above target; will titrate semaglutide.
   - Continue metformin 1000 mg BID.
   - Diabetic foot care education reinforced; daily foot exam.
   - Referred to podiatry for ongoing foot surveillance.
2. Diabetic peripheral neuropathy
   - Started gabapentin 100 mg TID for symptomatic control.
3. Hyperlipidemia - on atorvastatin, LDL 78 last month, continue.
```

## Expected extraction

```yaml
encounter:
  encounter_date: 2025-06-10
  setting: outpatient
  encounter_type: office

diagnoses_extracted:
  - icd10: E11.40
    span: "Type 2 diabetes mellitus with peripheral neuropathy"
    section: assessment
    assertion:
      temporality: current
      hedging: confirmed
    meat:
      linked: true
      categories: [monitor, evaluate, assess, treat]
      evidence: "A1c 7.8%; will titrate semaglutide; continue metformin; foot care education; podiatry referral"
    codable_for_this_dos: true

  - icd10: E11.40         # combination code already captures the neuropathy
    span: "Diabetic peripheral neuropathy"
    section: assessment
    assertion:
      temporality: current
    meat:
      linked: true
      categories: [evaluate, treat]
      evidence: "reduced sensation; gabapentin 100 mg TID started"
    codable_for_this_dos: true
    notes: "Second mention of the same combination concept; do not double-emit."

post_extraction_hcc_candidates:
  - hcc_v28: 18       # Diabetes with Chronic Complications
    source_icd10: E11.40
  - hcc_v28: 19       # Diabetes without Complications - candidate from naive mapping
    source_icd10: E11.9 if pipeline mis-extracted base T2DM separately
    note: "Should NOT appear if pipeline correctly maps to E11.40 combination code"

after_hierarchy_application:
  hccs_emitted:
    - hcc_v28: 18
      reason: "Diabetes with chronic complications; trumps HCC 19"
  hccs_suppressed_by_hierarchy:
    - hcc_v28: 19
      reason: "Suppressed by HCC 18 in the diabetes family hierarchy"

failure_modes_this_fixture_catches:
  - "Pipeline emits both HCC 18 and HCC 19, inflating RAF and failing audit."
  - "Pipeline emits E11.9 + G62.9 instead of the combination code E11.40, mapping to wrong HCC."
  - "Pipeline double-counts diabetes mentions across the two A&P bullets."
```

## Notes for reviewers

- The diabetes hierarchy is the most common hierarchy collision in real data. HCC 17 > HCC 18 > HCC 19. Members with complicated diabetes should produce HCC 18 (or 17 if acute) only.
- The right ICD-10 code here is the combination code E11.40 ("Type 2 diabetes mellitus with diabetic neuropathy"), not E11.9 + G62.9. Combination codes are common in diabetes and map to the higher-severity HCC. Pipelines that decompose combination concepts into separate codes often lose this specificity.
- Two A&P bullets ("Type 2 diabetes mellitus with peripheral neuropathy" and "Diabetic peripheral neuropathy") describe the same combination concept and should NOT double-count.
- Hierarchy application is a post-roll-up step. The extractor should emit both HCC 18 and HCC 19 candidates if the underlying codes support both; the roll-up suppresses HCC 19. See [`../hierarchies.md`](../hierarchies.md).
- The hyperlipidemia documentation is MEAT-supported but is not an HCC in CMS-HCC V28; do not emit.

## Library / pipeline checks

- ICD-10 candidate generator should prefer combination codes when the text supports them.
- Hierarchy file (CMS-HCC V28) must be loaded and applied after extraction.
- Evaluation harness should compare predictions to gold AFTER hierarchy application to both sides.
- Audit log should preserve the suppressed HCC 19 candidate with the reason ("trumped by HCC 18 in family hierarchy").

## See also

- [`../hierarchies.md`](../hierarchies.md) - hierarchy rule
- [`../cards/hcc-18-diabetes-with-complications.md`](../cards/hcc-18-diabetes-with-complications.md) - per-HCC card
