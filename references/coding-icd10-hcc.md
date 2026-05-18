# ICD-10-CM, HCC, and Risk Adjustment

> **For NLP / data-science teams building HCC extraction pipelines:** this file is the auditor-oriented reference. For model-building knowledge (MEAT as an NLP task, hierarchies as a post-extraction step, V28 / V24 / HHS-HCC versioning, RAF dollar-weighted metrics, RADV readiness, suspect vs validate engines, per-HCC cards, test fixtures), start in [`hcc/`](hcc/). The two directories share the same underlying coding knowledge and are kept in sync.

## ICD-10-CM basics

- 3–7 character alphanumeric codes (e.g., `E11.9` = Type 2 DM without complications)
- **Specificity matters**: `E11.9` vs `E11.65` (with hyperglycemia) vs `E11.21` (with nephropathy)
- **Combination codes** capture etiology + manifestation in one code
- **Laterality**: right/left/bilateral required for many codes
- **7th character extensions**: A (initial), D (subsequent), S (sequela) for injuries
- **Excludes1** = NEVER coded together; **Excludes2** = not included but may coexist
- Code only **confirmed diagnoses** in outpatient (not "rule out", "possible", "probable")
- Inpatient: uncertain diagnoses at discharge MAY be coded as if confirmed (per UHDDS)

## MEAT criteria (for HCC validation)

Every diagnosis claimed for risk adjustment must show at least one of:

- **M — Monitor**: signs, symptoms, disease progression/regression
- **E — Evaluate**: test results, response to treatment, exam findings
- **A — Assess/Address**: discussion, review of records, counseling, ordering tests
- **T — Treat**: medications, therapies, referrals, surgeries, plan changes

A diagnosis appearing only in the problem list with no MEAT in the encounter = **not codable** for that DOS.

Some auditors also use **TAMPER** (Treatment, Assessment, Monitor/Medicate, Plan, Evaluate, Referral).

## HCC / Risk Adjustment (CMS-HCC v28, HHS-HCC)

- Each beneficiary gets a **RAF (Risk Adjustment Factor) score** = sum of demographic + HCC coefficients
- Higher RAF → higher capitated payment to MA plan
- HCCs **reset annually** — every chronic condition must be documented & coded at least once per calendar year
- Common chronic HCCs that get dropped:
  - Diabetes with complications (vs uncomplicated)
  - CKD stage (specify stage 3a/3b/4/5)
  - Major depression (vs unspecified depression)
  - Vascular disease (PAD, AAA)
  - Morbid obesity (BMI ≥40, or ≥35 with comorbidity) — needs BMI + diagnosis
  - CHF — specify systolic/diastolic, acute/chronic
  - COPD — vs unspecified chronic bronchitis
  - Amputation status (Z89.x)
  - Ostomy status (Z93.x)

## Risk-adjustment audit checklist

For each claimed HCC on the encounter:
- [ ] Diagnosis appears in provider documentation (not just billing)
- [ ] MEAT criteria met within this DOS
- [ ] Specificity matches documentation (no upcoding)
- [ ] Signed and dated by qualified provider
- [ ] No conflicting documentation in same record
- [ ] Status codes (amputation, ostomy, transplant) reconfirmed annually

## Coding hierarchy & rules

- **Official ICD-10-CM Guidelines for Coding and Reporting** (updated annually by CMS/NCHS) — the source of truth
- **AHA Coding Clinic** — authoritative interpretations
- Code first underlying condition when guidelines instruct
- "Code also" notes indicate additional codes may be needed
- Manifestation codes (italicized in ICD-10) cannot be principal diagnosis

## Common compliance traps

- Coding from problem list alone (no MEAT) → audit denial
- "History of" coded as active condition (Z-codes vs active dx)
- Using "unspecified" when documentation supports specificity
- Coding ruled-out diagnoses in outpatient
- BMI/pressure ulcer stage coded without provider diagnosis of obesity/ulcer
