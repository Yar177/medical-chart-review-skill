# Terminology mapping for HEDIS chart-review NLP

Practical mapping from extracted concepts to standard code systems used in HEDIS reporting and downstream FHIR / claims pipelines. Pairs with [`extraction-patterns.md`](extraction-patterns.md) (how to find the concept in text) and the per-measure cards in [`../hedis/`](../hedis/) (what the concept must satisfy).

## Audience

NLP / ML engineers who need to map free-text findings to LOINC, SNOMED CT, RxNorm, CVX, CPT, HCPCS, and ICD-10 codes; analytics engineers wiring NLP output into measure pipelines that expect coded data.

## Scope

- Code-system overview per measure family
- Common code pitfalls (frequently mis-mapped or revised codes)
- Code-first vs phrase-first decision guidance
- Value-set landscape (NCQA proprietary; alternatives for development)

Not in scope: actual NCQA value sets (licensed/proprietary), full code-system reference, FHIR resource definitions.

> **MY caution:** Code system content changes annually (ICD-10 in October, CPT in January, RxNorm monthly, LOINC and SNOMED biannually). Pin your model to a measurement year and document the code-system version snapshot.

---

## 1. Code systems overview

| Code system | Domain | Update cadence | HEDIS role |
|---|---|---|---|
| **LOINC** | Lab tests, observations, surveys | Biannual (June, December) | Lab results (A1c, eGFR, uACR, etc.), questionnaire instruments (PHQ-9), structured observations |
| **SNOMED CT** | Clinical findings, diagnoses, procedures, body sites | Semiannual (US: March, September) | Problem-list entries, structured diagnoses, ACP, advance directive concepts |
| **RxNorm** | Medications (clinical drugs, drug components) | Monthly | Medication identification (prescription, dispense, adherence measures) |
| **NDC** | National Drug Code | Real-time / continuous | Dispensed medication identification (pharmacy claims) |
| **CVX** | Vaccines | As needed | Vaccine administration evidence (AIS-E) |
| **CPT** | Procedures and services (E&M, surgeries, screenings) | Annual (January) | Visit identification, procedure evidence (mammogram, colonoscopy, DXA) |
| **HCPCS Level II** | Supplies, drugs, services not in CPT | Annual / quarterly updates | Vaccines administered, supplies, some procedures |
| **ICD-10-CM** | Diagnoses | Annual (October 1) | Diagnosis-based numerators, denominators, exclusions |
| **ICD-10-PCS** | Inpatient procedures | Annual (October 1) | Inpatient procedure evidence (deliveries, surgeries) |
| **POS (Place of Service)** | Encounter setting | Annual updates | Telehealth (02, 10), inpatient (21), outpatient (22), ED (23), etc. |
| **NUCC Provider Taxonomy** | Provider specialty | Quarterly | Eligible provider role for measure attribution |

---

## 2. Per-measure-family code mapping

The grid below is a starting point. Each measure's actual value set is owned by NCQA and licensed; this table shows the **code system you'll need to pull from** for a given measure family.

### Diabetes (GSD, EED, KED, BPD, SUPD)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Diabetes diagnosis | ICD-10-CM (E10.*, E11.*) | Type 1 vs Type 2 distinction; gestational (O24.*) typically excluded |
| HbA1c lab result | LOINC | Multiple LOINCs (4548-4 most common); value in % units |
| eGFR | LOINC | Multiple LOINCs depending on method (CKD-EPI vs MDRD); units mL/min/1.73m² |
| uACR | LOINC | Both spot urine albumin (LOINC) and urine creatinine (LOINC) combined |
| Retinal exam (EED) | CPT (e.g., 92250 fundus photography), SNOMED for retinopathy findings | Multiple modalities accepted: dilated exam, fundus photo, OCT |
| BP reading | LOINC (separate codes for systolic and diastolic) | Setting matters for some measures |
| ACE/ARB / SGLT2i / GLP-1 / metformin / insulin | RxNorm, NDC | RxNorm clinical drug + drug component for class identification |
| Hospice exclusion | ICD-10 (Z51.5), POS, value-set | Cross-cuts most measures |

### Cancer screening (BCS-E, CCS-E, COL-E)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Mammogram | CPT (77067 screening, 77066 diagnostic, 77063 + DBT add-on, etc.) | Screening vs diagnostic distinction matters; 3D tomosynthesis codes evolved |
| Cervical cytology / HPV | CPT (88141-88175 for cytology, 87624/87625 for HPV) | HPV co-test scenarios |
| Colonoscopy | CPT (45378, 45380, 45385, etc.) | Screening modifier (PT) for Medicare; HCPCS G0105/G0121 |
| FIT / FOBT | CPT (82270 FOBT, 81528 Cologuard / mt-sDNA) | Cologuard / mt-sDNA has its own look-back |
| Bilateral mastectomy exclusion (BCS-E) | ICD-10 (Z90.13), CPT/ICD-10-PCS for procedures | Lifetime exclusion |
| Hysterectomy exclusion (CCS-E) | ICD-10 (Z90.71*, etc.), CPT/ICD-10-PCS | Total vs partial matters |

### Cardiovascular (CBP, SPC, PBH)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Hypertension diagnosis | ICD-10 (I10-I16) | Active vs historical; secondary HTN distinction |
| BP reading | LOINC | Setting and modality (home vs office) per spec |
| Statin medications | RxNorm | Class-level grouping; intensity (low/moderate/high) for some measures |
| ASCVD diagnosis | ICD-10 | Broad family of codes (CAD, MI, stroke, PAD) |
| Diabetes diagnosis (for SPC eligibility) | ICD-10 | Same as Diabetes family |

### Behavioral health (FUH, PHQ, DSF-E, DMS-E)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Mental health inpatient stay | ICD-10 principal dx (F*), POS (51 inpatient psych), DRG | Acute MH stay identification |
| Outpatient MH follow-up visit | CPT (90832-90838, 99214-99215 with MH dx), HCPCS | Provider type also matters |
| PHQ-9 administration | LOINC (44261-6 for PHQ-9 total) | Item 9 (item-level LOINC) for safety escalation |
| PHQ-2, PHQ-A, EPDS | LOINC | Distinct instrument codes |
| Depression diagnosis | ICD-10 (F32, F33) | MDD vs adjustment disorder vs unspecified |
| Suicide ideation / attempt | ICD-10 (R45.851, T14.91), SNOMED | Safety escalation; not a HEDIS numerator but operationally important |

### Transitions of care (MRP, TRC)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Inpatient discharge | UB-04 type-of-bill, DRG, claim-based discharge date | Discharge date is the anchor |
| Medication reconciliation | CPT (1111F category II code), HCPCS | Code presence helps but narrative documentation often required |
| Post-discharge office visit | CPT E&M codes with appropriate POS | Date proximity to discharge drives compliance |
| Discharge summary receipt | No standard code; document-level tracking | HIE feed timestamps |

### Pediatric / Perinatal (W30, WCV, WCC, PPC, AIS-E)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Well-child visit | CPT (99381-99385 new, 99391-99395 established) | Age band matters |
| BMI percentile (pediatric) | LOINC (59576-9 percentile for age) | Distinct from adult BMI |
| Vaccines | CVX, CPT (vaccine admin: 90460-90474), HCPCS | CVX is vaccine-specific; CPT/HCPCS is administration |
| Prenatal visit | CPT, SNOMED for OB-specific procedures | Trimester from EDC calculation |
| Postpartum visit | CPT (59430 global), discrete postpartum E&M | 7-84 day window |
| Live birth | ICD-10-CM (Z37.*), ICD-10-PCS for delivery, DRG | Excludes stillbirths, miscarriages |

### Older Adult (COA, ACP, OSW, FRM)

| Concept | Primary system(s) | Notes |
|---|---|---|
| Advance care planning | CPT (99497, 99498), SNOMED, document-level (Consent FHIR resource) | Time-based codes; documentation requirements |
| POLST/MOLST | Document-level; some state-specific codes | Scanned document tracking |
| Medication review | CPT (1111F), CMR (Star MTM) codes | Documentation often narrative |
| Functional status assessment | LOINC (Katz ADL, Lawton IADL, Barthel) | Standardized tool codes |
| Pain assessment | LOINC (numeric rating scale, FACES, PEG) | "Pain assessed" attestation often narrative |
| DXA scan | CPT (77080 axial, 77081 appendicular) | Modality must be DXA, not other imaging |
| Osteoporosis medications | RxNorm | Bisphosphonates, denosumab, teriparatide, abaloparatide, romosozumab, raloxifene |
| Hospice exclusion | ICD-10 (Z51.5), HCPCS hospice codes | Cross-cutting |
| Advanced illness / frailty | ICD-10 (multi-code combinations) | Spec-specific value sets |

---

## 3. Common code pitfalls

### LOINC pitfalls

- **HbA1c has multiple LOINCs.** 4548-4 is the most common (HbA1c in blood as %) but other LOINCs exist (4549-2 HbA1c by HPLC, 17856-6 estimated average glucose conversion, etc.). Map all accepted variants.
- **eGFR LOINCs vary by calculation method.** CKD-EPI 2009, CKD-EPI 2021, MDRD - different LOINCs. KED uses eGFR for staging; verify accepted methods.
- **Component LOINCs vs panel LOINCs.** Lab interfaces sometimes deliver only panel LOINCs; the component (e.g., urine albumin) requires drilling in.
- **Pediatric BMI percentile uses a distinct LOINC** from adult BMI - 59576-9. Do NOT use adult BMI LOINC for WCC-BMI.
- **PHQ-9 vs PHQ-9 item 9.** Total score has its own LOINC; item 9 (suicide ideation) has its own. Track both for safety operations.

### SNOMED pitfalls

- **Active vs historical.** Many SNOMED concepts are diagnostic; the assertion (active vs resolved vs ruled out) is qualified separately. Do NOT take SNOMED code presence as evidence of active condition without assertion checking.
- **Concept inactivation.** SNOMED retires concepts; you may see old codes that no longer match current value sets. Use historical-association mappings.

### RxNorm pitfalls

- **Clinical drug vs ingredient vs brand.** RxNorm has multiple term types (TTY): IN (ingredient), PIN (precise ingredient), SCD (semantic clinical drug), SBD (semantic branded drug). Choose the TTY that matches your use case. For class-level identification (statins, SGLT2i), aggregate at the ingredient or class level.
- **NDC vs RxNorm.** Pharmacy claims use NDC; EHR e-prescribing typically RxNorm. Maintain NDC ↔ RxNorm crosswalks.
- **Combination products.** ARB + thiazide combos, metformin + DPP4i combos - decide whether each component independently satisfies the measure (typically yes for class identification).

### CVX pitfalls

- **CVX is administered-vaccine specific.** Code 88 ("Influenza, unspecified") should be avoided; specific subtype codes are preferred. Older registries may emit only "unspecified" codes - decide whether to accept.
- **COVID-19 vaccine evolution.** Multiple CVX codes for monovalent, bivalent, and updated formulations. Verify current ACIP-recommended formulation against AIS-COVID acceptance.
- **Tdap vs Td.** Distinct CVX codes; tetanus-only does NOT satisfy Tdap-required indications.

### CPT pitfalls

- **Screening vs diagnostic.** Mammogram and colonoscopy have separate screening and diagnostic codes; HEDIS screening measures typically require the screening code. A diagnostic colonoscopy after a positive FIT often satisfies via "follow-up after positive screen" - verify per measure.
- **Annual code revisions.** CPT codes change January 1. Pin your model and value sets to a code-year snapshot.
- **Bundled vs separately billable.** Some services are bundled into E&M; absence of a procedure CPT code does NOT mean the procedure didn't happen.

### ICD-10 pitfalls

- **October 1 annual revisions.** New codes, deleted codes, code-description changes. Pin your model to a code-year and align with NCQA spec MY.
- **Code specificity.** ICD-10 has 7-character codes; HEDIS value sets often accept code families. Use parent-code rollups carefully.
- **Z-codes for screening / counseling.** Z-codes document services but may not satisfy diagnosis-based numerators. Verify per measure.
- **Pregnancy exclusion codes.** Pregnancy and postpartum codes appear in many exclusions; ensure your pipeline catches them.

### POS pitfalls

- **Telehealth POS codes evolved.** POS 02 (telehealth other than home) and POS 10 (telehealth in home) are distinct; spec acceptance may differ.
- **Inpatient vs observation.** POS 21 (inpatient hospital) vs 22 (on-campus outpatient) - observation stays sit in a grey zone for some measures.

---

## 4. Code-first vs phrase-first decision guidance

When evidence exists in both structured codes and narrative text, choose your extraction path deliberately.

### Use code-first when:

- The structured data is high-quality and complete (e.g., lab interfaces with LOINC-coded results, immunization registry feeds)
- The measure has clean code-based value sets and minimal narrative-only nuance (e.g., AIS-E vaccines, GSD A1c values)
- You're working with claims data (no narrative)
- You need MY-comparable consistency across many providers/practices

### Use phrase-first when:

- The numerator requires discussion documentation (ACP, counseling for WCC-NUTRITION, MRP reconciliation language)
- Structured fields are sparse or unreliable (outside records, scanned PDFs, free-form notes)
- You're looking for assertion qualification (refusal, "rule out", "history of")
- The measure has documentation-quality requirements beyond a code presence

### Hybrid (recommended for most measures):

1. **Start with structured codes** when available; they're date-clean and provenance-clean
2. **Add narrative extraction** to fill gaps, capture refusals, and provide MRRV-defensible snippets
3. **Reconcile** - if both sources are present, prefer the structured one but capture both for audit
4. **Flag conflicts** - structured says compliant, narrative says refused; investigate before scoring

---

## 5. Value-set sources

NCQA HEDIS value sets are **proprietary and licensed**. You cannot reproduce them publicly. For development:

- **License NCQA value sets** through NCQA's licensing program if you're building a production HEDIS engine
- **VSAC (Value Set Authority Center, NLM)** has many overlapping eCQM value sets - useful for prototyping and adjacent measures
- **Vendor value sets** - some HEDIS-certified vendors expose their value sets to licensed customers
- **State Medicaid quality programs** sometimes publish derivative value sets

For your development corpus and test fixtures, you can build **synthetic value sets** that mimic structure without exposing NCQA-licensed content. Document them clearly as synthetic.

> **Compliance:** Do not embed NCQA-licensed value sets in open repositories. Do not redistribute. Do reference value-set OIDs (Object Identifiers) when documenting which set your code targets.

---

## 6. Practical guidance for NLP teams

- **Pin code versions.** ICD-10-MY, CPT-MY, RxNorm-snapshot date, LOINC release, SNOMED edition. Document in your model card.
- **Crosswalk maintenance.** Build and maintain NDC ↔ RxNorm, ICD-10 ↔ SNOMED, LOINC ↔ local lab codes (for in-house labs with non-standard codes).
- **Lab-code mapping at the source.** Many health systems use local lab codes (Quest, LabCorp, in-house) that must be mapped to LOINC. Invest in this mapping table; it's a high-leverage asset.
- **Test with code-system updates.** When ICD-10 publishes October updates, re-run regression fixtures to catch new codes, deleted codes, and crosswalk drift.
- **Document the spec MY** your model targets. A model built for HEDIS MY2024 may not satisfy MY2025 without reverification.
- **Reconcile structured and narrative.** Build a reconciliation step that merges code-based evidence with narrative extraction and produces a single, ranked evidence record per measure per patient.

---

## See also

- [`extraction-patterns.md`](extraction-patterns.md) - how to extract concepts from text
- [`date-of-service.md`](date-of-service.md) - date selection across evidence sources
- [`negation-and-assertion.md`](negation-and-assertion.md) - qualifying coded and narrative findings
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - source-of-truth and MRRV
- Sibling `medical-chart-review` skill, `references/coding-icd10-hcc.md` - ICD-10 / HCC reference
- Sibling `medical-chart-review` skill, `references/coding-cpt-drg.md` - CPT / DRG reference
- Sibling `medical-chart-review` skill, `references/labs-imaging.md` - lab and imaging reference
- Sibling `medical-chart-review` skill, `references/medications.md` - medication reference
