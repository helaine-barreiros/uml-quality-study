# RE/REW family documentary collection audit

- FamilyBatchID: `MSB-RE-PREDISCOVERY-001`
- BatchExecutionDate: `2026-08-14T20:06:12Z`
- HTMLFilesFound: `18`
- BibTeXFilesFound: `8`
- RISFilesFound: `0`
- ZipFilesFound: `0`
- PlannedYearTrackPairs: `10`
- VerifiedProceedingsPairs: `8`
- CompleteDocumentaryUnits: `1`
- BlockedDocumentaryUnits: `7`
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
| 2022 | MAIN | VERIFIED | COMPLETE_CONTROLLED (49) | RECEIVED_VALIDATED (49) | COMPLETE / ITEM_LEVEL (47) | MSU-RE-2022-MAIN | COMPLETE | 49 | 49 | 0 |
| 2022 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (54) | RECEIVED_VALIDATED (54) | PARTIAL / TRACK_LEVEL (7) | MSU-REW-2022-WORKSHOPS | BLOCKED | 54 | 54 | 0 |
| 2023 | MAIN | VERIFIED | COMPLETE_CONTROLLED (63) | RECEIVED_VALIDATED (63) | PARTIAL / TRACK_LEVEL (56) | MSU-RE-2023-MAIN | BLOCKED | 63 | 63 | 0 |
| 2023 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (91) | RECEIVED_VALIDATED (91) | PARTIAL / TRACK_LEVEL (14) | MSU-REW-2023-WORKSHOPS | BLOCKED | 91 | 91 | 0 |
| 2024 | MAIN | VERIFIED | COMPLETE_CONTROLLED (69) | RECEIVED_VALIDATED (69) | PARTIAL / TRACK_LEVEL (55) | MSU-RE-2024-MAIN | BLOCKED | 69 | 69 | 0 |
| 2024 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (62) | RECEIVED_VALIDATED (62) | PARTIAL / TRACK_LEVEL (10) | MSU-REW-2024-WORKSHOPS | BLOCKED | 62 | 62 | 0 |
| 2025 | MAIN | VERIFIED | COMPLETE_CONTROLLED (80) | RECEIVED_VALIDATED (80) | PARTIAL / TRACK_LEVEL (76) | MSU-RE-2025-MAIN | BLOCKED | 80 | 80 | 0 |
| 2025 | WORKSHOPS | VERIFIED | COMPLETE_CONTROLLED (91) | RECEIVED_VALIDATED (91) | PARTIAL / TRACK_LEVEL (12) | MSU-REW-2025-WORKSHOPS | BLOCKED | 91 | 91 | 0 |
| 2026 | MAIN | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | — | NOT_STARTED | 0 | 0 | 0 |
| 2026 | WORKSHOPS | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | NOT_CHECKED | — | NOT_STARTED | 0 | 0 | 0 |

## Interpretation

Complete official publisher `PRIMARY_TOC` evidence is sufficient to materialize raw documentary membership. Validated publisher BibTeX is sufficient to populate normalized metadata for matched records. All locally available publisher TOCs for 2022–2025 are complete, and 559 raw plus 559 normalized rows are now materialized. Their normalized title multisets agree with the corresponding publisher BibTeX exports, with no material conflict. Publisher-export order differs from TOC order and was not used for membership or ordinals.

## Venue-crosscheck reconciliation

| Unit | Granularity | Exact | Normalized | Title drift | Author drift | Primary research only | Crosscheck only | Ambiguous | Material conflicts |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MSU-RE-2022-MAIN | ITEM_LEVEL | 29 | 1 | 11 | 9 | 0 | 6 | 0 | 0 |
| MSU-REW-2022-WORKSHOPS | TRACK_LEVEL | 0 | 1 | 2 | 0 | 41 | 4 | 0 | 0 |
| MSU-RE-2023-MAIN | TRACK_LEVEL | 31 | 6 | 3 | 9 | 16 | 16 | 0 | 0 |
| MSU-REW-2023-WORKSHOPS | TRACK_LEVEL | 0 | 0 | 6 | 0 | 80 | 8 | 0 | 0 |
| MSU-RE-2024-MAIN | TRACK_LEVEL | 27 | 12 | 4 | 13 | 17 | 12 | 0 | 0 |
| MSU-REW-2024-WORKSHOPS | TRACK_LEVEL | 0 | 0 | 0 | 0 | 57 | 10 | 0 | 0 |
| MSU-RE-2025-MAIN | TRACK_LEVEL | 45 | 4 | 2 | 23 | 20 | 25 | 0 | 0 |
| MSU-REW-2025-WORKSHOPS | TRACK_LEVEL | 0 | 0 | 4 | 0 | 82 | 8 | 0 | 0 |

`MSU-RE-2022-MAIN` is documentary-complete: its official accepted-paper list accounts for every authored publisher item, while eight editorial publisher records are legitimately absent and six accepted records belong to the broader event scope. The other seven pages confirm tracks or program sessions but do not enumerate complete proceedings papers, so those units remain blocked by `ITEM_LEVEL_VENUE_CROSSCHECK_REQUIRED`.

The family remains `BLOCKED` because seven verified units still lack sufficient item-level independent crosschecks. No new RE/REW 2026 HTML was found; both 2026 pairs remain `NOT_CHECKED`, with no proceedings unit instantiated and no publication status inferred. This status does not close the pre-discovery wave.

Partial track/session evidence is a process blocker rather than a material inventory conflict. It does not invalidate the publisher-defined raw or normalized inventories.

No candidate counts, discovery decisions, screening decisions, snowballing evidence, or trigger decisions were produced. No controlled HTML, BibTeX, RIS, ZIP, PDF, abstract, keyword, or full text is committed.
