# Technical Safeguards - implementation depth (164.312)

Depth-of-implementation reference for the Security Rule's technical safeguards. Pair with [`security-rule.md`](security-rule.md) for the standards-and-specs taxonomy.

## 1. Encryption at rest

| Topic | Guidance |
|---|---|
| **Standard** | FIPS 140-2 / 140-3 validated cryptographic module. The Breach Notification safe harbor attaches only to FIPS-validated encryption (HHS guidance). |
| **Algorithm** | AES-256 GCM (or other current NIST-approved AEAD) for new systems |
| **Scope** | Every storage location holding ePHI: primary DB, replicas, backups, search indices, caches, message queues, file storage, object storage, dev/test databases, log stores, archives, tape, removable media, workstation disks, mobile devices |
| **Key management** | Hardware-backed KMS / HSM (cloud KMS acceptable when BAA-covered). Rotate keys per policy. Separate key custodian from data administrator. Audit key access. Never embed keys in code or config in source control. |
| **Database column / field encryption** | Application-level for highly sensitive fields (SSN, certain identifiers, mental health, SUD, HIV, genetic) when DB admins should not see plaintext |
| **Backup encryption** | Always. Test restore with encryption in place. Common failure: backups encrypted in transit but landing in object storage without server-side encryption. |
| **Documentation** | Encryption inventory listing every ePHI storage location, encryption method, key custodian, rotation schedule, FIPS validation certificate references |

## 2. Encryption in transit

| Topic | Guidance |
|---|---|
| **Standard** | TLS 1.2 minimum; TLS 1.3 preferred for new systems. Disable SSLv2/v3 and TLS 1.0/1.1. |
| **Cipher suites** | Strong AEAD ciphers; forward secrecy (ECDHE); disable RC4, 3DES, CBC where avoidable |
| **Certificates** | Valid CA-issued; automated renewal; certificate transparency monitoring; appropriate key sizes (RSA ≥ 2048 / ECDSA P-256+) |
| **Internal traffic** | Service-to-service ePHI traffic must be encrypted - mTLS or service mesh. "It's behind the VPC" is not sufficient. |
| **Email** | Outbound email with ePHI requires opportunistic + enforced TLS; for member-facing email, encrypted patient portal or secure-email gateway preferred over relying on transport encryption |
| **SFTP / batch** | SFTP / FTPS with key-based auth, not FTP. AS2 / mutual-auth for batch interchange. |
| **APIs** | TLS + per-client authentication; webhook subscribers must validate TLS |

## 3. Access control (164.312(a)(1))

### Unique User Identification (Required)

Per-user identity for every account with ePHI access. **No shared service accounts** for ePHI access. Service accounts that act on behalf of a system must be uniquely identifiable and their usage tied to a responsible user or process.

### Emergency Access Procedure (Required)

Break-glass procedure to obtain ePHI in emergency (system outage, clinical emergency requiring elevated access). Must be:
- Documented
- Auditable (every break-glass use logged and reviewed)
- Time-limited (auto-revoke)
- Reviewed by privacy officer / security officer

### Automatic Logoff (Addressable)

Session timeout after predetermined inactivity. Common values:
- Clinical workstations in patient areas: 5-15 minutes
- Administrative workstations: 15-30 minutes
- Mobile devices: device-lock + app-level timeout
- Web app sessions: idle + absolute lifetime
- API tokens: short-lived access tokens + refresh tokens with rotation

Document the chosen value and rationale per system.

### Encryption and Decryption (Addressable - operationally Required, see above)

## 4. Audit controls (164.312(b)) - Required

Capture sufficient log data to record and examine activity in systems containing ePHI. At minimum:

| Event class | Detail |
|---|---|
| **Access to ePHI** | User, timestamp, source IP / device, resource accessed (patient ID, record type), action (read / create / update / delete / export), outcome (success / failure) |
| **Authentication events** | Login attempts (success / failure), MFA events, session establishment, logoff |
| **Authorization changes** | Role assignment, permission grants, group membership changes |
| **Administrative actions** | Privileged access usage, configuration changes, schema changes, backup / restore, key access |
| **Security events** | IDS / IPS alerts, anomaly detections, integrity-monitoring alerts |
| **System events** | Service starts/stops, errors involving ePHI-handling components |

**Log content discipline:**
- Do **not** log full PHI payloads (request bodies, AI prompts, response bodies)
- Log identifiers and references; if you need to debug, retrieve from source on demand
- Logs themselves contain ePHI (patient IDs, access patterns) - treat them as ePHI for storage, retention, encryption, access control

**Log integrity:**
- Append-only or WORM storage
- Cryptographic hashing for tamper evidence
- Separate access path from app admins to log admins

**Retention:** 6 years minimum (Privacy Rule documentation standard, 164.530(j)). Some categories longer for litigation or state law.

**Review:** Information System Activity Review (164.308(a)(1)(ii)(D)) is Required - regular review of logs and access reports. Document the cadence, what is reviewed, who reviews, what action is taken.

## 5. Integrity (164.312(c)(1))

### Mechanism to Authenticate ePHI (Addressable)

Detect unauthorized alteration or destruction. Implementations:
- DB-level checksums and constraints
- Cryptographic hashing of stored records
- File integrity monitoring on configuration and code paths
- Append-only or versioned storage for clinical records (immutable history)
- Backup verification with checksum comparison on restore tests

## 6. Person or Entity Authentication (164.312(d)) - Required

Verify identity before granting access.

| Control | Notes |
|---|---|
| **MFA** | Required-in-practice for any privileged ePHI access; strongly recommended for all ePHI access. Phishing-resistant MFA (WebAuthn / FIDO2) preferred for admin |
| **Password policy** | Current NIST 800-63B guidance: length-first, no forced rotation absent compromise, breached-password screening. Do **not** rely on 90-day forced rotation as a control. |
| **Service authentication** | mTLS, signed tokens, short-lived credentials; rotate credentials; no long-lived static keys |
| **Federation** | SAML / OIDC against an enterprise IdP; centralized lifecycle |

## 7. Transmission Security (164.312(e)(1))

### Integrity Controls (Addressable)

Detect modification in transit - TLS + message-level integrity for high-value flows (signed payloads, MACs).

### Encryption (Addressable - operationally Required, see §2)

## 8. Mobile and removable media

- Full-disk encryption on all workstations, laptops, mobile devices with ePHI access (FIPS-validated)
- MDM with remote-wipe capability
- Removable media policy: ideally prohibited; if allowed, encrypted + tracked + returned/destroyed
- BYOD requires container / app-level controls + remote wipe of the container (not the personal device)

## 9. Backups and disaster recovery

- Backups encrypted at rest with FIPS-validated module
- Off-site / cross-region copy
- Documented RTO / RPO
- Restore tests at documented cadence (untested backups don't count)
- Backup retention aligned to records retention + legal hold

## 10. Web tracking / analytics / session replay

Active OCR enforcement area (status varies; check current OCR guidance + counsel).

- Tracking technologies (pixels, tags, session-replay, SDK telemetry) on pages that may transmit ePHI to a third party generally require a BAA with that third party
- Unauthenticated marketing pages may also be in scope if they reveal symptoms / conditions / providers in the URL or DOM
- Default posture: do not deploy third-party tracking on any page that may interact with ePHI without privacy-officer + legal review

## 11. AI / ML systems

- Inference traffic with ePHI to a model service requires a BAA with the service provider
- Model providers commonly retain logs by default - disable or contract around it; verify in BAA
- Do not use ePHI to train, fine-tune, or evaluate models without explicit authorization; see [`baa-review.md`](baa-review.md) AI training carve-out
- Prompt and response payloads with ePHI must be encrypted in transit and at rest; consider field-level minimization in the prompt
- Output review: model responses may inadvertently include unrelated patient data if the prompt or context leaks - boundary controls required

## Common engineering pitfalls

- TLS 1.2+ at the edge but plaintext between internal services
- Encryption at rest in primary DB but not in backups, search indices, caches, or logs
- Logs contain full request / response bodies with PHI
- Shared service accounts with ePHI access
- No FIPS validation - encryption is in place but uses non-validated implementations
- MFA enforced only for admin, not for all ePHI access
- Tracking pixels on patient-facing pages without BAA
- AI service onboarded without BAA or with default log retention enabled
- Mobile devices with ePHI but no full-disk encryption or MDM
- Backups never restore-tested

## Defer to security officer when

- Choosing between Addressable implementations
- Accepting risk on encryption for legacy systems
- Approving any new third-party with ePHI access
- Reducing log retention below 6 years
- Allowing any AI service to retain ePHI logs / use ePHI for model improvement
