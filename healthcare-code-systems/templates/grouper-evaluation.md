# Grouper evaluation

> Use this template to evaluate and select a code grouper (CCSR, Elixhauser, Charlson, BETOS, APR-DRG, etc.) for a specific analytic purpose. Replace `{{...}}`.

---

## Analytic purpose

- **Question being answered**: {{e.g., "Stratify a cardiovascular cohort by comorbidity burden for a 30-day readmission model"}}
- **Data scope**: {{e.g., inpatient claims, 2019-2024, 1.2M encounters}}
- **Downstream consumer**: {{model | report | cohort definition | dashboard}}
- **Stakeholder**: {{role}}

## Candidate groupers

| Grouper | Type | Output | Licensing | Vintage match |
|---|---|---|---|---|
| **Charlson Comorbidity Index** (Quan ICD-10 adaptation) | Weighted comorbidity index | Single score | Public | Aligns with ICD-10-CM |
| **Elixhauser** (AHRQ refined) | Binary flag panel + van Walraven score | 40+ flags + index | Public | Aligns with ICD-10-CM |
| **CCSR Diagnoses** (AHRQ) | Mutually-exclusive + body-system categories | ~530 categories + multi-cat | Public | Aligns with ICD-10-CM |
| **CMS-HCC (V28)** | Risk-adjustment grouper | ~100 HCCs + RAF | Public (CMS) | Annual payment year |
| **APR-DRG severity / mortality sub-classes** (3M) | Inpatient case-mix | DRG + 4-level severity / mortality | **3M paid license** | Annual |

## Evaluation criteria

| Criterion | Charlson | Elixhauser | CCSR | CMS-HCC | APR-DRG |
|---|---|---|---|---|---|
| **Captures cardiovascular conditions relevantly?** | {{Y/N + note}} | {{Y/N + note}} | {{Y/N + note}} | {{Y/N + note}} | {{Y/N + note}} |
| **Granularity appropriate?** | Coarse (single score) | Mid (40 flags) | Fine (530 cats) | Mid (~100) | Coarse (DRG + sev) |
| **Validated for the target outcome?** | {{citation, fit}} | {{citation, fit}} | {{citation, fit}} | {{citation, fit}} | {{citation, fit}} |
| **Licensing acceptable?** | Yes | Yes | Yes | Yes | {{depends on org license}} |
| **Version cadence matches data refresh?** | Yes | Yes | Yes | Annual payment year | Yes |
| **Implementation burden** | Low | Low | Low | Medium | Medium |
| **Interpretability** | High (single score) | High (per-flag) | Medium (530 cats) | Medium | Medium |
| **Compatible with prior internal use?** | {{Y/N}} | {{Y/N}} | {{Y/N}} | {{Y/N}} | {{Y/N}} |

## Sensitivity test

Run all candidates on a **representative sample** (e.g., 50k encounters) and compare:

- **Distribution of scores / flag counts** per candidate
- **Performance on the target outcome** (AUC for prediction, R² for regression, etc.)
- **Stability** across two time windows (e.g., 2019 vs 2024) to detect coding-style drift

Document results:

| Grouper | Mean output | Distribution shape | AUC on outcome | Stability across years |
|---|---|---|---|---|
| Charlson | {{value}} | {{shape}} | {{value}} | {{value}} |
| Elixhauser (van Walraven) | {{value}} | {{shape}} | {{value}} | {{value}} |
| CCSR multi-cat | {{value}} | {{shape}} | {{value}} | {{value}} |
| CMS-HCC RAF | {{value}} | {{shape}} | {{value}} | {{value}} |
| APR-DRG severity | {{value}} | {{shape}} | {{value}} | {{value}} |

## Decision

**Selected grouper**: {{name}}

**Rationale**: {{2-4 sentences explaining the tradeoff that drove the choice. Explicitly address why the rejected candidates were rejected.}}

**Caveats**:

- {{e.g., "Charlson omits some clinically relevant cardiovascular subtypes; will supplement with custom ICD-10 flags for cardiogenic shock and acute heart failure"}}
- {{e.g., "CMS-HCC was rejected because RAF is payment-tuned and omits some non-payable but clinically relevant comorbidities"}}

## Version pinning

- **Grouper version**: {{e.g., "AHRQ Elixhauser Comorbidity Software v2024.1"}}
- **Underlying code-system version**: {{e.g., "ICD-10-CM FY2024"}}
- **Software / library used**: {{e.g., comorbidity R package v0.5.3, custom SQL implementation, vendor module}}
- **Source file location**: `{{path or URL}}`

## Custom modifications

- [ ] None
- [ ] Custom additions: {{list}}
- [ ] Custom exclusions: {{list}}
- [ ] Custom weighting: {{description}}

**Documentation of modifications**: `{{path}}`

## Validation

- **Sample size**: {{N}}
- **Reviewer**: {{role / name}}
- **Spot-check criteria**:
  - {{e.g., "Random 100 encounters: grouper flags match manual coder review ≥ 95% of the time"}}
  - {{e.g., "Comorbidity prevalence matches published benchmarks within ±10%"}}
- **Outcome**: {{summary}}
- **Sign-off date**: {{YYYY-MM-DD}}

## Re-evaluation triggers

This selection should be revisited if:

- The grouper publisher releases a new major version (e.g., AHRQ refines Elixhauser methodology).
- The underlying code system has a major revision (e.g., ICD-11 adoption).
- The downstream model / report performance degrades materially.
- A new candidate grouper emerges with stronger validation for the target use case.

## Approval

- **Selected by**: {{name}}
- **Reviewed by**: {{name}}
- **Approved by**: {{name}}
- **Date**: {{YYYY-MM-DD}}
- **Next re-evaluation due**: {{YYYY-MM-DD}}
