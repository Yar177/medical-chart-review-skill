# meat-gap

## Synthetic note

```
Encounter date: 09/12/2025
Provider: Lee, K. MD (Family Medicine)
Visit type: Acute visit - sinus congestion

Subjective:
54 y/o F here with 5 days of nasal congestion, sinus pressure, sore throat.
No fever. No SOB at rest. Reports recent travel.

PMH:
- Congestive heart failure, EF 35% on echo 2023
- Type 2 diabetes mellitus
- Hypertension
- Obesity

Medications (active):
- Furosemide 40 mg daily
- Metoprolol succinate 50 mg daily
- Lisinopril 10 mg daily
- Metformin 1000 mg BID
- Atorvastatin 40 mg

Allergies: NKDA

ROS:
Constitutional: no fever, no chills, mild fatigue
HEENT: nasal congestion, post-nasal drip, mild throat pain
Cardiovascular: no chest pain, no orthopnea, no PND, no leg swelling
Respiratory: no SOB at rest, no cough
GI: appetite ok

PE:
Vitals: T 98.6, HR 78, BP 128/76, SpO2 98% RA, weight 195 lb
HEENT: nasal mucosa erythematous, mild post-nasal drainage, throat mildly erythematous
Lungs: clear bilateral
Heart: regular, no murmur

Assessment/Plan:
1. Acute viral upper respiratory infection
   - Symptomatic management: saline nasal spray, OTC analgesics, fluids
   - No antibiotics indicated
   - Return if fever, worsening SOB, or symptoms persist > 10 days
```

## Expected extraction

```yaml
encounter:
  encounter_date: 2025-09-12
  setting: outpatient
  encounter_type: office

hccs_emitted:
  - icd10: J06.9          # Acute upper respiratory infection, unspecified
    hcc_v28: null          # Not an HCC
    assertion:
      temporality: current
    meat:
      categories: [evaluate, assess, treat]
      evidence: "PE findings; symptomatic management plan"
    codable_for_this_dos: true

hccs_NOT_emitted:
  - icd10: I50.32         # Chronic diastolic CHF (or similar specificity)
    hcc_v28: <CHF HCC>
    reason: |
      CHF is in the PMH and the patient is on furosemide and metoprolol (medications consistent
      with CHF management). However, this encounter has NO MEAT for CHF: the A&P does not address
      CHF, the encounter is for URI, the CV ROS is negative, the lung exam is clear. Furosemide
      on the active med list is a chronic medication, not Treat for THIS DOS.
      A different encounter in the year (e.g., a CHF follow-up) is the right place to validate.
      This encounter is invalid for CHF HCC despite the PMH presence.

  - icd10: E11.9          # T2DM
    hcc_v28: <DM HCC>
    reason: |
      DM in PMH, metformin on med list, but NO MEAT in this encounter. A1c not reviewed,
      diabetes not assessed, no plan change. Invalid for DM HCC for this DOS.

  - icd10: I10            # HTN
    hcc_v28: null
    reason: "Not an HCC, but documentation pattern is the same: PMH only, no MEAT."

  - icd10: E66.9          # Obesity unspecified
    hcc_v28: null         # Morbid obesity (E66.01) might be an HCC if BMI >= 35 with comorbidity or BMI >= 40
    reason: |
      BMI not documented in this encounter (weight only). No provider diagnosis of obesity in this DOS.
      Even if PMH says "obesity," the encounter does not establish current MEAT or BMI; not codable here.
```

## Notes for reviewers

- This is the most common silent failure mode in real-data HCC extraction. The chart MENTIONS the chronic conditions (in PMH and active med list); a naive pipeline emits HCCs for all of them. None of them have MEAT in THIS encounter.
- The encounter is legitimate (an acute URI visit) but it does not happen to address the chronic conditions. That is fine - other encounters in the year do. This encounter just is not the one.
- Active medications are NOT MEAT on their own. They are reconciliation. To count as Treat, the provider must address the medication in the context of the diagnosis in the current note (continuation rationale, dose change, side-effect discussion, etc.).
- A pipeline that emits CHF, DM, HTN, obesity HCCs from this encounter is over-coding. At scale, this pattern is the main driver of RADV findings.
- The right output is one diagnosis (URI) with strong MEAT, and explicit non-emission of the chronic HCCs with logged reasons. The audit log should let a reviewer see "considered CHF, no MEAT in this DOS, did not emit."

## Library / pipeline checks

- MEAT linkage classifier should require positive evidence of M / E / A / T for each emitted HCC, scoped to this encounter.
- Active medication list should not count as Treat without explicit current-encounter linkage to a diagnosis.
- PMH-section content should NOT be sufficient on its own; pipeline must look for current-encounter MEAT for each PMH item considered.
- ROS negative-finding patterns ("no orthopnea, no leg swelling") could in principle support Monitor if explicitly linked to CHF in the note; here the link is absent, so it does not count.

## See also

- [`../meat-criteria.md`](../meat-criteria.md) - MEAT contract
- [`../extraction-patterns.md`](../extraction-patterns.md) - validate-engine architecture
- [`../compliance-and-enforcement.md`](../compliance-and-enforcement.md) - why this pattern drives RADV findings
- [`problem-list-only.md`](problem-list-only.md) - related but distinct failure mode (problem-list-only diagnoses)
