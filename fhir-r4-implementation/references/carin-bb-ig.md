# CARIN Blue Button IG

> **Why this file exists:** CARIN Blue Button (CARIN BB) is the FHIR IG that defines the claims-side of US payer interop - specifically, the `ExplanationOfBenefit` (EOB) profiles that the CMS-mandated Patient Access API exposes to members. CARIN BB sits alongside US Core: US Core covers clinical data, CARIN BB covers adjudicated claims. The IG defines five EOB profile flavors, each modeling a different claim type with different element shapes and required adjudication fields. Getting the wrong profile means the EOB validates against the wrong schema and Inferno rejects.

Spec: <https://hl7.org/fhir/us/carin-bb/>.

## 1. Version map and regulatory anchor

| CARIN BB version | Regulatory anchor |
|---|---|
| CARIN BB 1.x | CMS-9115-F (2021) Patient Access API original anchor. |
| CARIN BB 2.0.0 | HTI / CMS-0057-F transitional baseline. |
| CARIN BB 2.1.0 | Current baseline for new implementations targeting CMS-0057-F (Jan 2027). |

Pin the version in `meta.profile` (e.g., `http://hl7.org/fhir/us/carin-bb/StructureDefinition/C4BB-ExplanationOfBenefit-Inpatient-Institutional|2.1.0`).

## 2. The five EOB profile flavors

CARIN BB defines five `ExplanationOfBenefit` profiles, each modeling a different claim category. The right profile depends on the claim type from the source data.

| EOB Profile | Source claim type | Examples |
|---|---|---|
| **C4BB-ExplanationOfBenefit-Inpatient-Institutional** | Inpatient hospital claims (institutional, type-of-bill 11x) | Acute inpatient admission, hospital DRG. |
| **C4BB-ExplanationOfBenefit-Outpatient-Institutional** | Outpatient institutional claims (TOB 13x, 71x, 73x, 76x, 77x, 12x, 14x, etc.) | Hospital outpatient, FQHC, rural health center, ambulatory surgery center (institutional billing). |
| **C4BB-ExplanationOfBenefit-Professional-NonClinician** | Professional / supplier claims (CMS-1500 / 837P) for non-clinician providers | DME suppliers, lab providers, ambulance services. |
| **C4BB-ExplanationOfBenefit-Pharmacy** | Pharmacy claims (NCPDP, 837P pharmacy) | Retail pharmacy, mail-order Rx. |
| **C4BB-ExplanationOfBenefit-Oral** | Dental claims (ADA J430D / 837D) | Dental services. |

Also (since 2.x): vision and other specialty profiles may exist depending on version. Check the IG version's full profile list.

Each profile constrains `ExplanationOfBenefit` differently - required slices on `adjudication`, required `extension`s for type-of-bill / claim-type, required `careTeam.role` codes, required `supportingInfo` codes.

## 3. Profile selection decision tree

```
What's the source claim format?
- UB-04 / 837I institutional → look at type-of-bill
   - Inpatient TOB (11x) → Inpatient-Institutional
   - Outpatient TOB → Outpatient-Institutional
- CMS-1500 / 837P professional → Professional-NonClinician
- NCPDP / pharmacy 837P → Pharmacy
- ADA J430D / 837D dental → Oral
- Vision-specific carrier format → check IG for Vision profile (where present)
```

When in doubt, look at the source `claim type` code on the inbound claim and map per the IG's mapping page.

## 4. Common EOB elements (all profiles)

| Element | Notes |
|---|---|
| `identifier` | Claim identifier(s); often slice for `claim-unique-id` and `claim-group-id`. |
| `status` | `active`, `cancelled`, `draft`, `entered-in-error`. |
| `type` | `CodeableConcept` from `claim-type` value set: `institutional`, `professional`, `oral`, `pharmacy`, `vision`. |
| `subType` | More granular (e.g., `inpatient`, `outpatient`). |
| `use` | `claim`, `preauthorization`, `predetermination`. |
| `patient` | Reference to US Core Patient. |
| `created` | Date the EOB was generated. |
| `insurer` | Reference to the payer Organization. |
| `provider` | Reference to billing provider. |
| `payee` | Where the payment goes (provider vs subscriber). |
| `claim` | Reference to upstream `Claim` (often omitted in member-facing). |
| `outcome` | `complete`, `error`, `partial`, `queued`. |
| `careTeam` | Practitioner / Organization references with role codes. |
| `supportingInfo` | Slices for claim-received-date, paid-date, billing-net-amount, MCO-paid-date, etc. (varies per profile). |
| `diagnosis` | Diagnoses with role + sequence (admitting, principal, secondary, etc.). ICD-10-CM coded. |
| `procedure` | Procedures with sequence. ICD-10-PCS or CPT/HCPCS. |
| `insurance` | Coverage reference + focal flag. |
| `item` | Line-level detail (revenue code, CPT/HCPCS, modifier, service date, quantity, unit price, charge, adjudication). |
| `total` | Aggregated totals (submitted, allowed, paid, patient responsibility, deductible, copay, coinsurance). |
| `payment` | Payment amount, date, type. |
| `adjudication` (line and total) | Adjudication categories: `submitted`, `allowed`, `deductible`, `copay`, `coinsurance`, `paidtopatient`, `paidtoprovider`, `noncovered`, `priorpayerpaid`, etc. |

## 5. Adjudication categories

CARIN BB defines a controlled vocabulary for `adjudication.category.coding`. Required categories vary by profile but include:

- `submitted` - billed amount
- `allowed` - allowed amount after contractual adjustment
- `eligible` - eligible for benefit calculation
- `deductible` - member deductible applied
- `copay` - copay
- `coinsurance` - coinsurance
- `noncovered` - non-covered amount
- `paidtoprovider` - net amount paid to provider
- `paidtopatient` - net amount paid to patient
- `priorpayerpaid` - amount paid by prior payer (COB)
- `denied` - denied amount
- `discount` - provider discount

Each profile mandates a minimum set of categories at line-level and / or total-level. Inferno verifies their presence.

## 6. Type-of-bill, revenue codes, and other CARIN-specific extensions

CARIN BB defines extensions to carry institutional-claim metadata not present in base `ExplanationOfBenefit`:

| Extension | Use |
|---|---|
| `C4BB-AdjudicationDiscriminator` | Adjudication-category discriminator. |
| `claim-bill-facility-type-code` | UB-04 type-of-bill facility-type digit. |
| `claim-bill-classification-code` | UB-04 type-of-bill classification digit. |
| `claim-bill-frequency-code` | UB-04 type-of-bill frequency digit. |
| `point-of-origin-for-admission-or-visit-code` | Source-of-admission. |
| `claim-care-team-role` | Care-team role within the claim context. |

Pin extension URLs at the IG version.

## 7. Required search parameters

CARIN BB mandates search support on `ExplanationOfBenefit` for:

- `patient` (always; the per-member access surface)
- `_lastUpdated` (for incremental sync)
- `type`
- `service-date` or `billable-period` (varies per profile)
- `identifier`

Declare in `CapabilityStatement.rest.resource.searchParam`. Inferno checks each.

## 8. Bundle pagination for member-facing EOB

Member-facing EOB endpoints can return thousands of EOBs per member. Use `_count` (typically 50-200) and follow `Bundle.link.next`. Members' apps must handle pagination - many fail this Inferno test.

## 9. Worked example - mapping an inpatient claim to EOB Inpatient-Institutional

> **[synthetic]** Internal inpatient claim with: claim-id `CLM-001`, member-id `M-001`, hospital-org `ORG-001`, admit date `2026-04-10`, discharge date `2026-04-15`, type-of-bill `111`, principal diagnosis `J18.9` (ICD-10-CM Pneumonia), DRG `193`, billed `$45,000`, allowed `$28,500`, member responsibility `$1,750` (deductible).

EOB shape (truncated, key elements only):

```json
{
  "resourceType": "ExplanationOfBenefit",
  "id": "eob-inpt-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/carin-bb/StructureDefinition/C4BB-ExplanationOfBenefit-Inpatient-Institutional|2.1.0"]
  },
  "identifier": [
    {
      "type": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "uc" }] },
      "system": "http://payer.example.org/eob",
      "value": "CLM-001"
    }
  ],
  "status": "active",
  "type": {
    "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "institutional" }]
  },
  "subType": { "coding": [{ "system": "http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBInstitutionalClaimSubType", "code": "inpatient" }] },
  "use": "claim",
  "patient": { "reference": "Patient/m-001" },
  "billablePeriod": { "start": "2026-04-10", "end": "2026-04-15" },
  "created": "2026-05-15T...",
  "insurer": { "reference": "Organization/payer-001" },
  "provider": { "reference": "Organization/org-001" },
  "outcome": "complete",
  "diagnosis": [
    {
      "sequence": 1,
      "diagnosisCodeableConcept": { "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "J18.9" }] },
      "type": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/ex-diagnosistype", "code": "principal" }] }]
    }
  ],
  "procedure": [],
  "insurance": [{ "focal": true, "coverage": { "reference": "Coverage/m-001-coverage" } }],
  "item": [
    {
      "sequence": 1,
      "productOrService": { "coding": [{ "system": "https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/MS-DRG-Classifications-and-Software", "code": "193" }] },
      "servicedPeriod": { "start": "2026-04-10", "end": "2026-04-15" },
      "adjudication": [
        { "category": { "coding": [{ "system": "...", "code": "submitted" }] }, "amount": { "value": 45000, "currency": "USD" } },
        { "category": { "coding": [{ "system": "...", "code": "allowed" }] }, "amount": { "value": 28500, "currency": "USD" } }
      ]
    }
  ],
  "total": [
    { "category": { "coding": [{ "system": "...", "code": "submitted" }] }, "amount": { "value": 45000, "currency": "USD" } },
    { "category": { "coding": [{ "system": "...", "code": "allowed" }] }, "amount": { "value": 28500, "currency": "USD" } },
    { "category": { "coding": [{ "system": "...", "code": "deductible" }] }, "amount": { "value": 1750, "currency": "USD" } },
    { "category": { "coding": [{ "system": "...", "code": "paidtoprovider" }] }, "amount": { "value": 26750, "currency": "USD" } }
  ],
  "payment": { "amount": { "value": 26750, "currency": "USD" }, "date": "2026-05-15" }
}
```

The mapping is best captured per-field; see [`templates/claims-to-eob-mapping.md`](../templates/claims-to-eob-mapping.md) for the structured spec.

## 10. CARIN BB vs Da Vinci PDex

Both touch member-access claims data, but the use case differs:

- **CARIN BB** - direct member-app access (member's app reads EOB from the member's payer).
- **Da Vinci PDex** - payer-to-payer transfer (one payer gives a member's data to another payer per CMS-0057-F Payer-to-Payer API). PDex *uses* CARIN BB EOB profiles for the claims portion. See [`da-vinci-overview.md`](da-vinci-overview.md).

## 11. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Profile mismatch - using Inpatient profile for an outpatient claim
- Missing required adjudication categories (Inferno fails)
- ICD-10-CM diagnoses without `principal` / `admit` / `secondary` role coding
- Pharmacy claims modeled as Professional (wrong profile)
- Missing `_lastUpdated` search support (breaks incremental sync)
- Confusing `Claim` (upstream) vs `ExplanationOfBenefit` (member-facing)
- Missing type-of-bill extensions on Institutional profiles
- Mixing CARIN BB versions across resources in a single export

## 12. Related references

- US Core Patient / Coverage / Practitioner / Organization (referenced from EOB) → [`us-core-ig.md`](us-core-ig.md)
- Profile mechanics, slicing, extensions → [`profiles-and-conformance.md`](profiles-and-conformance.md)
- Da Vinci PDex overview → [`da-vinci-overview.md`](da-vinci-overview.md)
- Claims → EOB mapping template → [`templates/claims-to-eob-mapping.md`](../templates/claims-to-eob-mapping.md)
- Conformance testing → [`conformance-testing.md`](conformance-testing.md)
- CARIN BB IG → <https://hl7.org/fhir/us/carin-bb/>
