# NLBSE controlled-evidence intake audit

- IntakeDate: `2026-08-15T00:06:33Z`
- DownloadsPath: `/home/helaine-barreiros/Downloads`
- HTMLFilesFound: `4`
- BibTeXFilesFound: `4`
- RISFilesFound: `0`
- ZipFilesFound: `2`
- CompletePrimaryTOCHTMLCount: `3`
- PartialOrDynamicHTMLCount: `0`
- VenueCrosscheckHTMLCount: `1`
- VerifiedMetadataExportFiles: `4`
- ExpectationMismatchCount: `1`
- CorruptedZipCount: `0`
- DuplicateFileCount: `0`
- AmbiguousFileCount: `0`
- InScopeEvidenceFiles: `10`
- ControlledEvidenceCommittedCount: `0`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- PDFCommittedCount: `0`

| File | Assignment | Role | Integrity | Records/items | Note |
| --- | --- | --- | --- | ---: | --- |
| `nlbse_2022_toc.bib` | 2022 | METADATA_SOURCE | EXPECTATION_MISMATCH | 15 | NLBSE '22 identity and series are reported, but the publisher field `year` is 2023; preserved. |
| `nlbse_2022_toc_pdfs.zip` | 2022 | CONTROLLED_FULLTEXT_PACKAGE | VERIFIED | 15 PDFs | Intake evidence only. |
| `nlbse_2023_toc.bib` | 2023 | METADATA_SOURCE | VERIFIED | 20 | Parse failures: 0. |
| `nlbse_2023_toc.html` | 2023 | PRIMARY_TOC | VERIFIED | 20 | COMPLETE_TOC. |
| `nlbse_2024_toc.bib` | 2024 | METADATA_SOURCE | VERIFIED | 16 | Parse failures: 0. |
| `nlbse_2024_toc.html` | 2024 | PRIMARY_TOC | VERIFIED | 17 | COMPLETE_TOC: front matter plus 16 research records. |
| `acm_pdfs_1786738916644.zip` | 2024 | CONTROLLED_FULLTEXT_PACKAGE | VERIFIED | 16 PDFs | Assigned by package/bibliographic title agreement; intake evidence only. |
| `nlbse_2025_toc.bib` | 2025 | METADATA_SOURCE | VERIFIED | 18 | Two distinct DOI records share one displayed title. |
| `nlbse_2025_toc.html` | 2025 | PRIMARY_TOC | VERIFIED | 18 | COMPLETE_TOC. |
| `nlbse_2026_official_site.html` | 2026 | VENUE_CROSSCHECK | VERIFIED | 0 | EVENT_LEVEL landing page only. |

All four BibTeX exports were parsed offline with `BibTeX::Parser 1.05` and zero parse failures. Abstract and keyword values remain controlled; only availability counts are reported. Both ZIPs passed integrity and PDF technical-metadata checks. No PDF text, OCR, discovery, or screening operation was performed.
