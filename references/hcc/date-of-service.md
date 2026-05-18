# Date of service for HCC NLP extraction

> **Why this file exists:** HCC date-of-service rules are stricter than HEDIS in some ways (calendar-year reset, face-to-face requirement, provider type whitelist) and looser in others (no measure-specific anchor windows). NLP teams that copy HEDIS DoS logic into an HCC pipeline get it wrong in subtle, audit-expensive ways.

The cross-cutting HEDIS DoS framework lives in [`../nlp/date-of-service.md`](../nlp/date-of-service.md). This file is HCC-specific. Read it before writing date logic for any HCC extractor.

---

## 1. The HCC date-of-service contract

For an HCC to count for a calendar year, the supporting evidence must come from:

1. A **face-to-face encounter** with the member
2. On a **date within that calendar year**
3. Documented and signed by an **acceptable provider type**
4. In an **acceptable encounter setting**
5. With the **diagnosis MEAT-supported** in the note for that encounter

All five must be true for the same diagnosis-encounter pair. Missing any one invalidates the HCC for that DOS. A different valid encounter in the same year can save the HCC; if no valid encounter exists in the year, the HCC does not contribute to RAF.

## 2. Calendar-year reset

CMS-HCC and HHS-HCC both reset January 1. The implications for NLP:

- A diagnosis documented December 28, 2025 supports RAF for **service year 2025** (payment year 2026 for CMS-HCC).
- The same diagnosis must be re-documented somewhere in 2026 to support RAF for service year 2026 (payment year 2027).
- Status conditions (amputation, ostomy, transplant) also reset and require annual recapture.
- "Carry-forward" of last year's HCCs is never valid for the current year.

**Pipeline implications:**

- Tag every extracted HCC with the service year. Do not let prior-year evidence leak forward.
- A suspect pipeline that flags "this member had HCC X last year but not yet this year" is genuinely valuable. The recapture rate on chronic HCCs is the most important operational metric for most MA plans.
- A validate pipeline must verify the evidence date is within the target calendar year.

## 3. Acceptable encounter settings

Generally acceptable (verify against current CMS guidance):

- Office / outpatient visits
- Inpatient admissions and discharge summaries
- Skilled nursing facility visits
- Home health visits with face-to-face provider component
- Telehealth (with restrictions; see section 5)
- Federally qualified health centers, rural health clinics
- Hospital outpatient department visits

Generally NOT acceptable on their own:

- Lab-only encounters (no provider face-to-face)
- Imaging-only encounters (radiology read without provider visit)
- Pharmacy fills
- DME orders
- Pre-admission paperwork
- Nurse-only telephone encounters
- Patient portal messages
- E-visits below the face-to-face threshold

**NLP implication:** Encounter type metadata is required input. Pipelines that extract from notes without knowing the encounter type cannot validate eligibility.

## 4. Acceptable provider types

The provider must be a credentialed, signing provider in an acceptable category. Typical whitelist (verify currency):

- Physicians (MD, DO)
- Nurse practitioners (NP)
- Physician assistants (PA)
- Clinical nurse specialists
- Certified nurse midwives (some settings)

Generally NOT acceptable as sole documenter:

- Medical students (notes must be attended)
- Resident notes alone (attending must attest)
- Scribes alone (provider must sign)
- Therapists, social workers, dietitians (their notes do not establish HCC on their own; useful as supporting evidence)
- RNs, LPNs (vital signs and triage do not establish HCC)
- Chiropractors (specialty-dependent)

**NLP implication:**

- Extract the signing provider and credential from the note header / footer.
- Reject extractions where the only signer is not on the whitelist.
- For resident + attending workflows, require the attending attestation block to be present and signed.

## 5. Telehealth eligibility (post-COVID landscape)

During the COVID PHE, CMS broadly allowed telehealth for risk adjustment, including audio-only. Post-PHE, the eligibility has narrowed and continues to evolve:

- **Video + audio synchronous telehealth:** generally acceptable for risk adjustment
- **Audio-only:** acceptance has narrowed; varies by service type and year
- **Asynchronous / store-and-forward:** generally not acceptable
- **E-visits / virtual check-ins:** generally not acceptable on their own

**NLP implication:**

- Distinguish telehealth from in-person via encounter metadata or explicit note language ("seen via video," "telephone visit," "telehealth via [platform]").
- Distinguish video from audio-only when possible ("video visit," "phone only," "could not connect video").
- For audio-only encounters, downgrade confidence pending the current-year CMS rule for that service.
- Do not apply a single static rule across multiple service years; pin to the rule in force for that service year.

## 6. Annual wellness visit (AWV) and the recapture trap

The AWV is the most common venue for HCC recapture. It is also a high-risk venue for over-coding because:

- AWVs cover a broad checklist; clinicians may carry the prior problem list into the assessment without independent MEAT.
- Some templates auto-populate "review of chronic conditions" without per-condition assessment text.
- Auditors specifically scrutinize AWV HCCs.

**Pipeline implications:**

- Treat AWV-sourced HCCs with extra MEAT-stringency in validate pipelines.
- Flag AWV documentation that uses templated language without per-condition reasoning.
- Surface "recapture-via-AWV" candidates separately from "newly-identified" candidates so reviewers can apply appropriate scrutiny.

## 7. Inpatient vs outpatient probable / likely / suspected

ICD-10-CM guidelines treat uncertain diagnoses differently by setting:

- **Outpatient:** Do NOT code probable, suspected, likely, rule-out, working-diagnosis, or differential-only conditions. Only confirmed diagnoses.
- **Inpatient:** Uncertain diagnoses present AT DISCHARGE may be coded as if confirmed (per UHDDS).

**NLP implication:**

- Encounter setting must be a first-class input.
- Outpatient extractors must detect and exclude hedged diagnoses: "probable," "likely," "suspected," "consistent with," "cannot rule out," "vs," "?diagnosis."
- Inpatient extractors must respect that the relevant statement is the discharge diagnosis, not interim impressions.
- A patient seen by inpatient consult during an admission is inpatient for this rule.

See [`negation-and-assertion.md`](negation-and-assertion.md) for the full hedging-language framework.

## 8. Date types in HCC charts

| Date type | Use for HCC? | Notes |
|---|---|---|
| Encounter / visit date | **Yes - primary** | The date the face-to-face occurred |
| Note signing date | Sometimes | Use if encounter date is missing; verify it matches a real visit |
| Discharge date | Yes for inpatient | The DOS for inpatient HCC is the discharge date for most purposes |
| Admission date | Sometimes | Used for some inpatient analytics; HCC typically anchors on discharge |
| Procedure date | Yes if face-to-face | Procedure-only encounters need provider visit component |
| Lab specimen date | No, on its own | Lab alone is not a face-to-face |
| Imaging exam date | No, on its own | Imaging alone is not a face-to-face |
| Order date | No | Ordering is not evidence of MEAT |
| Document scan date | No | Outside records: use the original document date |

## 9. Copy-forward and the DoS-attribution problem

Copy-forward (cloned text) is the same problem as in HEDIS but with higher stakes:

- A copy-forward A&P block dated October 1 that originally came from a January 15 note does NOT establish October 1 MEAT.
- Even within the same calendar year, the HCC is supported by the **original** encounter, not the encounter that copied the text.
- Across calendar years, copy-forward from prior year does NOT establish current-year MEAT.

**Detection signals** (same as the HEDIS framework, repeated for completeness):

- Identical multi-sentence blocks across notes
- Date-stamped phrases inside text that do not match the current encounter date
- Section headers referencing a prior date
- Imported outside-record markers

**Pipeline policy:** When copy-forward is detected for an A&P block, prefer the **original** encounter as the source of MEAT. If the original encounter cannot be located, downgrade confidence and route to human review.

See [`../nlp/extraction-patterns.md`](../nlp/extraction-patterns.md) for copy-forward detection patterns shared with the HEDIS pipeline.

## 10. The "any qualifying DOS in the year" property

Unlike most HEDIS measures, HCC has no measure-specific anchor window. The rule is simply: any qualifying encounter in the calendar year. This means:

- One good encounter in any month captures the HCC for the year.
- Multiple encounters that each separately validate the HCC are redundant for RAF but useful for audit defense.
- Most plans aim for at least one strong encounter per chronic HCC per year as audit insurance.

**Pipeline implication:** Year-level roll-up should track all qualifying encounters per HCC, not just the first one found. Surface "weakly supported" HCCs (only one borderline encounter) for re-documentation or query.

## 11. Common DoS failure modes

- **Cross-year leakage.** Pipeline finds last year's December encounter in this year's chart pull and credits this year. Calendar-year tagging at extraction prevents this.
- **Copy-forward attribution.** Validating today's encounter using text that originated months ago. Detect and downgrade.
- **Lab-only DOS.** Treating a standalone lab visit as a qualifying encounter. Encounter type must be checked.
- **Wrong signer.** Validating using a resident note with no attending attestation. Whitelist enforcement at the pipeline boundary.
- **Telehealth assumption.** Applying COVID-era telehealth permissiveness to current-year encounters. Pin telehealth rules to the service year.
- **AWV templating.** Validating templated AWV problem-list reviews without per-condition MEAT. Stricter MEAT enforcement for AWV-sourced HCCs.

## See also

- [`meat-criteria.md`](meat-criteria.md) - MEAT is the second leg of the DoS contract
- [`negation-and-assertion.md`](negation-and-assertion.md) - inpatient vs outpatient hedging rules
- [`extraction-patterns.md`](extraction-patterns.md) - copy-forward, section detection
- [`../nlp/date-of-service.md`](../nlp/date-of-service.md) - shared DoS framework with HEDIS
- [`compliance-and-enforcement.md`](compliance-and-enforcement.md) - RADV implications of DoS errors
