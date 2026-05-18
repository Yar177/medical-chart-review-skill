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

**False positives to filter**
- "advance directive brochure given" with no documented discussion
- "no advance directive" without follow-up offered (counts vary by spec)
- "code status discussed but patient deferred" - usually does not satisfy

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
