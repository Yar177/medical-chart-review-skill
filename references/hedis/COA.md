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

**False positives to filter**
- Review by MA / front-desk staff (not eligible provider)
- Medication list printed for patient without review documentation

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

**False positives to filter**
- Functional status discussed for an isolated complaint (e.g., post-op ROM) - not a comprehensive assessment

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

**False positives to filter**
- Pain referenced in a single-organ-system review without dedicated assessment
- "pain assessment unable to complete" without alternative method (e.g., non-verbal scale for dementia)

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
