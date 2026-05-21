# Value set manifest

> Use this template to declare a value set (NCQA, eCQM, custom). Replace `{{...}}`.

---

## Identity

- **Name**: {{e.g., "Diabetes Mellitus Diagnoses"}}
- **OID**: {{e.g., 2.16.840.1.113883.3.464.1003.103.12.1001}}
- **Version**: {{e.g., 20240101 or MY2024}}
- **Steward**: {{NCQA | NLM | CMS | internal}}
- **Purpose**: {{one sentence}}

## Scope

- **Clinical concept**: {{free-text description of what the value set is meant to capture}}
- **Used by**:
  - {{HEDIS measure name and ID}}
  - {{eCQM measure ID}}
  - {{internal cohort / pipeline name}}

## Code system composition

| # | Code system | Version | Member count | Definition style |
|---|---|---|---|---|
| 1 | ICD-10-CM | FY2024 | {{N}} | Intensional pattern + enumerated |
| 2 | SNOMED CT US Edition | 2024-03-01 | {{N}} | ECL expression |
| 3 | ICD-9-CM | (legacy, for pre-2015 data) | {{N}} | Enumerated |

## Definition (intensional, if applicable)

### Per code system

**ICD-10-CM**:
```
Pattern: E10.*, E11.*, E13.*
Excludes: E10.A*, E11.A* (gestational, handled separately)
```

**SNOMED CT**:
```
<< 73211009 |Diabetes mellitus|
MINUS << 11530004 |Brittle diabetes mellitus| (handled separately)
```

**ICD-9-CM** (legacy):
```
Pattern: 250.*
```

## Expansion (deterministic)

- **Expansion source**: {{VSAC | NCQA Value Set Directory | internal terminology service}}
- **Expansion date**: {{YYYY-MM-DD}}
- **Expansion artifact**: `{{path or table reference}}`
- **Member count (current expansion)**: {{N total across code systems}}
- **Last refresh**: {{YYYY-MM-DD}}
- **Refresh trigger**: {{source code-system release | quarterly | annual}}

## Change-management

- **Versioning policy**: {{semver | date-based | NCQA MY}}
- **Version bump rules**:
  - **Patch**: code added / removed but clinical intent unchanged
  - **Minor**: clinical intent broadened / narrowed within same concept
  - **Major**: redefinition of the underlying concept
- **Refresh process**: {{step-by-step or link}}
- **Approval workflow**: {{role(s) that must approve a version bump}}

## Storage

- **Warehouse table**: `{{schema.value_set}}`
- **Key columns**: `oid, version, code_system, code`
- **Indexes**: `{{joins-supporting index columns}}`

## Downstream consumers

| Consumer | Use |
|---|---|
| `{{measure pipeline}}` | Numerator / denominator membership |
| `{{cohort definition}}` | Inclusion criterion |
| `{{feature engineering}}` | ML feature flag |

## Known limitations

- {{e.g., "SNOMED expansion uses US Edition; non-US data requires International Edition expansion"}}
- {{e.g., "ICD-9 enumeration is fixed (no future updates) since ICD-9 is frozen post-2015"}}
- {{e.g., "Custom additions (3 codes) beyond NCQA value set for internal pilot - documented in `{{file}}`"}}

## Compliance / licensing

- **Source licensing**: {{NCQA HEDIS | VSAC (UMLS) | public domain | other}}
- **Re-distribution**: {{allowed | restricted | internal-only}}
- **Attribution text**: {{required attribution if any}}

## Provenance

- **Source download**: {{URL or file path with date}}
- **Build / refresh script**: `{{path}}`
- **Output artifact hash**: {{content hash or git SHA}}

## Change log

| Date | Version | Change | Owner |
|---|---|---|---|
| {{YYYY-MM-DD}} | 1.0 | Initial manifest from NCQA MY2024 | {{name}} |
| {{YYYY-MM-DD}} | 1.1 | Refreshed expansion for FY2025 ICD-10-CM | {{name}} |

## Approval

- **Owner**: {{name}}
- **Last reviewed**: {{YYYY-MM-DD}}
- **Next review due**: {{YYYY-MM-DD}}
