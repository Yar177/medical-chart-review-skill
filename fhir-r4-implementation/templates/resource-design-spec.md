# FHIR resource design spec

> Use this template to specify a single FHIR resource shape - its profile, identity, must-support elements, extensions, search behavior, and conformance plan - before implementation. Replace `{{...}}`.
>
> All example payloads, identifiers, and URLs are `[synthetic]` placeholders.

---

## Identity

- **Resource name**: {{e.g., Patient}}
- **FHIR base version**: {{R4 4.0.1 | R4B 4.3.0 | R5 5.0.0}}
- **Profile**: {{canonical URL with version pin, e.g., `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0`}}
- **IG**: {{e.g., US Core 6.1.0 | CARIN BB 2.1.0 | custom}}
- **Owner**: {{team / individual}}
- **Created**: {{YYYY-MM-DD}}
- **Last reviewed**: {{YYYY-MM-DD}}
- **Status**: {{draft | active | deprecated}}

## Purpose

{{One paragraph: what this resource represents in the system, what consumer(s) read it, what producer(s) write it, what business / regulatory anchor it serves (e.g., CMS-0057-F Patient Access, US Core mandatory).}}

## Logical identity vs business identifier

| Property | Value |
|---|---|
| Logical id assignment | {{server-assigned | client-supplied via PUT | UUID}} |
| `identifier.system` | {{canonical URI for the issuing system, e.g., `http://payer.example.org/member`}} |
| `identifier.use` | {{usual \| official \| temp \| secondary}} |
| Uniqueness strategy | {{e.g., `(system, value)` uniqueness enforced via `If-None-Exist`}} |

## Must-support elements

> List every element that must be supported per the profile. For each, declare data source, transform, and missing-data strategy.

| Element | Must-support per profile? | Source data field | Transform | Missing-data strategy |
|---|---|---|---|---|
| {{element.path}} | {{yes \| no}} | {{source field}} | {{logic}} | {{omit \| Data Absent Reason \| populate with default}} |
| {{element.path}} | | | | |

## Extensions used

| Extension | Canonical URL (version-pinned) | Source data field | Required by profile? |
|---|---|---|---|
| {{extension name}} | {{`http://hl7.org/fhir/.../StructureDefinition/...|x.y.z`}} | {{source field}} | {{yes \| no}} |

## Bound code values

> For each coded element, declare the binding strength and how source codes are validated / mapped.

| Element | Bound value set | Binding strength | Source coding | Validation strategy |
|---|---|---|---|---|
| {{element.path}} | {{value set URL}} | {{required \| extensible \| preferred \| example}} | {{e.g., source uses ICD-10-CM}} | {{server-side `$validate-code` \| pre-mapped \| pass-through}} |

## References to other resources

| Reference element | Target resource | Profile (if any) | Resolution strategy |
|---|---|---|---|
| {{element.path}} | {{e.g., Patient}} | {{`us-core-patient\|6.1.0`}} | {{literal reference \| logical reference \| contained}} |

## Search parameters supported (declared in CapabilityStatement)

| Search param | Type | Combinations required | Notes |
|---|---|---|---|
| `_id` | token | - | |
| `identifier` | token | - | |
| {{param}} | {{type}} | {{combo list}} | |

## Required operations

| Operation | Why | Profile / IG anchor |
|---|---|---|
| `$validate` | preflight before write | base spec |
| {{e.g., `$member-match`}} | {{e.g., PDex payer-to-payer}} | {{IG ref}} |

## Worked example payload `[synthetic]`

```json
{
  "resourceType": "{{Resource}}",
  "meta": {
    "profile": ["{{canonical URL with version pin}}"]
  },
  "identifier": [...],
  "...": "..."
}
```

## Conformance plan

- [ ] HAPI Validator CLI passes (`-version {{x.y.z}} -ig {{ig#version}} -profile {{url}}`)
- [ ] Server `$validate` passes on insertion
- [ ] Inferno {{kit name}} green
- [ ] Sample data covers every must-support element + extension at least once
- [ ] Search-param combinations exercised in CI

## Sign-off

| Role | Name | Date |
|---|---|---|
| Designer | {{}} | {{}} |
| Reviewer (FHIR) | {{}} | {{}} |
| Reviewer (clinical / business) | {{}} | {{}} |
