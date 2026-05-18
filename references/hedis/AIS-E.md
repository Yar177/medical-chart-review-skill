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

**False positives to filter**
- "vaccine recommended" / "offered today" - intent, not administration
- "due for flu shot" - reminder, not compliance
- Vaccine ordered but no administration record

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
