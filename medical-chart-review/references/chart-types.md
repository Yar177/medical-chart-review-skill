# Chart Types: Detection & Differentiation

> **Purpose:** Classify a chart by **care setting** and **payer program** from content signals before applying setting-specific review rules. Authoritative chart-type taxonomy for the repo - sibling skills (`hedis-nlp`, `hcc-nlp`) link here, not duplicate.

A "chart" can mean one encounter or a longitudinal record spanning many settings. Classify **per encounter** when the record is mixed (see §4).

## 0. How to use this file

1. If the user declared the chart type, validate against §1-§2 signals; only flag on contradiction.
2. If undeclared, scan §1 + §2 for high-precision signals.
3. Score confidence per §3; proceed, caveat, or ask the user.
4. Emit a triage report using [`../templates/chart-triage.md`](../templates/chart-triage.md).

Pair with [`note-types.md`](note-types.md), [`chart-structure.md`](chart-structure.md), [`coding-cpt-drg.md`](coding-cpt-drg.md), [`administrative-insurance.md`](administrative-insurance.md).

---

## 1. Care Settings - definition, signals, billing

`MDM` = medical decision making · `ESI` = Emergency Severity Index · `POS` = place of service · `LOS` = length of stay

| Setting | Definition | High-precision detection signals | Billing basis |
|---|---|---|---|
| **Inpatient acute** | Hospital admission, ≥2 midnights expected | "Admit to inpatient" order; admission H&P + daily progress notes + discharge summary at same facility | MS-DRG / APR-DRG |
| **Observation** | Hospital outpatient status, usually <2 midnights | "Place in observation" / "obs status" order; HCPCS G0378; hourly nursing flowsheet | APC + G0378 |
| **Outpatient / ambulatory** | Clinic, primary care, specialist office | Single SOAP encounter, longitudinal problem list, POS 11 | E&M 99202-99215 |
| **Emergency Department** | Hospital ED encounter | ESI level 1-5; triage acuity; EMTALA / medical screening exam; "disposition: admit/discharge/AMA"; POS 23 | ED E&M 99281-99285 |
| **Skilled Nursing Facility (SNF)** | Post-acute skilled care | **MDS 3.0 / RAI form** (the form name disambiguates; Section GG codes alone are shared across SNF/IRF/LTCH/HHA under IMPACT Act); RUG / PDPM HIPPS code; POS 31 | PDPM (Part A) |
| **Home Health (HHA)** | Skilled home care | **OASIS-E** items (M1800, M1860); CMS-485 plan of care; "homebound" + "face-to-face encounter for home health"; POS 12 | PDGM, 60-day episodes |
| **Inpatient Rehab (IRF)** | Intensive rehab admission | **IRF-PAI**; FIM / GG score table; "3-hour rule"; weekly team conference | IRF PPS / CMG |
| **Long-Term Care Hospital (LTCH)** | LTCH stay, ALOS >25 days | **LTCH-CARE Data Set**; MS-LTC-DRG | LTCH PPS |
| **Hospice** | Terminal illness, ≤6 mo prognosis | **Certification of Terminal Illness (CTI)**; election statement; IDG note; RHC/CHC/IRC/GIP levels | Per-diem |
| **Labor & Delivery (L&D)** | Pregnancy admission for delivery | Partogram / labor flowsheet; "cervical dilation / effacement / station"; fetal heart strip; APGAR 1/5 min; delivery note | DRG 765-768, 774-775, 783-788 |
| **Perioperative (surgical)** | OR encounter, any setting | **Pre-op H&P + anesthesia record + op note + PACU note** (the triad); EBL, ASA class | CPT surgical + facility |
| **Pediatric** | Patient <18, any setting | Growth-chart percentiles plotted for age; CVX childhood schedule; Bright Futures / WCC visits; developmental screening (ASQ-3, M-CHAT) | Same as adult by setting |
| **Telehealth** | Synchronous video/audio across distance | "Video visit" / "audio-only"; originating + distant site documented; POS 02 or 10; modifier 95/93 | E&M + modifier |
| **Behavioral health** | Psych / SUD treatment, any setting | Psychotherapy notes kept **separate** from medical record; CPT 90832-90838; treatment plan with goals; serial PHQ-9 / GAD-7 / MSE | E&M, psychotherapy, H-codes |
| **Urgent care** | Walk-in non-emergent | POS 20; HCPCS S9083/S9088; single SOAP, no triage acuity | E&M outpatient |

### Note-type and POS corroborators

POS codes alone are corroborating, not dispositive. Common values: `11` office, `12` home, `20` urgent care, `21` inpatient hospital, `22` outpatient hospital, `23` ED, `31` SNF, `32` nursing facility (non-skilled), `02`/`10` telehealth.

For note-level signals, see [`note-types.md`](note-types.md).

### Cross-cutting attributes (layer on a primary setting)

Some entries in the table above are **attributes** that combine with a primary setting rather than replace it. Capture them as separate fields in the triage report's `Attributes` row.

| Attribute | Combines with | How to record |
|---|---|---|
| **Pediatric** | Any setting | `attributes: [pediatric]` + primary setting (e.g., pediatric + ED) |
| **L&D / Newborn** | Inpatient acute (almost always) | `setting: inpatient acute, attributes: [L&D]` or `[newborn]` |
| **Perioperative** | Inpatient acute, outpatient (ASC), or outpatient hospital | `setting: <primary>, attributes: [perioperative]` |
| **Telehealth (modality)** | Outpatient, BH, urgent care | `setting: <primary>, attributes: [telehealth-modality]` (see §5) |

Use a standalone primary setting (`pediatric`, `L&D`, `perioperative`, `telehealth`) **only** when the attribute is the dominant axis and no underlying setting is identifiable.

---

## 2. Payer Programs

| Program | Identifies as | Key chart implications |
|---|---|---|
| **Medicare FFS** | 11-character alphanumeric MBI on face sheet (e.g., `1EG4-TE5-MK73`), no plan name | DRG inpatient; E&M outpatient; LCDs |
| **Medicare Advantage (MA)** | MA plan name (Humana Gold Plus, UnitedHealthcare AARP MA, Aetna Medicare, Kaiser Senior Advantage); contract ID starting with `H` | **HCC capture drives revenue**; HEDIS gated to MA; CMS-HCC V28 |
| **ACA Marketplace** | Plan tier (Bronze/Silver/Gold/Platinum); "Marketplace" / QHP issuer ID | **HHS-HCC model** (different from CMS-HCC); EHB |
| **Medicaid (state)** | State Medicaid ID; MCO name; "Medi-Cal" / "MassHealth" / "Apple Health"; CHIP | EPSDT for <21; state quality programs |
| **Commercial / ERISA** | Employer group; commercial issuer; PPO/HMO/EPO/POS | HEDIS commercial; prior auth heavy |
| **VA / DoD** | VA station number; MHS Genesis source; DEERS; TRICARE plan name | Service-connected dx; separate formularies |
| **Workers' Compensation** | WC claim number, employer, date of injury | Causation-focused documentation |
| **Auto / Liability (PIP/MedPay)** | Claim number, accident date, attorney info | Third-party documentation |
| **Self-pay / uninsured** | No payer; sliding scale; charity care flag | 501(r) compliance for nonprofits |

When multiple payers are listed with COB order, use the **primary** for classification and note COB.

---

## 3. Confidence Scoring

| Confidence | Criteria | Action |
|---|---|---|
| **High** | ≥1 high-precision signal from §1 **and** no contradicting signal **and** payer program identifiable (or explicitly unknown) | Proceed; cite signals in triage report |
| **Medium** | Only corroborating signals (POS code, note-type pattern), or one high-precision signal with weak corroboration | Proceed with caveat; surface alternatives; ask the user to confirm if downstream review depends on it |
| **Low** | No high-precision signals; ambiguous content (short generic note, no headers, no payer info) | **Stop and ask.** Do not guess. List what signals would resolve it |

Downgrade one level on any contradiction.

**Always ask the user, regardless of confidence:**
- Inpatient vs Observation when LOS is 24-48h and no explicit order is documented
- SNF vs IRF vs LTCH when the assessment instrument is missing
- Telehealth-as-modality vs Telehealth-as-setting (see §5)
- Behavioral health when the document may be a 42 CFR Part 2 protected psychotherapy note
- Payer program when a downstream review depends on it (HCC for MA, HEDIS commercial vs MA, EPSDT for Medicaid peds)

---

## 4. Disambiguation - dispositive signals

| Plausible pair | Dispositive signal (the one that wins) |
|---|---|
| Inpatient vs Observation | **Order text.** Obs wins even with long LOS unless the order was formally converted to inpatient |
| SNF vs IRF vs LTCH | **Assessment instrument.** MDS → SNF, IRF-PAI → IRF, LTCH-CARE → LTCH. No instrument → ask |
| HHA vs Hospice-at-home | **Signed CTI + election statement** → Hospice. Otherwise HHA |
| Urgent Care vs ED | **ESI triage level** documented → ED |
| Inpatient vs Ambulatory surgery | **Admit/discharge same calendar day + op note** → ambulatory surgery |

## 5. Telehealth: modality vs setting

- **Modality** (default): an outpatient or BH practice delivered a visit via video. Classify by the underlying setting; tag `modality=telehealth`.
- **Setting**: only when the entire chart is from a telehealth-only group with no bricks-and-mortar practice. Rare.

---

## 6. Multi-setting / Longitudinal Records

Common in Epic enterprise exports, Care Everywhere pulls, MA risk-adjustment sweeps. Procedure:

1. **Segment by encounter** using admission/discharge timestamps, encounter IDs, or facility changes as boundaries.
2. **Classify each segment** independently using §1-§3.
3. **Report a per-encounter table** in the triage output, not a single chart-level label.
4. **Identify transitions** (acute → SNF, acute → HHA, ED → admit, SNF → hospice) - these drive TRC / MRP / PCR quality measures and CDI hand-off review.
5. **Flag external records** (Care Everywhere, CCDA imports) and classify them by the source facility's signals.

---

## 7. Behavioral Health & 42 CFR Part 2

If you detect a Part 2 banner, a Part 2 program origin (methadone clinic, SUD treatment program), or psychotherapy notes maintained separately from the medical record: **stop and read [`hipaa-privacy.md`](hipaa-privacy.md) before proceeding.** Note the privacy class in the triage report; do not paste excerpts.
