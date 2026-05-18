# Changelog

All notable changes to this skill are documented here.
This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed - Repository restructure: monorepo of three skills

- Split the single skill into three independently installable skills under one repo:
  - `medical-chart-review/` - auditor / clinician / coder / CDI / quality-auditor skill (unchanged scope)
  - `hedis-nlp/` - per-measure HEDIS extractor engineering (cross-cutting NLP + 24 measure cards + model card + abstraction template)
  - `hcc-nlp/` - HCC / risk-adjustment extractor engineering (CMS-HCC V28 / V24 / HHS-HCC + MEAT + hierarchies + RADV + per-HCC cards + test fixtures + model card + NLP-assisted audit template)
- All moves performed with `git mv` to preserve file history.
- Each skill has its own `SKILL.md` with an embedded §0 PHI / scope safety gate. Splitting the safety gate across skills is non-negotiable - if a skill is installed alone, its gate must still run.
- New root `README.md` is the umbrella; per-skill `README.md` files cover install + layout + scope for each.
- `templates/hcc-audit.md` split into two:
  - Lean auditor version in `medical-chart-review/templates/hcc-audit.md` (no NLP-assisted fields, matches pre-NLP-v3 form)
  - NLP-assisted version in `hcc-nlp/templates/hcc-audit-nlp.md` (model version, MEAT evidence, hierarchy application, reviewer-override feedback)
- Cross-skill markdown links converted to prose pointers (e.g., "see the sibling `hcc-nlp` skill's `references/foo.md`") so each skill works standalone.
- HEDIS / HCC NLP triggers removed from the auditor skill's `SKILL.md` description; matching triggers added to the two new SKILL.md files.
- Future planned skill: `hipaa-compliance/` as a 4th sibling (BAA review, breach response, OCR audit prep, de-identification methodology, technical safeguards for any healthcare app).
- **No backward compatibility shims.** Existing installs that referenced the flat layout must reinstall against the new subpath (`Yar177/medical-chart-review-skill/<skill-name>`).

### Added - HCC / risk-adjustment NLP enablement (v3)

- New `references/hcc/` directory packaging chart-review knowledge for data-science / NLP teams building HCC extraction pipelines (suspect engines, validate engines, RAF estimation, RADV preparation):
  - `README.md` — audience, file index, core principles, library landscape, cross-links to the HEDIS NLP parallel.
  - `model-versions.md` — CMS-HCC V28 / V24 / HHS-HCC comparison, phase-in schedule (33/67/100% blend), what changed V24 → V28 (~2,000 codes removed), version-pinning required metadata.
  - `raf-calculation.md` — RAF formula (demographic + HCC + interactions + segment adjustment), disease-disease interactions (DM+CHF, DM+Renal, CHF+COPD, Cancer+Immune), calendar reset, payment-year vs service-year, dollar-weighted metrics.
  - `meat-criteria.md` — MEAT as a separate NLP task with two-pass architecture, per-category detection patterns (Monitor / Evaluate / Assess / Treat), linkage problem with worked examples, section-aware MEAT table, common failure modes.
  - `hierarchies.md` — within-family trumping (HCC 17 > 18 > 19 diabetes example), hierarchies as a post-extraction step (not in extractor), HHS-HCC separate hierarchies, hierarchy-aware metric computation, enforcement checklist.
  - `date-of-service.md` — 5-part DoS contract, calendar-year reset, acceptable encounter settings whitelist, provider-type whitelist (MD/DO/NP/PA/CNS/CNM acceptable; resident-alone / scribe / RN / therapist not), telehealth post-COVID narrowing, AWV recapture trap, copy-forward DoS attribution rule.
  - `negation-and-assertion.md` — 9-dimension assertion taxonomy, history-of as the #1 RADV finding with trigger phrases and disambiguation, Z-code family table (Z85/86/87 generally not HCCs; Z89/93/94/99 subset ARE; Z95.x cardiac implants do not imply current disease), family-history confusion, hedging asymmetry, section-aware priors, audit-ready assertion YAML record.
  - `extraction-patterns.md` — suspect vs validate pipeline split, two-pass extraction architecture, provenance requirements, problem-list-only invalid, RxNorm medication signals, cross-encounter context, common architecture mistakes.
  - `terminology-mapping.md` — terminology systems table, CMS source URLs, ICD-10 → HCC crosswalk structure, annual update cadence, SNOMED bridge gotchas, RxNorm drug-class-to-diagnosis table, LOINC for MEAT evaluation, BMI / pressure-ulcer joint-requirement rules, version-pinning checklist.
  - `evaluation-and-validation.md` — units of analysis (span / encounter-HCC / member-year-HCC / RAF), validate vs suspect engine metric requirements, hierarchy-aware metrics, dollar-weighted RAF precision / recall, decomposed error types, gold-standard construction, internal RADV simulation pattern, drift monitoring.
  - `annotation-guidelines.md` — annotator profiles (clinical + coder + adjudicator), per-encounter YAML annotation schema, span / assertion / MEAT linkage rules, hierarchy convention, IAA targets by dimension, adjudication workflow with rationale feedback loop.
  - `compliance-and-enforcement.md` — RADV / OIG / FCA regime overview, recent settlement patterns, RADV operational mechanics, two-way review obligation, precision targets for auto-validation (>0.97), CDI / provider-query workflow, NLP practices that increase vs reduce risk, escalation triggers.
  - `cards/` — 9-section exemplar HCC cards (identity / clinical definition / eligibility / required MEAT / DoS rule / hierarchy interaction / assertion pitfalls / status-code conflations / NLP extraction notes) for HCC 18 (diabetes w/ complications), HCC 22 (morbid obesity), HCC 85 (CHF), HCC 96 (specified arrhythmias), HCC 108 (vascular disease), HCC 111 (COPD).
  - `test-fixtures/` — synthetic note + expected-extraction pairs for the highest-volume failure modes: history-of trap, hierarchy collapse, status-code amputation, MEAT gap, problem-list-only.
- New `templates/hcc-model-card.md` — canonical YAML + Markdown per-HCC model card (YAML authoritative; stricter required-field discipline than HEDIS due to RADV exposure).
- `templates/hcc-audit.md` expanded with NLP-assisted fields: model version, HCC crosswalk version, emission type, confidence, extracted span, attributed DoS, attributed assertion, MEAT evidence captured, MEAT linkage method, hierarchy application, candidate-log entry, reviewer override, override direction and reason. Adds an NLP pipeline feedback section that loops overrides back into the failure-mode catalog and regression-fixture set.
- `references/coding-icd10-hcc.md` adds a cross-link header pointing NLP teams to `references/hcc/`; auditor-oriented content unchanged.
- `SKILL.md` and `README.md` updated to surface the HCC NLP enablement directory and data-science audience parallel to the HEDIS section.

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
