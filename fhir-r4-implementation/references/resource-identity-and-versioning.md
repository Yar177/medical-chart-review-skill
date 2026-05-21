# Resource identity and versioning

> **Why this file exists:** Every FHIR write hinges on three decisions that are easy to get silently wrong: (1) how this resource references other resources (reference vs contained vs `_include` / `_revinclude`); (2) how the server tracks the version of this resource (`meta.versionId`, ETag, `If-Match`); and (3) what the canonical URL of any profile or extension on this resource means. The decisions are independent but they interact - a `meta.versionId` race overwrites a profile-pinned resource if the writer ignored ETag; a contained resource cannot be referenced by `_include` because it has no `id` outside the parent. Get these wrong once and the bug shows up in production weeks later as a "missing" or "duplicated" resource.

## 1. Three ways to relate resources

### 1.1 Reference (the default)

A resource at a known URL points at another resource at another known URL:

```json
{
  "resourceType": "Encounter",
  "id": "encounter-1234",
  "subject": { "reference": "Patient/patient-5678" },
  "...": "..."
}
```

- Both resources exist as independently addressable URLs.
- The reference is a string of the form `ResourceType/id` (relative) or a full absolute URL.
- The referenced resource has its own version history, its own profile, its own search visibility.
- **Default choice for almost everything.** Use this unless one of the conditions below applies.

### 1.2 Contained (only when the referenced resource has no independent existence)

A resource embedded inline inside another resource, with no independent URL:

```json
{
  "resourceType": "MedicationRequest",
  "id": "mr-1",
  "contained": [
    {
      "resourceType": "Medication",
      "id": "med-inline",
      "code": { "...": "..." }
    }
  ],
  "medicationReference": { "reference": "#med-inline" },
  "...": "..."
}
```

- The `#`-prefixed reference points inside the containing resource.
- The contained resource **cannot be searched independently**, **cannot be referenced by other resources**, and **cannot be `_include`d** (it has no URL).
- Use only when the inner resource is meaningless without the parent (typically a one-off `Medication` for a one-off `MedicationRequest`, or a one-off `Practitioner` whose details aren't worth a top-level URL).
- US Core and CARIN BB generally **discourage contained** in favor of independent references, because contained breaks reusability and search.

### 1.3 `_include` / `_revinclude` (a search-time decision, not a modeling decision)

References stay as references; the search response inlines related resources alongside the matched resources:

- `_include=Encounter:subject` - for each matched Encounter, include the referenced Patient.
- `_revinclude=Observation:patient` - for each matched Patient, include Observations that reference the Patient.

This is a **search-server-side join**, not a data-modeling choice. It does not change how the data is stored. See [`search-parameters.md`](search-parameters.md) §6.

### 1.4 Decision tree

```
Does the referenced resource have a useful independent existence?
- yes → reference (§1.1) - almost always the answer
- no  → contained (§1.2) - only for one-off, never-reused inner resources

Do you need the related resource alongside the matched one in a search response?
- yes → reference + _include / _revinclude (§1.3) - search-time, not modeling
- no  → reference alone (client can do a follow-up read)
```

### 1.5 Common worked example

> **[synthetic]** A US Core `Observation.subject` references a `Patient` that already exists as a top-level resource:
>
> ```json
> {
>   "resourceType": "Observation",
>   "id": "obs-101",
>   "meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab|6.1.0"] },
>   "status": "final",
>   "subject": { "reference": "Patient/p-001" },
>   "code": { "...": "..." },
>   "valueQuantity": { "...": "..." }
> }
> ```
>
> Wrong: containing the `Patient` inside the `Observation`. Patient is independently addressable, has its own history, and is referenced by hundreds of other resources.

## 2. Resource identity

A FHIR resource has three identity layers:

1. **Logical id** (`Resource.id`): server-assigned (or client-assigned at create time, if the server supports it). Stable for the life of the resource.
2. **URL**: `BaseURL/ResourceType/id` (for a server-managed resource) - globally addressable.
3. **Business identifier** (`Resource.identifier`): zero or more domain identifiers (MRN, NPI, subscriber ID). Required for US Core Patient, US Core Practitioner, etc.

### 2.1 Logical id vs business identifier

| | Logical id (`Resource.id`) | Business identifier (`Resource.identifier`) |
|---|---|---|
| Set by | Server (or client at create) | Source-of-truth system (MRN issuer, NPPES, payer) |
| Format | Server-defined (UUID, monotonic, opaque) | Domain-specific (MRN, NPI, member ID) |
| Search by | `_id=` | `?identifier=system|value` |
| Stability | Stable for life of resource on this server | Stable to the extent the source system keeps it stable |
| Cardinality | 0..1 | 0..* |

### 2.2 Identifier matching anti-pattern

**Always match on `identifier.system + value`, never on `identifier.value` alone.** An MRN value of `12345` is meaningless without the issuing organization's identifier system. Cross-system value collisions are silent and very common.

```
Wrong: ?identifier=12345
Right: ?identifier=http://hospital.example.org/mrn|12345
```

See [`common-pitfalls.md`](common-pitfalls.md) for the full anti-pattern.

## 3. Resource versioning

Every server-managed FHIR resource has a **version chain** tracked in `meta.versionId`:

```json
{
  "resourceType": "Patient",
  "id": "p-001",
  "meta": {
    "versionId": "7",
    "lastUpdated": "2026-05-15T14:32:10Z"
  },
  "...": "..."
}
```

- Each update increments `meta.versionId`.
- The server exposes the version chain via `_history`:
  - `GET [base]/Patient/p-001/_history` - all versions of this resource.
  - `GET [base]/Patient/p-001/_history/3` - version 3 specifically (vread).
- The server returns an HTTP `ETag` header on read, matching `meta.versionId`.

### 3.1 Concurrency control with `If-Match`

To prevent lost-update race conditions on concurrent writes, the client sends `If-Match: W/"7"` on the PUT:

```
PUT [base]/Patient/p-001
If-Match: W/"7"
Content-Type: application/fhir+json

{ "resourceType": "Patient", "id": "p-001", ... }
```

- If the server's current version is `7`, the update succeeds and becomes version `8`.
- If the server's current version is `≥ 8` (someone else wrote between this client's read and write), the server returns `412 Precondition Failed`.
- The client must re-read, re-apply changes, and retry.

**Anti-pattern:** ignoring ETag / `If-Match`. The lost-update bug is real, common, and silent until reconciliation reveals it weeks later. See [`common-pitfalls.md`](common-pitfalls.md).

### 3.2 Conditional create (`If-None-Exist`)

To prevent duplicates on retry, conditional create uses `If-None-Exist`:

```
POST [base]/Patient
If-None-Exist: identifier=http://hospital.example.org/mrn|12345
Content-Type: application/fhir+json

{ "resourceType": "Patient", ... }
```

- If zero matches exist, the server creates and returns `201 Created`.
- If exactly one match exists, the server returns `200 OK` with the existing resource (no create).
- If multiple matches exist, the server returns `412 Precondition Failed`.

Without `If-None-Exist`, a network retry of a POST creates a duplicate. The retry-safety pattern for create is conditional create.

### 3.3 Conditional update / delete

`PUT [base]/Patient?identifier=http://hospital.example.org/mrn|12345` - update if exactly one match, create if no match, error if multiple matches.

`DELETE [base]/Patient?identifier=http://hospital.example.org/mrn|12345` - delete if exactly one match, no-op if no match, error if multiple matches (unless server allows multi-delete).

## 4. Canonical URLs

A **canonical URL** uniquely identifies a conformance artifact (profile, extension, value set, code system, operation) globally. Canonical URLs are pinned in `meta.profile`, in `code.coding.system`, in `extension.url`, and elsewhere.

### 4.1 Canonical URL structure

```
http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient
http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0
```

- Without a version pin, the URL points at "the current version" - fragile.
- With a `|version` suffix, the URL pins a specific version - required for any production / conformance work.

### 4.2 Where canonical URLs appear

| Slot | Example | Notes |
|---|---|---|
| `meta.profile` | `"meta": { "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"] }` | Claim that this resource conforms to this profile. Use the version-pinned form. |
| `code.coding.system` | `"system": "http://loinc.org"` | Code system identifier (no version unless code-system-version-specific). |
| `extension.url` | `"url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"` | Extension identifier. |
| `ValueSet.url`, `CodeSystem.url`, etc. | `"url": "http://hl7.org/fhir/ValueSet/observation-status"` | Self-identifier of the conformance artifact. |

### 4.3 Profile pinning rule

**Every payload that claims conformance to a profile must list the profile canonical URL in `meta.profile`, version-pinned.**

```json
{
  "resourceType": "Patient",
  "id": "p-001",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"
    ]
  },
  "...": "..."
}
```

Without the pin, downstream validators may pick a different version, the result drifts, and conformance is not reproducible. See [`profiles-and-conformance.md`](profiles-and-conformance.md).

## 5. References - relative vs absolute vs logical

| Form | Example | When |
|---|---|---|
| **Relative** | `"reference": "Patient/p-001"` | Resource is on the same server as the referencer. Default for most US payer / EHR-app work. |
| **Absolute** | `"reference": "https://other-server.example.org/fhir/Patient/p-001"` | Resource is on a different server (cross-server reference). Rare in US payer interop; sometimes used in Da Vinci payer-to-payer flows. |
| **URN / logical** | `"reference": "urn:uuid:..."` | Inside a transaction Bundle, for cross-entry references resolved server-side. See [`bundles-and-transactions.md`](bundles-and-transactions.md). |
| **Reference with identifier only** | `"identifier": { "system": "...", "value": "..." }` (no `reference` string) | When the URL is not known but the business identifier is. Server may resolve, may not. Use only when the literal reference is genuinely unknown. |

### 5.1 Reference resolution rules

- The referencer **must not assume** the server has resolved the reference. Many servers store the reference as a string and resolve only on `_include`.
- Clients **must not assume** a returned resource has all its references pre-resolved. Use `_include` / `_revinclude` to request inlining in a single round-trip.

## 6. `_history` - version-aware reads

- `GET [base]/Patient/p-001/_history` - bundle of all historical versions.
- `GET [base]/Patient/p-001/_history/3` - version 3 read (vread).
- `GET [base]/Patient/_history` - history across all Patients on the server (rare; mostly diagnostic).
- `GET [base]/_history` - history across all resources on the server (very rare).

Useful for:

- Auditing (when did this resource change?)
- Reconstructing point-in-time state for analytics or restatement.
- Investigating a `Provenance` chain.

Combined with `Provenance` resources, `_history` gives a full audit trail. See HIPAA audit-log program design in `hipaa-compliance/references/technical-safeguards.md`.

## 7. Worked example - full create + update sequence

> **[synthetic]** A SMART app creates a new Patient, then updates it with concurrency control.

### Step 1 - conditional create

```
POST [base]/Patient
If-None-Exist: identifier=http://hospital.example.org/mrn|12345
Content-Type: application/fhir+json

{
  "resourceType": "Patient",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0"]
  },
  "identifier": [
    {
      "system": "http://hospital.example.org/mrn",
      "value": "12345"
    }
  ],
  "name": [{ "family": "[synthetic]", "given": ["[synthetic]"] }],
  "gender": "female",
  "birthDate": "1980-01-01"
}
```

Server returns `201 Created`:

```
HTTP/1.1 201 Created
Location: [base]/Patient/p-001/_history/1
ETag: W/"1"
Content-Type: application/fhir+json

{ "resourceType": "Patient", "id": "p-001", "meta": { "versionId": "1", ... }, ... }
```

### Step 2 - read + update with `If-Match`

```
GET [base]/Patient/p-001
```

Returns `ETag: W/"1"` and the resource. Client modifies and PUTs:

```
PUT [base]/Patient/p-001
If-Match: W/"1"
Content-Type: application/fhir+json

{ "resourceType": "Patient", "id": "p-001", "telecom": [{ "system": "phone", "value": "555-0100" }], ... }
```

Server returns `200 OK`:

```
HTTP/1.1 200 OK
ETag: W/"2"
Location: [base]/Patient/p-001/_history/2
```

### Step 3 - concurrent update (would fail without `If-Match`)

If another writer updated the resource between step 2's GET and PUT, the server returns `412 Precondition Failed`. The client must re-read and retry.

## 8. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Matching on `identifier.value` without `identifier.system`
- Ignoring `meta.versionId` / ETag on writes (lost-update race)
- Conditional create without `If-None-Exist` (duplicate on retry)
- Containing a resource that's referenced elsewhere (breaks `_include`)
- Profile reference without version pin (`meta.profile` without `|x.y.z`)
- Storing a relative reference but assuming the server pre-resolved it

## 9. Related references

- Search-time inlining → [`search-parameters.md`](search-parameters.md) §6 `_include` / `_revinclude`
- Transaction-Bundle `urn:uuid:` cross-refs → [`bundles-and-transactions.md`](bundles-and-transactions.md)
- Profile semantics on `meta.profile` → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- `Provenance` / `AuditEvent` shape → [`profiles-and-conformance.md`](profiles-and-conformance.md) (resource mechanics); HIPAA audit-log program design → `hipaa-compliance/references/technical-safeguards.md`
