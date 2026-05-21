# hipaa-compliance

A skill for engineering and compliance teams building or operating PHI-handling apps (web, mobile, SaaS, data, AI). Covers HIPAA Privacy / Security / Breach Notification Rules, BAA review, OCR audit prep, de-identification methodology, technical safeguards, vendor / cloud shared responsibility, and incident response. **Not** for clinical chart review (use [`medical-chart-review`](../medical-chart-review/)). **Not** for HEDIS NLP (use [`hedis-nlp`](../hedis-nlp/)). **Not** for HCC NLP (use [`hcc-nlp`](../hcc-nlp/)). **Not** for legal opinions (defer to healthcare counsel).

> ⚠️ Outputs are engineering and compliance guidance, not legal advice. Material compliance decisions - notification timing, OCR responses, BAA terms, breach determinations - require sign-off from a privacy officer, a security officer, and healthcare counsel.

## What this skill provides

For covered entities and business associates (engineering, security, and compliance teams), this skill packages the recurring HIPAA work that comes up when building or running a PHI-handling system:

- **The three Rules** in [`references/`](references/): Privacy Rule (uses / disclosures / minimum necessary / NPP / patient rights), Security Rule (admin / physical / technical safeguards with required vs addressable handling), Breach Notification Rule (4-factor risk assessment, 60-day rule, OCR / media / individual notice thresholds)
- **De-identification methodology**: Safe Harbor 18 identifiers (verbatim), Expert Determination method, re-identification risk in real data environments, limited data sets
- **BAA review**: 45 CFR 164.504(e) required clauses, subcontractor flow-down, common gaps and redlines library
- **OCR audit prep**: Phase 2 audit protocol structure, evidence inventory, the findings OCR sees most
- **Technical safeguards**: encryption at rest and in transit, key management, integrity, audit logs, automatic logoff, integrity controls
- **Access & authorization**: RBAC patterns, minimum necessary in practice, workforce lifecycle (provisioning / deprovisioning / emergency access), training cadence
- **Vendor / cloud shared responsibility**: AWS / Azure / GCP HIPAA-eligible services lists, what's covered by a BAA and what isn't, BAA-covered AI services (Bedrock, Azure OpenAI on Foundry, Vertex)
- **Incident response**: security incident vs reportable breach, IR playbook phases, forensics preservation, OCR coordination
- **State-law overlap** (high level only): CCPA, CMIA, 42 CFR Part 2, GDPR boundaries and preemption
- **Templates**: BAA review checklist, breach 4-factor risk assessment, NIST 800-30-style risk analysis, IR playbook, OCR audit evidence binder

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill hipaa-compliance
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## When the agent loads it

Triggered by requests like:

- "Review this BAA"
- "Do a HIPAA risk analysis for [system]"
- "Assess this incident - is it a breach?"
- "Prepare for an OCR audit"
- "De-identify this dataset" / "Safe Harbor vs Expert Determination?"
- "Design HIPAA technical safeguards for [feature]"
- "Review our cloud / vendor shared responsibility for PHI"
- "Write an incident response playbook"
- "Check if our app is HIPAA-compliant"
- "Review encryption / access control / audit log requirements"
- "Can we send PHI to [vendor / AI service]?"

Not triggered for: clinical chart review (`medical-chart-review`), HEDIS NLP (`hedis-nlp`), HCC NLP (`hcc-nlp`), legal opinions (defer to counsel), or handling identifiable PHI in non-compliant environments.

## Quick start

```text
We're adding a new AI feature that sends de-identified discharge summaries to
a third-party LLM. Walk me through: (1) the BAA / shared-responsibility check,
(2) whether "de-identified" actually clears HIPAA in this data environment,
(3) the risk-analysis updates we owe, and (4) the audit-log requirements.
```

The agent will run the PHI/scope gate from `SKILL.md` §0, then load [`references/vendor-cloud-shared-resp.md`](references/vendor-cloud-shared-resp.md), [`references/de-identification.md`](references/de-identification.md), [`references/security-rule.md`](references/security-rule.md), and [`templates/risk-analysis.md`](templates/risk-analysis.md).

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, task routing |
| [references/](references/) | The three Rules, de-id, BAA review, OCR audit prep, technical safeguards, access, vendor/cloud, IR, state overlap |
| [templates/](templates/) | BAA checklist, breach 4-factor, risk analysis, IR playbook, OCR evidence binder |

### References

- [privacy-rule.md](references/privacy-rule.md) - uses, disclosures, minimum necessary, NPP, patient rights, marketing / fundraising boundaries
- [security-rule.md](references/security-rule.md) - admin / physical / technical safeguards, required vs addressable, NIST 800-66 mapping
- [breach-notification.md](references/breach-notification.md) - 4-factor risk assessment, 60-day rule, OCR / media / individual notice thresholds
- [de-identification.md](references/de-identification.md) - Safe Harbor 18 IDs, Expert Determination, re-ID risk, limited data sets
- [baa-review.md](references/baa-review.md) - 45 CFR 164.504(e) clauses, subcontractor flow-down, common gaps
- [ocr-audit-prep.md](references/ocr-audit-prep.md) - Phase 2 audit protocol, evidence inventory, common findings
- [technical-safeguards.md](references/technical-safeguards.md) - encryption, key management, integrity, audit logs, automatic logoff
- [access-and-authorization.md](references/access-and-authorization.md) - RBAC, minimum necessary, workforce lifecycle, emergency access
- [vendor-cloud-shared-resp.md](references/vendor-cloud-shared-resp.md) - AWS / Azure / GCP eligible services, AI service BAA coverage
- [incident-response.md](references/incident-response.md) - security incident vs breach, IR phases, forensics, OCR coordination
- [state-laws-and-overlap.md](references/state-laws-and-overlap.md) - CCPA / CMIA / 42 CFR Part 2 / GDPR boundaries (high-level)
- [README.md](references/README.md) - index

### Templates

[baa-review-checklist.md](templates/baa-review-checklist.md) · [breach-risk-assessment.md](templates/breach-risk-assessment.md) · [risk-analysis.md](templates/risk-analysis.md) · [incident-response-playbook.md](templates/incident-response-playbook.md) · [ocr-audit-evidence-binder.md](templates/ocr-audit-evidence-binder.md)

## Related skills in this repo

- [`medical-chart-review`](../medical-chart-review/) - clinical chart review for clinicians, coders, CDI / quality auditors. Its `references/hipaa-privacy.md` is the reviewer-facing 18-identifier checklist used during chart abstraction; this skill is the broader builder / compliance-officer view.
- [`hedis-nlp`](../hedis-nlp/) - HEDIS NLP engineering. HIPAA questions arising from a HEDIS pipeline (BAA with a vendor, breach response for an extraction-pipeline incident) come back here.
- [`hcc-nlp`](../hcc-nlp/) - HCC / risk-adjustment NLP. Same pattern - pipeline-specific HIPAA questions route here.
- [`claims-ml`](../claims-ml/) - healthcare-ML failure-mode auditor. Same pattern - PHI handling questions arising from claims-ML model training / scoring environments (training-data BAAs, de-id strategy, breach handling for scoring pipelines) route here.

## Compliance & safety guardrails

- PHI verification before reviewing any system, dataset, or document
- No legal advice; defer to healthcare counsel for legal interpretation
- No fabricated CFR sections, OCR fines, notification deadlines, or state-law citations
- Required vs Addressable distinction enforced in every Security Rule output
- Every recommended control must point to an evidence artifact
- 4-factor breach risk assessment required before declaring "not reportable"
- Default to least-privilege and minimum-necessary in every access-pattern suggestion
- Risk analysis must be re-run on material system changes
- No PHI written to agent memory (session, repo, or user scope)
- Explicit deferral to privacy officer, security officer, and counsel for material compliance decisions

## Out of scope

- Legal opinions and contract interpretation (use counsel)
- OCR investigator workflows (this skill is for covered entities + BAs, not regulators)
- Deep state-by-state law (see `state-laws-and-overlap.md` for the high-level pointer)
- HIPAA training curriculum design (mention only as out-of-scope)
- Building or deploying HIPAA-compliant infrastructure (this skill produces compliance documentation and reviews, not infra code)
- Clinical chart review (use `medical-chart-review`)
- HEDIS / HCC NLP engineering (use `hedis-nlp` / `hcc-nlp`)
- Handling identifiable PHI without a confirmed HIPAA-compliant environment

## License / disclaimer

Use at your own risk. Outputs are advisory and must be reviewed by appropriately credentialed humans (privacy officer, security officer, healthcare counsel) before being used for OCR response, breach notification, BAA execution, or any compliance / regulatory submission.
