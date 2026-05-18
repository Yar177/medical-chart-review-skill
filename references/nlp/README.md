# NLP enablement for HEDIS chart-review pipelines

This directory is for **data-science / NLP teams** building per-measure HEDIS extraction models. It packages the chart-review knowledge in the rest of this skill into model-friendly form: shared rules, pitfalls, test fixtures, and evaluation patterns.

The per-measure cards in [`../hedis/`](../hedis/) tell you **what counts** for each measure. The files here tell you **how to extract it reliably** across the two biggest failure modes we see in production: **date of service** and **assertion / negation**.

## Audience

- NLP / ML engineers building HEDIS evidence extractors
- Clinical informaticists annotating training and eval data
- Analytics engineers wiring extractor output into measure pipelines and supplemental-data submissions
- Chart-review SMEs validating model output

## Files

| File | Purpose |
|---|---|
| [`date-of-service.md`](date-of-service.md) | DoS taxonomy, anchor selection, copy-forward handling, measure × DoS-rule grid for all 24 measures, worked test cases |
| [`negation-and-assertion.md`](negation-and-assertion.md) | ConText 4-dimension framework, OSS library landscape, shared HEDIS anti-patterns, measure × pitfall grid, worked test cases |
| [`extraction-patterns.md`](extraction-patterns.md) | *(Phase 3)* section detection, abbreviation expansion, telehealth, outside-records, provider attribution |
| [`terminology-mapping.md`](terminology-mapping.md) | *(Phase 3)* LOINC / SNOMED / RxNorm / CVX / CPT / ICD-10 mapping by measure family |
| [`evaluation-and-validation.md`](evaluation-and-validation.md) | *(Phase 4)* metrics, IAA, MRRV simulation, failure-mode catalog, drift monitoring |
| [`annotation-guidelines.md`](annotation-guidelines.md) | *(Phase 4)* span and attribute schema, adjudication, synthetic data |
| [`test-fixtures/`](test-fixtures/) | *(Phase 4)* synthetic note snippets with expected evidence, DoS, and assertion attributes |

## How to use this directory

1. Read the cross-cutting file for your problem (DoS or negation) first - the shared frameworks save measure-by-measure rework.
2. Open the per-measure card in [`../hedis/`](../hedis/) for measure-specific signals, date rules, and pitfalls.
3. Use the worked test cases as initial regression fixtures.
4. Mirror the per-measure model card template (Phase 4) when documenting your model.

## Library landscape (clinical NLP for negation / assertion / temporality)

Named without version pins on purpose; **verify currency before adoption**:

- **medspaCy** - clinical spaCy components, includes a ConText implementation, target-rule matchers
- **negspacy** - lightweight NegEx-style negation for spaCy pipelines
- **pyConTextNLP** - reference Python implementation of the ConText algorithm
- **NegBio** - rule-based negation and uncertainty for radiology reports
- **scispaCy** - biomedical models (NER, linking to UMLS) for spaCy
- **HeidelTime** - rule-based temporal expression tagger
- **SUTime** - Stanford library for temporal expression extraction
- **Apache cTAKES** - end-to-end clinical NLP (UMLS dictionary lookup, ConText, dependency parser)
- **CLAMP** - clinical NLP toolkit with GUI; ConText built in

Embedding / LLM approaches (zero-shot classifiers, instruction-tuned models on clinical text) can supplement rule-based ConText for harder long-range or implied negation but should never be the sole source for HEDIS evidence without human review. See [`evaluation-and-validation.md`](evaluation-and-validation.md) (Phase 4).

## Core principles

1. **Measure intent first, phrasing second.** Phrase lists drift; the underlying measure definition is the contract.
2. **Capture the source snippet.** NCQA MRRV (Medical Record Review Validation) requires re-findable evidence; see [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md).
3. **Date and assertion are first-class fields.** An A1c value without a date or with the wrong assertion is not evidence.
4. **MY-aware.** Specs change every measurement year. Pin your model to a MY and document the spec version.
5. **Inverse-rate measures exist** (GSD Poor Control, BPD). Numeric extraction must preserve direction; downstream scoring must respect it.

## Out of scope here

- Actual model implementations or training code
- NCQA value sets (proprietary - license required)
- FHIR transformation code
- PHI handling, de-identification, or compliance controls (out of skill scope)
- LLM prompt templates (model-dependent and fast-changing)

## See also

- [`../hedis/README.md`](../hedis/README.md) - per-measure cards
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - provenance and MRRV rules
- [`../../templates/hedis-abstraction.md`](../../templates/hedis-abstraction.md) - abstraction worksheet (has NLP-assisted block)
