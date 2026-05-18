# PPC — Prenatal and Postpartum Care

**Reporting path:** Admin / Hybrid
**Population focus:** Women who delivered a live birth during the measurement window
**Sub-indicators (evaluated independently):**
- **PPC-Prenatal:** Timeliness of prenatal care
- **PPC-Postpartum:** Postpartum care visit

## Denominator

- Women who had a live birth between specific dates (typically Nov of year prior to MY through Nov of MY - verify current spec)
- Continuous enrollment from defined point through 60 days after delivery
- Allowed enrollment gap per spec

## PPC-Prenatal numerator

- Prenatal visit in the **first trimester**, OR
- Prenatal visit **within 42 days of enrollment** in the organization (for late enrollees)

Compliant visit must be with an OB/GYN, midwife, family practitioner, or other PCP delivering prenatal care.

## PPC-Postpartum numerator

- Postpartum visit on or between **7 and 84 days after delivery**
- Must include components such as: pelvic exam, BP, weight, breast exam, abdominal exam, BMI assessment, or other defined postpartum content

## Exclusions

- Non-live births (stillbirth, miscarriage)
- Hospice
- Per current spec - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rules; PPC has two sub-indicators with different DoS shapes.

| Sub-indicator | Anchor | Window | Date type that counts | Date types that mislead |
|---|---|---|---|---|
| **PPC-Prenatal** | Pregnancy (EDC anchors trimester) | First trimester (≤13w6d) OR within 42 days of plan enrollment for late enrollees | Prenatal visit encounter date with gestational age within first trimester | Pregnancy-confirmation date alone (lab pregnancy test), referral-to-OB date, OB intake scheduled but not completed |
| **PPC-Postpartum** | Delivery date | Postpartum visit on or between **day 7 and day 84** after delivery | Postpartum visit encounter date with documented postpartum components | Visit < day 7 (too early), visit > day 84 (too late), in-hospital day-0 postpartum check, phone check-in without exam components (verify spec) |

**Common date confusions for this measure**

- Delivery date inferred from infant DOB - usually correct but verify against maternal record
- First prenatal visit at outside OB practice - capture the outside visit date from transferred records, not the date records arrived
- Postpartum visit done at OB but billed without postpartum-specific E&M code - encounter date still applies if documentation has required components
- Postpartum depression screen done on a separate day from the 6-week visit - the screen and the visit have independent dates; only the postpartum-visit date is the PPC-Postpartum evidence date
- Transfer of prenatal care mid-pregnancy - first-trimester visit must have occurred (with prior or current provider); the date is from whichever provider performed it

## NLP signal phrases - PPC-Prenatal

**Section hints:** OB Hx, Assessment, Plan, problem list, Prenatal Flowsheet, scanned outside OB records

**Positive signals**
- "first prenatal visit"
- "OB intake" / "OB initial visit" / "new OB"
- "prenatal care initiated"
- "EDC" / "EDD" with first-trimester gestational age (≤13w6d at visit)
- "GA: 8 weeks today, initial prenatal"
- "transfer of prenatal care" with prior provider's first-tri records

**Trimester confirmation phrases**
- "first trimester pregnancy"
- "GA 6w / 8w / 10w / 12w"
- Calculation pattern: EDD minus visit date

**Negative / exclusion signals**
- "stillbirth" / "fetal demise" / "IUFD"
- "miscarriage" / "spontaneous abortion" / "SAB"
- "elective termination" / "TAB"

**Assertion / negation pitfalls - PPC-Prenatal**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **"Pregnancy confirmed"** without subsequent prenatal visit - confirmation is not a prenatal visit
- **"Referred to OB"** without visit completed - future intent
- **Visit with non-OB provider for unrelated issue during pregnancy** - not a prenatal visit
- **"Hx of prior pregnancy"** - historical reference; not the current pregnancy anchor
- **"Pregnancy test positive today"** alone - confirmation, not prenatal care
- **"OB intake scheduled for next week"** - future intent
- **"Patient declined OB visit"** - refusal; does NOT close measure
- **"FH of pregnancy complications"** - experiencer = family
- **GA documented as "approximately 14 weeks"** - hedged; first-trimester boundary requires precise GA ≤13w6d

## NLP signal phrases - PPC-Postpartum

**Section hints:** OB Hx, Assessment, Plan, problem list, postpartum flowsheet, scanned outside records

**Positive signals**
- "postpartum visit" / "6-week postpartum"
- "PPV" with day-count
- "post-partum exam"
- "lochia" / "fundal exam" / "perineal exam"
- "postpartum depression screen" (often part of PPC visit)
- "postpartum contraception counseling"
- "lactation assessment" (in context of postpartum visit)

**Component documentation**
- "pelvic exam normal"
- "weight: ___, BP: ___"
- "breast exam: normal"
- "abdominal exam: well-healed C-section incision"

**Negative / exclusion signals**
- "stillbirth" / "IUFD" / "fetal demise"
- "hospice"

**Assertion / negation pitfalls - PPC-Postpartum**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **"Postpartum follow-up scheduled"** without visit completed - future intent
- **Visit < 7 days post-delivery** - too early (in-hospital day-0 to day-2 checks do NOT count for PPC-Postpartum)
- **Visit > 84 days post-delivery** - too late
- **Phone check-in without exam content** - typically does NOT meet visit criteria (spec may accept some telehealth - verify)
- **"6-week postpartum visit done elsewhere"** without dated outside record - cannot place in 7-84 day window
- **"Lactation consult"** alone - lactation visit may or may not include postpartum exam components; verify
- **"Patient declined postpartum visit"** - refusal; does NOT close measure
- **"Hx of postpartum depression"** - historical; not the current postpartum visit
- **"Fundal exam wnl"** - normal result is positive evidence the exam occurred; do NOT let NegEx flip
- **"Postpartum depression screen positive, no exam done"** - screen done; postpartum exam still required for PPC-Postpartum

## Common documentation gaps

- Patient enrolled mid-pregnancy; the "42 days from enrollment" rule not flagged
- First prenatal visit at outside OB practice; records not transferred
- Postpartum visit done at OB but billed without enough postpartum components in the note
- Postpartum depression screen documented separately and not linked to postpartum visit
- Telehealth postpartum visit acceptance depends on current spec

## Notes

- The 7-84 day postpartum window is strict - earlier/later visits do NOT count
- Combined "PPC composite" reporting may be required
- Newer maternal care measures (PND-E, PDS-E - prenatal/postpartum depression) overlap with PPC - keep these aligned during NLP extraction
- ECDS direction: structured prenatal/postpartum encounter and component observations via FHIR

## See also

- [`PHQ.md`](PHQ.md) for postpartum depression screening
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
