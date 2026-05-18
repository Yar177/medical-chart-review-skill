# fuh-7-day-calendar

## Synthetic note

```
Encounter date: 03/24/2025 (Monday)
Provider: Patel, R. PMHNP-BC (Behavioral Health)
Visit type: Post-discharge MH follow-up

Subjective:
Patient discharged 03/17/2025 (Monday) from acute inpatient psychiatric unit
after admission for MDD with suicidal ideation. Presents today for first
outpatient psychiatric f/u.

Interval history:
Patient reports improved mood since discharge. Started on sertraline 50 mg daily
during inpatient stay. Sleep improved. No active SI today. C-SSRS negative.

Plan:
1. Continue sertraline 50 mg daily; increase to 100 mg in 2 weeks if tolerated.
2. Weekly therapy with on-site psychologist.
3. Return in 2 weeks.
```

## Expected extraction

```yaml
satisfies_numerator:
  fuh_7_day: false        # 7-day window closed 03/24 (calendar day 7)
                          # this visit is day 7 IF inclusive, but 8 calendar days from 03/17
                          # spec convention: 7 days post-discharge means 03/18-03/24 inclusive
                          # verify spec definition of "within 7 days"
  fuh_30_day: true        # well within 30-day window
evidence:
  - concept: mh_outpatient_followup
    value: null
    date_of_service: 2025-03-24
    date_source: explicit
    date_confidence: high
    assertion: positive
    provider_role: mh-provider
    section: encounter_header
    verbatim_snippet: "Post-discharge MH follow-up"
discharge_anchor:
  date: 2025-03-17
  source: encounter narrative
notes_for_reviewer: |
  Calendar-day window. Day-of-discharge does NOT count (day 0).
  Day 1 = 03/18; day 7 = 03/24. Whether the visit on day 7 qualifies as
  "within 7 days" depends on spec inclusivity - confirm against current
  MY spec. Many programs interpret "within 7 days" as days 1-7 inclusive,
  so 03/24 qualifies. Weekend gap (03/22-03/23) is irrelevant; calendar days only.
```

## Notes for reviewers

- The "calendar vs business days" trap costs measures.
- Day 0 (day of discharge) does not count.
- A PMHNP-BC visit is a qualifying MH-provider encounter.
- Document the spec-specific interpretation of "within N days" in your model card and stick to it.
