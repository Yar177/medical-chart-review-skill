# HCC 18 - Diabetes with Chronic Complications

> Exemplar card. Use the 9-section schema below as the template for building your own HCC cards. See [`../README.md`](../README.md#how-to-use-this-directory).

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 18 - Diabetes with Chronic Complications |
| **HCC (V24)** | 18 - Diabetes with Chronic Complications (analogous; verify against V24 crosswalk) |
| **HHS-HCC** | Multiple HHS-HCC variants for diabetes; verify benefit-year crosswalk |
| **RAF weight (V28 community)** | Moderate-to-high (verify against current coefficients file) |
| **Primary ICD-10 ranges** | E10.2x-E10.6x (Type 1), E11.2x-E11.6x (Type 2), E13.2x-E13.6x (other specified), with combination codes for nephropathy, neuropathy, retinopathy, circulatory, foot ulcer, gangrene, ketoacidosis, etc. |
| **Hierarchy** | Trumped by HCC 17 (Diabetes with Acute Complications); trumps HCC 19 (Diabetes without Complications) |

## 2. Clinical definition

Diabetes mellitus with one or more documented chronic complications affecting peripheral nerves (neuropathy), kidneys (nephropathy, CKD when DM-related), eyes (retinopathy, cataracts when DM-related), circulation (peripheral angiopathy, foot ulcer, gangrene), skin (chronic foot ulcer), or other systems. The combination codes (e.g., E11.40 for T2DM with neuropathy) capture this in a single ICD-10 code.

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter in the calendar year with an acceptable provider type
- See [`../date-of-service.md`](../date-of-service.md) for the full whitelist
- AWVs are common venues for diabetes recapture; apply stricter MEAT scrutiny per [`../meat-criteria.md`](../meat-criteria.md)

## 4. Required documentation (MEAT)

At least one of:

- **M**: A1c trend, fingerstick logs, foot exam findings, neuropathy symptom check, weight trend
- **E**: A1c value, eGFR, microalbumin, fundus exam, monofilament test result, foot exam findings
- **A**: Per-condition statement in assessment ("diabetes with neuropathy, controlled / uncontrolled"), counseling on glycemic control, foot-care education
- **T**: Medication continuation or change (metformin, insulin, SGLT2i, GLP-1, gabapentin for neuropathy), referrals (endo, podiatry, ophtho), procedures, education

The MEAT must be linked to the diabetes diagnosis (not just to a coincident comorbidity). See [`../meat-criteria.md`](../meat-criteria.md) section 4.

## 5. Date of service rule

- Any qualifying encounter in the calendar year captures the HCC for that year.
- Annual reset January 1; no carry-forward.
- Copy-forward A&P blocks attribute to the original encounter date, not the current note.
- AWV-sourced documentation is acceptable but receives stricter MEAT review.

## 6. Hierarchy interaction

```
HCC 17 (DM with Acute Complications)
  trumps
HCC 18 (DM with Chronic Complications) <-- this card
  trumps
HCC 19 (DM without Complications)
```

Pipeline must apply this after extraction. A member with both an acute complication (DKA, hyperosmolar state) and chronic neuropathy in the same year contributes ONLY HCC 17 to RAF.

Disease-disease interactions: CMS-HCC includes a DM + CHF interaction (verify against current model); when both HCCs are present, an additional coefficient applies.

## 7. Assertion / negation pitfalls

- **"History of diabetes" with diet-controlled remission** - usually still active for coding (diabetes is not considered "resolved" by remission for coding purposes); confirm against current guidelines. Diet-controlled DM is still DM.
- **"Pre-diabetes"** (R73.03, R73.09) is NOT diabetes; do not map to HCC 18/19.
- **"Borderline diabetes"** is not a valid coding diagnosis; do not map.
- **"Steroid-induced diabetes"** has its own code (E09.x); check whether the steroid is chronic (then code as DM) vs transient (then do not).
- **"Diabetes vs prediabetes"** in outpatient setting - hedged; do not code either.
- **Family history of diabetes** (Z83.3) is not patient diabetes; do not code as patient HCC.
- **Gestational diabetes** (O24.4) is a different ICD branch; some pipelines wrongly map it to E11.x.

## 8. Status-code conflations

- **Z79.4 (long-term insulin use)** - not an HCC itself but documents insulin dependence; pair with the underlying diabetes code.
- **Z89.5x (amputation status)** following diabetic foot complication - is its own HCC (amputation status); do NOT also code the original ulcer once healed.
- **Z86.39 (personal history of other endocrine / metabolic disease)** is not used for current diabetes; if you see this with documentation of current management, the dx is current, not historical.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "diabetes mellitus type 2," "T2DM," "T1DM," "DM2," "IDDM," "NIDDM," "DM with neuropathy," "diabetic peripheral neuropathy," "diabetic nephropathy," "diabetic retinopathy," "diabetic foot ulcer"
- Medications (RxNorm): metformin, sulfonylureas, GLP-1 agonists, SGLT2i, DPP-4i, insulin (all forms), thiazolidinediones
- Labs (LOINC): HbA1c, fasting glucose, fructosamine, C-peptide
- Diagnosis-adjacent: gabapentin / pregabalin (neuropathy treat), ACEi/ARB with microalbuminuria documentation (nephropathy)

**Suspect-engine signals (member-level):**

- Prior-year diabetes claims not yet captured this year
- Antihyperglycemic dispense in the year
- A1c result above diagnostic thresholds without prior dx
- Specialty referral to endocrinology, podiatry, or ophthalmology with DM context

**Validate-engine signals (encounter-level):**

- Combination code present in Assessment (E11.40, E11.21, etc.) is the strongest signal
- "Diabetes with [complication]" + linkage in same A&P block
- Per-complication MEAT (foot exam, A1c review with comment, gabapentin start, etc.)

**Reject signals:**

- Pre-diabetes only
- Family-history-only
- PMH-only with no current MEAT (see fixture [`../test-fixtures/meat-gap.md`](../test-fixtures/meat-gap.md))
- Hedged outpatient ("possible DM," "rule out DM")
- Resolved gestational diabetes only

**Failure-mode references:**

- [`../test-fixtures/hierarchy-collapse.md`](../test-fixtures/hierarchy-collapse.md) - HCC 18 vs 19 hierarchy
- [`../test-fixtures/meat-gap.md`](../test-fixtures/meat-gap.md) - PMH-only DM with no MEAT
- [`../test-fixtures/problem-list-only.md`](../test-fixtures/problem-list-only.md) - problem-list-only DM

**Specificity gap watch:** "Diabetes mellitus, unspecified" (E11.9 with no complication code) maps to HCC 19, not HCC 18. If the chart documents complications elsewhere but the assessment uses the unspecified code, surface a specificity-query opportunity rather than upcoding the HCC silently. See [`../extraction-patterns.md`](../extraction-patterns.md) on two-pass architectures.

## See also

- [`../hierarchies.md`](../hierarchies.md) - diabetes family hierarchy
- [`../meat-criteria.md`](../meat-criteria.md) - MEAT detection
- [`../terminology-mapping.md`](../terminology-mapping.md) - ICD-10 → HCC crosswalk handling
- [`../test-fixtures/hierarchy-collapse.md`](../test-fixtures/hierarchy-collapse.md)
- [`hcc-22-morbid-obesity.md`](hcc-22-morbid-obesity.md) - related metabolic HCC
