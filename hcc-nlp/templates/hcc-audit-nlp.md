# HCC / Risk Adjustment Audit

**Patient**: [ref] · **Plan year**: [YYYY] · **DOS reviewed**: [date range]
**Model**: [CMS-HCC v28 / v24 / HHS-HCC] · **Crosswalk snapshot**: [ISO date]
**Reviewer**: AI documentation auditor
**NLP pipeline (if applicable)**: [model name + version] · **Audit mode**: [human-only / NLP-assisted / NLP-validated]

## Summary
- HCCs claimed on encounter: [n]
- HCCs validated: [n]
- HCCs invalid (recommend retract): [n]
- HCCs missed (capture opportunity): [n]
- Net RAF impact (informational): [+/- estimate]
- NLP-emitted HCCs in scope: [n] · NLP suspect-only candidates: [n]
- NLP overrides by reviewer this audit: [n] (overturn rate this audit: [pct])

## Per-HCC findings

### HCC [code] — [description] · ICD-10: [code]
| Field | Detail |
|---|---|
| Claimed on DOS | [date / claim ID] |
| Documentation source | [note date, type, section] |
| Provider | [credentialed / signed?] |
| **M**onitor | [evidence or "Not documented"] |
| **E**valuate | [evidence] |
| **A**ssess/Address | [evidence] |
| **T**reat | [evidence] |
| Specificity match | [Yes / No — explain] |
| Conflicting documentation | [Yes / No — cite] |
| **Verdict** | ✅ Validated · ⚠️ Query recommended · ❌ Invalid |
| Notes | |

#### NLP-assisted fields (omit row if not NLP-assisted)
| Field | Detail |
|---|---|
| NLP model + version | [name + semver] |
| NLP HCC crosswalk version | [V28 / V24 / HHS-HCC + snapshot date] |
| NLP emission type | Validate / Suspect / Not emitted |
| NLP confidence | [0.0-1.0] |
| NLP-extracted span(s) | [verbatim text + section] |
| NLP-attributed DOS | [ISO date] |
| NLP-attributed assertion | [current / historical / negated / hypothetical / family / hedged / ruled-out] |
| NLP MEAT evidence captured | M: [text] · E: [text] · A: [text] · T: [text] · or "None" |
| NLP MEAT linkage method | [section-aware / sentence-window / model-scored / human-reviewed] |
| NLP hierarchy applied? | [Yes / No / Trumped by HCC nn] |
| NLP candidate-log entry (if not emitted) | [reason logged by extractor] |
| **Reviewer override?** | [Yes / No] |
| Override direction | [Reviewer added HCC NLP missed / Reviewer removed HCC NLP wrongly emitted] |
| Override reason | [free text - feeds back into failure-mode catalog] |

(Repeat per HCC)

## Capture opportunities (HCCs supported but not coded)
| ICD-10 | Description | Supporting documentation | Provider query? |
|---|---|---|---|

## Compliance notes
- [Any chart-cloning, copy-forward, or provider attestation concerns]

## Recommended actions
- [ ] Submit provider queries (see attached)
- [ ] Retract claims for invalid HCCs
- [ ] Schedule annual recapture for chronic conditions dropped this year
- [ ] Specificity education for [provider/group]

## NLP pipeline feedback (omit if not NLP-assisted)
- [ ] Override(s) logged to failure-mode catalog: [link]
- [ ] Regression fixture proposed for [failure mode]: [link or "n/a"]
- [ ] Model card overdue for review? See [`hcc-model-card.md`](hcc-model-card.md) · last review: [date]
- [ ] Suspect-engine output requiring outreach (not auto-validation): [list]
- [ ] Two-way review obligation triggered (invalid HCCs already submitted upstream)? [Yes / No]

## See also
- [`hcc-model-card.md`](hcc-model-card.md) - canonical model documentation that pairs with this audit
- [`../references/compliance-and-enforcement.md`](../references/compliance-and-enforcement.md) - RADV, OIG, FCA context
- [`../references/meat-criteria.md`](../references/meat-criteria.md) - MEAT contract
- [`../references/evaluation-and-validation.md`](../references/evaluation-and-validation.md) - how override data feeds eval

---
*Audit performed against current ICD-10-CM Official Guidelines and applicable CMS HCC model. Final determinations require a credentialed coder (CRC/CCS). NLP-assisted audits do not transfer responsibility from the credentialed coder; NLP outputs are decision support, not the final determination.*
