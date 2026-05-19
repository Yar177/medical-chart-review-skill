# De-identification (45 CFR 164.514(a)-(c))

> Builder / compliance-officer view. For the reviewer-side application of these identifiers during chart abstraction, see the sibling `medical-chart-review` skill's `references/hipaa-privacy.md`.

## Two methods only

PHI is considered de-identified - and outside HIPAA's scope - **only** when one of two methods has been applied:

1. **Safe Harbor** (164.514(b)(2)): remove all 18 specified identifier categories AND have no actual knowledge that the remaining information could be used alone or in combination to re-identify the individual
2. **Expert Determination** (164.514(b)(1)): a person with appropriate knowledge of and experience with generally accepted statistical and scientific principles and methods for rendering information not individually identifiable determines that the risk is very small AND documents the methods and results

There is no third option. "We removed names and birth dates" is **not** de-identification.

## Safe Harbor: the 18 identifiers

Remove all of the following with respect to the individual or relatives, employers, or household members:

1. Names
2. All geographic subdivisions smaller than a State, including street address, city, county, precinct, ZIP code, and equivalent geocodes - **except** the initial 3 digits of a ZIP code may be retained if (a) the combined population of all ZIP codes with the same initial 3 digits is > 20,000 per the current Census; (b) for the 3-digit ZIP codes with population ≤ 20,000, the initial 3 digits are changed to 000
3. All elements of dates (except year) for dates directly related to an individual, including birth date, admission date, discharge date, date of death; **and all ages over 89** and all elements of dates (including year) indicative of such age, except that such ages and elements may be aggregated into a single category of age 90 or older
4. Telephone numbers
5. Fax numbers
6. Electronic mail addresses
7. Social security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate / license numbers
12. Vehicle identifiers and serial numbers, including license plate numbers
13. Device identifiers and serial numbers
14. Web Universal Resource Locators (URLs)
15. Internet Protocol (IP) address numbers
16. Biometric identifiers, including finger and voice prints
17. Full face photographic images and any comparable images
18. **Any other unique identifying number, characteristic, or code** (other than as permitted by the re-identification code provision below)

**Plus the no-actual-knowledge requirement:** the CE must not have actual knowledge that the residual information could be used to identify the individual. Knowledge of an obvious re-ID path defeats Safe Harbor even if all 18 categories are removed.

### Common Safe Harbor failures

- Dates more granular than year retained (most common)
- ZIP > 3 digits retained
- Ages ≥ 90 retained as-is (must be aggregated to "90+")
- Free-text fields (clinical notes) that contain names, dates, locations - **never** assume note text is automatically clean; apply a de-id pipeline and validate
- Quasi-identifiers retained at high uniqueness (rare diagnoses + small geography → re-ID risk → "actual knowledge" defeats Safe Harbor)
- Device IDs or session IDs that link back to a person
- "Other unique identifying number, characteristic, or code" - the catch-all; includes patient-assigned random IDs **if** the CE retains the mapping

### Re-identification code (164.514(c))

A CE may assign a code or other means of record identification to allow re-identification by the CE, **provided**:
- The code is not derived from or related to information about the individual and could not otherwise be translated to identify the individual, AND
- The CE does not use or disclose the code for any other purpose AND does not disclose the mechanism for re-identification

Hash of an MRN with a known algorithm and no salt is **not** acceptable.

## Expert Determination

Used when Safe Harbor's identifier removal would destroy analytic utility (research, claims analytics) or when the data environment changes re-ID risk.

Requirements:
- A qualified expert (statistician, computer scientist, or other with the appropriate background) applies generally accepted statistical / scientific principles
- The risk is **very small** that the information could be used, alone or in combination with other reasonably available information, by an anticipated recipient to identify the individual
- The methods and results are **documented**

Methods typically used:
- k-anonymity, l-diversity, t-closeness
- Differential privacy
- Generalization, suppression, perturbation
- Synthetic data generation (with separate utility / privacy analysis)
- Re-ID risk analysis against external data sources the anticipated recipient could reasonably access

> Expert Determination is not a one-time judgment about the data alone - it is a determination about the data **in the data environment**. Same dataset released to two different environments may need two different determinations.

## Limited Data Set (164.514(e))

NOT de-identified. PHI with **direct identifiers** removed (names, addresses except town/city/state/ZIP, telephone, fax, email, SSN, MRN, account, certificate/license, vehicle, device IDs, URLs, IPs, biometrics, full face photos) but retaining dates, town/city/state/ZIP, and ages.

Used for research, public health, and healthcare operations under a **Data Use Agreement (DUA)** with the recipient that limits use and prohibits re-identification.

A Limited Data Set is **still PHI**. A DUA is required. Disclosure without a DUA is a Privacy Rule violation.

## Common engineering pitfalls

- **Treating a Limited Data Set as de-identified** - it is not; it requires a DUA
- **Applying Safe Harbor to structured fields only** - free-text clinical notes contain identifiers; a de-id pipeline is required
- **De-id of imaging without DICOM header / pixel review** - burned-in text in DICOM pixels carries identifiers
- **De-id of voice / audio** - voice prints are biometric identifiers (#16)
- **Re-ID via linked external data** - rare diagnoses + small geography + age = identifiable; "actual knowledge" of an obvious linkage defeats Safe Harbor
- **De-identification done by the receiving party** - the CE must do it (or a BA acting on its behalf) before disclosure
- **Reuse of de-identification across environments** - Expert Determination depends on the recipient's environment

## De-identification for AI training data

Active and unsettled area. Considerations:
- Apply one of the two methods (Safe Harbor or Expert Determination) before sending PHI to any model not covered by a BAA
- Free-text clinical notes typically require a learned de-id pipeline + manual validation
- Synthetic data generation requires its own privacy analysis (membership inference risk)
- Models trained on PHI may memorize - treat model weights with appropriate care; defer to counsel for residual-risk analysis
- The BAA-covered AI services list changes - see [`vendor-cloud-shared-resp.md`](vendor-cloud-shared-resp.md)

## Defer to expert / counsel when

- Choosing between Safe Harbor and Expert Determination
- The dataset will be released to a recipient with unknown external data access
- The dataset contains rare diagnoses, small populations, or geographic concentration
- The dataset will be used to train, fine-tune, or evaluate AI models
- The de-id output will be made publicly available
- The dataset includes 42 CFR Part 2 SUD records, mental health, genetic, or minors
