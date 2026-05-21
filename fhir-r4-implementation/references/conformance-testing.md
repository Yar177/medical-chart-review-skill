# Conformance testing

> **Why this file exists:** Three different validators check three different things. HAPI Validator CLI checks resource shape against a profile (StructureDefinition + invariants). A FHIR server's `$validate` checks the same but in-context (with terminology services resolving). Inferno runs scripted scenarios that hit your live endpoints and validate the full conformance surface (auth + search + profiles + operations). All three are needed; none replaces the others. Touchstone is HL7's testing platform and offers an alternative scripted approach. Get the layering right and conformance work is tractable.

## 1. The three-layer validation flow

| Layer | Tool | What it checks | When to run |
|---|---|---|---|
| 1. Local resource shape | HAPI Validator CLI (`validator_cli.jar`) | A single resource (or Bundle) against a profile + invariants + extensions. | Per-resource during development; per-export during ETL. |
| 2. In-context resource shape | Server `$validate` operation | Same as Layer 1 plus terminology resolution against the server's terminology service. | After resources land in a FHIR server. |
| 3. End-to-end scenarios | Inferno Framework + IG test kits | Auth + search + profile + operation conformance against a live endpoint. | Pre-release gate; periodic monitoring. |

All three matter. Skipping Layer 1 means you find shape bugs only after server ingestion. Skipping Layer 2 means terminology mismatches go undetected. Skipping Layer 3 means you're not conformant - Layer 1+2 don't check auth, search, pagination, operations, or end-to-end flow.

## 2. Layer 1 - HAPI Validator CLI

The reference open-source FHIR validator, distributed as a Java JAR.

Project: <https://github.com/hapifhir/org.hl7.fhir.core>.

### 2.1 Typical invocation

```
java -jar validator_cli.jar resource.json \
  -version 4.0.1 \
  -ig hl7.fhir.us.core#6.1.0 \
  -ig hl7.fhir.us.carin-bb#2.1.0 \
  -profile http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient
```

Key flags:

- `-version 4.0.1` - FHIR R4. Use `4.3.0` for R4B, `5.0.0` for R5.
- `-ig <package>#<version>` - load an IG package by ID. Repeatable.
- `-profile <url>` - assert the resource against the given profile (overrides `meta.profile`).
- `-tx <url>` - pin a terminology server (default is HL7's `tx.fhir.org`; set to `n/a` for offline).
- `-output <file>` - write structured OperationOutcome.

### 2.2 Output shape

The CLI emits an `OperationOutcome` with `issue[]`. Each issue has `severity` (`fatal`, `error`, `warning`, `information`), `location` (FHIRPath), and `diagnostics` (text). Treat any `error` or `fatal` as blocking. Treat `warning` per-team policy (often blocking for US Core mustSupport gaps).

### 2.3 Validator gotchas

- The validator downloads IG packages on first run; CI needs network access or a pre-populated package cache (`~/.fhir/packages/`).
- Version pinning matters: `-ig hl7.fhir.us.core` without a version pulls "latest" - non-deterministic. Always pin.
- The bundled terminology server can rate-limit. For CI volume, point at a local terminology server or use `-tx n/a` and accept that bound-code validation is skipped.

## 3. Layer 2 - Server `$validate`

Every conformant FHIR server exposes `$validate` at type level or instance level. The server validates against its loaded profiles and resolves terminology against its terminology service.

Two flavors:

- Type-level: `POST [base]/Patient/$validate?profile=...` with a resource body.
- Instance-level: `GET [base]/Patient/123/$validate?profile=...` validates the stored resource.

The response is an `OperationOutcome`. See [`operations.md`](operations.md) §4 for `$validate` details.

Use this for:

- "Will this resource land cleanly in the server?" preflight before write.
- "Does the stored data still conform after profile updates?" periodic audit.

## 4. Layer 3 - Inferno Framework

Inferno is ONC's open-source FHIR conformance testing tool. It runs scripted scenarios against a live FHIR endpoint and reports pass / fail per test.

Project: <https://inferno-framework.github.io/>. Hosted instance: <https://inferno.healthit.gov/>.

### 4.1 Inferno test kits relevant to this skill

| Kit | What it tests | Anchor |
|---|---|---|
| **ONC Certification (g)(10) Standardized API** | Full ONC certification surface - SMART App Launch, US Core, Bulk Data. Mandatory for ONC-certified Health IT. | HTI-1 / HTI-2. |
| **SMART App Launch** | Standalone + EHR launch flows, v2 scopes, PKCE. Often required as a dependency of g(10). | SMART App Launch IG. |
| **Bulk Data** | `$export` kickoff, status polling, file download, NDJSON contents. | Bulk Data IG. |
| **US Core** | Profile conformance + must-support + search params + combinations across all US Core profiles. | US Core IG (per version). |
| **CARIN BB** | EOB profile conformance across the 5 profile families. | CARIN BB IG. |
| **Da Vinci kits** (PDex, Plan-Net, HRex, PAS, CRD, DTR, etc.) | Per-IG conformance. | Each Da Vinci IG. |

### 4.2 How Inferno is typically used

1. Stand up your FHIR endpoint with seed test data and a test client registration.
2. Configure the kit (endpoint URL, auth mode, client credentials, sample patient IDs).
3. Run the test sequence. Inferno walks scenarios (auth → discovery → resource reads → searches → profile validation → operations).
4. Investigate failures using Inferno's per-test request/response trace.
5. Fix; re-run; until green.

### 4.3 Common Inferno failure modes

- **SMART discovery missing or malformed** - `.well-known/smart-configuration` not exposed, or missing required fields. Fix: implement per SMART App Launch IG §5.
- **`aud` rejected** - server doesn't validate `aud` matches its own FHIR base. Fix: per SMART v2.
- **Search-param combination not supported** - Inferno tries a US-Core-mandated combination (e.g., `name + birthdate`) and gets HTTP 400. Fix: declare and implement.
- **Profile validation failure on a sample resource** - must-support element missing, extension URL wrong, code value not in bound value set. Fix per OperationOutcome `location`.
- **Pagination missing** - Inferno requests `_count=20` on a large set and `Bundle.link.next` is absent. Fix: implement next-page links.
- **Bulk export status loop** - `$export` kickoff returns 202 + `Content-Location`, but polling returns wrong shape or no `Retry-After`. Fix per Bulk Data IG.
- **`mustSupport` extensions absent** - US Core Patient missing Race / Ethnicity / Birth Sex extensions on a test patient that has them. Fix.
- **Terminology validation fail** - code submitted is not in the bound `required` value set. Fix the data or use a permitted code.

### 4.4 Inferno modes

- **Hosted (inferno.healthit.gov)** - easiest path; your endpoint must be reachable from public internet.
- **Local Docker** - `docker compose up` from the kit repo. Use when your endpoint isn't public, or when you want sealed CI runs.
- **CI integration** - run local Inferno in CI and gate releases on green runs.

## 5. Touchstone (alternative scripted testing)

Touchstone is HL7's testing platform: <https://touchstone.aegis.net/touchstone/>.

Use cases:

- Scripted test execution against your endpoint with XML/JSON test scripts.
- Interop testing with other vendors (Touchstone-orchestrated peer scenarios).
- Connectathon-style multi-party testing.

Touchstone overlaps with Inferno but is generally more flexible / script-driven; Inferno is more "certified test kit per IG." Many teams use both: Inferno for IG certification, Touchstone for ad-hoc and peer testing.

## 6. Test data and environments

- Keep a dedicated test environment with `[synthetic]` patients. Never run conformance tests against prod with real PHI.
- Seed enough variety to exercise every must-support element + extension + code value. A common gap: test patients with only English names and no race/ethnicity, which hides US Core extension bugs.
- Synthea (<https://synthea.mitre.org/>) generates synthetic patients in FHIR R4 / US Core shape - good seed source.
- Keep test client registrations separate from prod credentials.

## 7. CI integration recipe

A practical gate setup:

1. **Pre-commit / PR check** - HAPI Validator CLI on changed sample resources + on any profile change. Fast (seconds).
2. **Nightly** - Local Inferno against the staging endpoint with US Core + SMART + Bulk Data kits. Slow (minutes).
3. **Pre-release** - Full Inferno kit relevant to the release (US Core, CARIN BB, Da Vinci as applicable) green.
4. **Production smoke** - periodic Inferno health check against prod read-only endpoints.

## 8. Reading OperationOutcome from any layer

All three layers emit `OperationOutcome` (Layer 3 wraps it in Inferno's per-test report). Key fields:

- `issue.severity` - `fatal` and `error` block; `warning` per policy; `information` for context.
- `issue.code` - machine-readable category (e.g., `structure`, `value`, `code-invalid`, `business-rule`).
- `issue.location` (deprecated in R5; use `expression`) - FHIRPath to the offending element.
- `issue.diagnostics` - human-readable detail.

See [`operations.md`](operations.md) §9 for full `OperationOutcome` shape.

## 9. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Treating HAPI Validator pass as "done" (Layer 1 alone, no auth / search / scenarios)
- Running Inferno against prod with real PHI
- Not pinning IG versions in validator runs (non-deterministic)
- Inferno timeouts mistaken for failures (often network or sample-size issues)
- Skipping pre-Inferno preflight ([`templates/smart-app-launch-checklist.md`](../templates/smart-app-launch-checklist.md), [`templates/fhir-conformance-audit.md`](../templates/fhir-conformance-audit.md))

## 10. Related references

- `$validate` operation mechanics → [`operations.md`](operations.md) §4
- Profile mustSupport / slicing semantics → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- Terminology resolution in validation → [`terminology-services.md`](terminology-services.md)
- SMART App Launch test kit dependency → [`smart-on-fhir.md`](smart-on-fhir.md)
- Bulk Data test kit → [`bulk-data-export.md`](bulk-data-export.md)
- US Core / CARIN BB / Da Vinci kit anchors → [`us-core-ig.md`](us-core-ig.md), [`carin-bb-ig.md`](carin-bb-ig.md), [`da-vinci-overview.md`](da-vinci-overview.md)
- HAPI Validator: <https://github.com/hapifhir/org.hl7.fhir.core>
- Inferno: <https://inferno-framework.github.io/>
- Touchstone: <https://touchstone.aegis.net/touchstone/>
