# FUH — Follow-Up After Hospitalization for Mental Illness

**Reporting path:** Admin
**Population focus:** Members 6+ discharged from inpatient with a principal mental health diagnosis

## Denominator

- Members 6 years and older
- Discharged alive from an acute inpatient setting with a **principal diagnosis of a mental health disorder** during MY (typically Jan 1 through Dec 1 to allow 30-day follow-up window within MY)
- Continuous enrollment from discharge through 30 days after
- Excludes transfers and discharges followed by readmission within 30 days for non-mental-health reasons (verify current spec)

## Numerator (reported as two rates)

1. **Follow-up within 7 days of discharge**
2. **Follow-up within 30 days of discharge**

Compliant follow-up = outpatient visit, intensive outpatient encounter, partial hospitalization, community mental health center visit, telehealth visit, or e-visit **with a mental health provider**.

## Exclusions

- Discharge against medical advice (AMA) - varies by spec
- Death during follow-up window
- Hospice

## NLP signal phrases

**Section hints:** Discharge summary, Plan, follow-up appointments, telehealth visit notes, scanned outside provider notes

**Positive signals - follow-up visit completed**
- "psychiatry follow-up"
- "outpatient mental health visit"
- "seen by psychiatrist on [date]" (within 7 or 30 days post-discharge)
- "follow-up appointment with [psychiatrist / psychologist / LCSW / LMHC]"
- "intensive outpatient program (IOP) day 1"
- "partial hospitalization program (PHP)"
- "community mental health center"
- "telepsychiatry visit"
- "tele-therapy session"

**Provider type signals (mental health provider required)**
- "psychiatrist" / "psychiatric NP / PA"
- "psychologist" / "PhD" / "PsyD"
- "LCSW" / "LMHC" / "LMFT" / "LCPC"
- "behavioral health provider"

**Diagnostic context (for denominator confirmation)**
- "major depressive disorder" / "MDD"
- "bipolar disorder" / "bipolar I / II"
- "schizophrenia" / "schizoaffective"
- "PTSD" / "post-traumatic stress disorder"
- "anxiety disorder" / "panic disorder"
- "substance use disorder" - check spec; SUD may be in a separate measure (FUA)
- "suicide attempt" / "suicidal ideation" / "self-harm"

**Negative / exclusion signals**
- "AMA discharge" (varies)
- "hospice"
- "expired"
- Follow-up visit > 30 days post-discharge

**False positives to filter**
- Follow-up scheduled but not attended (no-show)
- Visit with PCP only (not a mental health provider unless spec allows certain PCP scenarios)
- Phone call from staff without provider documentation
- ED visit (does NOT count as follow-up)

## Common documentation gaps

- Follow-up done at outside community mental health center; visit note not in EHR
- Telehealth visit billed but date/time of visit not parsed for the 7-day calculation
- Patient discharged to residential / SUD treatment - those visits may not satisfy depending on spec
- Discharge date misalignment between facility and outpatient calendar

## Notes

- **Two separate rates** (7-day and 30-day) - same patient counts in both denominator and may close both, one, or neither
- 7-day is the harder rate to close; aggressive post-discharge scheduling matters
- Telehealth and e-visits typically count under current spec - verify
- Related measures:
  - **FUM** = Follow-Up After ED Visit for Mental Illness
  - **FUA** = Follow-Up After ED Visit for Substance Use
- For NLP: discharge date is the anchor; calculate days-to-follow-up precisely

## See also

- [`TRC.md`](TRC.md)
- [`PHQ.md`](PHQ.md)
- [`../red-flags.md`](../red-flags.md) for safety signals at discharge
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
