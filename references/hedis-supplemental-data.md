# HEDIS supplemental data and hybrid sampling — provenance rules

When chart-abstracted data feeds HEDIS reporting, **how the data is captured and where it came from matters as much as what it says**. NCQA's Medical Record Review Validation (MRRV) and supplemental data validation are unforgiving on provenance. This reference summarizes the rules at a level useful for chart reviewers and NLP pipelines.

> **Disclaimer:** This is a working summary of NCQA's publicly documented data source framework. Verify against the current **NCQA HEDIS Volume 2 (Technical Specifications)** and **Volume 5 (HEDIS Compliance Audit)** before using for production reporting.

## The three data sources NCQA recognizes

| Tier | Source | Examples | Validation rigor |
|---|---|---|---|
| 1 | **Administrative data** | Claims, encounters, lab data, pharmacy data with member identifier | Highest acceptance; sampled by auditor |
| 2 | **Standard supplemental data** | Data from systems regularly used in clinical or operational workflows (EHR extracts, registries, state IIS, lab feeds, HIE) that have been **audited / approved** | Requires data source documentation, primary-source verification (PSV) sampling |
| 3 | **Non-standard supplemental data** | Data abstracted from medical records by the plan or vendor specifically for HEDIS reporting; not part of normal workflow | **Highest scrutiny** - all-member PSV sampling, strict abstraction tool requirements |

Hybrid sampling (medical record review for hybrid measures) is a separate framework that overlays Tier 3.

## Standard supplemental data requirements

To qualify as standard supplemental, the data source must typically:

- Be used in **routine clinical or operational workflow** (not created solely for HEDIS)
- Be **member-specific** (no aggregate or population-level data)
- Have a **documented data source description (DSD)** filed with the auditor
- Pass **primary-source verification** on an auditor-selected sample
- Use **standard codes** (CPT, ICD-10, LOINC, SNOMED, RxNorm, CVX, NDC) - not free-text only

Common standard supplemental sources:
- EHR data extracts (structured fields)
- State Immunization Information Systems (IIS)
- Lab vendor data feeds
- Pharmacy benefit data
- HIE / regional data exchange feeds
- Registry data (e.g., diabetes registry, cancer registry)

## Non-standard supplemental data requirements

When data is abstracted from medical records specifically for HEDIS:

- Must follow **NCQA-approved abstraction protocol**
- **Abstraction tool** must capture: member ID, abstractor ID, date of abstraction, source document, evidence text/snippet, encounter date
- Every record subject to **primary-source verification** during audit
- **Inter-rater reliability (IRR)** documentation typically required
- **Over-read** by a second abstractor for a sample
- Cannot be the **only** evidence used to determine compliance for all members - usually combined with admin data

## Hybrid sampling mechanics (overview)

For hybrid measures, plans report admin data PLUS medical record review on a sample:

- NCQA-defined sample size (commonly 411 members per measure with options for oversample)
- Random sample drawn from denominator
- Records reviewed against measure-specific abstraction criteria
- Substitutions allowed only for valid exclusion reasons (member not found, ineligible, etc.) up to a cap
- All numerator hits from medical record review must pass MRRV

## What counts as "primary source"

- The original source document in the medical record (e.g., the lab report, the imaging report, the signed note)
- A direct EHR screenshot or PDF showing the data element in context
- Auditor must be able to trace the abstracted data point back to a dated, identifiable source

What does **NOT** count as primary source:
- A summary or extract that does not show the original
- A spreadsheet of "captured measures" without source link
- A note that references a prior visit without copy of that visit's documentation
- Patient-reported data without clinician documentation (varies by measure)

## NLP pipeline implications

For chart-review NLP that feeds HEDIS:

- **Capture and store the source snippet** (paragraph, section, line numbers) with every extracted measure hit
- **Record the source document type, date, and signing provider** alongside the extracted value
- **Distinguish "current visit" vs "copy-forward"** evidence - many measures require the evidence to be from the relevant time window, not pulled forward from a prior note
- **Flag low-confidence extractions** for human review before they enter supplemental data pipelines
- **Standardize to coded value sets** (LOINC for labs, CVX for vaccines, RxNorm for meds, SNOMED for clinical concepts) - free-text-only extractions are weakest evidence
- **Audit log every transformation** - what the source said, what was extracted, who/what extracted it, what code it mapped to
- **Plan for MRRV**: every extracted positive must be re-findable in the source on request

## Refusal documentation

Patient refusal generally does NOT close a measure but may be tracked separately:

- Refusal must be member-specific and dated
- Generic "patient declines screening" without context typically does not qualify even for tracking
- Some measures allow specific exclusion language (e.g., documented mammogram refusal) - rare and measure-specific - verify

## Common compliance failures during audit

- Supplemental data submitted without DSD on file
- Abstraction tool missing required fields (no source citation, no abstractor ID)
- Free-text-only "compliant" flag with no underlying coded data
- Copy-forward documentation from outside MY counted as current
- Patient-reported data not attested by a clinician
- Telehealth visits captured without place-of-service alignment to measure spec

## See also

- [`hedis/README.md`](hedis/README.md) — per-measure cards
- [`nlp/`](nlp/) — NLP-team guidance for HEDIS extractors (date of service, negation/assertion, extraction patterns, evaluation)
- [`../templates/hedis-abstraction.md`](../templates/hedis-abstraction.md) — abstraction worksheet template
- NCQA HEDIS Volume 2 (Technical Specifications)
- NCQA HEDIS Volume 5 (HEDIS Compliance Audit)
- NCQA Data Aggregator Validation program documentation
