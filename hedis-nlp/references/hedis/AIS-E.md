# AIS-E — Adult Immunization Status

**Reporting path:** ECDS
**Population focus:** Adults 19+
**Note:** Multiple sub-indicators - each evaluated independently against its own denominator and lookback. A patient may close some but not all.

## Sub-indicators

| Sub-indicator | Vaccine | Typical age band | Notes |
|---|---|---|---|
| AIS-FLU | Influenza | 19+ | Annual; current flu season |
| AIS-TS / AIS-TDAP | Td or Tdap | 19+ | Within past 10 years; Tdap once-lifetime requirement may overlay |
| AIS-ZOSTER | Recombinant zoster (Shingrix) | 50+ | Two-dose series complete |
| AIS-PNEUMO | Pneumococcal | 66+ (typically) | Verify spec; pneumococcal recommendations have changed multiple times |
| AIS-HEPB | Hepatitis B | 19+ | Series complete (typically 2- or 3-dose) |
| AIS-COVID | COVID-19 | Spec-dependent | Recently added or proposed in some programs; confirm current MY |

> **MY caution:** Pneumococcal and COVID-19 sub-indicators have been changed/added by NCQA across recent measurement years. Verify which sub-indicators are in the spec for the MY you're reporting.

## Denominator (general)

- Adults 19+ continuously enrolled through MY
- Sub-indicator-specific age bands apply

## Numerator (general)

- Evidence of vaccine administration (claim, immunization registry, EHR immunization record, supplemental data)
- Series-complete sub-indicators require all doses
- Patient refusal does **not** count as compliant (separate refusal field exists)

## Exclusions

- Hospice
- Documented anaphylactic reaction to vaccine or component (vaccine-specific)
- Some specs allow patient-refusal exclusion - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rules; AIS-E has multiple sub-indicators with different look-back windows.

| Sub-indicator | Anchor | Window | Date type that counts | Date types that mislead |
|---|---|---|---|---|
| **AIS-FLU** | Current flu season | Aug 1 of MY-1 through end of MY (verify exact spec dates) | Vaccine administration date in current flu season | Prior-season flu shot; "flu shot recommended today" without admin; vaccine ordered but not given |
| **AIS-TDAP / AIS-TS** | None - lifetime/look-back | Within past 10 years through end of MY (Tdap once-lifetime may overlay) | Vaccine administration date in look-back window | "Tetanus booster recommended"; outside-record fragment without date |
| **AIS-ZOSTER** | Age 50+ | Lifetime through end of MY; 2-dose series required | Both dose administration dates with second dose by end of MY | Series-in-progress (1 dose only); "Shingrix recommended"; live zoster vaccine (Zostavax) may not satisfy current spec |
| **AIS-PNEUMO** | Age 66+ (typically) | Lifetime through end of MY (spec-specific schedule complexity) | Vaccine administration date(s) per current PCV/PPSV schedule | Outdated PCV product without current re-vaccination; "pneumovax recommended" |
| **AIS-HEPB** | None | Lifetime through end of MY; series complete | All series doses administered (2-dose Heplisav-B or 3-dose) with last dose by end of MY | Series-in-progress; "HepB recommended" |
| **AIS-COVID** | Spec-dependent | Spec-dependent current vaccine recommendation | Vaccine administration date(s) per current ACIP recommendation | Prior-formulation vaccine without current update; "COVID vaccine recommended" |

**Common date confusions for this measure**

- Vaccine administered at retail pharmacy / state IIS - the administration date counts; capture from IIS feed, not the date the data arrived in EHR
- Vaccine "recommended" today but administered next week - the administration date is the evidence date, not the recommendation date
- Series-complete measures (Zoster, HepB) - the **last** dose date determines compliance; an in-progress series with last dose after MY-end does NOT satisfy
- Outside-record fragments without administration date - cannot place in window
- Date of "first dose" used as evidence for series-complete measure - second dose is required
- Historical flu shot in a prior season - prior-season shots do NOT satisfy current AIS-FLU

## NLP signal phrases

**Section hints:** Immunization tab/section, Plan, ROS (recent illness), History (vaccine record), scanned outside records

**Positive signals**
- "influenza vaccine" / "flu shot" / "flu vaccine administered"
- "Tdap" / "Td" / "tetanus booster"
- "Shingrix" / "zoster vaccine" / "RZV" / "shingles vaccine"
- "PCV13" / "PCV15" / "PCV20" / "PPSV23" / "Prevnar" / "Pneumovax" / "pneumococcal vaccine"
- "Hepatitis B vaccine" / "HepB" / "Engerix" / "Recombivax" / "Heplisav-B" / "Hep B series complete"
- "COVID-19 vaccine" / "Pfizer" / "Moderna" / "Novavax" / "bivalent booster" / "updated COVID vaccine"
- Dates and dose numbers in immunization records

**Negative / exclusion signals**
- "anaphylaxis to vaccine"
- "egg allergy with anaphylaxis" (historical flu exclusion)
- "patient declined" - non-compliant, but document for refusal tracking
- "hospice"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Vaccine recommended" / "offered today"** - intent, not administration
- **"Due for flu shot"** - reminder, not compliance
- **Vaccine ordered but no administration record** - order placed; administration not confirmed
- **"Patient declined"** - refusal; non-compliant (some specs allow refusal exclusion)
- **"Got it elsewhere"** without confirming date / source - patient-reported; verify against IIS or outside record
- **"FH of vaccine reactions"** - experiencer = family
- **"Hx of flu shot in 2019"** - historical reference; prior-season for current AIS-FLU
- **"Anaphylaxis to egg"** - historical flu exclusion; verify spec - egg-allergy exclusion narrowed in recent years
- **"Tdap given as infant"** - childhood DTaP does NOT satisfy adult Tdap requirement
- **"Pneumovax 2018"** as evidence for current pneumococcal sub-indicator - PCV/PPSV schedule complexity; verify the current sequence requirement
- **"Shingrix dose 1 given"** alone - series incomplete; AIS-ZOSTER requires both doses
- **"COVID vaccine x2 in 2021"** - prior-formulation; verify current ACIP-recommended update for AIS-COVID
- **"Vaccine refused due to misinformation"** - documents refusal context but does NOT close measure
- **"Will get at pharmacy"** - future intent; verify subsequent IIS feed

## Common documentation gaps

- Vaccines administered at pharmacies / retail clinics not flowing into EHR immunization tab
- State Immunization Information System (IIS) data not synced
- Outside records scanned but not parsed into structured immunization fields
- Series-complete (HepB, Zoster) recorded as individual doses without "series complete" rollup

## Notes

- ECDS-only measure - structured immunization data (FHIR `Immunization` resource) is the preferred source
- Supplemental data from state IIS / HIE typically requires signed data-use agreement; see [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- Pharmacy claims for vaccines are administrative-data-acceptable; ensure vaccine administration NDCs are mapped

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2 (AIS-E sub-indicator definitions)
- CDC ACIP recommendations for clinical context
