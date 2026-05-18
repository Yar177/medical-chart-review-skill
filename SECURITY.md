# Security Policy

## Scope

This skill is plain Markdown loaded by AI agents. There is no runtime, no network code, and no data persistence. The relevant "security" surface is therefore:

1. **Prompt-injection or jailbreak vectors** that cause an agent loading this skill to bypass the safety/PHI gate in `SKILL.md` §0.
2. **Compliance regressions** — content changes that could encourage HIPAA violations, upcoding, leading provider queries, unauthorized disclosure, or practicing medicine without a license.
3. **Clinical-harm vectors** — content errors that could lead a downstream user to a decision causing patient harm (wrong reference range, wrong critical value, wrong drug interaction, etc.).

## Reporting a vulnerability

**Do not open a public GitHub issue for any of the above.**

Email the maintainer privately with:

- A description of the issue and which file/section is affected.
- Steps to reproduce (for prompt-injection: the exact prompt that bypasses the gate, and which agent/model you tested on).
- Your assessment of impact.
- Any suggested fix.

Report privately via GitHub's [Security Advisories](../../security/advisories/new) ("Report a vulnerability" on the repo's Security tab). Do not use email and do not open a public issue.

You can expect:

- Acknowledgement within 5 business days.
- A fix or mitigation plan within 30 days for confirmed issues.
- Credit in `CHANGELOG.md` if you want it.

## Out of scope

- Bugs in the host AI agent (Claude, Copilot, Cursor, etc.) — report those to the vendor.
- Theoretical risks that require the user to already be misusing the skill against its documented scope.
- Requests to add features that would weaken the safety gate "for testing" or "for demos." These will be declined.

## PHI in reports

If your reproduction involves real PHI, **do not send it**. Reproduce with synthetic data (Synthea or fabricated) before reporting.
