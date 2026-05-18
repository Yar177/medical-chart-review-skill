# Quality Measures: HEDIS, Stars, MIPS

> **Deep dives:** This file is the overview. For per-measure denominator / numerator / exclusion / NLP-signal cards, see [`hedis/`](hedis/). For data provenance and supplemental-data rules, see [`hedis-supplemental-data.md`](hedis-supplemental-data.md). For NLP-team guidance on date of service, negation/assertion, extraction patterns, and evaluation, see [`nlp/`](nlp/). For the abstraction worksheet, see [`../templates/hedis-abstraction.md`](../templates/hedis-abstraction.md).

## HEDIS (Healthcare Effectiveness Data and Information Set)

Published annually by NCQA. Used by health plans for accreditation and by CMS for MA Stars.

### Common HEDIS measures to check during chart review

| Measure | What to look for |
|---|---|
| **CBP** (Controlling Blood Pressure) | Most recent BP <140/90 in pts 18–85 with HTN |
| **HBD** (HbA1c Control for Diabetes) | A1c <8% in past year |
| **EED** (Eye Exam for Diabetes) | Retinal exam by eye care professional |
| **KED** (Kidney Health Eval for Diabetes) | eGFR + uACR in past year |
| **BCS-E** (Breast Cancer Screening) | Mammogram in past 2 years, women 50–74 |
| **COL** (Colorectal Cancer Screening) | Colonoscopy 10y, FIT annually, Cologuard 3y, etc. |
| **CIS / IMA** | Childhood / Adolescent immunizations |
| **AMM** | Antidepressant Medication Management adherence |
| **FUH** | Follow-up after Hospitalization for mental illness (7-day & 30-day) |
| **PCR** | Plan All-Cause Readmissions |
| **SUPD / SPC** | Statin Use in Persons with Diabetes / Cardiovascular Disease |
| **MRP** | Medication Reconciliation Post-Discharge |
| **TRC** | Transitions of Care |
| **OMW** | Osteoporosis Management in Women who had a Fracture |

### Hybrid measures
Some HEDIS measures allow **hybrid** (admin + medical record) sampling - chart review fills gaps that claims miss. Hybrid abstraction is subject to NCQA Medical Record Review Validation (MRRV); see [`hedis-supplemental-data.md`](hedis-supplemental-data.md) for provenance rules and audit-trail expectations.

### Per-measure deep-dive cards

The [`hedis/`](hedis/) directory has per-measure reference cards covering denominator, numerator, exclusions, NLP signal phrases, common documentation gaps, and notes. Cards are organized by clinical area:

- **Diabetes:** BPD, EED, GSD (replaces HBD MY 2024), KED, SUPD
- **Cardiovascular:** CBP, SPC
- **Cancer screening:** BCS-E, CCS-E, COL-E
- **Behavioral health:** FUH, PHQ (PHQ-2 / PHQ-9 instruments)
- **Transitions:** MRP, TRC (4 sub-indicators including TRC-Med and TRC-Patient)
- **Pediatric & perinatal:** PPC (prenatal + postpartum), WCC (BMI + nutrition + physical activity)
- **Older adult:** ACP, AIS-E (flu, Td/Tdap, zoster, pneumococcal, hepatitis B, COVID-19 sub-indicators)

See [`hedis/README.md`](hedis/README.md) for the full index and card structure.

## CMS Stars (Medicare Advantage & Part D)

- 1–5 star plan ratings, updated annually
- Heavy overlap with HEDIS + CAHPS (patient experience) + HOS (health outcomes survey) + Part D adherence
- **Triple-weighted** measures get extra attention:
  - Medication adherence (statins, diabetes meds, RAS antagonists) — Part D
  - Plan all-cause readmissions
  - Controlling blood pressure
  - Diabetes care — A1c control

## MIPS (Merit-based Incentive Payment System)

For clinicians billing Medicare Part B. Four categories:
- **Quality** (was PQRS) — ~200 measures, pick 6
- **Promoting Interoperability** (was Meaningful Use)
- **Improvement Activities**
- **Cost** (claims-based, no reporting)

## Gap analysis workflow

1. Identify measure-eligible population (denominator)
2. Check for exclusions (hospice, palliative, age cutoffs, etc.)
3. Search chart for numerator-compliant evidence
4. If gap exists: document recommended action (e.g., "order screening mammogram")
5. Distinguish **open gap** (no evidence) from **closed gap** (compliant) from **excluded**

## Documentation that closes gaps

- Result + date + source must be in the record
- Patient refusal counts as exclusion for some measures (must be documented)
- "Reviewed outside records" with date/source can close a gap
- Standing orders and care manager actions count if signed
