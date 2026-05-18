# WCC — Weight Assessment and Counseling for Nutrition and Physical Activity for Children/Adolescents

**Reporting path:** Hybrid historically; ECDS direction
**Population focus:** Children and adolescents 3-17
**Sub-indicators (each evaluated independently):**
1. **WCC-BMI:** BMI percentile documentation
2. **WCC-NUTRITION:** Counseling for nutrition
3. **WCC-PHYSACT:** Counseling for physical activity

## Denominator

- Members 3-17 as of end of MY
- Continuous enrollment through MY
- Outpatient or telehealth visit with a PCP or OB/GYN during MY

## WCC-BMI numerator

- **BMI percentile** documented during MY (not raw BMI - must be age-and-sex percentile for pediatrics)
- Some specs accept BMI percentile plotted on a growth chart with date

## WCC-NUTRITION numerator

- Counseling or anticipatory guidance for **nutrition** documented during MY
- Specific evidence: discussion of diet, eating habits, weight-related nutrition, food choices, anticipatory guidance, referral to nutrition

## WCC-PHYSACT numerator

- Counseling or anticipatory guidance for **physical activity** documented during MY
- Specific evidence: discussion of exercise, sports participation, screen time, sedentary behavior, anticipatory guidance, referral to PT/exercise program

## Exclusions

- Pregnancy during MY (for adolescents)
- Hospice

## NLP signal phrases - WCC-BMI

**Section hints:** Vitals, Growth Chart, Assessment, Plan, pediatric flowsheet

**Positive signals**
- "BMI percentile: 65%"
- "BMI %ile" / "BMI for age and sex"
- "growth chart updated"
- "weight: ___, height: ___, BMI: ___, %ile: ___"
- "tracking on growth chart"

**Negative / insufficient signals (DO NOT count)**
- "BMI: 22" alone without percentile (raw BMI is insufficient for pediatrics)
- Height and weight without BMI calculation
- "appropriate growth" without BMI percentile

**False positives to filter**
- BMI percentile in template but null/missing value
- Percentile calculated from outdated growth chart (different standard)

## NLP signal phrases - WCC-NUTRITION

**Section hints:** Assessment, Plan, Anticipatory Guidance, Patient Education

**Positive signals**
- "nutrition counseling provided"
- "diet discussed" / "discussed eating habits"
- "anticipatory guidance: nutrition"
- "reviewed food choices" / "discussed balanced diet"
- "referred to nutritionist / dietitian"
- "discussed sugary beverages / fast food / snacks"
- "MyPlate guidance"
- "anticipatory guidance regarding nutrition appropriate for age"

**False positives to filter**
- Generic "anticipatory guidance given" without topic specified
- "nutrition" mentioned only in handout list without discussion

## NLP signal phrases - WCC-PHYSACT

**Section hints:** Assessment, Plan, Anticipatory Guidance, Patient Education

**Positive signals**
- "physical activity counseling"
- "discussed exercise" / "discussed sports participation"
- "screen time reviewed" / "limit screen time"
- "anticipatory guidance: physical activity"
- "discussed 60 minutes of activity per day"
- "referred to PT" / "referred to exercise program"
- "discussed PE class participation"

**False positives to filter**
- Generic "anticipatory guidance" without physical activity topic
- "active child" descriptor without counseling content

## Common documentation gaps

- Raw BMI captured but percentile not calculated / not pulled into structured field
- Nutrition / physical activity counseling done verbally but no documentation
- "Anticipatory guidance" listed without topic specifics - fails both NUTRITION and PHYSACT
- Telehealth WCC visits with abbreviated documentation
- Sports physicals documented separately from WCC visit, evidence not linked

## Notes

- WCC has **three sub-indicators evaluated independently** - a chart can close BMI but miss counseling, or vice versa
- Each sub-indicator is its own rate
- Anticipatory guidance language must be specific (topic stated) - generic AG fails
- ECDS direction: structured BMI percentile via FHIR `Observation` (separate LOINC from adult BMI); counseling via `Procedure` or structured AG element

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
- CDC pediatric growth charts (reference for percentile calculation)
