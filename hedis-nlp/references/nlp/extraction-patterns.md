# Extraction patterns for HEDIS chart-review NLP

Practical patterns for extracting evidence from chart notes when building per-measure HEDIS models. Pairs with [`date-of-service.md`](date-of-service.md) (date selection) and [`negation-and-assertion.md`](negation-and-assertion.md) (qualifying the claim).

## Audience

NLP engineers, clinical informaticists, and analytics engineers who already have the per-measure intent from [`../hedis/`](../hedis/) and need to actually pull evidence out of free text reliably.

## Scope

Section detection, abbreviation handling, copy-forward, telehealth specifics, outside-record / scanned-PDF handling, provider attribution, doc-type classification, multi-doc linking, and structured-vs-narrative trade-offs.

Not in scope: model training code, value sets, FHIR transforms, PHI handling.

---

## 1. Document structure: section detection

EHR notes (Epic, Cerner, Athena, Meditech, Veradigm, NextGen) share section conventions but the **exact header strings vary by vendor, template, and clinic**. Robust extractors do header-aware section segmentation before downstream rules.

### Canonical clinical-note section taxonomy

| Canonical section | Header variants seen in the wild |
|---|---|
| Chief Complaint | "CC:", "Chief Complaint:", "Reason for Visit:", "Presenting Complaint:" |
| HPI | "HPI:", "History of Present Illness:", "Interval History:", "Subjective:" |
| Past Medical History | "PMH:", "Past Medical Hx:", "Medical History:", "Active Problems:" |
| Past Surgical History | "PSH:", "Surgical Hx:", "Procedures:" |
| Family History | "FH:", "Family Hx:", "Family History:" |
| Social History | "SH:", "Social Hx:", "Social History:", "Lifestyle:" |
| Medications | "Meds:", "Current Medications:", "Active Medications:", "Home Meds:", "Medication List:" |
| Allergies | "Allergies:", "Drug Allergies:", "NKDA" |
| Review of Systems | "ROS:", "Review of Systems:", "10-point ROS:" |
| Vital Signs | "Vitals:", "VS:", "BP/HR/Temp/SpO2:" |
| Physical Exam | "PE:", "Exam:", "Physical Examination:", "Objective:" |
| Assessment | "A:", "Assessment:", "Impression:", "Dx:" |
| Plan | "P:", "Plan:", "Treatment Plan:", "Recommendations:" |
| Assessment & Plan | "A/P:", "A&P:", "Assessment and Plan:" |
| Results / Labs | "Labs:", "Results:", "Lab Results:", "Recent Labs:" |
| Imaging | "Imaging:", "Radiology:", "Studies:" |
| Anticipatory Guidance | "AG:", "Anticipatory Guidance:", "Counseling:", "Education:" |
| Discharge Summary header blocks | "Discharge Diagnosis:", "Discharge Medications:", "Discharge Instructions:", "Pending Tests:", "Follow-up:" |
| Telehealth attestation | "Telehealth Attestation:", "Modality:", "Video Visit:", "Telephone Encounter:" |

### Why section context matters

The same phrase has different meaning in different sections:

- "diabetes" in PMH = historical diagnosis (typically counts)
- "diabetes" in FH = experiencer = family (does NOT count)
- "diabetes" in HPI as a differential = clinical reasoning (does NOT count)
- "diabetes" on the Problem List = active diagnosis (typically counts)
- "rule out diabetes" in Assessment = uncertain (does NOT count)

ConText handles assertion qualification within a sentence; **section context** is the orthogonal axis. Use both.

### Practical guidance

- Build a vendor-aware section parser (Epic SmartText, Cerner PowerNote, Athena dynamic templates each emit different markup)
- For scanned PDFs, OCR + heuristic header detection (regex on common patterns + indent/whitespace cues)
- Tag every extracted span with `section` as a feature; downstream rules can require or forbid certain sections per measure
- For SOAP notes, S/O/A/P are explicit; for free-form notes, fall back to "preceding header" heuristics
- Document the section taxonomy your model assumes; deviations cause silent recall drops

---

## 2. Abbreviation expansion

Clinical text is abbreviation-dense. Many abbreviations are ambiguous (lexical collisions) and require context.

### High-impact ambiguous abbreviations for HEDIS

| Abbreviation | Possible expansions | Disambiguation cue |
|---|---|---|
| MR | medical record, mitral regurgitation, mental retardation (obsolete), Med Review | section + adjacent terms |
| CBC | complete blood count, *no HEDIS conflict but high frequency* | usually unambiguous |
| RA | rheumatoid arthritis, right atrium, room air | section + adjacent terms |
| PE | physical exam, pulmonary embolism, pre-eclampsia | section header dominates |
| BS | blood sugar, bowel sounds, breath sounds | section + adjacent terms |
| BPD | blood pressure ... ?, bipolar disorder, bronchopulmonary dysplasia (peds), borderline personality disorder | clinical context |
| EDC | estimated date of confinement (OB), error data capture | section (OB Hx) |
| SI | suicidal ideation, sacroiliac | adjacent terms ("SI joint" vs "SI/HI") |
| DM | diabetes mellitus, *occasionally* differential | unambiguous in most contexts |
| SAB | spontaneous abortion, subarachnoid bleed | section + adjacent terms |
| TAB | therapeutic abortion, tablet | adjacent terms |
| ECT | electroconvulsive therapy, *occasionally* extracellular | adjacent terms |
| MS | multiple sclerosis, morphine sulfate, mitral stenosis | adjacent terms |
| HTN | hypertension | usually unambiguous |
| PE | physical exam, pulmonary embolism | section header |
| FH | family history, fundal height (OB) | section header |
| BMI | body mass index | usually unambiguous |
| DOS | date of service, *occasionally* denial of service (IT) | clinical domain |

### Practical guidance

- Maintain a domain-specific abbreviation dictionary per project; do NOT rely on generic English abbreviation lists
- Disambiguate by section header first, then by sentence-level neighbors
- For pediatric vs adult collisions (BPD bronchopulmonary dysplasia vs bipolar disorder), use patient age
- Spec-driven abbreviations (PHQ, GAD, CRAFFT, ASQ, EPDS) tend to be unambiguous; document the canonical list per measure card
- New abbreviations appear continuously - log unrecognized strings for review

---

## 3. Copy-forward detection

Copy-forward (also called copy-paste, note bloat, or template-pull) is the single largest source of stale evidence in EHR notes. A copy-forward value belongs to its **original** measurement date, not the note date.

### Common copy-forward patterns

- "Last A1c: 7.2%" repeated across 6 consecutive notes - one true measurement; five stale copies
- "PHQ-9 score: 4" copy-forwarded into every visit note - one administration; multiple stale references
- Problem list with date-stamped entries that get bulk-imported into every note's PMH section
- Discharge summary content templated into next-week's outpatient follow-up note
- "Imaging: CT chest negative" in HPI when the actual CT is from years ago

### Detection heuristics

- **Hash repetition:** identical multi-line spans across N consecutive notes for the same patient are likely copy-forward
- **Date-stamped repeats:** "A1c 7.2 on 2024-03-15" appearing in notes dated 2024-04-01, 2024-05-01, etc. - the result date is stable while the note date changes
- **Edit-distance similarity:** notes that differ by < 10% of content suggest heavy template reuse
- **Source-attribution markers:** Epic and Cerner sometimes emit "from prior note" or "imported" markers - capture these
- **Lab/result freshness mismatch:** a "today's labs" section containing a result with a 6-month-old date

### Practical guidance

- When extracting numeric results, **always extract the explicit date adjacent to the result**, not the note date
- If no result-date is present, fall back to note date but **flag the evidence** as low-confidence date provenance
- For results-section extractions, prefer structured lab tables over narrative restatements
- Document copy-forward handling per measure - some measures (GSD) are highly sensitive; others (active diagnoses) are less affected

---

## 4. Telehealth

Telehealth encounters introduce documentation patterns that differ from in-person visits and have spec-acceptance variability by measurement year.

### Encounter modality identification

Identify modality early because acceptance rules differ:

- **Video visit (synchronous A/V):** typically accepted for most measures when other components are documented
- **Telephone-only:** acceptance varies by measure and by MY; many measures introduced or removed phone acceptance during the COVID-19 era
- **E-visit / asynchronous messaging:** narrow acceptance; verify per measure
- **Remote patient monitoring (RPM):** typically counts for specific measures only (e.g., CGM for GSD)
- **Store-and-forward (e.g., teledermatology):** narrow acceptance

### Common telehealth markers

- "Telehealth Attestation: video, audio confirmed"
- "Modality: Video Visit" / "Modality: Telephone"
- "Patient connected via [Zoom / Doxy / EHR portal] video"
- "Telephone encounter, no video due to technical issue"
- "Asynchronous message reviewed and answered"
- CPT modifier 95 (synchronous telehealth) or POS code 02 / 10 in structured data

### Documentation gaps to watch for

- Telehealth note with no modality attestation - cannot confirm video vs phone
- "Telehealth visit" treated as compliant without verifying the measure-specific modality acceptance
- Physical-exam components documented in a telephone-only encounter - implausible; may be templated boilerplate
- Vital signs in a telehealth note that are patient-reported - capture the source attribution (self-report vs measured)

### Practical guidance

- Build a modality classifier as a separate model component; condition downstream extraction on its output
- Per-measure card should document telehealth acceptance for the MY you're reporting
- For physical-exam-dependent measures, downgrade evidence confidence for telephone-only encounters
- Track the spec MY for telehealth rules - they change

---

## 5. Outside records and scanned PDFs

Outside-provider records (consult notes, hospital discharge summaries, outside lab/imaging reports) are often the difference between an open and a closed measure - especially for procedures (BCS-E mammograms, COL-E colonoscopies, EED retinal exams, OSW DXA).

### Common formats

- **Faxed PDFs OCRed at intake** - quality varies; expect OCR noise on headers, dates, and numeric values
- **HIE-pulled CCDA / C-CDA documents** - structured but verbose; relevant content buried in narrative blocks
- **Patient-uploaded PDFs** (portal upload) - unverified provenance
- **Imported discharge summaries via direct messaging** - structured headers, narrative body
- **Lab interface results** - structured; usually high quality
- **Scanned legacy paper records** - heavy OCR cleanup required

### Date-attribution challenges

The **import date** (when the document landed in the receiving EHR) is **not** the date of service. Extract the date of service from the document body:

- Discharge summary: discharge date, not the date imported
- Mammogram report: study date, not the date scanned
- Outside consult note: visit date in the note header, not the date received
- Lab report: collection date and result date, not the date imported

OCR can mangle dates; build date-extraction redundancy:
- Look for multiple date occurrences within the document
- Cross-check format consistency
- Flag implausible dates (future dates, dates before plausible patient age)

### Provenance fields to capture

For every outside-record extraction, capture:

- `source_document_type` (discharge summary, mammogram report, consult note, etc.)
- `source_document_date` (date of service from document body)
- `source_import_date` (when it arrived in your EHR)
- `source_provider` (originating practice / facility, when identifiable)
- `confidence` (OCR-cleanup quality, date-extraction certainty)

These feed both the model's evidence quality assessment and MRRV defensibility.

### Practical guidance

- Build a doc-type classifier as an early pipeline step; specialized extractors per doc-type outperform generic ones
- For OCR'd PDFs, run cleanup (deskew, despeckle, header re-detection) before NLP
- Capture page numbers and bounding boxes when possible - MRRV requires re-findable evidence
- Test fixture coverage: include OCR'd outside records in evaluation sets; in-EHR-only fixtures will overstate real-world performance

---

## 6. Provider attribution

Many HEDIS measures require evidence from a **specific provider type** (PCP, OB/GYN, MH provider, eligible prescriber, clinical pharmacist). Extracting "provider type" reliably from notes is harder than it looks.

### Where provider type lives

- Structured: encounter `provider_id` → `provider_specialty` table lookup
- Note header: "Provider: Smith, Jane MD, Family Medicine"
- Signature block: "Electronically signed by Jane Smith, MD"
- Co-signature: residents and APPs co-signed by attending
- Free-text: "Seen by Dr. Garcia (cardiology) today"

### Common challenges

- Resident notes co-signed by an attending whose specialty differs
- PA / NP under a supervising MD - which specialty governs?
- Multi-specialty clinics where the same provider sees different patient populations
- Outside-record providers without specialty metadata
- Locum tenens / float providers not in the credentialing roster

### Eligible-role mapping (typical HEDIS examples)

| Measure | Eligible provider roles |
|---|---|
| PPC | OB/GYN, midwife, family practitioner, other PCP delivering prenatal/postpartum care |
| FUH | Mental health provider (psychiatrist, psychiatric APRN, licensed therapist - verify spec) |
| MRP | Prescribing practitioner, clinical pharmacist, RN |
| COA-Med Review | Prescribing practitioner, clinical pharmacist |
| CBP | Any provider taking a BP reading (some specs require qualifying setting) |
| WCV | PCP or OB/GYN |

Verify current NCQA spec per measure - eligible roles change.

### Practical guidance

- Prefer structured provider metadata over note-text inference when available
- Build a credentialing-roster join: map `provider_id` → `npi` → `taxonomy_code` → `eligible_role_for_measure`
- For outside-records, extract provider name and specialty from the note text; flag low confidence when missing
- Resident + attending co-sign: defer to attending's specialty per HEDIS convention (verify spec)

---

## 7. Multi-document linking

Real evidence often spans documents: an admission note, a discharge summary, a follow-up office visit, an outside lab result. Tying them to a single patient and encounter sequence matters.

### Linking dimensions

- **Patient identity:** MRN within an org; enterprise master patient index (EMPI) across orgs
- **Encounter identity:** encounter CSN (Epic) / FIN (Cerner) groups notes within a visit/stay
- **Episode:** a hospital stay (admit → discharge) groups multiple encounters
- **Care episode:** a referral → consult → follow-up chain
- **Temporal proximity:** documents within N days of a hospital discharge are candidates for TRC/MRP evidence

### Common challenges

- Document timestamps span midnight (admission 23:45, first inpatient note 00:15) - same episode
- Same patient with multiple MRNs in different orgs - EMPI required
- Encounter CSN missing in outside records - rely on date proximity and patient match
- Inpatient stay records linked to wrong outpatient follow-up due to date overlap

### Practical guidance

- Anchor encounters to a unified timeline per patient before extraction
- For post-discharge measures (FUH, MRP, TRC), build a "post-discharge window" view that pulls every note/document dated in the relevant window
- For longitudinal measures (GSD, BPD), pull all qualifying observations in MY and let downstream selection logic pick most-recent
- Document your linking heuristics; deduplicate evidence at the patient/measure level

---

## 8. Doc-type classification

Different doc types have different extraction shapes. A doc-type classifier as an early step lets specialized extractors run downstream.

### Useful doc-type categories for HEDIS

- Outpatient office visit (well-child, well-care, problem-focused, follow-up)
- Telehealth encounter (video, telephone, e-visit)
- Inpatient admission note
- Inpatient progress note
- Inpatient discharge summary
- ED note
- Consult note (specialty)
- Procedure note (colonoscopy, mammogram report, DXA report, etc.)
- Lab report (interface-delivered or scanned)
- Imaging report
- Pathology report
- Outside-records bundle (CCDA, faxed PDF, HIE pull)
- Behavioral health encounter
- OB/prenatal/postpartum visit
- Pediatric well-child visit
- Medication-management note (CMR, MTM)

### Practical guidance

- Classify by encounter metadata first (encounter type, billing code, POS), fall back to note text
- For ambiguous notes, run multiple extractors and reconcile downstream
- Maintain a "doc-type unknown" bucket for QA review; unknowns drive label-coverage drift

---

## 9. Structured vs narrative evidence trade-offs

For most HEDIS measures, **structured data is preferable** when available - dates are unambiguous, values are typed, and provenance is cleaner. Narrative-only evidence is necessary when structured data is missing.

### Hierarchy of preference (general)

1. Structured EHR field (e.g., LOINC-coded lab result, immunization registry entry, problem-list entry with onset date)
2. Structured outside data (HIE feed, IIS, lab interface)
3. Templated EHR section with parseable structure (e.g., flowsheet)
4. Narrative text in a known section
5. Narrative text without clear section attribution
6. Patient-reported information in narrative (lowest confidence; spec acceptance varies)

### When narrative wins

- Discussion-based numerators (ACP discussions, counseling, anticipatory guidance, education) live in narrative by definition
- Refusal documentation often only in narrative
- "Done elsewhere" patient-reported events sometimes only captured narratively

### Practical guidance

- Don't double-count: if a structured A1c result and a narrative restatement both appear, use the structured source (with the structured date)
- Capture **both** when possible for MRRV: structured value + narrative snippet for re-findability
- Document per-measure which sources you accept and in what priority

---

## See also

- [`date-of-service.md`](date-of-service.md) - date selection downstream of extraction
- [`negation-and-assertion.md`](negation-and-assertion.md) - assertion qualification on extracted spans
- [`terminology-mapping.md`](terminology-mapping.md) - code system mapping for structured extraction
- [`../hedis-supplemental-data.md`](../hedis-supplemental-data.md) - MRRV and provenance requirements
- Sibling `medical-chart-review` skill, `references/chart-structure.md` - general chart structure reference
- Sibling `medical-chart-review` skill, `references/note-types.md` - clinical note type reference
