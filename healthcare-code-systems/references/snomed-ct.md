# SNOMED CT

> **Why this file exists:** SNOMED CT is the clinical terminology used in EHRs and FHIR. It is **far richer and more granular than ICD-10-CM**, with hierarchical "is-a" relationships and a formal expression language (ECL). When you join EHR data to claims, SNOMED is on one side and ICD / CPT is on the other - and the mapping is lossy.

## 1. What it is

- **SNOMED CT** = **Systematized Nomenclature of Medicine - Clinical Terms**.
- Maintained by **SNOMED International** (formerly IHTSDO), with national extensions (e.g., US Edition).
- Used in **EHRs** for clinical documentation (problem lists, allergies, family history, procedures, observations) and in **FHIR** resources (Condition.code, Procedure.code, Observation.code in many contexts).
- **~360,000+ active concepts** (varies by release) - vastly more than ICD-10-CM.
- **Not used directly on US claims.** SNOMED → ICD-10-CM crosswalks bridge to billing.

## 2. Licensing

- **In the United States: free** under the **NLM UMLS Metathesaurus License**. The NLM has a country-license agreement that makes SNOMED CT US Edition free for use within the US.
- **Outside the United States**: licensing varies by country. Some countries are member countries of SNOMED International (free in-country use); others require affiliate licensing.
- **Commercial use** within the US is allowed under the NLM license but requires a free UMLS account and acceptance of the license terms.
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 3. Structure - concepts, descriptions, relationships

SNOMED CT is a **concept-based** terminology, not a code list:

- **Concept**: a unique clinical meaning, identified by a **SNOMED CT Identifier (SCTID)** - a long integer, e.g., `73211009` (Diabetes mellitus).
- **Description**: human-readable terms for the concept. Each concept has one **Fully Specified Name (FSN)** (e.g., "Diabetes mellitus (disorder)"), one **Preferred Term** per language / dialect, and zero or more **synonyms** (e.g., "DM", "Diabetes").
- **Relationship**: typed link between concepts. The most important is the **"is-a"** relationship, which builds the **subsumption hierarchy** (e.g., Type 2 diabetes IS-A Diabetes mellitus IS-A Disorder of glucose metabolism IS-A Metabolic disease).
- **Concept Model attributes**: defining attributes such as `Finding site`, `Associated morphology`, `Causative agent`, `Method`, etc.

### Worked example

```
Concept ID:  44054006
FSN:         "Type 2 diabetes mellitus (disorder)"
Preferred:   "Type 2 diabetes mellitus"
Synonyms:    "DM-2", "T2DM", "Type II diabetes"
Parents:     73211009 "Diabetes mellitus (disorder)"
             237599002 "Insulin resistance (disorder)"
Children:    8801005 "Type 2 diabetes mellitus without complication"
             199230006 "Pre-existing type 2 diabetes mellitus in pregnancy"
             ... many more
Attributes:  Finding site = 113331007 "Endocrine system structure"
             Pathological process = 472963003 "Hyperglycemia"
```

## 4. Hierarchies and subsumption

Every active SNOMED CT concept lives in a polyhierarchy under one of **19 top-level hierarchies**:

| Top-level | Examples |
|---|---|
| Clinical finding (404684003) | Diseases, signs, symptoms |
| Procedure (71388002) | Surgical, diagnostic, therapeutic |
| Observable entity (363787002) | "Heart rate", "Blood glucose level" |
| Body structure (123037004) | Anatomy |
| Organism (410607006) | Bacteria, viruses, fungi |
| Substance (105590001) | Drugs, chemicals, allergens |
| Pharmaceutical / biologic product (373873005) | Medications as products |
| Specimen (123038009) | Blood, urine, tissue |
| Qualifier value (362981000) | "Left", "Right", "Severe" |
| Event (272379006) | "Fall", "Motor vehicle accident" |
| Environment or geographical location (308916002) | "Home", "Hospital ward" |
| Social context (48176007) | "Married", "Employed" |
| Physical object (260787004) | "Wheelchair", "Stent" |
| Physical force (78621006) | "Gravity", "Electricity" |
| Record artifact (419891008) | "Health record" |
| Situation with explicit context (243796009) | **History of**, **Family history of**, **Suspected**, **Absent** - critical for assertion |
| Staging and scales (254291000) | "TNM stage", "Pain scale" |
| Special concept (370115009) | Navigational |
| Linkage concept (106237007) | Linkage / link assertions |

### "Situation with explicit context" - the assertion layer

SNOMED CT explicitly encodes context like "history of" and "family history of" as **distinct concepts** rather than as flags on the disease concept. This is fundamentally different from ICD-10-CM (where "history of" is a separate `Z` code rather than a contextualized version of the disease code).

- `73211009` "Diabetes mellitus (disorder)" - the disease
- `161445009` "History of diabetes mellitus" - the situation
- `160303001` "Family history of diabetes mellitus" - the family history situation

For NLP and chart-review work, these are **distinct concepts to model**, not the same one with a flag. See the `hcc-nlp` skill's `references/negation-and-assertion.md` for the NLP treatment.

## 5. Expression Constraint Language (ECL)

**ECL** is the formal query language for selecting sets of SNOMED concepts based on hierarchy and attributes. It is the SNOMED-native way to define a "value set" without enumerating every concept.

Examples:

```
<< 73211009                                         All descendants of and including Diabetes mellitus
<! 73211009                                         Direct descendants of Diabetes mellitus (one level)
<< 73211009 |Diabetes mellitus|                     Same, with FSN annotation (readability)
< 71388002 : 116676008 = 122855007                  Procedures where the associated morphology is "Stenosis"
^ 700043003                                         Members of the reference set with that ID (e.g., a value set)
```

ECL expressions are evaluated against a **specific SNOMED CT release**; results change as the terminology evolves. Always pin the release version when distributing ECL value-set definitions.

## 6. US Edition

- The **SNOMED CT US Edition** is the NLM-published US extension that combines the International Edition with US-specific content.
- Released **biannually** (March 1 and September 1).
- Contains all International content plus US extensions for things like SNOMED-to-ICD-10-CM mappings, US-specific anatomy / procedures, and reference sets for US use cases.
- Distributed via NLM (UMLS Knowledge Sources).

## 7. SNOMED-to-ICD-10-CM map

- NLM publishes the **SNOMED CT to ICD-10-CM Map** as part of the US Edition release.
- The map is **rule-based** - for each SNOMED concept, one or more candidate ICD-10-CM codes are listed with **map advice** describing when each candidate applies (age, sex, additional finding required, etc.).
- **Not a 1:1 mapping.** Many SNOMED concepts map to multiple ICD-10-CM candidates; many ICD-10-CM codes are reachable from multiple SNOMED concepts.
- The map is intended for **provider-side derivation of billing codes from EHR concepts**, not for analytics-time crosswalking after the fact (though it is often used that way).
- See [`crosswalks.md`](crosswalks.md).

## 8. Release cadence

| Release | Source | Cadence |
|---|---|---|
| International Edition | SNOMED International | Biannual (April 1, October 1) |
| US Edition | NLM | Biannual (March 1, September 1) |

The US Edition incorporates the most recent International release plus US extensions. The release-date gap means a US extension may add or revise content released by International earlier.

## 9. Storage considerations

- **SCTIDs are large integers** (up to 18 digits). Store as **string** or **bigint**; do not store as 32-bit int or float.
- **Concept IDs are stable across releases for active concepts.** Deprecated concepts are marked inactive but the ID is retained (do not reuse).
- **Concept inactivation** happens for duplicates, errors, or ambiguous concepts. Inactivated concepts have a **historical association** (e.g., "SAME AS", "REPLACED BY") pointing to the active replacement. Pipelines that filter out inactive concepts must still handle historical references in legacy data.
- **Description IDs** and **Relationship IDs** are also stable identifiers, separately versioned.

## 10. When you'll encounter SNOMED in your work

- **EHR problem-list extracts** - typically SNOMED-coded.
- **FHIR Condition / Procedure / Observation resources** - SNOMED is the most common terminology for clinical concepts (LOINC for labs; RxNorm for medications).
- **HEDIS hybrid measures** that pull from EHR data via SNOMED.
- **eCQM measures** (CQL-authored quality measures) - heavy SNOMED + LOINC use in value sets.
- **Research datasets** (i2b2, OMOP CDM) - often SNOMED-based at the concept layer.
- **Allergy lists** - SNOMED for both reaction (clinical finding) and allergen (substance).

For pure claims-only pipelines, you may never directly handle SNOMED. The day you join EHR data is the day it becomes essential.

## 11. Authoritative source

- **SNOMED International**: <https://www.snomed.org/>
- **NLM SNOMED CT US Edition (UMLS)**: <https://www.nlm.nih.gov/healthit/snomedct/us_edition.html>
- **SNOMED CT Browser** (NLM-hosted public browser): <https://browser.ihtsdotools.org/> (International) and <https://uts.nlm.nih.gov/uts/umls/home> (UMLS / US Edition)
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 12. Common pitfalls

- **Treating SNOMED as flat lookup.** SNOMED is hierarchical; ignoring the IS-A relationships throws away most of its value.
- **Storing SCTID as int / float.** Loses precision for IDs > 2^53.
- **Joining EHR SNOMED to claims ICD-10-CM 1:1.** Always lossy; use the SNOMED→ICD-10-CM map with awareness of map advice, or operate at a code-grouper level.
- **Ignoring "Situation with explicit context".** History-of and family-history concepts are distinct from the disease concepts; treating them as equivalent inflates active-disease counts.
- **Ignoring concept inactivation history.** Legacy data may reference now-inactive concepts; the historical-association table is required for clean longitudinal queries.
- **Conflating International and US Editions.** The US Edition has US extensions; ECL expressions evaluated against International miss US-extension concepts.
- **Not pinning the SNOMED release for ECL-defined value sets.** Hierarchy changes silently change the value-set membership.
