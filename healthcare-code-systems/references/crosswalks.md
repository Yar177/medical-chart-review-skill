# Crosswalks

> **Why this file exists:** Every healthcare data team needs to map between code systems sooner or later. **No clinically meaningful crosswalk is purely 1:1.** This file catalogs the major crosswalks, their **cardinality**, their **fallback strategies**, and the **failure modes** they introduce when used naively.

## 1. The cardinality rules

When discussing **any** crosswalk, always state:

| Property | Question | Why it matters |
|---|---|---|
| **Cardinality** | 1:1, 1:N, N:1, or N:M? | Determines whether mapping inflates or deflates row counts |
| **Fallback strategy** | What happens to unmapped source codes? | Drop / passthrough / "unknown" bucket / route-to-human |
| **Direction-symmetry** | Does forward-then-backward round-trip? | Often no - GEMs and most clinical maps are asymmetric |
| **Time-validity** | What release / version of source and target? | Code sets drift; the same code can map differently in different vintages |
| **Authority / source** | Who publishes it? | Determines update cadence, licensing, and trust level |
| **Use-restriction** | Billing vs analytics vs informational? | GEMs are translation aids, not billing-authoritative |

A spec for a custom crosswalk should address all six. See [`../templates/crosswalk-spec.md`](../templates/crosswalk-spec.md).

## 2. GEMs - ICD-9-CM ↔ ICD-10-CM and ICD-9-PCS ↔ ICD-10-PCS

- **Source**: CMS / NCHS, last updated **FY2018**.
- **Direction**: separate forward and backward map files.
- **Cardinality**: predominantly **N:M**. Many source codes have multiple target candidates; many target codes are reachable from multiple sources.
- **Round-trip**: rarely lossless. Forward-then-backward often returns a different code.
- **Use-restriction**: **translation aid**, not billing-authoritative. CMS explicitly states GEMs are not intended for picking "the" correct billing code for a specific encounter.
- **Staleness**: codes added to ICD-10-CM after FY2018 have no GEM row.
- See [`icd9-and-legacy.md`](icd9-and-legacy.md) for detail.

### GEM row flags (see icd9-and-legacy §5)

`Approximate` / `No Map` / `Combination` / `Scenario` / `Choice List` flags govern interpretation. A single ICD-9 may produce several ICD-10 candidate rows with different combination + scenario + choice-list flags - choosing which row applies for a specific encounter requires the clinical context that GEMs do not encode.

### Strategies

- **For rollup / cohort analysis at the chronic-condition level**: forward GEM → take the union of mapped ICD-10 candidates → roll up to a grouper (CCSR, Elixhauser, Charlson). The grouper absorbs the cardinality mess.
- **For payment / billing reconciliation**: do not use GEMs; use authoritative coder review of each encounter.
- **For modeling on pre-2015 data**: prefer keeping ICD-9 native and either (a) restrict the training window to post-2015 or (b) use grouper-based features that work in both eras.

## 3. NDC ↔ RxNorm

- **Source**: NLM RxNorm monthly release.
- **Direction**: NDC → RxCUI (most common); RxCUI → NDC available as the inverse.
- **Cardinality**:
  - **NDC → RxCUI**: typically **1:1** at a point in time (usually mapping to an SCD-level RxCUI or GPCK for packs).
  - **RxCUI → NDC**: **1:N** (one SCD corresponds to many NDCs across labelers and packages).
- **Round-trip**: NDC → RxCUI → NDC will expand to many NDCs at the SCD level. Joins for "same drug as this NDC" need awareness of this.
- **Use-restriction**: clinical / analytic use is fine. Billing reconciliation between medical-benefit J-codes and pharmacy-benefit NDCs requires care.
- **Staleness**: NDCs added in the past month may not be in last month's RxNorm release. New drugs from new labelers can take weeks to propagate.
- See [`rxnorm-ndc-and-drugs.md`](rxnorm-ndc-and-drugs.md).

### Strategies

- For **ingredient-level cohorts** ("anyone on metformin"), map NDC → SCD RxCUI → IN RxCUI → re-expand to all SCDs and back to all NDCs with that ingredient. Joining on the resulting NDC list catches all formulations.
- For **specific-product analysis** ("Lantus pens"), stay at SBD level.
- For **package-level inventory** work, NDC is the only useful identifier; RxNorm is not granular enough.
- For **inactive NDCs in historical claims**, RxNorm retains historical mappings - use the historical NDC table.

## 4. SNOMED CT ↔ ICD-10-CM

- **Source**: NLM SNOMED CT US Edition (biannual; March / September).
- **Direction**: SNOMED → ICD-10-CM (primary, "Map to ICD-10-CM"); ICD-10-CM → SNOMED via inverse lookup.
- **Cardinality**: **N:M**. SNOMED has ~360,000+ concepts; ICD-10-CM has ~70,000 codes. Many SNOMED concepts have no clinically meaningful ICD-10-CM match.
- **Use-restriction**: NLM positions the map as a **provider-side aid for deriving billing codes from EHR concepts**. Each map row carries **map advice** (age, sex, "MAP IS CONTEXT DEPENDENT", "ALWAYS \[code\]", "IF \[condition\] MAP TO \[code\] OTHERWISE \[code\]") that requires reasoning beyond a flat lookup.
- **Round-trip**: not symmetric. SNOMED→ICD→SNOMED often returns a different SNOMED concept (loses granularity going out, picks up alternative going back).
- **Staleness**: biannual.

### Strategies

- For **joining EHR problem lists to claims-based cohort definitions**, the map is acceptable but expect coverage gaps. Validate cohort sizes against expectation.
- For **deriving billing codes from EHR data**, the map is the intended use case but still requires clinical review of map-advice conditions.
- For **HEDIS / HCC measures defined on ICD-10-CM applied to EHR-SNOMED data**, the map is a necessary bridge but lossy; document the lossy expectation in the measure spec.

## 5. LOINC ↔ CPT (lab procedures)

- **Source**: Regenstrief / AMA jointly publish a LOINC ↔ CPT crosswalk.
- **Cardinality**: **N:M**. A single CPT can correspond to many LOINCs (different methodologies, different specimen types) and a single LOINC can be reached by multiple CPTs.
- **Use-restriction**: **informational**, not billing-authoritative.
- **Staleness**: published with LOINC biannual releases.

### Strategies

- For **lab utilization counting** (lab results from EHR plus lab claims from billing), use the crosswalk as a bridge but reconcile counts carefully - one billed CPT may produce multiple LOINC-coded results (a panel).
- For **HEDIS lab numerators** that are defined in both CPT (billing) and LOINC (result data) variants, prefer the per-data-source authoritative coding (CPT for claims, LOINC for EHR / lab interface).

## 6. ICD-10-CM → HCC

- **Source**: CMS publishes annually as part of the CMS-HCC Software ZIP for each payment year (V24, V28 during phase-in years).
- **Cardinality**: **N:1** at the active-code level. Many ICD-10-CM codes map to one HCC. Some ICD-10-CM codes are **HCC-eligible in one model version and not in another** (V24 ≠ V28 coverage).
- **Round-trip**: undefined; HCC → ICD-10-CM is a 1:N expansion (many ICD-10-CM contribute to one HCC).
- **Use-restriction**: **risk-adjustment payment-authoritative for the named payment year and model version**. Cross-year or cross-model use is not authoritative.
- **Staleness**: re-released annually with the payment-year notice. Mid-year ICD-10-CM additions can have transitional handling.
- **HHS-HCC**: separate annual file from CMS CCIIO for ACA marketplace; not interchangeable with CMS-HCC.

### Strategies

- For **production HCC NLP**, pin the crosswalk snapshot date in every model card and emission. See `hcc-nlp` skill.
- For **multi-payer analytics** (Medicare Advantage + ACA marketplace), maintain **both** crosswalks and pick by payer.
- For **V24 → V28 transition years**, store both HCC numbers in parallel; treat the active HCC for the payment-year model as authoritative for that year.

## 7. HCC ↔ HHS-HCC

- **Same conceptual structure** (ICD-10-CM → HCC), **different content**.
- HHS-HCC has separate models for **adult**, **child**, and **infant** age bands.
- HHS-HCC is sometimes mistakenly assumed to be a subset or relabeling of CMS-HCC; it is neither - the two are independently maintained for different programs.

## 8. RxNorm ↔ HCPCS J-codes

- **Source**: CMS publishes a partial HCPCS-to-NDC crosswalk for specific J-codes (e.g., separately payable drugs).
- **Cardinality**: **1:N** (one J-code can correspond to many NDCs of the same active ingredient).
- **Coverage**: incomplete; many J-codes are not covered (especially `J3490` / `J3590` unclassified).
- **Use-restriction**: ASP pricing reconciliation, drug utilization analysis.

### Strategies

- For **medical-benefit drug utilization**, J-code → ingredient via the partial crosswalk; for unclassified J-codes, use the NDC on the same claim line if present.
- For **total drug spend** (medical + pharmacy), see [`rxnorm-ndc-and-drugs.md`](rxnorm-ndc-and-drugs.md) §6.

## 9. CPT → ICD-10-PCS (no formal crosswalk)

- There is **no official crosswalk** between CPT (professional / outpatient) and ICD-10-PCS (inpatient facility).
- They describe overlapping procedures from different perspectives and the same procedure on an inpatient stay may carry both.
- Joining them requires manual or commercial mapping work and is **inherently lossy** because the granularity dimensions differ (PCS encodes approach + device + body part; CPT encodes the bundled service).
- For inpatient analytics that need both sides reconciled, route through a procedure-grouper (e.g., CCSR Procedures) rather than direct CPT↔PCS mapping.

## 10. Custom crosswalks (the team will need them)

Most production pipelines build **custom crosswalks** at some point:

- **ICD-10-CM → internal disease categories** (custom chronic-condition flags above and beyond CCSR)
- **CPT / HCPCS → internal service-line categories** (custom utilization buckets)
- **Provider taxonomy → internal specialty groupings**
- **Payer / plan code → internal payer normalization**
- **Lab result codes (LOINC + vendor codes) → internal lab concept** (the EHR vendor abstraction layer)

For each, the spec needs:

- **Source code system and version**
- **Target taxonomy and version**
- **Cardinality** (1:1, 1:N, etc.)
- **Fallback for unmapped source codes** (drop / "unknown" / route to human review)
- **Update cadence** (who reviews, when)
- **QA process** (how is correctness validated)
- **Provenance** (who built it, who signed off, change history)

The [`../templates/crosswalk-spec.md`](../templates/crosswalk-spec.md) template captures this.

## 11. Common pitfalls

- **Treating GEMs as 1:1**. The single most common crosswalk error in healthcare data work.
- **Using a stale crosswalk** for a current date of service.
- **No fallback for unmapped codes**, leading to silent row drops at the join.
- **Round-tripping** without acknowledging asymmetry (NDC → RxNorm → NDC expands to a set, not the original).
- **Multi-source claim joining** without per-source crosswalk handling (medical-benefit J-codes and pharmacy-benefit NDCs counted as if they were the same coordinate system).
- **Custom crosswalks without provenance** - no record of who built it, against which code-set version, with what validation.
- **Crosswalks embedded inline in code** with no externalized spec or version. The crosswalk drifts silently as the codebase changes.
- **Using an ICD-10 → HCC crosswalk for the wrong payment year or model version** (V24 vs V28).
- **Embedding CPT or AMA-derived crosswalks** in open repositories without an AMA Data File license.
