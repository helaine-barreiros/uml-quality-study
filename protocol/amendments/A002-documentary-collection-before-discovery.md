# Amendment A002 — documentary collection before discovery

- AmendmentID: `A002`
- DecisionDate: `2026-08-12`
- RecordedAt: `2026-08-12T22:16:05Z`
- Stage: Before continuation of manual documentary collection and before any manual discovery classification
- Status: `Applied`
- RecordedCommit:
- NextPlannedCollectionUnit: `MSU-MODELS-2024-COMPANION`

## Methodological decision

The review adopts the following operational gate:

```text
manual documentary collection
-> documentary collection closure
-> manual discovery classification
-> candidate consolidation and deduplication
-> formal Layer 1 screening
```

For the planned manual units, `manual documentary collection` comprises:

```text
PRIMARY_TOC
-> source_manifest.csv
-> raw/inventory_raw.csv
-> documentary reconciliation
-> normalized/inventory.csv
-> normalization audit
```

Manual discovery classification remains deferred until manual-search documentary collection is formally declared closed by a later auditable decision. Execution may continue unit by unit and in operational batches, but discovery classification must not occur between units while this gate remains closed.

## Operational consequences

1. `DocumentaryCollectionStatus=COMPLETE` is not equivalent to `UnitStatus=COMPLETE`.
2. A documentary unit may remain `IN_PROGRESS` after collection because discovery has not been executed.
3. Global unit states remain only `PENDING`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.
4. `DOCUMENTARY_COLLECTION_COMPLETE` is not introduced as a new `UnitStatus`.
5. Documentary progress is represented separately by `DocumentaryCollectionStatus`.
6. Discovery progress is represented by `DiscoveryPhaseStatus`.
7. While the gate is closed, `DiscoveryPhaseStatus=DEFERRED_BY_A002`.
8. `CandidateCount`, `ClearNonCandidateCount`, and `NonResearchItemCount` remain empty.
9. No item receives `CLEAR-CANDIDATE`, `POSSIBLE-CANDIDATE`, `CLEAR-NON-CANDIDATE`, or `NON-RESEARCH-ITEM` at this stage.
10. No dual-review or adjudication infrastructure is operationalized now.
11. Formal screening remains methodologically separate from manual discovery.
12. Snowballing is not anticipated by this amendment. Its start set and execution remain as defined in protocol v1.7.
13. Production automated searches, source consolidation, and deduplication remain separate stages and must be formally recorded before screening.

## Scope not changed

A002 does not change:

- research questions;
- review objective;
- the interval from 2022 to the final search date;
- eligibility criteria;
- Layer 1 or Layer 2 definitions;
- validated strings;
- the planned information-source set;
- the core and conditional venue sets;
- conditional-venue activation rules;
- snowballing rules;
- synthesis strategy;
- previously established documentary membership;
- raw or normalized data already produced.

## Current state: MODELS 2024 Main

- ManualSearchUnitID: `MSU-MODELS-2024-MAIN`
- UnitStatus: `IN_PROGRESS`
- DocumentaryCollectionStatus: `COMPLETE`
- PrimaryTOCStatus: `COMPLETE`
- RawInventoryStatus: `COMPLETE`
- ReconciliationStatus: `COMPLETE`
- NormalizationStatus: `COMPLETE`
- DiscoveryPhaseStatus: `DEFERRED_BY_A002`

The documentary universe, raw inventory, reconciliation, and normalized inventory are complete, but discovery classification has not started.

## Next planned unit

- ManualSearchUnitID: `MSU-MODELS-2024-COMPANION`
- UnitStatus: `PENDING`
- DocumentaryCollectionStatus: `NOT_STARTED`
- DiscoveryPhaseStatus: `DEFERRED_BY_A002`

Proceedings identity and authoritative sources will be established only during the unit-specific execution.
