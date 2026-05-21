# Bundles and transactions

> **Why this file exists:** A `Bundle` is the FHIR envelope for everything - search results, document compositions, batch operations, atomic transactions, and async / messaging flows. The `Bundle.type` is the single most consequential field on the resource, because the server processing model changes completely between `searchset`, `batch`, `transaction`, `document`, `message`, and `history`. A transaction Bundle with the wrong `urn:uuid:` reference pattern silently splits one logical resource graph into two disconnected halves. This file covers Bundle types, transaction atomicity, conditional operations inside Bundles, the `urn:uuid:` cross-entry reference pattern, and Bundle chunking strategy.

## 1. Bundle types

The full list (R4): <https://hl7.org/fhir/R4/valueset-bundle-type.html>.

| `Bundle.type` | Use | Atomicity | Cross-entry refs |
|---|---|---|---|
| `document` | A FHIR-native clinical document with a `Composition` as `entry[0]` and referenced resources after. | N/A (read-only typically) | Yes (resolved within the document) |
| `message` | A `MessageHeader`-led message, similar to HL7 v2 messages. | N/A | Yes |
| `transaction` | Atomic multi-operation: all-or-none. | All or none. | Yes, via `urn:uuid:` |
| `transaction-response` | Server's response to a `transaction` POST. | N/A | N/A |
| `batch` | Independent operations: each succeeds or fails on its own. | Per-entry. | No (cross-entry refs cannot resolve). |
| `batch-response` | Server's response to a `batch` POST. | N/A | N/A |
| `searchset` | Search results. | N/A | N/A |
| `collection` | Loose grouping of resources. | N/A | N/A |
| `history` | Resource history (`_history` response). | N/A | N/A |
| `subscription-notification` | (R4B / R5) Subscription notification payload. | N/A | N/A |

## 2. `transaction` vs `batch`

The difference is the single most common Bundle decision.

| | `transaction` | `batch` |
|---|---|---|
| Atomicity | All-or-none. Any failure rolls back all entries. | Per-entry. Failures isolated to the failing entry. |
| Cross-entry references | `urn:uuid:` placeholders resolve server-side. | No cross-entry resolution; each entry is independent. |
| Use when | A graph of resources must commit together (create Patient + Encounter + Observations atomically). | Independent operations where partial success is acceptable (bulk dashboard load of unrelated reads). |
| Returns | `Bundle.type = transaction-response`. | `Bundle.type = batch-response`. |

**Default to `transaction` for any write that creates linked resources.** Use `batch` only when entries are genuinely independent.

## 3. Transaction Bundle anatomy

A transaction Bundle is posted to the base URL:

```
POST [base]
Content-Type: application/fhir+json

{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:p-001",
      "resource": { "resourceType": "Patient", "...": "..." },
      "request": { "method": "POST", "url": "Patient" }
    },
    {
      "fullUrl": "urn:uuid:e-001",
      "resource": {
        "resourceType": "Encounter",
        "subject": { "reference": "urn:uuid:p-001" },
        "...": "..."
      },
      "request": { "method": "POST", "url": "Encounter" }
    }
  ]
}
```

Three structural rules:

1. Each entry has a `fullUrl` (the local id) and a `request` (HTTP method + URL).
2. Cross-entry references use the **referencer's `fullUrl`** as the reference string (typically a `urn:uuid:`).
3. The server resolves `urn:uuid:` references across the Bundle as part of the transaction commit. After commit, the server rewrites references to canonical URLs.

### 3.1 The `urn:uuid:` cross-entry pattern

The `fullUrl` is **not** the final URL of the resource. It's a local Bundle-scoped placeholder. The server assigns the final URL on commit and rewrites all matching `reference` strings within the transaction.

```json
{
  "fullUrl": "urn:uuid:7c2e3a8d-...",
  "resource": { "resourceType": "Patient", "...": "..." },
  "request": { "method": "POST", "url": "Patient" }
}
```

After commit, the server returns a `transaction-response` Bundle with the canonical URLs:

```json
{
  "resourceType": "Bundle",
  "type": "transaction-response",
  "entry": [
    {
      "fullUrl": "[base]/Patient/p-001",
      "response": { "status": "201 Created", "location": "Patient/p-001/_history/1", "etag": "W/\"1\"" }
    },
    {
      "fullUrl": "[base]/Encounter/e-001",
      "response": { "status": "201 Created", "location": "Encounter/e-001/_history/1", "etag": "W/\"1\"" }
    }
  ]
}
```

The order of entries in the response matches the order of entries in the request.

## 4. HTTP methods inside Bundle entries

| Method | Behavior |
|---|---|
| `POST [Type]` | Create new resource. Use with `fullUrl: urn:uuid:...`. |
| `PUT [Type]/[id]` | Update (or create with client-supplied id, if server allows). |
| `PATCH [Type]/[id]` | JSON Patch / FHIRPath Patch (server support varies). |
| `DELETE [Type]/[id]` | Delete. |
| `GET [Type]?...` | Read or search. Allowed in `batch`; some servers allow in `transaction`. |

## 5. Conditional operations inside Bundles

Conditional headers let entries express "create only if not exists" or "update only if version matches" semantics inside a Bundle.

### 5.1 Conditional create (`ifNoneExist`)

```json
{
  "fullUrl": "urn:uuid:p-001",
  "resource": { "resourceType": "Patient", "identifier": [{ "system": "...", "value": "12345" }], "...": "..." },
  "request": {
    "method": "POST",
    "url": "Patient",
    "ifNoneExist": "identifier=http://hospital.example/mrn|12345"
  }
}
```

- If no Patient matches, create. `urn:uuid:p-001` resolves to the new Patient.
- If exactly one Patient matches, no create. `urn:uuid:p-001` resolves to the matched Patient (other entries' references to `urn:uuid:p-001` now point at the matched Patient).
- If multiple match, the entire transaction fails.

### 5.2 Conditional update (`PUT` with search criteria)

```json
{
  "fullUrl": "urn:uuid:p-001",
  "resource": { "resourceType": "Patient", "...": "..." },
  "request": {
    "method": "PUT",
    "url": "Patient?identifier=http://hospital.example/mrn|12345"
  }
}
```

- Match exactly one → update.
- Match zero → create.
- Match multiple → fail.

### 5.3 Conditional update with version control (`ifMatch`)

```json
{
  "fullUrl": "[base]/Patient/p-001",
  "resource": { "resourceType": "Patient", "id": "p-001", "...": "..." },
  "request": {
    "method": "PUT",
    "url": "Patient/p-001",
    "ifMatch": "W/\"7\""
  }
}
```

- If current `versionId` is `7`, update.
- If current `versionId` is `≥ 8`, fail → entire transaction rolls back.

### 5.4 Conditional delete (`DELETE` with search criteria)

```json
{
  "request": {
    "method": "DELETE",
    "url": "Patient?identifier=http://hospital.example/mrn|12345"
  }
}
```

## 6. Worked example - 3-resource transaction with `urn:uuid:`

> **[synthetic]** Create a Patient + Encounter + Observation atomically.

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:p-001",
      "resource": {
        "resourceType": "Patient",
        "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"] },
        "identifier": [{ "system": "http://hospital.example/mrn", "value": "12345" }],
        "name": [{ "family": "[synthetic]", "given": ["[synthetic]"] }],
        "gender": "female",
        "birthDate": "1980-01-01"
      },
      "request": {
        "method": "POST",
        "url": "Patient",
        "ifNoneExist": "identifier=http://hospital.example/mrn|12345"
      }
    },
    {
      "fullUrl": "urn:uuid:e-001",
      "resource": {
        "resourceType": "Encounter",
        "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-encounter|6.1.0"] },
        "status": "finished",
        "class": { "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB" },
        "subject": { "reference": "urn:uuid:p-001" },
        "period": { "start": "2026-05-15T09:00:00Z", "end": "2026-05-15T09:30:00Z" }
      },
      "request": { "method": "POST", "url": "Encounter" }
    },
    {
      "fullUrl": "urn:uuid:o-001",
      "resource": {
        "resourceType": "Observation",
        "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab|6.1.0"] },
        "status": "final",
        "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory" }] }],
        "code": { "coding": [{ "system": "http://loinc.org", "code": "2339-0", "display": "Glucose [Mass/volume] in Blood" }] },
        "subject": { "reference": "urn:uuid:p-001" },
        "encounter": { "reference": "urn:uuid:e-001" },
        "effectiveDateTime": "2026-05-15T09:15:00Z",
        "valueQuantity": { "value": 142, "unit": "mg/dL", "system": "http://unitsofmeasure.org", "code": "mg/dL" }
      },
      "request": { "method": "POST", "url": "Observation" }
    }
  ]
}
```

Server response (success):

```json
{
  "resourceType": "Bundle",
  "type": "transaction-response",
  "entry": [
    { "fullUrl": "[base]/Patient/p-001", "response": { "status": "201", "location": "Patient/p-001/_history/1", "etag": "W/\"1\"" } },
    { "fullUrl": "[base]/Encounter/e-001", "response": { "status": "201", "location": "Encounter/e-001/_history/1", "etag": "W/\"1\"" } },
    { "fullUrl": "[base]/Observation/o-001", "response": { "status": "201", "location": "Observation/o-001/_history/1", "etag": "W/\"1\"" } }
  ]
}
```

If `ifNoneExist` matches an existing Patient, the Encounter and Observation still POST and reference the existing Patient. If the Encounter or Observation fails validation, the entire transaction rolls back - no orphan Patient.

## 7. Bundle chunking strategy

Servers cap transaction Bundle size. Common limits: 100, 500, or 1000 entries; sometimes a payload-size cap (e.g., 10 MB).

### 7.1 When to chunk

- Bulk loads of historical data (e.g., 50,000 historical Conditions for a patient population).
- Cross-server migrations.
- Bulk Data import staging.

### 7.2 Chunking rules

1. **Never split a logical graph across chunks.** If Patient + Encounter + Observations are linked by `urn:uuid:`, they must stay in one transaction. Otherwise the references won't resolve.
2. **Use `batch` if entries are independent.** Easier to retry per-entry on failure.
3. **Idempotency.** Each chunk should be re-runnable safely. Use `ifNoneExist` on creates and `ifMatch` on updates.
4. **Order matters.** For dependent batches across multiple Bundles, process in dependency order (Patients first, then Encounters, then clinical resources).
5. **Track failures explicitly.** A `transaction-response` Bundle with `4xx` / `5xx` on any entry means the entire transaction rolled back; re-queue. A `batch-response` Bundle may have per-entry failures; retry only the failures.

## 8. Document Bundle (`Bundle.type = document`)

A FHIR document is a `Composition`-led Bundle:

```json
{
  "resourceType": "Bundle",
  "type": "document",
  "identifier": { "system": "urn:ietf:rfc:3986", "value": "urn:uuid:..." },
  "entry": [
    { "fullUrl": "urn:uuid:c-001", "resource": { "resourceType": "Composition", "...": "..." } },
    { "fullUrl": "urn:uuid:p-001", "resource": { "resourceType": "Patient", "...": "..." } },
    ...
  ],
  "signature": { "...": "..." }
}
```

- `entry[0]` **must be** the `Composition`.
- The Composition's `subject`, `author`, `section.entry` references resolve within the document.
- Optionally signed; signature covers the canonical-form bundle.
- Common in C-CDA-equivalent FHIR documents and discharge summary delivery. Out of immediate scope for CARIN BB / Patient Access API; primarily relevant for clinical-document interop.

## 9. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Using `batch` for a write where atomicity matters (partial commit, orphan resources)
- `urn:uuid:` reference that doesn't match any entry's `fullUrl` (silent fail / unresolved reference)
- Splitting a logical resource graph across chunks (broken cross-entry refs)
- Conditional create without `ifNoneExist` (duplicate-on-retry)
- Mixing GET and POST in a `transaction` (server support varies - some allow, some don't)
- Bundle entries out of dependency order (server-side: most servers do not auto-reorder)
- Assuming `transaction-response` order matches request order (it does - but assuming "response[0] failed = no creates happened" is correct only because of all-or-none atomicity)

## 10. Related references

- Search Bundles (`searchset`) and pagination → [`search-parameters.md`](search-parameters.md)
- Resource versioning (`ifMatch` semantics) → [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md)
- `OperationOutcome` for error reporting → [`operations.md`](operations.md)
- Bulk Data Export (`$export` returns ndjson files, not Bundles) → [`bulk-data-export.md`](bulk-data-export.md)
