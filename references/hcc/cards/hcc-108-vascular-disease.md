# HCC 108 - Vascular Disease

> Exemplar card. Uses the 9-section schema.
>
> **V28 note:** Peripheral vascular disease was significantly affected by the V28 transition. Many vague vascular codes were removed from risk-adjusting. Always verify against the current crosswalk before assuming a code maps to this HCC.

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 108 (or current V28 vascular HCC; verify) - Vascular Disease |
| **HCC (V24)** | 108 - Vascular Disease |
| **HHS-HCC** | Separate HHS HCC for vascular conditions; verify |
| **RAF weight (V28 community)** | Moderate; reduced from V24 due to scope narrowing |
| **Primary ICD-10 ranges** | I70.xx (Atherosclerosis - aorta, native arteries of extremities), I71.xx (Aortic aneurysm / dissection), I73.xx (Other peripheral vascular diseases including PVD, Raynaud's), I74.xx (Arterial embolism and thrombosis). Note: many subcodes within these ranges were REMOVED from risk-adjustment in V28. |
| **Hierarchy** | Verify cardiac / vascular hierarchy; some severe vascular (AAA, dissection) may trump less severe |

## 2. Clinical definition

The HCC covers significant vascular disease. Common qualifying conditions in V28 (verify against crosswalk):

- Atherosclerosis of native arteries of extremities with claudication, rest pain, ulceration, gangrene
- Abdominal aortic aneurysm
- Thoracic aortic aneurysm
- Aortic dissection
- Arterial embolism and thrombosis
- Some specific other peripheral vascular disorders

V28 removed many vague codes that V24 historically risk-adjusted (e.g., generic "peripheral vascular disease, unspecified"). Pipelines that worked under V24 will lose substantial vascular HCC volume under V28.

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter with acceptable provider type in calendar year
- Vascular surgery, cardiology, vascular medicine, or primary care all qualify
- Imaging (CTA, MRA, ultrasound) reads alone do not establish a face-to-face

## 4. Required documentation (MEAT)

- **M**: claudication symptom check, walking distance, foot exam, pulses, ABI trend
- **E**: ABI value, duplex ultrasound result, CTA / MRA review, foot exam findings (ulceration, color, temperature)
- **A**: per-condition statement (severity, location, complications), surgical / endovascular candidacy
- **T**: antiplatelet / statin therapy, cilostazol, smoking cessation counseling, supervised exercise referral, vascular surgery referral, revascularization procedures

The MEAT must be linked to vascular disease specifically, not just to coincident CAD or DM.

## 5. Date of service rule

- Any qualifying encounter in the calendar year
- Annual reset; stent presence does NOT auto-recapture vascular disease
- Post-revascularization status alone is not the HCC; current vascular disease must be documented

## 6. Hierarchy interaction

- Severe vascular conditions (aortic dissection, gangrene-complicated vascular disease) may trump less severe within the family.
- Disease-disease interactions: DM + vascular and CHF + vascular are common clinically; verify whether the current model has explicit interaction terms for these.
- Verify V28 hierarchy carefully; the family was reorganized.

## 7. Assertion / negation pitfalls

- **"History of PVD"** without current symptoms or management - may be historical; check for current antiplatelet + statin therapy and current symptom assessment. If the patient is being actively managed as PVD, current. If truly resolved (rare for atherosclerotic disease), historical.
- **"Status post femoral-popliteal bypass" / "s/p stent"** - the procedure history (Z95.820 for graft, Z95.5/Z95.820 for stent) does NOT by itself establish current vascular disease. The underlying atherosclerosis may still be active or may have improved; require current documentation.
- **"Intermittent claudication"** (I73.9) - was an HCC under V24; verify current V28 status.
- **"Mild atherosclerosis on CTA"** without clinical correlation - imaging finding alone, not clinical diagnosis.
- **"Possible PVD, will order ABI"** - hedged outpatient; do not code.
- **Family history of vascular disease** - not patient.
- **"Cold feet" / "leg pain"** without explicit vascular diagnosis - symptoms, not diagnosis.

## 8. Status-code conflations

- **Z95.5 (presence of coronary angioplasty implant and graft)** - cardiac stent, does NOT establish PVD or vascular disease.
- **Z95.820 (presence of peripheral vascular graft)** - peripheral graft status; does NOT by itself establish current PVD.
- **Z86.71 (personal history of venous thrombosis and embolism)** - historical VTE; not the same as current vascular disease.
- **Z87.891 (personal history of nicotine dependence)** - common comorbidity; not the HCC.

**The stent pitfall:** Seeing Z95.5 or Z95.820 in a chart and emitting HCC 108 is over-coding. The stent / graft was placed for a vascular indication, but the HCC requires current vascular disease documentation, not just procedural history.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "PVD," "PAD," "peripheral arterial disease," "peripheral vascular disease," "intermittent claudication," "rest pain," "critical limb ischemia," "CLI," "AAA," "aortic aneurysm," "aortic dissection," "atherosclerosis of [aorta / iliac / femoral / popliteal]"
- Medications (RxNorm): cilostazol (specific to PAD), antiplatelets (aspirin, clopidogrel) with vascular indication, statins
- Imaging / tests: ABI, duplex ultrasound, CTA / MRA aorta or runoff, angiogram
- Procedures: angioplasty, stent, bypass (fem-pop, fem-tib, axillofemoral), endarterectomy, EVAR, TEVAR
- Foot exam: ulceration, gangrene, color changes, capillary refill, pulses

**Suspect-engine signals (member-level):**

- Prior-year vascular HCC not recaptured
- Stent / graft status without current vascular dx in this year
- Cilostazol dispense (very specific)
- Vascular surgery referral
- DM patient with foot ulcer

**Validate-engine signals (encounter-level):**

- Specific vascular code (I70.2x, I71.4, etc.) in Assessment with linkage
- ABI value documented with interpretation
- Per-condition statement of current vascular status

**Reject signals:**

- Stent / graft status alone (Z95.x) without current vascular disease documentation
- Imaging finding without clinical diagnosis
- "History of PVD" with no current symptoms or management
- Hedged outpatient
- Family history only
- Vague "atherosclerosis" without anatomic specification or clinical correlation

**V28 transition watch:**

Pipelines built or tuned for V24 will over-emit vascular HCCs under V28. Specifically, generic "peripheral vascular disease, unspecified" no longer risk-adjusts in V28. The pipeline must use the V28 crosswalk and check whether each candidate ICD code still maps. Tag every extraction with the model version and re-run historical extractions against the new crosswalk when model versions change. See [`../model-versions.md`](../model-versions.md).

**Common over-coding pattern:**

Most common: emitting HCC 108 from Z95.5 (coronary stent) or Z95.820 (peripheral graft) without current vascular disease documentation. Stents and grafts are procedural history; they do not validate the current-year HCC on their own.

## See also

- [`../model-versions.md`](../model-versions.md) - V28 narrowing of vascular HCCs
- [`../terminology-mapping.md`](../terminology-mapping.md) - crosswalk-version handling
- [`../negation-and-assertion.md`](../negation-and-assertion.md) - stent/graft status vs active disease
- [`hcc-85-chf.md`](hcc-85-chf.md) - common cardiac comorbidity
- [`hcc-18-diabetes-with-complications.md`](hcc-18-diabetes-with-complications.md) - common comorbidity driving vascular disease
