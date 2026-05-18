# HIPAA, Privacy & De-Identification

## What is PHI?

Protected Health Information = any individually identifiable health info held by a covered entity or business associate.

### 18 HIPAA Safe Harbor identifiers (must all be removed for de-identification)

1. Names
2. Geographic subdivisions smaller than state (street, city, county, precinct, ZIP — except first 3 digits of ZIP if population >20,000)
3. Dates (except year) directly related to individual — birth, admission, discharge, death; all ages >89 → "90+"
4. Phone numbers
5. Fax numbers
6. Email addresses
7. SSN
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers & serial numbers (incl. license plates)
13. Device identifiers & serial numbers
14. URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photos & comparable images
18. Any other unique identifying number, characteristic, or code

Plus: the covered entity must have no actual knowledge that the residual info could identify the individual.

**Alternative**: Expert Determination method — qualified statistician certifies very small re-identification risk.

## Agent rules when handling charts

1. **Verify status before reading.** Ask: de-identified, synthetic, or live PHI in HIPAA-compliant env?
2. **If unsure → stop.** Do not process. Tell the user why.
3. **Do not echo PHI unnecessarily.** Summaries can use role-based references ("the patient", "the cardiologist") instead of names.
4. **Do not transmit PHI to external tools/APIs** unless the environment is documented as BAA-covered for that service.
5. **Outputs should not introduce new PHI** (don't make up names, MRNs, etc.).
6. **Logs & memory**: do not write PHI into persistent notes, session memory, or repo memory.

## 42 CFR Part 2 (Substance Use Disorder records)

Stricter than HIPAA. Records from federally-assisted SUD treatment programs require **specific patient consent** for most disclosures, even within the care team in some cases. Re-disclosure prohibited without consent. Flag any SUD-program records and treat with extra care.

## State law

Some states (CA, NY, TX, WA, etc.) have stricter rules for HIV, mental health, genetic info, reproductive health, and minor consent. When in doubt, defer to user / legal.

## GDPR / international

If patient is in EU/UK or data is processed there, GDPR applies on top of (or instead of) HIPAA. Health data = "special category" requiring explicit basis for processing.

## Quick agent script

> "Before I proceed: is the chart data you've provided (a) de-identified per HIPAA Safe Harbor, (b) synthetic/sample data, or (c) live PHI in a HIPAA-compliant environment with an appropriate BAA in place? I need to confirm before reading."
