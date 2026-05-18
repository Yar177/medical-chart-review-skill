# Changelog

All notable changes to this skill are documented here.
This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added - NLP-team enablement (v2)

- New `references/nlp/` directory packaging chart-review knowledge for data-science / NLP teams building per-measure HEDIS extractors:
  - `date-of-service.md` — DoS taxonomy, anchor selection, copy-forward handling, measure × DoS-rule grid for all 24 measures, worked test cases.
  - `negation-and-assertion.md` — ConText 4-dimension framework, OSS library landscape (medspaCy, negspacy, pyConTextNLP, NegBio, scispaCy, HeidelTime, SUTime, Apache cTAKES, CLAMP), shared HEDIS anti-patterns, measure × pitfall grid, worked test cases.
  - `extraction-patterns.md` — section detection and EHR-vendor variants, abbreviation disambiguation, copy-forward detection, **telehealth** (modality classifier, CPT 95, POS 02/10), **outside-records / scanned PDFs** (CCDA, HIE, OCR, provenance fields), provider attribution, multi-document linking, doc-type classification.
  - `terminology-mapping.md` — code systems (LOINC / SNOMED / RxNorm / NDC / CVX / CPT / HCPCS / ICD-10-CM/PCS / POS / NUCC), per-measure-family mapping, common pitfalls, code-first vs phrase-first guidance.
  - `evaluation-and-validation.md` — span / document / patient-level metrics, DoS-aware metrics (concept + date + assertion all correct), IAA (Cohen / Fleiss kappa, target ≥ 0.70), MRRV simulation with failure-rate thresholds, downstream measure-rate sensitivity, failure-mode catalog template, drift monitoring playbook.
  - `annotation-guidelines.md` — span types, attribute schema, boundary conventions, annotator profiles (CCS / CPC / CRC coders, RN HEDIS abstractors, clinical informaticists, NLP engineers), IAA workflow, synthetic-data approaches, tooling (INCEpTION, BRAT, Prodigy, Doccano, LabelStudio, Tagtog), 10 common annotation pitfalls.
  - `test-fixtures/` — synthetic note + expected-extraction YAML pairs for GSD copy-forward, CCS patient-report, FUH calendar-day, MRP boilerplate, PPC postpartum window, WCV sports-physical, ACP brochure-vs-discussion.
- New `templates/per-measure-model-card.md` — canonical YAML schema + Markdown narrative for documenting per-measure extractors (YAML is authoritative on conflict). Cross-linked from `templates/hedis-abstraction.md` NLP-assisted abstraction section.
- All 24 measure cards in `references/hedis/` now include:
  - A `## Date of service rule` section with anchor event, compliance window, date types that count / do not count, "most recent" disambiguation, look-back / look-forward, and common date confusions.
  - An `**Assertion / negation pitfalls**` block replacing the prior `**False positives to filter**` block, with ConText-dimension labels (negation, hypothetical / future intent, historical, experiencer).
  - Cross-links to `references/nlp/date-of-service.md` and `references/nlp/negation-and-assertion.md`.
- `references/hedis/README.md` card structure expanded from 7 to 9 sections.
- `SKILL.md` and `README.md` updated to surface the NLP enablement directory and data-science audience.

## [0.1.0]

### Added
- Initial public release.
- `SKILL.md` with safety/PHI gate, 8 review-type router, on-demand reference loading.
- References: `chart-structure`, `note-types`, `coding-icd10-hcc`, `coding-cpt-drg`, `quality-measures`, `medications`, `labs-imaging`, `red-flags`, `abbreviations`, `hipaa-privacy`, `provider-queries`.
- Templates: `clinical-summary`, `cdi-review`, `hcc-audit`, `quality-gap`, `med-rec`, `utilization-review`, `coding-audit`, `data-abstraction`.
