# history-of-trap

## Synthetic note

```
Encounter date: 04/22/2025
Provider: Patel, R. MD (Internal Medicine)
Visit type: Annual wellness visit

Subjective:
67 y/o F here for AWV. Feeling well. No new complaints. Walks 30 min daily.

PMH:
- Hypertension, well controlled on lisinopril
- History of breast cancer, dx 2011, s/p right mastectomy and adjuvant chemo,
  completed therapy 2012, NED on annual oncology follow-up
- Hypothyroidism, on levothyroxine

PSH:
- Right mastectomy 2011

Medications:
- Lisinopril 20 mg daily
- Levothyroxine 75 mcg daily
- Calcium + vitamin D

Family History:
- Mother: breast cancer dx age 72, deceased
- Father: prostate cancer

Assessment/Plan:
1. AWV - up to date on screenings except colonoscopy (due, scheduling today).
2. HTN - controlled, BP 124/78 today, continue lisinopril.
3. Hypothyroidism - TSH 2.1 last month, continue levothyroxine.
4. Personal history of breast cancer - 14 years out, no signs/symptoms of
   recurrence, continues annual surveillance with oncology, last visit 02/2025.
5. Family history of cancer - reviewed, no additional screening indicated.
```

## Expected extraction

```yaml
encounter:
  encounter_date: 2025-04-22
  setting: outpatient
  encounter_type: awv

hccs_emitted:
  - icd10: Z85.3
    hcc_v28: null          # Z85.x is generally NOT an HCC; replaces the active cancer code
    assertion:
      temporality: historical
      history_modifier: post_curative
      experiencer: patient
    meat:
      linked: true
      categories: [monitor, assess]
      evidence: "annual surveillance with oncology, last visit 02/2025; no signs/symptoms of recurrence"
    codable_for_this_dos: true
    notes: "Personal-history-of code; supports the chart but does not contribute to RAF."

  - icd10: Z80.3              # Family history of malignant neoplasm of breast
    hcc_v28: null
    assertion:
      experiencer: family
    codable_for_this_dos: true

  - icd10: I10                # Essential hypertension
    hcc_v28: null             # HTN alone is generally not an HCC in V28
    assertion:
      temporality: current
    meat:
      categories: [monitor, evaluate, treat]
      evidence: "BP 124/78 today; continue lisinopril"
    codable_for_this_dos: true

hccs_NOT_emitted:
  - icd10: C50.911            # Active malignant neoplasm of right breast
    reason: "Historical with curative resection 14 years ago, NED. Coding as active is the #1 RADV finding pattern."
  - icd10: C50.912            # Active left breast
    reason: "Not the patient; family history of mother. Experiencer = family."
  - icd10: C61                # Active prostate cancer
    reason: "Family history (father). Experiencer = family, and also wrong sex for this patient."
```

## Notes for reviewers

- This is the canonical history-of trap. A naive pipeline that searches for "breast cancer" will fire C50 (active malignant neoplasm) and HCC for active cancer. Wrong answer; #1 RADV finding category.
- The correct extraction is Z85.3 (personal history of breast cancer), which is NOT an HCC in CMS-HCC V28. The chart documents history accurately; risk-adjustment correctly does not pay for it because the cancer is resolved.
- The family-history block must not produce patient diagnoses. Mother's breast cancer and father's prostate cancer are NOT the patient's diagnoses.
- The PSH ("right mastectomy 2011") is corroborating evidence for the history-of assertion. A pipeline that sees "mastectomy" and infers active cancer is making a similar but distinct mistake.
- AWV setting deserves extra MEAT scrutiny per [`../date-of-service.md`](../date-of-service.md). In this fixture the AWV has explicit per-condition assessment text, so MEAT passes for the conditions that are actually current (HTN, hypothyroidism, the history-of code).
- Hypothyroidism (E03.x) is documented and MEAT-supported but is generally not an HCC; not emitted as an HCC even though it is a valid claims diagnosis.

## Library / pipeline checks

- ConText / medspaCy should mark "history of breast cancer" as historical with `historical=True`.
- Section detection should mark "PMH" content as historical-prior, with explicit current-activity check.
- Family-history detection should classify "Mother: breast cancer" and "Father: prostate cancer" with `experiencer=family`.
- Status code mapper should know Z85.x is the correct replacement for active cancer after curative treatment + remission.

## See also

- [`../negation-and-assertion.md`](../negation-and-assertion.md) - history-of rules
- [`../cards/`](../cards/) - per-HCC cards with history-of pitfalls
