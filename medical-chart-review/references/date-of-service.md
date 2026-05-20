# Date of service (DoS) - clinical taxonomy for chart review

> **Why this file exists.** A chart abstractor never treats every date on the page as equivalent. The right DoS depends on the *kind* of date, *where* it appears in the note, *what tense* surrounds it, and *which note type* it lives in. This file is the authoritative clinical reference. NLP teams operationalize it via [`../../hedis-nlp/references/nlp/date-of-service.md`](../../hedis-nlp/references/nlp/date-of-service.md) and [`../../hcc-nlp/references/date-of-service.md`](../../hcc-nlp/references/date-of-service.md); both defer here for the clinical concepts.

---

## 1. Date kinds in a clinical chart

There are roughly 8 to 12 distinct date kinds in any clinical document. Only 2 to 3 are valid DoS for any given purpose.

| Date kind | Where it appears | Valid DoS for what? |
|---|---|---|
| **Service / Encounter / Visit date** (header / face sheet) | `Encounter Date:`, `Visit Date:`, `DOS:`, `Date of Service:` | Primary for visits, vaccines, screening encounters, AWVs |
| **Date of Procedure** (op-note header) | `Date of Procedure:`, `Procedure Date:` | Primary for COL-E, BCS-E procedure, CCS-E procedure |
| **Specimen collection date** (lab report) | `Collected:`, `Drawn:`, `Specimen Date:` | Primary for GSD HbA1c, lipid panels, KED, CBP cuff readings (per NCQA: collection, NOT result) |
| **Study / Exam date** (imaging) | `Exam Date:`, `Study Date:`, `Performed:` | Primary for mammogram (BCS-E), imaging numerators |
| **Result / Report date** | `Resulted:`, `Reported:`, `Verified:`, `Final:` | **Caution.** Often off by 1-7 days from true DoS. Shifts late-Dec / early-Jan tests across the measurement-period boundary |
| **Order date** | `Ordered:`, `Order Date:` | **Invalid.** Service may never have happened |
| **Scheduled date** | `Scheduled for:`, `Planned:` | **Invalid.** Future, not performed |
| **Note authored date** | `Documented by Dr. X on...` | **Invalid.** Often days after the encounter; legally distinct |
| **Note signed / attested date** | `Signed:`, `Electronically signed:` | **Invalid.** Up to weeks after the encounter |
| **Addendum date** | `Addendum 03/20:` | **Caution.** Refers to addendum content only, not the original encounter |
| **Pathology report date** | Path report timestamp | **Caution.** For COL-E the procedure date is correct; path date may be days later and refers to specimen handling |
| **Historical reference** | "last colonoscopy 2014", "h/o mammogram 2019" | **Caution.** Valid only if the measure look-back includes that year; precision usually year-only (see §5) |

**Single biggest blind spot:** pipelines and abstractors that treat every date string on the page as a candidate with equal status, then resolve attribution by character proximity. That is not how an abstractor reads a chart. Apply this hierarchy first; use proximity only within a structural boundary (sentence, table row, section).

## 2. Note type drives default DoS

Different note types have different *authoritative* DoS fields. The abstractor checks the header first; inline narrative dates are a fallback.

| Note type | Default DoS source | Confidence |
|---|---|---|
| Operative / procedure note | `Date of Procedure:` header | High |
| Pathology report | Specimen received / collected date (NOT report date for procedure-tied measures) | Medium |
| Lab report | Collection date | High |
| Imaging / radiology report | Exam / study date | High |
| Progress note / office visit | `Encounter Date:` header | High |
| Discharge summary | Discharge date (for TRC); admission date (for FUH index) | High |
| ED note | ED encounter date | High |
| Telephone / patient-portal communication | Often **not valid** for procedure measures | N/A |
| Scanned outside record | Inline dates only; header often missing or refers to scan date, not service | Low |

See [`note-types.md`](note-types.md) for the SOAP structure and full note-type catalog; this table is the DoS-attribution overlay on top of it.

## 3. Section semantics - where in the chart matters

The same date next to the same keyword has opposite meaning in `Plan` versus `Procedures Performed`. An MRRV reviewer will reject evidence without section-tagged provenance.

| Section | Status for evidence | Why (CCDS view) |
|---|---|---|
| Procedures / Procedures Performed | **Valid** | Active encounter, performed |
| HPI / History of Present Illness | **Valid** for narrative DoS | Current encounter content |
| Op Note Body | **Valid** | Use procedure-date header |
| Path Report Header | **Valid** | Specimen collection date |
| Lab Results (table) | **Valid** | Use collection date |
| Imaging Results | **Valid** | Use study date |
| Immunization Record | **Valid** | Date is administered date |
| Assessment | **Conditional** | Active diagnoses OK; "rule out" / "consider" NOT |
| Medications | **Conditional** | Active meds OK for med-based measures (MPM, AMR); not for procedures |
| Problem List | **Conditional** | List does not equal active management; needs MEAT and a date |
| PMH / Past Medical History | **Historical only** | Valid only if dated and within look-back; year-only precision typical |
| Plan | **Invalid** for procedure numerators | Future / proposed; not yet performed |
| Family History | **Invalid** | Not the patient |
| Social History | **Invalid** | Not a clinical service event |
| Allergies | **Invalid** | Not a procedure / service |
| Review of Systems (ROS) | **Invalid** for procedure DoS | Patient self-report |
| Patient Instructions / Discharge Instructions | **Invalid** | Not the service; future-tense |

See [`chart-structure.md`](chart-structure.md) for the universal note anatomy that defines these sections.

## 4. Tense and modality near the date

A CCDS scans the words around the date and the procedure keyword as the *primary* signal for whether the event happened. This is a separate axis from negation - "no diabetes" is negated, "scheduled colonoscopy 6/1/2024" is future-tense but not negated.

| Word or phrase near keyword | Class | DoS validity |
|---|---|---|
| `performed`, `completed`, `done`, `underwent`, `s/p`, `status post`, `hx of` (with date) | **PAST_DONE** | Valid |
| `scheduled`, `planned`, `will undergo`, `to be done`, `recommend`, `ordered`, `plan for` | **FUTURE_NOT_DONE** | Invalid - event has not occurred |
| `consider`, `discussed`, `offered`, `option`, `may benefit from` | **FUTURE_NOT_DONE** | Invalid - not done |
| `declined`, `refused`, `deferred`, `postponed`, `cancelled`, `no-show` | **FUTURE_NOT_DONE** | Invalid (also handled by negation; see below) |
| `reportedly`, `per patient`, `patient states`, `self-reported` | **PATIENT_REPORTED** | Lower precision; many measures require provider documentation |
| `outside`, `OSH` (outside hospital), `per outside records` | **PATIENT_REPORTED** / external | Source not primary; often excluded |

Three-class classification: **PAST_DONE**, **FUTURE_NOT_DONE**, **PATIENT_REPORTED**. Reject `FUTURE_NOT_DONE` outright; flag `PATIENT_REPORTED` for per-measure handling. Cross-reference [`coding-icd10-hcc.md`](coding-icd10-hcc.md) MEAT criteria (an event must have been Monitored / Evaluated / Assessed / Treated to count) - tense and MEAT overlap but are not identical.

For negation (the "no" / "denies" axis), see the negation handling described in each NLP skill's `negation-and-assertion.md`.

## 5. Date precision matters

Read "colonoscopy in 2022" and "colonoscopy on 11/14/2022" differently:

- "in 2022" → precision = **year**, lower bound = 2022-01-01, upper bound = 2022-12-31
- "on 11/14/2022" → precision = **day**, lower = upper = 2022-11-14

For a look-back ending 12/31/2024, the day-precision date is defensibly in window; the year-precision date is *not* (auditors reject silent normalization to 12/31). At year-only precision the correct action is a query, not an auto-close.

Per-measure precision rules:

- **Procedure measures** (COL-E, BCS-E, CCS-E): typically require day precision for DoS validation.
- **Risk-adjustment / HCC**: day precision preferred; month-precision can be acceptable if the month falls within the calendar service year.
- **Historical references** in PMH ("last colonoscopy 2014"): year precision is the norm. Valid only when the measure look-back fully contains that calendar year.

## 6. Specimen-collection vs result for labs

Critical for GSD (HbA1c), CBP (BP), KED (eGFR / uACR), APM (lab monitoring), and any lab-based measure. **NCQA: the collection date is the DoS, not the result-reported date and not the note-signed date.**

The late-December year-boundary trap: a specimen collected 12/28/2024 with results posted 1/4/2025 belongs to **MY 2024** (collection date). Picking the result date silently moves the test out of the measurement year and converts a compliant member into a non-compliant one.

Lab-report parsing rule: prefer `Collected:` / `Drawn:` / `Specimen Date:` over `Reported:` / `Verified:` / `Final:` for any date attribution.

## 7. Procedure-date header beats inline narrative

For COL-E, BCS-E, and CCS-E when the evidence comes from an op note or procedure note, the `Date of Procedure:` header is the gold standard. It beats any inline date in the body, the addendum date, and any path-report date that happens to sit on the same page.

If a pathology report sits on the same page as an op note, the **path-report dates must NOT be used as the procedure DoS** - they refer to specimen handling and are often 1-7 days later.

## 8. Copy-forward (cloned documentation)

This is the most-cited finding in NCQA MRRV audits and equivalent in RADV for HCC.

Copy-forward problems for DoS:
- An identical A&P block dated 10/1 that originated in a 1/15 note does **not** establish 10/1 MEAT or 10/1 DoS.
- Even within the same measurement year, the date attribution belongs to the **original** encounter, not the encounter that copied the text.
- Across measurement years or HCC calendar years, copy-forward from a prior year does **not** establish current-year MEAT.

Abstractor-side detection signals:
- Identical multi-sentence blocks across two or more notes
- Date-stamped phrases inside text that do not match the current encounter date ("A1c on 3/15/24" appearing in a note from 9/15/24)
- Section headers referencing a prior date ("From visit 6/2/24:")
- Imported outside-record markers ("Per outside records:", "From St. Elsewhere ED note dated 5/1/24:")

NLP teams implement the detection algorithm (multi-line block hashing across notes for the same member). See the NLP skills' DoS files for the operational spec.

## 9. Relative date expressions

Real chart text often has no inline date at all:

- `today`, `this morning`, `today's visit`
- `yesterday`, `2 days ago`, `last week`, `2 weeks ago`
- `earlier this year`
- `last colonoscopy 10 years ago`

These resolve against the document's *encounter date* (DocTime anchor) - not the signing date when those differ. For abstractor review: if no encounter date exists in the header, the signing date is a fallback with a confidence downgrade. Without DocTime anchoring, every "colonoscopy performed today" without an inline date is lost.

## 10. Administrative and header gates

Before counting any DoS-attributed evidence, an abstractor verifies:

1. **Member eligibility on the DoS** - was the member enrolled on that date for the relevant line of business?
2. **Coverage period** - does the DoS fall within the measurement year (HEDIS) or calendar year (HCC) for that LOB?
3. **Credentialed signer** - is the note signed by an acceptable provider type (MD / DO / NP / PA, with measure-specific exceptions)? Some measures require an attending attestation when a resident is the primary author.

These are often enforced downstream in HEDIS aggregation or HCC submission, not at the chart-review or NLP layer. Confirm before relying on it. If they are *not* enforced downstream, evidence rows that will never survive an audit are being shipped, and the abstraction work is wasted.

See [`administrative-insurance.md`](administrative-insurance.md) for face-sheet, eligibility, and coverage-period verification.

## 11. Common DoS failure modes (cross-walk)

| Failure mode | Cause | Mitigation |
|---|---|---|
| Counting a result-posting date instead of specimen collection | §6 not enforced | Parse `Collected:` explicitly; prefer over result/verified dates |
| Year-only date silently normalized to 12/31 | §5 not enforced | Track precision; query when year-only and look-back boundary is near |
| Future-scheduled procedure counted as completed | §4 tense not enforced | Reject `FUTURE_NOT_DONE`; require `PAST_DONE` tense |
| Patient-reported screening counted without provider documentation | §4 modality not enforced | Flag `PATIENT_REPORTED`; require source documentation |
| Copy-forward block credits the wrong encounter | §8 not detected | Detect cloned text; attribute to original encounter or downgrade |
| Section context ignored; Plan/PMH/FamHx evidence treated as valid | §3 not enforced | Tag every evidence row with source section; reject invalid sections per measure |
| Wrong signer (resident only, no attending attestation) | §10 not enforced | Verify credentialed signer; require attending block when resident-authored |
| Note-authored / note-signed date used as DoS | §2 / §1 ignored | Header DoS field beats note metadata; never default to signing date |

## See also

- [`note-types.md`](note-types.md) - SOAP, H&P, and note-type catalog
- [`chart-structure.md`](chart-structure.md) - universal note anatomy that defines the sections in §3
- [`chart-types.md`](chart-types.md) - care setting and payer program; DoS rules vary by setting (inpatient hedging allowed, outpatient not)
- [`coding-icd10-hcc.md`](coding-icd10-hcc.md) - MEAT criteria; tense and MEAT overlap
- [`administrative-insurance.md`](administrative-insurance.md) - eligibility and coverage-period gates
- [`provider-queries.md`](provider-queries.md) - non-leading queries when DoS is ambiguous
- Sibling [`../../hedis-nlp/references/nlp/date-of-service.md`](../../hedis-nlp/references/nlp/date-of-service.md) - strategy cascade, `dos_policy` schema, provenance columns, copy-forward detection algorithm, per-measure DoS grid
- Sibling [`../../hcc-nlp/references/date-of-service.md`](../../hcc-nlp/references/date-of-service.md) - HCC contract, calendar-year reset, face-to-face requirement, AWV trap
