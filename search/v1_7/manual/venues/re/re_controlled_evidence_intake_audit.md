# RE/REW controlled-evidence intake audit

- IntakeDate: `2026-08-14T20:06:12Z`
- DownloadsPath: `$HOME/Downloads`
- FamilyBatchID: `MSB-RE-PREDISCOVERY-001`
- HTMLFilesFound: `18`
- BibTeXFilesFound: `8`
- RISFilesFound: `0`
- ZipFilesFound: `0`
- CompletePrimaryTOCHTMLCount: `8`
- PartialOrDynamicHTMLCount: `0`
- VenueCrosscheckHTMLCount: `8`
- VerifiedMetadataExportFiles: `8`
- ExpectationMismatchCount: `0`
- CorruptedZipCount: `0`
- DuplicateFileCount: `2`
- AmbiguousFileCount: `0`
- InScopeEvidenceFiles: `26`
- ControlledEvidenceCommittedCount: `0`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- PDFCommittedCount: `0`
- BibTeXParser: `BibTeX::Parser 1.05`

Counts refer only to files whose local content identifies the RE/REW family. Three IEEE RIS search exports and the available ZIP archives were inspected at identification level and excluded because they do not represent RE/REW proceedings metadata exports or proceedings-level PDF packages. No network access was used.

## File summary

| Original file | Year/track | Role | Records | Integrity | Completeness/assignment | Note |
|---|---|---|---:|---|---|---|
| `re_2022_main.bib` | 2022 MAIN | METADATA_SOURCE | 49 | verified | assigned | All entries parsed; DOI base agrees with the locally observed proceedings identity. |
| `re_2022_main_toc.html` | 2022 MAIN | PRIMARY_TOC | 49 | verified | COMPLETE_TOC | Local page reports 1–49 of 49. |
| `re_2022_workshops.bib` | 2022 WORKSHOPS | METADATA_SOURCE | 54 | verified | assigned | All entries parsed. |
| `rew_2022_toc.html.html` | 2022 WORKSHOPS | PRIMARY_TOC | 54 | verified | COMPLETE_TOC | Local page reports 1–54 of 54. |
| `re_2023_main.bib` | 2023 MAIN | METADATA_SOURCE | 63 | verified | assigned | All entries parsed; one repeated publisher title occurs under distinct DOI records. |
| `re_2023_main_toc.html.html` | 2023 MAIN | PRIMARY_TOC | 63 | verified | COMPLETE_TOC | Local page reports 1–63 of 63. |
| `re_2023_workshops.bib` | 2023 WORKSHOPS | METADATA_SOURCE | 91 | verified | assigned | All entries parsed. |
| `rew_2023_toc.html` | 2023 WORKSHOPS | PRIMARY_TOC | 91 | verified | COMPLETE_TOC | Local page reports 1–91 of 91. |
| `re_2024_main.bib` | 2024 MAIN | METADATA_SOURCE | 69 | verified | assigned | All entries parsed. |
| `re_2024_main_toc.html` | 2024 MAIN | PRIMARY_TOC | 69 | verified | COMPLETE_TOC | Local page reports 1–69 of 69. |
| `re_2024_workshops.bib` | 2024 WORKSHOPS | METADATA_SOURCE | 62 | verified | assigned | All entries parsed; one repeated publisher title occurs under distinct DOI records. |
| `rew_2024_toc.html` | 2024 WORKSHOPS | PRIMARY_TOC | 62 | verified | COMPLETE_TOC | Local page reports 1–62 of 62. |
| `re_2025_main.bib` | 2025 MAIN | METADATA_SOURCE | 80 | verified | assigned | All entries parsed. |
| `re_2025_main_toc.html` | 2025 MAIN | PRIMARY_TOC | 80 | verified | COMPLETE_TOC | IEEE CSDL reports 80 out of 80. |
| `re_2025_workshops.bib` | 2025 WORKSHOPS | METADATA_SOURCE | 91 | verified | assigned | All entries parsed. |
| `rew_2025_toc.html` | 2025 WORKSHOPS | PRIMARY_TOC | 91 | verified | COMPLETE_TOC | Local page reports 1–91 of 91. |
| `re_2025.html` | 2025 MAIN | PRIMARY_TOC duplicate | 80 | verified | duplicate | Byte-different browser save of the same canonical page and ordered 80-item sequence; not used as an additional membership source. |

## Offline validation findings

The IEEE bulk BibTeX files concatenate entries without a line break between the closing brace and the next entry marker. The reusable audit tool inserts only this missing lexical boundary in memory and then requires `BibTeX::Parser 1.05` and `parse_ok` for every record. The source bytes are not changed.

All eight official publisher TOCs expose a complete local cardinality marker matching the extracted ordered-item count and corresponding publisher export count. The normalized title multisets agree for every unit. Publisher export order differs from TOC order and therefore does not define membership or source ordinal.

The IEEE CSDL 2025 Main page presents abbreviated visible authors for 71 authored records; the complete publisher BibTeX author lists differ diagnostically. This `AUTHOR_LIST_DRIFT` does not challenge membership. No external correction was applied.

The initial intake contained no independent official event page. Raw and normalized inventories were subsequently materialized from the complete publisher TOCs and reconciled publisher metadata exports under the corrected operational policy; those inventories were not regenerated during the crosscheck intake below.

No abstract text, keyword text, protected HTML, BibTeX export, RIS export, ZIP, PDF, or full text is committed.

## Incremental official venue-crosscheck intake

- HTMLUpdateTimestamp: `2026-08-14T22:42:09Z`
- NewHTMLFilesFound: `9`
- NewHTMLFilesProcessed: `9`
- DuplicateHTMLFiles: `1`
- AssignedCanonicalCrosscheckFiles: `8`
- AmbiguousHTMLFiles: `0`
- ItemLevelCrosscheckFiles: `1`
- PartialTrackOrSessionCrosscheckFiles: `7`
- RE2026HTMLFilesFound: `0`
- ControlledEvidenceCommittedCount: `0`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- PDFCommittedCount: `0`

| Original file | Year/track | Role | Observed records | Effective granularity | Assignment | Result |
|---|---|---|---:|---|---|---|
| `re_2022_main_crosscheck_accepted.html` | 2022 MAIN | VENUE_CROSSCHECK | 47 | ITEM_LEVEL | assigned | Covers all 41 publisher research items; eight publisher editorial items are legitimately primary-only and six broader-event accepted records are crosscheck-only. |
| `re_2022_main_crosscheck_accepted.html.html` | 2022 MAIN | VENUE_CROSSCHECK | 47 | ITEM_LEVEL | duplicate | Byte-different save of the same official accepted-paper page and item sequence; retained only as duplicate controlled evidence. |
| `rew_2022_workshops_crosscheck.html` | 2022 WORKSHOPS | VENUE_CROSSCHECK | 7 | TRACK_LEVEL | assigned | Workshop sessions do not enumerate complete proceedings papers. |
| `re_2023_main_crosscheck_research.html` | 2023 MAIN | VENUE_CROSSCHECK | 56 | TRACK_LEVEL | assigned | Session/program capture leaves 16 publisher research items unmatched. |
| `rew_2023_workshops_crosscheck.html` | 2023 WORKSHOPS | VENUE_CROSSCHECK | 14 | TRACK_LEVEL | assigned | Workshop sessions do not enumerate complete proceedings papers. |
| `re_2024_main_crosscheck_research.html` | 2024 MAIN | VENUE_CROSSCHECK | 55 | TRACK_LEVEL | assigned | Session/program capture leaves 17 publisher research items unmatched. |
| `rew_2024_workshops_crosscheck.html` | 2024 WORKSHOPS | VENUE_CROSSCHECK | 10 | TRACK_LEVEL | assigned | Workshop and catering events do not enumerate complete proceedings papers. |
| `re_2025_main_crosscheck_research.html` | 2025 MAIN | VENUE_CROSSCHECK | 76 | TRACK_LEVEL | assigned | Session/program capture leaves 20 publisher research items unmatched and includes broader event records. |
| `rew_2025_workshops_crosscheck.html` | 2025 WORKSHOPS | VENUE_CROSSCHECK | 12 | TRACK_LEVEL | assigned | Repeated workshop schedule events do not enumerate complete proceedings papers. |

Only `MSU-RE-2022-MAIN` has sufficient independent item-level coverage to complete its documentary reconciliation. The other seven units remain blocked for an item-level official venue crosscheck. No new RE/REW 2026 HTML was found, so neither 2026 proceedings unit is instantiated or advanced.
