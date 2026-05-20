# Date of Service (DoS) for HEDIS NLP extraction

> **Why this file exists:** Date of service is one of the two biggest accuracy killers in HEDIS NLP (the other is negation - see [`negation-and-assertion.md`](negation-and-assertion.md)). The wrong date can flip a compliant member to non-compliant, attribute evidence to the wrong measurement year, or trigger MRRV failure even when the clinical content is correct.

This file gives the shared DoS framework. Each per-measure card in [`../hedis/`](../hedis/) has a measure-specific DoS table; the grid below shows all 24 measures at a glance.

> **Clinical taxonomy lives in [`../../../medical-chart-review/references/date-of-service.md`](../../../medical-chart-review/references/date-of-service.md)** - 12 date kinds, note-type → DoS mapping, section semantics, tense / modality lexicon, precision rules, and the abstractor view of copy-forward. **This file owns the NLP pipeline design that operationalizes it**: strategy cascade, `dos_policy` schema, provenance columns, detection algorithms, the 24-measure grid, and worked test cases. Do not duplicate clinical content here; cross-link instead.

---

## 1. The DoS problem in chart text

A single chart can contain **many candidate dates** for one clinical fact:

- Note signing date
- Encounter date
- Service date / date of service (CMS billing concept)
- Lab specimen collection date
- Lab result-posting date
- Imaging exam date vs imaging report date
- Order date
- Result-acknowledgment date
- Referenced past date inside narrative ("last A1c was in March")
- Future-scheduled date ("colonoscopy scheduled for next month")
- Copy-forward date (the original date of pulled-forward text)
- Document scan / import date for outside records

HEDIS specs almost always require a **specific one of these**. Picking the wrong one is a silent miss.

## 2. Date-type taxonomy

| Type | Source | Notes |
|---|---|---|
| **Encounter date** | Visit metadata | Date of the in-person, telehealth, or e-visit encounter |
| **Service date** | Claim or note | The clinical service date (often = encounter date, not always) |
| **Specimen collection date** | Lab result | Use for lab-based measures (GSD, KED, CCS-E Pap, COL-E FIT) |
| **Result date** | Lab result | Posting / final-report date; usually NOT the right date |
| **Procedure date** | Procedure note | Use for procedure-based measures (COL-E colonoscopy, BCS-E mammogram) |
| **Report date** | Imaging report | Date radiologist signed; usually within a day or two of procedure date |
| **Order date** | CPOE | Earliest signal; usually NOT evidence on its own |
| **Vaccination administration date** | Immunization record / CVX | Use for AIS-E and pediatric immunizations |
| **Dispense date** | Pharmacy fill | Use for SUPD / SPC / adherence measures |
| **Discharge date** | Inpatient encounter | Anchor for FUH, MRP, TRC |
| **Document date** | Note metadata | Use only when no clinical date is available |

## 3. Anchor events vs MY-only windows

Two broad measure shapes:

**MY-only** - any qualifying evidence anywhere in the measurement year.
Examples: GSD, BPD, CBP, BCS-E (rolling 2-yr), CCS-E (rolling 3-5 yr by modality), EED, KED, AIS-E.

**Anchor + window** - an index event triggers a counted look-back / look-forward.
Examples: FUH (discharge from MH inpatient → 7-day & 30-day follow-up), MRP (discharge → 30-day med rec), TRC (4 sub-indicators each with their own window), PPC (delivery date anchors postpartum), DBM (positive screening anchors follow-up).

For anchor measures, the extractor must:

1. Identify the **anchor event** with high precision (right diagnosis, right setting, right discharge date)
2. Resolve **all relative dates in the window** to absolute dates
3. Score evidence dates against the window edges, inclusive/exclusive per spec

## 4. Relative and vague date expressions

Real chart text:

- "last A1c in March" - which March?
- "two weeks ago"
- "earlier this year"
- "during her recent admission"
- "next month"
- "follow up in 3 months"
- "Q3 mo" (every 3 months)
- "WNL last visit"

Resolution rules:

1. **Note signing date is the reference point** for "ago" / "next" / "earlier this year" expressions
2. **Year defaults to most recent past year** for bare-month references ("in March" with no year → March of current or prior year, whichever is most recent past)
3. **"Recent admission"** → look for an encounter linked to this member in the prior 60 days unless context narrows it
4. **Future-tense expressions** ("scheduled for", "will get") are NOT evidence regardless of date
5. **Vague expressions that cannot be resolved to a specific date** must be flagged as low-confidence and not auto-scored

OSS libraries that help: **HeidelTime**, **SUTime**, spaCy's date NER (weak on clinical), **medspaCy** target rules combined with custom anchor logic.

## 5. Copy-forward detection

Copy-forward (pulling text from a prior note into a current note) is the single biggest source of date errors in HEDIS NLP.

Signals that text is copy-forward:

- Identical multi-sentence blocks across two notes from same or different authors
- Date-stamped phrases that don't match the current encounter date ("A1c on 3/15/24" appearing in a note from 9/15/24)
- Section headers that reference a prior date ("From visit 6/2/24:")
- Imported outside-record markers ("Per outside records:", "From St. Elsewhere ED note dated 5/1/24:")

Rules:

- **Date inside copy-forward text takes precedence** over note signing date for that evidence
- Copy-forward of a result from a prior MY does NOT count as current-MY evidence even if the current note signing date is in MY
- Provenance tracking: store the original document the text came from when detectable

## 6. Outside records and scanned PDFs

- Outside-records sections may carry their **own embedded dates** that must be extracted (not the import date)
- Scanned PDFs need OCR; dates from OCR are lower confidence (digit confusion: 5/8/9/0)
- Faxed reports often have the fax timestamp at the top - this is NOT the service date
- Document type matters: lab report vs imaging report vs progress note - drives which date field to extract

## 7. Multi-date documents

A discharge summary can reference dozens of dates. The extractor must:

- Section-aware: dates in "Hospital course" describe events during admission; dates in "Discharge medications" can be future fill instructions
- For each candidate evidence span, identify the **closest preceding date** within the same logical section
- Where ambiguous, prefer the date that puts the evidence in the most clinically plausible window

## 8. Decision pseudocode

```
for each evidence_candidate in chart:
    candidate_dates = collect_dates_in_scope(evidence_candidate)
    primary_date = select_by_measure_rule(
        candidate_dates,
        measure.date_field_priority    # e.g. ["specimen_collection", "service_date", "encounter_date"]
    )
    if is_copy_forward(evidence_candidate):
        primary_date = embedded_date_in_copy_forward_text
    if primary_date is None or confidence < threshold:
        flag_for_review()
        continue
    if not within_measure_window(primary_date, measure, member.MY):
        drop()
        continue
    emit(evidence_candidate, primary_date, source_snippet, source_doc)
```

## 9. Measure × DoS-rule grid (all 24)

| Measure | Anchor / window shape | Date field that counts | Date field that often misleads |
|---|---|---|---|
| **GSD** | MY-only | Lab specimen collection date; CGM analysis window end | Result-posting date, copy-forward of prior-year A1c |
| **BPD** | MY-only | Encounter date of the visit where BP was taken | Note signing date when copy-forward includes old BP |
| **EED** | MY-only (with 2-yr look-back for negative result) | Eye exam date by eye care professional | PCP note mentioning prior eye exam without date |
| **KED** | MY-only | Lab specimen collection date for both eGFR and uACR | One component in MY, the other prior year |
| **SUPD** | MY-only | Pharmacy dispense date (PDC calc) | Prescription written date without fill |
| **CBP** | MY-only | Encounter date of most recent qualifying BP | BP recorded in a problem-list comment without encounter context |
| **SPC** | MY-only | Pharmacy dispense date (PDC calc) | Statin on med list without active fill in MY |
| **BCS-E** | Rolling 2-year look-back ending in MY | Mammogram procedure date | Order date, scheduled-future date |
| **CCS-E** | Rolling 3-yr (Pap) or 5-yr (Pap+HPV co-test or hrHPV) | Specimen collection date | "Per patient: had Pap last year" without date |
| **COL-E** | Modality-specific look-back (FIT 1y, FIT-DNA 3y, sigmoidoscopy 5y, colonoscopy 10y) | Procedure or specimen date | Order date for screening, "patient declined" |
| **DBM** | Anchor: abnormal mammogram → defined follow-up window | Date of follow-up imaging/biopsy/consult | Imaging report date vs procedure date |
| **FUH** | Anchor: MH inpatient discharge → 7-day and 30-day windows | Outpatient MH visit encounter date | Phone call dates that don't meet visit criteria |
| **PHQ** | MY-only (screening); follow-up if positive | Instrument administration date in note | Documented score without date |
| **MRP** | Anchor: discharge → 30 days | Med rec note date | Discharge summary signing date (vs actual rec date) |
| **TRC** | Anchor: inpatient discharge → multiple sub-indicator windows | Each sub-indicator's specific dated event | Mixing notification date with reconciliation date |
| **PPC** | Anchor: delivery date → prenatal look-back, postpartum 7-84 day window | Prenatal visit dates; postpartum visit date | Delivery date as inferred from infant DOB |
| **W30** | Anchor: child's 15-month / 30-month birthday → required visit count by age window | Well-child visit encounter date | Sick visits coded as well visits |
| **WCV** | MY-only, ages 3-21 | Well-care visit encounter date | Sports physical w/o full well-care components |
| **WCC** | MY-only, ages 3-17 | Encounter date for each sub-component (BMI, nutrition, activity) | BMI calc from height/weight without explicit BMI documentation |
| **ACP** | MY-only | Encounter date where ACP discussion or document signed | Reference to an old POLST without renewal |
| **AIS-E** | Look-back varies by vaccine (lifetime for some, 12-month for flu) | Vaccination administration date | Refusal date, ordered-but-not-given |
| **COA** | MY-only, 4 sub-indicators | Encounter date for each sub-component | Med review = full review, not "reviewed med list" boilerplate |
| **FRM** | HOS-anchored; chart angle uses MY-only fall risk discussion | Encounter date of fall risk assessment / discussion | Falls reported in HPI without intervention documented |
| **OSW** | MY-only (look-back to age 67 for DXA) | DXA date or pharmacy dispense date | Order for DXA without completion |

> Per-measure cards have the full table (anchor, window, date types that count, types that don't, disambiguation, look-back / look-forward). This grid is for quick triage.

## 10. Worked test cases

Each case shows raw text, the right answer, and the failure mode it guards against. Use these as initial regression fixtures; see [`test-fixtures/`](test-fixtures/) (Phase 4) for the structured versions.

**Case 1 - GSD copy-forward trap**
> Text: "Note dated 6/15/2025. Assessment: T2DM, A1c 7.2% on 4/10/2024, continue metformin."
> Right answer: Evidence date = 4/10/2024 (specimen date inside copy-forward), NOT 6/15/2025.
> Failure mode: Counting copy-forward result as current-MY evidence.

**Case 2 - GSD outside lab delayed posting**
> Text: Lab section shows "HbA1c 6.8, Specimen collected 12/28/2024, Result posted 1/4/2025". Member's MY = 2024.
> Right answer: Evidence date = 12/28/2024; counts for MY 2024.
> Failure mode: Using result-posting date excludes valid evidence.

**Case 3 - GSD CGM GMI**
> Text: "Dexcom report reviewed today (3/1/2025). GMI 7.1% based on data from 1/15/2025 - 2/12/2025."
> Right answer: Evidence date = 2/12/2025 (analysis window end).
> Failure mode: Using report-review date or upload date.

**Case 4 - BCS-E future-scheduled**
> Text: "Screening mammogram scheduled for 8/15/2025."
> Right answer: NOT evidence. Future intent.
> Failure mode: Counting scheduled procedures as completed.

**Case 5 - CCS-E vague patient report**
> Text: "Patient reports Pap smear at OB office last year, results normal."
> Right answer: NOT evidence on its own; needs documented result with date from primary source.
> Failure mode: Counting patient-reported screenings without provider documentation.

**Case 6 - COL-E modality-specific window**
> Text: "Colonoscopy 6/2017, normal." Member's MY = 2025.
> Right answer: Evidence. Colonoscopy 10-year look-back covers MY 2025 (eligible until 2027).
> Failure mode: Applying FIT 1-year window to colonoscopy.

**Case 7 - FUH discharge-anchored window**
> Text: Inpatient psych discharge 3/10/2025. Outpatient MH visit 3/16/2025.
> Right answer: 6-day gap, meets 7-day follow-up (FUH-7). Also meets FUH-30.
> Failure mode: Off-by-one (some specs are "within 7 days" inclusive of discharge day, others exclusive - verify spec).

**Case 8 - FUH calendar-day vs business-day**
> Text: Discharge Friday 3/14/2025. Outpatient MH visit Monday 3/24/2025 (10 days).
> Right answer: Does NOT meet 7-day. Calendar days, not business days.
> Failure mode: Treating weekends as excluded.

**Case 9 - PPC postpartum window**
> Text: Delivery 5/1/2025. Postpartum visit 5/3/2025 (in hospital).
> Right answer: In-hospital visit on postpartum day 2 typically does NOT meet the 7-84 day requirement - verify current spec.
> Failure mode: Counting any postpartum encounter regardless of timing.

**Case 10 - WCV sports physical**
> Text: "Sports clearance physical 8/20/2025. BP, vision, heart auscultation. Cleared for football."
> Right answer: Sports physical alone typically does NOT meet WCV requirements (no full age-appropriate well-care components documented).
> Failure mode: Treating any annual visit as a well-care visit.

**Case 11 - MRP discharge anchor mismatch**
> Text: Discharge 3/1/2025. Med rec note 4/5/2025 (35 days post-discharge).
> Right answer: Does NOT meet 30-day MRP window.
> Failure mode: Counting any post-discharge med rec regardless of timing.

**Case 12 - SUPD prescription vs dispense**
> Text: "Atorvastatin 40mg prescribed 5/1/2025." No pharmacy dispense in EHR.
> Right answer: Prescription alone does NOT meet PDC; need dispense data.
> Failure mode: Counting prescribed = filled.

**Case 13 - AIS-E vaccine refusal vs administration**
> Text: "Flu vaccine offered 10/15/2024, patient declined."
> Right answer: NOT a vaccination event. Refusal is tracked separately.
> Failure mode: Confusing offer/refusal documentation with administration.

**Case 14 - KED two-component date mismatch**
> Text: eGFR 12/10/2024 (in MY). uACR 1/5/2025 (next MY).
> Right answer: Only the eGFR counts for MY 2024; uACR not present in MY 2024. Member is NOT compliant for MY 2024 KED unless both components are present in MY.
> Failure mode: Counting partial KED as full numerator hit.

**Case 15 - BPD problem-list comment without encounter context**
> Text: Problem list entry "HTN - BP 138/82 last visit". No encounter date attached.
> Right answer: NOT directly scoreable - need the actual encounter where BP was recorded.
> Failure mode: Extracting BP values out of structured-context fields.

**Case 16 - DBM follow-up imaging report date trap**
> Text: Abnormal screening mammogram 3/1/2025 (BIRADS 0). Follow-up diagnostic mammogram performed 3/15/2025; report signed 3/17/2025.
> Right answer: Follow-up evidence date = 3/15/2025 (procedure date), not 3/17/2025 (report date).
> Failure mode: Using report-signing date for procedure-date measures.

## 11. Validation strategy for DoS extraction

- **Golden test set** per measure of 50-200 manually adjudicated date assignments, balanced across copy-forward, outside-record, telehealth, retro-entered scenarios.
- Metrics: exact-date accuracy, within-window classification accuracy (more forgiving), MY attribution accuracy.
- **Stratify** by note type (discharge summary, progress note, lab report, scanned PDF) - error rates vary wildly.
- **Audit log every date decision** so MRRV failures can be traced.

---

## 12. Why proximity-only attribution fails

The naive design picks the date with the smallest character distance from the keyword. A chart abstractor never does this. Three principles drive the best-in-class architectural shape (cTAKES temporal module, MedSpaCy section detection, Heideltime DocTime, Apixio / Optum HCC stacks discussed publicly all converge on it):

1. **Proximity is necessary but not sufficient.** Use proximity within a *structural boundary* (sentence, table row, section) - never raw character distance across the whole page.
2. **Structure beats distance.** A date 80 characters to the left in the same table row is far better evidence than a date 12 characters away across a section break.
3. **Provenance is part of the answer.** Every MATCH carries *how* it was dated. MRRV reviewers reject "smallest character distance" as a rationale; they accept "same row of the Procedures flowsheet on page 4."

### Date-keyword pattern catalog

A tight one-sided proximity window encodes exactly one of the six-plus ways clinicians write a date next to an event. Real EHR exports (Epic SmartText, flowsheets, Cerner PowerNotes, lab tables) use all of these:

| Pattern | Example | Caught by |
|---|---|---|
| **A.** Date after keyword, narrative | `colonoscopy on 03/15/2024` | S3 (same sentence) |
| **B.** Date before keyword, narrative | `On 03/15/2024, colonoscopy performed` | S3 (symmetric) |
| **C.** Tabular: Date \| Procedure \| Result | `03/15/2024    Colonoscopy    Negative` | S2 (same table row) |
| **D.** Section-header date | `PROGRESS NOTE 03/15/2024 ... Procedures: colonoscopy` | S5 (section header) |
| **E.** Lab-style row | `A1c    7.1    03/15/2024` | S2 (table row) |
| **F.** Parenthetical | `Colonoscopy (03/15/2024) - normal` | S1 (parenthetical) |
| **G.** Range | `Hospitalization 05/10-05/14/2024` | Date-extractor range handling (upstream) |
| **H.** Relative | `Colonoscopy 2 weeks ago` | S7 (DocTime-anchored) |
| **Header-driven** | `DATE OF PROCEDURE: 03/15/2024` (page header) | S0a-S0d (highest precision) |

A single one-sided 20-character window is structurally blind to B through E - dominant patterns in EHR exports. Symmetric structural cascade catches them all.

## 13. Strategy cascade (S0a-S7)

For each keyword hit, generate candidate `(date, strategy)` pairs. Pick the highest-precedence strategy that fires; within a strategy, tiebreak by token distance.

| Rank | Strategy | Fires when | Typical precision |
|---|---|---|---|
| 0a | **S0a_PROC_DATE_HEADER** | `Date of Procedure:` in op / procedure note for procedure measures | Very high |
| 0b | **S0b_LAB_COLLECTION_DATE** | `Collected:` / `Drawn:` / `Specimen Date:` field in lab report for lab measures | Very high |
| 0c | **S0c_IMG_STUDY_DATE** | `Study Date:` / `Exam Date:` / `Performed:` for imaging | Very high |
| 0d | **S0d_ENCOUNTER_HEADER_DATE** | `Encounter Date:` / `Visit Date:` / `DOS:` for visit-based numerators | High |
| 1 | **S1_PARENTHETICAL** | Date sits inside `()` or `[]` whose opening punct is within 3 chars from the keyword | Very high |
| 1 | **S2_SAME_TABLE_ROW** | Both spans on the same line AND the line is inside a detected table region | Very high |
| 2 | **S3_SAME_SENTENCE_ADJ** | Same sentence, within K tokens apart, no intervening clause boundary (`;` `.` `-`) | High |
| 3 | **S4_ADJACENT_TABLE_ROW** | Table region; date is on the immediately preceding or following row in the date column | Med-high |
| 4 | **S5_SECTION_HEADER_DATE** | No inline date; the enclosing section header carries a date (e.g., `Progress Note 03/15/2024`) | Medium |
| 5 | **S6_DOC_DATE** | None of the above; use note creation / signing date | Low - disqualifying for most procedure measures |
| 6 | **S7_DOCTIME_ANCHORED_RELATIVE** | `today` / `2 weeks ago` / `earlier this year` resolved against the document's encounter date | Medium |

**Notes**

- "Same sentence" requires upstream sentence segmentation that does not collapse table lines into one sentence. Use a clinical-aware splitter (medspaCy / sciSpacy) or a lightweight rule: split on `.\s+[A-Z]`, `\n{2,}`, line break + indent change.
- "Table region" detection: three or more consecutive lines with two or more runs of `\s{2,}` or `\t`. Compute once per page upstream.
- Direction is **symmetric** - a date can be before or after a keyword, bounded by structural context, not raw chars.
- Header strategies S0a-S0d are extracted once per page from the first ~500 chars and attached to every keyword hit in that document by default.

## 14. Per-measure `dos_policy` schema

Each measure has a config in `measures/.../<measure>.json` (or wherever the team's spec lives). Add a `dos_policy` block. This makes the cascade *spec-driven* and *auditable* without code changes.

```yaml
dos_policy:
  allowed_strategies: [S0a, S0b, S0c, S0d, S1, S2, S3, S4, S5]   # COLE excludes S6 and S7
  preferred_strategies: [S0a, S0d]                                # check header first for COLE
  invalid_sections: [Plan, Family History, Social History, Allergies, ROS, Patient Instructions]
  valid_sections:   [Procedures, HPI, Op Note Body, Path Report Header, Lab Results, Imaging Results, Immunization Record]
  invalid_note_types: [patient_message, phone_note, scanned_outside_unverified]
  invalid_date_kinds: [order_date, scheduled_date, signed_date, authored_date, addendum_date]
  preferred_date_kinds: [procedure_date, collection_date]
  invalid_tense:    [FUTURE_NOT_DONE]
  flag_tense:       [PATIENT_REPORTED]
  required_precision: day                                         # COLE / BCS-E / DBM
  doc_date_fallback_allowed: false                                # S6 rejected
  require_copy_forward_dedup: true
  require_credentialed_provider: true
  max_token_distance: 25                                          # used inside S3
  prefer_date_position: earlier                                   # for ranges / lab dates
```

**Per-measure diffs** (illustrative - confirm against current NCQA Volume 2):

- **COL-E** - as above. `preferred_strategies: [S0a, S0d]`, `preferred_date_kinds: [procedure_date]`, `required_precision: day`.
- **GSD / DBM (HbA1c)** - `preferred_strategies: [S0b, S2]`, `preferred_date_kinds: [collection_date]`, `required_precision: day`. The collection-vs-result trap (see [`../../../medical-chart-review/references/date-of-service.md`](../../../medical-chart-review/references/date-of-service.md) §6) is the dominant failure mode for this measure.
- **AIS-E (immunizations)** - `preferred_date_kinds: [administration_date]`. `invalid_date_kinds` includes `order_date` and `scheduled_date` (refusal / offer != administration).
- **FUH / MRP / TRC (anchor + window)** - cascade selects the *index* anchor date with S0d / S2; window evaluation is downstream of attribution.

Clinical justification for `invalid_sections` and the tense lexicon comes from [`../../../medical-chart-review/references/date-of-service.md`](../../../medical-chart-review/references/date-of-service.md) §3-4. Do not duplicate the word lists; reference and copy at code-generation time.

## 15. Tense and modality classifier

Distinct from negation (handled in [`negation-and-assertion.md`](negation-and-assertion.md)). Three-class output per keyword hit:

- **PAST_DONE** - event occurred. Required for procedure / event numerators.
- **FUTURE_NOT_DONE** - scheduled / planned / ordered / offered / declined / refused. **Reject outright.**
- **PATIENT_REPORTED** - patient-stated history without primary-source documentation. Flag; per-measure handling.

Implementation:

- Scan a 50-character window around the keyword for the lexicon entries in [`../../../medical-chart-review/references/date-of-service.md`](../../../medical-chart-review/references/date-of-service.md) §4.
- Run **before** date attribution in the per-measure step. Rejected hits never enter the cascade.
- Emit `MATCH_TENSE` provenance column (see §17).
- Negation handling runs in parallel; both gates must pass.

False-positive guards:

- `s/p` (status post) is **PAST_DONE**, not future. Special-case it.
- `history of` followed by a date is **PAST_DONE** with that date; without a date it's a low-confidence historical reference.
- `hold` (`hold on metformin`) is medication-management context, not future-tense for procedure DoS.

## 16. Copy-forward detection algorithm

§5 above describes signals. Production teams need a deterministic detection step. Lightweight first pass:

1. **Hash 3-line windows** across all notes for the same member. Use a normalized hash (strip whitespace, lowercase, drop dates and numbers) so date-stamp variation doesn't defeat the match.
2. A multi-line block appearing two or more times with identical normalized text across notes authored on different dates = **copy-forward suspect**.
3. Tag the evidence row `MATCH_IS_COPY_FORWARD = TRUE` and assign a stable `MATCH_COPY_FORWARD_GROUP_ID` (hash of the block).
4. Attribution rule: **prefer the original encounter** (earliest note containing the block) as the source of DoS. If the original cannot be located, downgrade confidence and route to human review.
5. **Dedupe for numerator counting** on `(member, measure, criteria, MATCH_DATE, evidence_block_hash)`. Without this, one copy-forwarded note inflates evidence count tenfold.

This is the single most-cited finding in NCQA MRRV audits. A pipeline that ships without copy-forward dedup has a known audit-fatal defect.

## 17. Provenance column schema (MERGE contract)

Replace the minimal `(MATCH_DATE, MATCH_DATE_TEXT)` output with the full provenance set. This is the column set a HEDIS auditor expects on every supplemental-data row.

```
MATCH_DATE                    DATE
MATCH_DATE_TEXT               STRING
MATCH_DATE_KIND               STRING   -- service | procedure | collection | study | result | order | scheduled | signed | authored | addendum | pathology | administration | unknown_inline
MATCH_DATE_PRECISION          STRING   -- day | month | year
MATCH_DATE_STRATEGY           STRING   -- S0a | S0b | S0c | S0d | S1 | S2 | S3 | S4 | S5 | S6 | S7
MATCH_DATE_DISTANCE_TOKENS    INT
MATCH_DATE_SECTION            STRING   -- e.g., "Procedures", "HPI", "Plan"
MATCH_DATE_IN_TABLE           BOOLEAN
MATCH_NOTE_TYPE               STRING   -- op_note | progress_note | lab_report | imaging_report | discharge_summary | path_report | ed_note | patient_message | phone_note | scanned_outside
MATCH_TENSE                   STRING   -- PAST_DONE | FUTURE_NOT_DONE | PATIENT_REPORTED
MATCH_IS_COPY_FORWARD         BOOLEAN
MATCH_COPY_FORWARD_GROUP_ID   STRING
MATCH_PROVIDER_CREDENTIAL     STRING   -- MD | DO | NP | PA | RN | OTHER | UNKNOWN
```

**Defensibility:** without these, the answer to a reviewer asking "why is this dated 03/15/2024?" is "20 char distance" - not defensible. With these, the answer is "S2 same row of the Procedures flowsheet on page 4, signed by attending MD, not copy-forward" - defensible.

## 18. Date precision

Date precision is not just a number. Per-measure `required_precision` (see §14) drives whether year-only references qualify.

- `day` - `11/14/2022` and `today` (anchored).
- `month` - `November 2022`. Lower = 2022-11-01; upper = 2022-11-30.
- `year` - `in 2022`. Lower = 2022-01-01; upper = 2022-12-31.

**Never silently normalize year-only to 12/31.** That makes year-only dates always appear in-window when the look-back ends mid-year. For look-back boundaries near year-end, year-precision dates must be flagged HINT, not MATCH, unless the entire calendar year is contained in the window.

Dateparser libraries (e.g., Python `dateparser`) parse `MM/DD` vs `DD/MM` ambiguously without pinned settings. **Pin locale settings** explicitly per source. Defaulting locale produces locale-dependent results that change between dev and prod.

## 19. DocTime anchoring

The document encounter date is the **DocTime anchor** for all relative-date resolution within that document:

- `today` → DocTime
- `yesterday` → DocTime - 1
- `last week` → DocTime - 7 days (with precision = week if needed)
- `2 weeks ago` → DocTime - 14 days
- `earlier this year` → year of DocTime, precision = year
- `last colonoscopy 10 years ago` → year of DocTime - 10, precision = year

Fallback when DocTime is missing: note signing date with confidence downgrade. Without DocTime, every `colonoscopy performed today` with no inline date is lost. This unlocks evidence that the proximity-only design cannot see at all.

## 20. Capability punch list (M1-M12)

Ranked by MRRV-defensibility ROI from a chart-reviewer-plus-engineer lens. Use this to sequence implementation.

| # | Capability | Why it matters | Effort |
|---|---|---|---|
| M1 | Document-header date extraction (Encounter / Visit / Procedure / Collection / Study) per page | Highest-precision DoS, no NLP-proximity needed | S |
| M2 | Note-type classification per document | Drives which DoS field is authoritative | S |
| M3 | Section detection and tagging of every char offset | Enables rejecting Plan / PMH / FamHx / Allergies; enables trusting Procedures / Op Note Body | M |
| M4 | Tense / modality classifier (PAST_DONE / FUTURE_NOT_DONE / PATIENT_REPORTED) | Stops `scheduled colonoscopy 6/1/2024` from being a MATCH | M |
| M5 | Date-kind classifier at extraction time | Replaces "any date near keyword" with "the right kind of date" | M |
| M6 | Date precision (day / month / year) + per-measure precision requirement | Removes silent `2022` → 12/31/2022 defensibility hole | S |
| M7 | Specimen-collection-date preference for lab-result evidence | Required for GSD / CBP / KED rate accuracy at year boundaries | S |
| M8 | Copy-forward detection + dedupe | NCQA MRRV #1 audit citation | M |
| M9 | DocTime anchoring of relative phrases | Unlocks evidence with no explicit date at all | M-L |
| M10 | Provider attribution on each evidence row | Some measures require MD / DO / NP / PA-signed documentation | S |
| M11 | Source-section provenance column written to MATCH | MRRV defensibility; reviewer asks "where did you find this?" | S |
| M12 | Date kind and provenance written to EVID_HISTORY | Diffable, auditable, supports model-card updates | S |

**Phased rollout:** start with **M1 + M6 + M7 + M11** (the four small-effort items that close the most-cited audit gaps in one release). M1 alone typically recovers a meaningful share of currently-downgraded MATCHes for COL-E, BCS-E, and GSD because the answer is sitting in the header. M3 / M4 / M5 / M8 form the second wave. M9 (DocTime) is the largest individual lift.

## 21. Per-measure rate-delta validation

After cascade rollout, the per-measure rate-delta report should add these breakdowns to catch silent regressions:

- Distribution of `MATCH_DATE_STRATEGY` per measure (sanity: COL-E should be S0a / S0d dominant after rework).
- Distribution of `MATCH_DATE_KIND` per measure (sanity: GSD / DBM should be `collection` dominant).
- Copy-forward rate per measure (sanity: typically 10-30% in primary care notes).
- Tense-rejection rate per measure (sanity: 1-5% downgrade from `FUTURE_NOT_DONE`).
- Year-only precision rate per measure (sanity: should drop after M6 lands).

If any of these distributions shift dramatically across runs, treat it as a regression signal.

## See also

- [`../../../medical-chart-review/references/date-of-service.md`](../../../medical-chart-review/references/date-of-service.md) - clinical taxonomy (date kinds, sections, tense lexicon, note-type → DoS)
- [`negation-and-assertion.md`](negation-and-assertion.md) - the other top failure mode; tense classifier runs in parallel with negation
- [`extraction-patterns.md`](extraction-patterns.md) - section detection, table-region detection, copy-forward heuristics *(Phase 3)*
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - metrics and failure-mode catalog *(Phase 4)*
- [`../hedis/README.md`](../hedis/README.md) - per-measure cards with measure-specific DoS tables
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - MRRV implications
- Sibling [`../../hcc-nlp/references/date-of-service.md`](../../hcc-nlp/references/date-of-service.md) - HCC contract and HCC-specific cascade deltas

## Defer to humans

Before flipping any of §13-§20 in production:

- An NCQA-certified HEDIS auditor should sign off on the per-measure `dos_policy` (especially `invalid_sections`, `invalid_date_kinds`, `required_precision`) per measure year.
- A CCDS or CRC credentialed reviewer should sign off on the tense / modality lexicon and the copy-forward dedup rule.
- Any change that moves publicly reported rates needs formal change control with rate-delta sign-off.
