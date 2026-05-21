# FHIR conformance audit

> Use this template to audit a vendor's FHIR export (or your own pre-release artifact) for IG conformance. One row per resource type / profile. Replace `{{...}}`.
>
> All example payloads, identifiers, and URLs are `[synthetic]` placeholders.

---

## Identity

- **Audit name**: {{e.g., "Vendor X US Core 6.1.0 export - pre-prod conformance audit"}}
- **Audited artifact**: {{vendor name + export ID, or staging endpoint base URL}}
- **Audit date**: {{YYYY-MM-DD}}
- **Auditor**: {{name / team}}
- **IG target(s) with version pins**: {{e.g., US Core 6.1.0, CARIN BB 2.1.0, SMART App Launch 2.2.0, Bulk Data 2.0.0}}
- **FHIR base version**: {{R4 4.0.1 | R4B | R5}}
- **Audit status**: {{in-progress | passed | failed | conditional pass}}

## Scope

- **In scope**: {{resource types / endpoints / operations covered}}
- **Out of scope**: {{e.g., R5 SubscriptionTopic deferred to next audit cycle}}

## Resources audited

| Resource type | Profile (version-pinned) | Sample count audited | Must-support coverage % | Validator pass rate | Gap count | Status |
|---|---|---|---|---|---|---|
| Patient | `us-core-patient\|6.1.0` | {{n}} | {{%}} | {{%}} | {{n}} | {{pass \| fail \| conditional}} |
| Condition (encounter dx) | `us-core-condition-encounter-diagnosis\|6.1.0` | | | | | |
| Observation (lab) | `us-core-observation-lab\|6.1.0` | | | | | |
| MedicationRequest | `us-core-medicationrequest\|6.1.0` | | | | | |
| {{additional rows}} | | | | | | |

## Per-resource must-support evidence

> For each resource above, list every must-support element with a "found in N of M samples" count and a "data source confirmed" flag.

### {{Resource type}}

| MS element | Found in N/M samples | Source data confirmed populated | Gap? | Severity | Remediation |
|---|---|---|---|---|---|
| {{element.path}} | {{x/y}} | {{yes \| no \| partial}} | {{yes \| no}} | {{critical \| high \| medium \| low \| info}} | {{action}} |
| {{element.path}} | | | | | |

### {{Next resource type}}

...

## Extensions audited

| Extension | Canonical URL (version-pinned) | Found in N/M expected samples | Gap? | Severity |
|---|---|---|---|---|
| US Core Race | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race` | {{x/y}} | | |
| US Core Ethnicity | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity` | | | |
| US Core Birth Sex | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex` | | | |
| {{additional}} | | | | |

## Search parameters audited

| Resource | Required search params per IG | All declared in CapabilityStatement? | All working against live endpoint? | Required combinations exercised? | Gap? |
|---|---|---|---|---|---|
| Patient | `_id, identifier, name, family, given, birthdate, gender, _lastUpdated` + combos | | | | |
| {{additional}} | | | | | |

## Operations audited

| Operation | Required by IG? | Declared in CapabilityStatement? | Working? | Gap? |
|---|---|---|---|---|
| `$validate` | yes | | | |
| `$everything` (Patient) | optional | | | |
| `$export` (Bulk Data) | per use case | | | |
| {{additional}} | | | | |

## Validator output

- **HAPI Validator CLI run**: {{command + log link + summary count of fatal/error/warning}}
- **Server `$validate` results**: {{summary across sample set}}
- **Inferno results**:
  - US Core kit: {{passed N / total M, failed test IDs}}
  - SMART App Launch kit: {{passed N / total M, failed test IDs}}
  - Bulk Data kit: {{passed N / total M, failed test IDs}}
  - CARIN BB kit: {{passed N / total M, failed test IDs}}
  - Da Vinci kits (per IG): {{}}

## Gaps summary

| # | Gap | Resource / Profile | Severity | Owner | Target fix date | Status |
|---|---|---|---|---|---|---|
| 1 | {{describe}} | {{ref}} | {{critical \| high \| medium \| low}} | {{}} | {{}} | {{open \| in-progress \| fixed \| accepted-risk}} |
| 2 | | | | | | |

## Recommendations

{{Narrative summary: what blocks release? what's accepted risk? what's deferred to next cycle? what cross-skill referrals are needed (HIPAA technical-safeguards audit-log program, clinical / coding judgment from medical-chart-review or NLP siblings, code-system selection from healthcare-code-systems)?}}

## Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Auditor | {{}} | {{pass \| conditional \| fail}} | {{}} |
| FHIR architect | {{}} | | {{}} |
| Vendor / implementation lead | {{}} | | {{}} |
| Release gate / compliance | {{}} | | {{}} |
