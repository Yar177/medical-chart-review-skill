# ICD-9-CM (legacy) and ICD-11 (awareness)

> **Why this file exists:** US claims data with dates of service before October 1, 2015, are coded in ICD-9-CM. Any longitudinal analysis crossing the 2015 boundary has to deal with this. The GEMs crosswalk is real, useful, and not a 1:1 mapping. ICD-11 is internationally adopted but not used on US claims; treat it as awareness-only.

## 1. ICD-9-CM - what it is

- **ICD-9-CM** = International Classification of Diseases, 9th Revision, **Clinical Modification**.
- Used in the US from approximately 1979 through **September 30, 2015** for diagnosis coding (Volumes 1 and 2) and inpatient procedure coding (Volume 3).
- Replaced by **ICD-10-CM** (diagnoses) and **ICD-10-PCS** (inpatient procedures) on October 1, 2015.

## 2. Structure - diagnosis codes (Volumes 1 / 2)

ICD-9-CM diagnosis codes are **3 to 5 characters**, mostly numeric, with a decimal point after the third character.

```
250.42
│ │ ││
│ │ │└─ 5th digit (specificity)
│ │ └── 4th digit
│ └──── decimal
└────── 3-digit category
```

- Numeric categories `001`-`999` cover diseases and injuries.
- **V-codes** (`V01`-`V91`) - factors influencing health status, analogous to ICD-10-CM **Z-codes**.
- **E-codes** (`E000`-`E999`) - external causes of injury / poisoning, analogous to ICD-10-CM **V-W-X-Y** chapter.
- Sub-classifications added a 4th digit (after the decimal) and sometimes a 5th digit for further specificity.

### Worked examples

| ICD-9-CM | Meaning |
|---|---|
| `250.00` | Type 2 diabetes mellitus, without complications, not stated as uncontrolled |
| `250.42` | Type 2 diabetes mellitus, with renal manifestations, uncontrolled |
| `428.0` | Congestive heart failure, unspecified |
| `496` | Chronic airway obstruction, NEC |
| `V58.69` | Long-term (current) use of other medications |
| `E885.9` | Fall from other slipping, tripping, or stumbling |

## 3. Structure - procedure codes (Volume 3)

ICD-9-CM Volume 3 procedure codes are **3 to 4 characters**, numeric, with a decimal after the second character.

| Code | Meaning |
|---|---|
| `47.0` | Appendectomy |
| `47.01` | Laparoscopic appendectomy |
| `81.51` | Total hip replacement |

A single ICD-9-PCS code often maps to many ICD-10-PCS codes because ICD-10-PCS encodes attributes (approach, device, body-part granularity) that ICD-9-PCS did not.

## 4. ICD-9 in modern data

You will encounter ICD-9 in:

- **Historical claims** (DOS < 2015-10-01) in any longitudinal warehouse.
- **Long-running risk-adjustment cohorts** doing pre-/post-ICD-10 trend analysis.
- **Registry data**, **research extracts**, **CMS public datasets** (older release vintages).
- **Free-text notes** referencing the old codes; some older clinical decision support content still uses ICD-9 reference lists.

You will **not** encounter ICD-9 in:

- US healthcare **claims with DOS on or after 2015-10-01**.
- HCC models published for payment years 2016+ (those map ICD-10-CM directly).
- HEDIS measures for measurement years 2016+ (value sets are ICD-10-based).

## 5. GEMs - General Equivalence Mappings

**GEMs** are the official ICD-9-CM ↔ ICD-10 translation aids, published by CMS and NCHS in two directions:

- **Forward map**: ICD-9-CM → ICD-10-CM (or ICD-9-PCS → ICD-10-PCS)
- **Backward map**: ICD-10-CM → ICD-9-CM (or ICD-10-PCS → ICD-9-PCS)

### What GEMs are NOT

- **Not 1:1 exact mappings.** Many rows are 1:N, N:1, or N:M.
- **Not a billing crosswalk.** GEMs translate between code systems; they do not adjudicate which code is correct for a specific clinical scenario.
- **Not bidirectional-symmetric.** Round-tripping a code through forward + backward GEMs often returns a different code from where you started.
- **Not maintained after 2018.** CMS announced GEMs would no longer be updated after FY2018; subsequent ICD-10-CM additions have **no GEM row**. For dates of service well past 2018, applying GEMs to bridge to ICD-10 is increasingly stale.

### GEMs row flags

Each GEM row has flags indicating the nature of the mapping:

| Flag | Position | Meaning |
|---|---|---|
| **Approximate** | 1 | The match is approximate; the codes are similar but not exactly equivalent |
| **No Map** | 2 | No corresponding code in the target system |
| **Combination** | 3 | The source code maps to a combination of target codes (composite) |
| **Scenario** | 4 | When combination=1, identifies which scenario this row belongs to |
| **Choice List** | 5 | When combination=1, identifies which choice list within a scenario |

A clinically correct mapping often requires choosing **which** ICD-10 code from a multi-row GEM result is the right one for a given encounter, which the GEMs themselves do not encode.

See the GEMs section of [`crosswalks.md`](crosswalks.md) for a fuller treatment.

## 6. Common longitudinal-analysis strategies

When working with a dataset that spans 2015-10-01:

- **Strategy A: Keep both systems native.** Store each code in its original system with a `code_system_version` tag (`ICD-9-CM` or `ICD-10-CM-FYxxxx`). Run analyses that handle each natively. Avoid cross-system joining where possible.
- **Strategy B: Map up to ICD-10.** Apply forward GEMs to ICD-9 codes to derive ICD-10 candidates, then unify. Acceptable for **rollup analyses** (chronic-condition prevalence, broad cohort definitions) where the loss of granularity does not change the conclusion. **Risky** for any individual-level clinical decision or payment-impacting use.
- **Strategy C: Map both to a code grouper.** Apply CCSR (or its predecessor CCS), Elixhauser, Charlson, or another grouper that operates on either ICD-9 or ICD-10. The grouper absorbs the cross-system difference. See [`code-groupers.md`](code-groupers.md).
- **Strategy D: Treat pre-2015 data as a separate dataset.** For trend / cohort studies, segregate the eras and acknowledge the discontinuity.

The right choice depends on the analytic question. For most risk-adjustment and quality-measure pipelines, the pre-2015 era is not in scope and ICD-9 can be left alone.

## 7. ICD-11 - awareness only for US data work

- **ICD-11** was endorsed by the World Health Assembly in 2019 and came into effect 2022-01-01 internationally.
- The US has **not adopted ICD-11** for claims, HEDIS, HCC, or other operational data.
- ICD-11 has substantially different structure (chapter codes are alphanumeric in a different scheme; "stem codes" plus optional extension codes for laterality, severity, etc.).
- ICD-11 has a Mortality and Morbidity Statistics (MMS) classification used by WHO for international mortality reporting; US mortality reporting (NCHS) uses ICD-10 currently.
- **Treat ICD-11 as awareness-only** for US healthcare data work. Be alert to international datasets and academic literature that may use it.

## 8. Authoritative sources

- **CMS / NCHS ICD-9-CM archive**: <https://www.cdc.gov/nchs/icd/icd9cm.htm> (legacy reference)
- **CMS GEMs and Reimbursement Mappings archive**: <https://www.cms.gov/medicare/coding-billing/icd-10-codes/2018-icd-10-cm-pcs> (final FY2018 GEMs)
- **WHO ICD-11**: <https://icd.who.int/> (international, not US claims)

## 9. Common pitfalls

- **Treating GEMs as a 1:1 crosswalk.** Mapping every ICD-9 code through GEMs and taking the first row is a recurring source of silent error in retrospective cohort builds.
- **Applying GEMs after 2018.** Codes added to ICD-10-CM after FY2018 are not in any GEM. A 2018-frozen GEM file degrades over time.
- **Joining ICD-9 codes to ICD-10-based HCC or HEDIS value sets.** They will not match; the right approach is per-era cohorting or rollup grouping.
- **Storing ICD-9 and ICD-10 in the same column without a system marker.** `250.00` (ICD-9 Type 2 DM without complications) and ICD-10 codes coexist visually but mean different things; a `code_system` column is mandatory.
- **Assuming pre-2015 data uses ICD-10.** Some shops migrated their warehouses to ICD-10-only storage and back-mapped legacy ICD-9 data using GEMs. This is auditable; verify before trusting.
- **Confusing ICD-11 with ICD-10-CM/PCS.** They are different systems; ICD-11 is not US claims data.
