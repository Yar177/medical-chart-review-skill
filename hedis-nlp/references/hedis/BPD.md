# BPD — Blood Pressure Control for Patients with Diabetes

**Reporting path:** Admin / Hybrid (varies by MY); ECDS direction
**Population focus:** Adults 18-75 with diabetes

## Denominator

- Members 18-75 as of end of MY
- Continuous enrollment through MY
- Diabetes diagnosis identification (typically two outpatient diagnoses or one inpatient diagnosis during MY or prior year, OR a dispensed antihyperglycemic medication)

## Numerator

- **Most recent BP reading during MY < 140/90 mmHg**
- Both systolic AND diastolic must meet the threshold
- The BP must be recorded by a clinician (or self-reported home BP captured by clinician, per current spec - verify)

## Exclusions

- Hospice during MY
- ESRD / dialysis
- Pregnancy during MY (any time)
- Non-acute inpatient stay during MY
- Advanced illness / frailty exclusion for members 66+
- Gestational or steroid-induced diabetes (denominator exclusion if it's the only diabetes evidence)

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-only |
| **Compliance window** | Most recent qualifying BP during MY |
| **Date types that COUNT** | Encounter date of the visit where BP was recorded by clinician |
| **Date types that do NOT count** | Note signing date when BP is copy-forward, historical BP narrative in HPI/PMH, prior-year BP, order date |
| **"Most recent" disambiguation** | If multiple BPs in MY, use the latest qualifying BP by encounter date; if multiple on same date, follow current spec (often lowest of the day or last recorded) |
| **Look-back / look-forward** | None |

**Common date confusions for this measure**

- Triage BP later re-checked same day - the re-check value is what scores; date is the encounter date
- BP copy-forwarded into a current note from a prior visit - the BP belongs to the prior encounter date, not the current note
- Home BP log dictated in narrative - the log date is the BP date, not the note date (verify spec acceptance of home BPs)
- BP value buried in a problem-list comment with no encounter linkage - not directly scoreable

## NLP signal phrases

**Section hints:** Vitals, Plan ("BP at goal"), Assessment ("HTN controlled"), Results, flowsheet

**Positive signals**
- BP value patterns like "BP 128/78" / "B/P 132/84" / "blood pressure 130/80"
- "BP at goal"
- "hypertension controlled"
- "normotensive today"

**Negative / exclusion signals**
- "ESRD" / "on dialysis" / "HD" / "PD" / "renal transplant"
- "pregnant" / "G_P_ with active pregnancy" / "EDC"
- "hospice" / "comfort care"
- "metastatic" / "advanced illness"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"BP at goal" / "BP controlled" / "normotensive" without numeric value** - hedged; needs the actual systolic/diastolic to score
- **"BP elevated, recheck recommended"** with no recheck value - first reading is the data; "recheck" is future intent
- **"Initial BP 160/95 due to pain, repeat after analgesia 132/78"** - spec-dependent handling; usually the repeat value scores
- **"PMH: HTN, BP usually 130s/80s"** - temporality: historical narrative, not current encounter value
- **BP from triage taken before pain treatment or panic** - often re-checked; use the most recent qualifying value per spec
- **"Patient denies HTN symptoms"** - negation of symptoms, not of BP value
- **"Mother's BP runs high"** - experiencer = family
- **"WNL" / "stable"** alone - hedged, no numeric value
- **"BP on home cuff: 122/76"** - patient-reported home reading; verify current spec acceptance (often requires clinician documentation)
- **"White coat hypertension"** - context modifier; does not automatically qualify a normal reading
- **"If BP elevated next visit, will start lisinopril"** - hypothetical; not evidence

## Common documentation gaps

- Multiple BPs in same visit - need clear "most recent" or "lowest of the day" handling per spec
- Home BP readings dictated into note but not captured as structured vitals
- BP at goal but no diabetes diagnosis on the same encounter chain (denominator failure, not numerator)

## Notes

- **BPD vs CBP**: BPD is diabetic-population BP control; [CBP](CBP.md) is the broader hypertension control measure
- Both share BP <140/90 threshold today; older specs used different thresholds for some populations
- ECDS direction: structured BP (FHIR `Observation` with LOINC for systolic + diastolic) is preferred

## See also

- [`CBP.md`](CBP.md)
- [`GSD.md`](GSD.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
