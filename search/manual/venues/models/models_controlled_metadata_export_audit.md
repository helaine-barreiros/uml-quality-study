# MODELS controlled metadata-export audit

- IntakeTimestamp: `2026-08-13T22:55:07Z`
- Parser: `BibTeX::Parser 1.05`
- BibTeXParseFailureCount: `0`
- BibTeXExpectationMismatchCount: `0`
- ControlledTextRedistributedCount: `0`

The detailed parsed rows and complete ZIP member inventories are retained under `.local-evidence/models/intake/`. This public audit reports only aggregate metadata and availability counts; it does not redistribute abstracts, author keywords, PDFs, or publisher exports.

## BibTeX validation

| Original file | SHA-256 verified | Entries | Type | Unique DOI | Duplicate DOI | Duplicate title | Missing DOI | Missing title | Missing authors | Abstract available | Keywords available | Observed year | ISBN |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `models_2018_companion.bib` | true | 45 | `inproceedings` | 45 | 0 | 0 | 0 | 0 | 0 | 42 | 38 | 2018 | `9781450349499` |
| `models_2018_conference.bib` | true | 45 | `inproceedings` | 45 | 0 | 0 | 0 | 0 | 0 | 42 | 38 | 2018 | `9781450349499` |
| `models_2019_companion.bib` | true | 117 | `inproceedings` | 117 | 0 | 0 | 0 | 0 | 0 | 117 | 98 | 2021 | `9781728151250` |
| `models_2020_companion.bib` | true | 94 | `inproceedings` | 94 | 0 | 0 | 0 | 0 | 0 | 94 | 92 | 2020 | `9781450381352` |
| `models_2022_companion.bib` | true | 133 | `inproceedings` | 133 | 0 | 0 | 0 | 0 | 0 | 133 | 122 | 2022 | `9781450394673` |
| `models_2022_conference.bib` | true | 35 | `inproceedings` | 35 | 0 | 0 | 0 | 0 | 0 | 35 | 30 | 2022 | `9781450394666` |
| `models_2024_companion.bib` | true | 156 | `inproceedings` | 156 | 0 | 0 | 0 | 0 | 0 | 156 | 153 | 2024 | `9798400706226` |
| `models_2024_conference.bib` | true | 26 | `inproceedings` | 26 | 0 | 0 | 0 | 0 | 0 | 26 | 24 | 2024 | `9798400705045` |

Every entry returned `parse_ok`. The two 2018 BibTeX files are byte-identical. The 2024 Main file is byte-identical to the metadata source already registered for the validated pilot and was not used to regenerate that unit.

The 2019 Companion export identifies `MODELS ’19 Companion`, uses 2019 DOI values, and reports publisher field `year=2021`. This source-level conflict is preserved and reported; no correction was made. The historical acquisitions from 2018, 2019, and 2020 are quarantined outside the protocol interval and do not instantiate production units.

## Controlled PDF-package validation

| Detected unit | Received archives | PDF members | Unique PDF hashes | Corrupted archives | Non-PDF members | Duplicate observation |
|---|---:|---:|---:|---:|---:|---|
| MODELS 2018 Main (historical) | 2 | 90 | 45 | 0 | 0 | Both archives contain the same 45 PDF hashes although ZIP bytes differ. |
| MODELS 2020 Companion (historical) | 2 | 94 | 94 | 0 | 0 | None across parts. |
| MODELS 2022 Main | 1 | 35 | 35 | 0 | 0 | None. |
| MODELS 2022 Companion | 3 | 122 | 110 | 0 | 0 | Twelve PDF hashes occur in both parts 1 and 3. |
| MODELS 2024 Main | 1 | 26 | 26 | 0 | 0 | Pilot supplementary package only. |
| MODELS 2024 Companion | 5 | 206 | 156 | 0 | 0 | Parts 3 and 4 are byte-identical. |

All 14 ZIPs passed integrity testing. Every ZIP member was a PDF, no archive contained duplicate member names, and all `pdfinfo` checks succeeded. `pdftotext`, OCR, and relevance inspection were not used.

Package cardinality is only complementary evidence. Neither equality with a BibTeX count nor a complete-looking ZIP establishes the publisher TOC or documentary membership.
