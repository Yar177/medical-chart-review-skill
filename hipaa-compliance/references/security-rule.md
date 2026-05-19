# Security Rule (45 CFR Part 164 Subpart C)

## Scope

The Security Rule applies to **electronic PHI (ePHI)** held or transmitted by CEs and BAs. It requires implementation of administrative, physical, and technical safeguards to ensure the confidentiality, integrity, and availability of ePHI.

The Security Rule is technology-neutral and risk-based - it does not prescribe specific products. It does prescribe a **risk analysis** (164.308(a)(1)(ii)(A)) as the foundation of the entire compliance program.

## Required vs Addressable - read this first

| Designation | What it means |
|---|---|
| **Required** | The entity must implement the specification |
| **Addressable** | The entity must (a) implement the specification as written, OR (b) implement an equivalent measure that achieves the objective, OR (c) document why neither is reasonable and appropriate. Addressable does **not** mean optional. |

For every Addressable spec, **document the decision**: which path was taken, why, what equivalent measure exists, when the decision was last reviewed. OCR audits flag undocumented Addressable decisions as findings.

## Administrative safeguards (164.308)

| Standard | Spec | R/A | Notes |
|---|---|---|---|
| Security Management Process | Risk Analysis | R | Accurate and thorough assessment of potential risks and vulnerabilities to ePHI. **Foundation of the program.** |
| | Risk Management | R | Sufficient measures to reduce risks to a reasonable level |
| | Sanction Policy | R | Workforce sanctions for noncompliance |
| | Information System Activity Review | R | Regular review of audit logs, access reports, incident reports |
| Assigned Security Responsibility | Security Officer | R | Designate one individual responsible |
| Workforce Security | Authorization / Supervision | A | Procedures for authorization and supervision of workforce with ePHI access |
| | Workforce Clearance | A | Determine ePHI access is appropriate |
| | Termination Procedures | A | Terminate access when employment ends or role changes |
| Information Access Management | Isolating Healthcare Clearinghouse Functions | R | If applicable |
| | Access Authorization | A | Granting access to ePHI |
| | Access Establishment and Modification | A | Establishing, documenting, reviewing, modifying access |
| Security Awareness and Training | Security Reminders | A | Periodic reminders |
| | Protection from Malicious Software | A | Procedures for guarding against, detecting, reporting |
| | Log-in Monitoring | A | Procedures for monitoring log-in attempts |
| | Password Management | A | Creating, changing, safeguarding passwords |
| Security Incident Procedures | Response and Reporting | R | Identify and respond to suspected/known security incidents; mitigate; document |
| Contingency Plan | Data Backup Plan | R | Establish and implement procedures to create and maintain retrievable exact copies of ePHI |
| | Disaster Recovery Plan | R | Restore any loss of data |
| | Emergency Mode Operation Plan | R | Continue critical business processes during emergency |
| | Testing and Revision Procedures | A | Periodic testing |
| | Applications and Data Criticality Analysis | A | Assess relative criticality of specific applications and data |
| Evaluation | Periodic Evaluation | R | Initially and periodically; technical and nontechnical |
| Business Associate Contracts | Written Contract | R | See [`baa-review.md`](baa-review.md) |

## Physical safeguards (164.310)

| Standard | Spec | R/A | Notes |
|---|---|---|---|
| Facility Access Controls | Contingency Operations | A | Allow facility access in support of restoration of lost data |
| | Facility Security Plan | A | Safeguard facility from unauthorized access |
| | Access Control and Validation | A | Validate access based on role |
| | Maintenance Records | A | Document repairs and modifications |
| Workstation Use | Use | R | Specify proper functions, manner, and physical attributes of workstations accessing ePHI |
| Workstation Security | Security | R | Physical safeguards for all workstations |
| Device and Media Controls | Disposal | R | Final disposition of ePHI and the hardware/media on which it is stored |
| | Media Re-use | R | Removal of ePHI from electronic media before re-use |
| | Accountability | A | Record of movements of hardware and media and persons responsible |
| | Data Backup and Storage | A | Retrievable, exact copy of ePHI before movement of equipment |

## Technical safeguards (164.312)

| Standard | Spec | R/A | Notes |
|---|---|---|---|
| Access Control | Unique User Identification | R | Per-user, no shared accounts |
| | Emergency Access Procedure | R | Procedures for obtaining ePHI in emergency |
| | Automatic Logoff | A | Terminate session after predetermined inactivity |
| | Encryption and Decryption | A | Encrypt and decrypt ePHI |
| Audit Controls | Audit Controls | R | Hardware, software, procedural mechanisms to record and examine activity in systems with ePHI |
| Integrity | Mechanism to Authenticate ePHI | A | Verify ePHI has not been altered/destroyed in an unauthorized manner |
| Person or Entity Authentication | Authentication | R | Verify the person or entity seeking access is the one claimed |
| Transmission Security | Integrity Controls | A | Ensure ePHI is not improperly modified in transit |
| | Encryption | A | Encrypt ePHI in transit whenever deemed appropriate |

> Encryption is **Addressable** in the regulation but **operationally Required** in practice - unencrypted ePHI is "unsecured" under the Breach Notification Rule, so any incident triggers full notification. Treat encryption as the default; document and justify every exception.

For implementation depth, see [`technical-safeguards.md`](technical-safeguards.md).

## Risk analysis (164.308(a)(1)(ii)(A)) - the foundation

The risk analysis is the most cited finding in OCR audits and enforcement actions. Requirements:

- **Scope:** all ePHI created, received, maintained, or transmitted by the entity (every system, every location, every BA chain)
- **Method:** generally accepted (commonly NIST 800-30); identify threats, vulnerabilities, current controls, likelihood, impact, residual risk
- **Documentation:** written, signed, dated, retained 6 years
- **Update:** when there is a material change in operations, technology, environment, or after a security incident
- **Action:** feed into Risk Management (164.308(a)(1)(ii)(B)) - actual remediation, accepted risk with executive sign-off, or transferred risk

Use [`../templates/risk-analysis.md`](../templates/risk-analysis.md).

## NIST 800-66 mapping

NIST SP 800-66 (Implementing the HIPAA Security Rule) maps the Security Rule to NIST controls and is the most commonly used implementation guide. Use it for control-mapping work; do not rely on it for legal interpretation.

The current rev (Rev. 2, 2024) replaces the 2008 Rev. 1; controls have been substantially restructured. Check the current rev when citing.

## Common engineering pitfalls

- **No documented risk analysis** - leading audit finding
- **Risk analysis scope limited to "our app"** instead of all ePHI flows including vendors, backups, logs, dev / test
- **Encryption claim that is not FIPS-validated** - safe harbor under Breach Notification only attaches to FIPS-validated encryption per HHS guidance
- **Shared service accounts** with ePHI access - violates Unique User Identification (Required)
- **No audit logs**, or logs without integrity protection, or logs retained < 6 years
- **Treating Addressable as Optional** without documentation
- **No annual evaluation** - Periodic Evaluation is Required
- **No sanction policy applied** when violations occur - audit finding even if sanctions exist on paper

## Defer to security officer + counsel when

- Risk acceptance at High level (executive sign-off + documented rationale)
- Material weakening of a safeguard
- Findings during an OCR audit or investigation
- Disagreement on Addressable implementation between security and business
- A control failure that may be a reportable security incident
