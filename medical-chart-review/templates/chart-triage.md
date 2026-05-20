# Chart Triage / Classification

**Source**: [EHR export / file(s), date range] · **Triage date**: [YYYY-MM-DD]
**Reviewer**: AI documentation reviewer (not a clinical opinion)
**Reference**: [`../references/chart-types.md`](../references/chart-types.md)

> Run after SKILL.md §0 PHI/scope gate, before any other review type. Omit sections that don't apply (don't leave empty placeholders).

## Summary

| Field | Value |
|---|---|
| Detected care setting | [primary setting from chart-types.md §1 - or "see per-encounter table" if longitudinal multi-setting] |
| Attributes | [optional: `pediatric`, `L&D`, `newborn`, `perioperative`, `telehealth-modality` - see chart-types.md §1 cross-cutting attributes; omit row if none] |
| Detected payer program | [program from §2, or `Unknown - ask user`] |
| Confidence | High / Medium / Low |
| 42 CFR Part 2 privacy class | None detected / Suspected / Confirmed |
| Recommended next review | [clinical-summary / cdi-review / hcc-audit / quality-gap / med-rec / utilization-review / coding-audit / data-abstraction] |

## Signals cited

| Signal observed | Source (note date + section, or face-sheet field) | Implies |
|---|---|---|
| e.g., `MDS 3.0 GG0130` | 2025-04-12 SNF admission packet, p.4 | SNF |
| e.g., `Humana Gold Plus HMO` | Face sheet, Insurance | Medicare Advantage |

## Per-encounter segmentation

*Include only for longitudinal records spanning multiple settings.*

| # | Dates | Facility | Setting | Confidence | Transition from prior |
|---|---|---|---|---|---|
| 1 | YYYY-MM-DD → YYYY-MM-DD | | | | n/a |
| 2 | YYYY-MM-DD → YYYY-MM-DD | | | | e.g., acute → SNF (TRC-relevant) |

## Disambiguation applied

*Include only when a §4 rule was needed.* Example: "Inpatient vs Observation: order says obs, LOS = 38h → observation."

## Unresolved questions for the user

*Required when confidence is Medium/Low or any §3 "always ask" condition fired.*

- [ ] [Specific question, e.g., "Was this billed inpatient or observation? Order documentation missing."]
- [ ] [Specific question, e.g., "Is this from a 42 CFR Part 2 program? A psychotherapy note appears separated from the medical record."]

## Routing rationale

[1-2 lines: which downstream review type fits and why, tied to detected setting/payer. E.g., "MA detected → HCC audit is highest-yield next step; setting=outpatient supports MEAT-based capture."]

---
*Chart triage is a documentation-classification step, not medical advice. Setting/payer attribution affects coding, billing, and quality-measure eligibility and must be confirmed by a credentialed reviewer before any reportable use.*
