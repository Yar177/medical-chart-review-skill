# Code system inventory

> Use this template to catalog the code systems present in your warehouse: source, version, owner, downstream consumers, refresh cadence. Replace `{{...}}` placeholders.

---

## Catalog entry

### Identity

- **Code system**: {{e.g., ICD-10-CM, HCPCS Level II, RxNorm, SNOMED CT US Edition}}
- **Owner / authority**: {{NCHS/CMS, AMA, NLM, etc.}}
- **License**: {{public domain | UMLS account | NCQA license | AMA Data File License | other}}
- **Current vintage in warehouse**: {{e.g., FY2024, MY2024, 2024-09 release}}
- **Vintage column**: {{warehouse field that records the vintage of each row}}

### Warehouse location

- **Table(s)**:
  - `{{schema.table}}` - reference table
  - `{{schema.table}}` - hierarchy / relationships (if applicable)
  - `{{schema.table}}` - historical versions / vintages
- **Primary key**: `{{code, vintage}}` (or other)
- **Row count (current vintage)**: ~{{N}}
- **Total row count (all vintages)**: ~{{N}}

### Ingest

- **Source URL**: {{official download URL}}
- **Source format**: {{ZIP, XLSX, CSV, RF2, FHIR, API}}
- **Refresh cadence**:
  - **Publisher cadence**: {{annual Oct 1 | quarterly | monthly | continuous}}
  - **Our refresh cadence**: {{when we re-ingest}}
  - **Grace period**: {{days between publisher release and our refresh}}
- **Ingest pipeline / job**: `{{repo/path/to/job}}`
- **Ingest owner**: {{team or individual}}
- **Last successful refresh**: {{date}}

### Vintage retention

- **Vintages retained**: {{e.g., "current + 5 historical"}}
- **Archive location**: {{cold storage path / table}}
- **Retention policy**: {{regulatory / business driver}}

### Downstream consumers

| Consumer | Type | Joins on | Refresh-sensitive? |
|---|---|---|---|
| `{{schema.table}}` | Fact table | `code = code_id` | Yes - DOS-vintage join required |
| `{{model name}}` | ML model | `code` features | Yes - feature definition pinned |
| `{{pipeline}}` | Pipeline | Code list lookups | Yes - value sets refresh on update |
| `{{report}}` | Report | Display only | No - cosmetic only |

### Drift monitoring

- **Drift monitoring job**: `{{job name}}` - runs {{cadence}}
- **Drift report delivered to**: {{stakeholder / channel}}
- **Last drift report**: {{date}} - {{summary: net additions, deletions, changes}}

### Known caveats

- {{e.g., "FY2024 added 200 codes; HCC mapping not yet updated"}}
- {{e.g., "Custom additions in `{{table}}` for internal taxonomies"}}
- {{e.g., "Vendor-specific aliases in `{{table.column}}` require cross-reference"}}

### Related code systems

- **Crosswalks to / from**: {{list of related crosswalks; reference `crosswalks` table}}
- **Value sets keyed on this system**: {{count, location}}
- **Groupers built from this system**: {{e.g., CCSR, Elixhauser for ICD-10-CM}}

### Compliance notes

- **PHI status**: {{none | indirect | direct}}
- **Licensing notice**: {{required attribution text, if any}}
- **Re-distribution restrictions**: {{public | internal-only | licensed-only}}

### Change log

| Date | Change | Owner |
|---|---|---|
| {{YYYY-MM-DD}} | Initial catalog entry | {{name}} |
| {{YYYY-MM-DD}} | Refreshed to {{vintage}} | {{name}} |
| {{YYYY-MM-DD}} | Added custom mapping for {{topic}} | {{name}} |

---

## Inventory roll-up

Repeat the entry above for each code system in scope. Maintain a master list (CSV or table) summarizing:

| Code system | Vintage | Refresh | Last refresh | Consumers | Owner |
|---|---|---|---|---|---|
| ICD-10-CM | FY2024 | Annual | 2023-10-01 | 14 | {{team}} |
| HCPCS Level II | 2024Q3 | Quarterly | 2024-07-01 | 9 | {{team}} |
| RxNorm | 2024-07 | Monthly | 2024-07-01 | 6 | {{team}} |
| ... | | | | | |
