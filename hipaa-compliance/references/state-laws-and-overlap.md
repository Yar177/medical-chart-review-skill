# State Laws and Overlap (high-level)

> **Scope of this file:** high-level pointer to the most commonly encountered overlapping regimes. **Deeper state-by-state work requires counsel and a state-specific compliance resource.** This file does not substitute for legal analysis.

## Preemption baseline

HIPAA generally preempts contrary state laws **unless** the state law is **more stringent** than HIPAA. "More stringent" means it provides greater protection to the individual, greater rights of access, or stricter standards of care for PHI. 45 CFR 160.203.

In practice that means HIPAA is a **floor**, not a ceiling. Engineering and compliance design should consider:

1. HIPAA requirements (federal floor)
2. Any state law more stringent than HIPAA in any relevant state
3. Any federal regime more stringent than HIPAA for specific data types (42 CFR Part 2 for SUD)
4. International requirements if any users / data subjects are outside the US (GDPR, others)

## Major overlapping regimes

### 42 CFR Part 2 - Substance Use Disorder records

| Aspect | Part 2 | HIPAA |
|---|---|---|
| Scope | SUD treatment records from federally-assisted programs | All PHI from CEs/BAs |
| Disclosure standard | Patient consent required for most disclosures, including TPO (with 2024 amendments harmonizing more with HIPAA) | TPO permitted without authorization |
| Re-disclosure | Recipient must agree to restrictions on re-disclosure | Generally not protected once disclosed to non-CE |
| Penalties | Criminal + civil | Civil + criminal (in some categories) |

**Engineering implication:** SUD records require separate handling, separate consent management, separate disclosure tracking. Mixing them in a general PHI store creates compliance risk. The 2024 final rule aligned several requirements with HIPAA (notice content, breach notification, civil + criminal penalties) but **patient consent for disclosure remains more stringent than HIPAA**.

Defer to counsel for any pipeline that handles SUD records.

### California - CMIA + CCPA / CPRA

**Confidentiality of Medical Information Act (CMIA)** - California state medical privacy law. More stringent than HIPAA in several areas (authorization specificity, marketing, employer access). Applies to providers and certain entities not covered by HIPAA.

**California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA)** - general consumer privacy law. Contains an exemption for "medical information" governed by CMIA and PHI governed by HIPAA, **but** the exemption is **for the data, not the entity** - other (non-PHI / non-medical-information) data the same entity holds may still be CCPA-regulated.

**Engineering implication:** California users add CMIA on top of HIPAA + CCPA for any non-PHI data. Consent and disclosure tracking must accommodate CMIA's specifics.

### Other state medical privacy regimes to flag

Many states have medical privacy laws layered on top of HIPAA. Specific high-impact areas include:

- **Mental health records** - many states (Texas, New York, others) impose extra restrictions
- **HIV / AIDS** - many states require specific consent for disclosure
- **Genetic information** - GINA federally; many state-level overlays (Florida, Illinois, others)
- **Reproductive health** - rapidly changing regulatory landscape post-Dobbs; OCR 2024 rule restricts certain disclosures of reproductive health information; multiple state-level statutes
- **Minors** - state-specific consent rules; minor mature-treatment exceptions vary widely
- **State breach notification laws** - most states have their own breach notification laws (often broader than HIPAA's PHI scope - covering SSN, financial, biometric, login credentials)

For any of these categories or any state-specific question, **engage counsel**.

### GDPR - EU General Data Protection Regulation

Applies if:
- The entity is established in the EU, OR
- The entity offers goods/services to data subjects in the EU, OR
- The entity monitors the behavior of data subjects in the EU

For US-based healthcare entities, GDPR most commonly arises with:
- EU users using a US patient portal
- Telehealth across borders
- Research involving EU subjects
- Multi-national clinical trials
- EU-based workforce accessing US PHI

GDPR is generally more stringent than HIPAA in several areas (data subject rights, lawful basis, cross-border transfer restrictions, data protection officer requirements, breach notification - 72 hours vs HIPAA's 60 days, fines).

International transfer to the US requires a valid transfer mechanism (Standard Contractual Clauses, Data Privacy Framework if applicable, Binding Corporate Rules). The legal landscape on US transfers has been litigated repeatedly - defer to counsel.

### Federal overlays beyond HIPAA

- **FERPA** - educational records; intersection with school health records
- **GINA** - genetic information non-discrimination
- **ADA** - employer access to health information
- **FTC Act §5** - unfair / deceptive practices; the FTC pursues health data practices that fall outside HIPAA (e.g., consumer health apps, recently enforced)
- **FTC Health Breach Notification Rule** - applies to vendors of personal health records (PHRs) and related entities **not** covered by HIPAA
- **State unfair-trade-practice statutes** - state AGs often co-enforce
- **HHS Section 1557 (ACA)** - nondiscrimination including in patient-facing technology
- **Information Blocking Rule (ONC)** - prohibits actors from interfering with access, exchange, or use of electronic health information; not a privacy rule but interacts with disclosure design

## Decision pattern for engineering

When designing a feature or pipeline that touches PHI:

1. **What is the data?** PHI? SUD? Mental health? HIV? Genetic? Reproductive? Minors?
2. **Where are the users / data subjects?** US states? Outside US?
3. **Who is the entity?** CE? BA? Subcontractor BA? Non-HIPAA entity offering health-adjacent services?
4. **What is the use?** TPO? Marketing? Research? Quality? Reporting to a non-CE?
5. Apply HIPAA AS THE FLOOR; layer the more stringent applicable regimes on top.
6. Escalate to counsel when ANY of the heightened categories appears, or when multiple regimes apply.

## Common engineering pitfalls

- Treating CCPA exemption as "California is fully covered by HIPAA" - the exemption is data-specific, not entity-wide
- Designing a single consent flow for all data when SUD or mental health requires separate consent
- Missing state breach notification deadlines because the team only tracked the HIPAA 60-day clock - state laws often shorter and broader in scope
- Failing to identify EU traffic and falling under GDPR by accident
- Storing reproductive health data alongside other PHI in a way that prevents the targeted disclosure controls required by the 2024 OCR rule
- Treating the FTC as "not our regulator" when offering consumer-facing health services outside the HIPAA boundary
- Ignoring 1557 / information-blocking when designing patient-facing features

## Defer to counsel for

- Any of the heightened data categories (SUD, mental health, HIV, genetic, reproductive, minors)
- Any state-specific question beyond the high-level pointer
- Any international data subject
- Any non-HIPAA federal regime (FTC, ONC, 1557, FERPA, GINA)
- Multi-jurisdiction breach analysis
- Conflicts between regimes
- Any cross-border data transfer
