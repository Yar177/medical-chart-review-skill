# Breach Notification Rule (45 CFR Part 164 Subpart D)

## Scope

Requires CEs and BAs to provide notification following a **breach of unsecured PHI**. Applies whenever there is an acquisition, access, use, or disclosure of PHI in a manner not permitted by the Privacy Rule that compromises the security or privacy of the PHI.

## Key definitions

- **Breach** (164.402): impermissible use or disclosure of PHI presumed to be a breach UNLESS the CE or BA demonstrates a **low probability that the PHI has been compromised** based on the 4-factor risk assessment.
- **Unsecured PHI**: PHI not rendered unusable, unreadable, or indecipherable to unauthorized persons through the use of a technology or methodology specified by HHS. As of writing, that means **encryption** (FIPS-validated) at rest and in transit, or **destruction** per NIST 800-88. PHI rendered unsecured under those methods is **not** subject to the breach rule when the unauthorized event occurs to the unsecured form.
- **Discovery**: a breach is treated as discovered on the first day it is known to the CE/BA, or by exercising reasonable diligence would have been known.

## The 4-factor risk assessment (164.402(2))

An impermissible use or disclosure is presumed a breach unless the CE/BA demonstrates a low probability that the PHI has been compromised based on a risk assessment of at least these four factors. Document each factor explicitly.

| # | Factor | Questions to answer |
|---|---|---|
| 1 | **Nature and extent of PHI involved** | Types of identifiers? Sensitive categories (mental health, SUD, HIV, genetic, financial, SSN)? Likelihood of re-identification? Volume? |
| 2 | **Unauthorized person who used PHI or to whom disclosed** | Another CE / BA (bound by HIPAA)? An individual with obligations of confidentiality? An external party with no legal duty? |
| 3 | **Whether PHI was actually acquired or viewed** | Forensic evidence of access? Logs, file system metadata, exfiltration indicators? Or only a theoretical opportunity? |
| 4 | **Extent to which risk has been mitigated** | Recovered? Recipient confirmed destruction in writing? Encryption status at time of incident? Compensating controls? |

**Output:** a written determination - "low probability of compromise" or "breach" - signed by the privacy officer with supporting evidence retained for 6 years.

> **Pitfall:** The standard is "low probability of compromise," **not** "no harm shown." Do not let a BA argue out of breach notification on a harm theory.

## Notification timing and recipients

| Recipient | Trigger | Deadline | Citation |
|---|---|---|---|
| **Affected individuals** | Any breach of unsecured PHI | Without unreasonable delay, **no later than 60 calendar days** from discovery | 164.404 |
| **Media** | Breach affecting **500+ residents of a State or jurisdiction** | Same 60-day window; prominent media outlets serving the State/jurisdiction | 164.406 |
| **HHS OCR - large breach** | Breach affecting **500+ individuals** | Same 60-day window; submit via OCR breach portal | 164.408(b) |
| **HHS OCR - small breach** | Breach affecting **<500 individuals** | **Annual** submission, no later than 60 days after end of calendar year | 164.408(c) |
| **BA → CE notification** | BA discovers a breach | Without unreasonable delay, **no later than 60 days** from BA discovery; many BAAs require much faster (24-72 hours) | 164.410 |

## Required content of individual notice (164.404(c))

1. Brief description of what happened, including date of breach and date of discovery
2. Description of the types of unsecured PHI involved (categories - SSN, DOB, diagnosis - not the actual values)
3. Steps individuals should take to protect themselves
4. Brief description of what the CE is doing to investigate, mitigate harm, protect against further breaches
5. Contact procedures - toll-free number, email, website, postal address

**Delivery:**
- First-class mail to last known address, or
- Email if the individual has agreed to electronic notice and has not withdrawn the agreement
- **Substitute notice** if 10+ individuals' contact info is out of date: conspicuous web posting for 90 days OR major print/broadcast media, PLUS toll-free number active for 90 days

## Delays

Law enforcement may request a delay if notification would impede a criminal investigation. Delay is permitted if the request is in writing with a specified time period (up to 30 days; if oral, document the request).

## Documentation retention

CEs and BAs must retain documentation of:
- The 4-factor risk assessment for each impermissible use/disclosure
- Notification documentation (or rationale for non-notification)
- Burden of proof is on the CE/BA to demonstrate notification was made or that the impermissible use/disclosure did not constitute a breach

Retention: **6 years** from the date of creation or last in effect (Privacy Rule documentation standard, 164.530(j)).

## Penalties

Civil monetary penalties tiered by culpability (annual inflation-adjusted; verify current amounts at HHS):

| Tier | Knowledge | Per-violation range | Annual cap per category |
|---|---|---|---|
| 1 | Did not know / could not have known | Lower bound | Lower cap |
| 2 | Reasonable cause | Mid range | Mid cap |
| 3 | Willful neglect - corrected | Higher range | Higher cap |
| 4 | Willful neglect - not corrected | Highest range | Highest cap |

> Caps were restructured by HHS 2019 Notification of Enforcement Discretion. Use current OCR figures, not historic ones. Defer specific exposure analysis to counsel.

## Common engineering pitfalls

- **Treating an incident as not-a-breach without a 4-factor assessment** - even when the team believes "no PHI was actually accessed," the assessment must be documented
- **Counting the 60 days from "when we finished investigating" instead of from discovery** - the clock starts at discovery
- **Sending PHI in the notification letter** (categories, not values)
- **Forgetting BA → CE notification timing in the BAA** - most BAAs need to be tighter than 60 days for the CE to meet its own 60-day deadline
- **Missing the annual small-breach submission** - common audit finding
- **Encryption claim that isn't FIPS-validated** - the safe harbor only attaches to FIPS-validated encryption per HHS guidance
- **Encryption at rest claim where the database is encrypted but the backup tapes, logs, or developer laptops are not** - all storage locations
- **Logs that retain PHI for years past necessity** - expanded breach surface

## Decision tree (high-level)

```
Impermissible use / disclosure of PHI?
├── Yes - was the PHI Unsecured (not FIPS-encrypted or destroyed)?
│   ├── No (was encrypted) → Breach Notification Rule does NOT apply to that PHI
│   └── Yes (unsecured) → Run 4-factor risk assessment
│       ├── Low probability of compromise (documented) → No notification required;
│       │   retain documentation 6 years
│       └── Cannot demonstrate low probability → BREACH. Notify per timing table above.
└── No → Document the analysis; no breach
```

Always pair the decision tree with the `templates/breach-risk-assessment.md` worksheet.

## Defer to counsel + privacy officer when

- The 4-factor assessment is borderline
- A breach affects 500+ individuals (regulatory and PR posture)
- Law enforcement is involved
- A BA is the source of the breach and the CE/BA roles are contested
- The breach involves heightened-protection data (SUD/42 CFR Part 2, mental health, genetic, minors)
- Multi-jurisdiction (state breach laws often impose additional requirements)
