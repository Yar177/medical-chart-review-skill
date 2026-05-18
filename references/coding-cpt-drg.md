# CPT, E&M, and DRG

## CPT basics

- 5-digit codes for procedures and services
- Categories: I (procedures), II (performance measures), III (emerging tech)
- **Modifiers** change meaning (e.g., `-25` significant separate E&M, `-59` distinct procedure, `-LT/-RT`, `-50` bilateral)
- HCPCS Level II for drugs, DME, supplies (e.g., `J3490`)

## E&M (Evaluation & Management) leveling — 2021+ rules

Office/outpatient E&M (99202–99215) leveled by either:

1. **Medical Decision Making (MDM)** — three elements:
   - Number/complexity of problems addressed
   - Amount/complexity of data reviewed
   - Risk of complications/morbidity/mortality
   
   Level = met or exceeded by 2 of 3 elements.

2. **Total time** on date of encounter (face-to-face + non-face-to-face by physician/QHP)

| Code | MDM | Time (established pt) |
|---|---|---|
| 99212 | Straightforward | 10–19 min |
| 99213 | Low | 20–29 min |
| 99214 | Moderate | 30–39 min |
| 99215 | High | 40–54 min |

Inpatient (99221–99239) and ED (99281–99285) have their own structures.

## DRG (MS-DRG for Medicare inpatient)

- Each inpatient stay → one DRG based on:
  - Principal diagnosis
  - Secondary diagnoses (CCs/MCCs affect severity)
  - Procedures performed (ICD-10-PCS)
  - Discharge disposition
- **CC** = Complication/Comorbidity; **MCC** = Major CC — they bump DRG to higher-weighted version
- DRG validation = confirming the coded principal dx is the condition that "after study" occasioned admission

## CDI documentation queries — when needed

Query the provider (compliantly) when documentation is:
- **Conflicting** (two different diagnoses for same condition)
- **Ambiguous** (e.g., "possible pneumonia" in inpatient)
- **Incomplete** (e.g., "CHF" without acuity/type)
- **Imprecise** (e.g., "anemia" without type or cause)
- **Clinically validated but not documented** (e.g., sepsis criteria met but not stated)

See `provider-queries.md` for compliant query templates.

## Audit red flags

- E&M leveling not supported by MDM or time documentation
- Modifier `-25` overuse (separate E&M with procedure)
- Cloned notes supporting high-level E&M
- Procedure coded without supporting op/procedure note
- Time-based codes without documented time
- DRG with single CC/MCC that lacks clinical validation
