# Common pitfalls

> **Why this file exists:** Every FHIR mistake costs an Inferno cycle, a re-export, or worse - silent data corruption. This file collects the 15 most common implementation errors that map 1:1 to SKILL.md §6 Red-Flag Triggers, plus a final note on Provenance / AuditEvent gaps where the FHIR design surface meets the HIPAA audit-log program (deferred to `hipaa-compliance`).
>
> All example payloads, identifiers, URLs, and Bundle snippets in this file are `[synthetic]` placeholders.

Each pitfall: brief example → correct pattern → cross-reference.

## 1. Matching on `identifier.value` without `identifier.system`

**Wrong:**

```
GET [base]/Patient?identifier=M-12345
```

Returns every Patient with `M-12345` in any identifier slot - MRN, account number, foreign payer ID. Cross-system collision is silent.

**Right:**

```
GET [base]/Patient?identifier=http://payer.example.org/member|M-12345
```

The `system|value` pair is the contract. Always include the system.

→ See [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §3.

## 2. Ignoring `meta.versionId` / `ETag` on writes

**Wrong:** Read a Patient, modify locally, `PUT` it back without `If-Match`. Concurrent updaters overwrite each other's changes (last-write-wins, silently).

**Right:** Capture `ETag` from the read response, send `If-Match: W/"<versionId>"` on the write. Server returns 409 / 412 on conflict; retry with re-read.

→ See [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §5.

## 3. `_total=accurate` on a hot search endpoint

**Wrong:** UI requests `GET [base]/Observation?patient=p-001&_total=accurate&_count=20`. Server has to count every matching row before returning the page. On large datasets, this is a full-table scan per request.

**Right:** Use `_total=none` (default in many servers) and rely on `Bundle.link.next` for pagination. Use `_total=estimate` when an approximate count is acceptable.

→ See [`search-parameters.md`](search-parameters.md) §6.

## 4. `_include` / `_revinclude` without server `_count` cap

**Wrong:** `GET [base]/MedicationRequest?patient=p-001&_include=MedicationRequest:medication&_include=MedicationRequest:requester` with no `_count`. Server may try to assemble thousands of related resources into one Bundle.

**Right:** Always set a `_count` (e.g., 100). Servers should enforce a max `_count` regardless. Plan iterative pagination.

→ See [`search-parameters.md`](search-parameters.md) §6, [`bundles-and-transactions.md`](bundles-and-transactions.md) §4.

## 5. Treating must-support as "must populate"

**Wrong:** Treating `mustSupport=true` on `Patient.telecom` as "every Patient must have telecom." Failing validation on patients without phone numbers.

**Right:** Must-support means: the server must support the element if data exists; producers populate when known; receivers must handle if received. Missing data is allowed (consider Data Absent Reason for known-missing).

→ See [`profiles-and-conformance.md`](profiles-and-conformance.md) §3.2, [`us-core-ig.md`](us-core-ig.md) §3.

## 6. Mixing R4 / R4B / R5 in one server

**Wrong:** Storing R4 Patients and R5 SubscriptionTopics in the same server, or accepting `meta.profile` URLs from different FHIR versions in one resource.

**Right:** Pick one FHIR base version per server. If migrating, run parallel endpoints (`/fhir-r4/...` and `/fhir-r5/...`) with a clear migration plan.

→ See [`resource-taxonomy.md`](resource-taxonomy.md) §3, [`operations.md`](operations.md) §7-8 (Subscription R4 vs R5).

## 7. Storing FHIR JSON without `meta.profile` pinning

**Wrong:** Resource lands in storage with no `meta.profile`. Later, profile updates ship and the validator can't tell which profile the resource was authored against. Downstream consumers can't apply version-specific rules.

**Right:** Always set `meta.profile = ["<canonical-url>|<version>"]` on writes. Pin the IG version.

→ See [`profiles-and-conformance.md`](profiles-and-conformance.md) §2, [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §4.

## 8. Conditional create without `If-None-Exist`

**Wrong:** Retry a failed POST → duplicate row with new id.

```
POST [base]/Patient
{...same payload as before...}
```

**Right:** Use `If-None-Exist` header with a search expression that uniquely identifies the resource.

```
POST [base]/Patient
If-None-Exist: identifier=http://payer.example.org/member|M-12345
{...payload...}
```

Server returns existing resource on match, creates on no-match, errors on multi-match.

→ See [`resource-identity-and-versioning.md`](resource-identity-and-versioning.md) §5, [`bundles-and-transactions.md`](bundles-and-transactions.md) §5.

## 9. Transaction Bundle cross-entry refs without `urn:uuid:`

**Wrong:** Transaction Bundle with `Observation.subject.reference = "Patient/temp-1"` where the Patient entry uses `fullUrl: "Patient/temp-1"` but no real id exists yet.

**Right:** Use `urn:uuid:` placeholders for entries with `request.method = POST`. The server resolves them transactionally.

```json
{ "fullUrl": "urn:uuid:abc-123", "resource": {...Patient...}, "request": { "method": "POST", "url": "Patient" } }
{ "fullUrl": "urn:uuid:xyz-789", "resource": { "...", "subject": { "reference": "urn:uuid:abc-123" } }, "request": { "method": "POST", "url": "Observation" } }
```

→ See [`bundles-and-transactions.md`](bundles-and-transactions.md) §3.

## 10. Ignoring `OperationOutcome.issue.severity`

**Wrong:** Treat any HTTP 2xx as success. Server returns `200 OK` with an `OperationOutcome` containing `severity=error` issues (e.g., terminology-validation failed but resource accepted as-is per server policy). Downstream consumes as if conformant.

**Right:** Always parse `OperationOutcome` returned with successful writes. Treat `severity=fatal|error` as blocking. Log `warning`.

→ See [`operations.md`](operations.md) §9, [`conformance-testing.md`](conformance-testing.md) §8.

## 11. SMART v1 scopes when server advertises v2

**Wrong:** Server's `.well-known/smart-configuration` advertises v2 scopes (`patient/Observation.rs`). Client requests v1-style `patient/Observation.read`. Server returns `invalid_scope`.

**Right:** Inspect the server's `capabilities` and `scopes_supported` in discovery; use the matching scope grammar. v2 scopes use `c`/`r`/`u`/`d`/`s` letters + optional `?` query qualifier.

→ See [`smart-on-fhir.md`](smart-on-fhir.md) §3.

## 12. Bulk-export polling without honoring `Retry-After`

**Wrong:** Client polls the `Content-Location` URL every 100ms. Server returns `429 Too Many Requests`. Client retries faster.

**Right:** Honor `Retry-After` header on 202 and on 429. Use exponential backoff with the server's advice. Bulk exports may take hours; polling cadence should be seconds-to-minutes.

→ See [`bulk-data-export.md`](bulk-data-export.md) §4.

## 13. Custom search param without declared `SearchParameter`

**Wrong:** Server supports `GET [base]/Observation?custom-tag=foo` but publishes no `SearchParameter` resource. Clients have no machine-readable contract; future changes break clients silently.

**Right:** Define a `SearchParameter` resource, register it in the `CapabilityStatement.rest.resource.searchParam`, expose its canonical URL.

→ See [`operations.md`](operations.md) §6, [`search-parameters.md`](search-parameters.md) §8.

## 14. R4 Subscription where R5 SubscriptionTopic expected

**Wrong:** Da Vinci notifications spec (uses R5 SubscriptionTopic backport for R4). Implementer ships an R4-style Subscription with `criteria=Observation?...`. Subscriber expects `topic` reference; integration fails.

**Right:** Read the IG. For R4 implementations of topic-based subscriptions, use the **R5 SubscriptionTopic Backport for R4** IG. For pure-R4 simple subscriptions, use R4 Subscription. For R5, use SubscriptionTopic + Subscription.

→ See [`operations.md`](operations.md) §7-8, [`da-vinci-overview.md`](da-vinci-overview.md) §1.

## 15. Missing `Provenance` / `AuditEvent` on writes

**Wrong:** Writes to the FHIR store with no `Provenance` (source attribution) and no `AuditEvent` (access log). USCDI requires Provenance. HIPAA Security Rule requires audit logs.

**Right (FHIR design surface):**

- Write `Provenance` alongside resources where USCDI / US Core / PDex requires it. US Core 6.1.0 includes `us-core-provenance`.
- Emit `AuditEvent` (or use server-side audit infrastructure) on reads and writes for HIPAA audit logs.

**HIPAA program design - defer:** The audit-log *program* (retention period, monitoring, anomaly detection, breach-investigation use of logs, who reviews logs) is HIPAA Security Rule administrative + technical safeguards work. Defer to `hipaa-compliance` (§ Technical Safeguards, § Incident Response).

→ See [`us-core-ig.md`](us-core-ig.md) §2.10, `hipaa-compliance/references/technical-safeguards.md` (audit log requirements).

## Related references

- Anti-patterns summary → `../SKILL.md` §7
- Conformance testing → [`conformance-testing.md`](conformance-testing.md)
- Reading `OperationOutcome` → [`operations.md`](operations.md) §9
