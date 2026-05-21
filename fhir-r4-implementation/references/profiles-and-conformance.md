# Profiles and conformance

> **Why this file exists:** Every US payer / EHR-app FHIR implementation lives or dies on `StructureDefinition` - the resource that defines profiles, extensions, slicing, and must-support semantics. A profile that "looks right" but never validates means the implementation is non-conformant. The profile vocabulary is also the trap-laden one: `mustSupport` does not mean "required"; slicing discriminators have specific semantic rules; extension URLs are global identifiers that must be unique and stable. This file covers the conformance mechanics that every profile author and reviewer needs.

## 1. The conformance resource family

| Resource | Purpose |
|---|---|
| `StructureDefinition` | Defines a profile, extension, or base resource shape. |
| `CapabilityStatement` | Declares what a server / client supports (resources, profiles, search params, operations, security). |
| `OperationDefinition` | Defines a custom operation (`$export`, `$validate`, `$expand`, custom `$risk-score`, etc.). |
| `SearchParameter` | Defines a search parameter (standard or custom). |
| `ImplementationGuide` | Packages a set of profiles + extensions + value sets + examples + narrative pages. |
| `ValueSet`, `CodeSystem`, `ConceptMap` | Terminology (covered in [`terminology-services.md`](terminology-services.md) and in `healthcare-code-systems`). |

## 2. `StructureDefinition` shape

```json
{
  "resourceType": "StructureDefinition",
  "url": "http://example.org/fhir/StructureDefinition/our-patient",
  "version": "1.0.0",
  "name": "OurPatient",
  "status": "active",
  "kind": "resource",
  "abstract": false,
  "type": "Patient",
  "baseDefinition": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient",
  "derivation": "constraint",
  "differential": {
    "element": [
      {
        "id": "Patient.identifier",
        "path": "Patient.identifier",
        "min": 1,
        "mustSupport": true,
        "slicing": {
          "discriminator": [{ "type": "pattern", "path": "type" }],
          "rules": "open"
        }
      },
      {
        "id": "Patient.identifier:MRN",
        "path": "Patient.identifier",
        "sliceName": "MRN",
        "min": 1,
        "max": "1",
        "patternIdentifier": {
          "type": {
            "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR" }]
          }
        }
      }
    ]
  }
}
```

Key fields:

- `url` - canonical URL of the profile (globally unique, version with `version` field).
- `baseDefinition` - the profile this one constrains (could be a base resource or another profile, e.g., constraining US Core Patient further).
- `derivation = constraint` - this profile constrains; `specialization` means it extends (rare outside HL7 / IG work).
- `differential.element` - only the elements that differ from the base. The full picture is the `snapshot` (usually server-generated).

## 3. Cardinality and must-support

### 3.1 Cardinality

`min` / `max` constraints (e.g., `min=1`, `max=1`, `max=*`). A profile can tighten but not loosen the base's cardinality. US Core Patient says `name min=1`; you can profile further to `min=2` but cannot relax to `min=0`.

### 3.2 `mustSupport`

`mustSupport: true` means: **the system claims to support this element if it is present, but the element is not required to be populated**. It is not the same as `min=1`. The IG-level definition of "support" varies - typically it means the element is rendered, persisted, and queryable.

US Core uses `mustSupport` extensively. A US Core Patient declares `name`, `identifier`, `gender`, `birthDate`, `address`, `telecom` as must-support - meaning a conformant server must be able to handle these elements if they're present in a payload, even if a given Patient instance doesn't populate them all.

A conformant profile **must implement** must-support elements. A conformant resource **may or may not populate** them, depending on data availability.

## 4. Slicing

Slicing partitions a repeating element into named sub-collections distinguished by a discriminator.

### 4.1 Discriminator types

| Type | Behavior |
|---|---|
| `value` | Slice by a fixed value at a path inside the element. |
| `pattern` | Slice by a pattern (subset-match) at a path inside the element. |
| `type` | Slice by the FHIR type at a path. |
| `profile` | Slice by which profile the element conforms to. |
| `exists` | Slice by presence / absence of an element. |

### 4.2 Slicing rules

| Rule | Behavior |
|---|---|
| `closed` | Only the declared slices are allowed; no additional elements. |
| `open` | Additional un-sliced elements are allowed. Most common. |
| `openAtEnd` | Additional elements allowed but only after all declared slices. |

### 4.3 Worked example - slicing `Patient.identifier`

> **[synthetic]** Slice `Patient.identifier` into "MRN" and "SSN" by `type`:

```json
{
  "id": "Patient.identifier",
  "path": "Patient.identifier",
  "min": 1,
  "slicing": {
    "discriminator": [{ "type": "pattern", "path": "type" }],
    "rules": "open"
  }
},
{
  "id": "Patient.identifier:MRN",
  "path": "Patient.identifier",
  "sliceName": "MRN",
  "min": 1,
  "max": "1",
  "mustSupport": true,
  "patternIdentifier": {
    "type": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR" }] }
  }
},
{
  "id": "Patient.identifier:SSN",
  "path": "Patient.identifier",
  "sliceName": "SSN",
  "min": 0,
  "max": "1",
  "patternIdentifier": {
    "type": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "SS" }] }
  }
}
```

A conformant Patient has at least one identifier with `type.coding.code = "MR"` (the MRN). It may have a single SSN. Other identifiers are allowed (the slicing rule is `open`).

### 4.4 Slicing anti-patterns

- Slicing with `rules = closed` when production data has unmodeled identifier types → blocks valid data.
- Slicing on `value` when the discriminating value is `Coding` (multi-component) → use `pattern` instead.
- Discriminator path that doesn't uniquely identify a slice → validator can't decide which slice an instance belongs to.

## 5. Extensions

An extension is a `StructureDefinition` of `kind=complex-type` and `type=Extension`. Extensions add elements to a resource without changing the base.

### 5.1 Extension shape

```json
{
  "resourceType": "StructureDefinition",
  "url": "http://example.org/fhir/StructureDefinition/our-patient-locale",
  "version": "1.0.0",
  "kind": "complex-type",
  "type": "Extension",
  "context": [{ "type": "element", "expression": "Patient" }],
  "differential": {
    "element": [
      { "id": "Extension", "path": "Extension", "max": "1" },
      { "id": "Extension.url", "path": "Extension.url", "fixedUri": "http://example.org/fhir/StructureDefinition/our-patient-locale" },
      { "id": "Extension.value[x]", "path": "Extension.value[x]", "min": 1, "type": [{ "code": "code" }] }
    ]
  }
}
```

### 5.2 Using an extension on a resource

```json
{
  "resourceType": "Patient",
  "extension": [
    {
      "url": "http://example.org/fhir/StructureDefinition/our-patient-locale",
      "valueCode": "en-US"
    }
  ]
}
```

### 5.3 `modifierExtension`

`modifierExtension` changes the meaning of containing elements. Use sparingly. A consumer that doesn't understand a modifier extension **must reject the resource**. Standard extensions are skipped silently when unknown.

### 5.4 Extension URL design rules

1. **Globally unique.** Use a URL on a domain you control (`http://example.org/fhir/StructureDefinition/...`).
2. **Stable.** Don't rename URLs across versions. Version with `version` field, not URL change.
3. **Pin in `meta.profile` for the host resource.** Consumers can discover extension definitions by canonical URL lookup.
4. **Use complex extensions for grouped sub-fields.** Don't flatten multi-component data across multiple top-level extensions if it's logically one unit.

### 5.5 Common worked example - US Core Race extension

```json
{
  "resourceType": "Patient",
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {
          "url": "ombCategory",
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2106-3",
            "display": "White"
          }
        },
        {
          "url": "text",
          "valueString": "White"
        }
      ]
    }
  ]
}
```

This is a **complex extension** - multiple sub-extensions under one parent URL.

## 6. `CapabilityStatement`

Declares the FHIR API surface a server exposes (or a client consumes).

```json
{
  "resourceType": "CapabilityStatement",
  "url": "http://example.org/fhir/CapabilityStatement/our-payer-api",
  "version": "1.0.0",
  "status": "active",
  "kind": "instance",
  "fhirVersion": "4.0.1",
  "format": ["application/fhir+json"],
  "rest": [
    {
      "mode": "server",
      "security": {
        "service": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/restful-security-service", "code": "SMART-on-FHIR" }] }],
        "extension": [
          {
            "url": "http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris",
            "extension": [
              { "url": "authorize", "valueUri": "https://example.org/oauth/authorize" },
              { "url": "token", "valueUri": "https://example.org/oauth/token" }
            ]
          }
        ]
      },
      "resource": [
        {
          "type": "Patient",
          "supportedProfile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"],
          "interaction": [
            { "code": "read" },
            { "code": "search-type" }
          ],
          "searchParam": [
            { "name": "_id", "type": "token" },
            { "name": "identifier", "type": "token" },
            { "name": "name", "type": "string" },
            { "name": "birthdate", "type": "date" }
          ]
        }
      ]
    }
  ]
}
```

Served at `GET [base]/metadata`.

### 6.1 What goes in `CapabilityStatement`

- Server URL, FHIR version, supported formats (JSON / XML).
- Security service (`SMART-on-FHIR` typically) + SMART OAuth URIs extension.
- Per-resource: supported profiles, interactions, search params, conditional ops, custom operations.
- For Bulk Data: declare the `$export` operations.

### 6.2 Conformance testing tools read `CapabilityStatement`

Inferno ONC g(10) and similar conformance kits start by retrieving `[base]/metadata`. If the `CapabilityStatement` doesn't declare a profile, the test won't run for it. **Every conformance claim must be reflected in `CapabilityStatement.rest.resource.supportedProfile` and the relevant `searchParam` entries.** A server that supports US Core Patient must list `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0` in `supportedProfile`.

## 7. Custom operations

A custom operation is defined by an `OperationDefinition` resource and invoked with `$operationName`:

```json
{
  "resourceType": "OperationDefinition",
  "url": "http://example.org/fhir/OperationDefinition/risk-score",
  "name": "RiskScore",
  "status": "active",
  "kind": "operation",
  "code": "risk-score",
  "resource": ["Patient"],
  "system": false,
  "type": false,
  "instance": true,
  "parameter": [
    { "name": "modelVersion", "use": "in", "min": 1, "max": "1", "type": "string" },
    { "name": "score", "use": "out", "min": 1, "max": "1", "type": "decimal" }
  ]
}
```

Invocation: `POST [base]/Patient/p-001/$risk-score` with a `Parameters` resource as the request body.

Custom operations are also declared in `CapabilityStatement.rest.resource.operation` or `CapabilityStatement.rest.operation`.

See [`operations.md`](operations.md) for `$validate`, `$expand`, `$validate-code`, `$everything`, and Subscription operations.

## 8. Custom `SearchParameter`

```json
{
  "resourceType": "SearchParameter",
  "url": "http://example.org/fhir/SearchParameter/Patient-state-of-residence",
  "version": "1.0.0",
  "name": "StateOfResidence",
  "status": "active",
  "code": "state-of-residence",
  "base": ["Patient"],
  "type": "token",
  "expression": "Patient.address.where(use = 'home').state"
}
```

Server must reindex to make the new search parameter queryable. Declare in `CapabilityStatement.rest.resource.searchParam`.

## 9. Profile inheritance and versioning

- A profile can derive from another profile (`baseDefinition` points at a profile, not just a base resource).
- Profile version is set with `StructureDefinition.version`.
- When referencing a profile in `meta.profile`, **always pin** with `|version`: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0`. See [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §4.

## 10. Validation flow

Three-layer validation (per the skill's standard workflow):

1. **HAPI FHIR Validator CLI** - local pre-validation against the profile and IG package. Catches structural errors fast.
2. **Server `$validate`** - `POST [base]/Patient/$validate` with the resource as payload. Validates against the server's loaded IG packages.
3. **Inferno** (or equivalent conformance kit) - runs IG-specific test scripts that go beyond `$validate`: SMART launch flow, search behavior, Bundle handling, pagination, etc.

See [`conformance-testing.md`](conformance-testing.md) for the tooling specifics.

## 11. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Confusing `mustSupport` with `min=1` (must-support says "handle if present", not "always populate")
- Slicing on the wrong discriminator type (value vs pattern vs type)
- Closed slicing on data that legitimately has unmodeled values
- Extension URL without a `version` field, then changing the URL across versions (breaks consumers)
- Custom operation invoked at the wrong level (instance vs type vs system)
- Conformance claim in code without matching `CapabilityStatement.supportedProfile` (Inferno won't see it)
- Profile reference in `meta.profile` without `|version` pin
- `modifierExtension` used where a regular `extension` would do (forces consumers to reject)

## 12. Related references

- Pinning in `meta.profile` → [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §4
- `$validate` shape → [`operations.md`](operations.md)
- US Core profile catalog → [`us-core-ig.md`](us-core-ig.md)
- CARIN BB profile catalog → [`carin-bb-ig.md`](carin-bb-ig.md)
- Terminology binding strength (`required`, `extensible`, `preferred`, `example`) → [`terminology-services.md`](terminology-services.md)
- Conformance testing → [`conformance-testing.md`](conformance-testing.md)
