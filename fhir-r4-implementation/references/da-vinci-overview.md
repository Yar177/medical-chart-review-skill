# Da Vinci IG overview

> **Why this file exists:** "Da Vinci" is not a single IG - it's an HL7 program with **dozens** of IGs targeting payer-provider workflows. The ones that matter most for CMS-mandated US payer interop are PDex (payer-to-payer + payer-to-app data exchange), HRex (the cross-IG building blocks), and Plan-Net (provider directories). Prior Authorization (PAS / CRD / DTR) is its own multi-IG ecosystem with depth that warrants a dedicated future skill (`prior-auth-da-vinci`). This file orients implementers across the Da Vinci landscape, covers the three IGs every payer needs to touch, gives a CDS Hooks primer, and explicitly defers PAS / CRD / DTR depth.

Da Vinci program: <https://confluence.hl7.org/spaces/DVP/>. IG index: <https://www.hl7.org/about/davinci/>.

## 1. Da Vinci IG map

| IG | Use | Status |
|---|---|---|
| **HRex** (Health Record Exchange) | Foundational profiles and patterns reused across other Da Vinci IGs. | Foundational. |
| **PDex** (Payer Data Exchange) | Payer-to-payer and payer-to-app health record exchange. Anchors CMS-0057-F Payer-to-Payer API. | In active use; CMS-mandated. |
| **PDex US Drug Formulary** | Formulary publication. | In active use. |
| **PDex Plan-Net** | Provider directories for payer networks. | In active use; anchors CMS Provider Directory API. |
| **PAS** (Prior Authorization Support) | X12 278 + FHIR for prior-auth submission. | Active; future skill. |
| **CRD** (Coverage Requirements Discovery) | CDS Hooks at order-time to surface coverage requirements. | Active; future skill. |
| **DTR** (Documentation Templates and Rules) | Author + run questionnaire-based documentation requirements. | Active; future skill. |
| **CDex** (Clinical Data Exchange) | Provider-to-payer clinical data exchange (records request workflow). | Active. |
| **CRD-CDex-DTR-PAS** ecosystem | The four IGs work together for end-to-end prior-auth + documentation flows. | Active. |
| **Member Attribution** | Attribute members to providers / ACOs. | Active. |
| **Risk-Adjustment** | Risk-adjustment data exchange. | Active. |
| **Notifications (Da Vinci Notifications / DaVinci Subscription Notifications)** | Event notifications using SubscriptionTopic patterns. | Active. |

This file covers PDex, HRex, and Plan-Net at orientation depth. Other IGs are flagged as future-skill territory.

## 2. HRex - the building blocks

HRex defines reusable profiles, extensions, capability patterns, and member-match operations used across other Da Vinci IGs.

Key contributions:

- `$member-match` operation - given a member identity from one payer, look up the matching member in another payer's records. Used in payer-to-payer.
- Task-based and document-based data-exchange patterns.
- Shared profiles (e.g., HRex Patient demographics profile) that extend or align with US Core.
- Consent profile for cross-organization data exchange.

Version pin example: `http://hl7.org/fhir/us/davinci-hrex/StructureDefinition/hrex-patient-demographics|1.0.0`.

## 3. PDex - payer-to-payer + payer-to-app

PDex defines the FHIR mechanics for two CMS-mandated flows:

### 3.1 Payer-to-app (member access)

Overlaps heavily with CARIN BB. PDex profiles **layer on top of** US Core (for clinical) + CARIN BB (for claims) plus PDex-specific additions:

- Consent for app-level data sharing.
- Provenance enriched with payer-specific source attribution.
- Profiles for member-attributed risk-score / coverage history (where applicable).

### 3.2 Payer-to-payer

CMS-0057-F mandates the Payer-to-Payer API (effective Jan 1, 2027 for impacted payers). PDex defines:

- The `$member-match` operation for member identification across payers.
- The Bulk Data + Async patterns for transferring member records.
- Consent capture and propagation across payer boundaries.
- Provenance attribution: the receiving payer must record the source payer.

Spec: <https://hl7.org/fhir/us/davinci-pdex/>.

## 4. Plan-Net - provider directories

Plan-Net defines profiles for publishing a payer's provider network - anchoring the CMS Provider Directory API.

Profile catalog:

- `plannet-Practitioner`
- `plannet-PractitionerRole`
- `plannet-Organization`
- `plannet-OrganizationAffiliation`
- `plannet-Location`
- `plannet-HealthcareService`
- `plannet-Endpoint`
- `plannet-Network`
- `plannet-InsurancePlan`

The Plan-Net surface is **public** (no auth required for read). A consumer can query "all in-network primary care physicians in zip 02115" by combining `PractitionerRole`, `Organization`, `Location`, `HealthcareService`, and `Network` references.

Search-param expectations include `name`, `specialty`, `location.address-postalcode`, `network`, `active`. Inferno has a Plan-Net kit.

Pin extension URLs at IG version (e.g., `http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Practitioner|1.1.0`).

Spec: <https://hl7.org/fhir/us/davinci-pdex-plan-net/>.

## 5. CDS Hooks primer

CDS Hooks is the open standard for invoking clinical decision support from an EHR at specific workflow points (e.g., order-entry, encounter-start). Several Da Vinci IGs (especially CRD, DTR) use CDS Hooks as the transport.

Spec: <https://cds-hooks.org/>.

### 5.1 The model

- **Hook**: a workflow event in the EHR (e.g., `order-select`, `order-sign`, `patient-view`, `encounter-start`).
- **Hook service**: an HTTPS endpoint that responds to the hook with cards.
- **Card**: a UI element (text + optional action link + optional suggestion) the EHR renders to the clinician.
- **Discovery**: hook services publish a `/cds-services` discovery endpoint listing the hooks they handle.

### 5.2 Flow

1. EHR reaches a workflow point (e.g., user signs an order).
2. EHR POSTs a hook request to the hook service URL with context (patient, encounter, order being signed):

   ```json
   {
     "hook": "order-sign",
     "hookInstance": "abc-123",
     "fhirServer": "https://ehr.example.org/fhir",
     "fhirAuthorization": { "access_token": "...", "scope": "...", "expires_in": 300 },
     "context": {
       "userId": "Practitioner/dr-001",
       "patientId": "p-001",
       "draftOrders": { "resourceType": "Bundle", "entry": [...] }
     }
   }
   ```

3. Hook service responds with cards:

   ```json
   {
     "cards": [
       {
         "summary": "Prior auth required for this MRI",
         "indicator": "warning",
         "detail": "Coverage requirements: ...",
         "source": { "label": "Payer CRD", "url": "..." },
         "suggestions": [
           {
             "label": "Open DTR questionnaire",
             "uuid": "...",
             "actions": [{ "type": "create", "description": "...", "resource": {...} }]
           }
         ],
         "links": [{ "label": "Open SMART app", "url": "https://dtr-app.example.org/launch", "type": "smart" }]
       }
     ]
   }
   ```

4. EHR renders cards inline at the order-sign step.

### 5.3 Da Vinci use of CDS Hooks

- **CRD** uses CDS Hooks to surface coverage requirements at order time.
- **DTR** uses CDS Hooks (often via card-launched SMART apps) to run questionnaire-based documentation collection.
- Both depend on the EHR supporting the hook + cards rendering.

Full CRD / DTR / PAS depth is out of scope for this skill (future `prior-auth-da-vinci`); this primer is enough to recognize CDS-Hooks-shaped designs.

## 6. CARIN BB vs PDex (when to use which)

| Use case | IG |
|---|---|
| Member-facing app reading EOB from member's own payer | CARIN BB (with US Core for clinical) |
| Member moving from Payer A to Payer B; Payer A sends records to Payer B | PDex (uses CARIN BB profiles for the claims slice) |
| New payer requesting prior payer's data for a newly-enrolled member | PDex (Payer-to-Payer API per CMS-0057-F) |
| Member granting third-party app access to their member portal | CARIN BB + SMART App Launch |

## 7. Worked example - payer-to-payer member-match

> **[synthetic]** Member moves from Payer A to Payer B. Payer B receives the new-enrollment file, then needs to fetch the prior 5 years of records from Payer A.

1. Payer B authenticates to Payer A's PDex endpoint with SMART Backend Services.
2. Payer B calls `$member-match` with the member's demographics + Payer A coverage identifier:

   ```
   POST [paya-base]/Patient/$member-match
   Content-Type: application/fhir+json

   {
     "resourceType": "Parameters",
     "parameter": [
       {
         "name": "MemberPatient",
         "resource": { "resourceType": "Patient", "identifier": [{...}], "name": [{...}], "birthDate": "..." }
       },
       {
         "name": "CoverageToMatch",
         "resource": { "resourceType": "Coverage", "subscriberId": "...", "...": "..." }
       }
     ]
   }
   ```

3. Payer A returns the matched Patient (or no-match).
4. Payer B requests Bulk Data `$export` against the matched Patient (or a Group containing the matched Patient).
5. Payer B ingests the export.
6. Payer B records `Provenance` for every imported resource attributing source to Payer A.

## 8. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Confusing CARIN BB and PDex roles (they overlap on EOB but the use case differs)
- Implementing PDex without HRex foundational profiles (some PDex profiles inherit from HRex)
- Missing Provenance on payer-to-payer imports (CMS-0057-F requires source attribution)
- Skipping `$member-match` and trying to match members on demographics alone (false-positive risk)
- Plan-Net behind auth (it should be public; auth is an Inferno fail)
- Conflating CDS Hooks with FHIR Subscriptions (different transports, different events)
- Trying to fit PAS/CRD/DTR into this skill (defer to future `prior-auth-da-vinci`)

## 9. What this skill does NOT cover (yet)

- **PAS** - the X12 278 + FHIR prior-auth submission protocol. Deep operational + payer-back-office surface.
- **CRD** - coverage-requirements discovery at order-time. CDS-Hooks-shaped; deep payer integration.
- **DTR** - documentation templates (Questionnaire + QuestionnaireResponse) with rules engine.
- **CDex** - clinical-data records-request workflow (provider-to-payer).

These will be covered in a future `prior-auth-da-vinci` skill. For now, recognize that requests in these domains are scoped to that future skill and defer.

## 10. Related references

- HRex / PDex / Plan-Net profile patterns build on → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- CARIN BB EOB (used inside PDex) → [`carin-bb-ig.md`](carin-bb-ig.md)
- US Core foundational profiles (Patient, Practitioner, Organization, Coverage) → [`us-core-ig.md`](us-core-ig.md)
- SMART Backend Services for payer-to-payer auth → [`smart-on-fhir.md`](smart-on-fhir.md) §7
- Bulk Data export for payer-to-payer transfer → [`bulk-data-export.md`](bulk-data-export.md)
- Subscription / SubscriptionTopic for Da Vinci notifications → [`operations.md`](operations.md) §7-8
- Conformance testing (Inferno Da Vinci kits) → [`conformance-testing.md`](conformance-testing.md)
