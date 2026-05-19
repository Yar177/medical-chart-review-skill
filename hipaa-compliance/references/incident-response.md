# Incident Response

## Security incident vs reportable breach - the key distinction

| Term | Definition | Trigger |
|---|---|---|
| **Security incident** (Security Rule, 164.304) | Attempted or successful unauthorized access, use, disclosure, modification, or destruction of information OR interference with system operations in an information system | Any security event - including port scans, login failure spikes, IDS alerts |
| **Breach** (Breach Notification Rule, 164.402) | Impermissible use or disclosure of unsecured PHI presumed to compromise security/privacy unless low probability demonstrated via 4-factor assessment | A security incident **involving PHI** that cannot be shown to have low probability of compromise |

Every breach is a security incident. Not every security incident is a breach.

## IR program elements

A HIPAA-compliant IR program must:

1. **Identify** suspected and known security incidents
2. **Respond** to them according to documented procedures
3. **Mitigate** harmful effects to the extent practicable
4. **Document** incidents and outcomes

Cite: 164.308(a)(6) - Required standard.

## IR playbook phases

Standard NIST 800-61 phases, mapped to HIPAA-specific actions:

### Phase 1 - Preparation (before any incident)

- Documented IR plan + playbooks for top scenarios
- IR team with named roles + 24x7 contact tree
- Tooling in place (SIEM, EDR, log aggregation, forensic capture, communication channels)
- BAAs with vendors include incident notification clauses (BA → CE notification timing)
- Counsel engagement protocol pre-established
- Tabletop exercises at least annually; live drill periodically
- Communication templates pre-drafted (internal, individual, media, OCR)
- Backup and DR tested - restore is part of IR

### Phase 2 - Detection and analysis

Triggers:
- SIEM / IDS / EDR alerts
- User reports (phishing, lost device, suspicious activity)
- Vendor reports (BA reports incident to CE; or downstream BA reports to BA)
- Audit log review
- External notification (researcher, law enforcement, customer)

Initial triage questions:
- What system or data is affected?
- Is ePHI involved or potentially involved?
- Is the incident ongoing or contained?
- Who has access to the affected system?
- What is the apparent vector?

Output: classification - security incident only, suspected ePHI involvement, or confirmed ePHI involvement.

### Phase 3 - Containment

Short-term:
- Isolate affected systems (network segmentation, account disable)
- Preserve evidence before remediation - **do not** wipe-and-reimage before forensic capture
- Capture volatile data (memory, network connections, logged-in users)
- Preserve logs - centralize, prevent rollover, hash and timestamp

Long-term:
- Apply patches / configuration changes
- Rotate compromised credentials
- Rebuild from known-good baselines
- Implement compensating controls before bringing systems back online

### Phase 4 - Eradication

- Remove malware / persistence mechanisms
- Close exploited vulnerabilities
- Validate eradication before recovery
- Document evidence of eradication (timestamps, command output, IDS confirmation)

### Phase 5 - Recovery

- Restore from clean backups
- Phased return to production with monitoring
- Verify integrity and availability of restored ePHI
- Heightened monitoring for a defined post-incident window

### Phase 6 - Post-incident

- After-action review within a documented window (commonly 30 days)
- Lessons learned documented and tracked to closure
- IR plan and playbooks updated
- Training updated
- Workforce sanctions applied if applicable
- Risk analysis updated if the incident reveals material risk

## Breach determination decision tree

Run this AFTER incident is contained enough to assess scope. Coordinate with privacy officer and counsel.

```
Was there an impermissible use or disclosure of PHI?
├── No → not a breach; document the analysis
└── Yes
    └── Was the PHI Unsecured (not FIPS-encrypted or destroyed)?
        ├── No (encrypted) → safe harbor; document
        └── Yes → run 4-factor risk assessment (see breach-notification.md)
            ├── Low probability of compromise (documented, signed) →
            │   no notification required; retain documentation 6 years
            └── Cannot demonstrate low probability → BREACH
                ├── Affected individuals < 500 → annual OCR submission;
                │   individual notice within 60 days of discovery
                └── Affected individuals ≥ 500 → OCR within 60 days;
                    media notice within 60 days for any State/jurisdiction
                    with 500+ affected; individual notice within 60 days
```

Reference: [`breach-notification.md`](breach-notification.md) for full breach notification mechanics, [`../templates/breach-risk-assessment.md`](../templates/breach-risk-assessment.md) for the 4-factor worksheet.

## Forensic preservation

- Engage forensic capability early - in-house if mature, external IR firm if not (pre-arranged retainer recommended)
- Chain of custody for any evidence handled
- Image affected systems before remediation when forensic value warrants
- Centralize and lock logs - prevent rotation; hash on capture
- Document every action with timestamp and operator
- Preserve communications about the incident under legal hold

## OCR coordination

If the incident is a reportable breach:

- OCR submission via the OCR Breach Portal
- Use accurate, complete information; avoid speculation that may need correction later
- Single point of contact for follow-up OCR inquiries (typically counsel + privacy officer)
- All written and verbal exchanges documented
- Cooperation expected; lack of cooperation is itself a finding

If OCR opens a compliance review:

- Engage counsel immediately
- Litigation/audit hold
- Treat as the audit-prep scenario in [`ocr-audit-prep.md`](ocr-audit-prep.md)

## BA-side IR (when you are the BA)

- BA → CE notification per the BAA (commonly faster than the 60-day Breach Rule floor; 24-72 hours typical; check BAA)
- BA does not directly notify individuals unless the BAA delegates it; default is the CE notifies
- Provide CE with sufficient information for the CE's 4-factor assessment + individual notice content (categories of PHI, identities affected, dates, mitigation)
- Cooperate with the CE's investigation - this is a Required BAA term

## Ransomware - default posture

OCR guidance: presence of ransomware on a system containing ePHI is a security incident, **and the access required for the ransomware to operate is presumed an impermissible use of PHI - therefore a breach** - unless the entity can demonstrate low probability of compromise via the 4-factor assessment.

Most ransomware incidents on ePHI systems should be treated as breaches absent very strong evidence to the contrary (e.g., systems that did not store PHI, ePHI was encrypted in a manner the ransomware did not compromise, full forensic confirmation of no access).

## Common engineering pitfalls

- No IR plan, or IR plan exists but workforce doesn't know who to call
- Wipe and rebuild before forensic capture (destroys evidence + ability to determine scope)
- 4-factor assessment never written down ("we decided it's not a breach")
- BA → CE notification timing in BAA at 60 days (leaves CE no margin)
- Treating ransomware as "not a breach because the data wasn't exfiltrated" without 4-factor + forensic basis
- No tabletop drills - first practice is during a real incident
- Logs roll over before they can be examined
- No pre-arranged forensic IR firm retainer - hours/days lost finding one mid-incident
- Communications about the incident on channels that are themselves compromised
- Internal communications not preserved for legal hold

## Defer to counsel + privacy officer + security officer when

- Initial classification of an incident as potentially involving PHI
- Breach determination after 4-factor assessment
- Any external communication about the incident (workforce, customers, media, regulators)
- Engagement with law enforcement
- OCR notification and follow-up
- Cyber-insurance claim
- Workforce sanctions
- Any BA dispute about notification responsibility
