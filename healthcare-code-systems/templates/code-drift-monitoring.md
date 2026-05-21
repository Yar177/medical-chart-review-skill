# Code drift monitoring plan

> Use this template to define a monitoring plan for tracking releases / drift of one or more code systems. Replace `{{...}}`.

---

## Scope

- **Code systems monitored**:
  - {{ICD-10-CM, ICD-10-PCS, CPT, HCPCS Level II, NDC, RxNorm, SNOMED CT US Edition, LOINC, CVX, NUCC Taxonomy, CCSR, AHRQ Elixhauser, CMS-HCC, NCQA HEDIS value sets, NCCI edits, BETOS, NPPES NPI, MS-DRG, APC, ...}}
- **Owner**: {{team / individual}}
- **Sponsor**: {{stakeholder}}
- **Frequency**: {{daily / weekly / on-release}}

## Monitoring objectives

1. **Detect** new / deleted / revised codes per release.
2. **Quantify** the impact on warehouse data and downstream consumers.
3. **Trigger** updates to crosswalks, value sets, and groupers.
4. **Alert** stakeholders when material drift requires restatement or process change.

## Release calendar tracking

| Code system | Release cadence | Next expected release | Owner-side action |
|---|---|---|---|
| ICD-10-CM | Annual (Oct 1) | {{YYYY-10-01}} | Refresh table; run drift report by Oct 15 |
| ICD-10-PCS | Annual (Oct 1) | {{YYYY-10-01}} | Refresh table; run drift report by Oct 15 |
| CPT | Annual Jan 1 + interim Jul/Oct | {{YYYY-01-01}} | Refresh table; HEDIS value-set re-expansion |
| HCPCS Level II | Quarterly | {{YYYY-MM-01}} | Refresh table; J-code pricing reconciliation |
| RxNorm | Monthly (first Monday) | {{YYYY-MM-DD}} | Auto-refresh NDC↔RxCUI; alert on unmapped NDC volume |
| SNOMED CT US Edition | Mar 1 / Sep 1 | {{YYYY-MM-01}} | Refresh terminology service; re-expand ECL-based value sets |
| LOINC | Biannual (~Jun, ~Dec) | {{YYYY-MM-DD}} | Refresh table; LOINC↔CPT crosswalk review |
| CVX | Event-driven | (continuous monitoring) | Refresh table; immunization measure value-set review |
| NUCC Taxonomy | Apr / Oct | {{YYYY-MM-DD}} | Refresh table; specialty mapping review |
| NPPES NPI file | Monthly | First-of-month | Auto-refresh; delta load |
| CCSR | Annual (after ICD-10-CM) | {{YYYY-MM-DD}} | Refresh grouper; re-feature-engineer where needed |
| AHRQ Elixhauser | Annual | {{YYYY-MM-DD}} | Refresh grouper; van Walraven recalculation |
| CMS-HCC | Annual (payment year) | {{YYYY-MM-DD}} | Refresh model; check V24/V28 phase-in |
| NCQA HEDIS Value Sets | Annual (per MY) | {{YYYY-MM-DD}} | Refresh value-set artifact; measure logic review |
| NCCI edits | Quarterly | {{YYYY-MM-01}} | Refresh edits; claim-edit pipeline regression test |
| BETOS 2.0 | With HCPCS cycle | {{YYYY-MM-01}} | Refresh service-line groupings |
| MS-DRG | Annual (Oct 1) | {{YYYY-10-01}} | Refresh grouper; inpatient case-mix review |
| APC | Annual (Jan 1) | {{YYYY-01-01}} | Refresh grouper; outpatient case-mix review |

## Detection logic

For each release:

1. **Download** new vintage to staging.
2. **Diff against current vintage** in warehouse on `code` (left/right anti-joins).
3. **Categorize**:
   - **Added**: in new, not in current.
   - **Deleted**: in current, not in new.
   - **Description changed**: present in both, description differs.
   - **Hierarchy / mapping changed** (SNOMED, GEMs, NDC↔RxCUI, etc.): present in both, relationships / target differs.
4. **Quantify**: count per category.
5. **Sample**: pull 10-20 representative changes for human review.

## Impact analysis

For each release, compute:

- **Warehouse row exposure**: how many recent fact rows reference the deleted / changed codes?
- **Value set exposure**: which value sets include any of the deleted / changed codes? (FK lookup)
- **Crosswalk exposure**: which crosswalks have source / target rows that involve any of the changes?
- **Grouper exposure**: which groupers' membership shifts?
- **Downstream consumer count**: number of pipelines / reports / models affected.

## Alerting

| Severity | Trigger | Recipients | Response time |
|---|---|---|---|
| **Critical** | New HCC-eligible diagnosis affecting risk scores; deleted code in active use | {{role}} | Same day |
| **High** | Material value-set composition change in production HEDIS measure | {{role}} | 1 business day |
| **Medium** | Net change > 100 codes in a single release; new code grouped to "Other" by default | {{role}} | 1 week |
| **Low** | Description-only changes; rare-use codes | {{role}} | Monthly digest |

## Drift report format

Each report contains:

- Release identity (code system + version + release date)
- Counts (added / deleted / description-changed / mapping-changed)
- Exposure summary (warehouse row count, value-set count, downstream consumer count)
- Top-10 representative changes with sample rows
- Triage status (open / in-progress / resolved) per affected artifact
- Action items with owners and due dates

## Refresh execution

After triage, the refresh sequence:

1. **Load new code-system vintage** into the warehouse (versioned, retaining prior vintages).
2. **Refresh derived artifacts** (value-set expansions, crosswalk-bound tables, grouper outputs).
3. **Re-validate** sample analytic outputs against expected ranges.
4. **Publish** vintage-tagged refresh notice to downstream consumers.
5. **Update** the inventory entry (see `code-system-inventory.md`).

## Restatement decision

A material drift may warrant **restatement** of prior published analytics. Criteria:

- Change affects a regulatory / contractual deliverable
- Change shifts a published rate / score by more than {{threshold, e.g., 0.5 percentage points}}
- Stakeholder request

Restatement decision:

- [ ] No restatement (changes captured in next reporting cycle)
- [ ] Restatement of current cycle only
- [ ] Restatement of {{N}} prior cycles

## Tools

- **Diff job**: `{{repo/path/to/diff-job}}`
- **Impact analysis query templates**: `{{repo/path/to/impact-queries}}`
- **Alerting channel**: {{Slack / email / dashboard}}
- **Drift report archive**: {{path / wiki}}

## Audit

- Drift reports are retained for {{N years}} for audit / restatement traceability.
- Each report links to the underlying source-data downloads and the diff queries used.

## Change log

| Date | Change | Owner |
|---|---|---|
| {{YYYY-MM-DD}} | Initial plan | {{name}} |
| {{YYYY-MM-DD}} | Added {{code system}} to monitored set | {{name}} |
