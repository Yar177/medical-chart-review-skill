# acp-brochure-vs-discussion

## Synthetic note

```
Encounter date: 04/18/2025
Provider: Hassan, S. MD (Internal Medicine)
Patient age: 72
Visit type: Annual Medicare wellness visit

Subjective:
72F here for AWV. Reports overall good health. Active, lives independently.

A/P:
1. HTN - controlled on lisinopril 20 mg.
2. T2DM - A1c 6.9 (03/2025).
3. Health maintenance:
   - Mammogram up to date (01/2025)
   - Colonoscopy: 2019, due 2029
   - DXA: 2022, normal
   - Advance directive brochure provided to patient. Encouraged review.
   - Vaccines: flu given today, Shingrix series complete 2023.
4. Annual labs ordered.
```

## Expected extraction

```yaml
satisfies_numerator: false      # ACP brochure alone is NOT discussion
evidence: []
acp_failure_reason: |
  "Advance directive brochure provided" is distribution, not discussion.
  The note does not document:
  - Patient's preferences or wishes
  - Code status discussion
  - Healthcare proxy / surrogate decision-maker identification
  - Existing advance directive on file
  - POLST/MOLST
notes_for_reviewer: |
  Common false-positive shape. Pipelines that match "advance directive"
  without requiring substantive discussion content over-close ACP.
  Contrast: "Discussed advance care planning; patient wishes full code at
  this time, has named daughter as healthcare proxy, will complete
  advance directive form at next visit" - this satisfies ACP for MY.
  Even better with documentation of POLST or signed AD on file.
```

## Notes for reviewers

- Distinguish distribution (brochure given) from discussion (substantive content).
- COA-ACP follows the same logic; same documentation typically satisfies both ACP and COA-ACP.
- "Will discuss at next visit" is future intent and does NOT count.
- Some specs allow lifetime AD-on-file evidence; verify against current spec MY.
