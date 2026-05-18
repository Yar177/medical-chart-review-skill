# FRM — Fall Risk Management

**Reporting path:** Primarily **HOS (Medicare Health Outcomes Survey)**; some chart-review angles
**Population focus:** Medicare Advantage members 65+ who report a fall in the past 12 months

> **Important distinction:** FRM has historically been **survey-based** (HOS), meaning the data comes from member self-report on the Medicare HOS - not from chart abstraction. The chart-review use case here is **documenting fall discussions and interventions so they show up in the medical record** even though the measure denominator itself comes from the survey. NCQA has also published chart-reviewable adjacent measures. Verify your program's exact measure source for the current MY.

## Denominator (HOS-based)

- Medicare Advantage members 65+
- Reported on the HOS that they had a fall, problems with balance, or problems with walking in the past 12 months

## Numerator (HOS-based)

- Member reports that a doctor or other health provider:
  - **Talked about falls or problems with balance/walking** in the past 12 months, AND
  - **Suggested ways to prevent falls or treat balance/walking problems**

Both parts typically required for full compliance.

## Chart-review angle

While the score itself comes from HOS, plans typically want providers to **document fall risk screening, discussion, and interventions** so:
- HOS responses are corroborated
- Adjacent NCQA / quality-program fall measures (where chart-reviewable) close
- Care plans reflect evidence-based fall prevention

Common chart-reviewable evidence:
- Fall risk screening (STEADI algorithm, Stay Independent questionnaire, Timed Up and Go - TUG)
- Documented fall in past 12 months (self-reported or witnessed)
- Discussion of fall prevention strategies
- Referral to PT for balance / gait training
- Home safety evaluation referral
- Medication review for fall-risk-increasing drugs (FRIDs)
- Vitamin D supplementation discussion
- Vision and hearing screening referrals

## Exclusions

- Hospice
- Bed-bound / non-ambulatory members (varies by spec)
- Per current spec - verify

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). FRM is HOS-driven (member self-report on the Medicare Health Outcomes Survey); the chart-review angle here is about documenting falls and interventions so they align with member self-report.

| Field | Value |
|---|---|
| **Anchor event** | Member-reported fall, balance problem, or walking problem in past 12 months (HOS-derived) |
| **Compliance window** | Discussion + intervention in past 12 months (HOS recall window) |
| **Date types that COUNT (chart-side alignment)** | Date of fall-risk screening, fall-discussion documentation, intervention referral, medication review for FRIDs |
| **Date types that do NOT count (chart-side)** | Boilerplate "fall precautions" without specifics, "PT recommended" without fall-specific rationale, intervention dated > 12 months before HOS administration |
| **"Most recent" disambiguation** | Most recent qualifying documentation aligns with member's recall window |
| **Look-back / look-forward** | 12 months look-back from HOS administration date |

**Common date confusions for this measure**

- HOS administration date sets the recall window; chart documentation older than 12 months prior to HOS does NOT corroborate
- Fall event date vs intervention date - both matter; the event must be within 12-month recall, and the intervention should follow
- Multiple falls - each fall date is potentially relevant; document each
- PT referral date vs PT visit date - the referral date can be the intervention date; the visit date is separate evidence
- FRID medication review date - the review event date is what aligns with HOS, not the date the medication was originally prescribed

## NLP signal phrases

**Section hints:** HPI (fall history), ROS (musculoskeletal, neurologic), Social Hx, Assessment, Plan, dedicated "Fall Risk" or "Geriatric Assessment" section

**Positive signals - fall history identification (for denominator alignment)**
- "fall in the past year"
- "history of falls"
- "fell last [month/week]"
- "near-fall" / "almost fell"
- "balance problems" / "unsteady gait"
- "difficulty walking" / "ambulatory dysfunction"
- "afraid of falling" / "fear of falling"

**Positive signals - discussion and intervention (for numerator alignment)**
- "fall risk assessed" / "fall risk: high/moderate/low"
- "STEADI screen completed"
- "Timed Up and Go: ___ seconds"
- "TUG test"
- "Stay Independent questionnaire"
- "Tinetti gait and balance"
- "discussed fall prevention"
- "fall prevention counseling"
- "home safety evaluation referral"
- "PT referral for balance training"
- "vestibular therapy"
- "vitamin D started for fall prevention"
- "reviewed medications for fall risk" / "deprescribed [med] to reduce fall risk"
- "discontinued [benzodiazepine / opioid / anticholinergic / antihypertensive] given fall risk"

**FRIDs (fall-risk-increasing drugs) commonly reviewed**
- Benzodiazepines, Z-drugs (zolpidem, eszopiclone)
- Opioids
- Antipsychotics
- Tricyclic antidepressants
- Anticholinergics
- Sedating antihistamines
- Antihypertensives with orthostatic risk (alpha blockers)
- Sulfonylureas, insulin (hypoglycemia → falls)

**Negative / exclusion signals**
- "bed-bound"
- "non-ambulatory"
- "hospice"
- "uses wheelchair full-time" - verify spec impact

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"Fall precautions"** boilerplate without specific discussion - generic template
- **"Fall risk: low"** without screening tool result behind it - unsupported attestation
- **Fall in HPI not followed by intervention or screening** - event documented; no compliance evidence
- **"PT recommended"** without fall-specific rationale - unrelated PT context
- **"Hx of falls"** in PMH without timeframe - historical reference; cannot place in 12-month recall window
- **"FH of falls in elderly parents"** - experiencer = family
- **"Patient denies falls"** - NEGATIVE; does NOT establish FRM denominator (denominator comes from HOS, not chart)
- **"Near-fall last year"** - near-falls may or may not align with HOS "fall" definition; verify
- **"Patient declined fall-prevention discussion"** - refusal; documents but does not close measure
- **"Will discuss fall prevention at next visit"** - future intent
- **"Education materials given on fall prevention"** alone - distribution without discussion documentation
- **"FRIDs reviewed: no changes"** - acceptable review evidence; do NOT mistake "no changes" for absence of review
- **"Vitamin D recommended"** in generic AG without fall-prevention rationale - generic recommendation
- **"Bed-bound"** - exclusion signal; do NOT flip

## Common documentation gaps

- Fall in HPI captured as incident but not linked to fall-risk assessment
- Screening tool (e.g., TUG) done but result not pulled into structured field
- Fall prevention discussion verbal only, not documented
- Medication review done but FRIDs not explicitly flagged in the documentation
- Vitamin D / home safety referrals discussed but not noted in Plan

## Notes

- **HOS is the primary measurement instrument** - chart documentation alone does not satisfy the measure score; it supports the experience the member reports
- STEADI (CDC's Stopping Elderly Accidents, Deaths & Injuries algorithm) is the recommended workflow framework
- Related measure: COA in older adult plans has functional status and pain components that intersect with fall risk
- ECDS direction: structured screening results (TUG, STEADI) via FHIR `Observation` / `Procedure`

## See also

- [`COA.md`](COA.md)
- [`ACP.md`](ACP.md)
- CDC STEADI toolkit
- NCQA HEDIS Technical Specifications and Medicare HOS technical specifications
