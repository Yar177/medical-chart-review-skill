# wcv-sports-physical

## Synthetic note

```
Encounter date: 08/12/2025
Provider: Nguyen, T. MD (Pediatrics)
Patient age: 14
Visit type: Sports physical

CC: pre-participation sports physical for soccer.

Subjective:
14yo M presents for sports clearance. No chest pain with exertion, no syncope,
no family hx of sudden cardiac death. No asthma symptoms.

Objective:
Vitals: BP 112/68, HR 64, BMI 21 (60th %ile).
Cardiac exam: RRR, no murmurs, normal S1/S2.
Lungs: clear.
MSK: normal ROM all joints. No scoliosis.

Plan:
Cleared for full sports participation. Form signed.
```

## Expected extraction

```yaml
satisfies_numerator: false       # WCV requires comprehensive well-care content
evidence: []
wcv_failure_reason: |
  Sports physical without comprehensive well-care components.
  Documented: cardiac screen, MSK exam, vitals, BMI.
  Missing: developmental/behavioral surveillance, anticipatory guidance
  (nutrition, physical activity, screen time, substance use, depression
  screening for adolescent), HEEADSSS or equivalent psychosocial review,
  immunization review.
notes_for_reviewer: |
  Sports physicals often get billed as well-care but lack the breadth
  required for WCV. The clinical fix is to add comprehensive content;
  the abstraction fix is to NOT auto-close WCV from a sports-physical-only
  encounter.
  Contrast: if the same visit had documented "anticipatory guidance:
  nutrition, physical activity, screen time, substance use, mental health;
  immunizations reviewed; depression screen negative" then WCV would close.
```

## Notes for reviewers

- Documentation depth is the failure mode, not provider type.
- Pediatric / FM providers are eligible roles.
- WCC-BMI is separately satisfiable from this note (BMI percentile is documented) but WCC-NUTRITION and WCC-PHYSACT fail without explicit counseling content.
- Sports clearance ≠ WCV without preventive-care content.
