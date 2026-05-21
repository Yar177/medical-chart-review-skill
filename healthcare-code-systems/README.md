# healthcare-code-systems

A skill for data engineers, data scientists, NLP engineers, and anyone working with healthcare data. Covers the standardized code systems that underpin every US healthcare pipeline (claims, EHR, risk, quality, analytics, ML): ICD, CPT, HCPCS, SNOMED CT, LOINC, RxNorm, NDC, NPI, plus the value sets, crosswalks, and groupers built on top of them. **Not for clinical NLP extraction** (use [`hcc-nlp`](../hcc-nlp/), [`hedis-nlp`](../hedis-nlp/)). **Not for measure logic or chart review** (use [`hedis-nlp`](../hedis-nlp/), [`medical-chart-review`](../medical-chart-review/)).

> ⚠️ Outputs are reference and tooling guidance, not certified coding or terminology services. Choices that drive submitted claims, risk-adjustment payment, or reported quality metrics require sign-off from credentialed coders (CPC/CCS/CRC), clinical informaticists, or NCQA-certified auditors. Several code systems have licensing constraints (CPT/AMA, UMLS, commercial drug DBs) that affect redistribution.

## What this skill provides

- **Per-system references** in [`references/`](references/) covering structure, semantics, conventions, version cadence, authoritative source, and common pitfalls for every code system you'll encounter in US healthcare data:
  - Diagnosis: ICD-10-CM, ICD-10-PCS, ICD-9-CM (legacy)
  - Procedures and services: CPT (Cat I/II/III + modifiers), HCPCS Level II
  - Institutional billing: revenue codes, type of bill, POS, MS-DRG, APR-DRG, APC
  - Clinical content: SNOMED CT, LOINC, UCUM
  - Pharmacy: RxNorm, NDC (10 vs 11 digit), ATC, commercial drug DBs
  - Other: CVX, MVX, race/ethnicity, HL7 v2 code systems
  - Provider: NPI, NPPES, taxonomy codes, TIN semantics
- **Cross-system infrastructure**:
  - Crosswalks: GEMs (ICD-9↔10), NDC↔RxNorm, ICD↔SNOMED, LOINC↔CPT, ICD-10→HCC, HCC↔HHS-HCC
  - Value sets: VSAC, OIDs, intensional vs expansion, NCQA value set directory, ECL for SNOMED
  - Code groupers: CCSR, CCS (legacy), Elixhauser, Charlson, CCI/NCCI, BETOS, AHRQ groupers
- **Operational guidance**:
  - Version cadences (ICD-10 Oct 1 annual, HCPCS quarterly, CPT Jan 1, RxNorm monthly, SNOMED semi-annual, LOINC semi-annual)
  - Longitudinal-data handling (restatement windows, retroactive code mapping, "as-of" code snapshots)
  - Source files and licensing (CMS, NLM/UMLS, AMA, FDA, NCQA, NCPDP)
  - Common pitfalls (truncated NDCs, ICD-10 decimal handling, Z-code traps, modifier loss, status-code conflation)
- **Templates** in [`templates/`](templates/):
  - `code-system-inventory.md` - catalog every code system in your warehouse with version, source, owner, and downstream consumers
  - `crosswalk-spec.md` - declarative spec for a custom crosswalk with cardinality, fallback, and QA
  - `value-set-manifest.md` - declarative value-set definition with provenance and version
  - `code-drift-monitoring.md` - monitoring plan for code-system release events
  - `grouper-evaluation.md` - structured evaluation for picking a comorbidity / utilization grouper

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill healthcare-code-systems
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## When the agent loads it

Triggered by requests like:

- "Explain the structure of ICD-10-CM"
- "What does CPT modifier -25 mean?"
- "Look up HCPCS J3490"
- "Crosswalk NDC 00378-0181-01 to RxNorm"
- "ICD-9 to ICD-10 with GEMs"
- "Build a value set for diabetes"
- "What's the VSAC OID for ACEi/ARB?"
- "Pick a comorbidity grouper for our cost model"
- "Elixhauser vs Charlson for readmission risk"
- "Manage code version drift across our warehouse"
- "Why is my NDC join missing - 10 vs 11 digit?"
- "Inventory the code systems in our claims warehouse"
- "Spec a custom ICD-10 to internal-category crosswalk"
- "CPT licensing for an open-source repo"
- "Where do I get the current ICD-10-CM file?"

Not triggered for: clinical NLP extraction (`hcc-nlp`, `hedis-nlp`), HEDIS measure logic (`hedis-nlp`), chart review (`medical-chart-review`), HIPAA compliance (`hipaa-compliance`), supervised claims ML (`claims-ml`), or FHIR resource modeling.

## Quick start

```text
We're loading 10 years of claims into a new warehouse. The ICD-10 codes span
FY2016 through FY2026. What's the right strategy for storing the code, the
crosswalk, and the value-set definitions so HEDIS and HCC pipelines downstream
get consistent answers?
```

The agent will run the §0 gate from `SKILL.md`, then load [`references/icd10-cm.md`](references/icd10-cm.md), [`references/versioning-and-drift.md`](references/versioning-and-drift.md), [`references/value-sets-and-vsac.md`](references/value-sets-and-vsac.md), and [`templates/code-system-inventory.md`](templates/code-system-inventory.md).

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, task routing |
| [references/](references/) | All code-system reference content (17 files) |
| [templates/](templates/) | Inventory, crosswalk, value-set, drift, grouper templates (5 files) |

## Related skills in this repo

- [`medical-chart-review`](../medical-chart-review/) - auditor / coder oriented chart review. Its `references/coding-icd10-hcc.md` is the auditor-oriented complement to this skill's data-engineering view of the same codes.
- [`hedis-nlp`](../hedis-nlp/) - HEDIS NLP per-measure extraction. Consumes value sets (VSAC OIDs, NCQA value set directory) defined and managed via this skill.
- [`hcc-nlp`](../hcc-nlp/) - HCC NLP per-HCC extraction. Consumes the ICD-10→HCC crosswalk and CMS-HCC model files documented here in [`references/crosswalks.md`](references/crosswalks.md) and [`references/versioning-and-drift.md`](references/versioning-and-drift.md).
- [`claims-ml`](../claims-ml/) - supervised ML on claims. Consumes code groupers (CCSR, Elixhauser, Charlson) documented in [`references/code-groupers.md`](references/code-groupers.md).
- [`hipaa-compliance`](../hipaa-compliance/) - HIPAA compliance for the platform hosting any of the above pipelines.

## Compliance & safety guardrails

- Always pin code-system versions (release date or version label) in any answer or stored artifact
- Always cite the authoritative publisher (CMS, NLM/UMLS, AMA, FDA, NCQA, NCPDP, Regenstrief, SNOMED International) - not a third-party scraped copy
- Surface licensing constraints (CPT/AMA, UMLS, commercial drug DBs) before recommending bulk distribution or embedding
- Never fabricate codes, descriptions, or crosswalk rows; route to primary source when unsure
- Name crosswalk cardinality (1:1, 1:N, N:1, N:M) and unmapped-row strategy explicitly
- Defer to credentialed coders / NCQA-certified auditors / clinical informaticists for choices that affect submitted claims or reported metrics

## Out of scope

- Clinical NLP extraction (use `hcc-nlp` / `hedis-nlp`)
- HEDIS measure logic / CQL authoring
- HCC extraction or RAF calculation (use `hcc-nlp`)
- Chart review (use `medical-chart-review`)
- HIPAA compliance program work (use `hipaa-compliance`)
- Supervised ML on claims (use `claims-ml`)
- FHIR resource modeling, SMART on FHIR, Bulk FHIR (future skill)
- Production ETL code (this skill produces reference + specs)

## License / disclaimer

MIT-licensed agent content. Code systems referenced (ICD-10-CM/PCS, CPT, HCPCS, SNOMED CT, LOINC, RxNorm, NDC, etc.) are owned by their respective publishers and subject to their own licenses. This skill does not redistribute any code-system file; it explains structure, points at authoritative sources, and surfaces licensing constraints.
