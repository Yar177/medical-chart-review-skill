# HCPCS Level II

> **Why this file exists:** HCPCS Level II covers everything CPT does not: drugs administered other than oral (the J-codes that drive infusion / chemotherapy analytics), DME, supplies, transportation, vision / hearing items, and many quality-reporting codes. It is CMS-maintained, free, and updates **quarterly** - faster than CPT.

## 1. What it is

- **HCPCS** = **Healthcare Common Procedure Coding System** (often pronounced "hick-picks").
- **Level I** = CPT (AMA-maintained) - see [`cpt-and-modifiers.md`](cpt-and-modifiers.md).
- **Level II** = CMS-maintained alphanumeric codes for items and services not in CPT.
- Used on professional and facility claims alongside CPT.
- **Public domain** - no license required for redistribution.
- Updated **quarterly** (January, April, July, October), with annual major release.

## 2. Structure

HCPCS Level II codes are **1 alpha + 4 numeric = 5 characters** (`A0021` through `V5364`).

| Section | Range | Use |
|---|---|---|
| `A` | `A0000`-`A9999` | Transportation, medical & surgical supplies, miscellaneous |
| `B` | `B4000`-`B9999` | Enteral and parenteral therapy |
| `C` | `C1000`-`C9999` | Outpatient PPS (hospital outpatient department temporary codes) |
| `D` | `D0000`-`D9999` | Dental procedures (CDT codes - actually maintained by ADA, integrated into HCPCS) |
| `E` | `E0100`-`E9999` | Durable medical equipment (DME) |
| `G` | `G0000`-`G9999` | Temporary procedures / professional services (CMS-defined) - many are quality measures |
| `H` | `H0001`-`H9999` | Behavioral health and substance abuse |
| `J` | `J0000`-`J9999` | **Drugs administered other than oral method** (injectable / infused drugs) |
| `K` | `K0000`-`K9999` | DME MAC temporary codes |
| `L` | `L0100`-`L9999` | Orthotics and prosthetics |
| `M` | `M0000`-`M9999` | Medical services (limited use) |
| `P` | `P0000`-`P9999` | Pathology and laboratory |
| `Q` | `Q0000`-`Q9999` | Temporary codes (CMS-defined, often drugs / biologicals pending J-code assignment) |
| `R` | `R0000`-`R9999` | Diagnostic radiology services (limited) |
| `S` | `S0000`-`S9999` | Temporary national codes (Blue Cross Blue Shield Association) - **not used by Medicare** |
| `T` | `T1000`-`T9999` | Temporary national codes for state Medicaid agencies - **not used by Medicare** |
| `V` | `V2020`-`V5364` | Vision and hearing services |

### Letters most data scientists encounter

- **`J`** - infusion / injectable drugs. The bridge from pharmacy data world (NDC) to medical-benefit drugs. A `J3490` "unclassified drug" line will require the NDC on the same claim line to identify the actual drug. See [`rxnorm-ndc-and-drugs.md`](rxnorm-ndc-and-drugs.md).
- **`G`** - CMS-defined services, many of which are quality measures (GxxxF codes) or care management (CCM, TCM, PCM).
- **`E`** - DME (wheelchairs, oxygen, CPAP, etc.).
- **`Q`** - drugs awaiting permanent J-code assignment; high turnover quarterly.
- **`A`** - supplies and ambulance.

## 3. J-codes - the drug bridge

J-codes are how injectable / infused drugs appear on the medical benefit claim (vs the pharmacy benefit, which uses NDC). The same drug can appear on either side:

| Claim type | Code system | Example for "Pembrolizumab 200 mg" |
|---|---|---|
| Medical claim | HCPCS J-code + units | `J9271` Injection, pembrolizumab, 1 mg, quantity 200 |
| Pharmacy claim | NDC + days supply | NDC `00006-3026-02` (illustrative) |

Implications:

- A single drug administration can be reported on either side; counting total utilization requires harmonizing both.
- **Units on J-code lines matter.** `J9271` is per 1 mg; reporting 200 mg requires `quantity = 200`. Pipelines that ignore units undercount drug usage massively.
- **`J3490` "Unclassified drugs"** and **`J3590` "Unclassified biologics"** are placeholders for drugs lacking a specific J-code. The actual drug identity must come from the **NDC field on the same claim line** plus the description text. Joining only on J-code misses these entirely.

## 4. G-codes - quality and care management

G-codes are CMS-defined codes for services Medicare wants tracked. High-volume examples:

- **`G0008`-`G0010`** - influenza, pneumococcal, hepatitis B vaccine administration
- **`G0402`-`G0444`** - preventive services (initial preventive physical exam, depression screening, etc.)
- **`G0438`/`G0439`** - **Annual Wellness Visit (AWV)** - first and subsequent. Critical for HCC capture (provides the face-to-face encounter for risk-adjustment).
- **`G2010`-`G2012`** - virtual check-ins
- **`G0500`-`G0511`** - chronic care management (CCM), transitional care management (TCM)
- **`G8978`-`G9999`** - quality measurement codes (large block, used in MIPS and historical PQRS)

## 5. Q-codes - temporary placeholders

- New drugs and biologicals frequently appear first as `Q` codes (e.g., `Q5101`-`Q5xxx` for biosimilars).
- They may later migrate to permanent `J` codes.
- Longitudinal analysis must track Q→J migrations to avoid double-counting or missing utilization across the migration boundary.

## 6. Quarterly update cycle

| Quarter | Effective date |
|---|---|
| Q1 | January 1 |
| Q2 | April 1 |
| Q3 | July 1 |
| Q4 | October 1 |

- The **annual major HCPCS Level II release** is January 1.
- Quarterly addenda add new codes (frequently drugs / biologicals), retire codes, or change descriptions.
- Coverage indicators (CMS Pricing, Coverage, BETOS) are sometimes updated separately.

### Implication

HCPCS quarterly cadence is **faster than CPT (annual)** and **faster than ICD-10 (annual)**. A monthly drift-monitoring job for HCPCS is appropriate; quarterly at minimum. See [`versioning-and-drift.md`](versioning-and-drift.md).

## 7. Modifiers (shared with CPT)

HCPCS Level II uses the same modifier system as CPT (`-25`, `-59`, `-26`, `-TC`, anatomic, etc.) and adds **HCPCS-specific modifiers**:

| Modifier | Meaning |
|---|---|
| `-KX` | Requirements specified in the medical policy have been met (DME, therapy caps) |
| `-GA`/`-GX`/`-GY`/`-GZ` | ABN / non-covered service notices |
| `-LT`/`-RT` | Left side / right side (anatomic) |
| `-NU`/`-RR`/`-UE` | New equipment / rental / used equipment (DME) |
| `-Q5`/`-Q6` | Substitute physician / locum tenens |
| `-AS`/`-80`/`-81`/`-82` | Assistant at surgery variants |
| `-FA`-`-F9`, `-TA`-`-T9` | Finger / toe anatomic specificity |

See [`cpt-and-modifiers.md`](cpt-and-modifiers.md) §5 for the analytics implications - they apply identically to HCPCS Level II codes.

## 8. Coverage indicators and pricing files

CMS publishes alongside the HCPCS code file:

- **Coverage indicator** - is the code Medicare-payable, contractor-priced, bundled, not separately payable, etc.
- **Pricing indicator** - how is the payment determined (fee schedule, percent of charges, ASP, etc.).
- **BETOS** classification - see [`code-groupers.md`](code-groupers.md).
- **Coverage code, payment policy indicator, ASC-payable indicator**.

For analytics that mix payable and non-payable codes (e.g., utilization counting), filter on coverage indicator deliberately.

## 9. Authoritative source

- **CMS HCPCS Level II**: <https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system>
- **Quarterly update files**: posted before each quarter's effective date.
- **HCPCS Level II Coding Manual**: free PDF reference.
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 10. Common pitfalls

- **J-code units ignored.** Reporting `quantity = 1` for a 200-mg dose of a per-1-mg J-code understates drug usage 200×.
- **NDC ignored when J-code is unclassified** (`J3490`, `J3590`). The actual drug identity is in the NDC field on the same claim line.
- **Q→J migration ignored.** A drug billed as a Q-code in 2024 and a J-code in 2025 is the same drug; longitudinal counting must crosswalk.
- **S-codes confused with national HCPCS.** S-codes are BCBSA-defined and **not recognized by Medicare**. Mixed-payer pipelines must handle.
- **T-codes confused with national HCPCS.** T-codes are state-Medicaid-defined; varies by state.
- **G-code retirement.** Quality measures churn G-codes frequently; a G-code that meant something in MY2022 may have been deleted by MY2024.
- **Treating HCPCS as alphabetic-prefix-only.** The letter is part of the code, but joining on letter alone (e.g., "all J-codes are drugs") is a useful coarse grouping, not a precise one (some G-codes are also drug-related, e.g., influenza vaccine administration).
