# BAA Review (45 CFR 164.504(e))

## Scope

A Business Associate Agreement (BAA) is the contract required between a covered entity (CE) and a business associate (BA), and between a BA and a subcontractor BA, whenever PHI is used or disclosed to the BA on behalf of the CE.

**Without a BAA, the disclosure to the BA is itself a Privacy Rule violation.** This is a leading audit finding category.

## Required clauses (164.504(e)(2))

A BAA must, at minimum:

1. **Establish permitted uses and disclosures** of PHI by the BA - the BAA cannot permit uses or disclosures that would violate the Privacy Rule if done by the CE
2. **Prohibit other uses and disclosures** except as permitted, required by the contract, or required by law
3. **Require appropriate safeguards** (administrative, physical, technical) to prevent impermissible use or disclosure, including compliance with the **Security Rule** with respect to electronic PHI (ePHI)
4. **Require reporting** to the CE of any use or disclosure not provided for by the BAA, of any security incident of which the BA becomes aware, and of any breach of unsecured PHI as required by 164.410
5. **Require flow-down to subcontractors** - any subcontractor that creates, receives, maintains, or transmits PHI on behalf of the BA must agree to the same restrictions and conditions
6. **Make PHI available** to the individual, for amendment, and for accounting of disclosures as required by 164.524 / 164.526 / 164.528
7. **Make internal practices, books, and records available to HHS** for purposes of determining the CE's compliance
8. **Return or destroy PHI** at termination of the contract; if not feasible, extend protections and limit further uses
9. **Authorize termination** by the CE if the CE determines the BA has violated a material term of the BAA

## Common gaps (work this list during review)

| Gap | Why it matters | Redline |
|---|---|---|
| **Breach notification timing beyond 60 days, or "as required by law"** | CE has its own 60-day deadline from discovery; the BA's notification has to be fast enough to let the CE meet that | Set BA → CE notice at 24-72 hours of discovery (commonly negotiated to 5 business days; defend the shorter end) |
| **Security incident reporting limited to "successful" incidents** | All security incidents must be reportable per Security Rule; many BAAs try to limit to incidents involving PHI | Require reporting of any security incident; allow categorized summary reporting for unsuccessful attempts (port scans, etc.) but require detailed reporting for any incident involving PHI or systems handling PHI |
| **Subcontractor flow-down weakened** | Required by 164.504(e)(5); some BAAs water it down to "substantially similar" | Require BA to have written agreements with subcontractors that are at least as protective as this BAA, and to provide them on request |
| **Indemnification missing or one-way** | Allocates risk for breach costs - notification, credit monitoring, OCR penalties, litigation | Mutual indemnification for breach of BAA; carve out gross negligence / willful misconduct |
| **Insurance requirements missing** | Cyber liability + tech E&O typical for BAs handling material PHI volume | Require specific cyber liability coverage at a level proportional to PHI volume and sensitivity |
| **Audit rights missing or narrow** | CE may need to inspect BA's safeguards; often resisted as "operational burden" | Reasonable audit on notice; SOC 2 Type II + HITRUST in lieu of on-site is common compromise |
| **Return / destruction at termination weak** | "If not feasible to return / destroy, extend protections" can become a forever-clause | Define "not feasible" tightly; require categorical destruction certificate; require return / destruction status report annually until purged |
| **De-identification clause that allows BA to de-identify for its own use** | BA may want to retain de-identified data for product improvement; permitted under Privacy Rule but should be explicit in the BAA | If allowed, require Safe Harbor or Expert Determination, prohibit re-identification, prohibit downstream sale; if not allowed, exclude explicitly |
| **AI / ML training carve-out** | BA may want to train models on PHI; not permitted without explicit authorization | Explicit clause: BA may not use PHI to train, fine-tune, or evaluate models for any purpose other than providing services to this CE, without separate written authorization |
| **Choice of law / venue unfavorable** | Affects enforcement | Negotiable; depends on CE's posture |
| **Notice provisions to wrong address** | Real-world incident-response failures | Verify and update annually |
| **Subpoena handling** | BA may receive a subpoena for PHI; must coordinate with CE | Require BA to notify CE within X days (or as soon as legally permitted) before producing PHI in response to legal process, to allow CE to seek a protective order |

## Subcontractor flow-down (164.504(e)(5))

Often missed in practice. A BA cannot expand its own permitted uses by routing PHI through a subcontractor with looser obligations.

Practical check:
- BA identifies all subcontractors that touch PHI
- Each has a signed BA-subcontractor agreement at least as protective as the CE-BA BAA
- Subcontractor list is maintained and made available to CE on reasonable request

Cloud, hosting, email, MFA, monitoring, log shipping, AI services, support outsourcing, backup providers - **all** of these are BAs if they touch PHI.

## When is a BAA NOT required?

- **Conduits** that transport PHI but do not access it other than incidentally - e.g., the US Postal Service, an ISP, a courier service. OCR construes "conduit" narrowly; data hosting and processing services are **not** conduits even if they claim they don't read the data
- **CE → CE for treatment, payment, operations** (164.506) - both are CEs, no BA relationship
- **Workforce members** of a CE - they are not BAs
- **De-identified data only** - per the two HIPAA de-identification methods; see [`de-identification.md`](de-identification.md)
- **Disclosures required by law** to recipients with statutory authority (public health authority, oversight)

## CE vs BA vs Subcontractor BA - quick decision

```
Does the entity create, receive, maintain, or transmit PHI on behalf of a CE?
├── No → not a BA
└── Yes → BA
    ├── Is the entity itself a CE acting in its CE capacity? → BAA not required for that capacity
    └── Does the BA hand PHI to anyone else who creates, receives, maintains, or
        transmits PHI on its behalf? → Each such party is a Subcontractor BA
        and must have a BA-Subcontractor agreement
```

## Working with a BAA review

Use the [`../templates/baa-review-checklist.md`](../templates/baa-review-checklist.md) template for any non-trivial BAA. Output for each clause: present? language meets minimum? language meets internal standard? gap requires redline?

## Defer to counsel when

- Negotiating indemnification, liability caps, or insurance
- Subpoena, e-discovery, or legal-hold language
- Choice-of-law or jurisdiction questions
- Any executed BAA with material gaps - amendment requires counsel
- BAAs spanning multiple jurisdictions (international transfers, state law overlays)
- BAA where the counterparty refuses required HIPAA clauses - this is a deal-stop, not a negotiation
