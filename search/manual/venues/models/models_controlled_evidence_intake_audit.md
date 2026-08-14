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
