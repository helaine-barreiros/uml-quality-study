# MODELSWARD family collection audit

- FamilyBatchID: `MSB-MODELSWARD-PREDISCOVERY-001`
- BatchExecutionDate: `2026-08-15T00:53:15Z`
- PlannedYearPairs: `5`
- VerifiedProceedingsPairs: `5`
- CompleteDocumentaryUnits: `0`
- BlockedDocumentaryUnits: `5`
- MaterialInventoryConflictCount: `0`
- TotalRawRows: `159`
- TotalNormalizedRows: `159`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`
- MODELSWARDFamilyAvailableProceedingsStatus: `BLOCKED`

| Year | Proceedings identity | PRIMARY_TOC | Metadata export | Venue crosscheck | Raw | Normalized | Material conflicts | Documentary status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 2022 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | EVENT_LEVEL | 43 | 43 | 0 | BLOCKED |
| 2023 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | EVENT_LEVEL | 30 | 30 | 0 | BLOCKED |
| 2024 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | EVENT_LEVEL | 40 | 40 | 0 | BLOCKED |
| 2025 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | EVENT_LEVEL | 46 | 46 | 0 | BLOCKED |
| 2026 | VERIFIED | PARTIAL_CONTROLLED | RECEIVED_VALIDATED | EVENT_LEVEL | 0 | 0 | 0 | BLOCKED |

The complete 2022–2025 SCITEPRESS publisher TOCs define 159 documentary members. Their aggregate BibTeX exports reconcile one-to-one by DOI, and 159 normalized rows were materialized without publishing abstracts or keywords. Official annual event landing pages were received for 2022–2026, but they contain no locally materialized paper list and therefore provide only `EVENT_LEVEL` crosschecks. The 2022–2025 units remain blocked pending item-level or complete session-level crosschecks. MODELSWARD 2026 also remains blocked because the received publisher page materializes only 50 of 59 publisher records; its partial HTML cannot define membership, so its inventories remain empty. The family status is `BLOCKED`; this does not close the global pre-discovery wave.

## Incremental crosscheck update

- CrosscheckUpdateTimestamp: `2026-08-15T13:14:30Z`
- CrosscheckHTMLFilesProcessed: `5`
- EventLevelCrosschecks: `5`
- ItemOrCompleteSessionLevelCrosschecks: `0`
- UnitsNewlyCompleted: `0`
- NewCompletePrimaryTOCs: `0`
- MaterialInventoryConflictCount: `0`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`

The controlled pages independently confirm the annual events and link to technical-program navigation, but the program contents are not present in the saved bytes. They do not complete item-level documentary reconciliation.
