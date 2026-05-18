# ACP — Advance Care Planning

**Reporting path:** Admin / ECDS variants exist; verify current MY
**Population focus:** Older adults (typically 65+ or 66+ depending on program)
**Related measures:** Care for Older Adults (COA) historically included an ACP component

## Denominator

- Members in the qualifying age band (verify exact lower bound in current spec - commonly 65+ or 66+)
- Continuous enrollment through MY with no more than the allowed gap
- One or more qualifying outpatient / telehealth encounters during MY

## Numerator

Documentation of any one of the following during MY (some specs allow lifetime evidence):

- Advance care planning discussion documented in the medical record
- Advance directive on file (living will, healthcare proxy, durable POA for healthcare)
- POLST / MOLST / MOST / POST form
- Surrogate decision-maker / healthcare agent identified
- Code status discussion documented with clinical context

## Exclusions

- Hospice or palliative care during MY
- Death during MY (program-dependent)
- Advanced illness / frailty exclusion may apply

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rule.

| Field | Value |
|---|---|
| **Anchor event** | None - MY-only (some specs allow lifetime evidence for advance directive on file) |
| **Compliance window** | Documentation during MY (or lifetime for some evidence types - verify spec) |
| **Date types that COUNT** | Date of ACP discussion in provider note; date advance directive was placed on file; date POLST/MOLST was signed |
| **Date types that do NOT count** | Date brochure was given to patient without discussion, date advance directive was "requested but not received", date discussion was "deferred" |
| **"Most recent" disambiguation** | Most recent documentation in MY (or lifetime evidence on file as of end of MY) |
| **Look-back / look-forward** | MY-only for discussion; some specs accept lifetime advance directive on file |

**Common date confusions for this measure**

- Advance directive scanned years ago and "on file" - lifetime evidence acceptance varies by spec; verify whether the scanned-document date counts or whether a MY-attestation is required
- Code status documented in flowsheet at multiple visits - any qualifying entry in MY satisfies
- POLST signed in prior MY but reviewed in current MY - "reviewed" is not a new signing; the signed-date is the evidence date
- Discussion documented in nurse / social work note but not provider note - some specs require provider attestation; the note-author role matters more than the date

## NLP signal phrases

**Section hints:** Plan, Assessment, Social Hx, dedicated "Advance Directives" tab, problem list, scanned-document index

**Positive signals**
- "advance directive on file"
- "advance care planning" / "ACP discussion"
- "POLST" / "MOLST" / "MOST" / "POST"
- "living will"
- "healthcare proxy" / "healthcare agent" / "DPOA-HC" / "durable power of attorney for healthcare"
- "code status: full code / DNR / DNI / DNAR / DNR-CC"
- "goals of care discussion"
- "patient wishes regarding resuscitation"
- "surrogate decision maker" / "next of kin designated"

**Negative / exclusion signals**
- "hospice" / "comfort care only" / "GIP hospice"
- "palliative care consult"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Advance directive brochure given"** with no documented discussion - distribution, not discussion
- **"No advance directive"** without follow-up offered - documentation of absence; spec-dependent whether this counts
- **"Code status discussed but patient deferred"** - hedged; usually does NOT satisfy
- **"Will discuss ACP at next visit"** - future intent
- **"Patient declined ACP discussion"** - refusal; documentation of refusal may satisfy in some specs - verify
- **"FH of advance directives"** - experiencer = family, not patient
- **"Code status: full code"** alone in template - acceptable in many specs but verify; some require attached narrative discussion
- **"Advance directive on file"** in problem list without document date - cannot confirm currency
- **"POLST in chart"** without timestamp - cannot confirm date of signing
- **"Discussed code status with family"** - family discussion only; patient may not have been involved
- **"Reviewed advance directive"** - review of existing AD is not a new discussion; existing AD on file is the satisfying evidence
- **"Goals of care discussion ongoing"** - hedged; not finalized

## Common documentation gaps

- Code status in flowsheet but no narrative ACP note from provider
- Advance directive scanned but not surfaced on problem list or signed-note text
- Discussion captured only in nurse / social work note (provider attestation may be required)

## Notes

- Compliant evidence varies between Medicare Advantage Stars, commercial HEDIS, and state programs
- Many EHRs have structured ACP fields - confirm whether the abstraction pipeline reads structured + free-text or just one
- ECDS direction favors structured Advance Directive resources via FHIR (e.g., `Consent`, `DocumentReference`)

## See also

- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- NCQA HEDIS Technical Specifications, Volume 2
