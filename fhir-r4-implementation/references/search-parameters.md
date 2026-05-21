# Search parameters

> **Why this file exists:** FHIR search is the API surface every implementer touches every day, and it is the surface where subtle mistakes are most expensive. A `Patient.name` search by default does case-insensitive starts-with matching, not exact match. A `_revinclude=Observation:patient` against a population of 1M patients can take down a server. A chained `Encounter:subject.name=Smith` quietly returns nothing if the chained search parameter isn't supported on that server. This file covers the search syntax, modifiers, prefixes, chaining, `_has`, pagination, and the per-resource search-parameter cheatsheets that catch ~80% of FHIR search bugs.

## 1. Search basics

A FHIR search is a GET to a resource type with parameters in the query string:

```
GET [base]/Patient?family=Smith&birthdate=ge1980
```

Returns a `Bundle` of type `searchset`:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 42,
  "link": [
    { "relation": "self", "url": "..." },
    { "relation": "next", "url": "..." }
  ],
  "entry": [
    { "fullUrl": "...", "resource": { "resourceType": "Patient", "id": "...", ... }, "search": { "mode": "match" } },
    ...
  ]
}
```

Each entry has `search.mode`:

- `match` - matched by the query.
- `include` - pulled in by `_include` / `_revinclude`.
- `outcome` - an `OperationOutcome` describing search issues.

## 2. Search parameter types

Every search parameter has a **type** that determines its syntax. The type is defined by the resource's `SearchParameter` definitions (e.g., <https://hl7.org/fhir/R4/searchparameter-registry.html>).

| Type | Example | Notes |
|---|---|---|
| `string` | `?family=Smith` | Default: case-insensitive, accent-insensitive, starts-with match. |
| `token` | `?identifier=http://hospital.example/mrn\|12345` | Coded value; `system\|value` form. Exact match. |
| `reference` | `?subject=Patient/p-001` | Reference to another resource. Can be chained. |
| `date` / `dateTime` | `?birthdate=ge1980-01-01` | Prefix-based comparison. Date precision affects matching. |
| `number` | `?probability=gt0.5` | Numeric comparison with prefix. |
| `quantity` | `?value-quantity=gt5.4\|http://unitsofmeasure.org\|mg` | Value + unit. |
| `uri` | `?url=http://hl7.org/fhir/StructureDefinition/...` | Exact URL match. |
| `composite` | `?code-value-quantity=loinc\|2339-0$gt7\|http://unitsofmeasure.org\|mmol/L` | Multi-component param joined by `$`. |
| `special` | varies | Resource-specific (e.g., `near` on Location). |

## 3. Modifiers

A modifier suffixes a parameter name with `:modifier` and changes the matching semantics. Server support varies - not every server implements every modifier.

### 3.1 String modifiers

| Modifier | Behavior | Example |
|---|---|---|
| (none) | Case-insensitive, accent-insensitive, starts-with | `?family=Smi` matches `Smith`, `smith`, `Smíth` |
| `:exact` | Case-sensitive, accent-sensitive, full string | `?family:exact=Smith` only matches `Smith` |
| `:contains` | Case-insensitive substring match | `?name:contains=mith` matches `Smith`, `Smithers` |

### 3.2 Token modifiers

| Modifier | Behavior |
|---|---|
| (none) | Exact match on `system + code`. |
| `:not` | Match resources where the token is **not** the given value. |
| `:text` | Match against the text representation of the coded value. |
| `:in` | Match if the token is in a given value set: `?code:in=http://hl7.org/fhir/ValueSet/observation-codes`. |
| `:not-in` | Inverse of `:in`. |
| `:above` | Match if the token is an ancestor of the given code (terminology-server-dependent). |
| `:below` | Match if the token is a descendant of the given code (e.g., all ICD-10 codes under `E11`). |
| `:of-type` | For `identifier`: match on type code + system + value. |

### 3.3 Reference modifiers

| Modifier | Behavior |
|---|---|
| (none) | Match by reference. |
| `:identifier` | Match the referenced resource by its `identifier` rather than its URL. Example: `?subject:identifier=http://hospital.example/mrn\|12345`. |
| `:[type]` | Disambiguate a polymorphic reference: `?subject:Patient=...`. |

### 3.4 Universal modifiers

| Modifier | Behavior |
|---|---|
| `:missing=true` | Match resources where the parameter is **absent**. `?gender:missing=true`. |
| `:missing=false` | Match resources where the parameter is **present**. |

## 4. Prefixes (date / number / quantity)

A prefix prepends the value. Applies to `date`, `dateTime`, `number`, `quantity`.

| Prefix | Meaning |
|---|---|
| `eq` | Equal (default if no prefix). |
| `ne` | Not equal. |
| `gt` | Greater than. |
| `lt` | Less than. |
| `ge` | Greater than or equal. |
| `le` | Less than or equal. |
| `sa` | Starts after (date / period only). |
| `eb` | Ends before (date / period only). |
| `ap` | Approximately (server-defined tolerance, typically ±10%). |

```
GET [base]/Observation?date=ge2026-01-01&date=lt2026-04-01
GET [base]/Observation?value-quantity=gt5.4|http://unitsofmeasure.org|mg
```

Date precision: `2026` matches anything in 2026; `2026-05` matches anything in May 2026; `2026-05-15` matches anything on May 15, 2026. The prefix applies against the **precision-adjusted range**, not the literal string.

## 5. Chaining and reverse chaining (`_has`)

### 5.1 Forward chaining

Search a resource by a parameter on a resource it **references**:

```
GET [base]/Encounter?subject.name=Smith
GET [base]/Encounter?subject:Patient.birthdate=ge1980
```

- `subject.name=Smith` - find Encounters whose Patient has `name=Smith`.
- Chain depth is server-dependent (often capped at 1 or 2).
- Use `:Patient` to disambiguate a polymorphic reference.

### 5.2 Reverse chaining (`_has`)

Search a resource by a parameter on a resource that **references it**:

```
GET [base]/Patient?_has:Observation:patient:code=http://loinc.org|2339-0
```

- Find Patients who have at least one Observation referencing them with `code=...`.
- Syntax: `_has:<ReferencingResourceType>:<ReferenceSearchParam>:<SearchParamOnReferencingResource>=<value>`.
- Reverse chaining is even more expensive than forward chaining; many servers disable it or limit chain depth.

### 5.3 Chained search anti-patterns

- **Assuming all servers support chaining.** The server's `CapabilityStatement` declares which chained search params are supported. Many production servers support only a small subset.
- **Deep chains (>2 hops).** Servers commonly cap at 1-2 hops. Beyond that, refactor to multiple queries.
- **Silent zero-result.** A chained query against an unsupported chained param often returns zero results without error. Always test against a known-positive case during development.

## 6. `_include` and `_revinclude`

Inline related resources in the search response.

### 6.1 `_include`

For each matched resource, include the resources it **references**:

```
GET [base]/MedicationRequest?patient=Patient/p-001&_include=MedicationRequest:requester&_include=MedicationRequest:medication
```

Each included resource appears in the Bundle with `entry.search.mode = "include"`.

### 6.2 `_revinclude`

For each matched resource, include the resources that **reference it**:

```
GET [base]/Patient?_id=p-001&_revinclude=Observation:patient&_revinclude=Condition:subject
```

### 6.3 Iterative include (`_include:iterate`)

Include references on already-included resources:

```
GET [base]/MedicationRequest?patient=Patient/p-001&_include=MedicationRequest:requester&_include:iterate=Practitioner:organization
```

The `:iterate` modifier walks one more hop on the included `Practitioner` resources.

### 6.4 Include all (`*`)

`_include=*` or `_include=MedicationRequest:*` - include all referenced resources. **Dangerous on large result sets**; many servers cap or disable.

### 6.5 Performance caution

`_revinclude` against a high-fanout parameter (`Observation:patient`, `Condition:subject`) can return tens of thousands of resources per Patient. Use only with a narrowed match set (`_id=` or a specific identifier) and a `_count`. See [`common-pitfalls.md`](common-pitfalls.md).

## 7. Pagination

Search responses use **link-based pagination**:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 12345,
  "link": [
    { "relation": "self", "url": "...?_count=100&_offset=0" },
    { "relation": "next", "url": "...?_getpages=abc-token&_offset=100" }
  ]
}
```

- **Always follow `link.relation = next`**, do not construct your own `_offset` URL. The server's `next` URL may embed an opaque token (e.g., cursor or page-id) that the server requires.
- `_count=100` - page size. Many servers cap at 100 or 1000.
- `total` may be omitted (server-defined; computing total can be expensive). Use `_total=accurate | estimate | none` to request a specific behavior on supporting servers.

## 8. Result-shaping parameters

| Param | Behavior |
|---|---|
| `_count=100` | Page size. |
| `_sort=date` | Sort ascending. `_sort=-date` sorts descending. Multi-key: `_sort=patient,-date`. Server support for sort keys is server-defined (see `CapabilityStatement`). |
| `_summary=true` | Return summary view (omits non-summary elements). |
| `_summary=text` | Return only the narrative `text` and a few required elements. |
| `_summary=data` | Return everything except narrative. |
| `_summary=count` | Return only the `total` count, no entries. |
| `_elements=id,name,gender` | Return only the named elements (plus mandatory elements). |
| `_total=none\|estimate\|accurate` | Server-side total computation behavior. |
| `_contained=true` | Return contained resources separately as top-level entries. |
| `_containedType=container\|contained` | Refines `_contained` behavior. |

## 9. Per-resource search-parameter cheatsheet (US payer / EHR-app most-used)

> Full registry: <https://hl7.org/fhir/R4/searchparameter-registry.html>. Per-resource list: each resource page (e.g., <https://hl7.org/fhir/R4/patient.html#search>).

### 9.1 Patient (US Core)

| Param | Type | Notes |
|---|---|---|
| `_id` | token | Logical id. |
| `identifier` | token | Business identifier. Always pair with `system`. |
| `name` | string | Any name part. Starts-with, case-insensitive. |
| `family` | string | Family name only. |
| `given` | string | Given name only. |
| `birthdate` | date | Use prefixes (`ge`, `le`). |
| `gender` | token | `male\|female\|other\|unknown`. |
| `telecom` | token | Phone, email. |
| `address-postalcode`, `address-city`, `address-state` | string | |

### 9.2 Observation (US Core)

| Param | Type | Notes |
|---|---|---|
| `patient` | reference | Use a specific patient; never bare. |
| `subject` | reference | Polymorphic; use `:Patient` modifier. |
| `code` | token | LOINC / SNOMED. Often paired with `value-quantity` in composite. |
| `date` | date | `Observation.effective[x]`. |
| `category` | token | `vital-signs`, `laboratory`, `social-history`, `survey`, ... |
| `status` | token | `final`, `amended`, `preliminary`, `cancelled`, ... |
| `value-quantity` | quantity | Composite-friendly. |
| `code-value-quantity` | composite | `?code-value-quantity=http://loinc.org\|2339-0$gt7\|http://unitsofmeasure.org\|mmol/L`. |

### 9.3 Condition (US Core)

| Param | Type | Notes |
|---|---|---|
| `patient` / `subject` | reference | |
| `code` | token | ICD-10-CM / SNOMED. |
| `category` | token | `problem-list-item`, `encounter-diagnosis`, `health-concern`. |
| `clinical-status` | token | `active`, `recurrence`, `relapse`, `inactive`, `remission`, `resolved`. |
| `verification-status` | token | `unconfirmed`, `provisional`, `differential`, `confirmed`, `refuted`, `entered-in-error`. |
| `onset-date` | date | |

### 9.4 Encounter (US Core)

| Param | Type | Notes |
|---|---|---|
| `patient` / `subject` | reference | |
| `class` | token | `AMB`, `IMP`, `EMER`, ... |
| `type` | token | |
| `status` | token | `in-progress`, `finished`, `cancelled`, ... |
| `date` | date | `Encounter.period`. Supports `ge`, `le`, `sa`, `eb`. |
| `service-provider` | reference | Organization. |
| `participant` | reference | Practitioner. |

### 9.5 MedicationRequest (US Core)

| Param | Type | Notes |
|---|---|---|
| `patient` / `subject` | reference | |
| `status` | token | `active`, `on-hold`, `cancelled`, `completed`, `entered-in-error`, `stopped`, `draft`, `unknown`. |
| `intent` | token | `proposal`, `plan`, `order`, `original-order`, `reflex-order`, `filler-order`, `instance-order`, `option`. |
| `authoredon` | date | |
| `medication` | reference | When `MedicationRequest.medicationReference` is used. |
| `code` | token | When `medicationCodeableConcept` is used (RxNorm). |

### 9.6 ExplanationOfBenefit (CARIN BB)

| Param | Type | Notes |
|---|---|---|
| `patient` | reference | |
| `_lastUpdated` | date | CARIN BB requires this for incremental sync. |
| `type` | token | `pharmacy`, `professional`, `institutional`, `oral`, `vision`. |
| `service-date` | date | |
| `identifier` | token | Claim identifier. |

## 10. Worked example - chained query with `_revinclude`

> **[synthetic]** A SMART app wants to load a patient + all their active conditions and recent lab observations in one round-trip.

```
GET [base]/Patient?_id=p-001
  &_revinclude=Condition:patient
  &_revinclude=Observation:patient
  &_count=200
```

To narrow to *active* conditions and *recent* labs, the SMART app needs separate queries (search filters apply to the matched resource, not to includes):

```
GET [base]/Patient?_id=p-001
GET [base]/Condition?patient=p-001&clinical-status=active&_count=200
GET [base]/Observation?patient=p-001&category=laboratory&date=ge2025-01-01&_count=200&_sort=-date
```

This is more API calls but predictable. The `_revinclude` shortcut is appropriate for small per-Patient fan-out (e.g., `AllergyIntolerance`), not for `Observation`.

## 11. Worked example - composite search

> **[synthetic]** Find Observations where the LOINC code is HbA1c (2339-0) and the value is greater than 7.

```
GET [base]/Observation?code-value-quantity=http://loinc.org|2339-0$gt7|http://unitsofmeasure.org|mmol/L
```

Composite separator is `$`. Each component has its own search-param syntax. Composite parameters are declared per resource in the search-param registry.

## 12. Worked example - `_has` reverse chain

> **[synthetic]** Find all Patients who have at least one Condition with ICD-10 `E11.9` (Type 2 diabetes without complications).

```
GET [base]/Patient?_has:Condition:patient:code=http://hl7.org/fhir/sid/icd-10-cm|E11.9
```

This is the canonical "patients with a condition" query when starting from `Patient`. Equivalent forward query: `GET [base]/Condition?code=...&_include=Condition:patient`, then deduplicate by Patient. Both work; `_has` is cleaner when downstream logic is patient-centric.

## 13. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Assuming `name=Smith` is an exact match (it's starts-with case-insensitive)
- Matching `identifier` without `system`
- Constructing `_offset` URLs manually instead of following `link.next`
- `_revinclude=Observation:patient` without narrowing matches
- Assuming all chained params are supported (always check `CapabilityStatement`)
- Date searches without timezone awareness on `Observation.effective[x]`
- Missing `_count` (server default may be 10, surprising downstream code)

## 14. Related references

- Bundle / pagination response shape → [`bundles-and-transactions.md`](bundles-and-transactions.md)
- `CapabilityStatement.rest.resource.searchParam` declares supported search params → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- Custom search params via `SearchParameter` resource → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- FHIRPath expressions backing search params → [`fhirpath.md`](fhirpath.md)
