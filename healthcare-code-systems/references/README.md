# references/ - reading order

The 17 reference files in this directory are grouped below by topic. Load only what your task needs; the `SKILL.md` §2 task-routing table is the canonical entry point.

## Diagnosis codes

- [icd10-cm.md](icd10-cm.md) - structure, conventions, Excludes1 / Excludes2, code-first / use-additional, Z-codes, annual Oct 1 update
- [icd10-pcs.md](icd10-pcs.md) - 7-character grid, root operations, body system / body part / approach / device / qualifier
- [icd9-and-legacy.md](icd9-and-legacy.md) - ICD-9-CM legacy handling, ICD-11 awareness, GEMs caveats

## Procedure / service codes

- [cpt-and-modifiers.md](cpt-and-modifiers.md) - Cat I / II / III, E/M codes, modifier catalog (-25, -59, -26, -TC, etc.), AMA licensing
- [hcpcs-level-ii.md](hcpcs-level-ii.md) - J-codes, DME, supplies, quarterly update cycle
- [institutional-billing-codes.md](institutional-billing-codes.md) - revenue codes, type of bill, POS, MS-DRG / APR-DRG / APC

## Clinical content / EHR terminologies

- [snomed-ct.md](snomed-ct.md) - clinical terminology, hierarchies, US Edition, ECL
- [loinc-and-ucum.md](loinc-and-ucum.md) - lab and clinical observations, units of measure

## Pharmacy

- [rxnorm-ndc-and-drugs.md](rxnorm-ndc-and-drugs.md) - RxNorm normalized drug names, NDC (10 vs 11 digit), ATC, commercial drug DBs

## Immunizations / other content

- [immunizations-and-other.md](immunizations-and-other.md) - CVX, MVX, race / ethnicity code sets, HL7 v2 code systems

## Provider / org

- [provider-identifiers.md](provider-identifiers.md) - NPI (Luhn check), NPPES, taxonomy codes, TIN semantics

## Cross-system infrastructure

- [crosswalks.md](crosswalks.md) - GEMs (ICD-9↔10), NDC↔RxNorm, ICD↔SNOMED, LOINC↔CPT, ICD-10→HCC, HCC↔HHS-HCC; cardinality, fallback, QA
- [value-sets-and-vsac.md](value-sets-and-vsac.md) - VSAC, OIDs, intensional vs expansion, NCQA value set directory, ECL for SNOMED
- [code-groupers.md](code-groupers.md) - CCSR, CCS (legacy), Elixhauser, Charlson, CCI / NCCI, BETOS, AHRQ groupers

## Operational

- [versioning-and-drift.md](versioning-and-drift.md) - release cadences, "as-of" snapshots, restatement, longitudinal data
- [sources-and-licensing.md](sources-and-licensing.md) - where to obtain each file; CPT / AMA, UMLS, commercial DB licensing
- [common-pitfalls.md](common-pitfalls.md) - truncated NDCs, decimal storage, Z-code traps, modifier loss, status codes, NOS/NEC

---

## Reading order for common goals

| Goal | Read these, in order |
|---|---|
| **First-time orientation to US healthcare codes** | `icd10-cm.md` → `cpt-and-modifiers.md` → `hcpcs-level-ii.md` → `rxnorm-ndc-and-drugs.md` → `common-pitfalls.md` |
| **Designing a new claims warehouse** | `versioning-and-drift.md` → `sources-and-licensing.md` → `crosswalks.md` → `value-sets-and-vsac.md` → `common-pitfalls.md` |
| **Implementing a HEDIS pipeline** | `value-sets-and-vsac.md` → `icd10-cm.md` → `cpt-and-modifiers.md` → `loinc-and-ucum.md` → `crosswalks.md` |
| **Implementing an HCC pipeline** | `icd10-cm.md` → `crosswalks.md` (ICD-10→HCC section) → `versioning-and-drift.md` → `common-pitfalls.md` (Z-codes, status codes) |
| **Implementing a cost / risk ML model** | `code-groupers.md` → `crosswalks.md` → `rxnorm-ndc-and-drugs.md` → `versioning-and-drift.md` |
| **Migrating ICD-9 data into ICD-10** | `icd9-and-legacy.md` → `icd10-cm.md` → `crosswalks.md` (GEMs section) → `versioning-and-drift.md` |
| **Joining EHR clinical data with claims** | `snomed-ct.md` → `loinc-and-ucum.md` → `crosswalks.md` (ICD↔SNOMED, LOINC↔CPT) |
