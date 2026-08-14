# MODELS controlled-evidence intake audit

- IntakeDate: `2026-08-13T22:55:07Z`
- DownloadsPath: `$HOME/Downloads`
- BibTeXFilesFound: `8`
- ZipFilesFound: `14`
- VerifiedBibTeXFiles: `8`
- ExpectationMismatchCount: `0`
- CorruptedZipCount: `0`
- DuplicateFileCount: `4`
- AmbiguousArchiveCount: `0`
- InScopeEvidenceFiles: `14`
- HistoricalEvidenceFiles: `8`
- ControlledEvidenceCommittedCount: `0`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- PDFCommittedCount: `0`
- BibTeXParser: `BibTeX::Parser 1.05`

`DuplicateFileCount` includes two received BibTeX duplicates, one byte-identical ZIP duplicate, and one pair of ZIPs whose archive bytes differ but whose 45 PDF member hashes are identical.

## File summary

| File | Format | Scope | Records/PDFs | Integrity | Assignment | Note |
|---|---:|---:|---:|---:|---:|---|
| `models_2018_companion.bib` | BibTeX | historical | 45 | verified | MODELS 2018 Main | Content identifies the Main proceedings. |
| `models_2018_conference.bib` | BibTeX | historical | 45 | verified | duplicate | Byte-identical to the preceding BibTeX. |
| `models_2019_companion.bib` | BibTeX | historical | 117 | verified | MODELS 2019 Companion | Publisher field `year=2021` conflicts with the MODELS '19 venue/DOI identity and is preserved unchanged. |
| `models_2020_companion.bib` | BibTeX | historical | 94 | verified | MODELS 2020 Companion | Outside the interval. |
| `models_2022_companion.bib` | BibTeX | in scope | 133 | verified | MODELS 2022 Companion | Metadata source only. |
| `models_2022_conference.bib` | BibTeX | in scope | 35 | verified | MODELS 2022 Main | Metadata source only. |
| `models_2024_companion.bib` | BibTeX | in scope | 156 | verified | MODELS 2024 Companion | Metadata source only. |
| `models_2024_conference.bib` | BibTeX | in scope | 26 | verified | duplicate | Same SHA-256 as the existing pilot evidence. |
| `models_2018_companion_pdfs.zip` | ZIP | historical | 45 | verified | MODELS 2018 Main | Controlled full-text package. |
| `models_2018_conference_pdfs.zip` | ZIP | historical | 45 | verified | duplicate | All 45 member hashes equal the preceding package. |
| `models_2020_companion_part1_pdf.zip` | ZIP | historical | 48 | verified | MODELS 2020 Companion | Controlled full-text package. |
| `models_2020_companion_part2_pdf.zip` | ZIP | historical | 46 | verified | MODELS 2020 Companion | Controlled full-text package. |
| `models_2022_companion_part1_pdf.zip` | ZIP | in scope | 36 | verified | MODELS 2022 Companion | Controlled full-text package. |
| `models_2022_companion_part2_pdf.zip` | ZIP | in scope | 43 | verified | MODELS 2022 Companion | Controlled full-text package. |
| `models_2022_companion_part3_pdf.zip` | ZIP | in scope | 43 | verified | MODELS 2022 Companion | Twelve PDF hashes overlap with part 1. |
| `models_2022_companion_pdfs.zip` | ZIP | in scope | 35 | verified | MODELS 2022 Main | Internal DOI locators identify Main. |
| `models_2024_companion_part1_pdf.zip` | ZIP | in scope | 33 | verified | MODELS 2024 Companion | Controlled full-text package. |
| `models_2024_companion_part2_pdf.zip` | ZIP | in scope | 35 | verified | MODELS 2024 Companion | Controlled full-text package. |
| `models_2024_companion_part3_pdf.zip` | ZIP | in scope | 50 | verified | MODELS 2024 Companion | Controlled full-text package. |
| `models_2024_companion_part4_pdf.zip` | ZIP | in scope | 50 | verified | duplicate | Byte-identical to part 3. |
| `models_2024_companion_part5_pdf.zip` | ZIP | in scope | 38 | verified | MODELS 2024 Companion | Controlled full-text package. |
| `models_2024_conference_pdfs.zip` | ZIP | in scope | 26 | verified | MODELS 2024 Main | Pilot supplementary controlled package. |

All eight BibTeX files matched their expected SHA-256 and entry count, and every entry returned `parse_ok`. All ZIPs passed integrity testing; every member was a PDF and no archive contained duplicate member names. Full member lists and metadata-only PDF checks remain in controlled storage.

The received BibTeX and ZIP packages do not establish documentary membership. No abstract, keyword text, PDF, ZIP, or licensed export is included in the public repository.

## Incremental HTML intake update

- HTMLUpdateTimestamp: `2026-08-14T09:43:28Z`
- NewHTMLFilesFound: `1`
- NewHTMLFilesProcessed: `1`
- DuplicateHTMLFiles: `1`
- AssignedHTMLFiles: `1`
- AmbiguousHTMLFiles: `0`
- CompletePrimaryTOCHTMLCount: `1`
- VenueCrosscheckHTMLCount: `0`
- DynamicOrPartialHTMLCount: `0`
- ControlledEvidenceCommittedCount: `0`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- PDFCommittedCount: `0`

| OriginalFilename | DetectedYear | DetectedTrack | DetectedPublisher | HTMLRole | HTMLCompletenessStatus | SHA256 | AssignmentStatus | ProcessingStatus | Notes |
|---|---:|---|---|---|---|---|---|---|---|
| `models_2024_conference.html` | 2024 | MAIN | Association for Computing Machinery | PRIMARY_TOC_CANDIDATE | COMPLETE_TOC | `e7ce91d104239e87fb1675ed64ca913933b47fbc193e5f7a7797c8472aa42efc` | DUPLICATE | DUPLICATE_RECORDED | New bytes represent the same canonical proceedings and the same ordered 27-item title, DOI, and locator sequences as the already registered pilot PRIMARY_TOC. The snapshot and its 89 browser-resource files remain controlled; MODELS Main 2024 was not modified. |

The previously acquired file `Proceedings of the ACM_IEEE 27th International Conference on Model Driven Engineering Languages and Systems _ ACM Conferences.html` has SHA-256 `7efdf33b0bb911988956d08f45f902c693ac046949ea570a049e116055702f8e` and is already registered as the pilot PRIMARY_TOC. Five additional top-level HTML files and other nested HTML documents in `Downloads` were inspected by title and did not identify MODELS proceedings or an official MODELS event crosscheck; they were excluded from this MODELS intake. Associated browser resource HTMLs were treated as parts of their parent saved page, not as independent evidence.

No new unit became eligible for materialization. The new complete HTML is a documentary duplicate for the protected, already complete MODELS Main 2024 pilot; it was not added to that unit's source manifest.
