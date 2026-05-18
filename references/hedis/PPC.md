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

**False positives to filter**
- "pregnancy confirmed" without subsequent prenatal visit
- "referred to OB" without visit completed
- Visit with non-OB provider for unrelated issue during pregnancy

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

**False positives to filter**
- "postpartum follow-up scheduled" without visit completed
- Visit < 7 days post-delivery (too early) or > 84 days (too late)
- Phone call check-in without exam content (varies by spec - some accept telehealth)

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
