# OCR Audit Preparation

## Background

The HHS Office for Civil Rights (OCR) conducts audits of HIPAA compliance under HITECH §13411 authority. The most-cited reference framework is the **Phase 2 HIPAA Audit Program (2016-2017)**. OCR has signaled the next round of audits is in development (status varies; check current OCR publications). Even between formal audit cycles, OCR uses the Phase 2 protocol structure in compliance reviews triggered by complaints and breach reports.

A modern audit-prep program assumes the Phase 2 protocol items will be requested with short turnaround (typically 10 business days from initial request).

## Phase 2 audit protocol - structure

The protocol organizes requests into three categories:

1. **Privacy Rule audit items** - Notice of Privacy Practices, patient access, authorization, accounting of disclosures, minimum necessary
2. **Security Rule audit items** - risk analysis, risk management, designation of security officer, workforce training, contingency plan, transmission security
3. **Breach Notification Rule audit items** - breach risk assessment process, notification timing and content, BA notification

Each item asks for **policies + evidence of operation**. OCR consistently observes that entities have policies on paper but cannot produce evidence the policies operate (training completion records, sanction logs, risk-analysis updates, access reviews, breach assessment documentation).

## Common findings (across Phase 1, Phase 2, and complaint-driven reviews)

| Finding | Frequency | Typical root cause |
|---|---|---|
| **Inadequate risk analysis** | Highest | Scope limited to one app; risk analysis not updated after material change |
| **Deficient risk management** | High | Risks identified but not remediated; no documented risk acceptance |
| **Inadequate BAAs** | High | Missing BAAs; outdated language; missing flow-down |
| **Insufficient information system activity review** | High | Logs exist but not reviewed; no documented review process |
| **Missing or weak access controls** | High | No periodic recertification; standing admin; shared accounts |
| **Workforce training gaps** | Medium | No annual refresher; no role-specific training; no completion records |
| **Inadequate audit controls** | Medium | Logs missing required fields; retention < 6 years; logs not integrity-protected |
| **Missing security incident response procedures** | Medium | No documented IR; no IR drills; no after-action records |
| **Encryption gaps** | Medium | Encryption at edge but plaintext between services; backups unencrypted |
| **Insufficient breach risk assessments** | Medium | No 4-factor assessment documented; assessment performed but not retained |
| **Patient access delays / denials** | Medium | No process for individual access requests; >30 day responses |
| **Marketing / fundraising without authorization** | Medium | Use of PHI for marketing without valid authorization; NPP doesn't describe fundraising |

## Evidence inventory - what OCR asks for

Maintain a current, retrievable inventory of the following. The [`../templates/ocr-audit-evidence-binder.md`](../templates/ocr-audit-evidence-binder.md) provides the binder structure.

### Foundational

- Designation of Privacy Officer + Security Officer (current + history)
- Current Notice of Privacy Practices (NPP) + versions in effect for the audit window + acknowledgment process
- Current policies and procedures library (privacy + security + breach) + version history + last review date
- Most recent risk analysis (and the ones for the prior 3 years, with the material-change triggers documented)
- Most recent risk management plan with status by finding

### Workforce

- Workforce training program description + curriculum + cadence
- Training completion records for the audit window
- Sanction policy + sanction log for the audit window
- Workforce access roster + role catalog + most recent periodic access review

### Vendors

- Vendor inventory of every entity that creates, receives, maintains, or transmits PHI on behalf of the entity
- Signed BAA for each entity
- Subcontractor BA flow-down evidence
- Vendor risk-review records

### Operational

- Audit log review process documentation + sampled review records
- Backup and DR plan + most recent successful restore test
- Encryption inventory by ePHI storage location
- Incident response plan + drill records + actual incident records for the audit window
- Breach risk assessments for every reported impermissible use or disclosure (whether or not determined to be a breach)
- Breach notifications sent (where applicable) - letters, OCR submissions, media notices

### Patient rights

- Individual access request log + sample responses + response times
- Amendment request log
- Accounting of disclosures process + sample
- Complaint log + dispositions

### Technical evidence

- Network diagrams showing ePHI flow
- Authentication architecture (IdP, MFA, federation)
- Encryption configuration evidence (FIPS validation certificates, KMS policies)
- Logging architecture + retention configuration
- Access control configuration (RBAC, attribute filters)
- Public-facing service configuration (TLS versions, certs, headers)

## Audit-prep readiness check

A useful self-test: pick three Phase 2 protocol items at random per quarter and run them against your current evidence inventory. Time the response. If you cannot produce the evidence within an audit-realistic window (10 business days), close the gap before the next quarter.

## What OCR does NOT require

- A specific product, framework, or certification (HITRUST, SOC 2 are useful but not required)
- A specific technology choice (no required cipher, no required IdP)
- Real-time perfection - what OCR looks for is a working program that identifies, manages, and remediates risk

## Active enforcement areas to track

(Status varies; check current OCR publications and press releases.)

- **Right of access** - settlement track record for delayed or denied individual access requests
- **Risk analysis** - perennial top finding
- **Web tracking technologies** - 2022 bulletin and subsequent litigation; current posture should be checked
- **Ransomware as a breach** - default presumption is breach unless 4-factor low-probability demonstrated
- **HIPAA Security Rule update (2025 NPRM activity)** - significant proposed changes including more prescriptive technical safeguards; track final rule and effective dates
- **AI / ML and PHI** - newer enforcement area; defer to counsel for current posture

## When an audit notice arrives

1. **Acknowledge promptly** - within the requested timeframe
2. **Engage counsel + privacy officer + security officer immediately**
3. **Preserve evidence** - issue a litigation/audit hold to relevant systems and personnel
4. **Single point of contact** for all OCR communications
5. **Provide complete, accurate, responsive answers** - over-production and under-production both create risk
6. **Document the engagement** - record every request, every response, every decision

## Common pitfalls

- Policy library that doesn't match practice (OCR asks for both)
- Risk analysis exists but scope is too narrow (just the app, not all ePHI flows)
- BAA inventory incomplete or out of date
- No periodic-access-review evidence
- Training records lost to vendor turnover
- Breach risk assessments performed verbally, never written down
- Trying to fix gaps during the audit window rather than before

## Defer to counsel + privacy officer when

- An audit notice is received
- A complaint is received from a patient, workforce member, or BA
- A breach is identified that may trigger a compliance review
- A finding from a self-assessment rises to the level of likely non-compliance
- Any communication with OCR
