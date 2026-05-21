# Crosswalk specification

> Use this template to specify any code-system crosswalk (vendor-supplied or custom). Replace `{{...}}`.

---

## Identity

- **Crosswalk name**: {{e.g., "ICD-10-CM → internal chronic-condition flags"}}
- **Owner**: {{team / individual}}
- **Created**: {{YYYY-MM-DD}}
- **Last reviewed**: {{YYYY-MM-DD}}
- **Status**: {{draft | active | deprecated}}
- **Version**: {{semver or date}}

## Purpose

{{One paragraph: what business / analytic question this crosswalk answers, and why an existing public crosswalk is insufficient.}}

## Source and target

| Property | Source | Target |
|---|---|---|
| **Code system** | {{e.g., ICD-10-CM}} | {{e.g., internal chronic-condition taxonomy}} |
| **Version** | {{e.g., FY2024}} | {{e.g., v3.2}} |
| **Authority** | {{NCHS/CMS}} | {{us}} |
| **Coverage scope** | {{e.g., all active codes}} | {{e.g., 24 chronic conditions}} |

## Cardinality

- [ ] 1:1 (one source → one target)
- [ ] 1:N (one source → multiple targets)
- [ ] N:1 (multiple sources → one target)
- [ ] N:M (multiple sources → multiple targets)

**Selected**: {{cardinality}}

**Implication for downstream joins**: {{how this affects row counts; whether deduplication is needed}}

## Definition

{{One of: enumerated table; SQL CASE / mapping rules; SNOMED ECL expression; pattern match on code; algorithmic logic. Show the actual definition or link to the source file.}}

### Example

```
{{Sample rows or pseudocode showing how a source code maps to target}}
```

## Fallback strategy for unmapped source codes

- [ ] Drop (silent)
- [ ] Drop with logging
- [ ] Map to "unknown" / "other" bucket
- [ ] Pass through (use source code as target)
- [ ] Route to human review queue
- [ ] Raise error

**Selected**: {{strategy}}

**Why**: {{justification - downstream consumer needs}}

## Direction symmetry

- **Forward** (source → target): {{always | conditional | not supported}}
- **Backward** (target → source): {{always | conditional | not supported}}
- **Round-trip**: {{lossless | lossy with documented characteristics}}

## Time validity

- **Source vintage(s) supported**: {{e.g., ICD-10-CM FY2022-FY2025}}
- **Target vintage(s) supported**: {{e.g., internal taxonomy v3.0+}}
- **What to do for older / newer source vintages**: {{rule}}

## QA / validation

- **Sample size for QA**: {{N rows reviewed}}
- **QA reviewer**: {{role / individual}}
- **QA criteria**:
  - {{e.g., "Every diabetes ICD-10 code maps to the 'Diabetes' chronic-condition category"}}
  - {{e.g., "No active ICD-10 code is silently dropped without 'Other' fallback"}}
  - {{e.g., "Round-trip on a 1000-code sample produces ≥99% match"}}
- **QA outcome**: {{date, summary, link to QA report}}

## Known limitations

- {{e.g., "Z-codes are not categorized; treated as 'Other' by default"}}
- {{e.g., "Codes added in FY2025 are not yet categorized; refresh planned by 2024-11-01"}}
- {{e.g., "External-cause codes (V-Y range) excluded by design"}}

## Refresh process

- **Trigger**: {{source code-system release date | quarterly review | downstream consumer request}}
- **Cadence**: {{annual | quarterly | as-needed}}
- **Owner**: {{team / individual}}
- **Steps**:
  1. {{download new source vintage}}
  2. {{run delta report against current crosswalk}}
  3. {{triage new / changed codes}}
  4. {{update crosswalk and bump version}}
  5. {{re-run QA on sample}}
  6. {{deploy to warehouse}}
- **Deprecation policy**: {{when prior versions are removed from warehouse}}

## Downstream consumers

| Consumer | Use | Sensitivity to crosswalk changes |
|---|---|---|
| `{{table / pipeline / model}}` | {{e.g., feature engineering for risk model}} | High - feature distribution shifts |
| `{{report}}` | {{e.g., chronic-condition prevalence report}} | Medium - numerator changes affect rates |

## Compliance / licensing

- **Source code-system licensing**: {{public | UMLS | AMA | NCQA | other}}
- **Target taxonomy licensing**: {{internal}}
- **Re-distribution allowed**: {{yes | no | internal-only}}
- **Attribution required**: {{text}}

## Provenance

- **Source data files used to build**: {{path or URL}}
- **Build script**: `{{repo/path/to/build-script}}`
- **Output artifact**: `{{path / table}}`
- **SHA / version hash**: {{git commit or content hash}}

## Change log

| Date | Version | Change | Owner |
|---|---|---|---|
| {{YYYY-MM-DD}} | 1.0 | Initial release | {{name}} |
| {{YYYY-MM-DD}} | 1.1 | Added {{N}} new ICD-10 codes from FY2025 | {{name}} |

## Approval

- **Reviewed by**: {{name, date}}
- **Approved by**: {{name, date}}
- **Next review due**: {{YYYY-MM-DD}}
