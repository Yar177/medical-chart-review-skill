# Contributing

Thanks for your interest in improving this skill. Healthcare content has a high bar — please read this before opening a PR.

## Hard rules

1. **No PHI. Ever.** Do not include real patient data in issues, PRs, examples, or test fixtures. Use synthetic data (e.g., [Synthea](https://synthetichealth.github.io/synthea/)) or fully fabricated examples. PRs containing anything resembling real PHI will be closed immediately and the data purged from git history.
2. **Cite authoritative sources.** Clinical, coding, and quality content must cite primary sources:
   - ICD-10-CM: CMS / CDC NCHS Official Guidelines for Coding and Reporting
   - CPT: AMA CPT codebook
   - HCC: CMS Risk Adjustment model documentation (specify v24 / v28)
   - HEDIS: NCQA HEDIS Technical Specifications (specify measurement year)
   - CDI / queries: ACDIS / AHIMA Practice Briefs
   - Drugs: FDA labeling, Beers Criteria, Lexicomp/Micromedex references
   - Privacy: 45 CFR (HIPAA), 42 CFR Part 2
   - FHIR: hl7.org/fhir/R4 base spec + US Core / CARIN BB / Da Vinci IGs (pin version)
3. **No upcoding guidance.** Coding suggestions must be MEAT-supported. Provider-query examples must be non-leading per ACDIS/AHIMA 2022.
4. **No clinical decision support.** This skill reviews documentation. It does not diagnose, prescribe, or recommend treatment for real patients.
5. **Update the changelog.** Every PR touching `SKILL.md`, `references/`, or `templates/` updates `CHANGELOG.md`.

## What good contributions look like

- Fixing outdated code-set references (annual ICD-10-CM, HCC, HEDIS updates).
- Adding a new review-type template with a matching reference doc and `SKILL.md` routing entry.
- Tightening the safety gate or PHI handling.
- Adding synthetic worked examples under `examples/`.
- Documenting install paths for additional agent platforms.

## What to avoid

- Adding payer- or organization-specific policy without putting it behind a clearly-scoped file (e.g., `references/local-policy.md`) and noting it's not universal.
- Broadening scope into live clinical workflows.
- Adding dependencies, build steps, or executable code — this skill is intentionally plain Markdown.

## PR process

1. Open an issue first for anything larger than a typo or single-file edit.
2. Keep PRs focused — one concern per PR.
3. In the PR description, state:
   - What changed and why.
   - Which authoritative source(s) back the change.
   - Whether any reference-year pin in `CHANGELOG.md` needs to move.
4. A maintainer will review for clinical accuracy, compliance posture, and tone before merging.

## Reporting security or safety issues

See [SECURITY.md](SECURITY.md). Do not file public issues for prompt-injection vectors that bypass the PHI gate or for any defect that could cause clinical harm.
