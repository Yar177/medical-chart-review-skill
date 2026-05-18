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

**False positives to filter**
- "PHQ form given to patient" without completed score
- Reference to PHQ in a templated note pulled from prior visit (verify date)
- "PHQ" mentioned in differential / education without actual screen

**Safety-critical signals (escalate regardless of measure)**
- "suicidal ideation" / "SI"
- "thoughts of self-harm"
- "plan to hurt self"
- PHQ-9 item 9 score > 0
- C-SSRS positive

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
