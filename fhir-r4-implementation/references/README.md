# references/ - reading order

The 15 reference files in this directory are grouped below by topic. Load only what your task needs; the `SKILL.md` §2 task-routing table is the canonical entry point.

## Core mechanics

- [resource-taxonomy.md](resource-taxonomy.md) - resource categorization (Foundation / Base / Clinical / Financial / Workflow / Conformance / Admin), R4 vs R4B vs R5 deltas, which resources matter for which use case
- [resource-identity-and-versioning.md](resource-identity-and-versioning.md) - reference vs contained vs `_include` / `_revinclude`, `meta.versionId`, ETag, conditional read / update, `_history`, canonical URL semantics
- [search-parameters.md](search-parameters.md) - syntax, modifiers, prefixes, chaining + `_has`, pagination (`_count`, `next`), `_sort`, `_summary`, `_elements`, `_total` cost, per-resource cheatsheet
- [bundles-and-transactions.md](bundles-and-transactions.md) - Bundle types, transaction atomicity, `urn:uuid:` cross-entry refs, `If-None-Exist`, `ifMatch`, conditional ops, batch vs transaction, chunking
- [fhirpath.md](fhirpath.md) - core expressions, common payer / EHR patterns, FHIRPath in profile invariants and `$validate` and SearchParameter expressions

## Conformance + terminology + operations

- [profiles-and-conformance.md](profiles-and-conformance.md) - `StructureDefinition`, profile vs extension vs slicing, **extension authoring** (URL design, `value[x]`, modifierExtension), must-support semantics, discriminators, binding strength, `CapabilityStatement` shape
- [terminology-services.md](terminology-services.md) - `CodeSystem`, `ValueSet`, `ConceptMap`, `$expand`, `$validate-code`, `$translate`, `$lookup`, binding strength, terminology server options (pointer to `healthcare-code-systems` for code selection)
- [operations.md](operations.md) - `OperationDefinition`, standard Operations (`$everything`, `$validate`, `$expand`, `$match`, `$translate`, `$populate`, `$document`), custom Operations, Subscription R4 vs R5 `SubscriptionTopic`

## Auth + bulk + IGs

- [smart-on-fhir.md](smart-on-fhir.md) - App Launch v2 (EHR + standalone), scopes v2, PKCE, refresh, `aud` validation, Backend Services (system scopes, JWKS, asymmetric client auth), launch context, common Inferno failures
- [bulk-data-export.md](bulk-data-export.md) - `$export` async pattern (kick-off, status poll, NDJSON, cleanup), Group / Patient / System scope, `_since` delta, partial-failure handling (defers auth to `smart-on-fhir.md` §Backend Services)
- [us-core-ig.md](us-core-ig.md) - US Core profile catalog, must-support per profile, USCDI v1-v5 → US Core 3.x-8.x version map, common conformance gaps, Inferno (g)(10) test kit pointer
- [carin-bb-ig.md](carin-bb-ig.md) - `ExplanationOfBenefit` profile family (Inpatient / Outpatient / Professional / Pharmacy / Oral), mapping internal claims → EOB, CARIN BB 1.x vs 2.x, common payer pitfalls
- [da-vinci-overview.md](da-vinci-overview.md) - Da Vinci IG map (HRex, PDex, Plan-Net, CRD / DTR / PAS pointer), distinguishing PDex from CARIN BB, CDS Hooks primer, Da Vinci Inferno kits

## Closing (load last when authoring; load first when debugging)

- [conformance-testing.md](conformance-testing.md) - Inferno (ONC g(10), Bulk Data, SMART App Launch, Da Vinci kits), Touchstone, HAPI validator CLI, server `$validate`, FHIR validator vs profile-aware validators, CI integration, pre-cert checklist
- [common-pitfalls.md](common-pitfalls.md) - ~15 anti-patterns with worked synthetic examples (identifier matching, must-support misread, `_total` cost, `_include` abuse, R4/R4B/R5 mixing, conditional ops, `urn:uuid:`, OperationOutcome, Subscription migration, missing Provenance / AuditEvent)

---

## Reading order for common goals

| Goal | Read these, in order |
|---|---|
| **First-time orientation to FHIR R4** | `resource-taxonomy.md` → `resource-identity-and-versioning.md` → `search-parameters.md` → `bundles-and-transactions.md` → `common-pitfalls.md` |
| **Building a SMART on FHIR app (EHR launch)** | `smart-on-fhir.md` → `us-core-ig.md` → `search-parameters.md` → `conformance-testing.md` |
| **Building a SMART Backend Services job (Bulk Data)** | `smart-on-fhir.md` → `bulk-data-export.md` → `conformance-testing.md` |
| **Building a CARIN BB payer API (CMS-9115-F / CMS-0057-F)** | `carin-bb-ig.md` → `profiles-and-conformance.md` → `smart-on-fhir.md` → `bulk-data-export.md` → `conformance-testing.md` |
| **Auditing a vendor FHIR export against US Core** | `conformance-testing.md` → `us-core-ig.md` → `profiles-and-conformance.md` → `common-pitfalls.md` |
| **Mapping internal claims → CARIN BB EOB** | `carin-bb-ig.md` → `profiles-and-conformance.md` → `terminology-services.md` → `resource-identity-and-versioning.md` |
| **Da Vinci orientation for a payer roadmap** | `da-vinci-overview.md` → `carin-bb-ig.md` → `smart-on-fhir.md` |
| **Authoring a profile / extension / slicing** | `profiles-and-conformance.md` → `fhirpath.md` → `terminology-services.md` → `conformance-testing.md` |
| **Debugging an OperationOutcome / search performance / Bundle failure** | `common-pitfalls.md` → matching deeper file |
