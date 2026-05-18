# Terminology and crosswalks for HCC NLP

> **Why this file exists:** ICD-10-CM → HCC mapping is the single biggest source of "looks like a bug but is a crosswalk version problem" failures in HCC NLP. This file maps the terminology landscape, points to the authoritative sources, and lists the gotchas.

We do not redistribute CMS or HHS crosswalk files in this skill. They are large, change annually, and have specific licensing / sourcing expectations. Always pull from the official annual release.

---

## 1. Terminology systems used in HCC NLP

| System | Owner | Use in HCC pipeline |
|---|---|---|
| **ICD-10-CM** | CMS / NCHS | The diagnosis code set. HCCs map FROM ICD-10-CM codes. |
| **CMS-HCC V28 / V24 crosswalk** | CMS | ICD-10-CM → HCC mapping for Medicare Advantage |
| **HHS-HCC crosswalk** | HHS / CCIIO | ICD-10-CM → HCC mapping for ACA marketplace |
| **SNOMED CT** | SNOMED International | Useful for clinical concept candidate generation; bridge to ICD-10-CM via SNOMED-to-ICD-10-CM map |
| **UMLS Metathesaurus** | NLM | Cross-terminology mapping; CUI as a stable concept identifier |
| **RxNorm** | NLM | Medication → diagnosis evidence (e.g., metformin → DM signal) |
| **LOINC** | Regenstrief | Lab orderable / result codes; A1c, eGFR, BNP, etc. for MEAT detection |
| **HCPCS / CPT** | CMS / AMA | Procedure codes; for encounter type and procedure-based MEAT |
| **HCC hierarchy file** | CMS | Parent-child trumping relationships |

## 2. Source URLs to bookmark

(Source these directly; do not rely on third-party reposts.)

- **CMS Medicare Advantage / Part C Risk Adjustment**: CMS publishes the HCC Software ZIP for each payment year. Includes the SAS macros, the ICD-10-CM → HCC crosswalk for V28 and V24 during the phase-in years, the coefficients table, and the hierarchy file.
- **ICD-10-CM annual release**: CMS / NCHS, updated October 1 each year. The new codes and changes apply to dates of service on or after that October.
- **HHS-HCC**: CMS CCIIO publishes the Notice of Benefit and Payment Parameters annually, plus the HHS-HCC model SAS package. Multiple model variants by age group and benefit year.
- **SNOMED CT US Edition**: NLM Value Set Authority Center (VSAC); free with UMLS license.
- **UMLS**: NLM, requires a free license.
- **RxNorm**: NLM, free.
- **LOINC**: Regenstrief, free with registration.
- **HCPCS Level II**: CMS, free.
- **CPT**: AMA, licensed.

## 3. Crosswalk file structure (CMS-HCC, conceptual)

The CMS-HCC crosswalk is a flat table with rows like:

```
ICD-10-CM code | HCC (V28) | HCC (V24, during phase-in) | Description
E11.40         | 18        | 18                          | Type 2 diabetes mellitus with diabetic neuropathy
E11.9          | (none)    | 19                          | Type 2 diabetes mellitus without complications
```

(Example values illustrative; verify against the actual file for the payment year.)

Pipeline implications:

- A single ICD-10-CM code may map to one HCC, multiple HCCs across model versions, or no HCC at all.
- Many ICD-10-CM codes are not HCCs in either model.
- The same ICD-10-CM code may have different HCC numbers in V28 and V24.
- The crosswalk is the single source of truth; do not infer HCC mappings from text similarity or from prior-year crosswalks.

## 4. Annual update cadence

- **ICD-10-CM updates**: October 1 each year. New codes, deleted codes, code text changes.
- **CMS-HCC model updates**: Annual, typically published in advance of the payment year. The crosswalk is updated to reflect new and deleted ICD-10-CM codes.
- **HHS-HCC model updates**: Annual benefit-year publication.
- **Code-set vintage matters**: A pipeline using FY24 ICD-10-CM codes against FY25 dates of service will miss new codes and may try to map deleted codes.

**Pipeline rule:** Tag every extraction with the ICD-10-CM vintage and the HCC model vintage used. When CMS releases the new model, run a controlled re-mapping pass against historical extractions, do not pretend the old extractions are still valid.

## 5. SNOMED CT and the candidate-generation bridge

Many clinical NLP libraries (medspaCy, scispaCy, MedCAT, cTAKES) produce SNOMED concepts more naturally than ICD-10-CM codes. A common pipeline pattern:

1. Extract SNOMED concepts from text
2. Use the SNOMED → ICD-10-CM map (NLM publishes one) to generate ICD-10-CM candidates
3. Use the CMS-HCC or HHS-HCC crosswalk to map ICD-10-CM to HCC

This works well for candidate generation but has gotchas:

- SNOMED → ICD-10-CM is many-to-many in places; specificity can be lost
- Some clinically precise SNOMED concepts map only to unspecified ICD-10-CM codes that do not risk-adjust
- The bridge map itself has versioning

Always validate the bridge output against the gold ICD-10-CM crosswalk before mapping to HCC. Do not skip the ICD-10-CM step.

## 6. RxNorm for medication-based suspect signals

Medications are strong suspect signals but weak validate signals (a med alone is not MEAT for the diagnosis).

| Drug class (RxNorm class) | Suggests | Cautions |
|---|---|---|
| Antihyperglycemics (metformin, sulfonylureas, SGLT2i, GLP-1 agonists) | Diabetes | Some used for weight management without DM (GLP-1 agonists especially) |
| Statins | Lipid disorder; potentially CAD | Lipid disorder is not an HCC; CAD requires the diagnosis |
| ACEi / ARB | HTN, CHF, CKD, post-MI | Highly ambiguous; pair with another signal |
| Loop diuretics | CHF, edema | CHF most common but not exclusive |
| Bronchodilators (LABA, LAMA, SABA) | COPD, asthma | Asthma usually not an HCC; COPD is |
| Insulin | Diabetes | Type 1 vs Type 2 distinction matters for HCC selection |
| Oncology agents | Active cancer | Some used for non-cancer indications (e.g., methotrexate for RA) |
| Anticoagulants | AFib, VTE, post-stroke | Multiple possible indications |
| Anti-dementia (cholinesterase inhibitors, memantine) | Dementia | Strong signal; HCC-relevant |

**Pipeline rule:** Use RxNorm signals in the suspect engine. Do not use them as MEAT in the validate engine without explicit linkage in the note text.

## 7. LOINC for MEAT evaluation

LOINC codes identify the lab test, not the result interpretation. For MEAT detection:

- A1c LOINC code → Evaluate evidence for diabetes
- eGFR LOINC → Evaluate evidence for CKD
- BNP / NT-proBNP LOINC → Evaluate evidence for CHF
- Spirometry / FEV1 LOINC → Evaluate evidence for COPD
- Troponin LOINC → Evaluate evidence for acute MI

Pair the LOINC with the value and the diagnosis linkage. The lab alone is signal; the lab + diagnosis assessment is MEAT.

## 8. Common crosswalk gotchas

- **Unspecified codes that do not risk-adjust.** "Diabetes, unspecified" or "diabetes without complications" often fail to support a high-RAF HCC even though they support a diagnosis. The pipeline must surface the specificity gap, not silently accept the unspecified code.
- **Combination codes.** Many ICD-10-CM codes are combinations (etiology + manifestation). The combination code may map to a different HCC than its parts.
- **7th-character extensions.** Injury codes use A / D / S extensions for initial / subsequent / sequela. The same root code with different extensions can have different HCC implications.
- **Laterality.** Some diagnoses require laterality (right / left / bilateral); unspecified laterality may fail to map.
- **Manifestation codes that cannot be principal.** Some codes are italicized in ICD-10 because they must follow another code; do not present them as standalone in pipeline output.
- **V28 removals vs V24.** A code that was an HCC in V24 may not be in V28. Pipelines that flagged the code as historical recapture must re-evaluate when V28 took over.
- **Z-codes that ARE HCCs.** Z89 (amputation status), Z93 (ostomy status), Z94 (transplant status), Z99 (dialysis dependence). Easy to miss because Z-codes are often blanket-treated as non-clinical.
- **Z-codes that ARE NOT HCCs but are required.** Z79.x long-term drug use codes, BMI Z-codes (Z68.x). They support specificity for other HCCs but are not HCCs themselves.

## 9. BMI documentation requires a diagnosis

BMI Z-codes (Z68.x) are coded from the documented BMI value. They support morbid obesity (HCC 22) but only when paired with a provider diagnosis of obesity / morbid obesity. The Z-code alone is not enough.

Pipeline rule for HCC 22:

- Find documented BMI value (or dx-equivalent text like "morbidly obese")
- Find provider diagnosis of obesity or morbid obesity
- Both must be present in the same encounter
- BMI alone is not codable as HCC 22

See [`cards/hcc-22-morbid-obesity.md`](cards/hcc-22-morbid-obesity.md).

## 10. Pressure ulcer / wound staging requires a diagnosis

Similar pattern to BMI:

- Pressure ulcer stage (L89.x) is coded from nursing documentation of the stage
- But the underlying pressure ulcer diagnosis must come from provider documentation
- Provider must document the existence of the ulcer; nursing can document the stage

Pipeline must capture both, link them, and reject either alone.

## 11. Tooling and versioning checklist

A well-versioned HCC pipeline records:

- [ ] ICD-10-CM code-set FY (October-to-September)
- [ ] CMS-HCC model version (V28 / V24) and crosswalk file vintage
- [ ] HHS-HCC benefit year and crosswalk file vintage (if applicable)
- [ ] SNOMED CT release (if used)
- [ ] UMLS release (if used)
- [ ] RxNorm release (if used)
- [ ] LOINC release (if used)
- [ ] Hierarchy file vintage (matches HCC model version)
- [ ] Pipeline software version

These metadata travel with every extraction.

## See also

- [`model-versions.md`](model-versions.md) - which model version applies to your service year
- [`hierarchies.md`](hierarchies.md) - hierarchy file pairs with crosswalk
- [`raf-calculation.md`](raf-calculation.md) - coefficient table pairs with crosswalk
- [`extraction-patterns.md`](extraction-patterns.md) - SNOMED bridge in pass 1
- [`../nlp/terminology-mapping.md`](../nlp/terminology-mapping.md) - shared HEDIS terminology framework
