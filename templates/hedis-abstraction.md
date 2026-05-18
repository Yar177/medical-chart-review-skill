# HEDIS Abstraction Worksheet

Use this template when abstracting medical-record evidence for HEDIS measure closure (hybrid sampling, supplemental data submission, or chart-review QA). Every captured numerator hit needs auditable provenance.

> **Disclaimer:** This worksheet is a working template, not an NCQA-approved abstraction tool. Validate against your plan's NCQA-filed Data Source Description (DSD) and current HEDIS Volume 2 + Volume 5 requirements before using for production reporting.

---

## Member header

| Field | Value |
|---|---|
| Member ID | |
| DOB / Age at end of MY | |
| Sex (administrative) | |
| Race / Ethnicity (REL) | |
| Continuous enrollment verified | Yes / No / N/A |
| Measurement year | |
| Reporting product line | Commercial / Medicaid / Medicare / Marketplace |
| Plan name | |

---

## Abstraction metadata

| Field | Value |
|---|---|
| Abstractor name / ID | |
| Date of abstraction | |
| Over-read by (if applicable) | |
| Over-read date | |
| Source system(s) reviewed | EHR (name), HIE, fax queue, scanned docs, etc. |
| Sampling type | Hybrid sample / Standard supplemental / Non-standard supplemental / QA |

---

## Measure-by-measure abstraction

Repeat this block per measure being abstracted. Use the per-measure cards in [`../references/hedis/`](../references/hedis/) as the field guide.

### Measure: ______ (e.g., CBP, GSD, BCS-E)

| Field | Value |
|---|---|
| Denominator confirmed | Yes / No - explain |
| Standard exclusions reviewed (hospice, palliative, advanced illness 66+) | Yes / No - found / not found |
| Measure-specific exclusions reviewed | Yes / No - found / not found |
| Numerator compliant | Yes / No |
| Compliance window / look-back used | e.g., MY 2025 + 27-month look-back |
| Source document type | Office note / Discharge summary / Lab report / Imaging report / Immunization record / Other |
| Source document date | |
| Signing / attesting provider | |
| Provider type acceptable to spec | Yes / No |
| Evidence snippet (verbatim, ≤500 chars) | "..." |
| Coded value extracted (LOINC / SNOMED / CPT / CVX / RxNorm) | code + display |
| Measurement result (if applicable) | value + unit |
| Confidence | High / Medium / Low - explain |
| Notes / discrepancies | |

---

## Exclusion documentation block (when excluding member)

| Field | Value |
|---|---|
| Exclusion type | Hospice / Advanced illness / Frailty / Pregnancy / ESRD / Bilateral mastectomy / Total colectomy / Total hysterectomy / Other (specify) |
| Date of qualifying exclusion event | |
| Source document type | |
| Source document date | |
| Signing provider | |
| Evidence snippet | "..." |
| Coded value (ICD-10 / SNOMED / CPT) | |
| Lifetime vs MY-specific | |

---

## Refusal documentation block (when applicable)

| Field | Value |
|---|---|
| Member-specific refusal documented | Yes / No |
| Refusal date | |
| What was refused (be specific) | |
| Source document and signing provider | |
| Evidence snippet | "..." |
| Counted toward measure | Yes / No - per current spec |

---

## NLP-assisted abstraction (when extraction was machine-suggested)

| Field | Value |
|---|---|
| Extraction model / pipeline name & version | |
| Extraction date | |
| Model-suggested numerator status | Compliant / Not compliant / Excluded |
| Model confidence score | |
| Human reviewer agrees with model | Yes / No |
| If No: human-corrected status + reason | |
| Source snippet that drove model decision | "..." |

---

## QA / over-read sign-off

| Field | Value |
|---|---|
| Over-read complete | Yes / No |
| Over-read decision | Confirms / Overturns abstractor |
| Discrepancy notes | |
| Final status submitted to reporting | |
| Submitter / date | |

---

## Audit trail requirements (checklist)

- [ ] Member ID and abstractor ID on every record
- [ ] Source document type + date captured
- [ ] Verbatim evidence snippet attached (not just a paraphrase)
- [ ] Coded value mapped to standard terminology where applicable
- [ ] Signing provider captured and verified as eligible per spec
- [ ] Compliance window aligns with measure spec
- [ ] Copy-forward evidence flagged (and excluded if outside window)
- [ ] Telehealth visit place-of-service verified against spec acceptance
- [ ] All exclusions cited with primary-source evidence
- [ ] Refusal documentation member-specific (not generic)
- [ ] NLP / machine-extracted decisions reviewed by a human before submission
- [ ] Record retained per audit retention policy (typically through next year's Volume 5 review)

---

## See also

- [`../references/hedis/README.md`](../references/hedis/README.md) — per-measure deep-dive cards
- [`../references/hedis-supplemental-data.md`](../references/hedis-supplemental-data.md) — provenance rules
- [`quality-gap.md`](quality-gap.md) — broader gap-analysis template
- NCQA HEDIS Volume 2 (Technical Specifications)
- NCQA HEDIS Volume 5 (HEDIS Compliance Audit)
