# Immunizations and other code systems

> **Why this file exists:** A grab-bag of smaller but important code systems: **CVX** (vaccine codes), **MVX** (vaccine manufacturers), **race / ethnicity** code sets (OMB / CDC / HL7), and a few **HL7 v2 user-defined code systems** you will encounter in eligibility, enrollment, and demographic files.

## 1. CVX - vaccine codes

- **CVX** = **CDC vaccine administered codes**.
- Maintained by **CDC** as part of the immunization data exchange standards.
- 2-3 digit numeric code identifying a specific vaccine product (combination, formulation, valence).
- Used in:
  - **HL7 v2 VXU** (vaccination update) and **QBP** (query) messages
  - **FHIR Immunization.vaccineCode**
  - **Immunization Information Systems (IIS)** state registries
  - HEDIS immunization measures (CIS, IMA, COL-IM)
- **Free**, public domain.
- Updated as new vaccines are licensed (event-driven, not on a fixed cadence).

### Examples

| CVX | Vaccine |
|---|---|
| `08` | Hepatitis B, adolescent or pediatric formulation |
| `10` | Polio - inactivated (IPV) |
| `20` | DTaP (Diphtheria, Tetanus, acellular Pertussis) |
| `49` | Hib (Haemophilus influenzae type b), PRP-OMP conjugate |
| `83` | Hepatitis A, pediatric / adolescent dosage |
| `133` | Pneumococcal conjugate PCV13 |
| `158` | Influenza, injectable, quadrivalent |
| `207` | COVID-19, mRNA, Moderna (LNP-S, PF, 100 mcg) - illustrative; COVID CVX codes proliferated 2020-2024 |
| `213` | SARS-COV-2 (COVID-19), unspecified |

CVX has separate codes for **different formulations of the same disease vaccine** (different manufacturers, valences, pediatric vs adult, etc.). Counting "doses of COVID vaccine" requires understanding which CVX codes are equivalent at the analytic level.

### CVX status

- **Active**: currently in use.
- **Inactive**: previously valid; may still appear in historical data.
- **Pending**: assigned but not yet released.
- **Non-US**: used internationally; should not appear in US registry data.

Filtering historical immunization data on "active only" silently drops legacy doses.

## 2. MVX - vaccine manufacturer codes

- **MVX** = **CDC manufacturer codes** for vaccines.
- 2-4 character alphanumeric code (e.g., `MSD` = Merck, `PFR` = Pfizer, `SKB` = GlaxoSmithKline).
- Paired with CVX on HL7 v2 RXA segments to fully identify a vaccine product (lot-level identification requires lot number, expiration date, NDC).

The **CVX + MVX** pair maps to a specific **trade-name vaccine** that can also be joined to NDC. CDC publishes the CVX-MVX-NDC crosswalk.

## 3. Race and ethnicity code sets

Multiple competing standards coexist; understanding which one a dataset uses matters for stratification.

### OMB 1997 standard

- **Race** (5 categories, multiple allowed): American Indian or Alaska Native; Asian; Black or African American; Native Hawaiian or Other Pacific Islander; White.
- **Ethnicity** (separate from race, 2 categories): Hispanic or Latino; Not Hispanic or Latino.

### OMB 2024 revision

- In **March 2024** OMB published revised standards (SPD 15):
  - **Single combined race / ethnicity question** (no longer separate).
  - **New "Middle Eastern or North African" (MENA) category**.
  - **Detailed sub-categories** required for federal data collection.
- Federal agencies have **5 years** to comply; legacy datasets will continue to use the 1997 standard for years.

### HL7 / CDC code system (PH_RaceAndEthnicity_CDC)

- Detailed hierarchical code set maintained by CDC PHIN (Public Health Information Network).
- ~900 race codes and ~40 ethnicity codes at the leaf level, rolled up into the 5 / 2 OMB top-level categories.
- Code format: numeric (e.g., `2106-3` White, `2054-5` Black or African American, `2186-5` Not Hispanic or Latino).
- Used in **FHIR US Core Patient resource** race / ethnicity extensions.

### Common pitfalls

- **Conflating race and ethnicity** under the 1997 standard - they are separate dimensions; "Hispanic" is an ethnicity, with members of any race.
- **Single-race assumption** - the 1997 standard allows multiple race selections; pipelines that store race as a single column lose multi-racial detail.
- **MENA classification** - prior to 2024, Middle Eastern / North African individuals were generally classified as "White" under OMB 1997. Post-2024 standards add a distinct MENA category; longitudinal data spans the change.
- **"Unknown" / "Patient declined" / "Other"** treated as missing - these are valid administrative categories with their own analytic implications, especially for equity analysis.
- **Self-reported vs administrative source** not distinguished - race / ethnicity from registration vs claims vs EHR may disagree.

## 4. HL7 v2 user-defined / HL7-defined code tables

HL7 v2 messages carry many small coded fields, each using a **table** of allowed values. Two flavors:

- **HL7-defined tables** (table number 0001-0999) - canonical values defined by HL7. Examples:
  - **Table 0001 Sex**: `F` Female, `M` Male, `O` Other, `U` Unknown, `A` Ambiguous, `N` Not applicable.
  - **Table 0002 Marital Status**: `S` Single, `M` Married, `D` Divorced, `W` Widowed, `A` Separated, etc.
  - **Table 0005 Race** (legacy; superseded by CDC PHIN values in most modern interfaces).
  - **Table 0189 Ethnic Group** (legacy).
  - **Table 0202 Telecommunication Equipment Type**: `PH` Phone, `FX` Fax, `MD` Modem, `CP` Cellular Phone, etc.
  - **Table 0203 Identifier Type**: `MR` Medical Record Number, `SS` Social Security Number, `DL` Driver License, `NPI` National Provider Identifier, `DN` Doctor Number, etc.
- **User-defined tables** (table number 0300+) - sites define their own values; portability across sites requires explicit mapping.

When ingesting HL7 v2 data, the **HL7 table reference** for each coded field is the source of truth. Vendor extensions are common; never assume a HL7 v2 coded field uses only the canonical values.

## 5. Other code systems you may encounter

| Code system | Use |
|---|---|
| **SOP** (Source of Payment Typology) | Payer / coverage type classification (PHDSC-maintained) - useful when normalizing payer data across systems |
| **HIPPS** (Health Insurance Prospective Payment System) codes | Used in SNF, HHA, IRF, and hospice payment grouping - 5-character alphanumeric |
| **DSM-5 / ICD-10-CM mental health crosswalk** | Mental-health diagnoses are coded in ICD-10-CM for billing; DSM-5 codes used in clinical practice are largely aligned but with some nuances |
| **CDT** (Current Dental Terminology) | Dental procedure codes, maintained by ADA; integrated into HCPCS Level II as D-codes |
| **NUCC Provider Taxonomy** | See [`provider-identifiers.md`](provider-identifiers.md) |
| **42 CFR Part 2 substance-use codes** | Subset of ICD-10-CM with privacy implications; see HIPAA `hipaa-compliance` skill |
| **ICD-O-3** | Oncology - separate code system for cancer registries (topography + morphology); not used on claims |

## 6. Common pitfalls

- **CVX active-only filtering** drops legacy / historical immunizations.
- **CVX + MVX combination ignored** - same CVX from different MVX manufacturers identifies different products.
- **Race / ethnicity standard not pinned** - OMB 1997 vs 2024, with-MENA vs without-MENA, single-select vs multi-select, all coexist.
- **HL7 v2 user-defined tables assumed to be standard** - a `Marital Status` value of `C` may mean "Common-law" at one site and not exist at another.
- **CDT (D-codes)** misclassified as medical HCPCS Level II - they are dental, follow ADA licensing, and route to dental adjudication.
- **HIPPS codes** treated as random alphanumerics instead of decoded into the underlying RUG / CMG / HHRG case-mix categories.

## 7. Authoritative sources

- **CVX / MVX**: <https://www2a.cdc.gov/vaccines/iis/iisstandards/vaccines.asp>
- **CDC PHIN Race / Ethnicity Code System**: <https://www.cdc.gov/phin/resources/vocabulary/index.html>
- **OMB 2024 SPD 15 revision**: <https://www.whitehouse.gov/wp-content/uploads/2024/03/SPD-15-Federal-Register-Notice.pdf>
- **HL7 v2 Tables**: <https://www.hl7.org/special/committees/vocab/> and the HL7 v2 implementation guides.
- **CDT (ADA)**: <https://www.ada.org/cdt> - licensed.
- See [`sources-and-licensing.md`](sources-and-licensing.md).
