# Terminology services

> **Why this file exists:** FHIR resources are full of coded values, and the codes only make sense against the right code system / value set / version. Picking the wrong `system` URL silently breaks interop. Validating a code without specifying the value-set version drifts as VSAC updates. This file covers the FHIR mechanics of terminology - binding strength, `$expand`, `$validate-code`, and version pinning - and points at `healthcare-code-systems` for the *selection* of code systems and value sets, which is its own discipline.

## 1. Binding strength

A profile binds an element (`code`, `Coding`, `CodeableConcept`) to a value set. The binding has a **strength** that defines how strict the binding is.

| Strength | Meaning |
|---|---|
| `required` | The value **must** come from the bound value set. Validator errors otherwise. |
| `extensible` | The value **should** come from the bound value set if a matching concept exists; otherwise a different code is permitted. |
| `preferred` | The bound value set is a recommendation; other codes are valid. |
| `example` | The bound value set is illustrative only; no constraint. |

US Core typically uses `extensible` for clinical codes (allowing real-world data variability) and `required` for status / category enumerations.

## 2. Value set identifiers - pin the version

```json
{
  "valueSet": "http://hl7.org/fhir/us/core/ValueSet/us-core-condition-code|6.1.0"
}
```

- Without a `|version`, the binding floats with the IG / VSAC update cycle.
- With a `|version`, the binding is reproducible and audit-safe.

This skill's rule: **every value-set reference in a profile or example must be version-pinned**. See `healthcare-code-systems` for the broader version-pinning discipline (terminology-version-pinning.md, value-sets-and-vsac.md, etc.).

## 3. `$expand`

`$expand` expands a value set to its complete list of codes. Useful for client-side value-set rendering, validation, and synchronization.

```
GET [base]/ValueSet/us-core-condition-code/$expand
GET [base]/ValueSet/$expand?url=http://hl7.org/fhir/us/core/ValueSet/us-core-condition-code|6.1.0
POST [base]/ValueSet/us-core-condition-code/$expand
```

Returns the `ValueSet` resource with the `expansion` element populated:

```json
{
  "resourceType": "ValueSet",
  "url": "http://hl7.org/fhir/us/core/ValueSet/us-core-condition-code",
  "version": "6.1.0",
  "expansion": {
    "timestamp": "2026-05-15T...",
    "total": 12345,
    "contains": [
      { "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9", "display": "Type 2 diabetes mellitus without complications" },
      { "system": "http://snomed.info/sct", "code": "44054006", "display": "Diabetes mellitus type 2" },
      ...
    ]
  }
}
```

### 3.1 `$expand` parameters

| Parameter | Purpose |
|---|---|
| `filter` | Text filter for autocompletion. |
| `count` | Page size. |
| `offset` | Pagination. |
| `includeDesignations` | Include alternative display strings (translations). |
| `displayLanguage` | Preferred display language. |
| `valueSetVersion` | Specific version of the input value set (if not in URL). |
| `system-version` | Pin a specific code-system version: `system-version=http://snomed.info/sct\|http://snomed.info/sct/731000124108/version/20240301`. |

### 3.2 Anti-pattern - `$expand` without version pinning

Different terminology servers may resolve the "current" value set to different versions on different days. Always pin both the value-set version and the underlying code-system version for reproducible expansion.

## 4. `$validate-code`

`$validate-code` checks whether a code (or `Coding`, or `CodeableConcept`) is a member of a value set or code system.

```
GET [base]/ValueSet/us-core-condition-code/$validate-code?system=http://hl7.org/fhir/sid/icd-10-cm&code=E11.9
POST [base]/ValueSet/us-core-condition-code/$validate-code
```

POST body (Parameters resource):

```json
{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "url", "valueUri": "http://hl7.org/fhir/us/core/ValueSet/us-core-condition-code|6.1.0" },
    { "name": "coding", "valueCoding": { "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9" } }
  ]
}
```

Response:

```json
{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "result", "valueBoolean": true },
    { "name": "display", "valueString": "Type 2 diabetes mellitus without complications" }
  ]
}
```

If `result = false`, the response includes a `message` parameter explaining why.

### 4.1 `$validate-code` on `CodeSystem`

```
GET [base]/CodeSystem/$validate-code?url=http://snomed.info/sct&code=44054006
```

Checks code membership in the code system itself (not in a value-set view of it).

## 5. `$translate`

`$translate` uses a `ConceptMap` to translate a code from one code system to another (e.g., LOINC ↔ SNOMED, ICD-9-CM ↔ ICD-10-CM).

```
GET [base]/ConceptMap/$translate?url=http://example.org/fhir/ConceptMap/icd9-to-icd10&system=http://hl7.org/fhir/sid/icd-9-cm&code=250.00
```

`ConceptMap` selection is covered in `healthcare-code-systems`.

## 6. Code-system identifiers (common ones)

| Code system | Canonical `system` URL |
|---|---|
| LOINC | `http://loinc.org` |
| SNOMED CT (US edition) | `http://snomed.info/sct` |
| ICD-10-CM | `http://hl7.org/fhir/sid/icd-10-cm` |
| ICD-10-PCS | `http://www.icd10data.com/icd10pcs` (not always - check IG) |
| RxNorm | `http://www.nlm.nih.gov/research/umls/rxnorm` |
| CPT | `http://www.ama-assn.org/go/cpt` |
| HCPCS Level II | `https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets` (verify against IG) |
| NDC | `http://hl7.org/fhir/sid/ndc` |
| CVX (immunizations) | `http://hl7.org/fhir/sid/cvx` |
| UCUM (units) | `http://unitsofmeasure.org` |
| HL7 v2 (e.g., identifier type) | `http://terminology.hl7.org/CodeSystem/v2-0203` |
| HL7 v3 (e.g., encounter class) | `http://terminology.hl7.org/CodeSystem/v3-ActCode` |

**Authoritative reference:** `healthcare-code-systems` maintains the full catalog. Use these identifiers verbatim - typos in `system` URLs are silently treated as a different code system and break interop.

## 7. VSAC and the `valueSetVersion` problem

VSAC (Value Set Authority Center) publishes hundreds of value sets used by quality measures (HEDIS, CMS quality programs). VSAC value sets update on a schedule (some quarterly, some annually for measurement-year alignment).

- **Pin the VSAC version** in `meta.profile`-style canonical references and in `valueSetVersion` parameters.
- **Document the value-set version in your conformance audit**, not just "this resource validates against the US Core Condition value set."

See `healthcare-code-systems/references/value-sets-and-vsac.md` for the VSAC lifecycle, OID conventions, and crosswalk strategies.

## 8. Terminology server architecture

Most production FHIR servers integrate with a dedicated terminology server (Ontoserver, Snowstorm, HAPI FHIR with loaded terminology, FHIR-server-bundled tx services). The terminology server hosts:

- Code systems (SNOMED, LOINC, ICD-10, RxNorm, etc., often as imported packages)
- Value sets (HL7, IG-shipped, VSAC, custom)
- Concept maps
- `$expand`, `$validate-code`, `$translate` operations

The base FHIR server delegates terminology operations to the terminology server. `$validate` on a resource cascades into `$validate-code` calls on coded elements.

## 9. Worked example - validating a Condition code

> **[synthetic]** A US Core Condition has `code.coding = [{ system: "http://hl7.org/fhir/sid/icd-10-cm", code: "E11.9" }]`. The profile binds `Condition.code` to `us-core-condition-code|6.1.0` with `extensible` binding.

Validation flow:

1. `$validate` on the Condition resource.
2. Validator sees the `code` element is bound to `us-core-condition-code|6.1.0`.
3. Validator calls `$validate-code` with `url=us-core-condition-code|6.1.0`, `coding={system: "http://hl7.org/fhir/sid/icd-10-cm", code: "E11.9"}`.
4. Terminology server expands the value set, checks membership, returns `result=true`.
5. Validator passes.

If the code were `E11.999` (not a valid ICD-10-CM code), step 4 returns `result=false`, and the validator reports an `extensible` binding warning (not error, because the binding is extensible).

## 10. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Using `code` without `system` (silent: a bare code is meaningless and most validators flag it)
- Wrong `system` URL (typo, trailing slash, http vs https) → silent treated as different code system
- Floating value-set version (no `|version` pin) → drift across deployments
- Floating code-system version on `$expand` (e.g., SNOMED edition / release date) → expansion drift
- Treating a `required` binding as `extensible` (validator errors not warnings)
- Loading the wrong VSAC measurement-year version → quality-measure mismatch

## 11. Related references

- Code-system / value-set selection, OIDs, VSAC, crosswalks → `healthcare-code-systems` (sibling skill)
- Profile binding declarations → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- `Parameters` resource shape (used by terminology ops) → [`operations.md`](operations.md)
- HEDIS measure value-set lifecycle → `hedis-nlp` (sibling skill, for the measurement-year discipline)
