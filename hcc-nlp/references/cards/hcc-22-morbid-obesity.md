# HCC 22 - Morbid Obesity

> Exemplar card. Uses the 9-section schema. See [`hcc-18-diabetes-with-complications.md`](hcc-18-diabetes-with-complications.md) for schema reference.

## 1. Identity

| Field | Value |
|---|---|
| **HCC (V28)** | 22 - Morbid Obesity |
| **HCC (V24)** | 22 - Morbid Obesity (analogous; verify) |
| **HHS-HCC** | Separate HHS HCC for obesity; verify benefit-year crosswalk |
| **RAF weight (V28 community)** | Moderate; verify current coefficients |
| **Primary ICD-10 ranges** | E66.01 (Morbid / severe obesity due to excess calories), E66.2 (Morbid obesity with alveolar hypoventilation). BMI Z-codes Z68.4x (BMI 40+) support specificity but are not HCCs themselves. |
| **Hierarchy** | Generally standalone; no within-family hierarchy in CMS-HCC. May contribute to disease-disease interactions when paired with other HCCs (verify). |

## 2. Clinical definition

Morbid (or "severe") obesity. Coding criteria typically require:

- BMI >= 40, OR
- BMI >= 35 with at least one significant obesity-related comorbidity (e.g., diabetes, OSA, HTN, OA of weight-bearing joints, CHF)

The provider must document the diagnosis of morbid obesity (or severe obesity). The BMI alone (Z68.x) is supporting evidence but not the diagnosis.

## 3. Eligibility (face-to-face + provider type)

- Face-to-face encounter with acceptable provider type in calendar year
- See [`../date-of-service.md`](../date-of-service.md)

## 4. Required documentation (MEAT)

Two things must be true simultaneously:

1. **BMI documented** in the encounter (calculated value, "BMI 42," or explicit category "morbidly obese")
2. **Provider diagnosis of morbid obesity / severe obesity** in the assessment

Plus MEAT for the diagnosis itself:

- **M**: weight trend, dietary log review, exercise tolerance changes
- **E**: BMI value, body composition, comorbidity screening (A1c, sleep study results)
- **A**: assessment statement, counseling, lifestyle discussion
- **T**: nutrition referral, weight-loss medication, bariatric surgery referral, GLP-1 agonist initiation, behavioral health referral for weight

Note: BMI documented by a nurse or in vitals is acceptable for the BMI Z-code, but the morbid-obesity diagnosis itself must come from the provider's assessment.

## 5. Date of service rule

- Any qualifying encounter in the calendar year
- Annual reset; BMI must be documented this year (cannot rely on prior year's BMI)
- Copy-forward BMI does not count; the BMI must reflect the current encounter

## 6. Hierarchy interaction

- No within-family hierarchy in CMS-HCC for obesity HCC.
- E66.01 (morbid obesity) is the HCC; E66.9 (obesity unspecified) and E66.3 (overweight) do NOT map to HCC 22.
- BMI Z-codes (Z68.4x) are required for specificity but not HCCs.

## 7. Assertion / negation pitfalls

- **"Overweight" (BMI 25-29.9)** - NOT obesity; do not map to HCC 22.
- **"Obesity" (E66.9) without "morbid" or BMI >= 40** - regular obesity is generally not an HCC in V28; check the specific BMI Z-code to determine if it qualifies via BMI >= 40 + provider diagnosis.
- **"BMI 42" with no provider diagnosis of obesity** - INSUFFICIENT. The Z-code can be coded but the HCC cannot.
- **"History of morbid obesity, status post bariatric surgery, BMI now 28"** - current BMI does not support; the diagnosis is historical (Z98.84 status post bariatric surgery). Do not code as current HCC.
- **"Class III obesity"** is synonymous with morbid obesity (BMI >= 40); accept as supporting language.
- **"Patient is heavyset" / "patient is large"** - colloquial, not a coding diagnosis. Reject.
- **Family history of obesity** - not patient.

## 8. Status-code conflations

- **Z68.4x (BMI 40+)** - required specificity for HCC 22; not the HCC itself.
- **Z98.84 (bariatric surgery status)** - documents the prior surgery; the morbid obesity HCC depends on current BMI and current diagnosis, not on the surgical history.
- **Z71.3 (dietary counseling)** - supportive but not the HCC.

## 9. NLP extraction notes

**Candidate generation signals:**

- Phrases: "morbid obesity," "severe obesity," "class III obesity," "BMI [value]," "morbidly obese"
- BMI parsing: extract numeric BMI from vitals; flag values >= 35 and >= 40
- Comorbidity context: morbid obesity often documented alongside DM, OSA, HTN

**Suspect-engine signals (member-level):**

- BMI >= 40 in any encounter without a documented morbid obesity dx
- BMI >= 35 with diabetes / OSA / HTN comorbidities and no documented morbid obesity dx
- Prior-year HCC 22 not yet recaptured

**Validate-engine signals (encounter-level):**

- BMI value present AND provider statement of morbid obesity in assessment
- Bariatric surgery referral or weight-loss medication initiation
- Linkage between BMI and diagnosis ("BMI 42, morbid obesity")

**Reject signals:**

- BMI alone without provider diagnosis (fails the two-part requirement)
- Provider statement without BMI value
- Overweight or non-morbid obesity
- History-of (post-bariatric, BMI now in normal range)
- Pediatric BMI percentiles (use age-specific Z-codes; HCC 22 is adult)

**Common over-coding pattern:**

A pipeline that emits HCC 22 from BMI alone (vitals-driven) will dramatically over-code, because morbid obesity is one of the most under-diagnosed conditions in primary care. The discipline: BMI alone is suspect-engine signal for outreach; HCC 22 validation requires the provider diagnosis. See [`../extraction-patterns.md`](../extraction-patterns.md) for the suspect / validate split.

**Common under-coding pattern:**

Many providers document "obesity" without specifying morbid obesity even when the BMI is well over 40. This is a legitimate documentation gap and a query opportunity. A suspect engine that surfaces "BMI 44 documented but only E66.9 coded" is doing valuable work; it should drive a provider query, not silent upcoding.

## See also

- [`../terminology-mapping.md`](../terminology-mapping.md) - BMI Z-codes and the two-part requirement pattern
- [`../meat-criteria.md`](../meat-criteria.md) - MEAT for HCC 22
- [`hcc-18-diabetes-with-complications.md`](hcc-18-diabetes-with-complications.md) - common comorbidity
- [`hcc-111-copd.md`](hcc-111-copd.md) - another common comorbidity
