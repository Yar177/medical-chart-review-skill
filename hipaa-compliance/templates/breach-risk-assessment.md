# Breach 4-Factor Risk Assessment

> Required for every impermissible use or disclosure of unsecured PHI. Pair with [`../references/breach-notification.md`](../references/breach-notification.md). Retain completed assessment for 6 years whether or not a breach is determined.

## Metadata

| Field | Value |
|---|---|
| Incident ID | |
| Date of incident | |
| Date of discovery | |
| Reporter | (workforce member, BA, third party) |
| Assessor | (privacy officer or designee) |
| Counsel involved | Y / N + name |
| System(s) involved | |
| BA involved | (name + role) |
| Date assessment completed | |

## Incident description

(Concise factual summary - what happened, who was involved, what systems and data were affected. No speculation. No PHI in this summary - reference IDs only.)

## Was the PHI Unsecured?

- [ ] Yes - PHI was not FIPS-encrypted in the form that was impermissibly used/disclosed, and was not destroyed per NIST 800-88
- [ ] No - PHI was rendered unsecured-PHI-safe (FIPS-encrypted or destroyed) in the form impermissibly used/disclosed → **Breach Notification Rule does not require notification for this PHI; document the analysis and the FIPS-validation evidence; stop here unless other PHI is implicated**

If Yes, continue with the 4-factor assessment.

## Factor 1 - Nature and extent of PHI involved

Document each:

- **Categories of identifiers** (names, SSN, DOB, MRN, address, financial, contact info, etc.):
- **Categories of clinical/health information** (diagnoses, medications, lab values, imaging, mental health, SUD, HIV, genetic, reproductive):
- **Volume** (number of individuals; number of records per individual):
- **Time period of records affected**:
- **Likelihood of re-identification** if some identifiers are absent:
- **Sensitivity assessment** - any heightened categories (mental health, SUD, HIV, genetic, reproductive, minors)? Yes / No - if yes, default presumption tilts toward breach

Factor 1 conclusion: [Higher / Moderate / Lower probability of compromise from this factor + brief rationale]

## Factor 2 - Unauthorized person who used PHI or to whom disclosed

- **Recipient identity** (or "unknown - exfiltration to external actor"):
- **Recipient HIPAA status** (CE, BA bound by BAA, workforce member with confidentiality obligations, external party with no obligations):
- **Recipient incentive to misuse** (financial gain, identity theft, curiosity, accidental):
- **Recipient cooperation** (returned/destroyed PHI with written confirmation? acknowledged?):

Factor 2 conclusion: [Higher / Moderate / Lower probability of compromise from this factor + brief rationale]

## Factor 3 - Whether PHI was actually acquired or viewed

- **Evidence of access**: (forensic logs, system audit trail, file access timestamps, network exfiltration indicators):
- **Evidence of viewing** (not just opportunity to access):
- **Evidence of acquisition** (download, screenshot, print, copy, exfiltration):
- **Forensic capability available** (was forensic capture performed? by whom? findings?):
- **Theoretical access only** vs **demonstrated access**:

Factor 3 conclusion: [Higher / Moderate / Lower probability of compromise from this factor + brief rationale]

## Factor 4 - Extent to which risk has been mitigated

- **PHI recovered** (Y/N - how, with what assurance):
- **Recipient destruction certificate** (Y/N - obtained in writing? from whom?):
- **Encryption status at time of incident** (consider for residual risk):
- **Credential rotation, access revocation, system rebuild** (Y/N - completed when):
- **Compensating controls now in place**:
- **Monitoring for misuse** (credit monitoring offered? identity protection?):

Factor 4 conclusion: [Higher / Moderate / Lower probability of compromise from this factor + brief rationale]

## Overall determination

Based on the 4 factors taken together:

- [ ] **Low probability of compromise has been demonstrated.** No notification required under 45 CFR 164.402. Retain this assessment.
- [ ] **Low probability of compromise CANNOT be demonstrated.** This is a **breach** requiring notification per 45 CFR 164.404 / 164.406 / 164.408 / 164.410.

### Rationale (required regardless of determination)

(Explain how the 4 factors weighed together. If determination is "low probability," explain specifically why the presumption of breach is rebutted. Do not rely on harm theory - the standard is low probability of compromise.)

### If determination is BREACH

Document the next-step plan:

| Recipient | Deadline | Owner | Status |
|---|---|---|---|
| Affected individuals | 60 days from discovery: [date] | Privacy Officer | |
| HHS OCR (if ≥ 500 individuals affected) | 60 days from discovery: [date] | Privacy Officer | |
| HHS OCR (if < 500 affected, annual submission) | 60 days after year end: [date] | Privacy Officer | |
| Media (if ≥ 500 in a State/jurisdiction) | 60 days from discovery: [date] | Communications + Privacy Officer | |
| BA → CE notification (if we are the BA) | Per BAA: [timing] | BA | |
| Law enforcement (if applicable) | | | |
| Counsel | Immediate | | |
| Cyber-insurance carrier (if applicable) | Per policy | | |

### Engagement of counsel

- [ ] Counsel reviewed this assessment and concurs with determination
- [ ] Counsel name + date: ____________________

## Sign-offs

| Role | Name | Signature / attestation | Date |
|---|---|---|---|
| Assessor | | | |
| Privacy Officer | | | |
| Security Officer | (if applicable) | | |
| Counsel | (recommended) | | |

## Retention

Retain this completed assessment for **6 years** per 45 CFR 164.530(j), along with any supporting forensic, communication, and remediation evidence. Apply legal hold if litigation or OCR investigation is reasonably anticipated.
