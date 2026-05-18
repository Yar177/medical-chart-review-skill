# HEDIS measure deep-dive cards

Per-measure quick-reference cards for HEDIS measures most commonly worked during chart review and NLP extraction. Use these as **reviewer/abstractor guidance and NLP extraction targets** - not as a replacement for the official NCQA HEDIS Technical Specifications.

## Disclaimer

- HEDIS® is a registered trademark of NCQA. These cards summarize publicly known measure intent and common documentation patterns. They do NOT reproduce NCQA value sets, code lists, or proprietary spec language.
- Measure definitions, age ranges, codes, and exclusion lists **change with every measurement year (MY)**.
- Before using for production HEDIS reporting, validate against the current **NCQA HEDIS Technical Specifications, Volume 2** for the relevant MY.
- Many measures have a parallel ECDS-reported version (suffix `-E`). The reporting path determines what evidence counts.

## Card structure

Each card has:

1. **Header** — full name, reporting path, population focus, related measures
2. **Denominator** — eligible population (age, continuous enrollment, qualifying events)
3. **Numerator** — what closes the gap, compliant evidence types
4. **Exclusions** — standard (hospice, advanced illness/frailty for 66+) plus measure-specific
5. **Date of service rule** — measure-specific anchor, window, date types that count vs. mislead, "most recent" disambiguation, common date confusions. Cross-cutting framework in [`../nlp/date-of-service.md`](../nlp/date-of-service.md).
6. **NLP signal phrases** — section hints + positive signals + negative/exclusion signals
7. **Assertion / negation pitfalls** — measure-specific anti-patterns (ConText-style). Cross-cutting framework in [`../nlp/negation-and-assertion.md`](../nlp/negation-and-assertion.md).
8. **Common documentation gaps** — why the measure often fails
9. **Notes** — MY-specific changes, ECDS direction, related measures

## Measures included

### Diabetes care
- [BPD](BPD.md) — Blood Pressure Control for Patients with Diabetes
- [EED](EED.md) — Eye Exam for Patients with Diabetes
- [GSD](GSD.md) — Glycemic Status Assessment for Patients with Diabetes (replaced HBD MY 2024)
- [KED](KED.md) — Kidney Health Evaluation for Patients with Diabetes
- [SUPD](SUPD.md) — Statin Use in Persons with Diabetes

### Cardiovascular
- [CBP](CBP.md) — Controlling High Blood Pressure
- [SPC](SPC.md) — Statin Therapy for Patients with Cardiovascular Disease

### Cancer screening
- [BCS-E](BCS-E.md) — Breast Cancer Screening
- [CCS-E](CCS-E.md) — Cervical Cancer Screening
- [COL-E](COL-E.md) — Colorectal Cancer Screening
- [DBM](DBM.md) — Documented Assessment After Mammogram (program-specific - see card)

### Behavioral health
- [FUH](FUH.md) — Follow-Up After Hospitalization for Mental Illness
- [PHQ](PHQ.md) — PHQ-2 / PHQ-9 instruments (depression screening)

### Transitions & medications
- [MRP](MRP.md) — Medication Reconciliation Post-Discharge
- [TRC](TRC.md) — Transitions of Care (4 sub-indicators)

### Pediatric & perinatal
- [PPC](PPC.md) — Prenatal and Postpartum Care (2 sub-indicators)
- [W30](W30.md) — Well-Child Visits in the First 30 Months of Life (2 sub-indicators)
- [WCV](WCV.md) — Child and Adolescent Well-Care Visits (ages 3-21)
- [WCC](WCC.md) — Weight Assessment and Counseling, Nutrition and Physical Activity for Children/Adolescents (3 sub-indicators)

### Older adult
- [ACP](ACP.md) — Advance Care Planning
- [AIS-E](AIS-E.md) — Adult Immunization Status (multiple sub-indicators)
- [COA](COA.md) — Care for Older Adults (4 sub-indicators: ACP, Med Review, Functional Status, Pain Assessment)
- [FRM](FRM.md) — Fall Risk Management (HOS-based, with chart-review angle)
- [OSW](OSW.md) — Osteoporosis Screening in Older Women

## Conventions

- **MY** = Measurement Year
- **CE** = Continuous Enrollment
- **ECDS** = Electronic Clinical Data Systems (FHIR-based reporting path NCQA is migrating measures toward)
- **`-E` suffix** = ECDS-reported variant (e.g., CCS-E, BCS-E, AIS-E, COL-E)
- **Section hints** use SOAP conventions (CC, HPI, ROS, PE, Vitals, Results, Assessment, Plan)
- **Advanced illness / frailty** is an aged-66+ exclusion concept defined by NCQA value sets - included as a generic mention only

## NLP signal phrase format

Plain-language phrases, not regex. They map well to:
- Keyword/lexicon matching with stemming and abbreviation expansion
- Embedding similarity / semantic search
- LLM prompts ("look for any of the following concepts")

False positives are called out per measure - filter those before scoring.

## See also

- [`../nlp/`](../nlp/) — cross-cutting NLP guidance for data-science teams building per-measure extractors (date of service, negation/assertion, extraction patterns, evaluation)
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) — provenance rules for chart-abstracted evidence
- [`../quality-measures.md`](../quality-measures.md) — broader quality framework overview
- [`../../templates/hedis-abstraction.md`](../../templates/hedis-abstraction.md) — abstraction worksheet
