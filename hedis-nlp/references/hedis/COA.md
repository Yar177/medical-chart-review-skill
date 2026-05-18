# COA — Care for Older Adults

**Reporting path:** Hybrid historically; ECDS direction
**Population focus:** Adults 66+ (historically Medicare Advantage Special Needs Plans; some programs broader)
**Sub-indicators (each evaluated independently):**
1. **COA-ACP** — Advance Care Planning
2. **COA-Med Review** — Medication Review
3. **COA-Func Status** — Functional Status Assessment
4. **COA-Pain Assess** — Pain Assessment

## Denominator

- Members 66+ as of end of MY
- Continuous enrollment through MY
- Program-defined enrollment (historically Medicare Advantage SNP; verify current spec for line of business)

## Sub-indicator numerators (during MY)

### COA-ACP
Documentation of advance care planning discussion, advance directive, surrogate decision-maker, or POLST/MOLST during MY.
→ Overlaps with standalone [ACP](ACP.md) measure - same documentation typically satisfies both. Check spec - some specs accept lifetime evidence for COA-ACP vs MY-only for ACP.

### COA-Med Review
- Medication review conducted by a prescribing practitioner or clinical pharmacist during MY, AND
- Medication list documented in the medical record

Both elements required - the review without a list, or the list without explicit review, does NOT satisfy.

### COA-Func Status
Functional status assessment using one of:
- Notation that ADLs (activities of daily living) were assessed
- Notation that IADLs (instrumental ADLs) were assessed
- Standardized assessment tool (Katz ADL, Lawton IADL, Barthel Index, etc.)
- Three or more of the following discussed: cognitive, ambulation, sensory (hearing/vision), other functional independence

### COA-Pain Assess
Documented pain assessment using:
- Standardized pain scale (0-10 NRS, FACES, FLACC for non-verbal, PEG, PAINAD)
- Notation that pain was assessed (presence/absence, location, severity)
- "No pain reported" with attestation typically counts

## Exclusions

- Hospice
- Death during MY
- Per current spec - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rules; COA has four sub-indicators each independently evaluated, all MY-bounded.

| Sub-indicator | Anchor | Window | Date type that counts | Date types that mislead |
|---|---|---|---|---|
| **COA-ACP** | None - MY-only (lifetime for AD on file - verify) | During MY | ACP discussion date, AD signing date, POLST signing date | Brochure-given date, "deferred" date |
| **COA-Med Review** | None - MY-only | During MY | Date of documented review by eligible provider (prescriber or clinical pharmacist), with current med list | Date med list was pulled into note without explicit review; date of review by ineligible role (MA, scribe) |
| **COA-Func Status** | None - MY-only | During MY | Date of functional status assessment (ADL/IADL or 3+ functional dimensions or standardized tool) | Date of isolated single-system assessment (e.g., post-op ROM) |
| **COA-Pain Assess** | None - MY-only | During MY | Date of pain assessment with severity/scale or "no pain reported" attestation | Date pain was mentioned in PMH without current assessment |

**Common date confusions for this measure**

- COA-Med Review and standalone MRP can share the same encounter date but require different elements (MRP is post-discharge reconciliation; COA-Med Review is annual ambulatory review)
- COA-ACP often satisfied by the same documentation as standalone ACP measure; the evidence date applies to both
- Functional status documented in nursing intake vs provider note - provider-attestation requirements vary
- Pharm.D. CMR done at retail pharmacy - the CMR date counts if documentation flows into plan EHR with provider role visible
- Pain assessment in vitals (5th vital sign) vs narrative pain discussion - vitals-based pain score date applies

## NLP signal phrases - COA-ACP

See [ACP](ACP.md) for full signal list. Key signals: "advance directive", "POLST/MOLST", "healthcare proxy", "code status discussed", "goals of care".

## NLP signal phrases - COA-Med Review

**Section hints:** Medications, Plan, problem list, dedicated "Annual Medication Review" or "Medication Reconciliation" section

**Positive signals**
- "medication review completed"
- "annual medication review"
- "medications reviewed by [Pharm.D. / MD / NP / PA]"
- "comprehensive medication review (CMR)" — also satisfies Stars MTM
- "current medications: [list]" with attestation
- "no changes to medication list this visit"
- "deprescribed [med] due to [reason]"

**Negative signals (insufficient)**
- "medications: see list" without review attestation
- "med rec" alone without explicit review by eligible provider
- Med list pulled into note without provider sign-off on review

**Assertion / negation pitfalls - COA-Med Review**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **Review by MA / front-desk staff** (not eligible provider) - eligible roles: prescriber or clinical pharmacist
- **Medication list printed for patient** without review documentation - distribution, not review
- **"Medications: see list"** without review attestation - listing, not review
- **"Med rec"** alone without explicit review by eligible provider - lexical ambiguity
- **Med list pulled into note** without provider sign-off on review - template artifact
- **"Will review meds at next visit"** - future intent
- **"Patient declined to review meds"** - refusal; does NOT close measure
- **"Hx of polypharmacy"** in PMH - historical reference, not current review
- **"Reviewed PRN meds only"** - partial; spec requires comprehensive review

## NLP signal phrases - COA-Func Status

**Section hints:** HPI, ROS, Social Hx, Assessment, dedicated "Functional Status" or "Geriatric Assessment" section

**Positive signals**
- "ADLs intact" / "ADLs assessed: independent in bathing, dressing, toileting, transferring, continence, feeding"
- "IADLs assessed" / "manages own medications, finances, transportation, meals"
- "Katz ADL score: ___"
- "Lawton IADL score: ___"
- "Barthel Index: ___"
- "patient ambulates independently with cane"
- "cognitive screen: SLUMS ___, MoCA ___, Mini-Cog ___"
- "hearing: WNL / impaired - uses hearing aids"
- "vision: corrected with glasses"
- "lives independently / with assistance / in ALF / SNF"

**Negative / insufficient signals**
- "no functional limitations" alone (lacks specificity per some specs)
- "geriatric review of systems" without functional content

**Assertion / negation pitfalls - COA-Func Status**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **Functional status discussed for an isolated complaint** (e.g., post-op ROM) - not a comprehensive assessment
- **"No functional limitations"** alone - lacks specificity per some specs (verify)
- **"Geriatric review of systems"** without functional content - generic
- **"Independent"** alone without ADL/IADL detail - hedged
- **"FH of dementia"** - experiencer = family
- **"Hx of stroke with residual weakness"** in PMH - historical context; need current functional assessment
- **"Patient declined functional assessment"** - refusal; does NOT close measure
- **"Will assess function at next visit"** - future intent
- **"Cognitive screen pending"** - future
- **"Lives with family"** alone - living arrangement noted; not a functional assessment

## NLP signal phrases - COA-Pain Assess

**Section hints:** Vitals (pain as 5th vital sign), HPI, ROS, Assessment, Plan

**Positive signals**
- "pain scale 0/10" / "pain: 3/10 in low back"
- "no pain reported" / "denies pain"
- "PEG score: ___"
- "FACES pain scale: ___"
- "FLACC: ___" (non-verbal)
- "PAINAD: ___" (dementia)
- "chronic pain: stable on current regimen, severity 4/10"
- "pain assessment: location, severity, character, alleviating/aggravating factors"

**Negative / insufficient signals**
- "pain" mentioned in PMH without current assessment
- "on pain medications" without current pain assessment

**Assertion / negation pitfalls - COA-Pain Assess**

> Cross-cutting assertion guidance lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).

- **Pain referenced in a single-organ-system review** without dedicated assessment - not a pain assessment
- **"Pain assessment unable to complete"** without alternative method (e.g., non-verbal scale for dementia) - barrier without resolution
- **"Pain" mentioned in PMH** without current assessment - historical context
- **"On pain medications"** without current pain assessment - treatment listed, not assessment
- **"Patient declined pain assessment"** - refusal; does NOT close measure
- **"FH of chronic pain"** - experiencer = family
- **"Will assess pain at next visit"** - future intent
- **"Chronic pain stable"** without severity/scale - hedged; severity needed
- **"Pain: yes"** in checkbox without scale - thin; spec acceptance varies
- **"No complaints today"** alone - generic absence of complaints; pain-specific attestation is stronger evidence

## Common documentation gaps

- COA-Med Review: medication list updated but no explicit "reviewed by" attestation
- COA-Func Status: only a single functional element documented (need ADLs OR IADLs OR ≥3 functional dimensions)
- COA-Pain Assess: "pain" referenced but no severity/scale documented
- ACP and COA-ACP captured in one but not duplicated to the other measure
- Pharm.D. CMR done at retail pharmacy but documentation not flowing into plan EHR

## Notes

- **COA is SNP-focused historically** but newer Medicare quality programs may extend the population - verify current spec
- All 4 sub-indicators are reported as separate rates
- Comprehensive Medication Review (CMR) from MTM programs often satisfies COA-Med Review - data integration across PBM and EHR matters
- ECDS direction: structured assessments via FHIR `Observation` (functional status, pain scores), `Procedure` (med review), `Consent` (ACP)

## See also

- [`ACP.md`](ACP.md) — standalone ACP measure with same overlap
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
