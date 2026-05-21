# Claims → ExplanationOfBenefit mapping

> Per-field mapping spec from an internal claims schema to a CARIN BB `ExplanationOfBenefit` profile. Replace `{{...}}`. One row per element. Use one spec per CARIN BB EOB profile (Inpatient-Institutional, Outpatient-Institutional, Professional-NonClinician, Pharmacy, Oral).
>
> All example payloads, identifiers, and URLs are `[synthetic]` placeholders.

---

## Identity

- **Spec name**: {{e.g., "Internal inpatient claim → C4BB-ExplanationOfBenefit-Inpatient-Institutional"}}
- **EOB profile (with version pin)**: {{`http://hl7.org/fhir/us/carin-bb/StructureDefinition/C4BB-ExplanationOfBenefit-Inpatient-Institutional|2.1.0`}}
- **Source schema**: {{internal table / file / data warehouse view}}
- **Source schema version**: {{snapshot date or semver}}
- **Owner**: {{team}}
- **Created**: {{YYYY-MM-DD}}
- **Last reviewed**: {{YYYY-MM-DD}}
- **Status**: {{draft | active | deprecated}}

## Scope

- **Claim type covered**: {{e.g., institutional inpatient, TOB 11x}}
- **Out-of-scope**: {{e.g., outpatient TOB 13x → routed to separate Outpatient-Institutional spec}}

## Top-level element mapping

> One row per element / sub-element. Include cardinality from the profile (`0..1`, `1..1`, `0..*`, `1..*`). Flag must-support (`MS`).

| EOB element (FHIRPath) | Cardinality | MS | Source field | Transform | Unmapped strategy |
|---|---|---|---|---|---|
| `identifier` | `1..*` | MS | {{claims.claim_id}} | Map to `identifier.value` with `identifier.system={{system URI}}` | Drop EOB if claim_id null (log) |
| `status` | `1..1` | MS | {{claims.status}} | `paid|denied|...` → `active`; `void` → `cancelled` | Default `active` |
| `type` | `1..1` | MS | {{claims.claim_type}} | Map to `institutional` for TOB 11x | - |
| `subType` | `0..1` | MS | {{claims.tob}} | TOB 11x → `inpatient` | - |
| `use` | `1..1` | MS | constant | `claim` | - |
| `patient` | `1..1` | MS | {{claims.member_id}} | `Reference(Patient/...)` resolved via member-id crosswalk | Drop EOB if no Patient (log) |
| `billablePeriod.start` | `0..1` | MS | {{claims.admit_date}} | ISO date | - |
| `billablePeriod.end` | `0..1` | MS | {{claims.discharge_date}} | ISO date | - |
| `created` | `1..1` | MS | {{claims.adjudication_date}} | ISO datetime | Default current timestamp at EOB build |
| `insurer` | `1..1` | MS | constant | `Reference(Organization/payer-id)` | - |
| `provider` | `1..1` | MS | {{claims.billing_npi}} | `Reference(Organization/...)` resolved via NPI crosswalk | Drop EOB if no Org (log) |
| `outcome` | `1..1` | MS | {{claims.adjudication_outcome}} | `paid` → `complete`; `denied` → `complete`; `pended` → `partial` | - |
| `diagnosis[]` | `0..*` | MS | {{claims.dx[]}} | Per-row map: `diagnosisCodeableConcept` with ICD-10-CM coding; `type` from `principal/admit/secondary` flag; `sequence` from ordinal | Skip rows with null code (log) |
| `procedure[]` | `0..*` | MS | {{claims.proc[]}} | Per-row map: ICD-10-PCS coding for inpatient; sequence ordinal | - |
| `insurance` | `1..*` | MS | {{claims.coverage_id}} | `Reference(Coverage/...)`; `focal=true` for primary | - |
| `item[]` | `0..*` | MS | {{claims.line[]}} | See `item` sub-spec below | - |
| `total[]` | `1..*` | MS | aggregated | See `total` sub-spec | - |
| `payment.amount` | `0..1` | MS | {{claims.paid_to_provider}} | Money | - |
| `payment.date` | `0..1` | MS | {{claims.payment_date}} | ISO date | - |

## `item[]` sub-spec (per line)

| EOB item element | Source field | Transform | Notes |
|---|---|---|---|
| `item.sequence` | line ordinal | int | |
| `item.productOrService` | {{line.rev_code or drg}} | CodeableConcept (DRG for inpatient; rev code optional) | |
| `item.servicedPeriod` | line dates | period | |
| `item.adjudication[]` | line amounts | per `adjudication.category` (submitted, allowed, deductible, copay, coinsurance, paidtoprovider, paidtopatient, noncovered) | Required categories per IG |

## `total[]` sub-spec

| Category | Source aggregate | Required by IG? |
|---|---|---|
| `submitted` | sum(line submitted) | yes |
| `allowed` | sum(line allowed) | yes |
| `deductible` | sum(line deductible) | yes |
| `copay` | sum(line copay) | yes |
| `coinsurance` | sum(line coinsurance) | yes |
| `noncovered` | sum(line noncovered) | yes |
| `paidtoprovider` | sum(line paid-to-provider) | yes |
| `paidtopatient` | sum(line paid-to-patient) | yes |
| `priorpayerpaid` | sum from COB segment | when COB present |

## Extensions used (CARIN BB)

| Extension | Source field | Applied at |
|---|---|---|
| `claim-bill-facility-type-code` | TOB digit 1 | EOB root |
| `claim-bill-classification-code` | TOB digit 2 | EOB root |
| `claim-bill-frequency-code` | TOB digit 3 | EOB root |
| `point-of-origin-for-admission-or-visit-code` | source-of-admission | EOB root |

## Unmapped source fields

| Source field | Decision | Rationale |
|---|---|---|
| {{source field}} | {{drop / log / route to extension / route to supportingInfo}} | {{}} |

## Validator output (most recent run)

- HAPI Validator CLI: {{pass / N errors / N warnings + log link}}
- Server `$validate`: {{pass / fail + log}}
- Inferno CARIN BB kit: {{pass / fail + run link}}

## Sign-off

| Role | Name | Date |
|---|---|---|
| Mapping author | {{}} | {{}} |
| FHIR reviewer | {{}} | {{}} |
| Claims SME reviewer | {{}} | {{}} |
| Conformance gate | {{}} | {{}} |
