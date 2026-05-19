# BAA Review Checklist

> Pair with [`../references/baa-review.md`](../references/baa-review.md). Output of a completed review is this filled-in checklist plus a one-page memo (template at bottom).

## Metadata

| Field | Value |
|---|---|
| Counterparty (BA) | |
| Our role | CE / BA (us → subcontractor) |
| Service description | |
| PHI in scope | (categories) |
| Volume / sensitivity | |
| Reviewer | |
| Date | |
| Counsel involved | Y/N + name |
| Privacy officer involved | Y/N + name |
| Security officer involved | Y/N + name |

## Required clauses (45 CFR 164.504(e)(2))

For each row: present in the document? language meets HIPAA floor? language meets our internal standard? action required?

| # | Required clause | Present? | Meets floor? | Meets our standard? | Action |
|---|---|---|---|---|---|
| 1 | Permitted uses and disclosures (no broader than CE's own) | | | | |
| 2 | Prohibition on other uses/disclosures except as permitted, required by contract, or required by law | | | | |
| 3 | Appropriate safeguards (including Security Rule for ePHI) | | | | |
| 4 | Reporting impermissible use/disclosure, security incidents, breaches per 164.410 | | | | |
| 5 | Subcontractor flow-down (same restrictions and conditions) | | | | |
| 6 | Make PHI available for individual access / amendment / accounting | | | | |
| 7 | Make books and records available to HHS | | | | |
| 8 | Return or destroy PHI at termination; if not feasible, extend protections | | | | |
| 9 | Authorize CE termination on material breach by BA | | | | |

## Operational clauses (commonly negotiated)

| # | Clause | Present? | Notes / redline |
|---|---|---|---|
| 10 | BA → CE breach notification timing | | Target: ≤ 5 business days; ideal 24-72 hours |
| 11 | Security incident reporting scope (not limited to "successful with PHI") | | |
| 12 | Subcontractor list + flow-down BAA available on request | | |
| 13 | Indemnification | | Mutual; carve out gross negligence / willful misconduct |
| 14 | Cyber liability insurance + tech E&O | | Limits proportional to PHI volume/sensitivity |
| 15 | Audit rights / SOC 2 Type II + HITRUST in lieu of on-site | | |
| 16 | Return / destruction at termination - tight definition of "not feasible" + annual purge status until destroyed | | |
| 17 | De-identification by BA - allowed? if allowed, Safe Harbor or Expert Determination only; no re-ID; no sale | | |
| 18 | AI / ML training carve-out - BA cannot use PHI for model training/fine-tuning/eval without separate authorization | | |
| 19 | Subpoena handling - BA notifies CE before producing PHI in response to legal process | | |
| 20 | Choice of law / venue | | |
| 21 | Notice provisions (to whom, what address, what method) | | Verify and refresh annually |
| 22 | Data residency / location restrictions | | |
| 23 | Survival of obligations beyond termination | | |

## Vendor risk additions (when this BAA accompanies a vendor onboarding)

| # | Item | Evidence collected |
|---|---|---|
| 24 | SOC 2 Type II report current within 12 months + reviewed | |
| 25 | HITRUST or ISO 27001 + HIPAA mapping | |
| 26 | Penetration test summary within 12 months | |
| 27 | Encryption at rest + in transit; FIPS validation | |
| 28 | MFA + SSO supported | |
| 29 | Audit log export available | |
| 30 | Documented IR plan + last drill date | |
| 31 | Subcontractor / sub-processor list | |
| 32 | Public security incident history (last 3 years) | |

## Determination

- [ ] **Approve** as drafted
- [ ] **Approve with redlines** (attached)
- [ ] **Reject pending revision** (BA must address required clause gaps before re-review)
- [ ] **Reject** (BA cannot or will not meet HIPAA-required terms - escalate to counsel + sourcing for deal-stop)

## Memo template (one page, sign and retain)

```
BAA REVIEW MEMO
Counterparty:        [BA name]
Service:             [description]
PHI in scope:        [categories]
Reviewer:            [name, role]
Date:                [YYYY-MM-DD]
Counsel:             [name]

Summary recommendation: [Approve / Approve with redlines / Reject pending revision / Reject]

Required-clause status: [n of 9 present and adequate; gaps listed below]

Negotiated-clause status:
- Breach notification timing: [X business days vs target ≤5]
- Security incident reporting: [scope as drafted]
- Subcontractor flow-down: [present + evidence available / present + on-request only / absent]
- [continue for each material negotiated clause]

Vendor risk (if applicable):
- SOC 2 Type II current and reviewed: [Y/N + date]
- Material exceptions: [list]
- [other items]

Material gaps / redlines:
1. [clause - issue - proposed language]
2. [...]

Decision:
[ ] Approve [ ] Approve with redlines [ ] Reject pending revision [ ] Reject

Sign-offs:
- Reviewer:               [name + date]
- Privacy Officer:        [name + date]
- Security Officer:       [name + date] (if applicable)
- Counsel:                [name + date]
```

Retain memo + completed checklist + redlined contract for at least the contract term + 6 years post-termination.
