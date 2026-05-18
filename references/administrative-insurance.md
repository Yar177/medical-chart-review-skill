# Administrative, Insurance & Prior Authorization

Chart-side review only. This file tells the agent **what to look for in the record** — not how to call payer APIs or verify eligibility against external systems. Anything beyond the chart is out of scope; defer to the user's billing/UR team.

For payer-specific rules (UHC, Aetna, BCBS plans, state Medicaid, MA plans), see `references/local-policy.md` if present.

## 1. Face sheet / registration anatomy

The face sheet (a.k.a. registration page, demographics page, patient summary) is the front door for any coding, UR, or denials review. Read it **before** the clinical notes.

| Field | Why it matters | Common gotcha |
|---|---|---|
| Patient name + DOB + sex | Identity, age-based measure eligibility | Preferred name vs legal name mismatch |
| MRN / enterprise MRN | Links encounters across facilities | Facility MRN ≠ enterprise MRN |
| Address + ZIP | Geographic eligibility, network adequacy | Out-of-state address with in-state plan |
| Guarantor | Who's financially responsible | Guarantor ≠ subscriber ≠ patient |
| Emergency contact / next of kin | Disposition, consent | Sometimes confused with healthcare proxy |
| Insurance (primary / secondary / tertiary) | Eligibility, COB, auth requirements | Stale plan info; effective dates not on face sheet |
| Employer | Sometimes drives plan + group # | Self-pay / uninsured status |
| Preferred language + interpreter need | Documentation requirement, quality measure | Missing → potential CMS / Joint Commission finding |
| Advance directive on file | Critical for inpatient/ED | "On file" without scanned copy attached |

### EHR-specific location
- **Epic**: Storyboard (left rail) + Registration activity; Coverages activity for insurance detail
- **Cerner (Oracle Health)**: PM Office / Patient Information band; Coverages tab
- **Athenahealth**: Quickview > Patient tab; Insurances tab on patient banner
- **Meditech**: Patient Header / Registration screen

## 2. Insurance verification checklist

For each active coverage, confirm the following is **documented in the chart** for the date of service being reviewed:

- [ ] Payer name (e.g., "BCBS of [state]", "Aetna Better Health", "Humana Medicare Advantage")
- [ ] Plan name / product (e.g., HMO, PPO, EPO, POS, MA, MA-PD, D-SNP, Medicaid managed care)
- [ ] Member ID / policy number
- [ ] Group number (employer-sponsored plans)
- [ ] Subscriber name
- [ ] Subscriber DOB
- [ ] Patient's relationship to subscriber (self / spouse / child / domestic partner / other)
- [ ] Effective date
- [ ] Termination date (or "active")
- [ ] Plan type indicator: commercial / Medicare / Medicare Advantage / Medicaid / Medicaid managed / Tricare / VA / workers' comp / auto / self-pay
- [ ] Copy of insurance card on file (front + back), date scanned

**Finding patterns:**
- Subscriber DOB on the card doesn't match the chart → demographic data integrity issue
- Patient listed as "self" but DOB ≠ subscriber DOB → wrong relationship code
- Card scanned >12 months ago → re-verification likely needed (some plans require annual)

## 3. Eligibility on the date of service (DOS)

The single highest-yield administrative check. Documentation must show coverage was **active on the exact DOS**.

| Situation | What to look for | Risk |
|---|---|---|
| Service rendered before effective date | Coverage start in the future of DOS | Full denial; patient liability |
| Service rendered after termination date | Term date prior to DOS | Full denial |
| Retroactive termination | Term date entered after DOS but backdated | Take-back / clawback |
| Plan change mid-encounter (inpatient) | Two payers across stay | Split-billing required |
| Newborn coverage gap | Baby not yet added to mother's plan | Common Medicaid issue |
| Medicaid redetermination lapse | Coverage gap during renewal | Retro-eligibility may restore |

**Reviewer note:** the chart usually shows the *last verified* eligibility status, not real-time. Flag any encounter where eligibility was verified more than 30 days before DOS as "re-verification recommended."

## 4. Coordination of Benefits (COB)

When a patient has more than one plan, determine which is primary.

**Standard rules (chart-side cues):**
- **Employer plan vs spouse's employer plan** → patient's own plan is usually primary for the patient
- **Children with two parents' plans** → "birthday rule": parent with earlier birthday in the calendar year is primary (not older parent)
- **Medicare + employer plan**:
  - Employer ≥20 employees → group plan primary, Medicare secondary (MSP)
  - Employer <20 employees → Medicare primary
- **Medicare + Medicaid** → Medicare primary, Medicaid payer of last resort
- **Workers' comp / auto / liability** → primary for the related condition; health plan secondary
- **Active duty Tricare** → primary over most commercial; rules differ for retirees
- **VA** → not health insurance for COB purposes; separate benefit

**What to verify in the chart:**
- COB questionnaire completed and dated
- Primary vs secondary explicitly labeled in the Coverages section
- Medicare Secondary Payer (MSP) questionnaire completed for every Medicare encounter (CMS requirement)

## 5. Prior authorization review

Prior auth (PA) failures are one of the top denial categories. The chart must contain auth evidence **before** the service was rendered (with limited retro-auth exceptions).

### What typically requires PA
- Most non-emergent inpatient admissions
- Outpatient surgery in many plans
- Advanced imaging (MRI, CT, PET, nuclear)
- High-cost or specialty drugs (biologics, infusions, oncology, GLP-1s in some plans)
- DME above a threshold
- Home health, SNF, acute rehab, LTACH admissions
- Out-of-network referrals
- Genetic testing
- Behavioral health intensive services (IOP, PHP, residential)

### Where it lives in the chart
- Authorizations / Referrals tab (Epic: Referrals activity; Cerner: Authorization band)
- Scanned approval letter in Media tab
- Free-text mention in scheduling/intake note ("Auth #ABC123 obtained 2026-04-10, valid through 2026-07-10, 6 visits approved")
- UR notes for inpatient stays (concurrent authorization)

### Fields to capture for each auth
- Auth / reference number
- Issuing payer
- Service authorized (CPT/HCPCS or service description)
- Approved date range
- Approved units / visits / days / dose
- Provider / facility authorized
- Notes (e.g., "step therapy required first," "in-network only")

### Common PA findings
| Finding | Detail |
|---|---|
| No auth on file for service that requires it | Likely denial |
| Auth for different CPT than billed | Mismatched service |
| Auth expired before DOS | Out of date range |
| Auth units exceeded | Visit 7 billed on a 6-visit approval |
| Auth for wrong site (inpatient vs outpatient) | Place-of-service mismatch |
| Auth for wrong provider | Network mismatch |
| Peer-to-peer (P2P) attempted | Document outcome and date |
| Retro-auth window | Some payers allow 24–72h post-service auth for emergent care |
| Continued-stay auth missing | Inpatient day 4+ with no concurrent review |

## 6. Referral requirements

Distinct from PA. A referral is permission from a gatekeeper (usually PCP) to see a specialist.

| Plan type | Referral usually required? |
|---|---|
| HMO | Yes — PCP referral on file for specialist |
| POS | Often yes for in-network referral pricing |
| PPO | No |
| EPO | Usually no, but out-of-network not covered |
| MA HMO | Yes |
| MA PPO | No |
| Medicaid managed care | Often yes; varies by state |
| Traditional Medicare | No |

### Reviewer checklist
- [ ] Referral on file for specialist encounter where required
- [ ] Referral date precedes the specialist visit
- [ ] Referral covers the specialty/CPT being billed
- [ ] Referral within its valid date range (often 90 days / 3 visits)
- [ ] Self-referral exceptions (OB/GYN, behavioral health, vision) noted appropriately

## 7. Payer policy cross-reference

The chart-review job is to confirm documentation supports medical necessity under the relevant policy. The agent does **not** memorize every payer's policy — it confirms the basics and flags items needing payer-specific lookup.

- **NCD / LCD** (Medicare): national and local coverage determinations define when a service is covered. Flag any service that has a known NCD/LCD (e.g., NIPT, PET imaging, bariatric surgery) for documentation review.
- **Medical necessity language**: documentation should explicitly tie the service to a covered indication (diagnosis + clinical rationale), not just list a code.
- **Step therapy**: many drug benefits require failure of preferred agents first — verify the trial-and-failure documentation.
- **Site-of-service**: payer may cover the same CPT outpatient but not inpatient (or vice versa). Confirm POS code matches setting.
- **Frequency limits**: HEDIS-style "once per year" or "once per lifetime" limits (e.g., colonoscopy screening intervals).
- **Bundling / NCCI edits**: Medicare NCCI edits bundle certain CPT pairs; modifier `-59` / `-25` use must be documented.
- **Payer-specific rules** → defer to `references/local-policy.md`.

## 8. Denial categories tied to administrative gaps

Group findings using these standard categories — they map cleanly to remit codes (CARC/RARC):

| Category | Typical cause | Where to look in chart |
|---|---|---|
| Eligibility | Service outside coverage dates | Face sheet, Coverages |
| No auth / referral | Required PA or referral missing | Authorizations tab |
| Auth mismatch | Auth for different CPT/date/provider | Authorization detail |
| Non-covered service | Service excluded by plan | Policy + diagnosis |
| Medical necessity | Documentation doesn't support indication | Assessment / Plan |
| COB | Wrong payer billed first | Coverages, COB questionnaire |
| Timely filing | Claim submitted past window | Billing system (often not in clinical chart) |
| Duplicate | Same service billed twice | Claim history |
| Modifier | Missing/incorrect modifier | Coding |
| Place of service | POS code mismatch with setting | Encounter header |

## 9. Reviewer red flags (always surface)

- Service rendered before coverage start or after termination
- Procedure documented with no prior auth on file when payer requires it
- Auth on file is for a different CPT, date, provider, or site than billed
- Specialist encounter on an HMO with no referral on file
- Medicare encounter with no MSP questionnaire documented
- Two active primary coverages with no COB determination
- Subscriber demographics on insurance card don't match face sheet
- Drug billed without step-therapy documentation when required
- Inpatient day ≥4 with no continued-stay authorization
- POS code on claim doesn't match documented setting (e.g., billed inpatient, documented as observation)

## 10. What this skill will NOT do

- Call payer eligibility APIs or 270/271 transactions
- Quote specific payer policies the agent hasn't been given
- Predict whether a denial will be overturned
- Generate appeals letters that assert medical facts not in the chart
- Replace a certified biller, UR nurse, or physician advisor

If the review requires any of the above, surface a deferral note and stop.
