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

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | Inpatient discharge with principal mental health diagnosis |
| **Compliance window** | Rate 1: outpatient MH follow-up within 7 days of discharge. Rate 2: within 30 days |
| **Date types that COUNT** | Encounter date of the outpatient MH visit (including qualifying telehealth / e-visit / IOP / PHP) |
| **Date types that do NOT count** | Scheduled-but-not-attended appointment date, no-show date, ED visit date, phone-only contact without provider documentation (verify spec), discharge date itself |
| **"Most recent" disambiguation** | First qualifying follow-up visit in the window closes the rate |
| **Look-back / look-forward** | Look-forward 7 and 30 days from discharge date (calendar days, not business days) |

**Common date confusions for this measure**

- Day-of-discharge visit - typically does NOT count; day 1 is the next calendar day
- Calendar vs business days - the 7-day window is calendar days; weekends and holidays count against you
- Telehealth visit date - the visit encounter date is the evidence date (not the chart-signing date)
- Outside community mental health center visit - capture the actual visit date from the outside note, not the import date
- Discharge date itself can be ambiguous on discharges that span midnight - use the spec-defined discharge date (typically the day the discharge order is signed)

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

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **Follow-up scheduled but not attended (no-show)** - intent / scheduling; not evidence of visit completion
- **"Patient seen by PCP for med refill"** - PCP visit alone typically does NOT count unless spec allows specific scenarios; MH provider attribution matters
- **Phone call from case manager / care coordinator** without provider documentation - typically does NOT meet visit criteria (verify spec)
- **ED visit post-discharge** - ED does NOT count as outpatient MH follow-up
- **"Discussed by phone with patient post-discharge"** - phone-only, no provider visit attribution
- **"Patient declined follow-up"** - refusal; does NOT close measure
- **"FH of bipolar disorder"** - experiencer = family
- **"Hx of MDD"** without current discharge anchor - historical reference; the inpatient anchor drives the measure
- **"Telepsychiatry visit" coded as phone-only encounter** - spec-acceptance varies; phone may or may not qualify depending on MY
- **"PHP day 1 scheduled for next week"** - future intent; the actual encounter date counts when it occurs
- **"Patient AMA from psych unit"** - AMA may exclude depending on current spec; check before scoring

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
