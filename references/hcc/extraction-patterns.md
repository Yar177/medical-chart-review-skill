# HCC extraction patterns

> **Why this file exists:** HCC pipelines do two structurally different jobs: **suspect** ("this member may have HCC X, surface for review or recapture") and **validate** ("this DOS supports HCC X with MEAT for billing or audit defense"). Conflating them is the most common HCC pipeline architecture mistake.

This file covers the suspect-vs-validate split, the provenance requirements that drive both, and the section / encounter / document handling shared with the HEDIS extraction-patterns file.

The cross-cutting HEDIS extraction-patterns reference is at [`../nlp/extraction-patterns.md`](../nlp/extraction-patterns.md). Most of that content (section detection, abbreviation expansion, doc-type classification, copy-forward detection) applies here unchanged; this file calls out HCC-specific extensions.

---

## 1. Suspect vs validate as separate pipelines

| Pipeline | Job | Precision target | Recall target | Output | Audit posture |
|---|---|---|---|---|---|
| **Suspect** | Identify members likely to have an HCC, including recapture | Moderate | High | Member-level scored list per HCC | Surfaces opportunities for re-encounter, query, or documentation outreach |
| **Validate** | Confirm a specific HCC is supported on a specific DOS | High | Moderate | Encounter-level assertion + MEAT record | Output drives claims and audit defense |

Why this split matters:

- A suspect engine that prioritizes precision misses recapture opportunities. The downstream cost of a missed recapture is real dollars.
- A validate engine that prioritizes recall over-codes. The downstream cost of over-coding is RADV exposure and FCA risk.
- They have different positive labels: suspect labels are "this member has the condition somewhere"; validate labels are "this DOS supports it with MEAT."
- They have different gold standards: suspect can use claims history and chart-wide signals; validate needs encounter-scoped span-level annotation.

Most mature plans run both. The suspect engine drives outreach and pre-visit prep; the validate engine drives claims submission and audit response.

## 2. Suspect-engine patterns

Common signal types:

- **Historical claims**: prior-year HCC claims, especially chronic ones not yet recaptured this year
- **Pharmacy fills**: a member filling metformin probably has diabetes
- **Lab results**: HbA1c trends suggest diabetes; eGFR trends suggest CKD; BNP suggests heart failure
- **Free-text mentions across the chart**: diagnosis mentioned anywhere (problem list, prior notes, outside records) without current-year recapture
- **Specialty referrals**: nephrology consult suggests CKD; oncology suggests cancer; pulmonology suggests COPD
- **Imaging / procedures**: cardiac cath suggests CAD; stress test ordered suggests cardiac suspicion
- **Care-gap signals**: no annual visit yet, no AWV scheduled

Aggregate to a member-level score per HCC. Surface as a worklist for care management or pre-visit planning.

Pipeline notes:

- Suspect output does NOT carry a DOS. It is member-level.
- Suspect output should never auto-submit to claims. It is a workflow signal.
- Suspect should incorporate the year context: highlight prior-year HCCs not yet captured THIS year.
- Strength of evidence matters; surface confidence so care teams prioritize correctly.

## 3. Validate-engine patterns

The validate engine is the one most NLP teams build first. It is also the one with the highest precision requirement.

Required inputs per encounter:

- Note text (full)
- Encounter date
- Encounter type / setting (office, inpatient, telehealth, AWV, etc.)
- Signing provider and credential
- (Ideally) prior encounters for the same member for cross-encounter context

Required output per validated HCC:

- HCC number and model version
- ICD-10 code
- Source span with character offsets
- Section detection
- Full assertion record (see [`negation-and-assertion.md`](negation-and-assertion.md))
- MEAT evidence with linkage (see [`meat-criteria.md`](meat-criteria.md))
- Copy-forward detection status
- Confidence score
- Suggested audit verdict: Auto-validate / Route to human / Reject

Validate output flows into:

- Claims submission decisions (post-human-review for most plans)
- Audit defense packets when challenged

## 4. Two-pass extraction architecture

A robust pipeline shape:

```
Pass 1: Candidate generation
  - Diagnosis NER on the note
  - ICD-10 / SNOMED candidate codes per span
  - Section, encounter date, signer attached
  - Output: superset of possible HCC candidates with low precision, high recall

Pass 2: Assertion + MEAT + hierarchy
  - Assertion classifier on each candidate
  - History-of / family / hypothetical / hedging filters
  - Status code disambiguation
  - MEAT detection and linkage
  - Discard candidates failing assertion or MEAT
  - Output: high-precision per-encounter HCC list

Pass 3 (post-encounter roll-up):
  - Year-level dedup
  - Hierarchy application
  - Interaction detection
  - Output: member-year HCC list for RAF estimation and claims
```

Why two passes: assertion and MEAT are conceptually orthogonal to diagnosis extraction. Combining them in one model muddies the gradient and makes errors hard to attribute. Two-pass with clear handoffs is easier to debug, evaluate, and improve.

## 5. Provenance requirements

Every extracted HCC must carry enough metadata to be re-found by an auditor:

- Source document identifier
- Encounter date
- Section name
- Character offsets in the source text (or equivalent for structured sources)
- Signing provider
- Pipeline version and model version
- Crosswalk vintage

This is non-negotiable for any HCC that will hit a claim. RADV requires the plan to produce the supporting chart on demand; if the pipeline cannot point an auditor at the exact span, the plan cannot defend it.

## 6. Problem-list-only is invalid

A diagnosis appearing only in the problem list, with no MEAT anywhere else in the encounter, is **not valid** for risk adjustment. The problem list is a chronic-condition registry, not encounter-specific documentation.

Pipeline rule:

- Problem list mentions can contribute to the **candidate** set in pass 1.
- Problem list mentions cannot, on their own, validate an HCC in pass 2.
- An HCC validated only from problem-list text must be rejected or routed to human review.

This is one of the easiest pipeline mistakes to make because problem-list content is structured, easy to parse, and often the most copious source of diagnosis mentions in a chart. It is also one of the highest-risk mistakes.

## 7. Section detection for HCC

The HEDIS section-detection guidance applies. HCC-specific additions:

- **PMH / Past Medical History** - historical assertion prior; current chronic conditions may live here but require explicit current-activity language
- **PSH / Past Surgical History** - drives status codes (s/p amputation, s/p transplant, s/p mastectomy)
- **FH / Family History** - never patient
- **AWV templates** - need recognition because they often have auto-populated problem-list review without per-condition MEAT; mark them and apply stricter MEAT scrutiny
- **Discharge summary "final diagnoses" / "discharge diagnoses"** - the inpatient-hedging exception only applies here

## 8. Telehealth, outside records, scanned PDFs

Same patterns as HEDIS (see [`../nlp/extraction-patterns.md`](../nlp/extraction-patterns.md)). HCC-specific notes:

- **Outside records**: useful for suspect, generally NOT valid for validate unless the outside encounter is itself a qualifying face-to-face that the plan can produce on RADV request. Default to suspect-only.
- **Scanned PDFs**: OCR introduces noise that affects assertion detection more than candidate detection. A garbled "history of" might extract as "history o" and miss the historical-modifier check.
- **Telehealth**: must distinguish video from audio-only; downgrade audio-only for current-year rules (see [`date-of-service.md`](date-of-service.md)).

## 9. Cross-encounter context

Some HCC decisions need cross-encounter context:

- Annual recapture: was this HCC also captured earlier in the year?
- Status verification: does the chart establish elsewhere that the amputation actually happened?
- Hierarchy reasoning: does an earlier encounter document the more severe form?
- Resolution detection: did a later encounter document "resolved" or "in remission"?

Pipelines that only look at the current note miss these. Patient-level state, updated as encounters are processed, is a useful pattern. Be careful: state must be timestamped so you do not leak future information into past decisions when reprocessing.

## 10. Multi-doc linking

A single member-year often spans multiple documents from multiple sources:

- PCP office notes
- Specialist consult notes
- Inpatient admission and discharge summaries
- ED visits
- Skilled nursing facility notes
- Outside records ingested via HIE

The validate engine processes encounters independently. The roll-up engine combines per-encounter results into the member-year HCC list, then applies hierarchies and interactions ([`hierarchies.md`](hierarchies.md), [`raf-calculation.md`](raf-calculation.md)).

## 11. Common architecture mistakes

- **Single-pass model that emits HCC numbers directly.** Loses provenance, hard to audit, hard to update for model-version changes.
- **Hierarchy logic in the extractor.** Couples extraction to a specific model version; better as a post-step.
- **No suspect engine.** Plan misses recapture opportunities equal to or exceeding the validate engine's lift.
- **Validate engine outputs claims directly with no human-in-the-loop.** Catastrophic precision risk; not defensible.
- **No provenance.** When an auditor asks for the chart, the plan cannot find it.
- **Problem-list-only validations.** RADV failure pattern.
- **No copy-forward detection.** Wrong-DOS attribution; cross-year leakage.
- **No version-pinning.** Cannot reproduce historical RAF estimates.

## See also

- [`../nlp/extraction-patterns.md`](../nlp/extraction-patterns.md) - shared HEDIS extraction patterns
- [`meat-criteria.md`](meat-criteria.md) - MEAT detection is the bulk of pass 2
- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion classification, also pass 2
- [`hierarchies.md`](hierarchies.md) - post-roll-up hierarchy enforcement
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - measuring both suspect and validate quality
