# fhir-r4-implementation

A skill for integration engineers, EHR-app developers, payer-API teams, digital-health startups, and conformance reviewers. Covers HL7 FHIR R4 / R4B implementation - resource modeling, search, Bundles, FHIRPath, profiles + extensions + slicing + must-support, `CapabilityStatement`, standard + custom Operations, terminology services (pointer to `healthcare-code-systems`), US Core, CARIN Blue Button, Da Vinci (HRex / PDex / Plan-Net orientation + CDS Hooks primer), SMART App Launch v2 + Backend Services, Bulk Data Export, and conformance testing (Inferno, HAPI validator, Touchstone). **Not for clinical NLP on FHIR narratives** (use `hcc-nlp`, `hedis-nlp`). **Not for chart review** (use `medical-chart-review`). **Not for code-system / value-set authoring** (use `healthcare-code-systems`). **Not for HIPAA program work** (use `hipaa-compliance`).

> ⚠️ Outputs are FHIR implementation guidance, not certified conformance attestations. Any production claim of US Core / CARIN BB / Da Vinci / ONC g(10) conformance requires a passing run at an ONC-Authorized Testing Lab (ATL). CMS-9115-F + CMS-0057-F (Patient Access API, Provider Access API, Payer-to-Payer API, Prior Authorization API - **effective January 1, 2027** for impacted payers) attestations follow the CMS process. This skill prepares teams; it does not certify them.

## What this skill provides

- **Per-mechanic and per-IG references** in [`references/`](references/) covering the full FHIR R4 / R4B + payer / EHR-app stack:
  - Core mechanics: resource taxonomy, identity + versioning, search (modifiers / prefixes / chaining / `_has` / pagination), Bundles + transactions, FHIRPath
  - Conformance: `StructureDefinition`, profile + extension + slicing + must-support, `CapabilityStatement`, terminology services (`$expand` / `$validate-code`), Operations (standard + custom + Subscription / `SubscriptionTopic`)
  - Auth + bulk: SMART App Launch v2 (EHR + standalone, scopes v2, PKCE), SMART Backend Services (system scopes, JWKS, asymmetric client auth), Bulk Data Export `$export` async pattern
  - IGs: US Core 3.x → 7.x (USCDI v1 → v4) profile catalog + must-support; CARIN Blue Button 1.x / 2.x `ExplanationOfBenefit` family; Da Vinci HRex / PDex / Plan-Net orientation + CDS Hooks primer; full PAS / CRD / DTR depth deferred to future `prior-auth-da-vinci` skill
  - Closing: conformance testing (Inferno ONC g(10) / Bulk Data / SMART App Launch / Da Vinci kits, HAPI validator, Touchstone), common pitfalls (~15 anti-patterns with worked synthetic examples)
- **Templates** in [`templates/`](templates/):
  - `resource-design-spec.md` - declarative spec for shaping a FHIR resource for a use case (identity, profile, must-support, extensions, search, example payload, conformance plan)
  - `capability-statement-skeleton.md` - starter `CapabilityStatement` for a payer-API or EHR-app server with placeholders + must-support per IG
  - `claims-to-eob-mapping.md` - mapping spec from internal claims schema to CARIN BB `ExplanationOfBenefit` with per-field lineage, profile target, cardinality, transformation, unmapped strategy, validator output, sign-off
  - `smart-app-launch-checklist.md` - pre-Inferno checklist for SMART app devs (scopes, PKCE, `aud`, refresh, context handling, secure storage, common Inferno test IDs)
  - `fhir-conformance-audit.md` - audit-report template for "is this vendor FHIR export US Core X.y compliant" (resources in scope, profile pinning, MS-element evidence per resource, validator output, gaps, severity, remediation, sign-off)

## Install

[![skills.sh](https://skills.sh/b/Yar177/medical-chart-review-skill)](https://www.skills.sh/Yar177/medical-chart-review-skill)

```bash
npx skills add Yar177/medical-chart-review-skill --skill fhir-r4-implementation
```

See the [root README](../README.md) for manual install, agent targeting, and global vs project scope.

## When the agent loads it

Triggered by requests like:

- "Write a US Core Patient resource for our payer API"
- "Design a FHIR search for all Encounters for a patient in the last year with `_revinclude` for Conditions"
- "Build a transaction Bundle that creates a Patient + Encounter + Observation with `urn:uuid:` cross-refs"
- "Validate this Observation against US Core 6.1.0"
- "Author a slice on `Patient.identifier` for MRN vs SSN"
- "Write a FHIRPath expression for `Observation.value.ofType(Quantity).value > 200`"
- "Design the SMART on FHIR launch flow for our EHR app (standalone launch, scopes v2)"
- "Build a SMART Backend Services client for Bulk Data `$export`"
- "Map our internal institutional claims to CARIN BB `ExplanationOfBenefit` Inpatient profile"
- "Audit this vendor FHIR export against US Core 6.1.0 - what's missing?"
- "Prep for Inferno ONC g(10) - what should the CapabilityStatement look like?"
- "Why is `_revinclude=Observation:patient` blowing up our HAPI server?"
- "What's the difference between CARIN BB and Da Vinci PDex for member access?"
- "CDS Hooks primer - what's the difference between a hook and a card?"
- "Subscription R4 vs `SubscriptionTopic` in R5 - what's the migration path?"

Not triggered for: code-system / value-set authoring (use `healthcare-code-systems`), HIPAA program work (use `hipaa-compliance`), chart review (use `medical-chart-review`), clinical NLP on FHIR narratives (use `hcc-nlp` or `hedis-nlp`), claims ML feature engineering (use `claims-ml`), C-CDA / USCDI documents (future `ccda-uscdi-documents` skill), HL7 v2 (future `hl7v2-message-handling` skill), full Da Vinci PAS / CRD / DTR depth (future `prior-auth-da-vinci` skill), ONC certification workflows (defer to ATL).

## Quick start

```text
We're a Medicare Advantage plan building the Patient Access API for the
CMS-0057-F January 2027 deadline. We need to expose claims as CARIN BB
ExplanationOfBenefit, with SMART on FHIR member-facing auth, and pass
Inferno before submitting our CMS attestation. What's the minimum
implementation surface, in what IG versions, and what's our validation
plan?
```

The agent will run the §0 gate from `SKILL.md`, then load [`references/carin-bb-ig.md`](references/carin-bb-ig.md), [`references/smart-on-fhir.md`](references/smart-on-fhir.md), [`references/profiles-and-conformance.md`](references/profiles-and-conformance.md), [`references/conformance-testing.md`](references/conformance-testing.md), [`templates/claims-to-eob-mapping.md`](templates/claims-to-eob-mapping.md), and [`templates/fhir-conformance-audit.md`](templates/fhir-conformance-audit.md).

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point - workflow, safety gates, task routing |
| [references/](references/) | All FHIR reference content (15 files + index) |
| [templates/](templates/) | Resource spec, CapabilityStatement, claims-to-EOB, SMART checklist, conformance audit (5 files) |

## Related skills in this repo

- `healthcare-code-systems` - code systems, value sets (VSAC), OIDs, crosswalks, terminology version pinning. This skill defers `CodeSystem` / `ValueSet` selection there and covers FHIR mechanics (`$expand`, `$validate-code`, binding strength) here.
- `hipaa-compliance` - HIPAA Privacy / Security / Breach Notification, BAA review, technical safeguards. This skill covers FHIR `Provenance` / `AuditEvent` resource shape; the HIPAA audit-log *program* lives there.
- `medical-chart-review` - clinician / coder / CDI / auditor lens on charts. FHIR-shaped charts (Bundle / DocumentReference / Composition) are this skill's territory; clinical reading of them lives there.
- `hedis-nlp` - HEDIS NLP per-measure extraction. When the source data is FHIR-shaped, the resource model lives here.
- `hcc-nlp` - HCC NLP per-HCC extraction. When the source data is FHIR-shaped, the resource model lives here.
- `claims-ml` - supervised ML on claims. FHIR is out of scope there; the FHIR layer is this skill.

## Compliance & safety guardrails

- Pin FHIR base version (R4 / R4B / R5) and every IG version (US Core x.y, CARIN BB x.y, Da Vinci IG releases, SMART App Launch, Bulk Data) on every artifact
- Cite `hl7.org/fhir/R4/...` canonical URLs; do not cite third-party doc mirrors as authority
- Never invent profile URLs, search parameter names, extension URLs, value-set canonical URLs, or `OperationDefinition` names
- Synthetic data only; every example payload `[synthetic]`-marked; no real PHI even in tests
- Validate in three layers (HAPI CLI → server `$validate` → Inferno) before any conformance claim
- Defer ONC certification claims to an ONC-Authorized Testing Lab (ATL)
- Defer HIPAA program work to `hipaa-compliance`; defer code-system / value-set work to `healthcare-code-systems`
- Surface CMS-0057-F January 2027 deadline when payer scope is in play

## Out of scope

- Authoring custom FHIR IGs (this skill helps you read them; authoring is its own multi-month workflow)
- Full Da Vinci PAS / CRD / DTR prior-auth depth (future `prior-auth-da-vinci` skill)
- C-CDA / USCDI document mapping (future `ccda-uscdi-documents` skill)
- HL7 v2 → FHIR mapping depth (future `hl7v2-message-handling` skill; this skill points at the official v2-to-FHIR mapping IG only)
- FHIR server selection / hosting / scaling / cost
- Production deployment, CI/CD, infra-as-code
- ONC certification / ATL workflows (orientation pointer only)
- Clinical or coding judgment derived from FHIR resource contents
- Real-PHI examples (synthetic only)
- Code-system / value-set authoring (use `healthcare-code-systems`)
- HIPAA program design (use `hipaa-compliance`)

## License / disclaimer

MIT-licensed agent content. HL7®, FHIR®, US Core®, CARIN Blue Button®, and Da Vinci IG names are trademarks of their respective owners. The IG specifications and the FHIR base spec are published by HL7 International under the HL7 license; this skill does not redistribute any IG package - it explains structure, points at authoritative `hl7.org` URLs, and surfaces conformance + version-pinning practice. ONC, CMS, and NCQA regulatory references are summaries only and are not legal or compliance advice; defer to counsel and the impacted-payer compliance program for attestation strategy.
