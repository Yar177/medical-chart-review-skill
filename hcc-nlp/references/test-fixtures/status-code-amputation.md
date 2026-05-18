# status-code-amputation

## Synthetic note

```
Encounter date: 03/03/2025
Provider: Garcia, M. NP (Internal Medicine)
Visit type: Routine follow-up

Subjective:
72 y/o M with T2DM, HTN, and prior right BKA (2019) following non-healing diabetic
foot ulcer. Ambulates with prosthesis; reports good fit, no skin breakdown. No falls.
Lives independently with home aide 3x/week.

PSH:
- Right below-knee amputation 03/2019

PE:
General: well-appearing, ambulatory with right BK prosthesis
Extremities: residual limb intact, no erythema, no breakdown, sock fit appropriate.
Left foot: protective sensation intact, no ulceration, pulses 2+.

Assessment/Plan:
1. Status post right BKA - residual limb healthy, prosthesis well fitted, continues
   home PT for gait. Reinforced daily inspection of left foot and stump.
2. Type 2 diabetes mellitus - A1c 7.2 last month, continue metformin.
3. HTN - BP 132/80, continue amlodipine.
```

## Expected extraction

```yaml
encounter:
  encounter_date: 2025-03-03
  setting: outpatient
  encounter_type: office
  signing_provider:
    type: np
    on_whitelist: true

hccs_emitted:
  - icd10: Z89.511         # Acquired absence of right lower leg below knee
    hcc_v28: <amputation status HCC; verify number against current crosswalk>
    assertion:
      temporality: current
      status_modifier: s_p_amputation
      experiencer: patient
    meat:
      linked: true
      categories: [monitor, evaluate, assess]
      evidence: "residual limb intact, no erythema, no breakdown; prosthesis well fitted; home PT"
    codable_for_this_dos: true
    annual_recapture_required: true
    notes: "Amputation status is permanent but the HCC requires annual recapture. This encounter satisfies recapture for service year 2025."

  - icd10: E11.9 or appropriate specificity
    hcc_v28: <DM HCC; HCC 19 unless complications documented>
    assertion:
      temporality: current
    meat:
      categories: [evaluate, treat]
      evidence: "A1c 7.2 last month; continue metformin"
    codable_for_this_dos: true
    notes: |
      DM here is documented as uncomplicated in this encounter. The BKA was related to
      a prior diabetic foot ulcer (per HPI) which would have justified HCC 18 historically,
      but unless current-encounter documentation supports an active complication, this
      encounter supports HCC 19 only. Other encounters in the year may support HCC 18.

hccs_NOT_emitted:
  - icd10: L97.5xx           # Non-pressure ulcer of foot
    reason: "Original ulcer healed; amputation status replaced it. Coding active ulcer is incorrect."
  - icd10: S88.119A          # Traumatic amputation, initial encounter
    reason: "This is not a traumatic amputation; it is a surgical (diabetic) amputation, well in the past. The Z89.x status code is correct, not an active injury code."
```

## Notes for reviewers

- Z89.x (acquired absence of limb) IS an HCC in CMS-HCC. It requires annual recapture even though the amputation is permanent. NLP pipelines that classify all Z-codes as non-HCC will silently lose this HCC every year.
- The MEAT for a status code is the documentation that confirms the status at this DOS (PE finding of the residual limb, PSH mention with current relevance, assessment block addressing the status). A bare entry in PSH with no current-encounter acknowledgment is weak; this fixture has explicit current-encounter PE and A&P, which is strong.
- Do NOT also emit the original wound or injury code. The status code replaces the active code once healed and amputation has occurred.
- The diabetes documentation here is "uncomplicated" at this encounter (no complications mentioned in this DOS). Even though the patient's history shows complications (the foot ulcer leading to BKA), the HCC for THIS DOS is HCC 19, not HCC 18. The year-level roll-up may have HCC 18 from another encounter; that does NOT retroactively apply to this DOS. See [`../meat-criteria.md`](../meat-criteria.md).
- Provider signer is NP, which is on the acceptable whitelist for HCC documentation. Pipeline should verify.

## Library / pipeline checks

- Status-code extractor should emit Z89.511 from "right BKA" + "right below-knee amputation" + "residual limb."
- Status-code → HCC mapper should know Z89.x is an HCC and requires annual recapture.
- Recapture tracking should flag this encounter as satisfying the recapture for service year 2025.
- Mutual-exclusion logic should suppress active wound / ulcer codes when amputation status with healed stump is documented.

## See also

- [`../negation-and-assertion.md`](../negation-and-assertion.md) - status modifier handling
- [`../date-of-service.md`](../date-of-service.md) - annual recapture and calendar reset
- [`../meat-criteria.md`](../meat-criteria.md) - MEAT for status codes
