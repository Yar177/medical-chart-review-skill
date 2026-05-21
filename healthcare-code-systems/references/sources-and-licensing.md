# Sources and licensing

> **Why this file exists:** Every code system has an **authoritative source** and a **licensing constraint**. Some are free public domain (ICD-10-CM, NDC, CVX), some require a free account (RxNorm, SNOMED in the US, LOINC), and some require **paid commercial licensing** (CPT, NCQA HEDIS, APR-DRG, CDT, commercial drug DBs). Mis-handling licensing exposes the organization to legal risk.

## 1. License risk matrix

| Code system | License | Free? | Redistribution OK? |
|---|---|---|---|
| **ICD-10-CM** | US government, public domain | Yes | Yes |
| **ICD-10-PCS** | US government, public domain | Yes | Yes |
| **ICD-9-CM** | US government, public domain | Yes | Yes |
| **CPT** | **AMA proprietary - paid license required** | **No** | **No, without AMA Data File License** |
| **HCPCS Level II** | CMS, public domain | Yes | Yes (the codes themselves; some descriptive content may have third-party rights) |
| **NDC Directory** | FDA, public domain | Yes | Yes |
| **RxNorm** | NLM, free with UMLS account | Yes | Yes, with attribution |
| **SNOMED CT (US Edition)** | Free in US under NLM country license; **paid affiliate license outside US** (varies) | Yes (US) / Varies (non-US) | Yes (US), with UMLS license terms |
| **LOINC** | Free with registration | Yes | Yes, with attribution |
| **UCUM** | Free, public | Yes | Yes |
| **CVX / MVX** | CDC, public domain | Yes | Yes |
| **NUCC Provider Taxonomy** | Free | Yes | Yes |
| **NPPES NPI file** | Public | Yes | Yes |
| **DEA registration data** | Restricted (DEA) | No bulk | No |
| **NCQA HEDIS value sets** | **NCQA proprietary - licensed** | **No** | **No, without NCQA license** |
| **AHRQ CCSR / Elixhauser / PSI / IQI / PDI** | Public domain | Yes | Yes |
| **MS-DRG (Medicare grouper)** | CMS, public | Yes | Yes |
| **APR-DRG (3M)** | **3M proprietary - paid license** | **No** | **No** |
| **APC** | CMS, public | Yes | Yes |
| **NCCI edits** | CMS, public | Yes | Yes |
| **BETOS 2.0** | CMS, public | Yes | Yes |
| **CCS (legacy)** | Public | Yes | Yes |
| **CDT (dental)** | **ADA proprietary - paid license** | **No** | **No** |
| **ATC** | WHOCC, free for non-commercial; commercial / large-scale requires arrangement | Conditional | Conditional |
| **First Databank (FDB)** | **Wolters Kluwer / FDB, paid commercial** | **No** | **No** |
| **Medi-Span** | **Wolters Kluwer, paid commercial** | **No** | **No** |
| **Multum** | **Cerner / Oracle Health, paid commercial** | **No** | **No** |
| **VSAC content** | Free with UMLS account; per-value-set license varies (HEDIS in VSAC still subject to NCQA license) | Conditional | Conditional |

## 2. The big ones to handle carefully

### CPT (AMA)

- **AMA owns the copyright** on CPT codes, descriptors, and modifiers.
- An **AMA Data File License** is required to use CPT in any software, database, or product. Pricing varies by use case (internal use, end-user product, OEM).
- **Healthcare providers and payers** typically have an existing AMA license for billing operations; using CPT for analytics within that org is usually covered, but redistribution outside the org is not.
- **Open-source projects**: cannot embed CPT codes / descriptions without each user obtaining their own AMA license.
- **Common-knowledge use** (referring to CPT in documentation, listing a few representative codes for illustration) is generally tolerated; bulk embedding of CPT tables is not.

**Practical guidance**: do not commit CPT tables, descriptions, or comprehensive crosswalks involving CPT to public repositories. Reference CPT via OID, code number, and brief description for illustration; rely on the consuming organization's licensed CPT data.

### NCQA HEDIS

- **NCQA owns** HEDIS measure specifications, value sets, and technical documentation.
- A **HEDIS license** is required for any organization implementing HEDIS measures.
- The **HEDIS Volume 2 Technical Specifications** and **Value Set Directory** are licensed products.
- Health plans operating in markets requiring HEDIS reporting already have a license.
- **Vendors** building HEDIS engines need NCQA licenses for the measures they implement.
- The `hedis-nlp` skill in this repo writes about the structure and approach but **does not embed NCQA value sets**; consuming organizations bring their own licensed value sets.

### APR-DRG (3M)

- **3M Health Information Systems owns** APR-DRG.
- Paid commercial license required.
- Widely used by states (Medicaid) and commercial payers; if your organization uses APR-DRG, the license is in place.
- Cannot embed APR-DRG logic / weights in open repositories.

### CDT (ADA)

- **American Dental Association owns** CDT.
- Annual update January 1.
- Used in dental insurance claims; integrated into HCPCS Level II as `D` codes.
- ADA licensing required for software / database use.

### Commercial drug knowledge bases (FDB / Medi-Span / Multum)

- All three are commercial, all three are paid, all three publish drug clinical content (interactions, dosing, allergy cross-reactivity).
- Most EHR vendors license one for clinical decision support.
- Analytics teams typically work downstream of EHR / pharmacy data already enriched with drug-knowledge-base attributes; the licensing flows through the vendor relationship.
- Cannot extract drug-DB content for use outside the licensed scope.

## 3. Free but registered

### NLM UMLS

- Required for **RxNorm**, **SNOMED CT (US)**, **VSAC**, **MeSH**, and the **Metathesaurus** (a unified terminology service).
- Free; requires a **UMLS Terminology Services (UTS) account**.
- License agreement requires:
  - Attribution
  - Compliance with the embedded license terms of each source vocabulary (e.g., SNOMED's country-specific terms)
  - Reporting of usage at NLM's request

### LOINC

- Free with **registration** at <https://loinc.org/>.
- LOINC license requires preserving the license notice in redistributed content.

## 4. Public domain

These can be freely used, embedded, and redistributed without license:

- **ICD-10-CM, ICD-10-PCS, ICD-9-CM** (US government)
- **HCPCS Level II codes** (CMS)
- **NDC Directory** (FDA)
- **CVX, MVX** (CDC)
- **NUCC taxonomy**
- **MS-DRG, APC** (CMS)
- **AHRQ CCSR, Elixhauser, PSI, IQI, PDI, BETOS 2.0** (AHRQ / CMS)
- **NCCI edits** (CMS)
- **NPPES NPI registry** (CMS)
- **CMS-HCC and HHS-HCC software** (CMS / HHS)

Even for public-domain content, **attribution to source** is good practice.

## 5. International / non-US considerations

- **SNOMED CT** licensing varies dramatically by country. The US country license makes SNOMED free within the US; many other countries are SNOMED International member countries (free in-country); some require paid affiliate licensing. Multi-country use requires per-country license analysis.
- **ICD-10** (WHO version, distinct from ICD-10-CM) is WHO copyright; permission required for redistribution. Most countries that use WHO ICD-10 have a national agreement.
- **ICD-11** (WHO) - similar; WHO licenses content for member-state use.

## 6. Authoritative source URLs

### Government / public

- **ICD-10-CM**: <https://www.cdc.gov/nchs/icd/icd-10-cm.htm>
- **ICD-10-PCS**: <https://www.cms.gov/medicare/icd-10/2024-icd-10-pcs>
- **HCPCS Level II**: <https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system>
- **NDC Directory (FDA)**: <https://www.accessdata.fda.gov/scripts/cder/ndc/>
- **MS-DRG**: <https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/MS-DRG-Classifications-and-Software>
- **APC**: <https://www.cms.gov/medicare/payment/prospective-payment-systems/hospital-outpatient>
- **NCCI**: <https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits>
- **NPPES**: <https://download.cms.gov/nppes/NPI_Files.html>
- **CMS-HCC software**: <https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors>
- **HHS-HCC (CCIIO)**: <https://www.cms.gov/cciio/resources/regulations-and-guidance>
- **CCSR (AHRQ)**: <https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp>
- **AHRQ Elixhauser**: <https://hcup-us.ahrq.gov/toolssoftware/comorbidity/comorbidity.jsp>
- **CVX / MVX**: <https://www2a.cdc.gov/vaccines/iis/iisstandards/vaccines.asp>
- **NUCC Taxonomy**: <https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40>
- **BETOS 2.0**: <https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/berenson-eggers-type-of-service-betos-classification-system>

### Free with registration

- **RxNorm**: <https://www.nlm.nih.gov/research/umls/rxnorm/>
- **SNOMED CT US Edition**: <https://www.nlm.nih.gov/healthit/snomedct/us_edition.html>
- **LOINC**: <https://loinc.org/>
- **VSAC**: <https://vsac.nlm.nih.gov/>
- **UCUM**: <https://ucum.org/>

### Licensed (paid)

- **AMA CPT**: <https://www.ama-assn.org/practice-management/cpt>
- **NCQA HEDIS**: <https://www.ncqa.org/hedis/>
- **3M APR-DRG**: <https://www.solventum.com/> (formerly 3M HIS)
- **ADA CDT**: <https://www.ada.org/cdt>
- **First Databank**: <https://www.fdbhealth.com/>
- **Wolters Kluwer Medi-Span**: <https://www.wolterskluwer.com/en/solutions/medi-span>

## 7. Practical guidance for this repo (and similar open ones)

- **Embed**: public-domain content (ICD-10-CM examples, NDC structure examples, CCSR examples, etc.).
- **Reference**: licensed content (CPT codes, HEDIS measure specifications, APR-DRG logic) - cite, illustrate sparingly, link to authoritative source.
- **Avoid**: comprehensive tables of licensed content. The exception is brief illustrative examples that fall within fair-use norms.
- **License note**: a `LICENSING.md` or section in each reference file noting the constraint is good hygiene.

## 8. Common pitfalls

- **Embedding CPT tables** in a public GitHub repository.
- **Distributing NCQA HEDIS value sets** to entities without their own NCQA license.
- **Using APR-DRG logic in open-source tooling** without 3M agreement.
- **Treating SNOMED CT as universally free** - it's free in the US under NLM license, not globally.
- **Skipping the UMLS account requirement** for RxNorm / SNOMED / VSAC.
- **Extracting drug-DB content** (FDB / Medi-Span / Multum) for use outside the licensed scope.
- **Assuming "public domain" means "uncontrolled"** - even public-domain content benefits from authoritative-source citation for reproducibility.
- **Out-of-date source URLs** - the CMS and NLM websites reorganize occasionally; URL drift requires periodic maintenance.
