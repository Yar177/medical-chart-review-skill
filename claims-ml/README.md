# claims-ml

An AI agent skill for auditing healthcare ML pipelines built on claims data. Designed for data-science teams building cost prediction, hospitalization / readmit prediction, ED utilization, disease onset, mortality, program-eligibility scoring, ICD-10 anomaly detection, and risk-stratification models on Medicare / Medicaid / commercial claims.

> ⚠️ This skill produces ML-engineering review, not actuarial certification, clinical guidance, or legal / fairness advice. Final model-deployment decisions require sign-off from a credentialed actuary, medical director, and compliance review.

This is one of five skills in this monorepo. For chart review see `medical-chart-review`; for HEDIS extractor engineering see `hedis-nlp`; for HCC extractor engineering see `hcc-nlp`; for HIPAA program work see `hipaa-compliance`.

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill claims-ml
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## Quick start

> *"Audit my feature spec for a 90-day hospitalization predictor on MA membership. Walk me through the safety gate first."*

> *"/claims-ml is prior-year RAF a leaky feature for predicting next-year cost?"*

The agent runs the PHI / scope check from `SKILL.md` §0, then audits feature spec, split design, target definition, metric set, baselines, production fitness, and fairness, citing references and producing findings using [templates/](templates/).

## When the agent loads it

Triggered by requests like:

- "review my feature spec" / "audit for target leakage" / "claims ML leakage check"
- "design train/test split for member-year data" / "split for claims data"
- "pick metrics for cost prediction" / "pick metrics for hospitalization" / "pick metrics for readmit"
- "build a claims ML model card" / "pre-deployment review"
- "drift monitoring spec" / "recalibration plan after V28"
- "is prior-year RAF a leaky feature?" / "which features are unsafe for daily scoring?"
- "competing risks for readmit" / "Tweedie vs log cost"
- "calibration by subgroup" / "fairness audit"
- "what baseline should I beat?"
- "review my ICD-10 anomaly detector" / "review my risk-stratification model"

**Not** triggered for: generic ML tutorials, sklearn / XGBoost / PyTorch how-to, MLOps tooling, FHIR / EDI ingestion, statistics basics, chart review, HEDIS / HCC NLP engineering, HIPAA program work.

## What it does

1. **Safety gate** - confirms PHI status, scope, and disclaimers before reviewing anything.
2. **Selects an audit type** - feature spec, leakage deep-dive, model card, pre-deployment checklist, recalibration plan.
3. **Runs a standard workflow** - orient → audit feature spec → audit split → audit target → audit metrics → audit baseline → audit production fitness → surface findings with severity and citations.
4. **Outputs** a structured review using the matching template.

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, routing |
| [references/](references/) | Deep domain knowledge, loaded on demand |
| [templates/](templates/) | Output formats, one per audit type |

### References (loaded only when needed)

- [target-leakage.md](references/target-leakage.md) - claim lag, lab-result lag, RAF circularity, look-ahead labels, retroactive attribution, death-feed lag, hospice flag lag
- [train-test-splits.md](references/train-test-splits.md) - member-year split, temporal holdout, MY-boundary, V24→V28 transition, COVID shock, episode-vs-member
- [target-definitions.md](references/target-definitions.md) - zero-inflated cost, Tweedie, competing risks, censoring, composite endpoints, onset semantics
- [evaluation-metrics.md](references/evaluation-metrics.md) - actuary vs ML lens, per-target metric guide, what AUROC hides
- [calibration-and-drift.md](references/calibration-and-drift.md) - PSI, prediction-distribution shift, realized-vs-predicted, MY-boundary retrain, V28 / COVID handling
- [production-scoring-constraints.md](references/production-scoring-constraints.md) - feature availability, latency, compute cost, scoring cadence
- [feature-engineering.md](references/feature-engineering.md) - rolling windows with claim lag, comorbidity rollups, episode grouping, missingness semantics, feature stability
- [baselines-and-benchmarks.md](references/baselines-and-benchmarks.md) - prior-year cost, prior-year admit, recency, 3-feature regression, industry ranges
- [fairness-and-equity.md](references/fairness-and-equity.md) - subgroup calibration, disparate impact, Obermeyer 2019, NAIC / CMS / state DOI guidance
- [target-types-and-projects.md](references/target-types-and-projects.md) - per-project pattern catalog (10 project types)

### Templates

[feature-spec-audit.md](templates/feature-spec-audit.md) · [leakage-audit-report.md](templates/leakage-audit-report.md) · [claims-ml-model-card.md](templates/claims-ml-model-card.md) · [pre-deployment-checklist.md](templates/pre-deployment-checklist.md) · [recalibration-plan.md](templates/recalibration-plan.md)

## Related skills in this repo

- [`medical-chart-review`](../medical-chart-review/) - chart-level review and abstraction; defer to this skill for clinical documentation, MEAT review, and care-setting taxonomy
- [`hcc-nlp`](../hcc-nlp/) - HCC extractor engineering; claims-ml consumes HCC extractor outputs as features and provides leakage / evaluation review for ML built on them
- [`hedis-nlp`](../hedis-nlp/) - HEDIS extractor engineering; claims-ml consumes HEDIS engine outputs as features and reviews downstream ML
- [`hipaa-compliance`](../hipaa-compliance/) - PHI handling on training data, de-identification methodology for analytics environments, BAA review for ML vendor stacks

## Compliance & safety guardrails

The skill enforces:

- **PHI verification** before reviewing any feature spec or notebook
- **No real-data examples** - all synthetic, tagged `[synthetic]`
- **Framework-agnostic** - pseudocode and YAML only; no sklearn / XGBoost / PyTorch / TensorFlow code
- **No actuarial certification, clinical advice, or legal interpretation**
- **Explicit deferral** to sibling skills and credentialed humans
- **Fairness gate** - regulatory questions trigger compliance-counsel deferral

## Customization tips

- Add `references/internal-benchmarks.md` for team-specific baseline performance ranges
- Add `references/scoring-platform-<X>.md` for stack-specific scoring-time latency tables
- Add `examples/` with 1-2 walked-through synthetic audits to anchor the agent's voice
