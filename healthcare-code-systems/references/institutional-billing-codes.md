# Institutional billing codes

> **Why this file exists:** Institutional claims (UB-04 / 837I) carry several code systems on top of ICD-10-CM / PCS and HCPCS / CPT - **revenue codes**, **type of bill (TOB)**, **place of service (POS)**, and the **DRG / APC** groupers that determine payment. These are the codes that determine *how* an encounter is classified for analytics (inpatient vs outpatient vs SNF vs HHA vs ED) and how it gets paid.

## 1. Revenue codes (UB-04)

- **4-digit numeric** codes (some sources show as 3-digit; the leading zero is required: `0450`, not `450`).
- Maintained by the **National Uniform Billing Committee (NUBC)** - licensed (NUBC subscription typically required for full code descriptions).
- Identify the **department / cost center / service category** that delivered the service.
- Appear on **institutional claims only** (UB-04 / 837I); do not appear on professional claims (CMS-1500 / 837P).
- Multiple revenue codes per claim are normal - one per service line.

### Major revenue-code series

| Range | Series |
|---|---|
| `0100`-`0179` | Room & board (inpatient) |
| `0200`-`0219` | Intensive care |
| `0220`-`0229` | Nursery |
| `0230`-`0239` | Incremental nursing charge |
| `0250`-`0259` | Pharmacy |
| `0260`-`0269` | IV therapy |
| `0270`-`0279` | Medical / surgical supplies |
| `0280`-`0289` | Oncology |
| `0290`-`0299` | DME |
| `0300`-`0319` | Laboratory |
| `0320`-`0359` | Radiology / imaging |
| `0360`-`0379` | Operating room services |
| `0400`-`0409` | Other imaging |
| `0410`-`0419` | Respiratory services |
| `0420`-`0449` | Physical / occupational / speech therapy |
| `0450`-`0459` | **Emergency room** |
| `0460`-`0469` | Pulmonary function |
| `0480`-`0489` | Cardiology / cath lab |
| `0490`-`0499` | Ambulatory surgical care |
| `0510`-`0529` | Clinic visits |
| `0540`-`0549` | Ambulance |
| `0550`-`0599` | Home health / SNF services |
| `0610`-`0619` | MRI |
| `0636`-`0636` | Drugs requiring detailed coding |
| `0710`-`0719` | Recovery room |
| `0762`-`0762` | Observation room |
| `0820`-`0859` | Hemodialysis / peritoneal dialysis |
| `0900`-`0999` | Behavioral health |

### Common analytics uses

- **ER identification**: revenue code `045x` on a facility claim flags an ED encounter. Combine with POS for cross-validation.
- **Observation status**: revenue code `0762` distinguishes observation from inpatient (a perennial source of confusion in inpatient cohort definitions).
- **Operating room utilization**: `036x` for OR, `071x` for recovery.
- **Pharmacy on facility claims**: `025x` covers facility-administered drugs.

## 2. Type of Bill (TOB)

- **4-digit** code on the UB-04 (formerly 3-digit; CMS expanded to 4 by adding a leading zero).
- Each digit position has defined meaning:

```
0  1  3  1
│  │  │  │
│  │  │  └─ Frequency (1 = admit-thru-discharge, 7 = replacement, 8 = void, etc.)
│  │  └──── Bill classification (1 = inpatient Part A, 2 = inpatient Part B, 3 = outpatient, 4 = OP/ASC, ...)
│  └─────── Type of facility (1 = hospital, 2 = SNF, 3 = HHA, 4 = religious nonmedical hospital, ...)
└────────── Leading zero (added in 4-digit form)
```

### Common TOB values

| TOB | Meaning |
|---|---|
| `0111` | Inpatient hospital, admit-thru-discharge |
| `0117` | Inpatient hospital, replacement |
| `0131` | Outpatient hospital, admit-thru-discharge |
| `0137` | Outpatient hospital, replacement |
| `0141` | Hospital non-patient (lab) |
| `0211` | SNF inpatient Part A, admit-thru-discharge |
| `0212` | SNF inpatient Part B (occurs after Part A benefits exhaust) |
| `0321` | HHA, admit-thru-discharge |
| `0341` | HHA non-patient |
| `0721` | ESRD outpatient, admit-thru-discharge |
| `0810` | Hospice, non-hospital |
| `0851` | Critical access hospital |

### Analytics implications

- **Inpatient vs outpatient identification** on facility claims is driven by TOB position 3 (`1` = inpatient, `3` = outpatient).
- **Setting identification** (hospital vs SNF vs HHA vs hospice) is TOB position 2.
- **Replacement and void claims** (TOB frequency `7` and `8`) supersede prior submissions; pipelines that count claims without filtering for the latest by submission sequence over-count.
- See the `medical-chart-review` skill's `references/chart-types.md` for the clinical / setting taxonomy that TOB + POS together drive.

## 3. Place of Service (POS) codes

- **2-digit numeric** code on professional claims (CMS-1500 / 837P).
- Identifies the **location where the service was furnished**.
- Maintained by **CMS** (POS code set on the CMS website).
- Free / public domain.

### Common POS values

| POS | Meaning |
|---|---|
| `01` | Pharmacy |
| `02` | **Telehealth - distant site (provider not at patient home)** |
| `10` | **Telehealth - patient at home** |
| `11` | Office |
| `12` | Patient home |
| `19` | Off-campus outpatient hospital |
| `20` | Urgent care facility |
| `21` | Inpatient hospital |
| `22` | On-campus outpatient hospital |
| `23` | Emergency room - hospital |
| `24` | Ambulatory surgical center |
| `31` | Skilled nursing facility |
| `32` | Nursing facility (non-skilled) |
| `33` | Custodial care facility |
| `34` | Hospice |
| `41` | Ambulance - land |
| `42` | Ambulance - air or water |
| `49` | Independent clinic |
| `50` | Federally qualified health center |
| `51` | Inpatient psychiatric facility |
| `52` | Psychiatric facility - partial hospitalization |
| `53` | Community mental health center |
| `57` | Non-residential substance abuse treatment |
| `61` | Comprehensive inpatient rehabilitation facility |
| `62` | Comprehensive outpatient rehabilitation facility |
| `65` | End-stage renal disease treatment facility |
| `71` | State or local public health clinic |
| `72` | Rural health clinic |
| `81` | Independent laboratory |

### Analytics implications

- **Telehealth identification on professional claims** is driven by POS `02` / `10` plus modifiers (`-95`, `-GT`, `-GQ`). All four signals matter.
- **POS `21` (inpatient hospital)** on a professional claim indicates the physician saw the patient during an inpatient stay - the facility-side claim will be separate with TOB `011x`.
- **Office (POS `11`) vs outpatient hospital (POS `22`)** is a perennial cost / quality classification question; the same patient, same procedure, same physician can be coded differently depending on the practice's affiliation, with significant payment implications.

## 4. DRG groupers - MS-DRG and APR-DRG

DRGs are the per-inpatient-stay payment / severity classification systems. The **grouper** takes the principal diagnosis, secondary diagnoses, principal procedure, other procedures, age, sex, and discharge status, and assigns a **single DRG** per stay.

### MS-DRG

- **Medicare Severity DRG** - maintained by **CMS**, used by **Medicare** for inpatient PPS payment.
- **3-digit numeric** values (`001`-`999`).
- Annual update aligned with the federal fiscal year (October 1).
- Stratified by **complication / comorbidity (CC) and major CC (MCC)** logic - secondary diagnoses on the CC / MCC list elevate the DRG.
- **Examples**: `291` Heart failure & shock w MCC, `292` Heart failure & shock w CC, `293` Heart failure & shock w/o CC/MCC.

### APR-DRG

- **All Patient Refined DRG** - maintained by **3M Health Information Systems** (proprietary; commercial licensing required).
- Used by many state Medicaid programs, commercial payers, and quality programs (AHRQ uses APR-DRG-derived measures).
- Adds **Severity of Illness (SOI)** and **Risk of Mortality (ROM)** sub-classes 1-4 (minor / moderate / major / extreme) to the base DRG.
- More granular than MS-DRG; not interchangeable.

### Analytics implications

- **MS-DRG and APR-DRG are not interchangeable.** A pipeline using MS-DRG cannot apply APR-DRG-trained models without re-grouping.
- The **DRG itself is computed by a grouper** - it is not a code typed by a coder. Two warehouses re-running different grouper versions on the same encounter can produce different DRGs.
- DRG version pinning is essential for any payment, severity, or quality use.

## 5. APC - Ambulatory Payment Classification

- **CMS-maintained** outpatient prospective payment system (OPPS) grouper for hospital outpatient services.
- **4-digit numeric** codes (`0001`-`9999`).
- Each APC is a bundle of related outpatient services that share clinical and resource characteristics.
- The hospital outpatient claim's HCPCS / CPT codes are grouped by the OPPS grouper into one or more APCs for payment.
- Updated quarterly (Addenda A and B publish quarterly).

### Analytics use

- Outpatient cost / utilization analytics often roll up to APC for service-line groupings.
- Status indicators (`S`, `T`, `V`, `X`, etc.) on each APC code govern how it is paid (separately, packaged, etc.).

## 6. UB-04 / 837I fields beyond codes

While not "code systems" per se, several other UB-04 fields use coded values:

- **Admission type** (`1` Emergency, `2` Urgent, `3` Elective, `4` Newborn, `5` Trauma)
- **Admission source** (`1` Non-healthcare facility, `2` Clinic, `4` Transfer from hospital, etc.)
- **Discharge status** (3-digit; commonly `01` discharged home, `02` discharged to short-term hospital, `03` SNF, `06` home with home health, `20` expired, `30` still patient, etc.)
- **Condition codes**, **Occurrence codes**, **Value codes** - each with their own NUBC-maintained code lists, used for context (e.g., condition code `04` Information only bill).

## 7. Authoritative sources

- **CMS POS code set**: <https://www.cms.gov/medicare/coding-billing/place-of-service-codes>
- **CMS MS-DRG / IPPS files**: <https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps>
- **CMS OPPS / APC files**: <https://www.cms.gov/medicare/payment/prospective-payment-systems/hospital-outpatient>
- **NUBC** (UB-04, revenue codes, condition / occurrence / value codes, TOB): <https://www.nubc.org/> - subscription required for full code descriptions.
- **3M APR-DRG**: commercial licensing via 3M.
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 8. Common pitfalls

- **Stripping the leading zero** from revenue codes / TOB / POS, losing meaning (`450` ≠ `0450`).
- **Inpatient vs observation confusion**: TOB `011x` is inpatient; revenue `0762` is observation. A patient can be in a hospital bed under either status, with vastly different payment and quality implications.
- **Counting replacement / void claims** as additional encounters instead of supersedes / cancellations.
- **DRG version mismatch** across years or across payers (MS-DRG vs APR-DRG).
- **POS `02` vs POS `10` telehealth split** (added 2022) treated as a single category, obscuring the patient-at-home vs other-site distinction.
- **NUBC code descriptions** scraped from non-subscription sources may be stale or inaccurate.
- **ER detection** by ICD-10 alone is unreliable; the canonical signals are revenue `045x` (facility), POS `23` (professional), or specific E/M codes (`99281`-`99285`).
