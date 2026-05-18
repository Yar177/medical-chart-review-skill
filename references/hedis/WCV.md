# WCV — Child and Adolescent Well-Care Visits

**Reporting path:** Admin
**Population focus:** Children and adolescents 3-21

## Denominator

- Members 3-21 as of end of MY
- Continuous enrollment through MY (with allowed enrollment gap per spec)

## Numerator

- **At least one comprehensive well-care visit during MY** with a PCP or OB/GYN practitioner
- Visit must be a well-care visit (preventive), not a sick visit

## Exclusions

- Hospice
- Death during MY
- Per current spec - verify

## What counts as a well-care visit

- AAP / Bright Futures annual preventive visit (school-age and adolescent)
- Sports physical that includes comprehensive preventive components (verify spec)
- Documentation must show preventive care content: developmental/behavioral surveillance, anticipatory guidance, immunizations review, growth/BMI tracking, physical exam, risk behavior screening (adolescent)

## NLP signal phrases

**Section hints:** Encounter type, Chief Complaint, Assessment, Plan, Anticipatory Guidance section, growth chart, immunization tab

**Positive signals - well-care visit identification**
- "well-child visit" / "WCV"
- "annual well-child check"
- "annual physical" / "annual preventive visit"
- "[age]-year-old well-child" / "5-year well", "12-year well"
- "preventive care visit"
- "Bright Futures visit"
- "annual health maintenance exam" / "HME" / "AHM"
- "sports physical" (only if comprehensive preventive content documented)
- "back-to-school physical" (only if comprehensive preventive content documented)

**Positive signals - preventive content components**
- "growth chart updated" / "BMI percentile documented"
- "developmental / behavioral surveillance"
- "ASQ-SE" / "PEDS questionnaire" (younger children)
- "PHQ-A" / depression screen (adolescents)
- "CRAFFT" / substance use screen (adolescents)
- "HEEADSSS interview" (adolescent psychosocial)
- "immunizations reviewed per CDC / AAP schedule"
- "anticipatory guidance: nutrition, physical activity, screen time, safety"
- "complete physical exam"
- "vision and hearing screening"

**Negative / sick-visit signals (DO NOT count)**
- "sick visit" / "acute visit"
- "follow-up for [acute condition]"
- "URI" / "strep throat" / "ear infection"
- Single-issue focused visits without preventive content

**False positives to filter**
- "annual visit" billed but documentation purely problem-focused
- Sports physical without comprehensive preventive components (some plans accept, some don't)
- Specialist visit (e.g., dermatology, ortho) without PCP attribution
- "appointment scheduled" without visit completed
- Telehealth well-care visit acceptance varies by spec; component completeness matters

## Common documentation gaps

- Sick visit + well visit combined; well-visit components not separately documented
- Sports physical signed by PCP but documentation lacks preventive depth
- Visit was preventive but billed with problem code only
- Adolescent visit done by OB/GYN for contraception but not coded/documented as comprehensive well-care
- Patient moves between plans; visits from prior plan not in current admin data

## Notes

- WCV consolidated and replaced some legacy adolescent/child well-care measures (W34 for ages 3-6 historically, AWC for adolescents). Verify current spec for what WCV currently encompasses
- Annual cadence - one visit per MY closes the measure
- WCV intersects with [WCC](WCC.md) (Weight Assessment & Counseling): a well-care visit is the typical event where BMI percentile and nutrition/physical activity counseling get documented
- AAP / Bright Futures periodicity schedule is the clinical reference for ages 3-21 annual visits
- ECDS direction: structured preventive encounter via FHIR `Encounter` with preventive type

## See also

- [`W30.md`](W30.md) — Well-Child Visits in the First 30 Months
- [`WCC.md`](WCC.md) — Weight Assessment & Counseling (often closed during WCV visits)
- [`PHQ.md`](PHQ.md) — Adolescent depression screening
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- AAP / Bright Futures periodicity schedule
