# Code groupers

> **Why this file exists:** Raw codes are too granular for most analytics. **Groupers** roll codes up into analytically useful categories (chronic conditions, comorbidities, procedure classes, utilization buckets). The grouper choice affects every downstream model, cohort, and stratification. Each grouper has a specific use case, version cadence, and known limitations.

## 1. What a grouper is

A **code grouper** is a rule-based or statistically derived mapping from a granular code system (typically ICD-10-CM, ICD-10-PCS, or CPT) to a smaller set of clinically or operationally meaningful categories.

Three common roles:

1. **Comorbidity indices** for risk adjustment and severity (Charlson, Elixhauser).
2. **Clinical classifications** for cohort definitions and analytics (CCSR, CCS legacy).
3. **Utilization / payment groupers** for service-line analysis (BETOS, DRG, APC, AHRQ groupers).

Different from a **value set**: a value set is a single named concept's code list; a grouper is a **partition** of the code space into many categories.

## 2. CCSR - Clinical Classifications Software Refined

- **Owner**: AHRQ (Agency for Healthcare Research and Quality), HCUP project.
- **Free**, public domain.
- **Updates**: annually with ICD-10-CM updates (October).
- **Two variants**:
  - **CCSR for ICD-10-CM Diagnoses**: rolls up diagnosis codes into **~530 mutually exclusive categories** (default category) and **multiple body-system categorizations**.
  - **CCSR for ICD-10-PCS Procedures**: rolls up inpatient procedure codes into **~320 categories** by body system + clinical purpose.
- **Each ICD-10-CM code maps to one default CCSR plus, optionally, up to 25 secondary CCSRs** when the code can plausibly represent multiple clinical concepts (e.g., a sepsis code may roll up to both "sepsis" and the infecting organism's body system).

### Use cases

- **Cohort definitions** at the chronic-condition level.
- **Feature engineering** for ML on claims (e.g., a CCSR feature vector per member-month).
- **Burden-of-disease reporting** for population health.
- **Stratification** for quality measures.

### Replaces / supersedes

- **CCS** (Clinical Classifications Software, the predecessor for ICD-9 and a pre-CCSR ICD-10 version) - **legacy**; CCSR is the current AHRQ standard for ICD-10 data.

## 3. Elixhauser comorbidity measures

- **Owner**: AHRQ (HCUP).
- **Free**, public domain.
- Originally **30 comorbidities** (Elixhauser, Steiner, Harris, Coffey 1998); AHRQ has published **refined versions** with **40+ comorbidities** and ICD-10-CM-specific mappings.
- Each comorbidity is a **flag** (present / absent) for a member or encounter based on ICD-10-CM presence.
- Commonly used as:
  - A **binary indicator panel** as ML features.
  - The **van Walraven score** - a weighted sum of Elixhauser comorbidities producing a single index (validated for inpatient mortality risk).

### Versions

- **AHRQ Elixhauser Comorbidity Software** is updated alongside the annual ICD-10-CM release. Pin the version to the data vintage.
- Multiple "flavors" exist in the literature - the original Elixhauser et al. version, AHRQ's refinement, the Quan et al. version, etc. **Specify which version your pipeline uses**; results differ.

## 4. Charlson Comorbidity Index (CCI)

- **Owner**: originally Mary Charlson et al. (1987), with multiple ICD adaptations published since.
- **17 conditions**, each with a weight (1, 2, 3, or 6). Sum = **Charlson Comorbidity Index** score; higher = greater 10-year mortality risk.
- Frequently combined with age (age-adjusted CCI).
- The **Quan et al. (2005)** ICD-10 adaptation is the most-cited version.
- **Free**.

### CCI vs Elixhauser

| Property | CCI | Elixhauser |
|---|---|---|
| Conditions | 17 | 30-40+ |
| Output | Single weighted score | Binary flags or weighted (van Walraven) |
| Original purpose | 10-year mortality | Inpatient outcomes |
| Granularity | Coarser | Finer |
| Common use | Long-term risk, research | Inpatient acuity, severity adjustment |

Both have valid use cases; many studies use both for sensitivity analysis. Neither is uniformly superior.

## 5. CCI / NCCI - National Correct Coding Initiative

- Note: **CCI** in this section refers to the **NCCI** (National Correct Coding Initiative), distinct from the **Charlson** CCI above. Naming collision is real and contextual.
- **Owner**: CMS.
- **NCCI Procedure-to-Procedure (PTP) edits** identify code pairs that cannot be billed together unless an appropriate modifier is applied.
- **Medically Unlikely Edits (MUEs)** identify the maximum reasonable units of a given code per day.
- **Updates**: quarterly.
- **Use**: claim editing, denial prediction, FWA detection, coding compliance.

Not a "rollup" grouper in the conventional sense; it's a **rule set** for valid code combinations.

## 6. BETOS - Berenson-Eggers Type of Service

- **Owner**: CMS (with the original Berenson-Eggers 1988 paper as the conceptual foundation; CMS publishes **BETOS 2.0** as the modern version).
- **Free**, public.
- Categorizes HCPCS / CPT codes into a **service-type taxonomy**: E&M, procedures (major / minor), imaging, tests, DME, drugs, etc.
- Multi-level hierarchy.
- **Use**: utilization analytics, service-line reporting, cost-of-care analysis.
- **Updates**: with the HCPCS quarterly release cycle.

## 7. AHRQ groupers (other)

AHRQ publishes several other groupers via the HCUP project:

- **Diagnosis-related groupers** beyond CCSR.
- **Procedure groupers** beyond CCSR Procedures.
- **Patient Safety Indicators (PSI)**, **Inpatient Quality Indicators (IQI)**, **Pediatric Quality Indicators (PDI)** - rule-based quality grouping that produce defined adverse-event or quality metrics from claims.
- **HCUP Tools**: SAS / Python / R packages for many of the above.

All free, all public domain.

## 8. DRG / APR-DRG / APC

See [`institutional-billing-codes.md`](institutional-billing-codes.md):

- **MS-DRG** (CMS, Medicare inpatient PPS).
- **APR-DRG** (3M, commercially licensed; widely used by states / commercial / quality programs).
- **APC** (CMS, outpatient PPS).

These are **payment / severity** groupers, not clinical-cohort groupers. Use them when payment, severity adjustment, or inpatient case-mix is the analytic question; use CCSR / Elixhauser / Charlson when the question is comorbidity burden.

## 9. HCC and HHS-HCC

- **CMS-HCC** (Medicare Advantage) and **HHS-HCC** (ACA marketplace) are **risk-adjustment groupers** that map ICD-10-CM diagnoses to ~80-200 HCCs (depends on model version) used to compute member-level risk scores (RAF).
- Functionally a grouper, but with **payment authority** that ordinary grouper choices lack.
- See [`crosswalks.md`](crosswalks.md) §6 and the `hcc-nlp` skill.

## 10. Choosing a grouper

| If your task is... | Consider |
|---|---|
| Cohort definition for a chronic-condition study | CCSR (default category) |
| Multi-condition flag panel for ML | Elixhauser (binary flags) or CCSR (multiple categorizations) |
| Single mortality-risk index | Charlson (van Walraven if you prefer Elixhauser-derived) |
| Hospital severity adjustment | Elixhauser (van Walraven score) or APR-DRG severity / mortality sub-classes |
| Service-line utilization analysis | BETOS 2.0 |
| Claim editing / denial prediction | NCCI PTP + MUE |
| Inpatient payment / case-mix | MS-DRG (Medicare) or APR-DRG (others) |
| Outpatient payment | APC |
| Risk-adjustment payment | CMS-HCC (V24/V28) or HHS-HCC |
| Quality / safety adverse events | AHRQ PSI / IQI / PDI |
| Pre-ICD-10 historical data | CCS (predecessor of CCSR) or stay in ICD-9 native |

The [`../templates/grouper-evaluation.md`](../templates/grouper-evaluation.md) template captures a structured grouper-selection process.

## 11. Versioning - always pin

Every grouper requires:

- **Grouper version** (e.g., "CCSR v2024.1", "AHRQ Elixhauser Software v2024.1", "Quan 2005 Charlson ICD-10 adaptation")
- **Underlying code-system version** the grouper was built against (e.g., "ICD-10-CM FY2024")
- **Any local modifications** (custom additions, code mappings overridden, conditions excluded)

A pipeline that emits CCSR-categorized data without pinning the CCSR version produces results that are non-reproducible after the next CCSR release.

## 12. Authoritative sources

- **CCSR**: <https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp>
- **AHRQ Elixhauser Comorbidity Software**: <https://hcup-us.ahrq.gov/toolssoftware/comorbidity/comorbidity.jsp>
- **Charlson Comorbidity Index (Quan adaptation)**: published academic literature; multiple SAS / Python / R implementations are freely available.
- **NCCI Edits**: <https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits>
- **BETOS 2.0**: <https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/berenson-eggers-type-of-service-betos-classification-system>
- **AHRQ Quality Indicators (PSI / IQI / PDI)**: <https://qualityindicators.ahrq.gov/>
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 13. Common pitfalls

- **Mixing Elixhauser versions** across cohorts (original vs AHRQ refined vs Quan). Results differ; document the version.
- **CCS used instead of CCSR** for ICD-10 data. CCS is legacy; CCSR is current.
- **Grouper version not pinned**. Re-running last year's analysis with this year's grouper produces different numbers and the cause is invisible.
- **Underlying code-system version mismatch.** A CCSR built for FY2024 ICD-10-CM applied to FY2026 codes misses the new codes.
- **APR-DRG licensing forgotten** in cost / quality reporting. APR-DRG is commercially licensed; redistribution requires 3M agreement.
- **NCCI (correct coding) confused with Charlson CCI.** Naming collision; specify which.
- **HCC used as a generic comorbidity grouper** for non-risk-adjustment purposes. HCC is payment-tuned; it omits conditions that don't drive payment but matter clinically.
- **Single grouper relied on for all analyses.** Different questions warrant different groupers; one-size-fits-all leads to mismatch.
- **Custom modifications undocumented.** "We added these 12 conditions to Elixhauser" without a written record means the next analyst cannot reproduce the cohort.
