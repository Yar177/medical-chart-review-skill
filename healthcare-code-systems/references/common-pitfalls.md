# Common pitfalls

> **Why this file exists:** Cross-cutting failure modes that recur across code systems. Use this as a pre-flight checklist for any new pipeline, query, or analytic deliverable.

## 1. Storage / serialization

### Leading-zero loss

- **NDC** stored as integer drops leading zero in the labeler segment → irreversible. Always store as fixed-width string.
- **NPI** stored as integer drops leading zero (rare today but possible). Store as 10-character string.
- **HCPCS / CPT** stored as integer for the few all-numeric Cat I codes mangles the modifier set and breaks join consistency. Store as string.
- **ICD-10-CM / PCS** without decimal preserved: `E1110` vs `E11.10` - both are seen; pick one convention.
- **CCN** stored as integer drops the 2-digit state prefix's leading zero for state codes < 10.

### Precision loss

- **SNOMED SCTIDs** exceed 32-bit int range and can exceed 2^53 (float64 precision). Store as `bigint` or string.
- **RxCUI** is currently safe in int32 but trending up; storing as `bigint` is future-proof.

### Mixed types in one column

- A `code` column that holds ICD-10-CM, CPT, HCPCS, and HCC values without a `code_system` discriminator is unrecoverable.

## 2. ICD-10-CM specific

- **Decimal handling**: codebase mixes `E11.10` and `E1110` styles; joins miss silently.
- **Excludes1 vs Excludes2** conflated: see [`icd10-cm.md`](icd10-cm.md) §3.
- **Z-code traps**: `Z85.*` (history of) treated as active disease; `Z11.*` / `Z12.*` (screening) treated as actual disease; `Z79.*` (long-term drug use) treated as the indication for the drug. See [`icd10-cm.md`](icd10-cm.md) §8.
- **NOS / NEC** distinction lost (NOS = "not otherwise specified", clinical detail missing; NEC = "not elsewhere classifiable", system limitation).
- **"With" convention** misread (combination codes that encode multiple conditions assumed to be separate codes).
- **Laterality codes** treated as separate diseases rather than as the same disease lateralized.
- **Annual October 1 update** missed → claims from the new fiscal year fail to validate against last year's table.

## 3. CPT / HCPCS specific

- **Modifiers stripped** during normalization (`-25`, `-59`, `-X{E,S,P,U}` are clinically and financially significant).
- **Modifier -25 / -59 abuse detection** flagged as random noise when it is the known indicator pattern.
- **Telehealth modifiers** (`-95`, `-GT`, `-GQ`) and **POS 02 vs POS 10** confused; both are in current use post-COVID with different meanings.
- **Cat II vs Cat I CPT** treated as billable encounters (Cat II are performance-measurement supplemental tracking codes).
- **CPT licensing** ignored in open-source distribution. See [`sources-and-licensing.md`](sources-and-licensing.md).
- **HCPCS quarterly updates** missed → new J-code drug pricing fails to match.
- **Unclassified J-codes** (`J3490`, `J3590`) treated as a specific drug instead of an unspecified placeholder requiring NDC for identification.

## 4. Drug / pharmacy specific

- **NDC 10-vs-11-digit** join mismatch.
- **11-digit NDC stored without original FDA format** preserved; reversal ambiguous.
- **Repackager NDCs** treated as different drugs from original-labeler NDCs.
- **Inactive NDCs** dropped from current-state tables but still valid for historical dates of service.
- **RxCUI TTY mixing**: querying "metformin" with IN-level RxCUI gives correct cohort; mixing IN, SCD, SBD in joins inflates / deflates counts.
- **J-code-only or NDC-only** drug counting → misses the medical-benefit or pharmacy-benefit half.
- **Days-supply aggregation** without overlap handling → MPR / PDC > 1.0 from overlapping fills.

## 5. SNOMED specific

- **SCTID stored as int / float** → precision loss.
- **Hierarchy ignored** → SNOMED used as flat lookup, throwing away its main value.
- **"Situation with explicit context"** conflated with disease concept (history-of and family-history are distinct concepts in SNOMED).
- **Concept inactivation** ignored → legacy data referencing now-inactive concepts breaks downstream.
- **International vs US Edition** confused; ECL expressions evaluated against International miss US-extension content.
- **ECL version not pinned** → SNOMED release silently changes value-set membership.

## 6. LOINC / UCUM specific

- **Vendor lab codes** present in HL7 v2 OBR-4 but LOINC slot empty / wrong → vendor-specific crosswalk required, often missing.
- **Unit normalization** deferred forever (mg/dL and mmol/L glucose values stored in same column).
- **UCUM case-folding** (`mg` vs `Mg`).
- **Curly-brace annotations** in UCUM (`{beats}/min` vs `/min`) treated as distinct units.
- **LOINC method specificity** ignored - method-specific and unspecified LOINCs treated as different observations when they are clinically equivalent (or vice versa).

## 7. Provider specific

- **NPI Luhn validation skipped** → typos propagate.
- **Type 1 vs Type 2 NPIs** mixed in entity-level analyses.
- **NPPES taxonomy** treated as current clinical specialty (often years stale).
- **Deactivated NPIs** treated as active.
- **Provider directory** trusted without ghost-network awareness.
- **TIN as NPI** in payment / contract-counting analyses.
- **CCN as NPI** in facility analyses (both appear on inpatient claims; they identify the same facility differently).

## 8. Crosswalks specific

- **GEMs treated as 1:1** (the single most common crosswalk error).
- **Stale crosswalk** vintage for current DOS.
- **No fallback** for unmapped source codes → silent row drops.
- **Round-trip asymmetry** ignored (NDC → RxNorm → NDC expands to a set; SNOMED → ICD → SNOMED loses granularity).
- **Wrong HCC model year** (V24 vs V28 for the wrong payment year).
- **Custom crosswalks** without provenance, version, or QA process.

## 9. Value set specific

- **Expansion-only** without intensional definition → silent staleness.
- **Intensional-only** without pinned expansion → non-deterministic across runs.
- **OID drift** → renaming breaks downstream references.
- **Cross-MY drift** in HEDIS (using last year's value sets against this year's measurement period).
- **Wrong code-system version** (SNOMED ECL evaluated against the wrong release).
- **Inline code lists** in pipeline code → no external spec, no review trail.

## 10. Versioning specific

- **"Current" code-system table** joined to historical claims; misses DOS-valid codes that are now retired.
- **Single-vintage warehouse** → no way to reproduce prior analyses.
- **Mid-cycle vintage updates** that silently change reporting numbers.
- **No drift monitoring** → team learns about new codes when downstream users complain.
- **HCC V24 / V28 phase-in** ignored.
- **Vintage tag missing** from published outputs; numbers cannot be reproduced or defended.

## 11. Licensing specific

- **CPT tables embedded** in public GitHub repos.
- **NCQA HEDIS value sets distributed** to entities without their own NCQA license.
- **APR-DRG logic in open-source tooling** without 3M agreement.
- **SNOMED assumed universally free** (US license; non-US licensing varies).
- **UMLS account requirement** skipped for RxNorm / SNOMED / VSAC.

## 12. Race / ethnicity specific

- **Race and ethnicity conflated** (OMB 1997 treats them as separate dimensions).
- **Single-race assumption** when multi-race selection is standard.
- **MENA category** missing pre-2024 OMB SPD 15 revision; longitudinal data spans the change.
- **"Unknown" / "Declined" / "Other"** treated as missing instead of valid administrative categories.
- **Source disagreement** (registration vs claims vs EHR self-report) not distinguished.

## 13. CVX / immunization specific

- **Active-only filtering** drops legacy doses.
- **CVX + MVX combination** ignored; same CVX from different manufacturers identifies different products.

## 14. Cross-cutting

- **No `code_system` discriminator** on join keys.
- **No `effective_from` / `effective_to`** on code reference tables.
- **No `version` / `vintage`** column on grouper outputs or value-set expansions.
- **No provenance** on custom crosswalks or internal taxonomies.
- **No drift monitoring** scheduled against release calendars.
- **No documented refresh schedule** for code-system updates.
- **Numbers published without vintage tags** → cannot be reproduced or defended.
- **One-size-fits-all grouper** for all analyses → wrong tool for many questions.
- **PHI (NPI, SSN as TIN) handled without HIPAA safeguards**. See `hipaa-compliance` skill.

## 15. Pre-flight checklist

Before shipping any new pipeline or analytic deliverable:

- [ ] Every code column has an associated `code_system` discriminator.
- [ ] Every code reference table is **versioned** with effective dates.
- [ ] Crosswalks have a **cardinality** documented and a **fallback strategy** for unmapped codes.
- [ ] Value sets have an **OID + version + expansion date** documented.
- [ ] Groupers have a **grouper version + underlying code-system version** documented.
- [ ] Outputs carry a **vintage tag** (which code-system + grouper + value-set versions were used).
- [ ] Licensed content (CPT, HEDIS, APR-DRG, CDT, commercial drug DBs) is not embedded inappropriately.
- [ ] PHI handling complies with HIPAA (see `hipaa-compliance`).
- [ ] Drift monitoring is in place for the relevant release cadences.
- [ ] Refresh schedule is documented and tied to release dates.
- [ ] Unit-normalization (UCUM) is performed at the data boundary.
- [ ] NDC normalization (11-digit fixed-width string) is performed at the data boundary.
- [ ] NPI Luhn-validation is performed at the data boundary.
- [ ] Sample-output / smoke-test reconciliation is run after each refresh.
