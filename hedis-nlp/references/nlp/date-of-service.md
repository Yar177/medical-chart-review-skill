# Date of Service (DoS) for HEDIS NLP extraction

> **Why this file exists:** Date of service is one of the two biggest accuracy killers in HEDIS NLP (the other is negation - see [`negation-and-assertion.md`](negation-and-assertion.md)). The wrong date can flip a compliant member to non-compliant, attribute evidence to the wrong measurement year, or trigger MRRV failure even when the clinical content is correct.

This file gives the shared DoS framework. Each per-measure card in [`../hedis/`](../hedis/) has a measure-specific DoS table; the grid below shows all 24 measures at a glance.

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

## See also

- [`negation-and-assertion.md`](negation-and-assertion.md) - the other top failure mode
- [`extraction-patterns.md`](extraction-patterns.md) - section detection, copy-forward heuristics *(Phase 3)*
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - metrics and failure-mode catalog *(Phase 4)*
- [`../hedis/README.md`](../hedis/README.md) - per-measure cards with measure-specific DoS tables
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - MRRV implications
