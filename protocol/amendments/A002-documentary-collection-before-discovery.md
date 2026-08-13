# Amendment A002 — two-wave documentary collection and discovery gate

- AmendmentID: `A002`
- DecisionDate: `2026-08-12`
- RecordedAt: `2026-08-12T22:16:05Z`
- Stage: Before continuation of manual documentary collection and before any manual discovery classification
- Status: `Applied`
- RecordedCommit: `e4807d849623a9648e1d10993ca3d4b34c1ea4a9`
- NextPlannedCollectionUnit: `MSU-MODELS-2024-COMPANION`
## Revision history

### A002-R1

- RevisionID: `A002-R1`
- RevisionDecisionDate: `2026-08-13`
- RevisionRecordedAt: `2026-08-13T14:36:41Z`
- RevisionStatus: `Applied`
- RevisionRecordedCommit: `8183e161db59a66e53837be290b1836a89834888`
- RevisionRationale: Resolve the circular dependency between conditional-venue activation and the deferral of discovery and snowballing.

### A002-R2

- RevisionID: `A002-R2`
- RevisionDecisionDate: `2026-08-13`
- RevisionRecordedAt: `2026-08-13T17:46:58Z`
- RevisionStatus: `Applied`
- RevisionRecordedCommit:
- RevisionRationale: Correct the temporal ordering of snowballing and conditional-venue trigger review, and formalize fixed-point closure of the final search update.

## Revised methodological sequence

The review adopts the following two-wave architecture:

```text
PRE-DISCOVERY DOCUMENTARY COLLECTION WAVE
-> PRE_DISCOVERY_COLLECTION_CLOSED
-> manual discovery classification
-> candidate consolidation and deduplication
-> formal Layer 1 screening of the initial corpus
-> backward and forward snowballing
-> discovery and formal screening of records identified by snowballing
-> post-screening and snowballing conditional-venue trigger review
-> documentary collection of newly activated venues
-> discovery and formal screening of records from newly activated venues
-> iterative final search update
-> FIXED_POINT_SEARCH_CLOSURE
-> FINAL_SEARCH_UPDATE_COMPLETE
-> final synthesis
```

`PRE_DISCOVERY_COLLECTION_CLOSED` and `FINAL_SEARCH_UPDATE_COMPLETE` are global process milestones, not `UnitStatus` values.

## Pre-discovery documentary collection wave

The first wave includes:

1. execution and formal recording of the production automated searches required to compose the initial corpus;
2. a formal decision to retain or exclude ScienceDirect under the rule already defined in protocol v1.7;
3. documentary collection for all applicable core venues published by the formal first-wave closure decision;
4. documentary collection for conditional venues activated before discovery by a relevant seed not retrieved by the core automated sources, evidence from production automated-search results, or a documented coverage-risk decision available before discovery;
5. materialization of the complete documentary pipeline for each included manual unit:

```text
PRIMARY_TOC
-> source_manifest.csv
-> raw/inventory_raw.csv
-> documentary reconciliation
-> normalized/inventory.csv
-> normalization audit
```

6. resolution of all material `InventoryConflict` cases in units included in the first wave.

Proceedings or issues not yet published at first-wave closure may remain explicitly pending and must be revisited during the final search update.

## Pre-discovery closure criteria

`PRE_DISCOVERY_COLLECTION_CLOSED` may be declared only by a later auditable decision when:

- every mandatory first-wave automated source has a formally recorded production execution;
- the ScienceDirect decision has been resolved;
- all applicable core venues available by the closure date have materialized documentary units;
- every conditional trigger available before discovery has been evaluated;
- every conditional venue activated during that review has been collected;
- every material documentary conflict has been resolved;
- the global source, venue, and unit registers are current;
- no unit required for the first wave remains `PENDING`, `BLOCKED`, or `IN_PROGRESS` without documented justification.

The decision date becomes the operational cutoff for the first wave. No closure date is assigned by A002-R1.

## Discovery and screening after first-wave closure

Only after `PRE_DISCOVERY_COLLECTION_CLOSED` may manual discovery classification, candidate consolidation, deduplication, and formal Layer 1 screening begin. Manual discovery remains separate from formal screening.

## Iterative final search update wave

Post-screening trigger review starts after initial Layer 1 screening and backward and forward snowballing. Snowballing may provide evidence that activates conditional venues. A newly activated venue may add Layer 1 studies, and each new Layer 1 study may expose additional references or citations. Snowballing and conditional-trigger review may therefore be reopened. The second wave is an iterative cycle rather than a sequence executed only once.

All conditional venues are reviewed using, when available:

- pilot-screening evidence;
- production-screening evidence;
- studies included in Layer 1;
- backward snowballing;
- forward snowballing;
- indexing or coverage gaps identified during execution;
- a documented methodological coverage-risk decision.

When a new trigger is satisfied, the transition is:

```text
ActivationStatus=PENDING_TRIGGER_REVIEW
-> ACTIVATED
```

Documentary collection is then reopened for the corresponding venue. Every newly identified record must pass through:

```text
source provenance
-> raw inventory
-> reconciliation
-> normalized inventory
-> discovery
-> candidate consolidation
-> formal screening
```

before synthesis.

### Final search update iteration

Each iteration performs:

1. execute the final or incremental update of retained automated sources;
2. identify and normalize new records;
3. apply discovery and formal screening to new records;
4. update the Layer 1 corpus;
5. execute backward and forward snowballing from newly included Layer 1 studies;
6. apply discovery and formal screening to records identified by snowballing;
7. review conditional-venue triggers using all currently available evidence;
8. collect documentary units for newly activated venues;
9. apply discovery and formal screening to records from newly activated venues;
10. update the Layer 1 corpus again;
11. determine whether another iteration is required.

Another iteration is mandatory whenever at least one condition holds:

```text
NewEligiblePrimaryStudyCount > 0
NewConditionalVenueActivationCount > 0
PendingConditionalTriggerCount > 0
PendingCitationRecordCount > 0
UnresolvedMaterialInventoryConflictCount > 0
```

### Fixed-point search closure

`FIXED_POINT_SEARCH_CLOSURE` is reached only when one complete iteration simultaneously produces:

```text
NewEligiblePrimaryStudyCount = 0
NewConditionalVenueActivationCount = 0
PendingConditionalTriggerCount = 0
PendingCitationRecordCount = 0
UnresolvedMaterialInventoryConflictCount = 0
```

An iteration without a new study is not stable while a trigger remains pending. An iteration without a new trigger is not stable while citation records remain pending. An iteration without new records is not stable while a material documentary conflict remains unresolved. Final closure requires the conjunction of all conditions. This fixed point is an operational closure criterion, not a claim of absolute exhaustiveness of the literature.

## Final closure criteria

`FINAL_SEARCH_UPDATE_COMPLETE` may be declared only when:

- every retained automated source has received its final update;
- snowballing has reached a stable iteration under protocol v1.7;
- every identified record has been screened;
- every conditional trigger has been evaluated;
- every activated venue has been collected;
- every record from those venues has passed through discovery and screening;
- snowballing has been reexecuted whenever new Layer 1 studies were incorporated;
- `PendingConditionalTriggerCount = 0`;
- `PendingCitationRecordCount = 0`;
- `UnresolvedMaterialInventoryConflictCount = 0`;
- a complete iteration has produced `NewEligiblePrimaryStudyCount = 0` and `NewConditionalVenueActivationCount = 0`;
- the global registers have been updated;
- the final search date has been recorded;
- the candidate corpus and included corpus have been consolidated and deduplicated.

Final synthesis cannot begin before `FinalSearchClosureStatus=CLOSED`.

## Preserved operational consequences

1. `DocumentaryCollectionStatus=COMPLETE` is not equivalent to `UnitStatus=COMPLETE`.
2. A documentary unit may remain `IN_PROGRESS` after collection because discovery has not been executed.
3. Global unit states remain only `PENDING`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.
4. Neither `PRE_DISCOVERY_COLLECTION_CLOSED` nor `FINAL_SEARCH_UPDATE_COMPLETE` is a `UnitStatus`.
5. `CandidateCount`, `ClearNonCandidateCount`, and `NonResearchItemCount` remain empty before discovery.
6. No item receives `CLEAR-CANDIDATE`, `POSSIBLE-CANDIDATE`, `CLEAR-NON-CANDIDATE`, or `NON-RESEARCH-ITEM` while discovery is deferred.
7. No dual-review or adjudication infrastructure is operationalized by this amendment.
8. Formal screening remains methodologically separate from manual discovery.

## Scope not changed

A002-R2 does not change:

- research questions;
- review objective;
- the interval from 2022 to the final search date;
- eligibility criteria;
- Layer 1 or Layer 2 definitions;
- validated strings;
- the planned information-source set;
- core venues;
- conditional venues;
- conditional-venue activation rules;
- snowballing rules;
- final-update rules;
- synthesis strategy;
- previously established documentary membership;
- existing raw or normalized data;
- the schema defined by A001.

## Current state: MODELS 2024 Main

- ManualSearchUnitID: `MSU-MODELS-2024-MAIN`
- UnitStatus: `IN_PROGRESS`
- DocumentaryCollectionStatus: `COMPLETE`
- PrimaryTOCStatus: `COMPLETE`
- RawInventoryStatus: `COMPLETE`
- ReconciliationStatus: `COMPLETE`
- NormalizationStatus: `COMPLETE`
- DiscoveryPhaseStatus: `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`

The documentary universe, raw inventory, reconciliation, and normalized inventory are complete, but discovery classification has not started.

## Next planned unit

- ManualSearchUnitID: `MSU-MODELS-2024-COMPANION`
- UnitStatus: `PENDING`
- DocumentaryCollectionStatus: `NOT_STARTED`
- DiscoveryPhaseStatus: `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`

Proceedings identity and authoritative sources will be established only during the unit-specific execution.

## Provenance

`RecordedCommit` identifies the commit that introduced A002 before continuation of manual documentary collection and before any manual discovery classification. The A002-R1 `RevisionRecordedCommit` identifies the commit that introduced the two-wave architecture. The A002-R2 `RevisionRecordedCommit` will identify the commit that corrects the ordering of snowballing and trigger review and introduces fixed-point closure before any execution of those stages.
