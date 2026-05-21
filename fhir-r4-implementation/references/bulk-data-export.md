# Bulk Data export

> **Why this file exists:** Bulk Data Export (`$export`) is the FHIR async-job pattern for population-scale extracts - the surface that powers payer-to-payer transfers, analytics warehousing, research pipelines, and CMS-mandated Bulk Data endpoints. The pattern (kickoff → poll → download ndjson) is small, but the failure modes (rate limits, partial failures, file expiration, async-status loops, scope mismatches) are subtle. This file covers the `$export` mechanics and operational guidance. **Authentication for Bulk Data uses SMART Backend Services - see [`smart-on-fhir.md`](smart-on-fhir.md) §7 for that flow.**

Spec: Bulk Data 2.0.0 - <https://hl7.org/fhir/uv/bulkdata/>.

## 1. Three export scopes

| Scope | URL | Use |
|---|---|---|
| **System** | `[base]/$export` | Everything the client is authorized to see across all patients. Rare; restricted to high-trust use cases. |
| **Patient** | `[base]/Patient/$export` | All resources for all patients (the client is authorized for). Common payer-to-payer pattern. |
| **Group** | `[base]/Group/g-001/$export` | All resources for patients in a defined cohort. Most common - the cohort is curated server-side. |

## 2. Kickoff request

```
POST [base]/Group/g-001/$export
Accept: application/fhir+json
Prefer: respond-async
```

Optional query / form parameters:

| Parameter | Behavior |
|---|---|
| `_outputFormat` | `application/fhir+ndjson` (default and most-supported). |
| `_since` | Only resources updated since this dateTime (incremental export). |
| `_type` | Comma-separated resource types to include: `_type=Patient,Observation,Condition`. |
| `_typeFilter` | Per-type search filter: `_typeFilter=Observation?category=laboratory`. |
| `includeAssociatedData` | `LatestProvenanceResources` (or other server-defined data buckets). |

## 3. Server response - async pattern

If accepted, the server returns `202 Accepted` with a `Content-Location` header pointing at a status URL:

```
HTTP/1.1 202 Accepted
Content-Location: https://server.example.org/fhir/$export-status/job-id
```

The client polls the status URL.

## 4. Status polling

```
GET https://server.example.org/fhir/$export-status/job-id
```

### 4.1 In-progress response

```
HTTP/1.1 202 Accepted
X-Progress: 30% complete
Retry-After: 120
```

- `Retry-After` is in seconds - wait at least this long before the next poll.
- `X-Progress` is informational.

### 4.2 Complete response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "transactionTime": "2026-05-15T14:32:10Z",
  "request": "https://server.example.org/fhir/Group/g-001/$export?_type=Patient,Observation",
  "requiresAccessToken": true,
  "output": [
    { "type": "Patient", "url": "https://server.example.org/files/job-id/Patient-1.ndjson" },
    { "type": "Patient", "url": "https://server.example.org/files/job-id/Patient-2.ndjson" },
    { "type": "Observation", "url": "https://server.example.org/files/job-id/Observation-1.ndjson" }
  ],
  "error": [
    { "type": "OperationOutcome", "url": "https://server.example.org/files/job-id/error-1.ndjson" }
  ]
}
```

- One or more ndjson files per resource type.
- `error` entries point at ndjson files of `OperationOutcome` resources - per-resource issues that didn't halt the export.
- `requiresAccessToken: true` → the client must present the Bearer token when downloading file URLs.

### 4.3 Error response

```
HTTP/1.1 5xx
Content-Type: application/fhir+json

{
  "resourceType": "OperationOutcome",
  "issue": [{ "severity": "error", "code": "..." }]
}
```

## 5. Downloading ndjson files

```
GET https://server.example.org/files/job-id/Patient-1.ndjson
Authorization: Bearer ...
Accept: application/fhir+ndjson
```

Each file is **newline-delimited JSON**: one FHIR resource per line, no array wrapper. Process line-by-line for memory efficiency at scale.

### 5.1 File expiration

Server-defined. Most servers expire files 24-72 hours after export completion. Document and respect the server's expiration; re-running an export is costly.

## 6. Cancellation

```
DELETE https://server.example.org/fhir/$export-status/job-id
```

Returns `202 Accepted`. Server may take time to actually stop the job; subsequent polls return `404` once cleaned up.

## 7. Authorization - SMART Backend Services

Bulk Data clients use SMART Backend Services (`client_credentials` + signed JWT assertion + JWKS). Scopes use `system/` grammar:

```
system/Patient.rs system/Observation.rs system/Condition.rs
```

The full auth flow is in [`smart-on-fhir.md`](smart-on-fhir.md) §7. Key points specific to Bulk Data:

- Scope grammar: `system/[Type].rs` (or `system/*.rs` for all).
- Access token must include all resource types you intend to extract.
- The same token used for kickoff is typically used for file download (some servers issue per-file URLs with embedded auth; check server docs).

## 8. Common worked example - incremental Group export

> **[synthetic]** A payer running incremental nightly extracts for a Medicare Advantage cohort to feed their analytics warehouse.

1. Backend Services auth: obtain access token with scopes `system/Patient.rs system/Observation.rs system/Condition.rs system/Encounter.rs system/Procedure.rs system/MedicationRequest.rs system/AllergyIntolerance.rs system/Immunization.rs system/ExplanationOfBenefit.rs`.
2. Kickoff:

   ```
   POST [base]/Group/medicare-advantage-cohort/$export?_since=2026-05-14T00:00:00Z&_type=Patient,Observation,Condition,Encounter,Procedure,MedicationRequest,AllergyIntolerance,Immunization,ExplanationOfBenefit
   Authorization: Bearer ...
   Accept: application/fhir+json
   Prefer: respond-async
   ```

3. Receive `202 Accepted` with `Content-Location: https://server.example.org/fhir/$export-status/job-2026-05-15`.
4. Poll with exponential backoff respecting `Retry-After` header. Common pattern: start at 60s, cap at 600s.
5. On `200 OK`, parse `output` and `error` arrays.
6. Download files in parallel (respecting server rate limits - many cap at 5-10 concurrent downloads).
7. Process ndjson line-by-line into the warehouse.
8. Record `transactionTime` as the `_since` for tomorrow's incremental.

## 9. Operational guidance

### 9.1 Rate limits

Servers enforce concurrency caps on `$export` kickoffs and file downloads. Common caps: 1-2 active jobs per client, 5-10 concurrent file downloads. Hitting limits returns `429 Too Many Requests` with `Retry-After`.

### 9.2 Partial failures

A per-resource validation failure does **not** halt the export. The failed resource appears in the `error` ndjson files as an `OperationOutcome`. Treat `error` files as first-class output - they tell you what your input data couldn't model.

### 9.3 Idempotency / retries

A `$export` kickoff is **not** idempotent - re-kicking off creates a new job. Track in-progress jobs in your pipeline to avoid duplicate kickoffs.

### 9.4 File integrity

- Validate ndjson files line-by-line (skip lines that fail JSON parse, log + alert).
- Optionally, run `$validate` on a sample of resources for profile-conformance spot-checks.
- Use `transactionTime` as the as-of date for downstream warehousing.

### 9.5 Cost / quota

Bulk Data jobs are expensive. Servers may bill per-job, per-byte, or per-resource. Schedule overnight off-peak. Avoid full-history exports when incremental (`_since`) works.

## 10. Bulk Data export from a Group resource

A `Group` resource defines the cohort:

```json
{
  "resourceType": "Group",
  "id": "medicare-advantage-cohort",
  "type": "person",
  "actual": true,
  "member": [
    { "entity": { "reference": "Patient/p-001" } },
    { "entity": { "reference": "Patient/p-002" } },
    ...
  ]
}
```

For a payer-curated cohort, the `Group` is server-managed. For a client-defined cohort, the client may POST a `Group` first, then `$export` against it.

## 11. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Forgetting `Prefer: respond-async` (server may return synchronous error or unexpected behavior)
- Polling without honoring `Retry-After` (rate-limited; export gets queued behind your own polls)
- Not handling `error` ndjson files (silently dropping per-resource failures)
- Assuming files persist forever (download promptly within expiration window)
- Bulk Data without Backend Services auth (no `patient/`-scoped tokens work here)
- Re-kicking the same export on retry (duplicate jobs, doubled cost)
- Incremental `_since` based on local wall-clock instead of server-returned `transactionTime` (drift / gaps)

## 12. Related references

- SMART Backend Services auth → [`smart-on-fhir.md`](smart-on-fhir.md) §7
- `OperationOutcome` shape in error ndjson → [`operations.md`](operations.md) §10
- Conformance testing for Bulk Data → [`conformance-testing.md`](conformance-testing.md) (Inferno Bulk Data kit)
- Bulk Data 2.0 IG → <https://hl7.org/fhir/uv/bulkdata/>
