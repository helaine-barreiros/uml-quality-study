# MODELS family documentary-collection audit

- FamilyBatchID: `MSB-MODELS-PREDISCOVERY-001`
- BatchExecutionDate: `2026-08-13T21:50:03Z`
- BatchIntervalStart: `2022-01-01`
- BatchCutoffDate: `2026-08-13`
- BatchScope: all officially published and verifiable MODELS Main and MODELS Companion proceedings available at execution time
- PlannedYearTrackPairs: `10`
- VerifiedProceedingsPairs: `5`
- CompleteDocumentaryUnits: `1`
- BlockedDocumentaryUnits: `4`
- BlockedYearTrackPairs: `7`
- NotYetPublishedPairs: `2`
- NotApplicablePairs: `0`
- MaterialInventoryConflictCount: `0`
- DiscoveryDataRows: `0`
- CandidateCountPopulatedUnits: `0`
- RawInventoriesModifiedAfterCommitCount: `0`
- ControlledEvidenceCommittedCount: `0`
- MODELSFamilyAvailableProceedingsStatus: `BLOCKED`

The family batch cannot be complete because four instantiated units require controlled publisher evidence and three published pairs still lack an official complete publisher volume locator. This family-level status does not alter `PreDiscoveryClosureStatus` and is not a final-search closure.

| Year | Track | Identity status | Unit | Documentary collection | Raw items | Normalized rows | Material conflicts | Evidence |
|---:|---|---|---|---|---:|---:|---:|---|
| 2022 | MAIN | VERIFIED | `MSU-MODELS-2022-MAIN` | BLOCKED | 0 | 0 | 0 | ACM HTTP 403; controlled evidence requested |
| 2022 | COMPANION | VERIFIED | `MSU-MODELS-2022-COMPANION` | BLOCKED | 0 | 0 | 0 | ACM HTTP 403; controlled evidence requested |
| 2023 | MAIN | BLOCKED | — | BLOCKED | n/a | n/a | 0 | Official complete publisher locator not established |
| 2023 | COMPANION | VERIFIED | `MSU-MODELS-2023-COMPANION` | BLOCKED | 0 | 0 | 0 | IEEE page empty/HTTP 202; metadata HTTP 418 |
| 2024 | MAIN | VERIFIED | `MSU-MODELS-2024-MAIN` | COMPLETE | 27 | 27 | 0 | Validated positive control |
| 2024 | COMPANION | VERIFIED | `MSU-MODELS-2024-COMPANION` | BLOCKED | 0 | 0 | 0 | ACM HTTP 403; controlled evidence requested |
| 2025 | MAIN | BLOCKED | — | BLOCKED | n/a | n/a | 0 | Official complete publisher locator not established |
| 2025 | COMPANION | BLOCKED | — | BLOCKED | n/a | n/a | 0 | Official complete publisher locator not established |
| 2026 | MAIN | NOT_YET_PUBLISHED | — | NOT_STARTED | n/a | n/a | 0 | Official event is forthcoming; no published identity established |
| 2026 | COMPANION | NOT_YET_PUBLISHED | — | NOT_STARTED | n/a | n/a | 0 | Official event is forthcoming; no published identity established |

## Required controlled evidence

- MODELS 2022 Main: complete ACM TOC HTML and publisher-generated BibTeX (or complete RIS/CSV).
- MODELS 2022 Companion: complete ACM TOC HTML and publisher-generated BibTeX (or complete RIS/CSV).
- MODELS 2023 Companion: complete IEEE conference-publication TOC HTML and complete publisher CSV/RIS.
- MODELS 2024 Companion: complete ACM TOC HTML and publisher-generated BibTeX (or complete RIS/CSV).

For 2023 Main and both 2025 pairs, official volume-level identity evidence is required before a controlled-evidence destination or unit can be assigned; see [uninstantiated_pair_evidence_requirements.md](uninstantiated_pair_evidence_requirements.md).

No raw inventory could be assessed for material conflicts in blocked/uninstantiated pairs. `MaterialInventoryConflictCount=0` means that no material conflict was observed in the one completed unit; it does not claim reconciliation of blocked pairs.
