# Chart Structure & EHR Systems

> **Classifying the chart first?** This file covers the *universal* anatomy that applies to most encounter notes. For **chart-type detection** (inpatient vs observation vs SNF vs HHA vs hospice vs IRF vs L&D vs perioperative vs telehealth vs behavioral health, plus payer-program signals), see [`chart-types.md`](chart-types.md). Setting-specific documents (MDS, OASIS, IRF-PAI, hospice CTI, anesthesia record, partogram, growth chart) are catalogued there - not here.
>
> **Validating dates against a section?** This file defines the sections; [`date-of-service.md`](date-of-service.md) defines which sections are valid evidence for DoS attribution (Procedures / HPI / Op Note Body = valid; Plan / PMH / FamHx / Allergies / ROS = invalid for procedure DoS).
>
> **Reading the chart from a FHIR feed (DocumentReference, Composition, Encounter, US Core profiles) rather than a native EHR view?** The clinical anatomy stays here; the FHIR resource shapes and US Core profiles live in the `fhir-r4-implementation` skill's `references/us-core-ig.md`.

## Universal chart sections

| Section | Contents | Common gotchas |
|---|---|---|
| Demographics | Name, DOB, MRN, sex, address, insurance | MRN may differ across facilities; check enterprise MRN vs facility MRN |
| Problem list | Active/inactive diagnoses with ICD-10 | Often stale; "active" problems may be resolved |
| Medication list | Active, discontinued, home, inpatient | Distinguish prescribed vs taking; reconcile across sources |
| Allergies | Drug, food, environmental + reaction | "NKDA" ≠ "no allergies on file"; document reaction severity |
| Encounters | Visit notes, telephone, portal messages | Filter by note type and provider |
| Results | Labs, imaging, pathology, micro | Check result status (preliminary vs final) |
| Orders | Active, completed, discontinued | Discontinued orders may still appear |
| Immunizations | CVX-coded with dates | Reconcile with state registry (e.g., CAIR, ImmTrac) |
| Vitals / flowsheets | BP, HR, RR, SpO2, temp, weight, BMI | Trended series matter more than single values |
| Social / family history | Smoking, alcohol, drugs, occupation, family hx | Often outdated; check last-updated stamp |
| Advance directives | Code status, POLST/MOLST, healthcare proxy | Critical for inpatient/ED |

## EHR-specific quirks

### Epic
- **SmartText / SmartPhrase / dot-phrases (`.xxxx`)** expand to templated text — major copy-forward source.
- **Notes**: Progress Note, H&P, Consult, Procedure Note, Discharge Summary, Telephone Encounter.
- **Problem List** vs **Hospital Problems** vs **Visit Diagnoses** — three different lists.
- **Care Everywhere** pulls outside records; mark these as external.
- **Storyboard** (left rail) is a summary view, not the source of truth.

### Oracle Health (Cerner)
- **PowerNotes** with auto-text and structured sections.
- **CareCompass** = task list; **PowerChart** = main chart.
- **Dynamic Documentation** templates; watch for auto-populated negatives.

### Athenahealth
- **Clinical Inbox** workflow; encounter-based structure.
- Discrete data may live in **Quality Management** module separate from notes.

### Meditech (Expanse)
- Notes often free-text with limited templating.
- **PCI** (Physician Care Index) workflows.

### eClinicalWorks / NextGen / Allscripts (Veradigm)
- Heavier use of free-text; structured data variable.
- Verify diagnosis source: assessment field vs problem list vs billing.

## Note headers to look for

- **Chief Complaint (CC)**
- **History of Present Illness (HPI)** — OPQRST or OLDCARTS framework
- **Review of Systems (ROS)** — by system; flag "all systems negative" as potential cloning
- **Past Medical History (PMH) / Past Surgical History (PSH)**
- **Family History (FH) / Social History (SH)**
- **Medications / Allergies**
- **Physical Examination (PE)** — by system
- **Assessment & Plan (A/P)** — the legal/coding-relevant section
- **Disposition** — admit, discharge, transfer, observation

## Encounter flow — reviewer checklist

Most encounter notes (outpatient visit, ED note, H&P, consult) follow a standard top-to-bottom flow. When reviewing one, walk it in order and check each section against the rules below. Missing or inconsistent sections are findings, not defects to ignore.

```
Patient Header (sticky — should be on every page/note)
└── Demographics · Allergies · Active medication list · Code status
         │
Encounter body (read in order)
├── 1. Chief Complaint (CC)
├── 2. History of Present Illness (HPI)
├── 3. Review of Systems (ROS) — by body system
├── 4. Past/Family/Social History (PMH/FH/SH)
├── 5. Physical Examination (PE) — by body system
├── 6. Vitals & flowsheet data (trended where relevant)
├── 7. Results reviewed (labs / imaging / prior records)
├── 8. Assessment — diagnoses with clinical reasoning
├── 9. Plan — orders, meds, procedures, referrals, patient education
├── 10. Disposition & follow-up
└── 11. Signature / attestation / co-sign (resident → attending)
```

| Section | What to verify | Common findings |
|---|---|---|
| Patient header | Allergies + active meds match the body of the note | Allergic drug prescribed in Plan; med list contradicts HPI |
| 1. CC | Present and matches HPI/A&P | "Follow-up" with no specified condition; CC doesn't match billed E&M |
| 2. HPI | Adequate detail for billed E&M level; OPQRST/OLDCARTS elements | HPI cloned from prior visit; HPI inconsistent with diagnosis |
| 3. ROS | System count matches billed E&M; not blanket "all negative" | "10-system negative ROS" copy-forward; ROS contradicts HPI |
| 4. PMH/FH/SH | Updated stamp recent; smoking/alcohol/substance status current | Last updated >12 months; conflicts with problem list |
| 5. PE | Findings support diagnoses in A&P | "Normal" PE with documented acute pathology; cloned PE across patients |
| 6. Vitals | In note matches flowsheet; abnormals addressed | BP 195/110 with no plan; SpO2 86% with no intervention |
| 7. Results | Labs/imaging cited actually exist on dates referenced | "Today's labs show..." with no lab from that date |
| 8. Assessment | Each diagnosis has MEAT (Monitor, Evaluate, Assess, Treat) | Diagnosis listed without supporting clinical detail (HCC risk) |
| 9. Plan | Each diagnosis in A has a corresponding plan element | Diabetes assessed, no diabetes management; medication started with no indication |
| 10. Disposition / follow-up | Appropriate for acuity; high-risk dx has interval and contingency | Discharge with no follow-up for new CHF/CAD/cancer dx |
| 11. Signature | Signed, timed, attribution clear; attending co-sign present if required | Note references "I, Dr. B" but signed by Dr. A; missing attending attestation |

### What to elevate

- **Missing section that justifies billing** → coding/CDI finding
- **Internal contradiction** (e.g., assessment doesn't match plan, vitals don't match flowsheet) → documentation finding
- **Abnormal value with no addressed plan** → critical / patient-safety finding
- **Section present but cloned from a prior date** → documentation integrity finding (see Copy-forward / cloning flags below)

## Copy-forward / cloning flags

- Identical ROS or PE text across multiple dates
- Vital signs that don't match flowsheet
- A/P that references "today's labs" with no labs from that date
- Provider attribution mismatch (note signed by Dr. A but text references "I, Dr. B")
- Time-stamped events that predate the note
