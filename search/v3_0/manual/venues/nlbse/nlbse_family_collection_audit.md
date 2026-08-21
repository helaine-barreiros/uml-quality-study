# NLBSE family collection audit

- FamilyBatchID: `MSB-NLBSE-PREDISCOVERY-001`
- BatchExecutionDate: `2026-08-15T00:06:33Z`
- PlannedYearPairs: `5`
- VerifiedProceedingsPairs: `4`
- CompleteDocumentaryUnits: `0`
- BlockedDocumentaryUnits: `4`
- NotCheckedOrNotVerifiedPairs: `1`
- MaterialInventoryConflictCount: `0`
- TotalRawRows: `55`
- TotalNormalizedRows: `55`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- ControlledEvidenceCommittedCount: `0`
- NLBSEFamilyAvailableProceedingsStatus: `BLOCKED`

| Year | Proceedings identity | PRIMARY_TOC | Metadata export | Venue crosscheck | Raw | Normalized | Material conflicts | Documentary status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 2022 | VERIFIED | REQUIRED | RECEIVED_EXPECTATION_MISMATCH | REQUIRED | 0 | 0 | 0 | BLOCKED |
| 2023 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | REQUIRED | 20 | 20 | 0 | BLOCKED |
| 2024 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | REQUIRED | 17 | 17 | 0 | BLOCKED |
| 2025 | VERIFIED | COMPLETE_CONTROLLED | RECEIVED_VALIDATED | REQUIRED | 18 | 18 | 0 | BLOCKED |
| 2026 | NOT_VERIFIED | NOT_CHECKED | NOT_RECEIVED | RECEIVED_EVENT_LEVEL | 0 | 0 | 0 | NOT_STARTED |

The 2023–2025 complete publisher TOCs and metadata exports reconcile without material conflict. Their raw and normalized inventories are materialized, but documentary completion remains blocked by missing independent official venue crosschecks. NLBSE 2022 lacks a membership-defining publisher TOC and also remains blocked. NLBSE 2026 is represented only by an event-level official site and is not instantiated as a proceedings unit. The family status is therefore `BLOCKED`; this does not close the global pre-discovery wave.
