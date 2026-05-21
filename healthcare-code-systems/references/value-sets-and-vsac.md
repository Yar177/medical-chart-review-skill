# Value sets and VSAC

> **Why this file exists:** A **value set** is a named, versioned collection of codes from one or more code systems that satisfies some clinical concept (e.g., "diabetes diagnosis codes", "ACE inhibitor / ARB medications"). HEDIS measures, eCQMs, public health surveillance, and clinical decision support all depend on value sets. Getting their **versioning** and **definition style** (intensional vs expansion) right is what keeps them stable.

## 1. What a value set is

A value set has three layers:

1. **Identity**: a name + OID + version. Stable across systems that reference it.
2. **Definition**: how the included codes are determined. Two styles - intensional and expansion (see §3).
3. **Expansion**: the concrete list of codes that satisfy the definition for a given code-system release.

A value set is **not** the same as a code set. The same value set definition applied to ICD-10-CM FY2024 vs FY2026 may produce a different expansion as codes are added or revised.

## 2. OIDs

- **OID** = **Object Identifier** = a dotted numeric string (e.g., `2.16.840.1.113883.3.464.1003.103.12.1001`).
- Globally unique identifier scheme inherited from ISO/ITU.
- Every value set in VSAC has an OID; the NCQA HEDIS value sets each have OIDs; eCQM value sets have OIDs.
- OIDs are **stable**: the same OID points to the same conceptual value set across versions. The **version metadata** is separate.

When referencing a value set in measure logic, pipeline configuration, or documentation, **cite the OID + version**, not the human-readable name (which can be ambiguous across publishers).

## 3. Intensional vs expansion definitions

### Intensional definition

The value set is defined by a **rule** (or set of rules) that selects codes from a code system based on properties:

```
SNOMED CT: descendantsOrSelfOf(73211009 |Diabetes mellitus|)
ICD-10-CM: codes matching pattern E10.*, E11.*, E13.*
RxNorm: descendantsOf(IN 6809 |Metformin|) at TTY = SCD
```

**Pros**: stable across code-system releases (new codes meeting the rule are automatically included), traceable to clinical intent, smaller artifact.

**Cons**: requires a terminology engine to expand, results can change silently as the underlying code system updates.

### Expansion definition

The value set is the **explicit enumeration** of codes:

```
E10.10, E10.11, E10.21, E10.22, E10.29, E10.311, E10.319, ...
```

**Pros**: deterministic; same value set, same expansion, every time.

**Cons**: must be re-generated when the code system updates; large artifact; new codes meeting the clinical intent are silently excluded until the expansion is refreshed.

### Best practice

For production use, publish **both**:

- **Intensional definition** in the source (authoritative; expresses intent).
- **Pinned expansion** at a stated code-system release date (deterministic; what the pipeline actually uses for the period).

Refresh the expansion on a documented schedule tied to code-system release dates.

## 4. VSAC - the Value Set Authority Center

- **VSAC** = **NLM Value Set Authority Center**.
- The US **authoritative** repository for value sets used in eCQMs, HEDIS, public health, and various federal programs.
- Free, requires UMLS account.
- Web UI: <https://vsac.nlm.nih.gov/>
- API: standards-based (SVS, FHIR Terminology Service).

### What's in VSAC

- **eCQM value sets** for CMS / ONC electronic clinical quality measures (drives CMS hospital and eligible-clinician quality programs).
- **HEDIS value sets** published by NCQA each measurement year.
- **Public health surveillance** value sets (CSTE, CDC).
- **U.S. Core Data for Interoperability (USCDI)** value sets.
- **Promoting Interoperability** (formerly Meaningful Use) value sets.

### Versioning in VSAC

- Each value set has an **OID** (stable) and an **expansion** keyed to a stated **release date**.
- NLM publishes the expansion for each VSAC release.
- HEDIS value sets follow the **NCQA HEDIS Measurement Year** versioning (separate publication schedule from VSAC).

## 5. NCQA HEDIS value set directory

- NCQA publishes value sets for HEDIS measures **per measurement year (MY)**.
- Distributed via the **HEDIS Measurement Year [YYYY] Value Set Directory** (Excel + import package).
- **Subject to NCQA licensing**: HEDIS measure specifications and value sets are licensed; commercial use and redistribution require an NCQA license.
- Annual MY release in late summer / fall prior to the measurement year.

The `hedis-nlp` skill in this repo consumes these value sets as the **input** to per-measure extraction logic.

## 6. SNOMED ECL value sets

For value sets defined over SNOMED CT, the **Expression Constraint Language (ECL)** is the native definition mechanism. See [`snomed-ct.md`](snomed-ct.md) §5.

```
<< 73211009                     All descendants of and including Diabetes mellitus
<< 73211009 MINUS << 11530004   Diabetes mellitus excluding brittle diabetes
^ 700043003                     Members of reference set with that ID
```

ECL is far more expressive than enumerated lists and is the SNOMED-native way to publish value sets.

## 7. Value set composition patterns

Beyond intensional / expansion, common composition patterns:

- **Single code system**: all members from one system (e.g., ICD-10-CM only, or LOINC only).
- **Multi-code-system**: members across systems for the same clinical concept (e.g., diabetes = ICD-10-CM codes + SNOMED codes + ICD-9-CM codes for historical periods).
- **Union / intersection / exclusion** of other value sets - common in FHIR ValueSet composition.
- **Grouping value set**: a value set whose members are other value sets (the FHIR ValueSet.compose.include syntax supports this).

## 8. Value set lifecycle in a pipeline

1. **Author** intensional definition (or import from VSAC / NCQA).
2. **Pin to a code-system release date** and expand.
3. **Cache** the expansion in a versioned warehouse table.
4. **Reference** the value set by OID + version in measure logic / extraction code.
5. **Monitor** for code-system release events; refresh expansion when needed.
6. **Version-bump** the local copy when intensional definition changes or when expansion changes materially.
7. **Archive** prior versions for retrospective / longitudinal use.

A `value-set` table in a warehouse typically has: `oid`, `version`, `code_system`, `code`, `code_system_version`, `expansion_date`, `source` (VSAC / NCQA / custom), with appropriate indexes for join performance.

## 9. The `value-set-manifest.md` template

The [`../templates/value-set-manifest.md`](../templates/value-set-manifest.md) template captures a declarative spec for a value set: identity (name + OID + version), purpose, code-system(s) and versions, intensional definition (where applicable), expansion source, expansion date, change-management process, downstream consumers.

## 10. Common pitfalls

- **Expansion-only value sets without intensional backup.** The expansion silently goes stale as the code system updates.
- **Intensional-only without pinned expansion.** Non-deterministic results across pipeline runs as the terminology service evolves.
- **OID drift.** Renaming a value set without preserving the OID breaks every downstream reference.
- **Cross-MY drift in HEDIS pipelines.** Using last year's value sets against this year's measurement period silently mis-numerates.
- **VSAC expansion pulled fresh on every pipeline run.** Inflates the chance of mid-run definition drift; cache the expansion at a pinned date.
- **Value set defined on the wrong code-system version.** A SNOMED ECL expression evaluated against International Edition may miss US Edition extensions.
- **Embedded inline code lists in pipeline code** instead of an externalized value-set artifact. The definition is hidden in code, change history is invisible, and review / audit becomes painful.
- **Redistribution of NCQA HEDIS or AMA CPT value sets** without appropriate licensing.
- **No documented refresh schedule.** Without a process, the expansion is updated on an ad-hoc basis driven by ad-hoc demand.
- **HEDIS Measurement Year confusion**: NCQA's MY versioning is distinct from the calendar year of execution; document both in the manifest.

## 11. Authoritative sources

- **VSAC**: <https://vsac.nlm.nih.gov/>
- **NCQA HEDIS Value Set Directory**: <https://www.ncqa.org/hedis/> (licensed product).
- **FHIR ValueSet specification**: <https://hl7.org/fhir/valueset.html>
- **SNOMED ECL specification**: <https://confluence.ihtsdotools.org/display/DOCECL>
- See [`sources-and-licensing.md`](sources-and-licensing.md).
