# ccs-vague-patient-report

## Synthetic note

```
Encounter date: 09/22/2025
Provider: Lopez, M. NP (Family Medicine)
Visit type: Annual wellness exam

Subjective:
35-year-old female here for annual exam. Reports she "had a Pap done last year
at the OB place I used to go to." Cannot recall specific date. No abnormal
bleeding, no pelvic pain.

PMH:
- None significant

Plan:
- Will request records from prior OB practice.
- If not obtained within 4 weeks, will offer in-office Pap today (deferred today).
```

## Expected extraction

```yaml
satisfies_numerator: uncertain     # patient-reported only; no document on file
evidence:
  - concept: cervical_screening
    value: null
    date_of_service: null
    date_source: missing
    date_confidence: low
    assertion: historical-patient-reported
    provider_role: unknown
    section: hpi
    verbatim_snippet: "had a Pap done last year at the OB place I used to go to"
exclusions_applied: []
notes_for_reviewer: |
  Patient-reported history without supporting document.
  CCS-E typically requires a dated, verifiable Pap/HPV result.
  Pipeline should flag for outreach (records request) rather than close.
  If records arrive later with a qualifying date, re-extract from the
  imported document and recompute the closure status.
```

## Notes for reviewers

- Avoid the temptation to close based on patient self-report.
- "Last year" is too vague to satisfy the spec's specific look-back windows.
- Flag for human review and outreach; do not auto-close.
- If outside records later arrive, extract the **document's** date, not the import date.
