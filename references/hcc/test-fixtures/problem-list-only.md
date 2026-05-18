# problem-list-only

## Synthetic note

```
Encounter date: 11/04/2025
Provider: Brooks, A. PA (Family Medicine)
Visit type: Suture removal

Subjective:
45 y/o M returns for suture removal from laceration repair 10 days ago (kitchen knife,
left index finger). Wound healing well. No fever, no drainage, no increased pain.

Problem List (chronic conditions):
- Chronic obstructive pulmonary disease (active)
- Type 2 diabetes mellitus, with peripheral neuropathy (active)
- Major depressive disorder, recurrent, moderate (active)
- Vitamin D deficiency (active)

Medications (active):
- Albuterol HFA PRN
- Tiotropium daily
- Metformin 1000 mg BID
- Sertraline 100 mg daily
- Vitamin D3 2000 IU daily

PE:
Left index finger: well-approximated wound, no erythema, no drainage. Sutures intact.

Procedure:
Sutures removed (4 nylon). Steri-strips applied. Wound care reviewed.

Assessment/Plan:
1. Status post laceration left index finger - healing well, sutures removed,
   patient to keep clean and dry, return if signs of infection.
```

## Expected extraction

```yaml
encounter:
  encounter_date: 2025-11-04
  setting: outpatient
  encounter_type: office
  signing_provider:
    type: pa
    on_whitelist: true

hccs_emitted:
  - icd10: Z48.02 or S61.x.D    # Encounter for removal of sutures / subsequent encounter of laceration
    hcc_v28: null
    assertion:
      temporality: current
    meat:
      categories: [evaluate, assess, treat]
      evidence: "wound exam; suture removal; wound care instructions"
    codable_for_this_dos: true

hccs_NOT_emitted:
  - icd10: J44.9           # COPD
    hcc_v28: <COPD HCC>
    reason: |
      COPD is in the problem list. No MEAT for COPD in this encounter:
      not assessed, not addressed in plan, ROS does not document
      respiratory symptoms or symptom-absence linked to COPD. The
      albuterol and tiotropium on the med list are reconciliation,
      not current-encounter Treat. Problem list alone is NEVER
      sufficient for HCC validation, per RADV standards.

  - icd10: E11.40          # T2DM with neuropathy
    hcc_v28: 18
    reason: |
      DM with neuropathy is in problem list. No MEAT in this encounter:
      not assessed, no A1c reviewed, no foot exam, no neuropathy
      symptom discussion. Metformin in med list is reconciliation only.

  - icd10: F33.1           # Major depressive disorder, recurrent, moderate
    hcc_v28: <MDD HCC where applicable>
    reason: |
      MDD in problem list. No MEAT in this encounter: not assessed,
      no PHQ score reviewed, no medication titration, no symptom check.
      Sertraline in med list is reconciliation only.

  - icd10: E55.9           # Vitamin D deficiency
    hcc_v28: null
    reason: "Not an HCC anyway, but same pattern: problem-list-only."
```

## Notes for reviewers

- This is the rule everyone gets wrong on their first HCC pipeline: a structured, parseable, easy-to-extract problem list is RIGHT THERE, and yet none of it is valid HCC evidence on its own.
- The encounter has one purpose (suture removal) and addresses one problem (the laceration). The chronic conditions exist for this patient but are not addressed at this DOS. That is fine clinically - this was not a chronic disease management visit.
- A pipeline that emits HCCs for COPD, DM, MDD from this encounter is wrong on multiple axes: (1) MEAT is absent, (2) problem-list-only is invalid for RADV. Either failure alone disqualifies; both together is a clear FP.
- This is one of the highest-volume sources of HCC over-coding in production pipelines because problem lists are easy to parse and feel authoritative. The discipline is to never let problem-list presence alone trigger a validated HCC.
- Active medication lists carry the same risk and require the same discipline. Albuterol + tiotropium are extremely suggestive of COPD, but suggestiveness is suspect-engine signal, not validate-engine evidence.
- A suspect engine looking at this chart should absolutely flag this member as likely having COPD, DM, MDD - the prior-year claims and medications support recapture targeting. But the suspect output should drive outreach to schedule a chronic-disease visit, not auto-submit HCCs from this encounter.

## Library / pipeline checks

- Problem-list section detection must mark all content as "problem-list source" so downstream MEAT-linkage logic can reject it as sole evidence.
- Active-medication list parsing must not produce Treat evidence without an explicit current-encounter linkage.
- Validate engine should produce an explicit "considered but not emitted" log entry for problem-list-only diagnoses, so reviewers can see what the pipeline saw and why it correctly stayed silent.
- Suspect engine should consume the same problem-list and med-list signals and produce member-level suspect outputs (different unit of analysis, different precision target).

## See also

- [`meat-gap.md`](meat-gap.md) - related: PMH + meds without current MEAT
- [`../extraction-patterns.md`](../extraction-patterns.md) - suspect / validate split
- [`../meat-criteria.md`](../meat-criteria.md) - MEAT contract
- [`../compliance-and-enforcement.md`](../compliance-and-enforcement.md) - why problem-list-only is a RADV failure pattern
