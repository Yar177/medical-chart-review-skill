# Provider identifiers

> **Why this file exists:** Provider data is harder than it looks. **NPI** is the universal identifier, but its **NPPES** record contains taxonomy, addresses, and ownership data that drift constantly. **TIN** is the tax identifier separate from NPI. Provider attribution and network analytics depend on getting all of this right.

## 1. NPI - National Provider Identifier

- **NPI** = **National Provider Identifier**, a HIPAA-mandated unique identifier for healthcare providers in the US.
- Issued by **CMS / NPPES** (National Plan and Provider Enumeration System).
- **10-digit numeric** identifier. The 10th digit is a **Luhn check digit** computed over the first 9 digits prefixed with `80840` (the issuer identifier).
- Two types:
  - **Type 1**: **Individual** providers (physicians, NPs, PAs, RNs, therapists, etc.)
  - **Type 2**: **Organizations** (hospitals, group practices, labs, pharmacies, DME suppliers)
- **Required** on virtually all HIPAA claims and electronic transactions.
- **Public**: the NPPES file is freely downloadable.

### Luhn check on NPI

```
1. Prefix the 9-digit NPI base with 80840 → 14-digit string
2. From right to left, double every other digit; subtract 9 if the result > 9
3. Sum all digits
4. The 10th NPI digit is the value that makes the total a multiple of 10
```

Validation is cheap and catches transcription errors at ingest. Several public utilities implement the check; ETL pipelines should validate NPIs at the boundary rather than discovering bad IDs downstream.

## 2. NPPES - the registry behind NPI

- The **NPPES Downloadable File** is released **monthly** by CMS.
- ~8 million records (active + deactivated).
- For each NPI:
  - Type 1 or Type 2 designation
  - Provider name (legal, other names)
  - **Mailing address** and **practice location address(es)** - can differ
  - **Taxonomy codes** (one primary + zero or more secondary)
  - License numbers (state, board, by taxonomy)
  - Deactivation status and reason
  - Entity-type details (Type 2 only: sole proprietor flag, EIN if applicable)
  - Authorized official name, contact info (Type 2)
  - Last update date

### Volatility

- Providers move practices, change names, gain or lose taxonomies, deactivate, reactivate.
- **The NPPES record represents the provider's self-reported status at the last update**; it is not real-time.
- For network analytics, snapshot NPPES monthly and track changes (new NPIs, deactivations, taxonomy changes, address changes).

## 3. Taxonomy codes - NUCC

- **Taxonomy codes** classify the **provider's specialty / type**.
- Maintained by the **National Uniform Claim Committee (NUCC)**.
- **10-character alphanumeric** (e.g., `207R00000X` Internal Medicine, `207RC0000X` Cardiovascular Disease, `261QM0850X` Adolescent and Young Adult Behavioral Health Clinic).
- **Hierarchical** with three levels:
  - **Provider Grouping** (e.g., "Allopathic & Osteopathic Physicians")
  - **Classification** (e.g., "Internal Medicine")
  - **Specialization** (e.g., "Cardiovascular Disease")
- A provider can claim **multiple taxonomies**; one is designated **primary** in NPPES.
- Updated by NUCC semi-annually (typically April and October).

### Common analytic uses

- **PCP vs specialist classification** for attribution and HEDIS denominator routing.
- **Hospital identification** by Type 2 taxonomy (`282N00000X` General Acute Care Hospital, `283X00000X` Rehabilitation Hospital, etc.).
- **Behavioral health network** carve-out identification.
- **Pharmacy / DME** entity identification.

### Caveats

- **Self-reported by the provider** at NPPES enrollment / update.
- **A cardiologist may have only "Internal Medicine" listed** if they never updated their NPPES taxonomy after subspecialty training.
- **A primary taxonomy** is the *administrative* primary, not necessarily the *clinical* primary practice today.
- For high-accuracy specialty classification, supplement NPPES taxonomy with **claims-based specialty detection** (volume / types of procedures performed).

## 4. TIN - Tax Identification Number

- **TIN** = **Tax Identification Number** issued by IRS for tax reporting.
- For individual providers: typically a **SSN** (sensitive PII) or an **EIN** if the provider has incorporated.
- For organizations: an **EIN** (Employer Identification Number, 9-digit).
- TIN appears on claims (837 Loop 2010AA / 2010BB) and identifies the **billing entity** for payment routing.
- **NPI ≠ TIN**: an individual physician has one NPI but may bill under a group's TIN; a hospital has one Type 2 NPI but may have multiple TINs across affiliated entities.

### Why the distinction matters

- **Payment routes to TIN**, not NPI.
- **Network contracting** is often at the TIN level (the group practice signs the contract; individual NPIs are listed as participating providers under the group).
- **Provider directory listings** are at the NPI level but referenced by TIN for the billing relationship.

## 5. CCN - CMS Certification Number

- **CCN** = **CMS Certification Number** (formerly Medicare Provider Number).
- 6-character identifier assigned by CMS to **facilities** (hospitals, SNFs, HHAs, ESRD facilities, etc.) for Medicare participation.
- Used on **inpatient and SNF claims** in addition to NPI.
- Encodes information in the digits: first 2 digits = state, subsequent digits indicate facility type (e.g., short-term acute hospitals fall in specific numeric ranges).
- Used by **Hospital Compare**, **Care Compare**, and other CMS quality reporting.

## 6. State medical license numbers

- Each US state / territory issues medical licenses with its own numbering system.
- **No national standard** for format.
- Stored in NPPES at the per-state per-taxonomy level.
- Lookup of license status (active / inactive / disciplined) requires querying the state medical board, not NPPES.

## 7. DEA number

- **DEA registration number** issued by the US Drug Enforcement Administration for prescribing controlled substances.
- **9-character alphanumeric**: 2 letters + 7 digits (e.g., `AB1234563`).
- First letter encodes registrant type (`A`, `B` practitioner; `M` mid-level practitioner; `F` hospital, etc.).
- Second letter is the first letter of the registrant's last name (for individuals).
- **Last digit is a check digit** computed over the other digits.
- Used on **controlled-substance prescriptions** and on some claims (especially Schedule II analytics).
- Separate from NPI; an NPI can have multiple DEA numbers (one per practice location for controlled-substance dispensing).

## 8. Provider directory and "ghost networks"

- Health plans publish **provider directories** listing in-network providers.
- Directories are notoriously inaccurate: ~20-50% of listed providers may be unreachable, no longer practicing, or no longer in-network (the "ghost network" problem).
- **No Surprises Act (2022)** and **CMS** rules require directory accuracy and provider verification at intervals.
- Analytic uses of provider directories (network adequacy, attribution) must account for the staleness.

## 9. Provider attribution

While "attribution" is an analytic / business-logic question rather than a code-system one, the **identifiers** above are what attribution logic operates on:

- **NPI** for the provider's identity
- **TIN** for the billing entity
- **Taxonomy** for primary-care vs specialist routing
- **CCN** for the facility
- **Encounter type / E&M codes** for the visit kind
- **Date range / look-back window** for the attribution period

Common rules: "plurality of E&M visits to a PCP-taxonomy NPI in the last 24 months". Variations: most-recent, weighted by encounter intensity, by paid amount, by HEDIS denominator membership.

The `medical-chart-review` and `hedis-nlp` skills have additional context on attribution from a clinical / measure perspective.

## 10. Authoritative sources

- **NPPES NPI Registry**: <https://npiregistry.cms.hhs.gov/> (single-NPI lookup) and <https://download.cms.gov/nppes/NPI_Files.html> (monthly bulk download)
- **NUCC Taxonomy**: <https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40>
- **CCN / Hospital files**: <https://data.cms.gov/provider-data/>
- **DEA**: <https://www.deadiversion.usdoj.gov/> (validation, not bulk file)
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 11. Common pitfalls

- **NPI stored as integer**, losing leading zeros (NPIs do not have leading zeros today but format hygiene matters).
- **Luhn validation skipped**, allowing typos through.
- **Type 1 and Type 2 NPIs mixed** without distinction in analyses.
- **Primary taxonomy assumed to be current clinical specialty.** May be years stale; supplement with claims-based detection.
- **Deactivated NPIs treated as active** in current-state analyses.
- **TIN treated as NPI** in payment-routing or contract-counting analyses.
- **CCN treated as NPI** in facility analyses (CCN is the Medicare ID; NPI is the HIPAA ID; both appear on inpatient claims and identify the same facility differently).
- **NPPES taxonomy used as gold standard** for specialty when claims-based specialty (procedure mix, E&M patterns) would be more accurate.
- **Provider directory join** assumed accurate without verification - many directories carry significant ghost-network noise.
- **DEA used as provider identifier** when it should only identify controlled-substance prescribing authority.
- **Storing PII (SSN as TIN)** without HIPAA-appropriate safeguards. See `hipaa-compliance`.
