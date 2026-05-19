# HIPAA Security Rule Risk Analysis

> NIST 800-30-style risk analysis worksheet mapped to the Security Rule (45 CFR 164.308(a)(1)(ii)(A)). Pair with [`../references/security-rule.md`](../references/security-rule.md). Retain for 6 years; refresh on material change.

## Metadata

| Field | Value |
|---|---|
| Entity | |
| Entity role | CE / BA |
| Scope of this analysis | (which systems / business units / ePHI flows) |
| Scope of ePHI | (categories + volume; reference inventory) |
| Methodology | NIST 800-30 / NIST 800-66 Rev. 2 / other |
| Lead | (security officer or designee) |
| Contributors | (privacy officer, IT/eng leads, app owners) |
| Date completed | |
| Trigger | (initial / annual refresh / material change - describe / post-incident) |
| Prior analysis ref | |

## 1. Scope statement

Document:
- All ePHI created, received, maintained, or transmitted **by the entity**, **anywhere**, including:
  - Production systems (apps, DBs, search, cache, queue, object storage)
  - Backups and DR copies
  - Audit logs and SIEM stores (logs are ePHI)
  - Dev / test / staging (if they hold real or recoverable ePHI)
  - Workstations and mobile devices
  - Removable media
  - BA-hosted systems (each BA + sub-BA chain)
  - Email systems (if PHI in transit)
- Out-of-scope items + rationale (e.g., a business unit explicitly not handling PHI)

## 2. Asset inventory

| Asset ID | Asset name | Type | ePHI volume | Sensitivity | Owner | BAA (if BA-hosted) |
|---|---|---|---|---|---|---|
| | | (system / dataset / vendor) | (records, individuals) | (standard / heightened) | | |

Include downstream BAs and sub-BAs.

## 3. Threat identification

Per asset (or grouped where threat profiles match):

| Threat | Source | Description |
|---|---|---|
| External actor | Cybercriminal | Ransomware, exfiltration, credential theft, phishing |
| External actor | Nation-state | Targeted intrusion, supply-chain |
| Insider (malicious) | Workforce | Unauthorized access, exfiltration, misuse |
| Insider (negligent) | Workforce | Misconfiguration, lost device, accidental disclosure |
| BA / vendor | Third party | BA breach, sub-processor failure |
| Environmental | | Power, fire, flood, regional outage |
| Technical failure | | Hardware, software bug, data corruption |
| Process failure | | Misrouted communication, incorrect access grant |

## 4. Vulnerability identification

For each asset + threat combination, identify vulnerabilities. Map to Security Rule standards.

| Asset | Threat | Vulnerability | Current controls | Control adequacy |
|---|---|---|---|---|
| | | | | (Sufficient / Partial / Insufficient) |

## 5. Likelihood and impact

| Factor | Levels | Notes |
|---|---|---|
| Likelihood | Very Low / Low / Moderate / High / Very High | Probability that the threat will exploit the vulnerability given current controls |
| Impact | Very Low / Low / Moderate / High / Very High | Consequence to confidentiality / integrity / availability of ePHI |

Risk = function(Likelihood, Impact). Document the matrix in use.

## 6. Risk register

| Risk ID | Asset | Threat | Vulnerability | Likelihood | Impact | Risk | Disposition |
|---|---|---|---|---|---|---|---|
| | | | | | | | (Mitigate / Accept / Transfer / Avoid) |

For each risk:

- **Disposition** with rationale
- **Owner**
- **Target date** if mitigating
- **Compensating controls** if accepted
- **Executive sign-off** if High accepted

## 7. Security Rule coverage map

Confirm coverage of every standard. For each, list assets/risks and link to risk register entries.

### Administrative (164.308)

| Standard | Spec | R/A | Coverage status | Link to risk register |
|---|---|---|---|---|
| Security Management Process | Risk Analysis | R | THIS DOCUMENT | n/a |
| | Risk Management | R | | |
| | Sanction Policy | R | | |
| | Information System Activity Review | R | | |
| Assigned Security Responsibility | Security Officer | R | | |
| Workforce Security | Authorization / Supervision | A | | |
| | Workforce Clearance | A | | |
| | Termination Procedures | A | | |
| Information Access Management | Isolating Healthcare Clearinghouse Functions | R | (if applicable) | |
| | Access Authorization | A | | |
| | Access Establishment and Modification | A | | |
| Security Awareness and Training | Security Reminders | A | | |
| | Protection from Malicious Software | A | | |
| | Log-in Monitoring | A | | |
| | Password Management | A | | |
| Security Incident Procedures | Response and Reporting | R | | |
| Contingency Plan | Data Backup Plan | R | | |
| | Disaster Recovery Plan | R | | |
| | Emergency Mode Operation Plan | R | | |
| | Testing and Revision Procedures | A | | |
| | Applications and Data Criticality Analysis | A | | |
| Evaluation | Periodic Evaluation | R | | |
| Business Associate Contracts | Written Contract | R | | |

### Physical (164.310)

| Standard | Spec | R/A | Coverage status | Link |
|---|---|---|---|---|
| Facility Access Controls | Contingency Operations | A | | |
| | Facility Security Plan | A | | |
| | Access Control and Validation | A | | |
| | Maintenance Records | A | | |
| Workstation Use | Use | R | | |
| Workstation Security | Security | R | | |
| Device and Media Controls | Disposal | R | | |
| | Media Re-use | R | | |
| | Accountability | A | | |
| | Data Backup and Storage | A | | |

### Technical (164.312)

| Standard | Spec | R/A | Coverage status | Link |
|---|---|---|---|---|
| Access Control | Unique User Identification | R | | |
| | Emergency Access Procedure | R | | |
| | Automatic Logoff | A | | |
| | Encryption and Decryption | A | | |
| Audit Controls | Audit Controls | R | | |
| Integrity | Mechanism to Authenticate ePHI | A | | |
| Person or Entity Authentication | Authentication | R | | |
| Transmission Security | Integrity Controls | A | | |
| | Encryption | A | | |

### Addressable decisions log

For every Addressable spec, record: implemented as written / equivalent measure / not implemented + rationale. Date last reviewed.

| Spec | Decision | Rationale | Date | Reviewer |
|---|---|---|---|---|

## 8. Risk management plan

(Drives 164.308(a)(1)(ii)(B).)

| Risk ID | Disposition | Target date | Owner | Status | Evidence on completion |
|---|---|---|---|---|---|

## 9. Sign-offs

| Role | Name | Signature | Date |
|---|---|---|---|
| Security Officer | | | |
| Privacy Officer | | | |
| Executive sponsor | | | |
| (Counsel) | | | |

## 10. Revision triggers

Re-run this analysis (in whole or for the affected scope) when any of:

- Material change to systems, data flows, or vendors
- Significant business change (acquisition, divestiture, new product line)
- New regulatory requirement
- Significant security incident
- Significant control gap identified
- Annually at minimum

## Retention

Retain this analysis and all prior versions for at least 6 years per 164.530(j). Maintain a change log showing what was revised and why.
