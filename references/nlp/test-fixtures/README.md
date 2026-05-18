# Test fixtures for HEDIS chart-review NLP

Synthetic note snippets with expected extraction outcomes. Use as regression test seeds, annotation-training examples, and demonstration cases for stakeholders.

## Audience

NLP engineers, annotators, evaluation leads.

## Contents

| File | Measure family | What it demonstrates |
|---|---|---|
| `gsd-copy-forward.md` | GSD | Copy-forward A1c with stale date; should NOT count for current MY |
| `gsd-cgm-gmi.md` | GSD | CGM GMI as A1c alternative; sub-question on spec acceptance |
| `bcs-future-scheduled.md` | BCS-E | Mammogram scheduled but not done; future intent, NOT compliance |
| `ccs-vague-patient-report.md` | CCS-E | Patient-reported "had Pap last year" without document; uncertain |
| `col-modality-window.md` | COL-E | Colonoscopy modality with screening window |
| `fuh-7-day-calendar.md` | FUH | 7-day follow-up with weekend gap; calendar vs business days |
| `ppc-postpartum-window.md` | PPC-Postpartum | 7-84 day postpartum window edge cases |
| `wcv-sports-physical.md` | WCV | Sports physical without comprehensive components |
| `mrp-boilerplate.md` | MRP | "Medications reviewed" boilerplate; NOT reconciliation |
| `supd-prescription-vs-dispense.md` | SUPD | Prescription written vs pharmacy dispense |
| `ais-refusal.md` | AIS-E | Patient refusal documented; non-compliant for refused vaccine |
| `ked-two-component-mismatch.md` | KED | eGFR present, uACR missing; partial KED |
| `bpd-problem-list.md` | BPD | BP value with diabetes on problem list; inverse-rate direction |
| `dbm-follow-up-imaging.md` | DBM | Follow-up imaging after positive mammogram; report-date sensitivity |
| `trc-discharge-window.md` | TRC | Multi-sub-indicator discharge windows |
| `coa-med-review-eligibility.md` | COA-Med Review | Eligible provider role vs MA review |
| `acp-brochure-vs-discussion.md` | ACP | Brochure given vs discussion documented |
| `osw-bisphosphonate-context.md` | OSW | Bisphosphonate for non-osteoporosis indication |

## Fixture file format

Each fixture file has three sections:

1. **Synthetic note** - the source text (note body, OCR-style noise where applicable)
2. **Expected extraction** - YAML block describing what the model should produce
3. **Notes for reviewers** - what makes this fixture instructive

### Example skeleton

```markdown
# <measure>-<scenario>

## Synthetic note

<note text>

## Expected extraction

```yaml
satisfies_numerator: <true|false|uncertain>
evidence:
  - concept: <string>
    value: <string|null>
    date_of_service: <ISO date|null>
    date_source: <explicit|inferred|missing>
    assertion: <positive|negated|historical|...>
    provider_role: <string|unknown>
    section: <string>
    verbatim_snippet: <string>
exclusions_applied: [<string>]
notes_for_reviewer: <string>
```

## Notes for reviewers

<what makes this fixture instructive; common annotator confusions>
```

## How to use

- **Regression testing:** load each fixture, run your pipeline, compare output to expected. Diffs are regression signal.
- **Annotation training:** use the synthetic notes (without the expected block visible) as practice cases; compare annotator output to expected; calibrate
- **Stakeholder demos:** walk product / clinical / compliance through specific fixtures to show what the model handles and where it needs human review
- **CI integration:** automate fixture-based regression in your model build

## Synthetic-only disclaimer

All fixtures are synthetic. No real PHI. Identifiers, dates, names, and clinical details are fabricated for educational purposes. Do not use these fixtures as evidence in any real HEDIS submission.

## Adding new fixtures

When you discover a new failure mode in production:

1. Capture the pattern (de-identified, paraphrased to avoid PHI)
2. Write a synthetic fixture that exercises the pattern
3. Add the expected-extraction YAML
4. Link the fixture to a failure-mode catalog entry (see [`../evaluation-and-validation.md`](../evaluation-and-validation.md))
5. Add to your regression suite

## See also

- [`../evaluation-and-validation.md`](../evaluation-and-validation.md) - how regression fixtures fit into the broader evaluation strategy
- [`../annotation-guidelines.md`](../annotation-guidelines.md) - schema for the expected-extraction YAML
- [`../date-of-service.md`](../date-of-service.md) - DoS worked cases (alternative starter set)
- [`../negation-and-assertion.md`](../negation-and-assertion.md) - assertion worked cases (alternative starter set)
