# MEAT criteria for HCC NLP

> **Why this file exists:** MEAT is the documentation contract that turns an ICD-10 code into a valid risk-adjusted HCC. An NLP pipeline that finds the code but cannot detect MEAT evidence will pass review on suspect lists and fail RADV on validation. MEAT extraction is its own task with its own signals.

The auditor framing of MEAT lives in the sibling `medical-chart-review` skill's `references/coding-icd10-hcc.md` (in this same repo). This file is the NLP-pipeline framing.

---

## 1. What MEAT is

For every diagnosis claimed for risk adjustment, the medical record on that date of service must demonstrate at least one of:

- **M - Monitor:** signs, symptoms, disease progression / regression, vital trends, lab trends
- **E - Evaluate:** test results reviewed, exam findings, response to treatment
- **A - Assess / Address:** discussion of the condition, decision-making, counseling, ordering tests
- **T - Treat:** medications, therapies, referrals, surgeries, plan changes

A diagnosis appearing only in a problem list, billing slip, or copy-forward block with no MEAT in the encounter narrative is **not codable** for that DOS. This is the #2 RADV finding category after history-of misclassification (see [`negation-and-assertion.md`](negation-and-assertion.md)).

Some auditors also use **TAMPER** (Treatment, Assessment, Monitor / Medicate, Plan, Evaluate, Referral). It is a superset; if you can detect MEAT you can detect TAMPER.

## 2. MEAT as a separate NLP task

MEAT is best modeled as **per-(diagnosis, encounter) evidence classification**, distinct from diagnosis extraction.

Pipeline shape:

1. **Diagnosis candidate extraction** - produce (concept, assertion, location) tuples from the note.
2. **Encounter scoping** - group spans by encounter date.
3. **MEAT detection** - for each (diagnosis, encounter) pair, classify evidence into M / E / A / T categories.
4. **MEAT roll-up** - require at least one category with confident evidence for the (diagnosis, encounter) pair to validate.

Why separate: a single diagnosis often appears in multiple sections (HPI, problem list, assessment, plan). MEAT evidence can come from any of them, and the same span can contribute to multiple categories.

## 3. Detection patterns per category

### Monitor

Section hints: HPI, ROS, Vitals, Results-review

Signal patterns:
- "BP trending up," "weight down 4 lbs since last visit"
- "A1c improving / worsening / stable"
- "asymptomatic today" (counts as monitoring of an active condition)
- Vital sign documentation linked to the condition
- "no new symptoms"

Anti-patterns (looks like monitor but is not):
- Pure historical narrative ("BP was high years ago")
- Family history monitoring
- Copy-forward vital signs that did not happen at this encounter

### Evaluate

Section hints: Results, PE, Assessment

Signal patterns:
- "A1c 8.2," "Cr 1.8," "EF 35%"
- "exam reveals trace edema"
- "responded well to lisinopril"
- "ECG shows AFib, rate-controlled"
- "review of CT chest from 6/1"

Anti-patterns:
- Test ordered but no results reviewed in this note ("will check A1c") - that is Treat / Plan, not Evaluate
- Results in note without linkage to a condition assessment

### Assess / Address

Section hints: Assessment, A&P, Impression

Signal patterns:
- "Diabetes type 2 with neuropathy - well controlled on metformin"
- "discussed importance of statin adherence"
- "reviewed COPD action plan"
- "considered escalation to GLP-1, deferred for now"
- Numbered or bulleted problem list with explicit status per problem

Anti-patterns:
- Problem list dump with no per-problem commentary
- Generic "stable" with no condition reference

### Treat

Section hints: Plan, Medications, Orders, Procedure

Signal patterns:
- "continue metformin 1000 mg BID"
- "start atorvastatin 40 mg"
- "referred to nephrology"
- "scheduled cardiology follow-up in 4 weeks"
- "completed ablation today"
- "ordered repeat A1c in 3 months"

Anti-patterns:
- Medication reconciliation lists without any change or continuation rationale tied to a diagnosis
- Generic "follow up PRN" with no condition linkage

## 4. The "linkage" problem

MEAT evidence must be **linked to the diagnosis it supports**. The hardest NLP failure mode here:

- Note has "diabetes type 2" in problem list
- Note has "BP 135/82" in vitals
- Note has "continue lisinopril" in plan
- None of the assessment text mentions diabetes
- Pipeline finds the diagnosis + monitor + treat evidence and validates the HCC

The audit will fail. The MEAT evidence is for hypertension, not diabetes. The diabetes diagnosis has no MEAT in this encounter.

**Linkage strategies:**

- **Local proximity:** MEAT evidence within the same A&P numbered problem block as the diagnosis
- **Coreference resolution:** "the diabetes is well-controlled" - link "diabetes" forward and back
- **Medication-to-diagnosis mapping:** metformin → diabetes; ACEi alone → hypertension OR CKD OR CHF (ambiguous, need additional signal)
- **Test-to-diagnosis mapping:** A1c → diabetes; BNP → CHF; PFTs → COPD

Loose linkage produces false positives. Strict linkage produces false negatives. Calibrate based on whether you are running a suspect pipeline or a validate pipeline (see [`extraction-patterns.md`](extraction-patterns.md)).

## 5. Section-aware MEAT

Treat note section as a strong prior:

| Section | Best MEAT match | Notes |
|---|---|---|
| HPI | Monitor | Symptom trajectory |
| ROS | Monitor | Negative ROS still counts as monitoring |
| PE | Evaluate | Exam findings |
| Vitals | Monitor + Evaluate | Trends + current |
| Results | Evaluate | Lab / imaging review |
| Assessment | Assess | Per-condition statement |
| Plan | Treat | Meds, orders, referrals |
| Medications | Treat | Active med list with linkage |
| Problem list | None on its own | Must be paired with evidence elsewhere |

This is the most reliable rule-based prior. Train classifiers on top of it; do not skip it.

## 6. Provider type and signature requirements

MEAT evidence must come from an **acceptable provider type** documented in a **face-to-face encounter** signed by that provider. See [`date-of-service.md`](date-of-service.md) for the provider whitelist and signature rules. An NLP pipeline that extracts MEAT from an unsigned student note or an unacceptable provider type will produce technically-correct extractions that fail validation.

## 7. Common MEAT-detection failure modes

- **Treating problem-list presence as MEAT.** Problem list is necessary for context but never sufficient on its own.
- **Counting med-rec lists as Treat.** Pure reconciliation without active continuation or change is not Treat.
- **Counting "noted" or "discussed" without diagnosis linkage.** "Discussed risk factors" is not MEAT for any specific HCC.
- **Counting copy-forward A&P blocks as MEAT.** If the entire A&P is verbatim from a prior note with no update, it does not establish current-encounter MEAT. Detect via the copy-forward signals in [`extraction-patterns.md`](extraction-patterns.md).
- **Counting future-tense plans without current encounter action.** "Will start statin if LDL > 130" is not Treat.
- **Counting "stable" without diagnosis linkage.** "Patient is stable" with no per-condition statement is not MEAT for any HCC.

## 8. MEAT confidence and human review

A reasonable confidence scheme for MEAT detection:

- **High confidence**: At least 2 MEAT categories with strong linkage; passes auto-validation.
- **Medium confidence**: 1 MEAT category with strong linkage, or 2+ with weak linkage; route to human review.
- **Low confidence**: No clear linkage; route to human review or reject for this DOS.

Calibrate auto-validation thresholds against your team's risk tolerance and the precision requirements in [`compliance-and-enforcement.md`](compliance-and-enforcement.md). When in doubt, route to human review.

## See also

- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion comes BEFORE MEAT; a history-of diagnosis is not eligible for MEAT
- [`extraction-patterns.md`](extraction-patterns.md) - section detection and copy-forward
- [`date-of-service.md`](date-of-service.md) - provider type and face-to-face requirements
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - how to measure MEAT detection quality
- Sibling `medical-chart-review` skill, `references/coding-icd10-hcc.md` - auditor framing
