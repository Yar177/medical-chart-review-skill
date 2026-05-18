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

**False positives to filter**
- "statin recommended" / "discussed starting statin" - no fill
- "statin held due to elevated LFTs" - not currently on
- "patient refuses statin" - not compliant

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
