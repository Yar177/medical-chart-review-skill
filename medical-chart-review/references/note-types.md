# Clinical Note Types

> **Validating the DoS for a note?** For the default DoS source per note type (op note → `Date of Procedure:` header; lab report → collection date; progress note → encounter header date; etc.), see [`date-of-service.md`](date-of-service.md) §2.

## SOAP format
- **S — Subjective**: patient's reported symptoms, HPI, ROS, history updates
- **O — Objective**: vitals, exam findings, labs, imaging, measured data
- **A — Assessment**: diagnoses with clinical reasoning; one per problem
- **P — Plan**: workup, treatment, medications, follow-up, patient education

For each Assessment item, look for **MEAT** (see `coding-icd10-hcc.md`).

## Common note types

| Note | Purpose | Key fields | Coding relevance |
|---|---|---|---|
| **H&P** (History & Physical) | Admission baseline | Full HPI, ROS, PE, A/P, problem list | Anchors inpatient stay |
| **Progress Note** | Daily inpatient or follow-up | Interval history, exam, A/P | Required for each day billed |
| **Consult Note** | Specialist evaluation | Reason for consult, recs | E&M consult codes; HCC capture |
| **Discharge Summary** | End-of-stay summary | Hospital course, dx, meds, f/u | DRG validation, transitions of care |
| **Procedure Note** | Bedside/minor procedure | Indication, technique, findings | CPT capture |
| **Operative Note** | Surgical case | Pre/post-op dx, procedure, EBL, specimens | DRG, CPT, modifiers |
| **ED Note** | Emergency visit | Triage, MDM, disposition | ED E&M leveling |
| **Telephone / Portal** | Async communication | Patient concern, response | Usually non-billable but legal record |
| **Nursing Note** | Care delivery, observations | Vitals, intake/output, behavior | Supports medical necessity |
| **Therapy Notes** (PT/OT/SLP) | Functional status | Goals, progress, plan | Supports SNF/HHA necessity |

## HPI frameworks

**OLDCARTS**: Onset, Location, Duration, Character, Aggravating/Alleviating, Radiation, Timing, Severity
**OPQRST**: Onset, Provocation/Palliation, Quality, Region/Radiation, Severity, Timing

## ROS systems (14 systems for comprehensive)
Constitutional, Eyes, ENT, Cardiovascular, Respiratory, GI, GU, MSK, Skin, Neuro, Psych, Endocrine, Heme/Lymph, Allergic/Immuno

## Physical Exam systems
Constitutional, Eyes, ENT, Neck, Respiratory, CV, Chest/Breasts, GI/Abdomen, GU, MSK, Skin, Neuro, Psych, Lymphatic
