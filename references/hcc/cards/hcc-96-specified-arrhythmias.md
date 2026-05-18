# HCC 96 - Specified Heart Arrhythmias

> Exemplar card. Uses the 9-section schema.

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 96 (verify current V28 number) - Specified Heart Arrhythmias |
| **HCC (V24)** | 96 - Specified Heart Arrhythmias |
| **HHS-HCC** | Separate HHS HCC; verify |
| **RAF weight (V28 community)** | Moderate |
| **Primary ICD-10 ranges** | I48.x (Atrial fibrillation / flutter), I47.x (Paroxysmal tachycardia), I49.x (Other arrhythmias - sick sinus, vent fib, etc.). Many arrhythmias do NOT risk-adjust (e.g., premature beats, sinus tachycardia). |
| **Hierarchy** | Cardiac hierarchy; verify against V28 file |

## 2. Clinical definition

The HCC covers specified clinically significant arrhythmias. The most common qualifying conditions:

- Atrial fibrillation (chronic, paroxysmal, persistent, permanent)
- Atrial flutter
- Ventricular fibrillation / flutter
- Sick sinus syndrome
- Some forms of SVT (paroxysmal supraventricular tachycardia, certain re-entrant tachycardias)

Notably NOT covered (verify against current crosswalk):

- Sinus tachycardia (R00.0)
- Premature beats / PACs / PVCs (I49.1, I49.3)
- Bradycardia alone (R00.1)

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter with acceptable provider type in calendar year
- ECG / cardiac event monitor reviews must be tied to a face-to-face encounter
- Holter monitor read alone is not a face-to-face

## 4. Required documentation (MEAT)

- **M**: heart rate / rhythm monitoring, palpitation symptom check, syncope check
- **E**: ECG review with rhythm, Holter / event monitor report review, rate control assessment
- **A**: per-condition statement ("AFib, rate-controlled"), stroke-risk discussion (CHA2DS2-VASc)
- **T**: anticoagulant continuation or change (warfarin, DOACs), rate / rhythm control medication (beta-blocker, calcium-channel blocker, amiodarone, flecainide), procedures (ablation, cardioversion), device management (pacemaker, ICD checks)

CHA2DS2-VASc discussion and anticoagulation rationale are particularly strong MEAT for AFib.

## 5. Date of service rule

- Any qualifying encounter in the calendar year
- Annual reset; pacemaker presence does NOT auto-recapture the underlying arrhythmia
- Ablation does not automatically resolve AFib for coding purposes; depends on documented outcome

## 6. Hierarchy interaction

- Vent fib / vent flutter (severe) may trump less severe arrhythmias within the cardiac hierarchy; verify against current V28 hierarchy file.
- No standard interaction terms specific to arrhythmias in the disease-disease interaction set, but CHF + arrhythmia frequently co-occur clinically.

## 7. Assertion / negation pitfalls

- **"History of AFib, in normal sinus rhythm post-ablation, off anticoagulation"** - this is the classic ablation trap. If the documentation supports resolution (sustained NSR for 12+ months, off antiarrhythmics, off anticoagulation), the diagnosis may be historical. If the documentation continues to manage the patient as having AFib (any antiarrhythmic, anticoagulation, periodic rhythm monitoring), the HCC is current. Default to current unless explicit resolution.
- **"Paroxysmal AFib"** - episodic but the diagnosis is ongoing; codable as current.
- **"Persistent / permanent AFib"** - chronic; codable as current.
- **"PACs / PVCs"** - generally not the specified-arrhythmia HCC; do not code as AFib equivalent.
- **"Sinus tachycardia"** - not an HCC; do not code as arrhythmia HCC.
- **"Pacemaker for sick sinus syndrome"** - the SSS is the codable HCC; the pacemaker is a status code (Z95.0), not the diagnosis.
- **Family history of AFib** - not patient.
- **"Possible AFib"** in outpatient - hedged; do not code until confirmed by ECG / monitor.

## 8. Status-code conflations

- **Z95.0 (pacemaker)** - status code; does NOT establish the underlying arrhythmia. The pacemaker was placed for some indication (SSS, AV block, etc.); that underlying diagnosis is what supports the HCC, with appropriate documentation.
- **Z95.810 (ICD)** - status; the underlying ventricular arrhythmia or risk is what matters.
- **Z79.01 (long-term anticoagulant use)** - paired with AFib often; supports MEAT but is not the HCC itself.
- **Z45.0xx (pacemaker / ICD adjustment encounter)** - encounter type code, not the underlying arrhythmia.

**The pacemaker pitfall:** Seeing Z95.0 in a chart does NOT mean the patient currently has an arrhythmia HCC. A pacemaker patient with stable rhythm and no documented arrhythmia in the current year does not get HCC 96 from the pacemaker alone. The underlying arrhythmia must be documented and MEAT-supported.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "atrial fibrillation," "AFib," "AF," "atrial flutter," "Aflutter," "PSVT," "ventricular tachycardia," "VT," "ventricular fibrillation," "VF," "sick sinus syndrome," "SSS"
- Medications (RxNorm): warfarin, apixaban, rivaroxaban, dabigatran, edoxaban, amiodarone, flecainide, sotalol, propafenone, dronedarone, digoxin, beta-blockers, diltiazem, verapamil
- Procedures: ablation, cardioversion (electrical or chemical), Watchman / LAA closure
- Devices: pacemaker, ICD, loop recorder
- ECG / monitor terms: "irregularly irregular," "no discrete P waves"

**Suspect-engine signals (member-level):**

- Prior-year AFib claim not recaptured
- Anticoagulant dispense without explicit indication
- Pacemaker presence with no underlying arrhythmia dx in current year
- ECG/Holter report with arrhythmia finding and no clinical dx coded

**Validate-engine signals (encounter-level):**

- Specific arrhythmia code in Assessment with linkage
- CHA2DS2-VASc score documented
- Anticoagulation rationale tied to AFib
- Rate control discussion / titration

**Reject signals:**

- Pacemaker status alone (Z95.0) without underlying arrhythmia documentation
- PACs / PVCs / sinus tach as the only finding
- "History of AFib s/p successful ablation, off everything, in NSR" - likely historical
- Hedged outpatient "possible AFib"
- Family history only
- Holter report without face-to-face encounter

**Common over-coding pattern:** Pipelines that key on "pacemaker" or "anticoagulant" and emit HCC 96 without verifying the underlying arrhythmia diagnosis over-code substantially. The pacemaker is signal for suspect (worth investigating) but not validation evidence on its own.

**Common under-coding pattern:** Paroxysmal AFib without recent episodes is sometimes documented as "history of AFib" by clinicians who mean "we have been managing this." Without explicit current language, pipelines may classify as historical and miss the HCC. Surface to providers for specificity ("currently managed AFib" vs "resolved post-ablation, off therapy").

## See also

- [`../negation-and-assertion.md`](../negation-and-assertion.md) - status code vs active disease distinction
- [`../meat-criteria.md`](../meat-criteria.md) - MEAT for arrhythmias
- [`hcc-85-chf.md`](hcc-85-chf.md) - common cardiac comorbidity
- [`hcc-108-vascular-disease.md`](hcc-108-vascular-disease.md) - related cardiovascular HCC
