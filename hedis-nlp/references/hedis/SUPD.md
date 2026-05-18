# SUPD — Statin Use in Persons with Diabetes

**Reporting path:** Pharmacy claims / PQA measure used in CMS Medicare Stars
**Population focus:** Adults 40-75 with diabetes
**Note:** SUPD is a **PQA (Pharmacy Quality Alliance) measure** used in Medicare Stars; not strictly an NCQA HEDIS measure but commonly grouped with HEDIS in quality programs.

## Denominator

- Members 40-75 as of end of MY
- Diabetes identified by **two or more fills of a diabetes medication** during MY (insulin, biguanides, sulfonylureas, TZDs, DPP-4 inhibitors, GLP-1 agonists, SGLT2 inhibitors, etc.)
- Continuous enrollment per spec

## Numerator

- At least one fill of any statin during MY

## Exclusions

- ESRD / dialysis
- Hospice
- Pregnancy / lactation during MY
- Rhabdomyolysis / myopathy
- Cirrhosis / liver disease
- PCSK9 inhibitor use (replaces statin)
- Some specs exclude pre-diabetes / metformin-only as denominator

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-only |
| **Compliance window** | At least one statin fill during MY |
| **Date types that COUNT** | Pharmacy dispense date (fill date) |
| **Date types that do NOT count** | Prescription written date alone, "on statin" mention without fill evidence, sample given in office, prior-year fill with no MY refill |
| **"Most recent" disambiguation** | Any qualifying fill in MY satisfies; PDC sub-measures aggregate fills across MY |
| **Look-back / look-forward** | None for the basic SUPD; PQA PDC variants have their own look-back rules |

**Common date confusions for this measure**

- Outside-pharmacy cash fills (GoodRx, 340B, mail order outside plan) - chart may show "on statin" with no claim; the evidence date is the dispense date if obtainable, otherwise the case fails admin scoring
- Office samples - sample distribution date is NOT a pharmacy dispense
- Prescription written prior MY with first fill in current MY - the **fill date** counts, not the write date
- 90-day fill spanning the year boundary - the dispense date is the day the prescription is filled, not the days-supply end date

## NLP signal phrases

**Section hints:** Medications list, Active Meds, Prescriptions, Plan, scanned outside med lists, pharmacy fill history

**Positive signals (statin names)**
- Generic: "atorvastatin" / "simvastatin" / "rosuvastatin" / "pravastatin" / "lovastatin" / "fluvastatin" / "pitavastatin"
- Brand: "Lipitor" / "Crestor" / "Zocor" / "Pravachol" / "Mevacor" / "Lescol" / "Livalo"
- Combos: "Caduet" (atorvastatin/amlodipine) / "Vytorin" (simvastatin/ezetimibe)
- Generic phrasing: "statin therapy" / "on a statin" / "HMG-CoA reductase inhibitor"

**Diabetes confirmation (for denominator)**
- "diabetes mellitus" / "T2DM" / "T1DM" / "DM"
- Diabetes medications: insulin, metformin, glipizide, glyburide, glimepiride, pioglitazone, sitagliptin, linagliptin, empagliflozin, dapagliflozin, canagliflozin, semaglutide (Ozempic, Wegovy, Rybelsus), liraglutide, dulaglutide, tirzepatide (Mounjaro, Zepbound)

**Negative / exclusion signals**
- "rhabdomyolysis" / "statin-induced myopathy"
- "statin intolerance" (documented adverse reaction)
- "cirrhosis" / "decompensated liver disease"
- "pregnant" / "breastfeeding"
- "ESRD" / "on dialysis"
- "hospice"
- "PCSK9 inhibitor" / "alirocumab" / "evolocumab" / "Praluent" / "Repatha"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Statin recommended" / "discussed starting statin" / "will start atorvastatin"** - temporality: future intent; not a fill
- **"Statin held due to elevated LFTs" / "statin paused"** - currently off; needs spec-specific handling and may require exclusion documentation
- **"Patient refuses statin"** - refusal alone does NOT close the measure and does NOT exclude unless paired with documented intolerance
- **"Statin intolerance" / "rhabdomyolysis on prior statin" / "myalgia with atorvastatin"** - exclusion signal; needs specific reaction documented to qualify
- **"PCSK9 inhibitor" / "alirocumab" / "evolocumab" / "Praluent" / "Repatha"** - exclusion signal; replaces statin in some specs
- **"Atorvastatin" on med list** without fill evidence - presence on med list alone does not equal a dispense; verify pharmacy data
- **"FH of statin myopathy"** - experiencer = family; does not exclude the patient
- **"Niacin" / "ezetimibe" / "fish oil"** - NOT statins; do not credit as numerator
- **"Combination therapy with statin"** - vague; need explicit drug name (Caduet, Vytorin contain statins; many combos do not)
- **"Pre-diabetes" / "metformin alone for PCOS"** - check denominator definition; may not qualify as diabetes for SUPD
- **"Cirrhosis" / "decompensated liver disease"** - exclusion signal

## Common documentation gaps

- Statin discontinued temporarily but never restarted; no fills during MY
- Outside-pharmacy fills not in plan's pharmacy claims (e.g., GoodRx cash fills, 340B)
- Statin intolerance documented but no exclusion code submitted
- Diabetes med list shows metformin only - some denominator definitions exclude metformin-only

## Notes

- SUPD is pharmacy-claims based; chart documentation matters for **exclusion documentation** more than numerator (numerator = a fill)
- For chart review, focus on **documenting exclusions properly** so the patient is correctly removed from denominator
- Statin intolerance must be documented with specific reaction, not just patient preference, to qualify in some specs
- Related but separate: [SPC](SPC.md) (Statin Therapy for Cardiovascular Disease)

## See also

- [`SPC.md`](SPC.md)
- [`GSD.md`](GSD.md)
- PQA technical specifications for SUPD
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
