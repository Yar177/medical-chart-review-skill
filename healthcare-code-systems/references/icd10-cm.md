# ICD-10-CM

> **Why this file exists:** ICD-10-CM is the diagnosis code set used on virtually every US healthcare claim and every clinical encounter that touches a US payer. Almost every analytic, NLP, quality, and risk-adjustment pipeline starts here. The structure looks simple and is not.

## 1. What it is

- **ICD-10-CM** = International Classification of Diseases, 10th Revision, **Clinical Modification**.
- US-specific adaptation of WHO ICD-10, maintained by **CDC/NCHS** (the clinical modifications) with **CMS** (procedure coding for inpatient via ICD-10-PCS, a separate system - see [`icd10-pcs.md`](icd10-pcs.md)).
- Used for **diagnosis** coding in all US healthcare settings: inpatient, outpatient, ED, professional, behavioral, dental (limited), etc.
- Replaced ICD-9-CM for US claims on **October 1, 2015** (the "ICD-10 transition"). See [`icd9-and-legacy.md`](icd9-and-legacy.md) for legacy handling.
- The ICD-11 conversation is real internationally but **US claims have not adopted ICD-11**. Treat ICD-11 as awareness-only for US data work.

## 2. Structure

ICD-10-CM codes are **3 to 7 characters**, alphanumeric, with a decimal point after the third character.

```
E  1  1  .  3  1  1  A
│  │  │     │  │  │  │
│  │  │     │  │  │  └─ 7th-character extension (selected categories)
│  │  │     │  │  └──── 6th character (further specificity)
│  │  │     │  └─────── 5th character (further specificity)
│  │  │     └────────── decimal point (storage convention varies)
│  │  └──────────────── 3rd character (category)
│  └─────────────────── 2nd character (category)
└────────────────────── 1st character (alpha, chapter indicator)
```

- **1st character** is always alphabetic and indicates the chapter (e.g., `A`/`B` = infectious, `C`/`D` = neoplasms, `E` = endocrine/metabolic, `I` = circulatory, `J` = respiratory, `S`/`T` = injury / poisoning, `V`-`Y` = external causes, `Z` = factors influencing health status).
- **First three characters** form the **category** (e.g., `E11` = Type 2 diabetes mellitus).
- **Characters 4-6** add etiology, anatomic site, severity, manifestation.
- **7th character extension** (when present) is most often **A** (initial encounter), **D** (subsequent encounter), **S** (sequela) for injuries; or other letters for fractures, OB, etc.
- **Placeholder `X`** is used to pad positions 4-6 when a 7th-character extension is required but lower positions are empty (e.g., `T81.4XXA`).

### Worked example

| Code | Meaning |
|---|---|
| `E11` | Type 2 diabetes mellitus (category - **not billable alone**) |
| `E11.9` | Type 2 DM without complications |
| `E11.40` | Type 2 DM with diabetic neuropathy, unspecified |
| `E11.311` | Type 2 DM with unspecified diabetic retinopathy with macular edema |
| `S72.001A` | Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| `T81.4XXA` | Infection following a procedure, initial encounter (note `X` placeholders) |

## 3. Conventions (the parts that bite you)

### Excludes1 vs Excludes2

- **Excludes1** = "NOT CODED HERE" - the two conditions cannot be reported together; if one applies, the other does not.
- **Excludes2** = "Not included here" - the excluded condition is **separate** and **may be reported additionally** if present.
- The two are visually identical at a glance. Confusing them is a classic coding error.

### Code first / use additional

- **"Code first"** notes indicate an etiology code must be sequenced before the manifestation code.
- **"Use additional code"** indicates a secondary code to provide additional information.
- Examples: code first the underlying diabetes (`E11.x`) when reporting a diabetic manifestation; use additional code for any infectious agent.

### Combination codes

- Some codes combine two conditions, a condition with a complication, or a condition with a manifestation, in **one** code. Reporting them separately is wrong.
- Example: `E11.21` = Type 2 DM with diabetic nephropathy - do not also separately code the nephropathy.

### Laterality

- Many codes have right (`1`), left (`2`), bilateral (`3`), unspecified (`0` or `9`) variants encoded in the 5th or 6th character. Using `unspecified` when documentation supports a side is a common quality issue.

### Default codes

- The Alphabetic Index lists certain codes as defaults when the medical record does not specify type, site, or severity. The Tabular List is always authoritative over the Index.

### "With" convention

- The word "with" or "in" in a code title or sub-term in the Alphabetic Index is interpreted as "associated with" or "due to" when the two conditions are listed together - a presumed causal link **without** requiring explicit documentation of cause (e.g., diabetes with chronic kidney disease).

### NOS vs NEC

- **NOS** = "Not Otherwise Specified" = unspecified (equivalent to "unspecified" in the title).
- **NEC** = "Not Elsewhere Classifiable" = the code is for "other specified" conditions not covered by more specific codes.

## 4. Z-codes (a major NLP/risk pitfall)

Chapter 21 (`Z00`-`Z99`) covers "Factors influencing health status and contact with health services." Some are billable as primary; many are status / history codes that look like active disease but are not.

- **History-of** codes (`Z85.x` = personal history of malignant neoplasm; `Z86.x` = personal history of certain other diseases; `Z87.x` = personal history of other diseases and conditions): the condition is **resolved**, not active. Do not treat as active diagnosis for risk adjustment or HEDIS denominators without per-family logic. See [`common-pitfalls.md`](common-pitfalls.md).
- **Status** codes (`Z89.x` = absence of limb; `Z93.x` = ostomy; `Z94.x` = transplant; `Z95.x` = cardiac implants; `Z96.x` = other implants; `Z99.x` = dependence on enabling machines): some IMPLY ongoing risk-adjusted disease (amputation status, transplant status); some do not (post-cardiac-implant `Z95.x` does not by itself imply current heart failure).
- **Screening** (`Z11`, `Z12`, `Z13`): screening for disease, not the disease itself.
- **Encounter for** codes (`Z00`-`Z02`, etc.): visit reason rather than disease.

See the `hcc-nlp` skill's `references/negation-and-assertion.md` for the NLP-side treatment.

## 5. External cause codes, place of occurrence, activity

- `V00`-`Y99` external causes (mechanism of injury), `W` / `X` / `Y` for place / activity. Many payers do not require them but some quality programs do.

## 6. Annual update cycle

- **Effective date: October 1** of each year (federal fiscal year start). Codes added, deleted, or revised on that date apply to **dates of service on or after October 1**.
- Mid-year addenda are rare but possible (recent example: COVID-19 codes added off-cycle).
- The NCHS / CMS coordinate the annual update. Files published in advance (typically June-August) for the upcoming October.

### Implication for pipelines

- Always join an ICD-10-CM code to the **code-set version that was effective on the date of service**, not the latest. A code that became active 2023-10-01 will not be found in the 2023-09-30 file.
- Pipelines that join against "the latest code file" will silently drop or mis-describe codes on old dates of service. Store an `effective_from` / `effective_to` per code or attach a `code_system_version` snapshot date to every code emission. See [`versioning-and-drift.md`](versioning-and-drift.md).

## 7. Storage conventions (pick one and document it)

| Convention | Example | Pros | Cons |
|---|---|---|---|
| **With decimal** | `E11.40` | Matches printed form; human-readable | Variable width; some systems strip dots silently |
| **Without decimal** | `E1140` | Fixed-ish width; simpler joins | Hides category boundary; harder to read; conflict with codes whose 4+ chars start at a digit |
| **Mixed** | both stored | Maximum compatibility | Doubles storage; risk of divergence |

Recommendation: pick **one canonical form** for storage, document it in the warehouse contract, and convert at the boundary. The common-pitfalls file lists join misses caused by decimal mismatches between source systems.

## 8. Coding guidelines

The **ICD-10-CM Official Guidelines for Coding and Reporting** (jointly published by CDC / NCHS / CMS / AHIMA / AHA each year) are the authoritative interpretive guidance. The guidelines are **part of HIPAA** and must be followed for HIPAA-covered transactions.

Key sections to be aware of (numbering follows the standard guideline structure):

- **Section I** General coding guidelines (Excludes, sequencing, signs / symptoms, combination codes, "with" convention)
- **Section II** Selection of principal diagnosis (inpatient)
- **Section III** Reporting additional diagnoses (inpatient)
- **Section IV** Diagnostic coding for outpatient services

For HCC-specific coding rules and MEAT criteria layered on top of ICD-10-CM, see the `hcc-nlp` skill.

## 9. Authoritative source

- **CDC / NCHS** publishes the **ICD-10-CM Tabular List, Alphabetic Index, and Guidelines** annually: <https://www.cdc.gov/nchs/icd/icd10cm.htm>
- **CMS** publishes the ICD-10-CM and ICD-10-PCS files in a unified annual release: <https://www.cms.gov/medicare/coding-billing/icd-10-codes>
- Pull from the primary source; do not rely on a third-party code lookup site for production data. See [`sources-and-licensing.md`](sources-and-licensing.md).

## 10. Common pitfalls (quick list - full treatment in `common-pitfalls.md`)

- **Decimal handling mismatch** between source systems causes silent join misses (`E11.40` vs `E1140`).
- **Truncated codes** (3-character categories like `E11` stored as if billable) - not billable; usually a documentation or data-quality artifact.
- **"Unspecified" code dominance** - quality penalty in many programs; an indicator the upstream documentation is missing detail.
- **Z-code conflation** - treating `Z85.x` (history of) as active disease for risk adjustment is the single most common risk-adjustment NLP error. See `hcc-nlp` and [`common-pitfalls.md`](common-pitfalls.md).
- **Cross-FY version drift** - joining DOS-2018 codes against a FY2026 code file misses codes added after 2018 and mis-describes codes whose meaning evolved.
- **Excludes1 misuse** - reporting two codes together that are mutually exclusive triggers payer edits.
- **7th-character extension dropped** or stored separately, breaking the code's meaning (e.g., `S72.001` instead of `S72.001A`).

## 11. What this file does NOT cover

- **ICD-10-PCS** (inpatient procedures, separate 7-character system) → [`icd10-pcs.md`](icd10-pcs.md).
- **ICD-9-CM** legacy and **GEMs** crosswalk → [`icd9-and-legacy.md`](icd9-and-legacy.md) and [`crosswalks.md`](crosswalks.md).
- **ICD-10 → HCC** mapping → [`crosswalks.md`](crosswalks.md); production HCC NLP logic → `hcc-nlp` skill.
- **HEDIS value sets** referencing ICD-10-CM → [`value-sets-and-vsac.md`](value-sets-and-vsac.md); per-measure logic → `hedis-nlp` skill.
- **Z-code disambiguation as NLP** → `hcc-nlp` skill's `references/negation-and-assertion.md`.
