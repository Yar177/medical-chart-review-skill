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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rules; WCC has three sub-indicators each independently evaluated.

| Sub-indicator | Anchor | Window | Date type that counts | Date types that mislead |
|---|---|---|---|---|
| **WCC-BMI** | None - MY-only | BMI percentile documented during MY | Encounter date where BMI percentile was documented (not raw BMI alone) | Date raw BMI was calculated without percentile; height/weight without BMI |
| **WCC-NUTRITION** | None - MY-only | Counseling documented during MY | Encounter date where nutrition counseling was documented with specifics | Date a generic "AG given" was noted without nutrition topic specificity |
| **WCC-PHYSACT** | None - MY-only | Counseling documented during MY | Encounter date where physical activity counseling was documented with specifics | Date a generic "AG given" was noted without physical-activity topic specificity |

**Common date confusions for this measure**

- BMI percentile auto-calculated from prior visit's height/weight via copy-forward - the BMI %ile belongs to the *original* measurement date
- Telehealth WCC with no in-clinic measurement - height/weight may be patient-reported with measurement date being the telehealth date (verify spec)
- Sports physical date vs WCC visit date - components from a sports physical may or may not link to a WCC visit at a different date depending on documentation
- Counseling discussed at one visit, documented in a separate addendum days later - the counseling event date is the encounter date

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

**Assertion / negation pitfalls - WCC-BMI**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **"BMI: 22" alone without percentile** - raw BMI is insufficient for pediatrics; need age-and-sex percentile
- **Height and weight without BMI calculation** - need explicit BMI and percentile
- **"Appropriate growth"** without BMI percentile - hedged
- **BMI percentile in template but null/missing value** - template artifact, not documentation
- **Percentile calculated from outdated growth chart standard** - verify which standard the spec accepts
- **"BMI normal"** without numeric percentile - hedged
- **Copy-forward BMI %ile** from prior visit - the percentile belongs to the original measurement date
- **"Patient declined weight check"** - refusal; cannot calculate BMI
- **"BMI percentile pending"** - future; not documented

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

**Assertion / negation pitfalls - WCC-NUTRITION**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **Generic "anticipatory guidance given"** without topic specified - hedged; does NOT specifically credit nutrition
- **"Nutrition"** mentioned only in handout list without discussion documentation
- **"Reviewed handouts"** without topic-specific content
- **"Discussed lifestyle"** without specific nutrition content
- **"Will discuss diet at next visit"** - future intent
- **"Patient declined to discuss nutrition"** - refusal; does NOT close measure
- **"FH of obesity"** alone - experiencer-related family context, not patient counseling
- **"Eats healthy"** as a one-liner - thin; verify spec-acceptance for substantive counseling
- **Same-paragraph mention of "nutrition" in differential** - clinical reasoning, not counseling

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

**Assertion / negation pitfalls - WCC-PHYSACT**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **Generic "anticipatory guidance"** without physical activity topic specified - hedged
- **"Active child"** descriptor without counseling content
- **"Plays sports"** in HPI as a fact about the child - context, not counseling
- **"Will discuss exercise at next visit"** - future intent
- **"Patient declined physical activity counseling"** - refusal; does NOT close measure
- **"PE class"** mentioned in social history - context, not counseling
- **"Limit screen time"** in handout list without discussion documentation
- **"FH of sedentary lifestyle"** - experiencer-related context
- **"Sports physical signed"** alone - form completion does not equal physical-activity counseling
- **Same-paragraph "exercise" in differential** - clinical reasoning, not counseling

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
