# Resource taxonomy

> **Why this file exists:** Before authoring or consuming any FHIR resource, you need to know which of the ~145 R4 resources is in scope, which category it belongs to (Foundation / Base / Clinical / Financial / Workflow / Conformance / Admin), how the categorization affects which IG governs it, and how R4 / R4B / R5 differ for the resources you'll touch. The wrong resource choice is the most expensive FHIR mistake - it propagates into every downstream profile, search query, and validator run.

## 1. The seven FHIR resource categories

FHIR R4 organizes ~145 resources into seven categories. The category drives **which IG typically governs the resource**, **which audience uses it**, and **what stability level** it has.

| Category | Examples | Typical IG governance | Stability |
|---|---|---|---|
| **Foundation** | `Bundle`, `OperationOutcome`, `Parameters`, `Binary`, `Subscription`, `Linkage`, `MessageHeader` | Base FHIR spec (no IG profiling typically) | Normative for core types |
| **Base** | `Patient`, `Practitioner`, `PractitionerRole`, `Organization`, `Location`, `HealthcareService`, `Endpoint`, `Person`, `RelatedPerson`, `Group` | US Core, Plan-Net, custom | Normative or trial-use |
| **Clinical** | `Condition`, `Observation`, `Procedure`, `AllergyIntolerance`, `Immunization`, `CarePlan`, `Goal`, `CareTeam`, `MedicationRequest`, `MedicationStatement`, `MedicationDispense`, `MedicationAdministration`, `Medication`, `DiagnosticReport`, `ImagingStudy`, `Specimen`, `BodyStructure`, `FamilyMemberHistory`, `ClinicalImpression` | US Core (USCDI), USCDI++ | Trial use; some normative |
| **Financial** | `Coverage`, `CoverageEligibilityRequest`, `CoverageEligibilityResponse`, `Claim`, `ClaimResponse`, `ExplanationOfBenefit`, `Account`, `ChargeItem`, `Invoice`, `PaymentNotice`, `PaymentReconciliation`, `EnrollmentRequest`, `EnrollmentResponse` | CARIN BB, Da Vinci PDex, Da Vinci PAS | Trial use |
| **Workflow** | `Task`, `Appointment`, `AppointmentResponse`, `Schedule`, `Slot`, `ServiceRequest`, `RequestGroup`, `Communication`, `CommunicationRequest`, `DeviceRequest`, `SupplyRequest`, `SupplyDelivery` | Da Vinci (CRD / DTR / PAS workflows), US Core (some) | Trial use |
| **Conformance** | `StructureDefinition`, `ValueSet`, `CodeSystem`, `ConceptMap`, `CapabilityStatement`, `OperationDefinition`, `SearchParameter`, `ImplementationGuide`, `StructureMap`, `MessageDefinition`, `GraphDefinition`, `ExampleScenario` | Base FHIR + every IG ships these | Normative |
| **Administration** | `Encounter`, `EpisodeOfCare`, `Flag`, `Library`, `List`, `DocumentReference`, `DocumentManifest`, `Composition`, `Basic`, `Provenance`, `AuditEvent`, `Consent`, `Contract` | US Core (`Encounter`, `DocumentReference`), HIPAA-adjacent (`Provenance`, `AuditEvent`, `Consent`) | Trial use |

Source: <https://hl7.org/fhir/R4/resourcelist.html>.

## 2. Which resources matter for which use case

### 2.1 US Core Patient Access API (CMS-9115-F / CMS-0057-F)

The CMS-mandated **Patient Access API** surface, as of CMS-0057-F (effective Jan 1, 2027), is anchored on **US Core** profiles plus CARIN BB for claims and **EHR clinical data**. Minimum resource set:

- **Demographics / coverage:** `Patient`, `Coverage`, `Organization`, `Practitioner`, `PractitionerRole`, `Location`
- **USCDI clinical:** `AllergyIntolerance`, `CarePlan`, `CareTeam`, `Condition`, `DiagnosticReport`, `DocumentReference`, `Encounter`, `Goal`, `Immunization`, `MedicationRequest`, `Observation` (Lab + Vitals + Smoking Status + Social History), `Procedure`, `Provenance`, `ImmunizationRecommendation` (where in scope), `RelatedPerson`, `ServiceRequest`, `Specimen`
- **Claims (CARIN BB):** `ExplanationOfBenefit` (five profile flavors - see [`carin-bb-ig.md`](carin-bb-ig.md))

See [`us-core-ig.md`](us-core-ig.md) for the full per-profile catalog.

### 2.2 SMART-on-FHIR EHR app

Typical SMART app uses **US Core** clinical resources plus context. Minimum set:

- Context: `Patient`, `Encounter`, `Practitioner` (from launch context)
- Clinical: `Condition`, `Observation`, `MedicationRequest`, `AllergyIntolerance`, `Immunization`, `Procedure`
- Documents: `DocumentReference`
- Auth orchestration: not a FHIR resource - see [`smart-on-fhir.md`](smart-on-fhir.md)

### 2.3 Bulk Data export (population analytics, research)

Group / Patient / System scope `$export` typically pulls **all USCDI resources** for the cohort. See [`bulk-data-export.md`](bulk-data-export.md). Adds:

- `Group` (defines the cohort)
- `OperationOutcome` (per-file partial-failure semantics)

### 2.4 Da Vinci PDex member-access (payer-to-payer / payer-to-app)

Layers on top of US Core + CARIN BB:

- `Patient`, `Coverage`, `Organization`, `Practitioner`, `PractitionerRole`
- `ExplanationOfBenefit` (CARIN BB profiles)
- USCDI clinical resources (US Core profiles)
- `Consent` (member consent for payer-to-payer exchange)
- `Provenance`

### 2.5 Provider directory (Plan-Net / Provider Directory API)

- `Practitioner`, `PractitionerRole`, `Organization`, `Location`, `HealthcareService`, `Endpoint`, `InsurancePlan`, `OrganizationAffiliation`

## 3. R4 vs R4B vs R5 deltas (payer / US-interop relevant only)

The CMS-mandated US payer-interop surface is **R4-anchored** as of CMS-9115-F and CMS-0057-F. R4B and R5 exist but should not be mixed into an R4 server. Surface the deltas only when migration is in play.

### 3.1 R4 → R4B

R4B is a minor errata-driven release of R4 that **lets implementers adopt updated versions of select resources** without moving to R5. Resources updated in R4B include:

- `Citation`
- `Evidence`, `EvidenceReport`, `EvidenceVariable`
- `SubscriptionStatus` (companion to R4 `Subscription`)
- `SubscriptionTopic` (backported pattern; full pattern is R5-native)
- `Topic` (renamed / refactored)
- `NutritionProduct`

For US payer interop, R4B is rarely material - the impacted resources are EBM / research-flavored. **Do not mix R4 and R4B resources in the same server unless you have a clear migration story.**

Source: <https://hl7.org/fhir/R4B/diff.html>.

### 3.2 R4 → R5 (payer / interop deltas only)

- **`Subscription` → `SubscriptionTopic` + `Subscription`**: R5 splits the topic (what to watch) from the subscription (who's watching). R4 servers can adopt the **Subscriptions R5 Backport IG** to use R5-style topics on R4. See [`operations.md`](operations.md).
- **`MedicationRequest`**: several cardinality + element changes; renamed elements. Migration requires careful profile update.
- **`InsurancePlan`**: significant additions in R5.
- **`Patient`, `Practitioner`**: minor element additions; backwards-compatible for most uses.
- **`Encounter`**: changes to participant / location structure (more nested).
- **Money type**: still uses ISO 4217 currency code; semantics unchanged.
- **`Observation`**: minor changes; `triggeredBy` added in R5.
- **`Bundle`**: `Bundle.issues` added in R5.
- New R5 resources irrelevant for US payer interop today: `Ingredient`, `ManufacturedItemDefinition`, `PackagedProductDefinition`, etc.

For US payer interop today, **stay on R4** unless the IG explicitly targets R4B or R5.

Source: <https://hl7.org/fhir/R5/diff.html>.

## 4. Resource-selection decision tree

```
1. Is this a person?
   - patient → Patient
   - clinician → Practitioner (+ PractitionerRole for role at org)
   - non-clinician staff or family → RelatedPerson or Person
   - generic role-only directory entry → PractitionerRole

2. Is this a clinical event or finding?
   - dx → Condition
   - measurement (vital sign, lab value, SDOH) → Observation
   - completed procedure → Procedure
   - allergy → AllergyIntolerance
   - immunization → Immunization
   - planned care → CarePlan / Goal / CareTeam

3. Is this a medication?
   - order / request → MedicationRequest
   - reported active med (no order) → MedicationStatement
   - dispense event → MedicationDispense
   - administration event (e.g., inpatient MAR) → MedicationAdministration
   - the product itself → Medication

4. Is this financial?
   - eligibility request → CoverageEligibilityRequest / Response
   - claim (submitted by provider) → Claim
   - adjudicated EOB (to member) → ExplanationOfBenefit (CARIN BB)
   - insurance coverage → Coverage

5. Is this a document or composition?
   - reference to an external document (PDF, narrative) → DocumentReference
   - structured composition of clinical content → Composition (often inside a document Bundle)

6. Is this provenance / audit?
   - who/when/why created/updated → Provenance
   - system audit log entry → AuditEvent
   - consent / authorization → Consent

7. Is this conformance?
   - profile / extension definition → StructureDefinition
   - value set / code system / mapping → ValueSet / CodeSystem / ConceptMap
   - server capability advertisement → CapabilityStatement
   - operation definition → OperationDefinition
   - search-param definition → SearchParameter
```

## 5. Resources commonly confused

| Pair | Use |
|---|---|
| `MedicationRequest` vs `MedicationStatement` | `MedicationRequest` = an order. `MedicationStatement` = a reported active medication regardless of source (member self-report, reconciliation). They are not interchangeable. |
| `Practitioner` vs `PractitionerRole` | `Practitioner` = the person (NPI, name, credentials). `PractitionerRole` = the person *in a role at an organization* (specialty, location, services). Most US Core / Plan-Net work needs both. |
| `Patient` vs `RelatedPerson` vs `Person` | `Patient` = the patient. `RelatedPerson` = a person related to the patient (parent, spouse, caregiver) in the context of *this* patient. `Person` = a generic person record that can link to `Patient` / `Practitioner` / `RelatedPerson` (rare in US payer interop). |
| `DocumentReference` vs `Composition` | `DocumentReference` = pointer / metadata for an external document (typical for C-CDA pointers in US Core). `Composition` = a structured FHIR-native document composition (rare in pure-claims work; common in C-CDA-equivalent FHIR documents). |
| `Encounter` vs `EpisodeOfCare` | `Encounter` = a single visit / contact. `EpisodeOfCare` = a longitudinal grouping of encounters under one care arrangement (e.g., a pregnancy, a cancer treatment course). |
| `Condition` vs `Observation` | `Condition` = a diagnosis / problem. `Observation` = a measurement or finding. SDOH screening answers are `Observation` (US Core SDOH profile), not `Condition`. |
| `Procedure` vs `ServiceRequest` | `Procedure` = a completed procedure. `ServiceRequest` = an order / request for a service. |
| `Coverage` vs `InsurancePlan` | `Coverage` = a specific person's coverage instance. `InsurancePlan` = the plan offering (used in Plan-Net / payer directory). |
| `Claim` vs `ExplanationOfBenefit` | `Claim` = the submitted claim (provider → payer). `ExplanationOfBenefit` = the adjudicated, member-facing EOB. CARIN BB profiles target `ExplanationOfBenefit`. |
| `Group` (Bulk Data) vs `Group` (cohort) | Same resource; in Bulk Data, `Group` identifies the cohort for `$export`. |
| `Bundle` (transaction) vs `Bundle` (searchset) vs `Bundle` (document) vs `Bundle` (message) | Same resource, different `Bundle.type`. Server processing differs significantly. See [`bundles-and-transactions.md`](bundles-and-transactions.md). |

## 6. Resources to NOT model when something simpler exists

- Do not model a SDOH screening result as `Condition`. Use `Observation` with the US Core SDOH profile.
- Do not model a "current medication list" as repeated `MedicationRequest`. Use `MedicationStatement` or curate the source `MedicationRequest` resources with statuses.
- Do not invent a custom `Basic` resource when a standard resource exists. `Basic` is a last resort.
- Do not model a payer-internal claim line as a custom resource. Use `Claim.item` + line-level fields, or `ExplanationOfBenefit.item` for the adjudicated view.
- Do not use `Composition` for a simple external PDF; `DocumentReference` with the binary attachment URL is sufficient.

## 7. Common worked example

> **[synthetic]** A payer is building the CMS-0057-F Patient Access API. The member-facing surface needs demographic + coverage + clinical (USCDI) + claims (CARIN BB) data. The resource set is:
>
> - `Patient` (US Core)
> - `Coverage` (US Core)
> - `Organization`, `Practitioner`, `PractitionerRole`, `Location` (US Core)
> - `AllergyIntolerance`, `CarePlan`, `CareTeam`, `Condition`, `DiagnosticReport`, `DocumentReference`, `Encounter`, `Goal`, `Immunization`, `MedicationRequest`, `Observation` (Lab, Vitals, Smoking Status, SDOH), `Procedure` (US Core)
> - `ExplanationOfBenefit` × 5 profile flavors (CARIN BB)
> - `Provenance` on every write
>
> FHIR version: R4 (4.0.1). US Core 6.1.0. CARIN BB 2.1.0. SMART App Launch 2.2.0. Bulk Data 2.0.0.

## 8. Related references

- Profile mechanics → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- US Core specifics → [`us-core-ig.md`](us-core-ig.md)
- CARIN BB specifics → [`carin-bb-ig.md`](carin-bb-ig.md)
- Da Vinci IG map → [`da-vinci-overview.md`](da-vinci-overview.md)
- Operations (Subscription, SubscriptionTopic) → [`operations.md`](operations.md)

## 9. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Mixing R4 / R4B / R5 in one server
- Using `Basic` instead of a fit-for-purpose resource
- Modeling a SDOH `Observation` as a `Condition`
- Confusing `MedicationRequest` vs `MedicationStatement`
