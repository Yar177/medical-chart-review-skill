# Coding Audit (DRG / CPT / E&M)

**Patient**: [ref] · **Claim / Encounter**: [id, DOS]
**Audit scope**: [DRG validation / CPT / E&M leveling / professional fee]
**Reviewer**: AI coding auditor (final determination requires CCS/CPC/CRC)

## Codes billed vs documented
| Code type | Billed | Supported by documentation? | Source citation | Recommendation |
|---|---|---|---|---|
| Principal Dx | | | | |
| Secondary Dx | | | | |
| Procedure (ICD-10-PCS) | | | | |
| CPT / HCPCS | | | | |
| Modifiers | | | | |
| E&M level | | | | |

## Administrative evidence
- Payer / plan / product: [...]
- Eligibility on DOS: [verified / not verified / unable to confirm]
- Place of service (POS) code vs documented setting: [match / mismatch]
- Prior authorization # tied to billed CPT(s): [auth # → CPT(s)] · [match / mismatch / not required]
- Referral on file (specialist + HMO/POS): [yes / no / N/A]
- Step therapy / medical-necessity documentation (if applicable): [...]
- Payer-specific modifier or bundling rules: [see `references/local-policy.md` if present]

## DRG analysis (inpatient)
- Billed DRG: [n] — [description]
- Recommended DRG: [n] — [description]
- Driver: [PDx change / CC-MCC change / procedure]
- Financial impact: [informational only — do not let this drive coding]

## E&M MDM analysis
| Element | Documented | Level |
|---|---|---|
| Problems addressed | | |
| Data reviewed | | |
| Risk | | |
| **Overall MDM** | | |
| Time documented | | |
| **Supported level** | | |

## Findings
- [ ] Overcoding: [...]
- [ ] Undercoding: [...]
- [ ] Missing modifiers: [...]
- [ ] Unbundling: [...]
- [ ] Documentation insufficient for billed level: [...]

## Recommendations
- Rebill / no change / educate / refund
