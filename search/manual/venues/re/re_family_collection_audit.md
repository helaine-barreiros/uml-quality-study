# RE/REW family documentary collection audit

- FamilyBatchID: `MSB-RE-PREDISCOVERY-001`
- BatchExecutionDate: `2026-08-14T20:06:12Z`
- HTMLFilesFound: `9`
- BibTeXFilesFound: `8`
- RISFilesFound: `0`
- ZipFilesFound: `0`
- PlannedYearTrackPairs: `10`
- VerifiedProceedingsPairs: `8`
- CompleteDocumentaryUnits: `0`
- BlockedDocumentaryUnits: `8`
- NotCheckedPairs: `2`
- NotYetPublishedPairs: `0`
- MaterialInventoryConflictCount: `0`
- TotalRawRows: `559`
- TotalNormalizedRows: `559`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`
- REFamilyAvailableProceedingsStatus: `BLOCKED`

## Pair-level status

| Year | Track | Identity | Primary TOC | Metadata export | Venue crosscheck | Unit | Documentary status | Raw rows | Normalized rows | Material conflicts |
|---:|---|---|---|---|---|---|---|---:|---:|---:|
| 2022 | MAIN | VERIFIED | COMPLETE_CONTROLLED (49) | RECEIVED_VALIDATED (49) | REQUIRED | MSU-RE-2022-MAIN | BLOCKED | 49 | 49 | 0 |
| 2022 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (54) | RECEIVED_VALIDATED (54) | REQUIRED | MSU-REW-2022-WORKSHOPS | BLOCKED | 54 | 54 | 0 |
| 2023 | MAIN | VERIFIED | COMPLETE_CONTROLLED (63) | RECEIVED_VALIDATED (63) | REQUIRED | MSU-RE-2023-MAIN | BLOCKED | 63 | 63 | 0 |
| 2023 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (91) | RECEIVED_VALIDATED (91) | REQUIRED | MSU-REW-2023-WORKSHOPS | BLOCKED | 91 | 91 | 0 |
| 2024 | MAIN | VERIFIED | COMPLETE_CONTROLLED (69) | RECEIVED_VALIDATED (69) | REQUIRED | MSU-RE-2024-MAIN | BLOCKED | 69 | 69 | 0 |
| 2024 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (62) | RECEIVED_VALIDATED (62) | REQUIRED | MSU-REW-2024-WORKSHOPS | BLOCKED | 62 | 62 | 0 |
| 2025 | MAIN | VERIFIED | COMPLETE_CONTROLLED (80) | RECEIVED_VALIDATED (80) | REQUIRED | MSU-RE-2025-MAIN | BLOCKED | 80 | 80 | 0 |
| 2025 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (91) | RECEIVED_VALIDATED (91) | REQUIRED | MSU-REW-2025-WORKSHOPS | BLOCKED | 91 | 91 | 0 |
| 2026 | MAIN | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | — | NOT_STARTED | 0 | 0 | 0 |
| 2026 | WORKSHOPS | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | — | NOT_STARTED | 0 | 0 | 0 |

## Interpretation

Complete official publisher `PRIMARY_TOC` evidence is sufficient to materialize raw documentary membership. Validated publisher BibTeX is sufficient to populate normalized metadata for matched records. All locally available publisher TOCs for 2022–2025 are complete, and 559 raw plus 559 normalized rows are now materialized. Their normalized title multisets agree with the corresponding publisher BibTeX exports, with no material conflict. Publisher-export order differs from TOC order and was not used for membership or ordinals.

The family remains `BLOCKED` because every verified unit lacks the required independent official event program, accepted-papers page, or track page. This audit does not infer the publication status of either 2026 pair. It does not close the pre-discovery wave.

Documentary completion remains `BLOCKED` until an independent official venue crosscheck is acquired and reconciled, or a later explicit methodological decision justifies its absence. This blocker is separate from material inventory conflict and does not invalidate the publisher-defined raw inventory.

No candidate counts, discovery decisions, screening decisions, snowballing evidence, or trigger decisions were produced. No controlled HTML, BibTeX, RIS, ZIP, PDF, abstract, keyword, or full text is committed.
