# Annotation guidelines for HCC NLP

> **Why this file exists:** HCC gold standards drive every metric and every model. Without explicit annotation guidelines, two careful annotators will disagree on 30%+ of edge cases (history-of nuance, MEAT linkage, hierarchy application). This file documents the schema, conventions, and adjudication process.

The HEDIS annotation guidelines live in the sibling `hedis-nlp` skill's `references/nlp/annotation-guidelines.md` (in this same repo). HCC-specific schema and rules are below.

---

## 1. Annotation goals

Produce, per encounter, a labeled record that lets evaluation distinguish:

- Did the model find the right diagnosis spans?
- Did it assign the right assertion class?
- Did it link MEAT evidence correctly?
- Did it map to the right HCC under the right model version?
- Did it apply hierarchies correctly?

The annotation schema must support all five.

## 2. Annotator profiles

| Profile | Role | Required background |
|---|---|---|
| **Clinical annotator** | Reads chart, identifies diagnoses and MEAT | RN, MD, or experienced clinical NLP annotator |
| **Coder annotator** | Maps to ICD-10 and HCC, applies hierarchies | CPC, CRC, CCS-P, or experienced HCC coder |
| **Adjudicator** | Resolves disagreements | Senior coder (CRC preferred) with audit experience |

Pure-clinical or pure-coder annotation is rarely sufficient. The clinical lens catches MEAT and assertion nuance; the coder lens catches HCC mapping and hierarchy nuance. Most mature teams pair them.

## 3. Annotation unit

Per encounter, produce:

```yaml
encounter:
  encounter_id: <opaque id>
  encounter_date: YYYY-MM-DD
  encounter_type: office | inpatient | telehealth_video | telehealth_audio | awv | sn  f | home_health
  setting: outpatient | inpatient
  signing_provider:
    type: physician | np | pa | resident_with_attending | scribe | other
    on_whitelist: true | false
diagnosis_annotations:
  - span:
      text: "diabetes type 2 with peripheral neuropathy"
      char_offsets: [4521, 4565]
      section: assessment | hpi | problem_list | pmh | psh | fh | ros | pe | vitals | plan | discharge_dx | other
    icd10:
      preferred: E11.40
      alternates: []
    hcc:
      v28: 18
      v24: 18
      hhs_hcc: null
    assertion:
      negation: present | absent
      temporality: current | historical | future
      history_modifier: none | hx_of | pmh | resolved | remission | nedrecur | post_curative
      status_modifier: none | s_p_amputation | s_p_transplant | s_p_ostomy | other
      experiencer: patient | family | other
      hypothetical: real | hypothetical | conditional
      hedging: confirmed | probable | suspected | ruleout | other
    meat:
      monitor: [list of supporting span ids or "none"]
      evaluate: [...]
      assess: [...]
      treat: [...]
      linked_to_this_diagnosis: true | false
      linkage_confidence: high | medium | low
    copy_forward:
      detected: true | false
      original_date: YYYY-MM-DD | null
    codable_for_this_dos: true | false
    annotator_notes: "freeform"
```

Store the schema versioned. Schema changes always force a re-evaluation against the new schema.

## 4. Span conventions

- **Annotate the minimal sufficient span.** Include the disease name + qualifying modifiers (with neuropathy, chronic, acute). Do not include leading articles or trailing punctuation.
- **One diagnosis per span.** "Diabetes and hypertension" is two spans even if they share words.
- **Combination diagnoses get one span if expressed as a single concept.** "Diabetes with neuropathy" is one span when it appears as a single phrase mapped to a single ICD code (E11.40).
- **Multi-mention same diagnosis** in one encounter: annotate every mention; mark MEAT-linkage and codability on the primary (most informative) mention; secondary mentions are reference-only.

## 5. Assertion annotation rules

Apply the dimensions independently. A single span can be Present + Historical (history-of breast cancer) + Real + Patient. The history-of dimension does NOT collapse into negation.

Tricky cases and the rule:

| Phrase | Annotation |
|---|---|
| "history of CHF" with no current activity | Historical; not codable as active CHF; consider Z-code |
| "history of CHF, currently decompensated" | Current; codable as active CHF |
| "s/p MI 2015" with no current ischemia | Historical (old MI, Z86.7x); not codable as acute MI |
| "PMH: diabetes" with active management in this encounter | Current; codable |
| "PMH: diabetes" with no active management in this encounter | Current chronic but FAILS MEAT for this DOS - mark as not codable |
| "Mother with breast cancer" | Experiencer = family; not codable |
| "Patient denies family history of cancer" | Negation of family history; no codable concept |
| "Probable PE" in outpatient setting | Hedging = probable; setting = outpatient; not codable |
| "Probable PE" in inpatient discharge summary final diagnoses | Hedging = probable; setting = inpatient discharge; codable |
| "Diabetes vs prediabetes" | Hedging; not codable as either |
| "If A1c > 9, will start insulin" | Hypothetical; not codable |
| "Resolved pneumonia" | Historical; not codable as active |
| "Active CKD stage 3b" | Current; codable; specificity intact |
| "CKD" with no stage | Current; codable but specificity gap; HCC mapping may downgrade |

## 6. MEAT linkage rules

A diagnosis is MEAT-linked when at least one explicit evidence span can be tied to it in the same encounter. Linkage strength:

- **High**: same A&P numbered problem block; explicit reference ("the diabetes is controlled"); diagnosis-specific test or medication explicitly mentioned with the diagnosis
- **Medium**: same section; medication or test in plan that maps unambiguously to the diagnosis (e.g., metformin alone is medium linkage to DM)
- **Low**: different sections; weak inferential link; medications or tests with multiple possible indications

Annotation rule: link MEAT evidence to a diagnosis only when linkage is high or medium. Low-linkage evidence is captured but not used as codability support.

## 7. Hierarchy annotation convention

Pick one convention and document it:

**Convention A (extract-level):** Annotate every supported diagnosis with its HCC. Do not pre-apply hierarchies. The evaluator applies hierarchies to both predictions and gold before computing metrics.

**Convention B (post-hierarchy):** Annotate only the surviving HCCs after hierarchy. Predictions must also be hierarchy-collapsed before comparison.

Convention A is generally more flexible (lets you compute both naive and hierarchy-aware metrics, and supports specificity-error analysis). It also matches the recommended pipeline architecture.

Convention B is simpler for downstream consumers.

Pick one. Document it in every gold-standard release.

## 8. Status code annotation

Status codes (Z89, Z93, Z94, Z99 subset) are their own diagnoses. Annotate them like any other diagnosis with:

- The Z-code as the preferred ICD-10
- The corresponding HCC
- "Status modifier" set appropriately
- MEAT for status codes is the explicit statement of the status (which is itself the evidence; for permanent status conditions, presence in PSH or as a current status statement counts as MEAT)

Common confusion: amputation status (Z89.x) does require annual recapture even though the amputation itself is permanent. The recapture evidence is documenting the absence of the limb at this DOS (PE, ROS, or assessment mention).

## 9. Copy-forward annotation

When the same A&P block appears verbatim in multiple encounters:

- Annotate every encounter's text
- Mark `copy_forward.detected = true` on the duplicate encounters
- Record `original_date` if identifiable
- Codability for the duplicate encounters depends on whether the duplicate encounter has independent MEAT (most do not)

This is one of the most labor-intensive parts of HCC annotation. Tooling that highlights duplicates across encounters saves substantial time.

## 10. Inter-annotator agreement (IAA)

Target Cohen's kappa per dimension:

- Diagnosis span boundaries: 0.75+
- ICD-10 code (preferred): 0.80+
- HCC mapping (given correct ICD-10): 0.85+ (this is largely deterministic from crosswalk; lower numbers signal crosswalk-version mismatch)
- Assertion: temporality 0.75+, history_modifier 0.70+, experiencer 0.85+, hedging 0.70+, hypothetical 0.85+
- MEAT linkage: 0.60+ (this one is genuinely hard; below 0.5 signals a guideline gap)
- Codable_for_this_dos overall: 0.70+

If you cannot hit these, the guidelines need clarification, not the annotators.

## 11. Adjudication workflow

- Disagreements surface in a tracking system after each annotation batch.
- Adjudicator resolves with a brief written rationale.
- Rationale feeds back into a "guidelines clarifications" document, versioned.
- When a rationale establishes a new convention, re-annotate prior affected encounters and update the IAA baseline.

Do not let adjudication be a black box. The rationales are training material for future annotators and the audit trail for why the gold standard says what it says.

## 12. Synthetic and adversarial examples

Supplement real-data annotation with synthetic examples for:

- Rare HCCs (long tail with insufficient real positives)
- Adversarial constructions (history-of within an active-management section, hierarchy collisions, family-history confusion)
- Known failure modes from the failure-mode catalog (see [`evaluation-and-validation.md`](evaluation-and-validation.md))

Mark synthetic examples explicitly and report metrics separately. Synthetic-only positive rates can mask real-data weakness if blended without separation.

## 13. Common annotation pitfalls

- **Annotating problem list as codable on its own.** Problem-list presence is not MEAT.
- **Annotating family history as patient diagnosis.** Section context is overlooked.
- **Skipping the historical dimension.** Annotators check "negation" and call it done; "history of" goes unrecorded.
- **Collapsing combination diagnoses.** "Diabetes with neuropathy" annotated as two diagnoses (E11.9 + G62.9) instead of one (E11.40). The latter is the combination code that maps to a different HCC.
- **Not capturing MEAT linkage strength.** Without strength, evaluation cannot distinguish strict-linkage failures from loose-linkage failures.
- **Not annotating copy-forward.** Drives wrong-DOS attribution errors that look like extraction errors.
- **Inconsistent hierarchy convention.** Some encounters annotated post-hierarchy, others pre-hierarchy. Metric computation breaks.

## 14. Tooling notes

- **Brat / Inception / Prodigy**: general-purpose annotation tools; need custom schema configuration for the assertion taxonomy.
- **Custom internal tooling**: most mature plans build their own. The encoder for the assertion dimensions and the MEAT linkage UI are the parts off-the-shelf tools handle worst.
- **Highlight duplicates**: copy-forward detection should be visible to annotators in real time, not discovered after annotation.
- **Allow code suggestions from prior claims**: lets annotators verify rather than recall HCC numbers; speeds annotation and improves accuracy.

## See also

- [`evaluation-and-validation.md`](evaluation-and-validation.md) - what the annotations drive
- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion taxonomy reference
- [`meat-criteria.md`](meat-criteria.md) - MEAT detection rules
- [`hierarchies.md`](hierarchies.md) - hierarchy convention
- Sibling `hedis-nlp` skill, `references/nlp/annotation-guidelines.md` - shared HEDIS annotation guidance
