# HCC 85 - Congestive Heart Failure

> Exemplar card. Uses the 9-section schema.

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 85 (or current V28 CHF HCC; verify against crosswalk) - Congestive Heart Failure |
| **HCC (V24)** | 85 - Congestive Heart Failure |
| **HHS-HCC** | Separate HHS HCC for CHF; verify benefit-year crosswalk |
| **RAF weight (V28 community)** | High; one of the most impactful chronic HCCs |
| **Primary ICD-10 ranges** | I50.xx (Heart failure - acute, chronic, systolic, diastolic, combined; HFrEF vs HFpEF). Subsumed-by relationships with cardiomyopathy (I42.x) and rheumatic heart disease (I09.81). |
| **Hierarchy** | Verify per V28 hierarchy file; some cardiac HCCs trump within the cardiac family. CHF often participates in disease-disease interactions (e.g., CHF + DM, CHF + COPD). |

## 2. Clinical definition

Congestive heart failure: the heart's inability to pump sufficient blood for the body's needs. Subtypes:

- **Systolic / HFrEF** (reduced ejection fraction): I50.2x
- **Diastolic / HFpEF** (preserved ejection fraction): I50.3x
- **Combined**: I50.4x
- **Unspecified**: I50.9 (avoid; specificity gap)
- **Acute / chronic / acute-on-chronic**: 5th character modifier

Specificity matters for both coding accuracy and clinical communication. CHF is one of the most under-specified diagnoses in real charts.

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter with acceptable provider type in calendar year
- Echo / BNP review encounters that include face-to-face provider component count
- Lab-only or imaging-only encounters do NOT count on their own

## 4. Required documentation (MEAT)

- **M**: weight trend (volume status), dyspnea / orthopnea / PND assessment, edema check, exercise tolerance, NYHA class, vital trends (BP, HR), JVP, lung exam
- **E**: BNP / NT-proBNP value, echo result with EF, chest x-ray review, electrolytes (relevant to diuretic management), eGFR (relevant to cardiorenal management)
- **A**: per-condition statement ("CHF stable / decompensated / NYHA class II"), discussion of triggers, education
- **T**: diuretic continuation or titration, GDMT (ACEi/ARB/ARNI, beta-blocker, MRA, SGLT2i), device discussions (ICD, CRT), referrals (cardiology, HF clinic), salt / fluid restriction counseling

The MEAT must be linked to CHF, not just to a coincident HTN or AFib.

## 5. Date of service rule

- Any qualifying encounter in the calendar year
- Annual reset; even with implanted device (LVAD, ICD), the diagnosis must be re-documented yearly
- Echo from prior year does not establish current-year MEAT on its own; the current-year encounter must reference it or have its own evaluation evidence

## 6. Hierarchy interaction

- Verify the V28 cardiac hierarchy. Some cardiac HCCs (specific cardiomyopathy, severe forms) may trump CHF; others may be trumped by CHF.
- Disease-disease interactions: CHF + DM and CHF + COPD are common interaction pairs that add coefficient lift (verify against current model).
- Acute on chronic CHF (I50.x3): the acute episode coding does not retroactively negate the chronic; both can support the HCC depending on documentation.

## 7. Assertion / negation pitfalls

- **"History of CHF"** without current-activity language - the classic RADV trap. If the chart documents an old admission years ago with no current symptoms, current echo, current meds, or current management, the diagnosis is historical (Z86.79 or similar) and HCC 85 does NOT apply.
- **"History of CHF, currently decompensated"** - current overrides historical; codable as active.
- **"Heart failure ruled out"** - negation; do not code.
- **"Heart failure vs COPD as cause of dyspnea"** - hedging in outpatient setting; do not code either until confirmed.
- **"Diastolic dysfunction"** on echo without clinical CHF diagnosis - this is an echo finding, not a clinical diagnosis. Do NOT code as I50.3x without provider diagnosis.
- **"Reduced EF" without CHF diagnosis** - same pattern; the echo finding requires provider clinical correlation.
- **Family history of CHF** - not patient.
- **"Pulmonary edema 2/2 acute CHF, resolved"** - the acute episode resolved but if chronic CHF persists, the chronic component is current.

## 8. Status-code conflations

- **Z95.811 (presence of cardiac assist device)** - device status; does not by itself establish current CHF.
- **Z95.0 (presence of cardiac pacemaker)** - does not establish CHF.
- **Z86.79 (personal history of other diseases of circulatory system)** - historical; not the CHF HCC.
- **Z99.2 (dialysis dependence)** - separate HCC; relevant for cardiorenal context but not CHF itself.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "CHF," "heart failure," "HFrEF," "HFpEF," "systolic dysfunction with HF," "diastolic heart failure," "acute on chronic HF," "decompensated HF," "NYHA class II/III/IV"
- Medications (RxNorm): furosemide, torsemide, bumetanide, spironolactone, eplerenone, sacubitril/valsartan, ACEi/ARB, beta-blockers (carvedilol, metoprolol succinate, bisoprolol), SGLT2i (in CHF context), digoxin, hydralazine + isosorbide
- Labs/imaging (LOINC): BNP, NT-proBNP, echo with EF
- Procedures: ICD/CRT placement, heart cath, LVAD placement

**Suspect-engine signals (member-level):**

- Prior-year CHF claim not yet recaptured
- Echo report with reduced or preserved EF in the chart but no CHF dx in current-year encounters
- BNP elevation without CHF diagnosis
- Diuretic dispense without CHF dx
- HF clinic referral

**Validate-engine signals (encounter-level):**

- Specific CHF code (I50.22, I50.32, I50.42, etc.) in Assessment with linkage
- Per-condition statement of CHF status
- Documented volume status, BNP review, EF reference, diuretic management

**Reject signals:**

- "History of CHF" with no current activity
- Echo findings alone (diastolic dysfunction, reduced EF) without provider CHF diagnosis
- Hedged outpatient ("possible CHF")
- Family history only
- Unspecified I50.9 in a chart that clearly supports systolic or diastolic - surface as specificity query rather than auto-validate

**Failure-mode references:**

- [`../test-fixtures/meat-gap.md`](../test-fixtures/meat-gap.md) - CHF in PMH with no current MEAT (URI visit fixture)
- [`../test-fixtures/problem-list-only.md`](../test-fixtures/problem-list-only.md) - similar pattern

**Specificity gap watch:** I50.9 (heart failure unspecified) is generally accepted but is a documentation weakness. A pipeline that captures I50.9 should also surface the specificity gap so providers can be queried to specify HFrEF vs HFpEF and acute vs chronic. The CHF HCC fires either way; specificity matters for clinical care and may affect coefficients in some model versions.

## See also

- [`../hierarchies.md`](../hierarchies.md) - cardiac hierarchy
- [`../raf-calculation.md`](../raf-calculation.md) - CHF interactions
- [`hcc-96-specified-arrhythmias.md`](hcc-96-specified-arrhythmias.md) - common cardiac comorbidity
- [`hcc-108-vascular-disease.md`](hcc-108-vascular-disease.md) - common cardiovascular comorbidity
- [`../test-fixtures/meat-gap.md`](../test-fixtures/meat-gap.md)
