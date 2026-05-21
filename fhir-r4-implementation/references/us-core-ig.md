# US Core IG

> **Why this file exists:** US Core is the foundational US-realm FHIR IG - the profile set that defines what "USCDI on FHIR" looks like, and the surface every CMS-9115-F / CMS-0057-F Patient Access API and every ONC-certified EHR exposes. The versioning story is messy: US Core 3.x → 8.x correspond to USCDI v1 → v4+ over the last several years, and CMS / ONC pin specific versions for specific deadlines. This file covers the profile catalog at a depth useful for "what resources / must-supports do I need for this use case" and points at the IG itself for full element-by-element specs.

Spec: <https://hl7.org/fhir/us/core/>.

## 1. Version map (USCDI ↔ US Core ↔ regulatory anchor)

| US Core version | USCDI version | Regulatory anchor |
|---|---|---|
| US Core 3.1.1 | USCDI v1 | ONC Cures Final Rule (HTI-1 predecessor); CMS-9115-F Patient Access API original anchor. |
| US Core 5.0.1 | USCDI v2 | HTI-1 transitional. |
| US Core 6.1.0 | USCDI v3 | HTI-1 current anchor (as of 2026 baseline); CMS-0057-F default reference. |
| US Core 7.0.0 | USCDI v4 | HTI-2 (in flight). |
| US Core 8.0.0-ballot | USCDI v5 (in flight) | Future. |

**Always pin the exact version** in `meta.profile` (e.g., `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0`) - the profile content changes meaningfully across major versions.

## 2. Profile catalog (US Core 6.1.0 baseline)

Grouped by category. Each profile is at `http://hl7.org/fhir/us/core/StructureDefinition/us-core-<name>`.

### 2.1 Patient / demographics / coverage

- `us-core-patient`
- `us-core-relatedperson`
- `us-core-practitioner`
- `us-core-practitionerrole`
- `us-core-organization`
- `us-core-location`
- `us-core-coverage`

### 2.2 Clinical - diagnoses, allergies, immunizations

- `us-core-condition-encounter-diagnosis` (Encounter Diagnosis)
- `us-core-condition-problems-health-concerns` (Problem List Item, Health Concern)
- `us-core-allergyintolerance`
- `us-core-immunization`

### 2.3 Clinical - vitals (`Observation` profiles)

- `us-core-blood-pressure`
- `us-core-bmi`
- `us-core-body-height`
- `us-core-body-weight`
- `us-core-body-temperature`
- `us-core-head-circumference`
- `us-core-heart-rate`
- `us-core-respiratory-rate`
- `us-core-pulse-oximetry`
- `us-core-vital-signs` (parent)

### 2.4 Clinical - labs

- `us-core-observation-lab`
- `us-core-diagnosticreport-lab`

### 2.5 Clinical - social history / SDOH

- `us-core-smokingstatus`
- `us-core-observation-sdoh-assessment`
- `us-core-observation-social-history`
- `us-core-observation-survey`
- `us-core-observation-occupation`
- `us-core-observation-pregnancystatus`
- `us-core-observation-pregnancyintent`
- `us-core-observation-sexual-orientation`

### 2.6 Clinical - procedures, care planning

- `us-core-procedure`
- `us-core-careplan`
- `us-core-careteam`
- `us-core-goal`
- `us-core-servicerequest`

### 2.7 Medications

- `us-core-medicationrequest`
- `us-core-medication`
- `us-core-medicationdispense`

### 2.8 Diagnostic / clinical reports

- `us-core-diagnosticreport-note` (notes / clinical reports, not lab)
- `us-core-documentreference`

Clinical notes are represented via `us-core-documentreference` and `us-core-diagnosticreport-note` per the US Core Clinical Notes Guidance. There is no separate `us-core-clinical-note` profile; do not invent one.

### 2.9 Encounters

- `us-core-encounter`

### 2.10 Provenance and provider-related

- `us-core-provenance` (required on writes that the IG covers)

### 2.11 Specimen / imaging

- `us-core-specimen`
- `us-core-imagingstudy` (in newer versions)

### 2.12 Other

- `us-core-questionnaireresponse`
- `us-core-medicationstatement` (newer versions)

## 3. Must-support semantics in US Core

US Core uses `mustSupport` extensively. The IG defines what "support" means for each element class. Read [`profiles-and-conformance.md`](profiles-and-conformance.md) §3.2 for the general semantics, then read the US Core "Must Support" page for the IG-specific definitions: <https://hl7.org/fhir/us/core/general-guidance.html#must-support>.

Highlights:

- Must-support data elements: the server must be able to populate, store, and return the element when the source data has it.
- Must-support extensions (US Core Race, US Core Ethnicity, US Core Birth Sex, etc.): the server must handle them on read and write.
- Must-support coded values: the server must accept and store coded values from the bound value set.
- Missing data: when an element is must-support but no data is available, the server may either omit the element or include a Data Absent Reason extension.

## 4. Common US Core extensions

| Extension | URL | Used on |
|---|---|---|
| US Core Race | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race` | Patient |
| US Core Ethnicity | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity` | Patient |
| US Core Birth Sex | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex` | Patient |
| US Core Sex (newer) | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex` | Patient |
| US Core Genderidentity | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity` | Patient |
| US Core Tribal Affiliation | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-tribal-affiliation` | Patient |

Always pin the IG version when citing extension URLs in profile work.

## 5. US Core CapabilityStatements

US Core publishes CapabilityStatements for **Server** and **Client** roles, with profile lists, search params, and operations declared. Implementers should:

1. Start from the US Core CapabilityStatement for the relevant role.
2. Customize for site-specific extensions / additional profiles.
3. Publish at `[base]/metadata`.

See [`templates/capability-statement-skeleton.md`](../templates/capability-statement-skeleton.md) for the starter.

## 6. Search parameter expectations

US Core mandates specific search parameter support per resource. Examples (US Core 6.1.0 Patient):

- `_id`, `identifier`, `name`, `family`, `given`, `birthdate`, `gender`, `_lastUpdated`
- Combination searches: `(family + birthdate)`, `(name + birthdate)`, `(gender + name)`, etc.

The IG lists the required search params + combinations per resource - see the resource-specific US Core profile page (e.g., <https://hl7.org/fhir/us/core/StructureDefinition-us-core-patient.html#mandatory-search-parameters>).

Conformance: declare every required search param + combination in `CapabilityStatement.rest.resource.searchParam` and implement them correctly. Inferno tests verify each one.

## 7. US Core ↔ USCDI mapping

USCDI is a data class catalog (the "what"); US Core is the FHIR representation (the "how"). For example:

| USCDI v3 data class | US Core profile / element |
|---|---|
| Patient Demographics | `us-core-patient` + US Core Race, Ethnicity, Birth Sex extensions |
| Allergies and Intolerances | `us-core-allergyintolerance` |
| Health Concerns | `us-core-condition-problems-health-concerns` |
| Smoking Status | `us-core-smokingstatus` |
| SDOH Assessment | `us-core-observation-sdoh-assessment` |
| Care Team Members | `us-core-careteam` + `us-core-practitionerrole` |
| Laboratory | `us-core-observation-lab` + `us-core-diagnosticreport-lab` |
| Encounter Diagnoses | `us-core-condition-encounter-diagnosis` |
| Goals | `us-core-goal` |
| Procedures | `us-core-procedure` |
| Vital Signs | `us-core-blood-pressure`, `us-core-bmi`, ... |
| Medications | `us-core-medicationrequest` + `us-core-medication` |
| Immunizations | `us-core-immunization` |
| Provenance | `us-core-provenance` |

Full USCDI map per US Core version: <https://hl7.org/fhir/us/core/uscdi.html>.

## 8. Common worked example - minimum CMS-0057-F Patient Access surface

> **[synthetic]** A payer building the CMS-0057-F Patient Access API for January 2027.

| US Core profile | Required for | Notes |
|---|---|---|
| `us-core-patient\|6.1.0` | Member demographics | Race, Ethnicity, Birth Sex extensions must-support |
| `us-core-coverage\|6.1.0` | Insurance coverage | |
| `us-core-organization\|6.1.0` | Payer / provider org references | |
| `us-core-practitioner\|6.1.0` | Provider identity | |
| `us-core-practitionerrole\|6.1.0` | Provider role at org | |
| `us-core-location\|6.1.0` | Service location | |
| `us-core-allergyintolerance\|6.1.0` | USCDI: Allergies | |
| `us-core-condition-problems-health-concerns\|6.1.0`, `us-core-condition-encounter-diagnosis\|6.1.0` | USCDI: Problems, Health Concerns, Encounter Diagnoses | |
| `us-core-encounter\|6.1.0` | Visits | |
| `us-core-medicationrequest\|6.1.0` + `us-core-medication\|6.1.0` | USCDI: Medications | RxNorm coding |
| `us-core-immunization\|6.1.0` | USCDI: Immunizations | CVX coding |
| `us-core-observation-lab\|6.1.0`, vital-sign profiles, `us-core-smokingstatus\|6.1.0`, `us-core-observation-sdoh-assessment\|6.1.0`, `us-core-observation-social-history\|6.1.0` | USCDI: Lab, Vitals, Smoking, SDOH, Social History | LOINC coding |
| `us-core-procedure\|6.1.0` | USCDI: Procedures | CPT/ICD-10-PCS coding |
| `us-core-careplan\|6.1.0`, `us-core-careteam\|6.1.0`, `us-core-goal\|6.1.0` | USCDI: Care planning | |
| `us-core-documentreference\|6.1.0` + `us-core-diagnosticreport-note\|6.1.0` | USCDI: Notes / Documents | |
| `us-core-servicerequest\|6.1.0` | USCDI: Service Requests | |
| `us-core-specimen\|6.1.0` | USCDI: Specimens | |
| `us-core-provenance\|6.1.0` | USCDI: Provenance | Required on all writes |
| `us-core-relatedperson\|6.1.0` | Authorized representatives | |

Plus CARIN BB `ExplanationOfBenefit` profiles for claims data - see [`carin-bb-ig.md`](carin-bb-ig.md).

## 9. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Pinning US Core 3.1.1 in 2026+ work (the regulatory anchor has moved)
- Mixing must-support semantics across versions (changed meaningfully between 3.x and 6.x)
- Implementing `us-core-patient` but not its required extensions (Race, Ethnicity, Birth Sex)
- Omitting `us-core-provenance` on writes (USCDI requires it)
- Picking the wrong Condition profile (Encounter Diagnosis vs Problem / Health Concern is meaningful)
- Forgetting required search-param combinations (Inferno tests them explicitly)

## 10. Related references

- Profile mechanics → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- Terminology bindings → [`terminology-services.md`](terminology-services.md)
- CARIN BB (claims, sibling IG) → [`carin-bb-ig.md`](carin-bb-ig.md)
- Conformance testing (Inferno ONC g(10)) → [`conformance-testing.md`](conformance-testing.md)
- US Core IG → <https://hl7.org/fhir/us/core/>
