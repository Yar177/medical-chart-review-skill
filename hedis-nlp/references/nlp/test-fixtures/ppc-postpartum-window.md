# ppc-postpartum-window

## Synthetic note

```
Encounter date: 11/15/2025 (PPV)
Provider: Tran, A. MD (OB/GYN)
Visit type: Postpartum visit

Subjective:
34F G2P2, s/p NSVD on 08/28/2025. Returns today for postpartum exam.
Reports normal lochia resolved by week 6. Breastfeeding well. Mood good,
EPDS 4/30. No bleeding concerns.

Objective:
Vitals: BP 118/72, weight 168 lb (down from 184 at discharge).
General: well-appearing, NAD.
Abdomen: soft, non-tender, well-healed.
Pelvic: external normal. Vaginal walls intact, no lacerations evident.
Cervix appears normal, no discharge.

A/P:
1. Postpartum status - day 79 post-delivery. Normal exam.
2. Contraception - patient electing IUD; will schedule placement.
3. Lactation - going well.
4. Follow up PRN.
```

## Expected extraction

```yaml
satisfies_numerator: true       # PPC-Postpartum
evidence:
  - concept: postpartum_visit
    value: null
    date_of_service: 2025-11-15
    date_source: explicit
    date_confidence: high
    assertion: positive
    provider_role: obgyn
    modality: in-person
    section: encounter_header
    verbatim_snippet: "Postpartum visit"
    satisfies_numerator: true
    satisfies_numerator_reason: |
      Day 79 post-delivery (delivery 08/28/2025, visit 11/15/2025).
      Within 7-84 day window. Documentation includes required components:
      BP, weight, abdominal exam, pelvic exam, lactation, contraception,
      and postpartum depression screen (EPDS).
delivery_anchor:
  date: 2025-08-28
  source: subjective narrative
exclusions_applied: []
notes_for_reviewer: |
  Day-count calculation: 84 days from 08/28 is 11/20/2025. Visit on 11/15
  is day 79 - inside the window.
  Components documented: pelvic, BP, weight, abdominal, lactation, mood
  screen (EPDS). Strong compliance evidence.
```

## Notes for reviewers

- Verify day count: a visit on day 85+ would NOT satisfy.
- Day 7 lower boundary catches in-hospital day-0-to-day-6 checks - those don't count.
- EPDS satisfies postpartum depression screen for some related measures (PND-E / PDS-E); track separately if those are in scope.
- Telehealth-only postpartum visits without pelvic exam: acceptance varies; verify spec.
