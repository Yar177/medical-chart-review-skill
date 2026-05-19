# Privacy Rule (45 CFR Part 164 Subpart E)

> Builder / compliance-officer view. For the clinical-reviewer view of HIPAA (18 identifier list applied during chart abstraction), see the sibling `medical-chart-review` skill's `references/hipaa-privacy.md`.

## Scope

The Privacy Rule governs **uses and disclosures of PHI** by covered entities (CEs) and business associates (BAs). It defines patient rights with respect to their PHI and the conditions under which PHI may be used or disclosed without authorization.

**Covered entities:** health plans, healthcare clearinghouses, healthcare providers who transmit any health information electronically in connection with a HIPAA transaction.

**Business associates:** any person or entity that performs functions or activities involving the use or disclosure of PHI on behalf of a CE. As of HITECH (2009) / Omnibus Rule (2013), BAs are **directly liable** for Privacy and Security Rule violations.

**PHI** is individually identifiable health information held or transmitted by a CE or BA, in any form or medium. Past, present, or future. Includes demographic and payment information when linked to health information.

## Uses and disclosures

### Permitted without authorization

| Category | Notes | Citation |
|---|---|---|
| **Treatment, Payment, and Operations (TPO)** | Disclosures among providers for treatment; to insurers for payment; for internal QA, training, accreditation, audits | 45 CFR 164.506 |
| **To the individual** | Subject's own PHI | 45 CFR 164.502(a)(1)(i) |
| **Public health activities** | Reporting to PHA, disease surveillance, FDA-regulated product reports | 45 CFR 164.512(b) |
| **Required by law** | Subpoenas with safeguards, court orders, mandatory reporting (abuse, gunshot) | 45 CFR 164.512(a) |
| **Health oversight** | Audits, investigations, inspections by oversight agencies | 45 CFR 164.512(d) |
| **Judicial / administrative proceedings** | Court orders, subpoenas with notice + protective order | 45 CFR 164.512(e) |
| **Law enforcement** | Limited categories - identification, victims, decedents, crime on premises | 45 CFR 164.512(f) |
| **Decedents** | To coroners, medical examiners, funeral directors | 45 CFR 164.512(g) |
| **Research** | With IRB / Privacy Board waiver, or with authorization, or with limited data set + DUA | 45 CFR 164.512(i) |
| **Serious threat to health or safety** | To prevent or lessen | 45 CFR 164.512(j) |
| **Workers' compensation** | As authorized by state law | 45 CFR 164.512(l) |

### Require authorization

- **Psychotherapy notes** (always - even for TPO with few exceptions per 164.508(a)(2))
- **Marketing** with limited exceptions (face-to-face, promotional gifts of nominal value) - 164.508(a)(3)
- **Sale of PHI** - 164.508(a)(4)
- **Most research uses** without IRB / Privacy Board waiver

### Authorization requirements (164.508(c))

Valid authorization must contain:
1. Specific description of information
2. Specific identification of who may disclose
3. Specific identification of who may receive
4. Description of each purpose
5. Expiration date or event
6. Signature and date
7. Right to revoke + how
8. Conditioning statement (services not contingent on authorization, with few exceptions)
9. Re-disclosure statement (PHI may no longer be protected once disclosed to a non-CE)
10. Plain language

## Minimum necessary

CEs and BAs must make reasonable efforts to limit PHI use, disclosure, and request to the **minimum necessary** to accomplish the intended purpose. 45 CFR 164.502(b).

**Does not apply to:**
- Disclosures to / requests by a healthcare provider for treatment
- Disclosures to the individual
- Uses or disclosures pursuant to an authorization
- Disclosures to HHS for compliance / enforcement
- Uses or disclosures required by law

**In practice for engineering:**
- Role-based access controls (RBAC) sized to the minimum necessary for each role
- Default to deny; grant least privilege
- Field-level minimization in queries, exports, API responses, AI prompts
- Periodic review of access against current role

## Notice of Privacy Practices (NPP)

CEs must provide patients with an NPP describing:
- Uses and disclosures the CE may make
- The individual's rights
- The CE's legal duties
- A point of contact for complaints

Direct treatment providers must provide at first service delivery and make a good-faith effort to obtain written acknowledgment. 45 CFR 164.520.

## Patient rights

| Right | Citation | Notes |
|---|---|---|
| **Access** to PHI | 164.524 | 30 days, one 30-day extension; electronic if maintained electronically; fees limited to labor + supplies |
| **Amendment** | 164.526 | CE may deny under narrow conditions; patient may submit statement of disagreement |
| **Accounting of disclosures** | 164.528 | 6 years back; excludes TPO, to individual, authorized, incidental |
| **Restriction request** | 164.522(a) | CE need not agree EXCEPT must agree to restriction on disclosure to a health plan for items paid in full out-of-pocket |
| **Confidential communications** | 164.522(b) | Alternative means or location for communications |
| **Complaint to CE and to OCR** | 164.530(d) | No retaliation permitted |

## Marketing and fundraising

**Marketing** (paid communications encouraging purchase of a product or service) requires authorization with limited exceptions. The exceptions are tightly scoped - check the definition before relying on them.

**Fundraising** can use limited categories of PHI (demographics, dates of service, department, treating physician, outcome, insurance status) for the CE's own fundraising **without authorization** if the NPP describes it AND the communication includes an opt-out. 164.514(f).

## Re-disclosure caution

Once PHI is disclosed to a non-CE / non-BA, HIPAA generally no longer protects it. The disclosing party should consider whether other laws (state, contractual) impose downstream restrictions.

## Common engineering pitfalls

- **Calling something "TPO" to bypass authorization when it's actually marketing** - especially anything with a third-party economic incentive
- **Sending PHI to a third-party analytics, advertising, or session-replay service without a BAA** - the December 2022 OCR bulletin on tracking technologies makes this an active enforcement target (status varies; check current OCR guidance + counsel)
- **Treating minimum-necessary as "all data in the same table"** - it is per-purpose and per-role
- **NPP not updated** after a material change in uses / disclosures
- **No process for patient access requests** - leading common-finding category in OCR audits

## Defer to counsel + privacy officer when

- Any law-enforcement disclosure request
- Subpoena or court order
- Research use without an existing IRB / Privacy Board determination
- Marketing or fundraising that doesn't squarely fit an exception
- Cross-border / multi-jurisdiction disclosure
- Any psychotherapy notes question
- Substance-use disorder records (42 CFR Part 2 is stricter than HIPAA - see `state-laws-and-overlap.md`)
