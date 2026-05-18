# HCC NLP test fixtures

Synthetic chart snippets with expected HCC extraction outputs. Use as seed regression coverage for the failure modes described in the cross-cutting references.

**Synthetic data only.** No real or de-identified PHI. All names, dates, MRNs, and providers are fabricated. Safe to commit, share, and use in CI.

## Fixtures

| File | Failure mode it covers | Primary references |
|---|---|---|
| [`history-of-trap.md`](history-of-trap.md) | "h/o breast cancer" should NOT fire C50 (active) | [`../negation-and-assertion.md`](../negation-and-assertion.md) |
| [`hierarchy-collapse.md`](hierarchy-collapse.md) | DM with neuropathy should fire HCC 18 alone, NOT both HCC 18 + HCC 19 | [`../hierarchies.md`](../hierarchies.md) |
| [`status-code-amputation.md`](status-code-amputation.md) | BKA patient needs Z89.5x; not active wound; annual recapture | [`../negation-and-assertion.md`](../negation-and-assertion.md) |
| [`meat-gap.md`](meat-gap.md) | Problem list says CHF, no MEAT in note - invalid for HCC | [`../meat-criteria.md`](../meat-criteria.md) |
| [`problem-list-only.md`](problem-list-only.md) | Diagnosis only in problem list, never assessed - invalid for RADV | [`../extraction-patterns.md`](../extraction-patterns.md) |

## Usage

1. **As regression tests.** Feed the synthetic note into your extractor; assert that the structured output matches "Expected extraction." Mismatches are real bugs.
2. **As annotation training.** Have new annotators label these notes blind, then compare to the expected output. Discuss disagreements against the cross-cutting references.
3. **As pipeline-architecture sanity checks.** If your pipeline cannot pass these, it has fundamental issues that real-data evaluation will surface eventually.

## Format

Each fixture has:

- `## Synthetic note` - the chart text in a fenced block
- `## Expected extraction` - the structured output your pipeline should produce
- `## Notes for reviewers` - what the failure mode looks like, why it matters, and what an adequate pipeline gets right

## Adding fixtures

When you discover a new failure mode in your real-data evaluation:

1. Build a minimal synthetic note that reproduces it
2. Annotate the expected output
3. Add the failure mode to the failure-mode catalog described in [`../evaluation-and-validation.md`](../evaluation-and-validation.md)
4. Open a PR adding the fixture here

Synthetic notes only. Never commit real or de-identified PHI to this repository.

## See also

- [`../README.md`](../README.md) - HCC NLP overview
- [`../evaluation-and-validation.md`](../evaluation-and-validation.md) - how to use fixtures in your eval pipeline
- Sibling `hedis-nlp` skill, `references/nlp/test-fixtures/` - parallel HEDIS fixtures
