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

**False positives to filter**
- "statin recommended, patient declined"
- "discussed starting statin"
- "statin held this admission for ___"
- "non-statin lipid therapy: ezetimibe alone" - does NOT satisfy

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
