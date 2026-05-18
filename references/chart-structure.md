# Chart Structure & EHR Systems

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

## Copy-forward / cloning flags

- Identical ROS or PE text across multiple dates
- Vital signs that don't match flowsheet
- A/P that references "today's labs" with no labs from that date
- Provider attribution mismatch (note signed by Dr. A but text references "I, Dr. B")
- Time-stamped events that predate the note
