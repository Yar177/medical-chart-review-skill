# Negation and assertion for HEDIS NLP extraction

> **Why this file exists:** Naive keyword extractors on clinical text generate huge false-positive rates because clinical narrative is full of negated, hedged, historical, hypothetical, and family-attributed mentions. For HEDIS, an unhandled negation can flip non-compliant members to compliant (or vice versa) and survive QA when only spot-checked. This is one of the two top failure modes; the other is date of service (see [`date-of-service.md`](date-of-service.md)).

This file gives the shared assertion framework. Each per-measure card in [`../hedis/`](../hedis/) has a measure-specific assertion-pitfalls block; the grid below shows all 24 measures.

---

## 1. The ConText framework (4 dimensions)

The ConText algorithm (Chapman et al.) extends NegEx with three additional assertion dimensions. Most clinical NLP libraries implement some form of it. The four dimensions:

| Dimension | Values | Question it answers |
|---|---|---|
| **Negation** | affirmed / negated | Is the concept asserted as present or absent? |
| **Temporality** | current / historical / future / hypothetical | Is the concept happening now, in the past, planned, or conditional? |
| **Experiencer** | patient / other (family, donor, etc.) | Whose concept is this? |
| **Certainty** | definite / possible / probable / hedged | How confident is the author? |

For HEDIS evidence, the default acceptable assertion profile is usually:
- Negation = **affirmed**
- Temporality = **current** (within the measure's window)
- Experiencer = **patient**
- Certainty = **definite**

Exceptions exist (e.g., historical procedures with a long look-back like COL-E colonoscopy are valid; see measure cards).

## 2. NegEx triggers and scope

NegEx works on trigger phrases with a scope window (typically forward 5-6 tokens, blocked by sentence boundaries and termination triggers).

Common trigger families:

- **Pre-negation:** "no", "denies", "no evidence of", "not", "without", "negative for", "ruled out"
- **Post-negation:** "ruled out", "not present", "is absent"
- **Pseudo-negation (look like negation but aren't):** "not only", "no further", "no change", "no significant change", "not necessarily"
- **Termination triggers:** "but", "however", "though", "except", section boundaries

HEDIS-specific gotchas:

- **"Negative mammogram"** literally means a screening mammogram with a normal result - this is POSITIVE evidence for BCS-E, not a negated mammogram. NegEx will get it wrong if you treat "negative" as a generic negator over the concept "mammogram".
- **"Patient denies chest pain"** is negation of the symptom, not of the patient.
- **"Without complications"** in a procedure note is a quality modifier, not a negation of the procedure.

## 3. Temporality pitfalls

Historical mentions are the largest source of false positives in HEDIS extraction:

- **"Hx of breast cancer"** - historical; relevant for BCS-E exclusion logic, not numerator
- **"PMH: T2DM, HTN, HLD"** - problem-list-style historical mentions; need separate active-vs-resolved logic
- **"Last A1c was 11% in 2022"** - temporality = historical with embedded date; honor the date, do not attribute to current MY
- **"Will schedule colonoscopy"** - future intent; not evidence
- **"If symptoms recur, consider repeat imaging"** - hypothetical; not evidence
- **"Pre-op clearance for upcoming knee surgery"** - future-anchored; not the procedure itself

Section-level temporality cues:

- "Past Medical History" / "PMH" / "History" → default historical
- "Hospital Course" → events during admission (relative to discharge date)
- "Plan" → often future or conditional
- "Assessment" → current findings
- "Results" → current data with their own dates

## 4. Experiencer pitfalls

- "FH of breast cancer in mother" - family history, not patient evidence
- "Donor with hep C exposure" - other experiencer
- "Spouse has T2DM, patient asking about screening" - context for current visit, but the diabetes is the spouse's
- "Sister deceased from CRC age 45" - family history (relevant for COL-E risk stratification, not patient evidence)

Common false positives:

- Pediatric notes that include parent / sibling history alongside child's history in the same paragraph
- Counseling notes that describe family members in detail

## 5. Certainty / hedging pitfalls

- "Possible UTI" - hedged, not definitive diagnosis
- "Rule out PE" - workup hypothesis, not diagnosis
- "Cannot exclude malignancy" - hedged
- "Suspected dementia" - hedged
- "Concerning for" - hedged
- "Consistent with" - hedged (lab/imaging interpretation language)

For HEDIS measures requiring a definite finding (e.g., the diabetes diagnosis qualification for GSD denominator), hedged mentions should not auto-qualify.

## 6. HEDIS-specific anti-patterns

These patterns recur across measures; per-measure cards add measure-specific ones.

| Anti-pattern | What it looks like | Why it bites |
|---|---|---|
| **"Negative result" = positive evidence** | "negative mammogram", "Pap negative", "FIT negative" | Screening completed with normal result; counts as numerator hit |
| **Refusal ≠ negation of measure** | "patient declined screening" | Tracked separately; does not close measure |
| **Order ≠ completion** | "A1c ordered", "referred for colonoscopy" | Future / intent; not evidence |
| **"Stable" / "at goal" without value** | "A1c at goal, continue regimen" | Hedged; needs the actual number |
| **Copy-forward problem list** | "Active: T2DM, HTN, HLD" repeated across notes | Problem-list-driven historical mentions; not necessarily evidence of current encounter activity |
| **Future tense for the measure action** | "will get her flu shot next visit" | Future intent |
| **Boilerplate review** | "Med list reviewed and reconciled" without actual reconciliation evidence | Especially bites COA, MRP, TRC - measures need substantive review, not pro-forma phrases |
| **Provider note about non-patient** | "Mother had cervical cancer" appearing in a same-paragraph context with patient screening discussion | Experiencer confusion |
| **Symptom denial** | "Denies chest pain, SOB, edema" | Negation of symptoms, not of clinical actions or findings |
| **Pseudo-negation** | "no change in A1c", "no further imaging needed" | "no" appears but is not negating the measure concept |

## 7. Library landscape

Named without version pins; **verify currency before adoption**:

- **medspaCy** - spaCy pipeline with ConText, target rules, sentence splitter; good production starting point for Python shops
- **negspacy** - lightweight NegEx-only for spaCy
- **pyConTextNLP** - reference ConText implementation in Python
- **NegBio** - rule-based negation / uncertainty tuned for radiology; transferable patterns
- **Apache cTAKES** - Java pipeline with UMLS lookup, ConText, dependency parser; mature in enterprise settings
- **CLAMP** - clinical NLP toolkit with GUI rule authoring; ConText built in
- **scispaCy** - biomedical NER and UMLS linking; pair with negspacy / medspaCy for assertion

For implied or long-range negation (cross-sentence, cross-section), **transformer-based assertion classifiers** (fine-tuned on i2b2 / 2010 challenge data, MedNLI, or in-house annotated data) can outperform rule-based ConText. They are heavier to deploy and harder to audit; pair with rule-based ConText as a backstop for HEDIS use.

LLM-based assertion classification is feasible but should be validated against a measure-specific golden set before use in production, and never as sole source for evidence that feeds supplemental-data submissions.

## 8. Measure × pitfall grid (all 24)

| Measure | Top assertion pitfall | Why |
|---|---|---|
| **GSD** | "Negative for retinopathy; HbA1c 6.8%" - "negative" scopes too far | NegEx must respect concept boundaries |
| **BPD** | "BP at goal" or "BP controlled" without numeric value | Hedged; needs the value |
| **EED** | "Will refer to ophthalmology" | Future referral, not exam |
| **KED** | "uACR ordered" without result | Order ≠ evidence |
| **SUPD** | "Statin therapy intolerance documented" | Exclusion signal; may exclude from denominator |
| **CBP** | "BP elevated today, recheck recommended" | Encounter BP is the data; "recheck" is future |
| **SPC** | "Patient declines statin due to side effects" | Refusal; not negation of measure concept |
| **BCS-E** | "Negative mammogram 6 months ago" | Negative = normal result = POSITIVE evidence |
| **CCS-E** | "Pap deferred until next visit" | Future intent |
| **COL-E** | "Cologuard kit given to patient" | Distribution ≠ completion; need result |
| **DBM** | "Recommended diagnostic mammogram" after abnormal screening | Recommendation, not the follow-up itself |
| **FUH** | "Phone call with patient post-discharge" | Phone ≠ qualifying visit (verify spec - some sub-indicators accept telehealth) |
| **PHQ** | "PHQ-2 reviewed in chart" | Review of past PHQ ≠ new administration |
| **MRP** | "Med list reviewed" boilerplate | Needs substantive reconciliation, not pro-forma phrase |
| **TRC** | "Discharge summary received" | Receipt ≠ all four TRC sub-indicators |
| **PPC** | "Hx of pregnancy" without delivery anchor | Historical reference, needs current pregnancy anchor |
| **W30** | "Sick visit, also discussed development" | Sick visit is not a well visit even if some well content covered |
| **WCV** | "School physical form completed" | May not meet full well-care components |
| **WCC** | "BMI calculated" without documented value or percentile (peds) | Need explicit BMI documentation; pediatric needs percentile |
| **ACP** | "Patient has living will" | Existence ≠ this-MY discussion or document |
| **AIS-E** | "Up to date on immunizations" without specific vaccine + date | Hedged, non-specific |
| **COA** | "Functional status: independent" without assessment evidence | Boilerplate, not assessment |
| **FRM** | "No falls reported" | Negation of falls; but the measure asks about fall-risk management when risk is present |
| **OSW** | "DXA ordered" without completion | Order ≠ evidence |

## 9. Worked test cases

**Case 1 - "Negative mammogram" for BCS-E**
> Text: "Patient had negative screening mammogram on 3/1/2024."
> Right answer: POSITIVE evidence for BCS-E.
> Failure mode: NegEx flips it to negated.

**Case 2 - "Patient denies chest pain"**
> Text: "Patient denies chest pain, shortness of breath, palpitations."
> Right answer: Symptoms are negated. Does NOT affect any HEDIS measure evidence; just symptom history.
> Failure mode: Scoping negation onto unrelated downstream concepts.

**Case 3 - GSD A1c near "negative for retinopathy"**
> Text: "Eye exam negative for diabetic retinopathy. HbA1c 7.1%."
> Right answer: HbA1c is POSITIVE evidence (affirmed, current, patient, definite).
> Failure mode: Sentence-boundary failure lets "negative" scope into the next sentence.

**Case 4 - PMH historical T2DM**
> Text: "PMH: T2DM, HTN, HLD. Today's visit: knee pain."
> Right answer: Diabetes diagnosis is historical PMH - valid for GSD denominator (chronic dx persists), but does NOT mean today's visit is a diabetes-management encounter.
> Failure mode: Treating PMH mentions as today's encounter evidence.

**Case 5 - "Last A1c was 11% in 2022"**
> Text: Note from 6/1/2025: "Last A1c was 11% in 2022, patient lost to follow-up."
> Right answer: Temporality = historical; date = 2022; does NOT count as MY 2024 or MY 2025 evidence.
> Failure mode: Attributing historical value to current MY because note is in current MY.

**Case 6 - "Will check A1c next visit"**
> Text: "Plan: continue metformin, will check A1c next visit."
> Right answer: Future; not evidence.
> Failure mode: Plan-section concepts treated as current findings.

**Case 7 - "Mother had breast cancer at 45"**
> Text: "FH significant for mother with breast cancer at age 45."
> Right answer: Experiencer = family; relevant for BCS-E risk discussion (not numerator), not patient evidence.
> Failure mode: Counting family history toward patient measure.

**Case 8 - "Possible UTI"**
> Text: "A: possible UTI, will await urinalysis."
> Right answer: Hedged; not a definite diagnosis.
> Failure mode: Hedged diagnoses qualifying members for chronic-condition measures.

**Case 9 - "Patient declined screening"**
> Text: "Discussed colorectal screening. Patient declined at this time."
> Right answer: Refusal documented; does NOT close measure; tracked separately.
> Failure mode: Treating refusal as a numerator-closing action or as negation of measure relevance.

**Case 10 - "Cologuard kit given"**
> Text: "Cologuard kit dispensed to patient today."
> Right answer: NOT evidence; need result.
> Failure mode: Counting distribution as completion.

**Case 11 - "Med list reviewed and reconciled"**
> Text: "Medications reviewed and reconciled with patient at today's visit."
> Right answer: Marginal for MRP / COA-Med Review / TRC-Med - boilerplate without details may or may not pass MRRV depending on context and spec stringency.
> Failure mode: Accepting boilerplate as substantive reconciliation.

**Case 12 - "No change in A1c"**
> Text: "A1c stable at 6.9%, no change from last quarter."
> Right answer: POSITIVE evidence (A1c value present); "no" does NOT negate.
> Failure mode: Pseudo-negation triggers NegEx.

**Case 13 - "Up to date on immunizations"**
> Text: "Vaccines: up to date."
> Right answer: NOT specific evidence for AIS-E sub-indicators; need named vaccine + date.
> Failure mode: Hedged, non-specific phrase qualifying multiple immunization measures.

**Case 14 - "Living will on file"**
> Text: "Patient has living will on file from 2019."
> Right answer: For ACP, existence alone may not satisfy current MY discussion requirement (spec-dependent).
> Failure mode: Counting pre-existing document as current-MY ACP action.

**Case 15 - "Phone call with patient" for FUH-7**
> Text: "Day 5 post-discharge: phone call with patient by case manager. Discussed med list and follow-up."
> Right answer: For FUH, phone calls typically do NOT meet visit criteria unless explicitly spec-allowed (verify MY).
> Failure mode: Counting non-qualifying contacts.

**Case 16 - "Telehealth visit for med rec"**
> Text: "Telehealth visit 5 days post-discharge with PCP, med list reconciled."
> Right answer: Telehealth often qualifies for MRP / TRC sub-indicators - verify spec and place-of-service.
> Failure mode: Excluding telehealth when spec accepts it (reverse of Case 15 failure).

**Case 17 - "Recommend diagnostic mammogram"**
> Text: "Screening mammogram BIRADS 0. Recommend diagnostic mammogram with US."
> Right answer: Recommendation alone is NOT the DBM follow-up; need actual completion.
> Failure mode: Counting recommendation as completion.

**Case 18 - "Sports physical"**
> Text: "Annual sports physical: cleared for football. BP 110/70, vision 20/20."
> Right answer: For WCV, sports physical typically does not meet full well-care components.
> Failure mode: Treating any annual visit as a well visit.

**Case 19 - "Statin not tolerated"**
> Text: "Atorvastatin caused myalgia, discontinued. Statin therapy not tolerated."
> Right answer: For SPC / SUPD, this is a documented exclusion signal that may exempt from denominator (spec-dependent).
> Failure mode: Treating exclusion-language as evidence of non-compliance.

**Case 20 - "Patient sister had CRC at 40"**
> Text: "FH: sister with CRC dx at 40."
> Right answer: Family history affecting screening risk (earlier screening may be indicated), not patient evidence for COL-E.
> Failure mode: Attributing family history to patient.

## 10. Validation strategy for assertion extraction

- **Golden test set** per measure of 100-500 manually annotated spans with ConText attributes (negation, temporality, experiencer, certainty).
- Metrics: per-attribute accuracy, F1 on the affirmed-current-patient-definite "scoreable" class.
- **Stratify failures** by ConText dimension - usually one dimension drives most errors per measure.
- **Inter-annotator agreement** (Cohen's kappa) on each dimension before treating the gold set as ground truth.
- **Adversarial test pack** of the patterns in section 6 - keep these always-on as regression gates.

## See also

- [`date-of-service.md`](date-of-service.md) - the other top failure mode
- [`extraction-patterns.md`](extraction-patterns.md) - section detection, copy-forward, telehealth *(Phase 3)*
- [`annotation-guidelines.md`](annotation-guidelines.md) - how to label assertion attributes *(Phase 4)*
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - metrics, failure-mode catalog *(Phase 4)*
- [`../hedis/README.md`](../hedis/README.md) - per-measure cards with measure-specific pitfalls
