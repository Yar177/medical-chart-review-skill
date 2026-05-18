# PHQ — PHQ-2 and PHQ-9 Depression Instruments

**Note:** PHQ-2 and PHQ-9 are **clinical instruments**, not standalone HEDIS measures. They appear as numerator evidence in HEDIS depression-related measures (e.g., DSF-E Depression Screening and Follow-Up for Adolescents and Adults; DMS-E Depression Monitoring; ADD-E for adolescents). This card describes how to recognize and extract them so they correctly feed those measures.

## PHQ-2 (brief screen)

- **2 items** covering little interest/pleasure and feeling down/depressed
- Score range: **0-6**
- Positive screen threshold: **≥ 3**
- Typical use: initial screen; positive PHQ-2 triggers PHQ-9

## PHQ-9 (full screen / severity)

- **9 items** plus a functional impairment question
- Score range: **0-27**
- Severity bands (clinical convention - verify NCQA spec for measure-specific cut points):
  - 0-4: minimal
  - 5-9: mild
  - 10-14: moderate
  - 15-19: moderately severe
  - 20-27: severe
- Item 9 (suicidal ideation) is a **safety-critical** signal - elevate immediately even if total score is low

## Where PHQ feeds HEDIS

- **DSF-E (Depression Screening and Follow-Up for Adolescents and Adults):** PHQ-2 or PHQ-9 documented; if positive, follow-up within a defined window
- **DMS-E (Depression Monitoring):** repeat PHQ-9 within a defined window after positive screen or diagnosis
- **ADD-E / pediatric measures:** PHQ-A or similar adolescent tools

Confirm measure-specific instrument acceptance against current NCQA spec - DSF-E typically accepts PHQ-2, PHQ-9, PHQ-A, EPDS (perinatal), and others.

## Date of service rule

> Cross-cutting DoS guidance lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This section captures the instrument-specific rule. PHQ is an instrument feeding multiple parent measures; the parent measure dictates the compliance window.

| Field | Value |
|---|---|
| **Anchor event** | For follow-up measures (DMS-E): positive screen or depression diagnosis date |
| **Compliance window** | Parent-measure-specific (DSF-E annual; DMS-E follow-up window after positive screen) |
| **Date types that COUNT** | Instrument administration date (date the patient completed the questionnaire) |
| **Date types that do NOT count** | Note signing date when the PHQ score is copy-forward, date the form was "given to patient" without completion, prior-visit PHQ referenced without re-administration |
| **"Most recent" disambiguation** | Latest qualifying administration in the window |
| **Look-back / look-forward** | Driven by parent measure |

**Common date confusions for this measure**

- PHQ score in flowsheet vs PHQ score in narrative - both should share the administration date; if dates differ, the flowsheet entry is usually the source-of-truth
- Copy-forward of prior PHQ score with a new note date - the score belongs to the original administration date, not the current note
- Pediatric vs adult instrument administered on the same visit - track separately; each has its own date and parent measure

## NLP signal phrases

**Section hints:** ROS (psych), Assessment, Plan, dedicated "Screening" or "Depression" section, structured questionnaire/flowsheet

**Positive signals (screen administered)**
- "PHQ-2" with score (e.g., "PHQ-2: 1")
- "PHQ-9" with score (e.g., "PHQ-9: 7")
- "depression screen completed"
- "PHQ score" / "depression score"
- Individual item phrasings:
  - "little interest or pleasure in doing things"
  - "feeling down, depressed, or hopeless"
  - "trouble falling or staying asleep"
  - "feeling tired or having little energy"
  - "poor appetite or overeating"
  - "feeling bad about yourself"
  - "trouble concentrating"
  - "moving or speaking slowly / restlessness"
  - "thoughts of being better off dead or hurting yourself" (item 9 - safety-critical)

**Positive result signals**
- "PHQ-2 positive" / "PHQ-2 ≥ 3"
- "PHQ-9 moderate" / "PHQ-9 elevated"
- "screen positive for depression"

**Negative signals**
- "PHQ-2 negative" / "depression screen negative"
- "PHQ-9 score 0" / "no depressive symptoms"

**Follow-up signals (for DSF-E / DMS-E numerator)**
- "referred to behavioral health"
- "started on SSRI" / specific antidepressant names
- "psychotherapy referral"
- "follow-up in 4 weeks for depression"
- "safety plan reviewed"

**Assertion / negation pitfalls**

> Cross-cutting assertion guidance (ConText framework, library recommendations, shared HEDIS anti-patterns) lives in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md). This block captures measure-specific pitfalls.

- **"PHQ form given to patient"** without completed score - distribution, not administration
- **"PHQ-2 reviewed in chart"** - review of prior score is NOT a new administration
- **"PHQ in differential" / "considered PHQ"** - clinical reasoning, not screening
- **Copy-forward PHQ score** appearing across multiple notes - the score belongs to the original administration date
- **"Depression screen negative"** - NEGATIVE result IS positive evidence that the screen was administered
- **"Patient refused PHQ"** - refusal; typically does NOT count as screening
- **"FH of depression"** - experiencer = family
- **"Hx of MDD, currently stable"** - historical context; not a screen administration
- **"PHQ-9 of 12"** as free text only - extractable, but admin / claims-only pipelines may miss when not in structured field
- **"PHQ-A" used for adult patient** (or vice versa) - instrument-age mismatch may not satisfy parent measure
- **Safety-critical item 9 > 0** - escalate regardless of total score and regardless of measure scoring
- **"EPDS positive"** in perinatal context - perinatal-specific instrument; verify spec acceptance for the parent measure

## Common documentation gaps

- PHQ done by MA / RN, score in flowsheet but never re-stated in provider note (provider attestation needed in some specs)
- PHQ-2 positive but no PHQ-9 documented same visit - follow-up may still satisfy
- Score documented as text ("PHQ-9 of 12") not in structured field - admin claims-only pipelines miss it
- Pediatric vs adult instrument confusion - verify spec accepts the version used

## Notes

- Most HEDIS depression measures evaluate the **screen + follow-up pair**, not just one
- Refusal to complete PHQ is typically NOT compliant - separate refusal field
- ECDS direction: structured questionnaire response via FHIR `QuestionnaireResponse` is ideal
- Annual screening cadence depends on the parent measure - verify

## See also

- DSF-E / DMS-E / ADD-E technical specs (NCQA Volume 2)
- [`hedis-supplemental-data.md`](../hedis-supplemental-data.md)
- [`../red-flags.md`](../red-flags.md) for safety escalation paths
