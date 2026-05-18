# medical-chart-review

An AI agent skill for expert-level review of medical charts, EMRs, and EHRs. Designed for documentation review, coding/quality auditing, and clinical data abstraction — **not** for direct patient care.

> ⚠️ This skill produces documentation analysis, not medical advice. Final clinical, coding, and compliance decisions require credentialed humans (physicians, CCS/CPC/CRC coders, CCDS specialists).

## Install

This skill follows the [Agent Skills](https://agentskills.io/) open standard. It works in **Claude Code**, **GitHub Copilot** (VS Code, CLI, cloud agent), **Cursor**, **Codex**, **Windsurf**, **Gemini**, **Cline**, and other skills-compatible agents.

### Recommended: one-line install via `skills.sh`

```bash
npx skills add Yar177/medical-chart-review-skill
```

This auto-detects your agent(s) and drops the skill into the correct directory for each one. No platform-specific paths to remember. See [skills.sh](https://skills.sh) for details.

### Manual install

The folder name must be `medical-chart-review` (it has to match the `name` field in `SKILL.md`).

#### Claude Code

Personal (available in all projects):
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git \
  ~/.claude/skills/medical-chart-review
```

Project-only (commit alongside the repo):
```bash
mkdir -p .claude/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git \
  .claude/skills/medical-chart-review
```

#### GitHub Copilot (VS Code, CLI, cloud agent)

Personal (available in all workspaces):
```bash
mkdir -p ~/.copilot/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git \
  ~/.copilot/skills/medical-chart-review
```

Project-only (commit alongside the repo):
```bash
mkdir -p .github/skills
git clone https://github.com/Yar177/medical-chart-review-skill.git \
  .github/skills/medical-chart-review
```

In VS Code, the skill appears as `/medical-chart-review` in the chat slash-command menu and is also auto-loaded when your prompt matches the description.

### Verify it loaded

- **Claude Code**: ask *"What skills do you have available?"* or type `/medical-chart-review`.
- **VS Code Copilot**: open the Chat view → Configure Chat (gear icon) → Skills tab. Or type `/` in chat and look for `medical-chart-review`.

## Quick start

Once installed, try one of these prompts:

> *"I want to do an HCC audit on a synthetic patient chart. Walk me through the safety gate first."*

> *"/medical-chart-review summarize this discharge summary"* *(paste de-identified or synthetic chart text)*

The agent will run the PHI/scope check from `SKILL.md` §0, then route to the appropriate template under [templates/](templates/).

## When the agent loads it

Triggered by requests like:
- "review this chart" / "summarize this patient's history"
- "audit these records for HCC capture" / "validate ICD-10 coding"
- "perform a CDI review" / "write a provider query"
- "do a HEDIS gap analysis"
- "reconcile these medications"
- "extract structured data from this note"

**Not** triggered for: live patient care, prescribing, diagnosis of real patients, handling identifiable PHI in non-compliant environments.

## What it does

1. **Safety gate** — confirms PHI status, scope, and disclaimers before reading anything.
2. **Selects a review type** — clinical summary, CDI, HCC audit, HEDIS gap, med rec, utilization review, coding audit, or data abstraction.
3. **Runs a standard workflow** — orient → index → read → cross-reference → apply domain rules → surface findings with citations.
4. **Outputs** a structured report using the matching template.

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point — workflow, safety gates, routing |
| [references/](references/) | Deep domain knowledge, loaded on demand |
| [templates/](templates/) | Output formats, one per review type |

### References (loaded only when needed)

- [chart-structure.md](references/chart-structure.md) — EHR systems (Epic, Cerner, Athena, Meditech) and universal chart sections
- [note-types.md](references/note-types.md) — SOAP, H&P, OLDCARTS/OPQRST, note taxonomy
- [administrative-insurance.md](references/administrative-insurance.md) — face sheet, insurance verification, eligibility on DOS, COB, prior auth, referrals, payer policy basics, denial categories
- [coding-icd10-hcc.md](references/coding-icd10-hcc.md) — ICD-10-CM, MEAT criteria, CMS-HCC, RAF
- [coding-cpt-drg.md](references/coding-cpt-drg.md) — CPT modifiers, E&M 2021+ leveling, MS-DRG
- [quality-measures.md](references/quality-measures.md) — HEDIS, CMS Stars, MIPS
- [medications.md](references/medications.md) — Beers, interactions, polypharmacy, controlled substances
- [labs-imaging.md](references/labs-imaging.md) — Reference ranges, critical values, CKD staging
- [red-flags.md](references/red-flags.md) — Must-not-miss patient-safety findings
- [abbreviations.md](references/abbreviations.md) — Clinical shorthand + JCAHO Do-Not-Use list
- [hipaa-privacy.md](references/hipaa-privacy.md) — 18 Safe Harbor identifiers, 42 CFR Part 2
- [provider-queries.md](references/provider-queries.md) — Compliant ACDIS/AHIMA query templates
- [hedis/](references/hedis/) — Per-measure cards (denominator, numerator, exclusions, NLP signal phrases, **date-of-service rule**, **assertion / negation pitfalls**)
- [hedis-supplemental-data.md](references/hedis-supplemental-data.md) — Standard / non-standard supplemental data, hybrid sampling, MRRV
- [nlp/](references/nlp/) — **NLP-team enablement (HEDIS)**: date of service, assertion / negation, extraction patterns, terminology mapping, evaluation methodology, annotation guidelines, test fixtures
- [hcc/](references/hcc/) — **NLP-team enablement (HCC / risk adjustment)**: model versions (V28 / V24 / HHS-HCC), RAF calculation, MEAT, hierarchies, date of service, assertion / negation, extraction patterns, terminology mapping, evaluation, annotation, compliance, test fixtures, per-HCC cards

### Templates

[clinical-summary.md](templates/clinical-summary.md) · [hcc-audit.md](templates/hcc-audit.md) · [cdi-review.md](templates/cdi-review.md) · [quality-gap.md](templates/quality-gap.md) · [med-rec.md](templates/med-rec.md) · [utilization-review.md](templates/utilization-review.md) · [coding-audit.md](templates/coding-audit.md) · [data-abstraction.md](templates/data-abstraction.md) · [hedis-abstraction.md](templates/hedis-abstraction.md) · [per-measure-model-card.md](templates/per-measure-model-card.md) · [hcc-model-card.md](templates/hcc-model-card.md)

## For data-science / NLP teams

If you are building per-measure HEDIS extractors (e.g., GSD, BCS-E, FUH, MRP, TRC), start in [references/nlp/](references/nlp/). It packages the chart-review knowledge here into model-friendly form for the two highest-impact failure modes in production HEDIS NLP:

- **Date of service** ([references/nlp/date-of-service.md](references/nlp/date-of-service.md)) — DoS taxonomy, anchor selection, copy-forward handling, measure × DoS-rule grid for all 24 measures, worked test cases.
- **Assertion / negation** ([references/nlp/negation-and-assertion.md](references/nlp/negation-and-assertion.md)) — ConText 4-dimension framework, OSS library landscape (medspaCy, negspacy, pyConTextNLP, NegBio, scispaCy, HeidelTime, SUTime, cTAKES, CLAMP), shared HEDIS anti-patterns, measure × pitfall grid, worked test cases.

Supporting files cover extraction patterns (sections, abbreviations, copy-forward, telehealth, outside records / OCR, provider attribution), terminology mapping (LOINC / SNOMED / RxNorm / NDC / CVX / CPT / HCPCS / ICD-10), evaluation methodology (span / document / patient-level metrics, IAA, MRRV simulation, failure-mode catalog, drift monitoring), annotation guidelines, and synthetic test fixtures. Use [templates/per-measure-model-card.md](templates/per-measure-model-card.md) as the canonical model documentation per extractor.

Each HEDIS measure card in [references/hedis/](references/hedis/) also has its own **date-of-service rule** and **assertion / negation pitfalls** sections.

## For HCC / risk-adjustment NLP teams

If you are building HCC extraction pipelines (suspect engines, validate engines, RAF estimation, RADV preparation), start in [references/hcc/](references/hcc/). It packages the same chart-review knowledge into model-friendly form for the HCC-specific failure modes that drive RADV findings and One Touch / two-way review obligations:

- **Model versions** ([references/hcc/model-versions.md](references/hcc/model-versions.md)) — CMS-HCC V28 / V24 / HHS-HCC differences, phase-in schedule, what changed V24 → V28, version-pinning requirements per artifact.
- **MEAT criteria** ([references/hcc/meat-criteria.md](references/hcc/meat-criteria.md)) — MEAT as a separate NLP task with two-pass architecture, per-category detection patterns, linkage, section-aware MEAT, common failure modes.
- **Hierarchies** ([references/hcc/hierarchies.md](references/hcc/hierarchies.md)) — within-family trumping as a post-extraction step, HHS-HCC differences, hierarchy-aware metrics.
- **Negation & assertion** ([references/hcc/negation-and-assertion.md](references/hcc/negation-and-assertion.md)) — 9-dimension assertion taxonomy, history-of (the #1 RADV finding), Z-code family disambiguation (Z85/86/87 not HCCs; Z89/93/94/99 subset ARE), section-aware priors.
- **Date of service** ([references/hcc/date-of-service.md](references/hcc/date-of-service.md)) — 5-part DoS contract, calendar-year reset, provider-type whitelist, telehealth boundaries, AWV recapture trap, copy-forward attribution rule.
- **Extraction patterns** ([references/hcc/extraction-patterns.md](references/hcc/extraction-patterns.md)) — suspect vs validate split, two-pass architecture, provenance requirements, problem-list-only invalid.
- **Evaluation & validation** ([references/hcc/evaluation-and-validation.md](references/hcc/evaluation-and-validation.md)) — units of analysis (span / encounter-HCC / member-year-HCC / RAF), hierarchy-aware metrics, dollar-weighted RAF precision / recall, decomposed errors, internal RADV simulation.
- **Compliance & enforcement** ([references/hcc/compliance-and-enforcement.md](references/hcc/compliance-and-enforcement.md)) — RADV / OIG / FCA context, two-way review obligation, precision targets for auto-validation, CDI / provider-query workflow.
- **Per-HCC cards** ([references/hcc/cards/](references/hcc/cards/)) — 9-section exemplar cards for HCC 18 (diabetes w/ complications), 22 (morbid obesity), 85 (CHF), 96 (specified arrhythmias), 108 (vascular disease), 111 (COPD).
- **Test fixtures** ([references/hcc/test-fixtures/](references/hcc/test-fixtures/)) — synthetic-note + expected-extraction pairs for the highest-volume failure modes (history-of trap, hierarchy collapse, status-code amputation, MEAT gap, problem-list-only).

Use [templates/hcc-model-card.md](templates/hcc-model-card.md) as the canonical per-HCC model documentation (YAML wins on conflict; stricter required-field discipline than HEDIS due to RADV exposure). Use the expanded [templates/hcc-audit.md](templates/hcc-audit.md) when an HCC chart audit is NLP-assisted; the new NLP fields capture model version, MEAT evidence, hierarchy application, and reviewer overrides for failure-mode feedback.

## Compliance & safety guardrails

The skill enforces:

- **PHI verification** before reading any chart content (Safe Harbor de-identified, synthetic, or BAA-covered environment)
- **No diagnosis / prescribing** for real patients
- **No upcoding** — coding suggestions must be supported by documentation (MEAT)
- **Non-leading provider queries** per ACDIS/AHIMA 2022 Practice Brief
- **No PHI written to agent memory** (session, repo, or user scope)
- **Explicit deferral** to credentialed humans for ambiguous coding, fraud signals, and CMS/RAC/legal submissions

## Customization tips

- Add `references/medicare-advantage.md` or `references/specialty-<X>.md` for domain-specific deep dives
- Add `examples/` with 1–2 walked-through synthetic reviews to anchor the agent's voice
- For organization-specific coding rules or payer policies, add `references/local-policy.md` and reference it in `SKILL.md`
- Update annually — ICD-10-CM guidelines, HCC model versions (v24 → v28 transition), HEDIS measure set, and Beers Criteria all change yearly

## Out of scope

- Real-time clinical decision support
- Prescribing or order entry
- Anything requiring a licensed clinician's signature on the legal record
- Handling identifiable PHI without a confirmed HIPAA-compliant environment

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans before being used for billing, compliance, regulatory submission, or patient care decisions.
