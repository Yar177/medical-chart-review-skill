# Access and Authorization

Practical guide to implementing 45 CFR 164.308 (Workforce Security, Information Access Management) and 164.312(a) (Access Control) - role design, minimum necessary in practice, and the workforce lifecycle.

## 1. RBAC design

### Start from purpose, not from org chart

Define roles by **what task requires what ePHI**, not by job title. Common categorical roles:

| Role family | Typical ePHI access |
|---|---|
| Treating clinician | Read/write clinical record for assigned patients (treatment relationship) |
| Care team support (MA, RN, nurse practitioner) | Read clinical record + write specific fields per scope |
| Front-desk / registration | Demographics + insurance + appointment; limited clinical |
| Billing / coding | Encounter + diagnosis + procedure for billed encounters |
| Care management / quality | Aggregated + sampled records per program scope |
| Research (with authorization or LDS) | Per protocol; limited data set or de-identified |
| Patient services / call center | Demographics + appointment + limited clinical for verification only |
| System administrator | System metadata; **not** application data by default; break-glass with audit |
| Database administrator | Schema and operational metadata; field-level encryption or just-in-time access for plaintext |
| Application developer | **No** production ePHI by default; synthetic data in dev/test |
| Security analyst | Audit logs (which are ePHI); not application data |

### Permission granularity

Permissions should be granular enough to enforce minimum necessary but not so granular that admin becomes impossible. Common pattern:

- **Resource type** (encounter, lab, imaging, medication, problem, note, billing record)
- **Action** (read, create, update, delete, export, print)
- **Scope** (assigned-only, panel, department, organization-wide)

### Attribute-based filtering

Layer attribute-based filters on top of RBAC for relationship-based access:
- Treating provider relationship (assigned, on-call, covering)
- Encounter participation
- Care-team membership
- Organizational unit

A clinician with "read clinical record" RBAC permission still needs an attribute-level relationship check to access a specific patient.

## 2. Minimum necessary in practice

- **Per query** - filter to fields and records needed for the specific purpose
- **Per role** - role grants the floor; per-query filters apply on top
- **Per export** - exports are higher-risk; require explicit purpose + approval + audit
- **API responses** - return only requested fields; do not return full record by default
- **Logs** - log identifiers, not full payloads
- **AI prompts** - minimize fields sent to a model

> Reminder: minimum necessary does **not** apply to treatment-related disclosures to a provider, disclosures to the individual, authorized disclosures, or disclosures required by law. See [`privacy-rule.md`](privacy-rule.md).

## 3. Workforce lifecycle

### Provisioning (164.308(a)(3)(ii)(A) - Authorization and/or Supervision)

- Authorization request tied to a role, an identity, and a business justification
- Approver is the role owner, not the requester's manager by default
- Automated provisioning from IdP / HRIS where possible
- Verify the identity before granting access (HR-verified hire start, contractor vetting)

### Workforce clearance (164.308(a)(3)(ii)(B))

- Pre-employment background check appropriate to the role (especially for roles with broad ePHI access)
- Confidentiality agreement signed

### Training (164.308(a)(5))

- HIPAA training at hire + annually
- Role-specific training for roles with elevated access
- Phishing awareness
- Document completion; retain 6 years

### Periodic access review

- Quarterly or semi-annual recertification of access for ePHI-touching roles
- Role owner attests that each user's access is still required
- Stale access removed within a documented SLA
- Service-account inventory reviewed the same way

### Role change

- Access changes when role changes
- Same-day removal of access no longer required
- Common failure: role change but old access lingers (creates "access creep")

### Termination (164.308(a)(3)(ii)(C))

- Trigger from HRIS within minutes / hours of termination
- Disable all accounts, including federated, third-party SaaS, VPN, mobile, code repos that touch production
- Recover hardware, badges, removable media
- Document the timeline; periodic audit of termination-to-disable latency

### Contractor / BA workforce

- Same lifecycle requirements
- Notification responsibility on the BA when their staff leave - confirm via BAA
- Vendor service-account hygiene: rotate credentials, audit usage, expire unused

## 4. Privileged access

- Just-in-time elevation with approval workflow, not standing admin
- Separate admin accounts from regular user accounts
- Phishing-resistant MFA (WebAuthn / FIDO2) for admin
- Session recording for highly privileged sessions
- Privileged Access Management (PAM) tooling for credential vaulting and rotation
- All privileged actions logged and reviewed

## 5. Service accounts

- Per-purpose service accounts, not per-team catch-alls
- Unique identifiable accounts (164.312(a)(2)(i))
- Short-lived credentials where possible (workload identity, OIDC federation, IAM roles)
- Rotation on a schedule; rotation on workforce changes for the responsible team
- Inventory + ownership documented

## 6. Emergency access (break-glass)

- Documented procedure tied to specific scenarios (clinical emergency, IR investigation, restore from disaster)
- Auto-elevation with full audit
- Time-limited (auto-revoke)
- Mandatory post-use review by privacy or security officer
- Sanctions applied for misuse

## 7. Patient access (164.524)

Engineering responsibilities for patient-rights requests:
- Patient portal supports export in human-readable + machine-readable formats
- API access for the individual (or designee) per ONC interoperability rules where applicable
- Verification of identity before fulfilling - high enough for trust, low enough not to be a barrier
- Logged as a permitted disclosure; included in disclosure accounting where required
- 30-day response window (one 30-day extension permitted)

## 8. Common engineering pitfalls

- **Role drift** - roles added over time, never pruned; users accumulate permissions
- **Shared admin accounts** ("we all use `admin` for emergencies") - violates Unique User Identification (Required)
- **Service account passwords in source control** - rotate immediately + investigate exposure
- **Dev environment with production data copy** - either de-identify (Safe Harbor / Expert Determination) or treat dev as production for access control
- **Federated logout that doesn't propagate** - user "logs out" of IdP but downstream sessions continue
- **Mobile devices retaining session tokens past logout**
- **Patient access request manual + slow** - common audit finding
- **Break-glass with no post-use review**
- **Vendor service accounts that survive vendor employee turnover**

## 9. Documentation expectations

For each ePHI-handling system:

- Role catalog with role → permission → ePHI scope mapping
- Workforce-to-role assignment with current attestation
- Periodic access-review evidence
- Break-glass procedure + log of uses
- Termination procedure + termination-to-disable latency report
- Training completion records (6-year retention)
- Patient access request log

## Defer to privacy officer + security officer when

- Granting access broader than minimum necessary - require written justification
- Approving break-glass use after the fact when misuse is suspected
- Designing patient access verification (balance friction vs spoofing risk)
- Approving production access for developers under any standing arrangement
- Granting service-account access to a third party
