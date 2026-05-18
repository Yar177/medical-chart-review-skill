# HCC model versions: V28, V24, and HHS-HCC

> **Why this file exists:** Almost every HCC NLP decision (which ICD codes count, which HCC they map to, what the RAF weight is, whether a condition still risk-adjusts) depends on which model version you are targeting. Building one extractor and assuming it works across all three models is a common and expensive mistake.

This file is the first stop. Read it before [`raf-calculation.md`](raf-calculation.md), [`terminology-mapping.md`](terminology-mapping.md), or any of the per-HCC cards.

---

## 1. The three models at a glance

| Dimension | CMS-HCC V28 | CMS-HCC V24 | HHS-HCC |
|---|---|---|---|
| **Used for** | Medicare Advantage | Medicare Advantage (legacy) | ACA marketplace individual / small group |
| **Payer** | CMS to MA plans | CMS to MA plans | HHS to ACA issuers (premium stabilization) |
| **HCC count** | ~115 | 86 | ~127 (variant counts by year) |
| **Disease grouping** | Reorganized into ~30 condition categories | Original grouping | Separate grouping, age / sex / metal-level stratified |
| **ICD-10 → HCC mapping** | New crosswalk; ~2,000 codes removed from risk-adjusting vs V24 | Original crosswalk | Independent crosswalk |
| **Annual reset** | Calendar year | Calendar year | Calendar year |
| **Coefficient regression base** | More recent claims years | Older claims years | ACA enrollee population |
| **Status as of MY 2026** | 100% blended weight for payment year 2026 | Closed out at end of PY 2026 | Active, updated annually |

## 2. CMS-HCC V28 vs V24 phase-in schedule

CMS phased V28 in over three payment years. Each MA risk score during the phase-in was a blend:

| Payment year | V24 share | V28 share |
|---|---|---|
| **2024** | 67% | 33% |
| **2025** | 33% | 67% |
| **2026** | 0% | 100% |

**NLP implication during phase-in:** Both crosswalks had to be applied to the same encounter and reconciled. Suspect lists, validate scorecards, and RAF estimates all needed dual outputs. Post-2026, V24 still matters for retrospective work (RADV audits, claims re-reviews, historical re-runs) but not for new payment.

## 3. What changed from V24 to V28

The major model-level changes:

- **~2,000 ICD-10 codes lost risk-adjustment status.** Big categories of removals included some vague diabetes complications, much of peripheral vascular disease, and some major depression codes.
- **Reorganized condition categories.** HCC numbers between V24 and V28 do not align. A condition that was HCC X in V24 may be HCC Y, split across two HCCs, or removed entirely in V28.
- **Recalibrated coefficients.** Even where an HCC exists in both, the RAF weight is different.
- **Some new HCCs added.** A few specific conditions split into more granular HCCs.

**NLP implication:** Code-only mapping is not sufficient. You need crosswalks per model version, and the per-HCC cards must specify the V28 HCC, the V24 equivalent (if any), and the HHS-HCC equivalent (if any).

## 4. HHS-HCC is a different model

HHS-HCC is for ACA marketplace plans (individual and small group). It is **not** a relabeling of CMS-HCC. Key differences:

- **Separate condition categories.** Some overlap in concept (CHF, diabetes, COPD) but the HCC numbers and definitions are independent.
- **Age / sex / metal-level stratification.** HHS-HCC uses separate models for adult / child / infant, and adjusts for metal tier and induced demand.
- **Premium stabilization, not capitation.** HHS uses HHS-HCC for risk-adjustment transfers between issuers within a state, not for paying plans directly per member.
- **Annual model updates by HHS.** Coefficients and code lists are republished each benefit year.

**NLP implication:** If your team serves both Medicare Advantage and ACA marketplace lines of business, you need two parallel extractor configurations sharing extraction logic but using different crosswalks and reporting different HCC numbers.

## 5. Out-of-scope models (called out so you do not confuse them)

- **CDPS (Chronic Illness and Disability Payment System)** - used by many state Medicaid programs. Different model family. Not covered here.
- **ESRD model** - separate CMS-HCC variant for ESRD beneficiaries. Mentioned here for awareness; check CMS publications if you have an ESRD-heavy book.
- **PACE risk-adjustment** - separate frailty-weighted variant.
- **Rx-HCC** - Part D prescription-drug risk adjustment; uses pharmacy fills, distinct model.

If your team needs any of these, the patterns in this skill transfer but the model details do not. Source from the relevant CMS publication.

## 6. Where to source authoritative model files

- **CMS-HCC V28 and V24:** CMS Risk Adjustment page. Look for the annual "HCC Software" or "Model Software" ZIP files. They include the SAS code, ICD-10 → HCC mapping, coefficients, and hierarchies for the relevant payment year.
- **HHS-HCC:** CMS Center for Consumer Information and Insurance Oversight (CCIIO) publishes the HHS Notice of Benefit and Payment Parameters annually, plus the HHS-HCC model SAS package.
- **Annual updates:** Both CMS-HCC and HHS-HCC are republished every year with the ICD-10-CM update (typically October 1 release for the following payment year).
- **Do not rely on third-party reposts.** They drift quickly. Source from CMS / HHS directly and version-pin your extractor.

## 7. Version-pinning your extractor

Required metadata on every HCC prediction:

- HCC model version: `V28` / `V24` / `HHS-HCC-{benefit_year}`
- Crosswalk vintage: year of the ICD-10 → HCC file used
- ICD-10-CM code-set vintage: FY of the code set (October-to-September)
- Coefficient vintage: payment year the coefficients are calibrated for
- For phase-in payment years, the blended weight used

Without this metadata, your output is not auditable and you cannot reproduce RAF estimates after the fact.

## See also

- [`raf-calculation.md`](raf-calculation.md) - how the model outputs combine into a RAF score
- [`hierarchies.md`](hierarchies.md) - hierarchy rules per model version
- [`terminology-mapping.md`](terminology-mapping.md) - ICD-10 → HCC mapping and gotchas
- [`compliance-and-enforcement.md`](compliance-and-enforcement.md) - why version drift causes RADV exposure
