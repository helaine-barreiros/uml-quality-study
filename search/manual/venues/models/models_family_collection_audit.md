# MODELS family collection audit

- AuditTimestamp: `2026-08-14T09:43:28Z`
- PlannedYearTrackPairs: `10`
- InstantiatedUnits: `4`
- CompleteDocumentaryUnits: `1`
- BlockedDocumentaryUnits: `3`
- MaterialInventoryConflictCount: `0`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`
- MODELSFamilyAvailableProceedingsStatus: `BLOCKED`

`BLOCKED` is required because three verified and instantiated units still lack controlled official publisher TOCs and official venue crosschecks. This family status does not close the pre-discovery wave or the final search update.

Unit `source_manifest.csv` files contain only documentary-pipeline sources. Controlled PDF ZIPs remain exclusively in `controlled_evidence_intake_log.csv` and aggregate intake audits as `CONTROLLED_FULLTEXT_PACKAGE`; they are not `AUXILIARY_NAVIGATION`, cannot create membership, and cannot authorize raw or normalized inventory population. The ZIP and PDF totals already audited are unchanged.

## Year × track status

| Year | TrackType | ManualSearchUnitID | UnitStatus | DocumentaryCollectionStatus | PrimaryTOCStatus | VenueCrosscheckStatus | RawRows | NormalizedRows | Notes |
|---:|---|---|---|---|---|---|---:|---:|---|
| 2022 | MAIN | `MSU-MODELS-2022-MAIN` | BLOCKED | BLOCKED | REQUIRED | REQUIRED | 0 | 0 | Publisher metadata source registered in the unit manifest; controlled full-text package recorded only in the intake log; primary and crosscheck evidence still required. |
| 2022 | COMPANION | `MSU-MODELS-2022-COMPANION` | BLOCKED | BLOCKED | REQUIRED | REQUIRED | 0 | 0 | Publisher metadata source registered in the unit manifest; controlled full-text packages recorded only in the intake log; primary and crosscheck evidence still required. |
| 2023 | MAIN |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; no unit instantiated. |
| 2023 | COMPANION |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; no unit instantiated. |
| 2024 | MAIN | `MSU-MODELS-2024-MAIN` | IN_PROGRESS | COMPLETE | COMPLETE | COMPLETE | 27 | 27 | Validated pilot preserved byte-identically; incremental HTML was a documentary duplicate. |
| 2024 | COMPANION | `MSU-MODELS-2024-COMPANION` | BLOCKED | BLOCKED | REQUIRED | REQUIRED | 0 | 0 | Publisher metadata source registered in the unit manifest; controlled full-text packages recorded only in the intake log; primary and crosscheck evidence still required. |
| 2025 | MAIN |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; publication status not inferred. |
| 2025 | COMPANION |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; publication status not inferred. |
| 2026 | MAIN |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; publication status not inferred. |
| 2026 | COMPANION |  |  |  | NOT_CHECKED | NOT_CHECKED | 0 | 0 | No MODELS evidence received in this intake; publication status not inferred. |

## Incremental HTML update

- HTMLUpdateTimestamp: `2026-08-14T09:43:28Z`
- HTMLFilesProcessed: `1`
- UnitsNewlyCompleted: `0`
- UnitsStillBlocked: `3`
- UnitsWaitingForCrosscheck: `3`
- UnitsWaitingForPrimaryTOC: `3`
- MaterialInventoryConflictCount: `0`
- TotalRawRowsAdded: `0`
- TotalNormalizedRowsAdded: `0`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`

The incremental file `models_2024_conference.html` is a complete saved ACM TOC with the same canonical proceedings identity and ordered 27-item documentary sequence as the existing MODELS Main 2024 source. It was retained as controlled duplicate evidence and did not reopen or modify the pilot.

No new PRIMARY_TOC or VENUE_CROSSCHECK was received for MODELS 2022 Main, MODELS 2022 Companion, or MODELS 2024 Companion. Those units remain blocked and no raw or normalized rows were added.
