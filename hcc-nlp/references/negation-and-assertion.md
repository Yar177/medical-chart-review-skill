# Negation and assertion for HCC NLP

> **Why this file exists:** Misclassifying "history of" as "active" is the #1 RADV finding category. Status codes are #2. The general HEDIS negation framework does not handle either correctly out of the box. HCC pipelines need an assertion taxonomy that goes well beyond present / absent.

The cross-cutting HEDIS framework lives in the sibling `hedis-nlp` skill's `references/nlp/negation-and-assertion.md` (in this same repo). This file extends it for HCC. Use both.

---

## 1. The HCC assertion taxonomy

For each candidate diagnosis span, classify across at least these dimensions:

| Dimension | Values | HCC consequence |
|---|---|---|
| **Negation** | Present / Absent | Absent → never code |
| **Temporality** | Current / Historical / Future | Historical → status-code question; Future → never code |
| **History modifier** | None / "history of" / "h/o" / "PMH:" / "resolved" / "remote" | Triggers status-code check |
| **Status modifier** | None / status-post / s/p / "on dialysis" / "with pacemaker" | Maps to Z-code, not active disease |
| **Experiencer** | Patient / Family / Other | Family → never code for patient |
| **Hypothetical** | Real / Hypothetical / Conditional | Hypothetical → never code |
| **Hedging (outpatient)** | Confirmed / Probable / Suspected / Rule-out | In outpatient, hedged → never code |
| **Setting** | Inpatient / Outpatient | Selects hedging rule (see section 5) |
| **Subject** | This encounter / Carried forward / Outside record | Affects MEAT validation, not the assertion itself |

A diagnosis is **codable** only when assertion is Present + Current + Real + Patient + (Confirmed if outpatient).

## 2. History-of: the #1 RADV finding

"History of breast cancer in remission for 12 years, s/p mastectomy" is NOT C50 (active breast cancer). It is Z85.3 (personal history of malignant neoplasm of breast). Coding it as active inflates RAF and fails audit immediately.

The pipeline must detect history-of as a first-class assertion class, not as a flavor of negation.

**Trigger phrases for history-of:**

- "history of" / "h/o" / "hx of" / "hx:"
- "PMH:" / "past medical history" / "past surgical history"
- "remote history of" / "remote hx"
- "previously diagnosed with"
- "in remission" / "no evidence of recurrence" / "NED" / "NER"
- "status post" / "s/p" / "post-" (for surgical resolution)
- "resolved" / "cleared" / "treated and resolved"
- Dates many years prior with no current activity ("breast cancer 2008, treated, NED since")

**Disambiguation patterns to be careful of:**

- "PMH includes diabetes, hypertension, CHF" - these are CURRENT chronic conditions appearing under a PMH heading. Diabetes does not become history-of just because it is in the PMH section.
- "PMH significant for stroke 2 weeks ago" - the stroke may still be acute / sequelae-coded.
- "history of CHF, currently decompensated" - the "currently decompensated" overrides; this is active.
- "history of acute MI in 2015" - the acute event is historical (Z86.xx old MI codes), but residual cardiomyopathy might be current.

The decision rule: history-of language flags candidate status. Then check for explicit current-activity language (current decompensation, active treatment, current symptoms, current monitoring) that overrides the historical reading.

## 3. Status codes (Z-codes) and HCC

Many "personal history of" and "status of" Z-codes either map to their own HCC (e.g., amputation status, transplant status, ostomy status) or are documentation-required complements to active codes.

Key Z-code families to handle explicitly:

| Z-code family | Meaning | HCC behavior |
|---|---|---|
| **Z85.x** | Personal history of malignant neoplasm | Generally NOT an HCC; replaces active cancer code when in remission |
| **Z86.7x** | Personal history of certain cardiac conditions | Generally NOT an HCC (e.g., old MI) |
| **Z87.x** | Personal history of other diseases | Mostly not HCCs |
| **Z89.x** | Acquired absence of limb (amputation) | **IS an HCC** - must be recaptured annually |
| **Z93.x** | Artificial opening status (ostomy, tracheostomy) | **IS an HCC** for several variants - must be recaptured |
| **Z94.x** | Transplanted organ / tissue status | **IS an HCC** - must be recaptured |
| **Z95.x** | Presence of cardiac / vascular implants | Generally not HCCs themselves but document the underlying disease state (e.g., Z95.5 stent does not imply current PVD) |
| **Z99.x** | Dependence on enabling machines (vent, dialysis) | **IS an HCC** in some variants (e.g., Z99.2 dialysis dependence) |

**Pipeline implications:**

- Treat status / Z-code detection as a separate extractor head, parallel to active-disease extraction.
- For HCC-eligible status codes (Z89, Z93, Z94, Z99 subsets): annual recapture is required. Surface them on the open-HCC list each new year.
- For non-HCC Z-codes that replace an active code (Z85.x replacing active cancer): the pipeline must NOT also emit the active code.
- Z95.x cardiac / vascular implant codes are particularly tricky: they say a procedure happened, not that the underlying disease is currently active. Stent presence (Z95.5) does not establish PVD; document the disease state separately if it is active.

## 4. Family history is not patient history

Common confusion:

- "FH: mother with breast cancer, father with diabetes" - Z80.x and Z83.x; do NOT code the diseases for the patient.
- "FHx significant for early CAD" - Z82.49; not patient's CAD.
- "Patient denies family history of cancer" - the negation here is on family history, which is itself absent; no codable concept.

Pipeline must distinguish:

- Section: family history sections (FH, FHx, Family History) - all content is family
- Phrase: "mother / father / brother / sister / aunt / uncle / grandparent has X" - X is family
- Phrase: "no family history of X" - X is absent in family
- "Patient's family" - same as family

**Failure mode:** a pipeline that treats family-history section content as patient-attributable will fire HCCs for every family-history mention. Catastrophic over-coding.

## 5. Inpatient vs outpatient hedging asymmetry

Repeated from [`date-of-service.md`](date-of-service.md) because it lives at the assertion boundary:

- **Outpatient setting:** Do NOT code probable, suspected, likely, rule-out, working, differential, "consistent with," "cannot rule out," "vs," "?diagnosis."
- **Inpatient setting:** Uncertain diagnoses present AT DISCHARGE may be coded as if confirmed.

Hedging trigger phrases:

- "probable" / "likely" / "suspected" / "presumed"
- "rule out" / "r/o" / "vs" / "versus"
- "cannot rule out" / "could not exclude"
- "consistent with" (sometimes confirmed, sometimes hedged - context-dependent)
- "concerning for" / "worrisome for"
- "differential includes"
- "?" before diagnosis
- "working diagnosis"

Pipeline must:

- Detect hedging spans with the same precision as negation spans.
- Branch on encounter setting (must be input metadata).
- In outpatient mode, treat hedged diagnoses as non-codable.
- In inpatient mode, allow hedged diagnoses only when they appear in the discharge summary's discharge-diagnoses or final-impression section.

## 6. Resolution and remission

Specific assertion classes that look like present but are not:

- "Resolved" / "treated and resolved" / "course completed"
- "In remission" / "complete remission" / "no evidence of recurrence"
- "Cured" (rare in real text but appears)
- "Status post curative resection"

These behave like history-of for coding purposes. The condition is in the past; if a status code exists, use it. The most-watched example is cancer (Z85.x for remission).

## 7. Acute vs chronic and the "old MI" problem

"Old MI" is documentation that an MI occurred in the past, with the patient stable. The acute MI code is no longer appropriate; the correct code is Z86.71 or similar.

Pattern:

- "s/p MI 2012, on aspirin and statin" - old MI, not acute MI
- "acute MI" with current ECG changes and elevated troponin - acute MI, codable as active
- "NSTEMI 3 weeks ago, currently stable" - within the 4-week acute window for some coding purposes; verify against current guidelines

A similar pattern applies to stroke (acute vs old CVA, Z86.73), CHF (acute exacerbation vs chronic), and several other cardiac and neurologic conditions.

## 8. Section-aware assertion

| Section | Assertion priors |
|---|---|
| **HPI** | Current; check for hedging language |
| **PMH** | Historical OR chronic; needs current-activity check |
| **PSH** | Historical (surgical); often triggers status codes |
| **FH** | Family - never patient |
| **SH** | Social - usually not diagnoses |
| **ROS** | Current symptoms or current absence of symptoms |
| **PE** | Current findings |
| **Assessment** | Current and confirmed in outpatient; current with hedging allowed in inpatient |
| **Plan** | Future intent; not evidence on its own |
| **Problem list** | Active but needs MEAT in note; status indicator (active / resolved / inactive) when present is authoritative |

Train classifiers on top of section priors. Do not skip the section signal.

## 9. Library landscape (HCC-specific)

The HEDIS library landscape in the sibling `hedis-nlp` skill's `references/nlp/negation-and-assertion.md` applies here. Specifically for HCC:

- **pyConTextNLP / medspaCy ConText** - handles historical, hypothetical, experiencer, negation natively. The historical and experiencer dimensions are the ones that pay off most for HCC.
- **negspacy** - too narrow on its own; pair with explicit history-of and section-detection rules.
- **MedCAT** - useful for status-code identification when paired with SNOMED.
- **LLM classifiers** - can be tuned for the full assertion taxonomy in section 1, but require careful eval (see [`evaluation-and-validation.md`](evaluation-and-validation.md)). Never auto-submit LLM-only HCC extractions.

## 10. Common assertion failure modes

| Failure | Result | Fix |
|---|---|---|
| History-of treated as active | Over-code, RADV fail, FCA risk | Dedicated history-of detector + section-aware priors |
| Family history treated as patient | Massive over-code | Family-history section detection + relationship-word patterns |
| Status code conflated with active disease | Over-code (Z85 + active cancer both fire) | Mutual-exclusion logic between status code and active code |
| Outpatient hedging not respected | Probable diagnoses fire HCCs | Setting-aware hedging rules |
| Inpatient hedging suppressed everywhere | Miss legitimate discharge HCCs | Allow hedging in inpatient discharge sections |
| "Resolved" missed | Over-code | "Resolved" / "in remission" / "NED" detection |
| Z95.x cardiac/vascular implant fires PVD | Over-code | Implant codes do NOT imply current disease |
| AWV templated problem-list review treated as MEAT | Over-code | Stricter MEAT for AWV-sourced (see meat-criteria.md) |
| Carried-forward A&P fires current-year HCC | Wrong-year attribution | Copy-forward detection + original-date attribution |
| Old MI coded as acute MI | Wrong code, wrong HCC | "Old" / "s/p" / years-prior detection |

## 11. The audit-ready assertion record

For every extracted HCC, store enough metadata to reconstruct the assertion decision:

```yaml
hcc_extraction:
  hcc_v28: 18
  icd10: E11.40
  span: "diabetes with peripheral neuropathy"
  source_span_offset: [4521, 4565]
  source_section: "Assessment"
  assertion:
    negation: present
    temporality: current
    history_modifier: none
    status_modifier: none
    experiencer: patient
    hypothetical: real
    hedging: confirmed
    setting: outpatient
  confidence: 0.92
  meat_link: { ... }
  copy_forward_detected: false
  signing_provider_type: physician
  encounter_date: 2025-06-14
```

This record is what a reviewer or RADV auditor needs to confirm or refute the extraction. Without it, the extraction is not defensible.

## See also

- Sibling `hedis-nlp` skill, `references/nlp/negation-and-assertion.md` - shared HEDIS framework
- [`meat-criteria.md`](meat-criteria.md) - MEAT applies AFTER assertion clears
- [`date-of-service.md`](date-of-service.md) - encounter setting required for hedging rules
- [`extraction-patterns.md`](extraction-patterns.md) - section detection, copy-forward
- [`cards/`](cards/) - per-HCC assertion pitfalls
