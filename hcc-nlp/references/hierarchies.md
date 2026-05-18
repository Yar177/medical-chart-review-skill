# HCC hierarchies and deduplication

> **Why this file exists:** HCC hierarchies are not optional. Pipelines that emit both HCC 18 (Diabetes with Chronic Complications) and HCC 19 (Diabetes without Complications) for the same member inflate RAF, fail RADV, and create FCA exposure. Hierarchy enforcement is a required pipeline stage, not a nice-to-have.

The CMS-HCC and HHS-HCC models both define hierarchies within condition categories. The more severe HCC in a hierarchy "trumps" the less severe one for the same member-year: only the most severe HCC contributes to RAF.

---

## 1. The hierarchy rule

If a member has both HCC X and HCC Y in the same calendar year, and HCC X is hierarchically superior to HCC Y in the model, then HCC Y does not contribute to RAF.

The member can still legitimately be coded with both diagnoses (the underlying ICD codes are valid). But for risk adjustment, only the superior HCC counts.

**Why CMS does this:** It avoids double-counting severity within a condition family. Diabetes with chronic complications already captures the risk of diabetes; adding uncomplicated diabetes on top would inflate.

## 2. Where hierarchies live

CMS publishes the hierarchy file with the HCC software package each year. It is a simple parent-child table: "HCC X trumps HCC Y." A few hierarchies are chains of 3 or more.

You apply the hierarchy file as a post-extraction filter:

1. Collect the set of HCCs the member has for the calendar year.
2. For each pair, check the hierarchy table.
3. Drop any HCC that is trumped by another HCC the member has.
4. Sum coefficients only over the remaining HCCs.

This is the right place in the pipeline. Do not try to encode hierarchy decisions into the diagnosis extractor.

## 3. Examples (V28; verify against current file)

These illustrate the pattern. The specific HCC numbers shift between V24 and V28 - always check the current model's hierarchy file.

### Diabetes family

```
HCC 17 (Diabetes with Acute Complications)
  trumps
HCC 18 (Diabetes with Chronic Complications)
  trumps
HCC 19 (Diabetes without Complications)
```

Member has all three? Only HCC 17 contributes.
Member has HCC 18 and HCC 19? Only HCC 18 contributes.

### CHF / cardiac family

The cardiac hierarchies in V28 are more granular than V24. Some examples of trumping relationships (illustrative):

- Acute MI trumps old MI
- Specific cardiomyopathy HCCs trump less specific ones

### Cancer family

```
HCC for Metastatic Cancer
  trumps
HCC for Lung / Esophageal / etc.
  trumps
HCC for Other Cancers
```

A member with metastatic disease only gets the metastatic HCC, even if the primary site is also coded.

### CKD family

```
HCC for CKD Stage 5 / ESRD
  trumps
HCC for CKD Stage 4
  trumps
HCC for CKD Stage 3
```

(Exact HCC numbers vary by model version.)

## 4. Hierarchies are NOT mutual-exclusion at extraction time

Common NLP mistake: writing extraction rules that try to detect "is this the severe form?" and emit only one HCC.

The correct pattern:

1. **Extract every supported diagnosis** with its specificity intact. If the note documents "diabetes mellitus type 2" and also "diabetic neuropathy" elsewhere, extract both.
2. **Map each to its HCC** using the crosswalk.
3. **Apply the hierarchy filter** post-extraction.

Reasons:

- The underlying ICD codes are all valid. Suppressing them at extraction loses provenance for claims and audit.
- A single encounter can have one diagnosis; the hierarchy applies across the **member-year**, not the encounter. You need to keep both extractions visible until the year-level roll-up.
- Hierarchies change between model versions. Pushing them into extraction logic forces re-extraction every time CMS updates the model. Keep extraction model-agnostic; apply hierarchies as a model-version-specific post-step.

## 5. Cross-family interactions are not hierarchies

Do not confuse:

- **Hierarchy:** within-family trumping (CHF Stage 4 trumps CHF Stage 3).
- **Interaction:** cross-family combination that adds an additional coefficient (DM + CHF interaction adds a third positive coefficient).

Both are post-extraction steps. They are separate logic and applied independently. See [`raf-calculation.md`](raf-calculation.md).

## 6. HHS-HCC hierarchies

HHS-HCC has its own hierarchy table with its own parent-child relationships. Many concepts overlap with CMS-HCC (diabetes severity, CKD stages, cancer staging) but the specific HCC numbers and trumping pairs are different. If you run both CMS-HCC and HHS-HCC pipelines, you need both hierarchy files and apply each within its own scoring pipeline.

## 7. When the hierarchy file disagrees with the chart

Sometimes the chart will document both a severe and a less-severe form of the same condition for different encounters in the same year (for example, an acute exacerbation in March and a routine chronic visit in October). The hierarchy still applies at the year level: only the most severe HCC for that family contributes to RAF for the year.

**NLP implication:** The supporting documentation for the surviving HCC must still pass MEAT and the calendar-year reset rules. Hierarchy filtering does not validate evidence - it only deduplicates after each HCC has independently passed extraction and MEAT.

## 8. Hierarchy as an evaluation hazard

When measuring extractor precision and recall, hierarchies create a measurement pitfall:

- A model predicts HCC 18 and HCC 19. The gold standard has only HCC 18 (because HCC 18 trumps HCC 19, and the auditor pre-applied the hierarchy).
- A naive comparison reports HCC 19 as a false positive.
- A hierarchy-aware comparison applies the hierarchy to predictions first, then compares.

Always apply hierarchies to both predictions and gold standard before computing metrics. Otherwise your precision and recall numbers will be misleading. See [`evaluation-and-validation.md`](evaluation-and-validation.md).

## 9. Hierarchy enforcement checklist

A correct pipeline must:

- [ ] Use the hierarchy file from the **same model version vintage** as the coefficient file.
- [ ] Apply hierarchies at the **member-year roll-up**, not at the encounter level.
- [ ] Apply hierarchies **after** MEAT validation and calendar-year reset checks.
- [ ] Preserve the suppressed HCCs in audit logs (so a human can see "HCC 19 extracted but trumped by HCC 18").
- [ ] Apply hierarchies separately for each model (CMS-HCC V28, V24, HHS-HCC) if running multi-model.

## See also

- [`model-versions.md`](model-versions.md) - which hierarchy file to use
- [`raf-calculation.md`](raf-calculation.md) - hierarchies feed the coefficient sum
- [`extraction-patterns.md`](extraction-patterns.md) - keep extraction independent of hierarchy logic
- [`evaluation-and-validation.md`](evaluation-and-validation.md) - apply hierarchy before computing metrics
- [`cards/hcc-18-diabetes-with-complications.md`](cards/hcc-18-diabetes-with-complications.md) - worked example of within-family trumping
