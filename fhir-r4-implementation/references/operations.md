# Operations

> **Why this file exists:** Anything that doesn't fit the REST CRUD + search model is a FHIR **operation** - invoked with `$operationName` after a base, type, or instance URL. Operations cover validation (`$validate`), terminology (`$expand`, `$validate-code`, `$translate`), patient-everything (`$everything`), bulk export (`$export`), subscriptions, and any custom operation an IG defines. They share a common request / response shape via the `Parameters` resource. This file covers the standard operations every implementer touches, plus the Subscription / `SubscriptionTopic` shift between R4 and R5 (the most common operations-area migration question).

## 1. Invocation patterns

| Level | URL shape | Use |
|---|---|---|
| System | `[base]/$op` | System-wide (e.g., `$export` system-level). |
| Type | `[base]/Patient/$op` | Across all instances of a type (e.g., `$validate` against a profile, `$export` patient-level). |
| Instance | `[base]/Patient/p-001/$op` | Against a specific resource (e.g., `$everything`, `$validate` of an updated resource, custom `$risk-score`). |

Invocation HTTP method:

- `POST` with a `Parameters` resource body (general case, especially for complex inputs).
- `GET` with URL query parameters (allowed only when the operation has no in-parameters of type `Resource`, and the operation is `affectsState=false`).

## 2. `Parameters` resource

The standard input / output envelope for operations:

```json
{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "resource", "resource": { "resourceType": "Patient", "...": "..." } },
    { "name": "profile", "valueUri": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0" }
  ]
}
```

A parameter can carry a `value[x]` (primitive), a `resource` (nested resource), or sub-parameters (`part[]`).

## 3. `$validate`

Validate a resource against a profile and IG packages loaded on the server.

```
POST [base]/Patient/$validate
Content-Type: application/fhir+json

{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "resource", "resource": { "resourceType": "Patient", "...": "..." } },
    { "name": "profile", "valueUri": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0" }
  ]
}
```

Response: an `OperationOutcome`.

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    { "severity": "error", "code": "invariant", "diagnostics": "us-core-8: ...", "expression": ["Patient.name[0]"] },
    { "severity": "warning", "code": "code-invalid", "diagnostics": "Code 'X' not in value set ..." }
  ]
}
```

Issue severities: `fatal`, `error`, `warning`, `information`. Validators differ on what they treat as warning vs error (typically: missing must-support data → warning; failed required binding → error; failed invariant → error).

See [`fhirpath.md`](fhirpath.md) §14 for reading the FHIRPath expressions in `OperationOutcome.issue`.

## 4. `$expand`, `$validate-code`, `$translate`

Terminology operations covered in [`terminology-services.md`](terminology-services.md).

## 5. `$everything`

`$everything` returns all resources related to a target (patient, encounter, or group).

```
GET [base]/Patient/p-001/$everything?_since=2026-01-01
GET [base]/Encounter/e-001/$everything
GET [base]/Group/g-001/$everything
```

Returns a `Bundle` of type `searchset` containing the target plus every resource that references it (and references those, transitively, depending on server policy).

### 5.1 Parameters

| Parameter | Behavior |
|---|---|
| `_since` | Only include resources updated since this dateTime. |
| `_type` | Restrict to specific resource types. |
| `_count` | Page size. |
| `start`, `end` | Date range for clinical events. |

### 5.2 Caveats

- `$everything` is expensive. Many servers cap recursion depth or response size.
- Use `$export` (Bulk Data) for population-scale equivalents.
- Some servers don't implement `$everything`; check `CapabilityStatement`.

## 6. `$export` (Bulk Data)

Covered in detail in [`bulk-data-export.md`](bulk-data-export.md). Brief: kick off with `POST [base]/$export` (or `Patient/$export`, `Group/g-001/$export`), poll status, retrieve ndjson files.

## 7. Subscription - R4 model

R4 `Subscription` is a single resource that bundles "what to watch" and "what to do":

```json
{
  "resourceType": "Subscription",
  "status": "requested",
  "reason": "Notify when a new Observation for the cohort is created",
  "criteria": "Observation?patient=Group/g-001&_lastUpdated=ge2026-05-15",
  "channel": {
    "type": "rest-hook",
    "endpoint": "https://subscriber.example.org/webhook",
    "payload": "application/fhir+json",
    "header": ["Authorization: Bearer ..."]
  }
}
```

- `criteria` is a search string (with limitations vs full search).
- `channel.type` can be `rest-hook` (most common), `websocket`, `email`, `sms`, `message`.
- The server activates the Subscription (`status: active`), monitors matching events, and POSTs notifications to the endpoint.

### 7.1 R4 Subscription limitations

- The `criteria` syntax is a subset of search; not all search params are supported.
- No standardized batch / topic concept - one Subscription per consumer per criteria.
- Server scalability is implementation-specific.

## 8. Subscription - R5 / R4B model (`SubscriptionTopic` + Subscription)

R5 introduces `SubscriptionTopic`: a server- or IG-defined "event topic" that a Subscription subscribes to. R4 implementations can adopt the **Subscriptions R5 Backport IG** to use the R5 pattern on an R4 server.

```json
{
  "resourceType": "SubscriptionTopic",
  "url": "http://example.org/SubscriptionTopic/new-encounter",
  "status": "active",
  "resourceTrigger": [
    {
      "resource": "Encounter",
      "supportedInteraction": ["create"],
      "fhirPathCriteria": "Encounter.status = 'in-progress'"
    }
  ]
}
```

Subscription references the topic:

```json
{
  "resourceType": "Subscription",
  "status": "requested",
  "topic": "http://example.org/SubscriptionTopic/new-encounter",
  "channelType": { "system": "http://terminology.hl7.org/CodeSystem/subscription-channel-type", "code": "rest-hook" },
  "endpoint": "https://subscriber.example.org/webhook"
}
```

Notifications use `Bundle.type = subscription-notification` (R4B / R5) with a `SubscriptionStatus` first entry.

### 8.1 R4 → R5 Subscription migration path

1. Adopt the **Subscriptions R5 Backport IG** on the R4 server (no full R5 upgrade needed).
2. Define `SubscriptionTopic` resources for the events of interest.
3. Migrate consumers from criteria-based to topic-based Subscriptions.
4. Old criteria-based Subscriptions can coexist during transition.

Backport IG: <https://hl7.org/fhir/uv/subscriptions-backport/>.

## 9. Custom operations

Defined by `OperationDefinition` (see [`profiles-and-conformance.md`](profiles-and-conformance.md) §7). Invoked the same way as standard ops:

```
POST [base]/Patient/p-001/$risk-score
Content-Type: application/fhir+json

{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "modelVersion", "valueString": "v3.2" }
  ]
}
```

Response:

```json
{
  "resourceType": "Parameters",
  "parameter": [
    { "name": "score", "valueDecimal": 0.78 }
  ]
}
```

Declare in `CapabilityStatement.rest.resource.operation` so consumers and conformance kits know it exists.

## 10. `OperationOutcome`

Standard error / warning envelope returned by operations, validation, conditional writes, and many other server responses.

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",            // fatal | error | warning | information
      "code": "invariant",            // standard issue code (see below)
      "details": { "text": "Human-readable message" },
      "diagnostics": "FHIRPath: ...",
      "location": ["Patient.name[0]"],   // deprecated; prefer `expression`
      "expression": ["Patient.name[0]"]
    }
  ]
}
```

### 10.1 Common `issue.code` values

`invalid`, `structure`, `required`, `value`, `invariant`, `security`, `login`, `unknown`, `expired`, `forbidden`, `suppressed`, `processing`, `not-supported`, `duplicate`, `multiple-matches`, `not-found`, `conflict`, `code-invalid`, `extension`, `too-costly`, `business-rule`, `transient`, `lock-error`, `no-store`, `exception`, `timeout`, `incomplete`, `throttled`, `informational`.

Always read the `OperationOutcome` from any non-2xx response. Don't guess from HTTP status alone.

## 11. Worked example - `$validate` with a profile pin

> **[synthetic]** Validate a Patient against US Core Patient 6.1.0:
>
> ```
> POST [base]/Patient/$validate
> Content-Type: application/fhir+json
>
> {
>   "resourceType": "Parameters",
>   "parameter": [
>     {
>       "name": "resource",
>       "resource": {
>         "resourceType": "Patient",
>         "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"] },
>         "identifier": [{ "system": "http://hospital.example/mrn", "value": "12345" }],
>         "name": [{ "use": "official", "family": "[synthetic]", "given": ["[synthetic]"] }],
>         "gender": "female",
>         "birthDate": "1980-01-01"
>       }
>     },
>     { "name": "profile", "valueUri": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0" }
>   ]
> }
> ```
>
> Response: `OperationOutcome` with `issue = []` (or only `information` issues) → resource validates.

## 12. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Using GET on an operation that mutates state (must be POST)
- Forgetting the `Parameters` wrapper on POST input
- Treating `OperationOutcome.issue.severity = warning` as fatal (warnings are informational; pipeline gates should distinguish)
- Migrating to R5 Subscription without the Backport IG (breaks R4 server compatibility)
- Custom operation defined but not declared in `CapabilityStatement` (consumers can't discover it)
- Confusing `$everything` with `$export` (single-patient interactive vs population async)

## 13. Related references

- `$validate` interpretation → [`fhirpath.md`](fhirpath.md) §14 (reading `OperationOutcome` FHIRPath expressions)
- Terminology operations → [`terminology-services.md`](terminology-services.md)
- Bulk Data `$export` → [`bulk-data-export.md`](bulk-data-export.md)
- Custom `OperationDefinition` shape → [`profiles-and-conformance.md`](profiles-and-conformance.md) §7
- Subscriptions R5 Backport IG → <https://hl7.org/fhir/uv/subscriptions-backport/>
