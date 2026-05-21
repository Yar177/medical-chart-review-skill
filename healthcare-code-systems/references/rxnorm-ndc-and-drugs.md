# RxNorm, NDC, and drug code systems

> **Why this file exists:** Drug data is split across **NDC** (the FDA package-level code on every pharmacy claim and drug label), **RxNorm** (the NLM normalized name and the bridge between systems), **HCPCS J-codes** (medical-benefit injectables / infusions - see [`hcpcs-level-ii.md`](hcpcs-level-ii.md)), and several commercial knowledge bases (First Databank, Medi-Span, Multum). The NDC 10-vs-11-digit problem and the NDC↔RxNorm cardinality are the recurring failure modes.

## 1. NDC - National Drug Code

- **NDC** = **National Drug Code** - the **FDA-assigned** unique identifier for a packaged drug product in the US.
- Appears on:
  - Every retail pharmacy claim (NCPDP D.0)
  - Drug label / packaging
  - Medical claim lines for facility-administered drugs (paired with HCPCS J-code)
  - 340B / inventory / supply-chain data
- **Public**, free, downloadable from FDA.
- Updated **continuously** (FDA NDC Directory refreshes daily / weekly).

### NDC structure

The NDC is a **3-segment code**: **labeler - product - package**.

```
Segment 1 (labeler)  - FDA-assigned to the manufacturer / distributor
Segment 2 (product)  - labeler-assigned to the specific drug formulation
Segment 3 (package)  - labeler-assigned to the specific package size / type
```

### The 10-vs-11-digit problem

The FDA NDC is **10 digits** in one of three configurations:

| Format | Segments | Example | Used by |
|---|---|---|---|
| **4-4-2** | labeler-product-package | `1234-5678-90` | FDA |
| **5-3-2** | labeler-product-package | `12345-678-90` | FDA |
| **5-4-1** | labeler-product-package | `12345-6789-0` | FDA |

**HIPAA standard claims (NCPDP D.0)** require an **11-digit** NDC in **5-4-2** format. Conversion zero-pads the segment that is short:

| FDA format | HIPAA 11-digit form | Zero-pad inserted |
|---|---|---|
| `4-4-2` → `5-4-2` | Pad **labeler** with leading zero | `01234-5678-90` |
| `5-3-2` → `5-4-2` | Pad **product** with leading zero | `12345-0678-90` |
| `5-4-1` → `5-4-2` | Pad **package** with leading zero | `12345-6789-00` |

### Why this matters

- **The 11-digit form is ambiguous if you do not know the original FDA format.** Storing `01234567890` without preserving format makes it impossible to reverse to the original FDA NDC.
- **Joining 10-digit FDA NDC to 11-digit claims NDC fails** unless one side is normalized.
- Many warehouses **store the 11-digit form without hyphens** (`01234567890`); some store with hyphens (`01234-5678-90`); some store as integer (loses leading zero - **broken**); some store both.
- Some sources strip the package segment, leaving a **9-digit product code** that identifies the drug but not the package. Useful for clinical analytics; insufficient for inventory or 340B work.

**Rule:** Store NDC as **fixed-width 11-digit string**, document the convention, and convert at the boundary. Preserving the original FDA format requires a separate field.

## 2. RxNorm

- **RxNorm** = **NLM's normalized naming system for medications**.
- Free, downloadable from NLM. Updated **monthly** (typically the first Monday).
- Provides a **stable normalized concept identifier (RxCUI)** for clinical drug names at multiple levels of abstraction.
- Used by FHIR (`Medication.code`), EHR e-prescribing (Surescripts), clinical decision support, and as the bridge between NDC and proprietary drug databases.

### RxNorm term types (TTY) - the abstraction levels

A given drug exists in RxNorm at multiple "term types":

| TTY | Meaning | Example |
|---|---|---|
| **IN** | Ingredient | "Metformin" |
| **PIN** | Precise ingredient (specific form / salt) | "Metformin hydrochloride" |
| **MIN** | Multiple ingredients | "Lisinopril / Hydrochlorothiazide" |
| **DF** | Dose form | "Oral Tablet" |
| **SCDC** | Semantic clinical drug component | "Metformin 500 MG" |
| **SCDF** | Semantic clinical dose form | "Metformin Oral Tablet" |
| **SCD** | **Semantic clinical drug (generic, with strength + dose form)** | "Metformin 500 MG Oral Tablet" - **the most commonly used level for clinical analytics** |
| **SBDC** | Semantic branded drug component | "Glucophage 500 MG" |
| **SBDF** | Semantic branded dose form | "Glucophage Oral Tablet" |
| **SBD** | **Semantic branded drug** | "Glucophage 500 MG Oral Tablet" |
| **BN** | Brand name | "Glucophage" |
| **GPCK** / **BPCK** | Generic / Branded pack | Combination packs (e.g., birth control sample packs) |

### RxCUI

- Each TTY-level concept has an **RxCUI** (RxNorm Concept Unique Identifier) - a stable integer.
- RxCUIs are **stable across releases for active concepts**; deprecated RxCUIs are retained for historical reference.
- Relationships link RxCUIs across TTYs (e.g., an SCD RxCUI is linked to its IN RxCUI, SCDC RxCUI, SCDF RxCUI, etc.).

### Worked example

```
Metformin 500 MG Oral Tablet  (SCD)   RxCUI 860975
  ingredient                  (IN)    RxCUI 6809   "Metformin"
  dose form                   (DF)    RxCUI 317541 "Oral Tablet"
  brand                       (SBD)   RxCUI 261546 "Glucophage 500 MG Oral Tablet"
    brand name                (BN)    RxCUI 8772   "Glucophage"
```

For most clinical analytics, the **SCD** ("Metformin 500 MG Oral Tablet") is the right level - it captures ingredient + strength + dose form but is generic-neutral.

For **ingredient-level cohorts** ("anyone on metformin"), use the **IN** RxCUI and join via the related concepts.

## 3. NDC ↔ RxNorm

- RxNorm publishes the **NDC-to-RxCUI** crosswalk as part of its monthly release.
- The mapping is generally **NDC → one RxCUI** at a specific TTY (usually SCD or GPCK for packages).
- **Caveats**:
  - An NDC can be **inactivated** at FDA but still appear in historical claims. RxNorm marks inactive NDCs.
  - A drug can be **reformulated** by the same labeler with a new NDC; the old and new NDCs may map to different (but clinically equivalent) RxCUIs.
  - **Obsolete NDCs** that no longer exist in the NDC Directory may still appear in old claims - RxNorm retains the historical mapping.
  - **Repackager NDCs**: a labeler that repackages another labeler's drug gets its own labeler segment; the resulting NDC is different from the original even though the drug is the same.

### Mapping cardinality

- **NDC → RxCUI**: typically 1:1 at a given point in time.
- **RxCUI → NDC**: 1:N - one SCD-level RxCUI corresponds to many NDCs (multiple manufacturers, multiple package sizes).

## 4. ATC - Anatomical Therapeutic Chemical classification

- **ATC** = **WHO Collaborating Centre for Drug Statistics Methodology** classification.
- 5-level hierarchical classification by therapeutic / anatomic group, e.g.:
  - `A10BA02` = Metformin (A = alimentary tract, A10 = drugs used in diabetes, A10B = blood glucose lowering drugs excl. insulins, A10BA = biguanides, A10BA02 = metformin)
- Used heavily in **research, pharmacoepidemiology, international literature**; less common in US operational data.
- Free; downloadable from WHO Collaborating Centre (registration required).
- Useful for cross-national drug studies or when needing a **therapeutic class** rollup that RxNorm does not natively provide.

## 5. Commercial drug knowledge bases

- **First Databank (FDB)** - extensive drug knowledge: interactions, allergies, contraindications, dose checking, IV compatibility. Commercial license.
- **Medi-Span (Wolters Kluwer)** - similar scope; commercial license.
- **Multum (Cerner)** - similar scope; commercial.
- These products provide structured data (drug-drug interactions, allergy cross-reactivity, REMS programs) not present in RxNorm or NDC.
- Most EHRs license one of these for clinical decision support.
- For analytics teams, these are **rarely the primary identifier**; they are typically joined onto data already keyed by NDC or RxCUI.

## 6. The medical-benefit drug crossover (J-codes)

Drugs administered in clinical settings (infusions, injections, chemotherapy) appear on **medical claims** keyed by **HCPCS J-codes** rather than NDC. See [`hcpcs-level-ii.md`](hcpcs-level-ii.md) §3.

Bridging to RxNorm requires a **HCPCS-to-RxNorm crosswalk** (CMS publishes one for some J-codes; coverage is incomplete) or NDC on the same claim line (when present) and then NDC → RxNorm.

Counting total drug utilization (medical + pharmacy benefit) requires:

1. Pharmacy side: NDC → RxNorm (ingredient or SCD level).
2. Medical side: J-code → RxNorm (best-effort via available crosswalk; fall back to NDC on the claim line if present; otherwise treat as unknown ingredient).
3. Union by ingredient RxCUI, with units harmonized (pharmacy days-supply / quantity; medical J-code units × dose-per-unit).

## 7. Release / update cadences

| System | Cadence |
|---|---|
| **NDC Directory (FDA)** | Continuously updated; downloads refresh daily / weekly |
| **RxNorm (NLM)** | Monthly (first Monday) |
| **HCPCS J-codes (CMS)** | Quarterly (see [`hcpcs-level-ii.md`](hcpcs-level-ii.md)) |
| **ATC (WHO)** | Annually |

A drift-monitoring job for the **monthly RxNorm release** catches new drugs, new NDCs, and deprecations promptly. See [`versioning-and-drift.md`](versioning-and-drift.md).

## 8. Authoritative sources

- **FDA NDC Directory**: <https://www.accessdata.fda.gov/scripts/cder/ndc/>
- **RxNorm (NLM)**: <https://www.nlm.nih.gov/research/umls/rxnorm/index.html> - requires free UMLS account.
- **ATC (WHOCC)**: <https://www.whocc.no/atc_ddd_index/>
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 9. Common pitfalls

- **NDC stored as integer.** Drops leading zeros; irreversible. Always store as fixed-width string.
- **10-digit FDA NDC joined to 11-digit claims NDC** without normalization. Silent join miss.
- **11-digit form stored without preserving FDA format.** Reverse engineering is ambiguous.
- **Repackager NDCs** treated as different drugs from the original labeler's NDC. They are the same drug.
- **NDC inactivation ignored.** A historical NDC may not appear in the current FDA Directory but is valid for old dates of service.
- **Joining only on RxCUI without TTY discipline.** A query for "metformin" needs the IN RxCUI; a query for "metformin 500 mg tablets" needs the SCD RxCUI. Mixing levels produces inconsistent cohorts.
- **Branded RxCUI joined to claims that report only generic SCD.** Use IN or SCD level for cohort definitions; reserve SBD for brand-specific studies.
- **J-code-only drug counting.** Misses pharmacy-benefit drugs entirely. NDC-only counting misses medical-benefit drugs entirely. Total utilization requires both.
- **Outdated RxNorm.** A 6-month-old RxNorm release is missing dozens of new drugs and NDCs.
- **Days-supply not normalized.** Pharmacy claims report days-supply per fill; computing adherence (MPR / PDC) requires aggregating days-supply over time without double-counting overlaps.
