# Incident Response Playbook

> Operational template. Pair with [`../references/incident-response.md`](../references/incident-response.md). Tailor sections per system / scenario. Tabletop annually, drill periodically.

## 0. Activation

Activate this playbook on ANY of:

- SIEM / IDS / EDR alert involving an ePHI-handling system
- User report of suspected phishing, lost/stolen device, suspicious activity, unauthorized access
- Vendor (BA) report of incident
- Audit log review surfacing suspicious activity
- External notification (researcher, customer, law enforcement)
- Failed login spike or anomalous access pattern on ePHI systems

When in doubt, activate. De-escalation later is cheap; missed activation is not.

## 1. Incident Response team and contacts

| Role | Primary | Backup | Contact (24x7) |
|---|---|---|---|
| Incident Commander | | | |
| Security Officer | | | |
| Privacy Officer | | | |
| Counsel | | | |
| Communications | | | |
| Engineering on-call | | | |
| Forensics (in-house) | | | |
| Forensics (external IR firm) | (pre-arranged retainer) | | |
| Cyber-insurance carrier | | | |
| Executive sponsor | | | |
| Law enforcement liaison | | | |

> Maintain this contact tree out-of-band (printed + offline copy). Primary communication during an incident must use channels not themselves compromised.

## 2. Phase 1 - Detection and analysis

### Initial triage (Incident Commander, ≤ 30 min from activation)

- [ ] Classify severity (low / medium / high / critical) - default to high if PHI may be involved
- [ ] Identify affected systems
- [ ] Determine whether incident is ongoing or contained
- [ ] Notify IR team via out-of-band channel
- [ ] Open incident record (ticket / war-room / secure channel)
- [ ] Engage forensics if PHI may be involved
- [ ] Engage counsel if PHI may be involved or external party may need to be notified
- [ ] Engage executive sponsor if severity ≥ high

### Information to capture at activation

- Incident ID, date/time of detection, date/time of suspected occurrence
- Source of detection
- Systems affected
- Data potentially affected (categories - not values)
- Apparent vector
- Known timeline so far
- Initial responder

### Classification - is ePHI involved?

- [ ] No PHI in affected systems → handle as security incident only; document; continue with phases below as applicable
- [ ] PHI possibly in affected systems → treat as PHI-involved; engage privacy officer + counsel
- [ ] PHI confirmed in affected systems → PHI-involved; proceed with breach assessment in parallel with containment

## 3. Phase 2 - Containment

### Short-term

- [ ] Isolate affected systems (network segmentation, account disable, service stop)
- [ ] **Preserve evidence BEFORE remediation** - do not wipe-and-reimage before forensic capture
- [ ] Capture volatile data (memory, network connections, logged-in users, running processes)
- [ ] Preserve and protect logs (centralize, prevent rollover, hash with timestamps)
- [ ] Block known indicators (IPs, domains, hashes) at perimeter
- [ ] Rotate credentials for any compromised account or any account with access to affected systems
- [ ] Snapshot affected systems for forensic imaging

### Long-term

- [ ] Apply patches / configuration changes to root cause
- [ ] Rebuild from known-good baselines
- [ ] Implement compensating controls before bringing systems back

## 4. Phase 3 - Eradication

- [ ] Remove malware / web shells / persistence mechanisms (registry, scheduled tasks, cron, systemd units, IAM roles, OAuth tokens, API keys)
- [ ] Close exploited vulnerabilities (patch, configuration, code fix)
- [ ] Confirm eradication via independent scan
- [ ] Document evidence of eradication

## 5. Phase 4 - Recovery

- [ ] Restore from clean backups (verify backup pre-dates compromise)
- [ ] Phased return to production with elevated monitoring
- [ ] Verify integrity and availability of restored ePHI
- [ ] Heightened monitoring for a defined post-incident window (commonly 30-90 days)
- [ ] Re-enable affected user accounts after credential rotation + identity reverification

## 6. Phase 5 - Breach determination (run in parallel with containment / eradication once scope is knowable)

Use [`breach-risk-assessment.md`](breach-risk-assessment.md) for the formal 4-factor assessment.

Decision tree:

```
Was there an impermissible use/disclosure of PHI?
├── No → not a breach; document; continue
└── Yes → was PHI Unsecured (not FIPS-encrypted)?
    ├── No → safe harbor; document
    └── Yes → run 4-factor risk assessment
        ├── Low probability of compromise (documented, signed) → no notification; retain
        └── Cannot demonstrate low probability → BREACH → notify per timing table
```

### Notification matrix (if breach)

| Recipient | Trigger | Deadline | Owner |
|---|---|---|---|
| Affected individuals | Always | 60 days from discovery | Privacy Officer |
| HHS OCR (≥ 500 individuals) | At threshold | 60 days from discovery | Privacy Officer |
| Media | ≥ 500 in any State/jurisdiction | 60 days from discovery | Communications + Privacy Officer |
| HHS OCR (< 500 individuals) | Always for small breaches | Annual - 60 days after year end | Privacy Officer |
| BA → CE | Always when BA-side | Per BAA | BA |
| State regulators | Per state breach laws | Varies | Privacy Officer + counsel |
| Law enforcement | Per circumstance | | Counsel |
| Cyber insurance | Per policy | Often within hours | Risk / Finance + counsel |

## 7. Phase 6 - Post-incident

- [ ] After-action review within 30 days
- [ ] Root cause analysis (technical + process + human)
- [ ] Lessons learned documented and tracked to closure
- [ ] IR plan and this playbook updated
- [ ] Training updated; awareness communication to workforce
- [ ] Workforce sanctions applied if applicable
- [ ] Risk analysis updated if material new risk surfaced
- [ ] Communications retention - apply legal hold if litigation or OCR review reasonably anticipated

## 8. Documentation expectations (throughout)

- Timeline of detection → notification → containment → eradication → recovery, with timestamps and actor for each step
- Decisions made + by whom + rationale
- Evidence collected (with chain of custody)
- Communications sent + received
- Costs incurred (for insurance + lessons-learned)

## 9. Communications

### Internal

- IR team channel (out-of-band, separate from compromised infrastructure)
- Executive briefings at defined cadence
- Workforce communication after containment, coordinated with counsel

### External

- All external communication routed through Communications + counsel
- No social media or press without sign-off
- Customer / patient / partner notifications drafted in advance for major scenarios

## 10. Scenario-specific quick references

### Ransomware

Default presumption per OCR: ransomware on an ePHI system is a breach unless 4-factor low-probability demonstrated. Forensic confirmation required to support any non-breach determination.

### Lost / stolen device

- Verify encryption state at time of loss (FIPS-validated) - safe harbor if confirmed
- Remote-wipe if possible; log success/failure
- Reset credentials for any saved sessions
- 4-factor assessment if encryption cannot be confirmed

### Phishing (credentials compromised)

- Identify affected account(s) and access scope
- Determine whether attacker accessed any ePHI - review audit logs from credential-theft window
- Rotate credentials, force re-auth, review MFA enrollment for tampering
- Notify other accounts with shared resources

### Misdirected disclosure (email / fax to wrong recipient)

- Recover PHI if possible; obtain destruction confirmation
- 4-factor assessment focusing on recipient identity + cooperation
- Tighten controls (recipient validation, DLP, training)

### BA / vendor breach

- BA notifies CE per BAA timing
- CE evaluates whether BA's facts support low probability or breach
- CE leads individual notification unless BAA delegates to BA
- Vendor risk review re-run

### Insider misuse

- HR + counsel engagement; sanctions per policy
- Access immediately revoked
- Audit log review for full scope
- Notification per breach determination

## 11. Quarterly readiness checks

- [ ] Contact tree current
- [ ] Out-of-band channel operational
- [ ] Forensic capability retained and available
- [ ] Backups recent + successfully restore-tested
- [ ] Playbook review completed
- [ ] Tabletop or drill within 12 months
- [ ] Cyber-insurance policy current

## Sign-off

| Role | Name | Date approved |
|---|---|---|
| Security Officer | | |
| Privacy Officer | | |
| Counsel | | |
| Executive sponsor | | |
