# ICD-10-PCS

> **Why this file exists:** ICD-10-PCS is the US **inpatient procedure** coding system. It's structurally completely different from ICD-10-CM (despite the shared "ICD-10" name) and from CPT (despite both being procedure systems). Treating PCS as if it were CPT - or as if it were a flat lookup - is a recurring mistake.

## 1. What it is

- **ICD-10-PCS** = International Classification of Diseases, 10th Revision, **Procedure Coding System**.
- Used by **US inpatient facilities** to report procedures on inpatient claims (UB-04 / 837I).
- Maintained by **CMS** (not NCHS - CMS owns PCS, NCHS owns CM).
- Replaced ICD-9-CM Volume 3 on **October 1, 2015**.
- **Not used by**:
  - Outpatient facility claims (use **CPT / HCPCS**)
  - Professional / physician claims (use **CPT / HCPCS**)
  - Pharmacy claims (use **NDC**)
  - EHR clinical documentation (typically SNOMED CT for procedures)

This narrow scope catches teams off-guard: PCS codes appear on inpatient facility claims **only**, and only on a small fraction of total US claim volume.

## 2. Structure - the 7-character grid

Every ICD-10-PCS code is **exactly 7 characters**, alphanumeric, **no decimal**. Each character position has a defined meaning that varies by section (the first character).

```
0   F   T   4   0   Z   Z
│   │   │   │   │   │   │
│   │   │   │   │   │   └─ Qualifier
│   │   │   │   │   └───── Device
│   │   │   │   └───────── Approach
│   │   │   └───────────── Body part
│   │   └───────────────── Root operation
│   └───────────────────── Body system
└───────────────────────── Section
```

### The seven character positions

| Position | Name | Example values |
|---|---|---|
| 1 | **Section** | `0` Medical/Surgical, `1` Obstetrics, `2` Placement, `3` Administration, `4` Measurement & Monitoring, `5` Extracorporeal Assistance, `6` Extracorporeal Therapies, `7` Osteopathic, `8` Other Procedures, `9` Chiropractic, `B` Imaging, `C` Nuclear Medicine, `D` Radiation Therapy, `F` PT/Rehab, `G` Mental Health, `H` Substance Abuse Treatment, `X` New Technology |
| 2 | **Body system** | Varies by section (e.g., Medical/Surgical: `0` Central Nervous System, `F` Hepatobiliary System and Pancreas) |
| 3 | **Root operation** | 31 root operations in the Medical/Surgical section - see §3 |
| 4 | **Body part** | Specific anatomic site |
| 5 | **Approach** | Open, Percutaneous, Percutaneous Endoscopic, Via Natural or Artificial Opening, Via Natural or Artificial Opening Endoscopic, External |
| 6 | **Device** | What is left in place (drainage device, monitoring device, synthetic substitute, autologous tissue, etc.) - `Z` = No Device |
| 7 | **Qualifier** | Additional attribute - often `Z` = No Qualifier |

The character-to-meaning map is **section-dependent**. Position 3 means "Root Operation" in Medical/Surgical but "Root Type" in Imaging. Always interpret characters in the context of the section character.

## 3. The 31 root operations (Medical/Surgical section)

The hardest part of PCS coding is choosing the correct **root operation** - the objective of the procedure. The 31 root operations are grouped:

- **Take out some/all of a body part**: Excision, Resection, Detachment, Destruction, Extraction
- **Take out solids/fluids/gases**: Drainage, Extirpation, Fragmentation
- **Cutting or separation only**: Division, Release
- **Put in / put back or move**: Transplantation, Reattachment, Transfer, Reposition
- **Alteration of diameter or route**: Restriction, Occlusion, Dilation, Bypass
- **Always involves a device**: Insertion, Replacement, Supplement, Change, Removal, Revision
- **Inspection / exploration**: Inspection, Map
- **Other repairs**: Control, Repair
- **Other objectives**: Fusion, Alteration, Creation

CMS publishes the **ICD-10-PCS Reference Manual** with formal definitions and examples for each root operation. Coders apply a **decision tree** approach (objective → root operation → body system → body part → approach → device → qualifier) using the Index and Tables. There is **no narrative-to-code lookup table** equivalent to ICD-10-CM's Alphabetic Index - PCS coding is more constructive.

## 4. Worked examples

| Code | Section | Decoding |
|---|---|---|
| `0FT40ZZ` | Medical/Surgical | `0` Med/Surg, `F` Hepatobiliary, `T` Resection, `4` Gallbladder, `0` Open, `Z` No Device, `Z` No Qualifier → **Open cholecystectomy** |
| `02HV33Z` | Medical/Surgical | `0` Med/Surg, `2` Heart and Great Vessels, `H` Insertion, `V` Superior Vena Cava, `3` Percutaneous, `3` Infusion Device, `Z` No Qualifier → **Insertion of infusion device into superior vena cava, percutaneous** |
| `B240ZZZ` | Imaging | `B` Imaging, `2` Heart, `4` CT Scan, `0` Heart, Right, `Z` No Contrast, `Z` Unenhanced and Enhanced, `Z` No Qualifier → **CT scan of right heart** |
| `0DTJ4ZZ` | Medical/Surgical | `0` Med/Surg, `D` Gastrointestinal, `T` Resection, `J` Appendix, `4` Percutaneous Endoscopic, `Z` No Device, `Z` No Qualifier → **Laparoscopic appendectomy** |

(Code values are illustrative; verify against the current PCS Tables.)

## 5. Conventions

- **No decimal.** Codes are stored as 7 characters straight, e.g., `0FT40ZZ`.
- **No multi-axis combinations** beyond the 7 characters. If a procedure crosses body systems, code each separately.
- **Letters `O` and `I` are not used** - they would be visually confused with `0` and `1`. PCS uses the digits.
- **The Index is a starting point, not authoritative.** The PCS **Tables** are authoritative; valid codes are constructed from valid combinations the table allows for a given section / body system / root operation row.
- **Bilateral procedures** that have a single bilateral body-part value use that value; if no bilateral body-part value exists, code the right and left sides separately.
- **Multiple body parts in one root operation**: code each body part separately.
- **Discontinued procedures**: rules differ by section; refer to the official Guidelines.

## 6. Annual update cycle

- **Effective October 1** of each year, same cadence as ICD-10-CM.
- New tables, new body-part values, new device values, occasional new root operations.
- **New Technology Section X** is a release-vehicle for emerging procedures and devices (e.g., novel devices, novel drugs administered via specific approach); codes added here can later migrate into the main sections.

## 7. PCS vs CPT - the most common confusion

| Aspect | ICD-10-PCS | CPT |
|---|---|---|
| Owner | CMS | AMA |
| Use | Inpatient facility | Outpatient + professional |
| Structure | 7-character constructive | 5-digit lookup |
| Update cadence | Annual Oct 1 | Annual Jan 1 |
| Licensing | Free | AMA-licensed |
| Modifiers | None (attributes embedded in code) | Yes (extensive modifier system) |
| Coding approach | Constructive (decision tree → table → valid combination) | Lookup |

A single inpatient stay may carry **both** ICD-10-PCS codes (on the facility 837I) and CPT codes (on the attending physician's professional 837P), describing overlapping procedures from facility and professional perspectives. Joining them requires care - see [`crosswalks.md`](crosswalks.md).

## 8. ICD-9-CM Volume 3 → ICD-10-PCS

- Pre-2015 inpatient claims used **ICD-9-CM Volume 3** (3-4 digit procedure codes, e.g., `47.0` appendectomy).
- The GEMs (General Equivalence Mappings) cover ICD-9-PCS ↔ ICD-10-PCS but the mapping is **highly lossy** because ICD-9-PCS is far less granular than ICD-10-PCS. A single ICD-9-PCS code often maps to many ICD-10-PCS codes.
- For longitudinal pre-/post-2015 analysis of inpatient procedures, treat the GEMs as a translation aid only and consider whether procedure rollups (e.g., CCSR Procedures) are a better unit of analysis. See [`code-groupers.md`](code-groupers.md).

## 9. MS-DRG / APR-DRG relationship

- ICD-10-PCS codes are **inputs** to inpatient DRG groupers (MS-DRG for Medicare, APR-DRG for many other payers and quality programs).
- The DRG grouper assigns a single payment / severity group per inpatient stay based on the principal diagnosis (ICD-10-CM), secondary diagnoses, principal procedure (ICD-10-PCS), and other procedures. See [`institutional-billing-codes.md`](institutional-billing-codes.md).

## 10. Authoritative source

- **CMS** publishes the **ICD-10-PCS Tables, Index, and Reference Manual** annually: <https://www.cms.gov/medicare/coding-billing/icd-10-codes>
- The Reference Manual is essential for understanding root-operation definitions.
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 11. Common pitfalls

- **Treating PCS like a flat lookup.** A "cholecystectomy" string does not map to one PCS code; the correct code depends on the approach (open vs laparoscopic), body part (whole gallbladder vs partial), and any device left in place.
- **Confusing PCS with CPT on outpatient procedures.** PCS does not appear on outpatient claims. If you see "PCS-like" codes on outpatient data, you likely have a data-quality issue.
- **Decoding character positions without checking the section.** The position-to-meaning map is section-dependent.
- **Joining inpatient PCS to outpatient CPT** without acknowledging they describe overlapping but not identical procedures.
- **Pre-2015 procedure analysis** using ICD-9-PCS without acknowledging the granularity gap.
