# gsd-copy-forward

## Synthetic note

```
Encounter date: 07/15/2024
Provider: Smith, J. MD (Family Medicine)
Visit type: Diabetes follow-up

Subjective:
Patient with T2DM, returns for routine f/u. Reports adherence to metformin 1000 mg
BID. No hypoglycemia. Diet generally ok, exercise sporadic.

PMH:
- Type 2 diabetes mellitus, dx 2019
- Hypertension
- Hyperlipidemia

Recent Labs (from chart):
- Last A1c: 7.1% on 02/12/2024
- Lipid panel: LDL 88, HDL 45 (02/12/2024)

Assessment/Plan:
1. T2DM - A1c trending at goal. Continue metformin. Recheck A1c at next visit.
2. HTN - on lisinopril, BP today 128/76.
```

## Expected extraction

```yaml
satisfies_numerator: true   # GSD numerator: A1c documented in MY
evidence:
  - concept: a1c_value
    value: "7.1"
    units: "%"
    date_of_service: 2024-02-12   # NOT the encounter date 2024-07-15
    date_source: explicit
    date_confidence: high
    assertion: positive
    provider_role: unknown        # lab order vs result not shown
    section: results
    verbatim_snippet: "Last A1c: 7.1% on 02/12/2024"
exclusions_applied: []
notes_for_reviewer: |
  Common copy-forward shape. The A1c is real but the result-date is
  4 months prior to the encounter date. The result still qualifies for
  GSD in MY2024, but downstream "most recent" logic and any narrower
  measure windows must use 2024-02-12, NOT 2024-07-15.
```

## Notes for reviewers

- The most frequent date-attribution error is defaulting to the encounter date.
- Annotators must extract the **explicit result-date adjacent to the value**.
- A pipeline that captures only "A1c 7.1%" with no date earns partial credit at best - HEDIS evidence requires the date.
- Inverse-rate variant: if reporting GSD Poor Control instead of GSD, value direction inverts but date attribution rule is identical.
