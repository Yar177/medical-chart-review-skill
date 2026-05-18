# HCC 111 - Chronic Obstructive Pulmonary Disease

> Exemplar card. Uses the 9-section schema.

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 111 (verify current V28 number) - Chronic Obstructive Pulmonary Disease |
| **HCC (V24)** | 111 - Chronic Obstructive Pulmonary Disease |
| **HHS-HCC** | Separate HHS HCC for COPD; verify benefit-year crosswalk |
| **RAF weight (V28 community)** | Moderate-to-high |
| **Primary ICD-10 ranges** | J44.x (COPD, including J44.0 with lower respiratory infection, J44.1 with acute exacerbation, J44.9 unspecified). Adjacent: J43.x (emphysema), J41.x / J42 (chronic bronchitis). Note: simple chronic bronchitis (J41) and unspecified chronic bronchitis (J42) may not map to the COPD HCC; verify. |
| **Hierarchy** | Pulmonary hierarchy; verify against V28 file |

## 2. Clinical definition

Chronic Obstructive Pulmonary Disease: a chronic inflammatory lung disease that causes obstructed airflow from the lungs. Includes emphysema and chronic obstructive bronchitis. Defined clinically by symptoms (chronic dyspnea, cough, sputum) and confirmed by spirometry showing post-bronchodilator FEV1/FVC < 0.70.

Distinction: J44.x is COPD (the HCC); J41.x simple chronic bronchitis and J42 unspecified chronic bronchitis are generally NOT the COPD HCC. J43.x (emphysema without COPD designation) - verify mapping.

Asthma (J45.x) is generally not the COPD HCC. "Asthma-COPD overlap" needs careful coding.

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter with acceptable provider type in calendar year
- Spirometry / PFT reading alone does not establish face-to-face

## 4. Required documentation (MEAT)

- **M**: dyspnea trend, exacerbation frequency, exercise tolerance, oxygen requirement, smoking status update
- **E**: PFT / spirometry review (FEV1, FEV1/FVC), oxygen saturation, chest x-ray review, ABG review (severe disease), GOLD stage if documented
- **A**: per-condition statement (GOLD stage, exacerbation status, action plan), smoking cessation counseling
- **T**: inhaler continuation or change (SABA, LABA, LAMA, ICS, combination), oral steroids or antibiotics for exacerbation, oxygen prescription, pulmonary rehab referral, vaccination (flu, pneumococcal, COVID)

Smoking cessation counseling is particularly strong MEAT for COPD when documented.

## 5. Date of service rule

- Any qualifying encounter in the calendar year
- Annual reset; oxygen prescription does not auto-recapture
- PFT from prior year does not establish current-year MEAT on its own

## 6. Hierarchy interaction

- Severe / acute COPD (J44.0 with infection, J44.1 with exacerbation) may have different coefficient or interaction implications than stable COPD; verify.
- Disease-disease interaction: COPD + CHF is a recognized interaction in CMS-HCC (verify against current model).

## 7. Assertion / negation pitfalls

- **"History of COPD"** with no current symptoms or management - check carefully; COPD does not generally resolve. If patient is on any COPD-specific inhaler (LABA, LAMA, or combinations), the diagnosis is current. If truly off all therapy with documented normalization (rare), historical.
- **"Possible COPD, will check PFTs"** - hedged outpatient; do not code until PFTs confirm and provider documents.
- **"Chronic bronchitis"** - simple chronic bronchitis (J41.x) is NOT the COPD HCC unless documented as part of COPD; check for J44 code specifically.
- **"Emphysema"** alone - depending on documentation, may map to J43.x or J44.x; verify the specific code captured.
- **"Asthma"** - J45.x is not the COPD HCC.
- **"Asthma-COPD overlap" / "ACO"** - generally codes as both J44.x and J45.x; the J44.x captures the HCC. Documentation must support COPD specifically.
- **"COPD exacerbation, resolved"** - the exacerbation episode resolved but the chronic COPD persists; current.
- **Smoker without COPD diagnosis** - smoking is risk factor, not diagnosis; do not infer COPD from smoking history alone.
- **Family history of COPD** - not patient.

## 8. Status-code conflations

- **Z99.81 (dependence on supplemental oxygen)** - documents oxygen dependence; supports MEAT for COPD when paired with the diagnosis but is not the HCC on its own.
- **Z87.891 (personal history of nicotine dependence)** - smoking history; not the COPD HCC, but contextual.
- **F17.2xx (nicotine dependence)** - current smoking; separate code, supports MEAT for COPD when linked.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "COPD," "chronic obstructive pulmonary disease," "emphysema" (with COPD designation), "chronic bronchitis with airflow obstruction," "GOLD stage [1-4]," "FEV1 [value]%," "post-bronchodilator FEV1/FVC < 0.70"
- Medications (RxNorm): tiotropium, umeclidinium, aclidinium, glycopyrrolate (LAMAs); formoterol, salmeterol, olodaterol (LABAs); fluticasone-salmeterol, budesonide-formoterol, umeclidinium-vilanterol, fluticasone-umeclidinium-vilanterol (combinations); albuterol, levalbuterol (SABAs - non-specific to COPD); roflumilast (specific to COPD)
- Labs / tests: spirometry / PFT (LOINC), pulse oximetry, ABG
- Procedures / services: pulmonary rehab, oxygen titration, BiPAP / CPAP (sometimes for COPD), smoking cessation counseling
- Adjacent dx: cor pulmonale (I27.81) common late-stage finding

**Suspect-engine signals (member-level):**

- Prior-year COPD claim not recaptured
- LAMA or LABA dispense without COPD dx
- Oxygen dispense without respiratory dx
- Smoking history >= 10 pack-years with dyspnea
- Multiple COPD-pattern exacerbations in claims (acute respiratory + steroid bursts)

**Validate-engine signals (encounter-level):**

- Specific COPD code (J44.0, J44.1, J44.9) in Assessment with linkage
- PFT results documented with interpretation
- Inhaler regimen with COPD rationale
- Pulmonary rehab referral
- Smoking cessation counseling linked to COPD

**Reject signals:**

- Asthma only (J45.x)
- Chronic bronchitis only (J41.x, J42) without COPD designation
- Smoking history alone without diagnosis
- "Possible COPD" pending PFTs
- Family history only
- SABA-only management without documented COPD dx (could be asthma or other)
- "History of COPD" patient off all therapy with no symptoms (likely historical or never-confirmed)

**Common over-coding pattern:** Pipelines that key on "inhaler" or "smoker" emit COPD HCC without verifying the diagnosis. SABA inhalers are common across asthma, exercise-induced bronchospasm, and COPD; smoking is a risk factor not a diagnosis.

**Common under-coding pattern:** PFT results documented in chart but provider has not yet established the COPD diagnosis in their assessment. Suspect-engine should surface; do NOT auto-validate without provider diagnosis.

**Acute vs chronic specificity:** J44.0 (COPD with acute lower respiratory infection) and J44.1 (COPD with acute exacerbation) are typically used during the acute episode encounter; J44.9 (COPD, unspecified) is used in routine follow-up. Both support the HCC. Encoding the right specificity matters for clinical accuracy and may affect coefficient in some models.

## See also

- [`../meat-criteria.md`](../meat-criteria.md) - MEAT for COPD
- [`../terminology-mapping.md`](../terminology-mapping.md) - medication-driven extraction nuance
- [`hcc-85-chf.md`](hcc-85-chf.md) - common interaction pair (COPD + CHF)
- [`hcc-22-morbid-obesity.md`](hcc-22-morbid-obesity.md) - common comorbidity
