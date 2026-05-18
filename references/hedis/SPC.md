# SPC — Statin Therapy for Patients with Cardiovascular Disease

**Reporting path:** Admin (pharmacy + medical claims)
**Population focus:** Men 21-75 and women 40-75 with clinical atherosclerotic cardiovascular disease (ASCVD)

## Denominator

- Men 21-75 OR women 40-75 as of end of MY
- Continuous enrollment per spec
- Clinical ASCVD identified by qualifying event during MY or prior year:
  - MI (myocardial infarction)
  - CABG (coronary artery bypass graft)
  - PCI (percutaneous coronary intervention)
  - Other revascularization
  - Ischemic stroke or TIA (depending on spec)
  - Peripheral vascular disease (PVD)
  - Stable / unstable angina with confirmed ischemia

## Numerator (reported as two separate rates)

1. **Received Statin Therapy:** at least one fill of a high or moderate intensity statin during MY
2. **Statin Adherence (PDC ≥ 80%):** proportion of days covered ≥ 80% during MY (chronic adherence rate)

## Exclusions

- Pregnancy / lactation
- ESRD / dialysis
- Cirrhosis / decompensated liver disease
- Rhabdomyolysis / myopathy / statin intolerance (documented)
- Hospice
- IVF treatment during MY (some specs)
- PCSK9 inhibitor monotherapy

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | Qualifying ASCVD event in MY or prior year (MI, CABG, PCI, ischemic stroke/TIA, PVD, angina with confirmed ischemia) |
| **Compliance window** | Rate 1 (Received Statin): at least one statin fill during MY. Rate 2 (PDC ≥80%): days-covered calculation across MY |
| **Date types that COUNT** | Pharmacy dispense date (fill); ASCVD-event procedure or diagnosis date |
| **Date types that do NOT count** | Prescription written date alone, "on statin" mention without fill evidence, sample given in office, ASCVD diagnosis date outside the look-back window |
| **"Most recent" disambiguation** | Any qualifying fill in MY satisfies Rate 1; Rate 2 aggregates all fills across MY |
| **Look-back / look-forward** | ASCVD event identifiable in MY or prior year; no look-forward |

**Common date confusions for this measure**

- Statin held during admission and never restarted at discharge - fill history will show the gap; the held period does not generate a dispense
- 90-day fill spanning year boundary - dispense date is the fill day, not the days-supply end
- ASCVD event in late prior MY - still qualifies for current-MY denominator
- Outside-pharmacy cash fills (GoodRx, mail order outside plan) - chart shows "on statin" but no claim; missing dispense breaks Rate 2 even when patient is adherent

## NLP signal phrases

**Section hints:** Medications, Past Medical Hx (cardiac), Problem List, Plan, cardiology consult notes

**Positive signals - statin names**
- Generic: "atorvastatin" / "simvastatin" / "rosuvastatin" / "pravastatin" / "lovastatin" / "fluvastatin" / "pitavastatin"
- Brand: "Lipitor" / "Crestor" / "Zocor" / "Pravachol" / "Mevacor" / "Lescol" / "Livalo"
- Combos: "Caduet" / "Vytorin" / "Liptruzet" (atorvastatin/ezetimibe)
- Intensity language: "high-intensity statin" / "atorvastatin 40-80mg" / "rosuvastatin 20-40mg"

**ASCVD confirmation (for denominator)**
- "MI" / "myocardial infarction" / "STEMI" / "NSTEMI" / "history of MI"
- "CABG" / "coronary artery bypass" / "s/p CABG x___"
- "PCI" / "percutaneous coronary intervention" / "stent placement" / "DES" / "BMS"
- "stroke" / "CVA" / "ischemic stroke" / "TIA"
- "PVD" / "PAD" / "peripheral arterial disease" / "claudication"
- "angina" / "stable angina" / "unstable angina"
- "atherosclerotic cardiovascular disease" / "ASCVD"
- "CAD" / "coronary artery disease" / "ischemic heart disease"

**Negative / exclusion signals**
- "statin intolerance" with specific reaction
- "rhabdomyolysis on prior statin"
- "elevated CK on statin"
- "transaminitis on statin"
- "cirrhosis" / "decompensated liver disease"
- "pregnant" / "actively trying to conceive" / "breastfeeding"
- "ESRD" / "on dialysis"
- "hospice"
- "on PCSK9 inhibitor"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Statin recommended, patient declined" / "discussed starting statin"** - temporality: future intent or refusal; not a fill
- **"Statin held this admission"** - currently off; needs spec-aware handling
- **"Statin intolerance"** vague ("patient doesn't like statins") - typically does NOT exclude; need specific reaction (myalgia, rhabdo, transaminitis)
- **"Rhabdomyolysis on prior statin" / "CK >10x ULN on statin" / "transaminitis on statin"** - exclusion signal with documented reaction
- **"PCSK9 inhibitor" / "alirocumab" / "evolocumab"** monotherapy - exclusion signal in some specs
- **"Ezetimibe alone" / "niacin" / "fibrate"** - non-statin lipid therapy; does NOT satisfy numerator
- **"Atorvastatin on med list"** without fill evidence - presence on med list ≠ dispense
- **"FH of statin myopathy"** - experiencer = family
- **"Hx of MI 2010"** - historical ASCVD event; qualifies for denominator (lifetime for major events per most specs)
- **"CAD" alone without confirmed ischemia / event** - may or may not qualify for denominator (spec-dependent)
- **"Pregnant" / "actively trying to conceive" / "breastfeeding"** - exclusion signal
- **"Combination therapy with statin"** - vague; need explicit drug name (Caduet, Vytorin = statin-containing; Liptruzet = atorvastatin/ezetimibe)

## Common documentation gaps

- ASCVD on problem list but no statin in active meds (and no intolerance documented)
- Patient on statin filled at outside pharmacy not in claims
- Statin intolerance documented as "patient says doesn't like statins" - too vague; needs specific reaction
- Statin held during admission and never restarted at discharge
- PDC <80% due to gap in fills - adherence rate fails but receipt rate passes

## Notes

- Two rates: **Received Statin** (any fill) and **Statin Adherence** (PDC ≥80%) - very different denominators of success
- Adherence rate is often the harder one to close - requires consistent refills, not just one fill
- For NLP: distinguish "currently taking" vs "previously prescribed" - active med list date matters
- ECDS direction: structured medication statements + adherence calculated from dispense records

## See also

- [`SUPD.md`](SUPD.md)
- [`CBP.md`](CBP.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
