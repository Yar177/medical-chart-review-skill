# LOINC and UCUM

> **Why this file exists:** LOINC is the universal code for **lab and clinical observations** (every lab result, vital sign, survey question, document type). UCUM is the **units of measure** standard paired with it. Together they are what makes a "Hemoglobin A1c = 7.2 %" value comparable across vendors.

## 1. LOINC - what it is

- **LOINC** = **Logical Observation Identifiers Names and Codes**.
- Maintained by the **Regenstrief Institute**.
- Used in EHRs, lab interfaces, HL7 v2 / v3 / FHIR messages, eCQMs, and HEDIS for **identifying observations**: lab tests, lab panels, clinical observations (vitals), survey instruments, document types, radiology study types, document section types.
- **~100,000+ active terms** (varies by release).
- **Free** with registration; redistribution requires preserving the license notice. See [`sources-and-licensing.md`](sources-and-licensing.md).

## 2. Structure - the 6-axis model

A LOINC term is fully specified by six **axes**:

| Axis | Description | Example |
|---|---|---|
| 1. **Component** | What is being measured / observed | "Hemoglobin A1c/Hemoglobin.total" |
| 2. **Property** | Kind of quantity | "MFr" (mass fraction), "SCnc" (substance concentration), "ACnc" (arbitrary concentration), "PrThr" (presence/threshold) |
| 3. **Time aspect** | Time interval over which the observation was made | "Pt" (point in time), "24H" (24-hour collection) |
| 4. **System (specimen)** | Where the observation was obtained | "Bld" (blood), "Ser/Plas" (serum or plasma), "Ur" (urine), "^Patient" (the patient themselves) |
| 5. **Scale type** | The scale of the measurement | "Qn" (quantitative), "Ord" (ordinal), "Nom" (nominal), "Nar" (narrative), "Doc" (document) |
| 6. **Method** | How the test was performed (often omitted) | "IFCC", "HPLC", "Manual count.microscopy" |

Each axis has its own vocabulary, and the 6-tuple uniquely identifies a LOINC term.

### Worked examples

| LOINC | Long Common Name |
|---|---|
| `4548-4` | Hemoglobin A1c/Hemoglobin.total in Blood |
| `17856-6` | Hemoglobin A1c/Hemoglobin.total in Blood by HPLC |
| `2160-0` | Creatinine [Mass/volume] in Serum or Plasma |
| `48642-3` | Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum, Plasma or Blood by Creatinine-based formula (MDRD) |
| `8302-2` | Body height |
| `29463-7` | Body weight |
| `8480-6` | Systolic blood pressure |
| `8462-4` | Diastolic blood pressure |
| `9279-1` | Respiratory rate |
| `8867-4` | Heart rate |
| `8310-5` | Body temperature |
| `LP12345-6` | A LOINC Part code (not a full term; used as a building block) |

### LOINC code format

- **Numeric + check digit**, separated by a hyphen (`4548-4`).
- The check digit is computed via a defined algorithm.
- **LOINC Parts** (`LP` prefix) are sub-components used to build LOINC terms; they are not themselves observation codes.

## 3. Common analytic uses

- **Lab result identification**: every lab result from a HL7 v2 ORU message or a FHIR Observation resource will carry a LOINC code in the observation identifier slot.
- **HEDIS lab numerator detection**: HbA1c < 8.0%, eGFR for kidney disease, BNP for heart failure, LDL for cardiovascular - all keyed by LOINC.
- **Vital sign normalization**: SBP / DBP / HR / RR / temp / weight / height all have stable LOINC codes.
- **Document classification**: LOINC document type codes (`Doc` scale) label what kind of document a clinical note is (`34117-2` History and physical, `28570-0` Procedure note, etc.).
- **Survey instrument identification**: PHQ-9, PROMIS, SF-36, etc. each have LOINC codes for the instrument and for each question.

## 4. LOINC vs CPT for labs

- **CPT** identifies the **billable lab procedure** ("HbA1c").
- **LOINC** identifies the **observation result** ("HbA1c value in blood").
- These describe related-but-distinct things. **One CPT can correspond to multiple LOINCs** (e.g., HbA1c by different methodologies) and **one LOINC can be reached by multiple CPTs**.
- A **LOINC ↔ CPT crosswalk** exists (published by Regenstrief and via the AMA) but is **not 1:1**; the mapping is informational, not authoritative for billing.
- See [`crosswalks.md`](crosswalks.md).

## 5. Release cadence

- **Biannual major releases**: typically June and December.
- Mid-cycle updates rare.
- Term IDs are stable across releases for active terms.

## 6. LOINC reference sets

- **LOINC Document Ontology** for clinical document classification.
- **LOINC Top 2000 Lab Observations** - a curated list of the most-used lab terms, useful for prioritizing implementation effort.
- **LOINC SNOMED Ontology** - mapping LOINC to SNOMED Observable concepts for systems that need both.
- **LOINC FHIR resources** - LOINC publishes FHIR-conformant CodeSystem and ValueSet resources.

## 7. UCUM - units of measure

- **UCUM** = **Unified Code for Units of Measure**.
- Maintained by **Regenstrief** (same organization as LOINC).
- Standard for **case-sensitive** unit codes used alongside numeric values.
- Used by **FHIR** as the recommended unit system; required by many HL7 v2 lab interfaces.
- **Free**, public.

### UCUM examples

| UCUM | Meaning |
|---|---|
| `mg/dL` | Milligrams per deciliter |
| `mmol/L` | Millimoles per liter |
| `kg` | Kilogram |
| `[lb_av]` | Pound (avoirdupois) - bracketed for non-SI |
| `Cel` | Degrees Celsius |
| `[degF]` | Degrees Fahrenheit |
| `%` | Percent |
| `mm[Hg]` | Millimeters of mercury |
| `{beats}/min` | Beats per minute (curly braces = annotation, not part of measurement) |
| `10*3/uL` | Thousand per microliter (e.g., WBC count) |
| `mL/min/{1.73_m2}` | Milliliters per minute per 1.73 square meters (eGFR) |

### Conventions

- **Case-sensitive.** `mg` (milligram) ≠ `Mg` (megagram).
- **Multiplication = `.`**, **Division = `/`**, **Exponent = `*`** (or `^` in some variants).
- **Curly braces `{ }`** denote **annotations** that have no semantic meaning - they are descriptive labels for human readers, not part of the unit definition. `{beats}/min` and `/min` are the same unit; only the annotation differs.
- **Square brackets `[ ]`** denote **arbitrary / non-SI units** (US customary, Imperial, etc.) - `[lb_av]` for avoirdupois pound, `[in_i]` for international inch.

## 8. Reference ranges and result units

A lab result is fully specified by:

- **What was measured** (LOINC code)
- **Result value** (numeric, ordinal, narrative, or coded)
- **Units** (UCUM code) - for quantitative results
- **Reference range** (low / high / interpretation) - varies by lab / vendor / patient demographics

Two labs reporting the "same" result with different UCUM units (`mg/dL` vs `mmol/L` for glucose) require unit conversion before comparison. Many warehouses store the raw value and unit and defer conversion to analytic-time logic.

### Common conversion factors

- Glucose: `mg/dL × 0.0555 = mmol/L`
- Creatinine: `mg/dL × 88.4 = umol/L`
- Cholesterol: `mg/dL × 0.0259 = mmol/L`
- HbA1c: `% × 10.929 - 23.5 = mmol/mol` (the IFCC unit)

A pipeline that joins multi-vendor lab data without unit normalization at the boundary will produce nonsensical analytics.

## 9. Authoritative sources

- **LOINC**: <https://loinc.org/> - free with registration. LOINC tables, RELMA mapping tool, multilingual variants.
- **UCUM**: <https://ucum.org/> - free.
- **LOINC FHIR resources**: <https://loinc.org/fhir/>
- **NLM Value Set Authority Center (VSAC)** value sets often reference LOINC: <https://vsac.nlm.nih.gov/>
- See [`sources-and-licensing.md`](sources-and-licensing.md).

## 10. Common pitfalls

- **Lab vendor codes used in place of LOINC.** Many vendors emit proprietary codes in HL7 v2 messages alongside LOINC; if the LOINC slot is empty or `OBR-4` carries a vendor code, downstream normalization is impossible without a vendor-specific crosswalk.
- **Method-specific LOINC ignored.** `4548-4` (HbA1c, method unspecified) and `17856-6` (HbA1c by HPLC) are distinct terms; clinical equivalence is often safe but documenting the choice matters.
- **Unit normalization deferred forever.** Storing `mg/dL` and `mmol/L` glucose values in the same column without converting produces noise.
- **Curly-brace annotations treated as part of the unit.** `{beats}/min` and `/min` differ only in annotation; treating them as different units mis-categorizes data.
- **Case-folding UCUM.** `mg` and `Mg` differ by 9 orders of magnitude.
- **LOINC Part codes (`LP` prefix) used as observation codes.** Parts are building blocks; full LOINC observation codes are numeric with check digit.
- **Stale LOINC version.** Biannual releases occasionally add terms or revise descriptions; using a 5-year-old LOINC table misses new content.
- **Mapping LOINC to CPT 1:1 for billing reconciliation.** The mapping is informational; multiple LOINCs can correspond to one CPT and vice versa.
