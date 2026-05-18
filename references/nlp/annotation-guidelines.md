# Annotation guidelines for HEDIS chart-review NLP

Practical conventions for building gold-standard datasets for per-measure HEDIS extraction models. Pairs with [`evaluation-and-validation.md`](evaluation-and-validation.md) (how to use the gold) and the per-measure cards in [`../hedis/`](../hedis/) (what each measure requires).

## Audience

Clinical informaticists, annotation leads, RN abstractors, certified coders, and NLP engineers who design and operate annotation projects for HEDIS extraction.

## Scope

- Span and attribute schemas
- Annotator selection and training
- IAA workflows and adjudication
- Synthetic data generation and de-identification
- Annotation tooling considerations
- Common pitfalls

Not in scope: actual PHI handling, IRB / data-governance procedures, specific tool tutorials.

> **Compliance reminder:** Annotation work on real chart data requires HIPAA-compliant infrastructure, BAAs with all vendors, de-identification (Safe Harbor or Expert Determination), and access controls. None of the guidance here substitutes for those controls.

---

## 1. Annotation schema

For each measure, the schema defines what annotators identify and what attributes they tag.

### Core span types

| Span type | What it captures | Example |
|---|---|---|
| `evidence-concept` | The clinical concept that satisfies the numerator | "HbA1c 7.2", "BP 124/78", "mammogram normal" |
| `evidence-date` | The date the evidence was generated (not the note date) | "03/15/2024", "last week", "in March" |
| `provider-role` | Provider type performing the action | "OB/GYN", "Dr. Smith, FP" |
| `assertion-context` | Negation / temporality / experiencer / certainty modifier | "no", "history of", "father with" |
| `modality` | For procedures: how it was done | "dilated exam", "fundus photo", "OCT" |
| `refusal` | Patient refusal documentation | "patient declined mammogram" |
| `exclusion-evidence` | Hospice, frailty, anatomical exclusion | "on hospice", "bilateral mastectomy 2018" |

### Core attribute schema (per evidence-concept span)

```yaml
evidence_id: <unique id>
measure: <measure code, e.g., GSD>
sub_indicator: <if applicable, e.g., TRC-Patient>
concept_label: <a1c_value | bp_reading | mammogram | ...>
value: <if numeric, the value>
units: <if applicable>
date_of_service: <ISO date or null + null_reason>
date_source: <explicit | inferred-from-note-date | inferred-from-document-header>
date_confidence: <high | medium | low>
assertion: <positive | negated | hypothetical | conditional | historical | family>
provider_role: <pcp | obgyn | mh-provider | prescriber | clinical-pharmacist | rn | other | unknown>
modality: <if applicable>
section: <hpi | pmh | assessment | plan | results | ...>
source_document_type: <office_visit_note | discharge_summary | mammogram_report | ...>
source_document_date: <ISO date>
source_document_id: <reference>
verbatim_snippet: <string>
span_char_start: <int>
span_char_end: <int>
page_number: <if paginated>
satisfies_numerator: <true | false | uncertain>
satisfies_numerator_reason: <free text>
annotator_id: <id>
annotation_timestamp: <ISO datetime>
notes: <free text>
```

Adapt per measure: not all attributes apply to every measure. Document which attributes are required vs optional per measure in the measure-specific annotation guide.

### Span boundary conventions

- **Concept spans:** include the full clinical phrase, exclude leading/trailing punctuation. "HbA1c was 7.2%" → span = "HbA1c was 7.2%" or just "7.2%" depending on guideline; pick one and document
- **Date spans:** include the full date expression including modifiers ("approximately March 2024" → full span)
- **Assertion modifiers:** capture the trigger phrase separately ("no evidence of" is its own span linked to the concept it modifies)
- **Nested spans:** allow them; many tools support span hierarchies

Document boundary conventions in your annotation guide so all annotators apply them consistently.

---

## 2. Annotator profiles

| Annotator type | Strengths | Weaknesses |
|---|---|---|
| Certified medical coder (CCS, CPC, CRC) | Code-to-concept mapping, ICD-10/CPT fluency | May default to claims-coding habits over clinical-evidence reading |
| RN with HEDIS abstraction experience | Clinical context, measure intent | May vary in pace and terminology consistency |
| Clinical informaticist | Structure / metadata familiarity | May miss nuances in narrative |
| NLP engineer (non-clinical) | Tool fluency, schema consistency | Not equipped to make clinical judgment calls |

**Mixed-team recommendation:** at least one clinically-credentialed annotator per measure; NLP engineers can do span markup but should not make clinical compliance calls without sign-off.

### Annotator training

1. Walk through 5-10 annotated examples per measure
2. Have trainees annotate 10-20 cases independently
3. Compare to gold; review every disagreement
4. Repeat until trainee reaches target IAA (kappa ≥ 0.70) with the team

### Calibration cadence

- Weekly: short calibration session with 3-5 cases discussed by the whole team
- Monthly: full IAA refresh on a held-out shared set
- After guideline changes: re-annotate affected categories

---

## 3. Inter-annotator agreement workflow

See [`evaluation-and-validation.md`](evaluation-and-validation.md) for metric definitions. Operational workflow:

### Pilot phase (small N)

- 2-3 annotators annotate the same 20-30 cases independently
- Compute kappa per attribute
- Hold a calibration meeting; resolve disagreements; update guidelines
- Iterate until kappa ≥ 0.70

### Production phase (larger N)

- Single-annotator throughput on most cases
- Double-annotate 10-15% of cases as ongoing IAA check
- Adjudicator resolves disagreements; updates guidelines as patterns emerge
- Drift signal: if rolling 30-day kappa drops below 0.65, pause and re-calibrate

### Adjudication

- Adjudicator is a senior clinical SME (typically RN with HEDIS specialty or MD)
- Adjudicator's decision becomes gold
- Track adjudication rationale; recurring patterns drive guideline edits

---

## 4. Synthetic data generation

When real PHI is unavailable or risky to use for development, synthetic notes are essential.

### Synthesis approaches

| Approach | Strengths | Weaknesses |
|---|---|---|
| Hand-written by clinicians | High realism, full control over edge cases | Slow, expensive |
| Template-based with parameterized fields | Fast, covers many measure scenarios | May lack realistic linguistic variability |
| LLM-generated from prompts | Fast, varied | Risk of hallucinated medical content; must be clinician-reviewed |
| De-identified real data | Realistic, in-distribution | Compliance burden; residual re-identification risk |

### Guidelines for synthetic notes used as gold

- Always clinician-reviewed before adding to gold corpus
- Cover edge cases explicitly: copy-forward, OCR-style noise, telehealth, outside-records, negation, refusal, sub-indicator confusion
- Include both positive (numerator-satisfying) and negative (numerator-failing) cases per measure
- Tag synthetic vs real provenance; report metrics separately when feasible
- Do not mix real PHI into synthetic corpus; keep clearly separated

### De-identification of real data (when used)

- HIPAA Safe Harbor: remove 18 categories of identifiers
- Expert Determination: a qualified statistician certifies low re-identification risk
- Date shifting: preserve relative dates; obscure absolute dates (be careful - HEDIS evaluation often requires accurate dates relative to MY)
- Free-text de-identification: requires NLP-based identifier detection plus manual review

---

## 5. Annotation tooling considerations

You will need a tool that supports:

- Multi-user collaboration with role-based access
- Span annotation with attributes (not just labels)
- Nested / overlapping spans
- Pre-annotation (model-suggested spans for reviewer acceleration)
- IAA computation built-in or exportable
- Export to standard formats (JSON, BRAT, CoNLL)
- Audit trail (who annotated, when, what changed)
- Document-level metadata fields beyond span annotations
- Compliance features (PHI access logs, BAA-eligible vendor)

Common tools (vendor-neutral mention; not endorsements):

- INCEpTION
- BRAT
- Prodigy
- Doccano
- LabelStudio
- Tagtog
- Vendor-built or in-house tools (common at large health systems)

Document your tool's quirks (boundary handling, attribute schema flexibility, IAA computation method) so they're reproducible.

---

## 6. Common annotation pitfalls

- **Annotators overfit to template language.** They learn that "BMI: 22 (BMI %ile: 65)" satisfies WCC-BMI; they miss "growth chart updated, BMI 22 at 65th percentile" because the surface form differs. Mitigate with diverse examples in training.
- **Compliance vs documentation conflation.** Annotators sometimes mark "should be compliant if the doc were better" instead of "is compliant per current spec." Anchor every annotation in the spec's actual wording.
- **Date defaulting.** Annotators copy note-date as date-of-service without checking for explicit result-date in narrative. Reinforce: date attribution is a primary annotation decision.
- **Assertion under-tagging.** "PMH of diabetes" gets tagged the same as "diabetes today" because the historical context is not noticed. Make assertion tagging mandatory, not optional.
- **Sub-indicator confusion.** COA-Med Review vs MRP, TRC sub-indicators, PPC-Prenatal vs PPC-Postpartum. Reinforce sub-indicator identification as a separate decision.
- **Provider-role guessing.** When the note doesn't specify, annotators guess. Make `unknown` a valid label and require evidence for any role assignment.
- **Refusal nuance.** "Patient declined" needs context: what was declined, when, by which provider, for which measure. Tag refusals fully or not at all.
- **Inferred dates.** Annotators sometimes write derived dates ("2 weeks ago = 2024-03-15") that may not be auditable. Capture the original phrase and the derivation rationale; mark date_confidence accordingly.
- **Outside-record confusion.** Annotators may tag the import-date as date-of-service. Reinforce: extract from document body, not the import metadata.
- **Negation scope errors.** "No diabetes, hypertension, or obesity" - annotators sometimes flip the negation on only the first concept. Train on coordinated negation patterns.

---

## 7. Guideline-maintenance lifecycle

Annotation guidelines are living documents.

- Version the guideline; tag each version with the date and the team that approved it
- Every adjudicated disagreement may produce a guideline edit
- Re-baseline IAA after any non-trivial edit
- Re-annotate affected categories if the edit changes the gold for past cases
- Document the spec MY the guideline targets; revise annually

---

## 8. Cross-references

- [`evaluation-and-validation.md`](evaluation-and-validation.md) - how to use the gold to evaluate models
- [`extraction-patterns.md`](extraction-patterns.md) - upstream extraction patterns annotators should be aware of
- [`date-of-service.md`](date-of-service.md) - date-attribution conventions
- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion tagging conventions
- [`../hedis/`](../hedis/) - per-measure cards with measure intent
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - provenance and MRRV
- [`../../templates/per-measure-model-card.md`](../../templates/per-measure-model-card.md) - canonical per-measure documentation
- [`test-fixtures/README.md`](test-fixtures/README.md) - synthetic fixtures (annotation starter set)
