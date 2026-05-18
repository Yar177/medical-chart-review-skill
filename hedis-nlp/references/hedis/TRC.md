# TRC — Transitions of Care

**Reporting path:** Hybrid historically; ECDS direction
**Population focus:** Adults 18+ with inpatient discharge during MY
**Sub-indicators (each evaluated independently):**
1. **Notification of Inpatient Admission** — notification to PCP within 2 days of admission
2. **Receipt of Discharge Information** — PCP receives discharge info within 2 days of discharge
3. **Patient Engagement After Inpatient Discharge** — outpatient visit / phone visit / telehealth with provider within 30 days
4. **Medication Reconciliation Post-Discharge** — med rec completed within 30 days (overlaps with [MRP](MRP.md))

User-named sub-indicators in this skill:
- **TRC-Patient** = Patient Engagement After Inpatient Discharge
- **TRC-Med** = Medication Reconciliation Post-Discharge

## Denominator

- Members 18+ as of end of MY
- Continuous enrollment from discharge through 30 days post-discharge (allowed gap per spec)
- Discharged alive from an acute or non-acute inpatient stay during MY (excluding certain stays - psych, hospice, etc. per spec)

## TRC-Patient (Patient Engagement) numerator

- Outpatient visit, telehealth visit, or e-visit with a PCP or ongoing-care provider within **30 days of discharge**
- Visit must occur on day 1-30 (day of discharge typically does NOT count)

## TRC-Med (Medication Reconciliation) numerator

- Medication reconciliation conducted by a prescribing practitioner, clinical pharmacist, or registered nurse within **30 days of discharge**
- Must be documented with explicit reconciliation language (not just "medications reviewed")

## TRC-Notification numerator

- Documented notification of the inpatient admission to the receiving primary practitioner on day of admission or following day

## TRC-Discharge Info numerator

Receipt of discharge information by PCP on day of discharge or following day, including at minimum:
- Discharge dx / problem list
- Discharge medications
- Pending tests / follow-up needs
- Treating provider info

## Exclusions

- Hospice
- Death during inpatient stay
- Transfers between inpatient settings (may be counted as single stay per spec)
- Inpatient psychiatric or chemical dependency stays handled differently

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the measure-specific rules; TRC has four sub-indicators each with its own DoS shape.

| Sub-indicator | Anchor | Window | Date type that counts | Date types that mislead |
|---|---|---|---|---|
| **TRC-Notification** | Inpatient admission | Notification on day of admission or following day | Date PCP / receiving practitioner was notified (HIE feed timestamp, fax-received date, EHR cross-system message date) | Date the hospital generated the message (if delayed); date discovered in inbox later |
| **TRC-Discharge Info** | Inpatient discharge | Receipt on day of discharge or following day | Date the discharge document was received by PCP system, with required components | Discharge summary signing date by hospital provider (vs receipt date); fax-cover-sheet date |
| **TRC-Patient** | Inpatient discharge | Outpatient visit within 30 days of discharge (day of discharge does NOT count) | Encounter date of the post-discharge visit | Scheduled date, no-show date, ED visit, phone-only contact (verify spec) |
| **TRC-Med** | Inpatient discharge | Med rec within 30 days of discharge (day of discharge does NOT count) | Date the med-rec documentation was entered by eligible provider | Day-0 hospital med rec, med-list refresh without explicit reconciliation, reconciliation by ineligible role |

**Common date confusions for this measure**

- Discharge date ambiguity on overnight discharges - use spec-defined discharge date
- HIE-feed timestamp vs receiving-system file-import timestamp - capture the earliest evidence the document was available to PCP
- Same-day discharge and outpatient visit - day-0 visit typically does NOT count for TRC-Patient or TRC-Med
- Calendar days, not business days - weekend gaps count against the windows
- TRC-Med vs MRP - same intent, same window; some programs report both, some only one

## NLP signal phrases - TRC-Patient

**Section hints:** Encounter type, Plan, scheduling section, follow-up appointments

**Positive signals**
- "post-hospital follow-up"
- "transition of care visit"
- "follow-up after hospitalization"
- "discharged on [date], seen in office on [date]" within 30-day window
- Telehealth: "video visit s/p discharge"

**Negative / exclusion signals**
- "hospice" / "comfort care"
- "expired during hospitalization"

**Assertion / negation pitfalls - TRC-Patient**

- Visit scheduled but not attended - intent, not completion
- Phone-only contact without provider documentation - verify spec; many sub-indicators reject phone-only
- ED visit post-discharge - ED does NOT count as TRC-Patient follow-up
- "Patient declined post-discharge visit" - refusal; does NOT close measure
- "Visit with PA / NP only" - acceptable when PCP / ongoing-care provider role; verify scope
- "Telehealth visit" coded as phone-only - spec acceptance varies
- Day-of-discharge office visit - day 0 typically does NOT count

## NLP signal phrases - TRC-Med

**Section hints:** Medications section, Plan, dedicated "Medication Reconciliation" tab, post-discharge visit note

**Positive signals**
- "medication reconciliation completed"
- "med rec done"
- "reconciled discharge medications with home medications"
- "discharge medications reviewed and updated"
- "no discrepancies identified between home and discharge meds"
- "discrepancies identified: ___, addressed by ___"

**Negative signals (insufficient)**
- "medications reviewed" alone - typically NOT explicit reconciliation
- "current meds listed" alone

**Assertion / negation pitfalls - TRC-Med**

> See also [`MRP.md`](MRP.md) - same intent, same window.

- "Medications reviewed" alone - boilerplate; not reconciliation
- "Current meds listed" alone - listing is not reconciliation
- "Med rec" in unrelated context (medication-assisted, medical record) - lexical collision
- Med list refresh at visit without reference to discharge meds - not reconciliation
- "Med rec by MA / scribe" - eligible roles only (prescriber, clinical pharmacist, RN)
- Day-0 med rec - does NOT count
- "Will reconcile at next visit" - future intent

## NLP signal phrases - TRC-Notification and TRC-Discharge Info

**Section hints:** PCP inbox messages, scanned outside hospital documents, EHR cross-system messaging, dedicated TOC fields

**Positive signals**
- "admission notification received from [hospital]"
- "discharge summary received [date]"
- "TOC document received via [HIE / fax / Direct]"
- "hospital course summary on file"
- Date-of-receipt logged in document management

**Assertion / negation pitfalls - TRC-Notification and TRC-Discharge Info**

- Discharge summary received outside the 2-day window - too late, does NOT count
- Discharge summary received but missing required components (dx list, discharge meds, pending tests, treating provider) - incomplete; does NOT satisfy
- "Admission notification expected" / "awaiting hospital report" - future intent
- Notification received via HIE feed but not surfaced to PCP inbox - capture the earliest receipt timestamp, not the inbox-acknowledgment date
- Fax cover sheet timestamp vs actual document receipt - use the document timestamp
- "Hospital report on file" without timestamp - cannot place within the 2-day window

## Common documentation gaps

- Med rec done verbally in visit but documented as "meds reviewed" rather than "reconciled"
- Discharge summary received but timestamp not captured
- Patient engagement visit was telehealth but coded as phone-only (acceptance varies)
- Notification of admission via HIE feed not surfaced in PCP workflow

## Notes

- **TRC-Med ↔ MRP overlap:** TRC's med rec sub-indicator and the standalone [MRP](MRP.md) measure share intent but live in different measure structures - verify which your program reports
- All 4 sub-indicators are reported as separate rates
- ECDS direction: structured encounter + medication statements + clinical document references via FHIR
- 30-day rule excludes the day of discharge - day 1 is the next calendar day

## See also

- [`MRP.md`](MRP.md)
- [`FUH.md`](FUH.md)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
