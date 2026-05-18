# Compliance and enforcement context for HCC NLP

> **Why this file exists:** HCC pipelines do not just produce data - they produce inputs to billing that the government can later audit and prosecute. Teams that build HCC NLP without understanding the RADV / FCA / OIG context calibrate precision wrong, do not invest in audit defense, and put their plan at material risk.

This is context for NLP and analytics engineers, not legal advice. Your plan's compliance team is the authoritative voice for any specific decision.

---

## 1. The enforcement landscape, briefly

Three overlapping regimes apply to HCC submissions:

| Regime | Mechanism | Stakes |
|---|---|---|
| **CMS RADV** | Annual contract-level audit of Medicare Advantage HCC submissions | Refund of overpayments; extrapolated penalties at contract level |
| **OIG audits** | HHS Office of Inspector General targeted audits, often plan-specific | Refunds, corrective action plans, potential referral to DOJ |
| **DOJ / False Claims Act (FCA)** | Civil and criminal liability for knowing submission of false claims | Treble damages + per-claim penalties; potential criminal exposure for executives |

Whistleblower (qui tam) actions under FCA have driven most of the high-dollar settlements. Internal employees who observe over-coding patterns can file under seal; DOJ investigates and decides whether to intervene.

## 2. Notable recent settlements (context only, not exhaustive)

The major MA risk-adjustment settlements over the last decade have generally involved:

- Allegations of "one-way chart reviews" that added HCCs without also removing unsupported ones
- Allegations of pressuring or incentivizing providers to add diagnoses without independent clinical support
- Allegations of accepting NLP / chart-review output without sufficient human validation
- Settlement amounts ranging from tens of millions to over a billion dollars
- Often paired with Corporate Integrity Agreements requiring multi-year compliance program oversight

The pattern that matters for NLP teams: **precision-light pipelines that auto-submit are the failure mode**. High-recall suspect engines are fine. High-precision validate engines with human review are fine. Auto-submission without per-claim human validation is the high-risk shape.

## 3. RADV mechanics (operational view)

CMS RADV audits sample member-years from the plan's submissions. For each sampled member-year:

- The plan must produce the medical records supporting each claimed HCC.
- CMS coders re-review the records under HCC documentation standards.
- Validated HCCs stand; invalid HCCs are denied.
- The plan refunds the excess RAF dollars for that sample.
- Under certain rules (extrapolation), refund obligations can scale beyond the sample to the contract population.

NLP-relevant implications:

- The plan must be able to produce the exact supporting chart and span for every claimed HCC. **Provenance is non-negotiable.**
- If the pipeline auto-submitted an HCC with no human review, the plan still owns the audit risk.
- Validate-engine precision below 90% on the sample population translates to material refund exposure.
- Records that are illegible (poor OCR), incomplete (missing pages), or unsigned do not validate even if the diagnosis is technically present.

## 4. The "two-way" review obligation

Plans are expected to do "two-way" chart reviews:

- Add HCCs the encounter supports but the provider's claim did not include
- **Remove** HCCs the provider claimed but the encounter does not support

NLP teams almost always build the first side first. The second side (deletion / non-submission of unsupported HCCs) is equally important and often missing.

**Pipeline implication:** A validate engine that produces both "this claim is supported" and "this claim is not supported, recommend non-submission" outputs is a much stronger compliance posture than one that only adds.

## 5. Precision targets and the asymmetric cost of errors

| Error | Direct cost | Audit cost | Total exposure |
|---|---|---|---|
| **False negative** (missed HCC) | RAF dollars not captured | None | Linear, recoverable next year |
| **False positive** (over-claimed HCC) | RAF dollars over-paid | Refund + potential FCA + reputational | Often 3-10x the direct cost |

This asymmetry is why HCC precision targets are typically much higher than HCC recall targets.

A common framing:

- For **auto-validation** (no human in the loop): require validate-engine precision above 0.97 on a held-out gold set.
- For **human-in-the-loop** (every prediction reviewed before claims submission): validate-engine precision can be lower because human reviewers catch the false positives, but the reviewers must be properly trained and the workflow must be auditable.

Pure auto-submission of HCC predictions is rare at mature plans and is the configuration that has driven most settlements.

## 6. The "documentation integrity" workflow

Many plans operate a clinical documentation integrity (CDI) or provider-query function alongside HCC NLP:

- Pipeline surfaces suspect HCCs and weak validate HCCs
- CDI clinician reviews the chart
- If supportive evidence exists but the documentation is ambiguous, CDI sends a non-leading query to the provider
- Provider amends documentation (or declines)
- Resulting documentation is re-evaluated by the pipeline + reviewer

This is the strongest compliance shape: pipeline output is workflow signal, not direct claims input. NLP teams should design suspect-engine outputs to feed this workflow.

**Compliance landmines in the query process:**

- Leading queries ("Would you like to add 'diabetes with chronic complications'?") are not acceptable
- Pre-filled diagnosis suggestions in EHR templates create RADV exposure
- Queries that imply payment incentive create FCA exposure
- Provider attestations to copy-forward templates without independent review create exposure

NLP outputs that drive any of these patterns should be reviewed by Compliance before deployment.

## 7. Specific NLP-pipeline practices that increase risk

- Auto-submitting validate-engine output to claims without human review
- Suspect engines that surface HCCs to providers as "you should code this" rather than "consider reviewing this"
- Templates that auto-populate problem-list HCCs into the current note's assessment
- Pipelines that count any mention as evidence regardless of section or assertion
- Pipelines without version-pinning (cannot reconstruct what was submitted and why)
- Pipelines with no MEAT enforcement
- Pipelines that do not check encounter eligibility (lab-only encounters, unsigned notes)
- Pipelines that aggregate across years without calendar-year boundaries

## 8. NLP-pipeline practices that reduce risk

- Suspect / validate split with different precision targets
- Full provenance per extraction
- Version-pinning of code-set, crosswalk, coefficients, and pipeline
- Explicit MEAT and assertion records
- Human-in-the-loop validation before claims submission
- Two-way review (additions and deletions)
- Periodic internal RADV simulations (see [`evaluation-and-validation.md`](evaluation-and-validation.md))
- Failure-mode catalog with regression coverage
- Audit logs that show why each HCC was or was not submitted
- Compliance review of pipeline changes that affect precision

## 9. Documentation NLP teams should produce

For compliance, every deployed pipeline should have:

- Model card per HCC (use [`../../templates/hcc-model-card.md`](../../templates/hcc-model-card.md))
- Operational runbook (what the pipeline does, where outputs go, who reviews them)
- Version history (model, code-set, crosswalk, coefficients per release)
- Internal RADV simulation results, current and trended
- Failure-mode catalog
- Change log per release

This documentation matters in three places: internal compliance review, external audit response, and litigation discovery.

## 10. When to escalate

NLP teams should escalate to Compliance / Legal when:

- A pipeline change would materially increase precision risk (e.g., reducing human review)
- Audit results show a pattern of unsupported HCCs in a specific provider group, specialty, or template
- An employee raises concerns about pipeline behavior
- Internal RADV simulation results trend down for any HCC
- A new EHR template or vendor feed introduces unfamiliar documentation patterns
- The pipeline is asked to submit HCCs based solely on outside-record content
- The pipeline is asked to apply different precision standards to "high-value" HCCs than to common ones

Escalation is cheap. The settlements that drive industry-wide changes are the ones where employees did not escalate.

## 11. The mindset

The MA risk-adjustment system is funded by taxpayer Medicare dollars. Every false-positive HCC is, in effect, an over-billing to the federal government. The compliance regime treats it that way.

NLP teams that internalize this calibrate their work correctly. Teams that treat HCC NLP as a generic information-extraction problem produce technically-correct work that fails the compliance test.

## See also

- [`evaluation-and-validation.md`](evaluation-and-validation.md) - RADV simulation pattern
- [`extraction-patterns.md`](extraction-patterns.md) - suspect / validate split
- [`meat-criteria.md`](meat-criteria.md) - the MEAT contract that drives validation
- [`../../templates/hcc-model-card.md`](../../templates/hcc-model-card.md) - documentation expected per HCC
