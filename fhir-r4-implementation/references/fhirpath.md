# FHIRPath

> **Why this file exists:** FHIRPath is the expression language that backs FHIR invariants (`StructureDefinition.constraint.expression`), search parameters (`SearchParameter.expression`), `$validate` rule output, profile slicing discriminators, and many extension and operation definitions. You don't need to be a FHIRPath expert to read FHIR - you do need it to write profiles, debug validator failures, and shape custom search parameters. This file covers the most-used FHIRPath patterns for profile authors and conformance reviewers, not the full language spec.

Spec: <https://hl7.org/fhirpath/N1/>. FHIR-specific FHIRPath: <https://hl7.org/fhir/R4/fhirpath.html>.

## 1. Core model

A FHIRPath expression evaluates against a **context** (a resource or part of a resource) and returns a **collection** of items. Every expression result is a collection - even single values are collections of one.

```
context: Patient resource
expression: name.family
result: ["[synthetic]", "[synthetic]"]   (collection of family names)
```

Empty collections are valid (no error, just zero items). `{}` is the empty collection literal.

## 2. Navigation

| Pattern | Meaning |
|---|---|
| `Patient.name` | All `name` elements on the Patient. |
| `Patient.name.family` | All `family` values across all `name` elements. |
| `Patient.name[0]` | First `name` element (0-indexed). |
| `Patient.name.first()` | Same as `[0]` but expressive. |
| `Patient.name.last()` | Last element. |
| `Patient.name.count()` | Cardinality of the collection. |
| `Patient.name.exists()` | True if collection is non-empty. |
| `Patient.name.empty()` | True if collection is empty. |

## 3. Type filters

Polymorphic elements (`value[x]`, `medication[x]`, `effective[x]`, `onset[x]`) are filtered with `ofType()`:

```
Observation.value.ofType(Quantity)
Observation.value.ofType(Quantity).value > 200
Observation.value.ofType(CodeableConcept).coding.where(system = 'http://loinc.org').code
```

`ofType()` returns the items in the collection that match the given type (no items if the polymorphic element is a different type).

`as()` is similar but returns at most one item (cast-like):

```
Observation.value as Quantity
```

## 4. Filtering with `where()`

```
Patient.identifier.where(system = 'http://hospital.example/mrn').value
Patient.name.where(use = 'official').family
Observation.component.where(code.coding.where(system = 'http://loinc.org' and code = '8480-6').exists())
```

`where(expr)` keeps items where `expr` is true.

## 5. Boolean and comparison operators

| Operator | Meaning |
|---|---|
| `=`, `!=` | Equality / inequality (element-wise on collections - use `~` for equivalence). |
| `<`, `<=`, `>`, `>=` | Comparison. |
| `and`, `or`, `xor`, `not()` | Boolean (short-circuit). |
| `in` | `'x' in ('x' \| 'y' \| 'z')` - membership. |
| `contains` | `('x' \| 'y' \| 'z') contains 'x'` - reverse of `in`. |
| `implies` | Logical implication: `A implies B` ≡ `(not A) or B`. Used heavily in invariants. |

## 6. Collection operators

| Operator / function | Meaning |
|---|---|
| `\|` (pipe) | Union of two collections (deduplicated). |
| `first()`, `last()` | First / last item. |
| `tail()` | All but first. |
| `skip(n)`, `take(n)` | Slice. |
| `count()` | Cardinality. |
| `distinct()` | Deduplicate. |
| `union(...)`, `intersect(...)`, `exclude(...)` | Set operations. |
| `single()` | Return the one and only item, error if 0 or >1. |
| `all(criteria)` | True if criteria true for every item. |
| `any(criteria)` | True if criteria true for any item. |
| `exists(criteria)` | Equivalent to `where(criteria).exists()`. |

## 7. Conditionals

```
iif(Patient.gender = 'female', 'F', 'M')
```

`iif(condition, then, else)` is the FHIRPath ternary.

## 8. Strings and numbers

| Function | Behavior |
|---|---|
| `lower()`, `upper()` | Case conversion. |
| `length()` | String length. |
| `startsWith(s)`, `endsWith(s)`, `contains(s)` | Substring matching. |
| `matches(regex)` | Regex match. |
| `replace(target, replacement)` | String replace. |
| `substring(start, length)` | Substring. |
| `toInteger()`, `toDecimal()`, `toString()` | Conversion. |
| `abs()`, `round()`, `floor()`, `ceiling()`, `truncate()` | Numeric. |

## 9. Extensions

```
Patient.extension('http://hl7.org/fhir/us/core/StructureDefinition/us-core-race')
Patient.extension('http://hl7.org/fhir/us/core/StructureDefinition/us-core-race').extension('ombCategory').value.ofType(Coding).code
```

`extension(url)` is shorthand for `extension.where(url = '<url>')`. Always pin the full canonical URL.

## 10. `$this`, `%context`, `%resource`

Inside a `where()` or other filter, `$this` refers to the current item:

```
Observation.component.where($this.code.coding.code = '8480-6')
```

`%resource` refers to the root resource (useful when navigating from deep inside).

## 11. Common FHIRPath patterns

### 11.1 Pull a coded value by code system

```
Observation.code.coding.where(system = 'http://loinc.org').code.first()
```

### 11.2 Check that a value exists and meets a constraint

```
Observation.value.ofType(Quantity).exists() and
Observation.value.ofType(Quantity).value > 0
```

### 11.3 Get all references of a given type from a Bundle

```
Bundle.entry.resource.ofType(Patient)
```

### 11.4 Navigate a `Reference` element

FHIRPath does not auto-resolve references. To get the referenced resource, use `resolve()`:

```
Encounter.subject.resolve().ofType(Patient).name.family
```

`resolve()` is a FHIR-specific addition; only works in contexts where references can be resolved (in-Bundle or with a `%context` server).

### 11.5 Extract a slice value from a sliced array

```
Patient.identifier.where(type.coding.where(system = 'http://terminology.hl7.org/CodeSystem/v2-0203' and code = 'MR').exists()).value.first()
```

This extracts the MRN from a `Patient.identifier` slice keyed on `type`.

## 12. FHIRPath in profile invariants

Profile invariants use FHIRPath in `StructureDefinition.constraint.expression`. Example from US Core Patient (excerpted, paraphrased):

```json
{
  "key": "us-core-8",
  "severity": "error",
  "human": "Patient.name.given or Patient.name.family SHALL be present (or, if neither, the Data Absent Reason Extension SHALL be present).",
  "expression": "(name.given.exists() or name.family.exists()) or name.extension('http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()"
}
```

A `$validate` failure references the invariant key (e.g., `us-core-8`) and the human-readable description. To debug, evaluate the `expression` against the offending resource using a FHIRPath playground (e.g., `fhirpath.js` REPL, HAPI FHIR validator output).

## 13. FHIRPath in SearchParameter

```json
{
  "resourceType": "SearchParameter",
  "id": "Patient-birthdate",
  "code": "birthdate",
  "base": ["Patient"],
  "type": "date",
  "expression": "Patient.birthDate",
  "...": "..."
}
```

The `expression` says which element(s) the search parameter matches against. Custom search parameters require a `SearchParameter` resource with a valid FHIRPath expression and server reindex.

## 14. FHIRPath in `$validate` output

When `$validate` fails an invariant, the response `OperationOutcome.issue` includes the FHIRPath expression that failed, with location pointing at the offending element. Read the expression, evaluate it against the resource, see why it's false.

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "invariant",
      "diagnostics": "us-core-8: Patient.name.given or Patient.name.family SHALL be present...",
      "expression": ["Patient.name[0]"]
    }
  ]
}
```

## 15. Worked example - US Core invariant

> **[synthetic]** A Patient resource fails US Core `us-core-8`:
>
> ```json
> {
>   "resourceType": "Patient",
>   "id": "p-001",
>   "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"] },
>   "identifier": [{ "system": "http://hospital.example/mrn", "value": "12345" }],
>   "name": [{ "use": "official" }],
>   "gender": "female"
> }
> ```
>
> Invariant: `(name.given.exists() or name.family.exists()) or name.extension('http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()`
>
> Evaluation:
>
> - `name.given.exists()` → false
> - `name.family.exists()` → false
> - `name.extension('http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()` → false
>
> All three clauses are false; the invariant evaluates to false; `$validate` reports `us-core-8` violation.
>
> Fix: add `name.family` or `name.given`, or add the Data Absent Reason extension if the name is genuinely unknown.

## 16. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Using `=` (element-wise equality) where you wanted `~` (equivalence)
- Forgetting `ofType()` on a polymorphic `value[x]` (collection is empty when type doesn't match)
- Assuming `resolve()` works without a Bundle / server context
- Using a non-pinned extension URL in `extension(url)` (matches nothing if the resource uses a versioned URL)
- Confusing `exists()` with `not(empty())` (same result, different idiomatic use)
- Treating FHIRPath as XPath (different syntax, different semantics)

## 17. Related references

- Profile invariants → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- Custom `SearchParameter` definitions → [`search-parameters.md`](search-parameters.md) §14, [`profiles-and-conformance.md`](profiles-and-conformance.md)
- `$validate` operation → [`operations.md`](operations.md)
- FHIRPath spec → <https://hl7.org/fhirpath/N1/>
- FHIRPath in FHIR (resolve, slice navigation, etc.) → <https://hl7.org/fhir/R4/fhirpath.html>
