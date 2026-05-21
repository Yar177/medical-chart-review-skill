# Versioning and drift

> **Why this file exists:** Every code system in this skill has a **release cadence**. Pipelines that ignore this drift silently break, produce non-reproducible analytics, or quietly misrepresent claims over time. Versioning is not glamorous; it is what separates a healthcare data team that can defend its numbers from one that cannot.

## 1. Release cadence cheat sheet

| Code system | Owner | Cadence | Effective date |
|---|---|---|---|
| **ICD-10-CM** | NCHS / CMS | Annual | October 1 (FY) |
| **ICD-10-PCS** | CMS | Annual | October 1 (FY) |
| **CPT** | AMA | Annual (main) + interim | January 1 (main), Jul + Oct (interim) |
| **HCPCS Level II** | CMS | Quarterly | Jan 1, Apr 1, Jul 1, Oct 1 |
| **NDC Directory** | FDA | Continuous | Daily / weekly refresh |
| **RxNorm** | NLM | Monthly | First Monday |
| **SNOMED CT International** | SNOMED Int'l | Biannual | April 1, October 1 |
| **SNOMED CT US Edition** | NLM | Biannual | March 1, September 1 |
| **LOINC** | Regenstrief | Biannual | ~June, ~December |
| **CVX (vaccines)** | CDC | Event-driven | As vaccines licensed |
| **NUCC Taxonomy** | NUCC | Semi-annual | April, October |
| **NPPES NPI file** | CMS | Monthly | Beginning of month |
| **DRG (MS-DRG)** | CMS | Annual | October 1 (FY) |
| **APR-DRG** | 3M | Annual | Varies by 3M release |
| **APC** | CMS | Annual | January 1 (CY) |
| **CCSR** | AHRQ | Annual | Aligned with ICD-10-CM |
| **AHRQ Elixhauser** | AHRQ | Annual | Aligned with ICD-10-CM |
| **CMS-HCC** | CMS | Annual | Payment year |
| **HHS-HCC** | CMS CCIIO | Annual | Payment year |
| **NCQA HEDIS value sets** | NCQA | Annual | Per Measurement Year |
| **VSAC expansions** | NLM | On-demand + scheduled | As underlying code systems update |
| **NCCI edits** | CMS | Quarterly | Jan 1, Apr 1, Jul 1, Oct 1 |
| **BETOS 2.0** | CMS | With HCPCS cycle | Quarterly |
| **CDT (dental)** | ADA | Annual | January 1 |
| **DEA Schedule changes** | DEA | Event-driven | As scheduled |

## 2. Effective-date vs received-date

Two distinct time concepts:

- **Effective date**: the date the code was valid for use in clinical / billing reality (date of service, date of birth, prescription fill date).
- **Received date / processed date**: when the claim, message, or record arrived in the warehouse.

A claim with a **DOS in FY2023** received in FY2024 must be coded against **FY2023 ICD-10-CM**, not the current vintage. Pipelines that always join against "current" code-system tables silently mis-validate retroactive claims.

A code-system table in a warehouse should always include:

- `code`
- `code_system_version` (e.g., `icd10cm_fy2024`)
- `effective_from` / `effective_to`
- `description` (the textual description for that version)

And join logic must use the **DOS-appropriate version**, not the current version.

## 3. As-of snapshots and longitudinal data

For multi-year longitudinal analytics, three strategies:

### A) Pinned to historical code-system version per period

Each year's data is processed against the code-system version effective during that year. Joins are **temporal** - join on code AND effective-date range.

**Pros**: highest fidelity. Reproduces what providers / payers were operating against.

**Cons**: complex queries; cross-year aggregation requires a unifying concept (grouper or crosswalk).

### B) Forward-translated to current

Historical codes are translated forward (via GEMs for ICD-9 → ICD-10, via CCSR / HCC for grouping) to current vintage; all analytics run against current.

**Pros**: simple queries; everyone speaks one language.

**Cons**: information loss at the translation step; the forward translation cannot recover detail that didn't exist in the source (e.g., laterality added in ICD-10 isn't reverse-derivable from ICD-9).

### C) Forward-translated to a stable concept layer (recommended for ML)

All codes mapped to a stable concept layer (CCSR for diagnoses, RxNorm IN for drugs, NUCC for taxonomy) and analytics operate at that layer. Code-system version still recorded for traceability.

**Pros**: simplest analytics, stable across versions, hides cosmetic code changes.

**Cons**: the choice of concept layer constrains the questions you can answer; granular code-level questions still require the underlying code.

Most production teams use **C** as the analytic default and **A** for any audit / restatement / payment-reconciliation work.

## 4. Restatement risk

When a code system updates (especially **annual ICD-10-CM**, **CMS-HCC model versions**, or **grouper releases**), prior analytic outputs may need restatement:

- Comorbidity counts change as Elixhauser definitions update.
- HCC risk scores change as V24 → V28 transitions.
- HEDIS numerators / denominators change as Measurement Year value sets update.

Restatement protocols:

- **Document the analytic vintage** in every published number ("CCSR v2024.1, ICD-10-CM FY2024 codes").
- **Lock the vintage** for a given reporting cycle; do not silently update mid-cycle.
- **Publish reconciliation** when the vintage changes ("the population's prevalence of CHF moved from 6.3% to 6.7% with the FY2025 ICD-10-CM update because three new heart-failure codes were added; the underlying clinical reality is unchanged").

## 5. Drift monitoring

A monitoring job should run on each code-system release to:

1. **Detect new codes**: codes in the new release but not the prior. Flag for any value-set / grouper / crosswalk impact.
2. **Detect deleted codes**: codes in the prior release but not the new. Flag for any value-set membership; data prior to the deletion date still has these codes.
3. **Detect description changes**: codes whose descriptions changed; rare but happens.
4. **Detect relationship / hierarchy changes**: especially for SNOMED CT, where parent / child relationships can shift.
5. **Detect mapping changes**: when GEMs / SNOMED↔ICD / NDC↔RxNorm updates change existing mappings.

The output is a **drift report**: net additions / deletions / changes per code system per release.

See [`../templates/code-drift-monitoring.md`](../templates/code-drift-monitoring.md).

## 6. ICD-10-CM annual update example

A typical October 1 release adds ~200-500 new codes, retires a small number, and may revise descriptions.

What can break:

- **HCC mapping**: a new diagnosis may be HCC-eligible (boosts RAF scores in the new year vs the prior).
- **CCSR / Elixhauser mapping**: a new code may not yet have a CCSR / Elixhauser categorization; the grouper authoritative release lags by 1-3 months.
- **Value set expansions**: VSAC and NCQA value sets are republished with each new MY to incorporate the new codes.
- **Custom crosswalks**: new codes have no row in the team's custom mappings; need triage and addition.

Plan: monitor October 1, publish a drift report by mid-October, update HCC / CCSR / Elixhauser packages as their releases drop, refresh value-set expansions, triage custom crosswalks within 30 days.

## 7. RxNorm monthly drift example

Each monthly release brings:

- New drugs (rare ingredients monthly; new formulations and brands frequently).
- New NDCs as labelers register / repackage / launch products.
- Deprecations and historical-association updates.

What can break:

- **Pharmacy claims with brand-new NDCs** fail to join.
- **Adherence / utilization metrics** for new drugs require knowledge of the new RxCUI's TTY position.

Plan: monitor monthly; auto-refresh the NDC→RxCUI table; alert on unmapped NDC volume in claim feeds.

## 8. CPT annual + interim update example

- **January 1**: main release.
- **July 1**, **October 1**: interim releases for emerging clinical needs (most notably during COVID).
- New CPTs may be Cat I, Cat II, or Cat III; Cat III may later promote to Cat I (different code).

What can break:

- **HEDIS / quality measure** value sets that enumerate CPTs need refresh.
- **Custom service-line groupers** need new-code triage.
- **NCCI PTP edits** include the new CPTs in new code-pair edits; claim-edit pipelines must update.

## 9. Recommended posture

1. **Pin everything**. Every published number has an associated code-system vintage; every grouper version; every value set version.
2. **Monitor every release**. Automated drift report; manual triage of high-impact items.
3. **Refresh on a documented schedule**. Tied to release dates plus a grace period.
4. **Hold the vintage for a reporting cycle**. Do not silently update within a cycle.
5. **Publish reconciliation** when vintage changes.
6. **Archive prior vintages**. The data warehouse must support multi-vintage queries.

## 10. Common pitfalls

- **"Current" code-system table joined to historical claims**. Misses codes valid at DOS but retired since.
- **Single-vintage warehouse**. No way to reproduce prior analyses.
- **Mid-cycle vintage updates** that silently change reporting numbers.
- **No drift monitoring**. The team learns about new codes when a downstream user complains.
- **Vendor-supplied groupers / crosswalks** trusted without version provenance.
- **NCQA HEDIS MY confusion**: MY2024 value sets vs MY2025 vs the actual data vintage they evaluate.
- **HCC V24 / V28 phase-in** ignored. Payment year matters; phase-in years require **blended** model use.
- **Holiday season releases**: ICD-10-CM Oct 1, HCPCS Oct 1, CCSR / Elixhauser Oct-Dec lag, value-set republication all collide; expect a busy fourth-quarter cycle.
- **Forward-translation losses**: ICD-9 → ICD-10 via GEMs loses detail that was never in ICD-9; backward-translation loses ICD-10 detail. Document which direction is authoritative for each use case.
- **Vintage tags missing from published outputs**. Numbers without vintage tags cannot be defended or reproduced.
