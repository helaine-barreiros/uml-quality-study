# Amendment A002 — two-wave documentary collection and discovery gate

- AmendmentID: `A002`
- DecisionDate: `2026-08-12`
- RecordedAt: `2026-08-12T22:16:05Z`
- Stage: Before continuation of manual documentary collection and before any manual discovery classification
- Status: `Applied`
- RecordedCommit: `e4807d849623a9648e1d10993ca3d4b34c1ea4a9`
- NextPlannedCollectionUnit: `MSU-MODELS-2024-COMPANION`
- RevisionID: `A002-R1`
- RevisionDecisionDate: `2026-08-13`
- RevisionRecordedAt: `2026-08-13T14:36:41Z`
- RevisionStatus: `Applied`
- RevisionRecordedCommit: `8183e161db59a66e53837be290b1836a89834888`
- RevisionRationale: Resolve the circular dependency between conditional-venue activation and the deferral of discovery and snowballing.

## Revised methodological sequence

The review adopts the following two-wave architecture:

```text
PRE-DISCOVERY DOCUMENTARY COLLECTION WAVE
-> PRE_DISCOVERY_COLLECTION_CLOSED
-> manual discovery classification
-> candidate consolidation and deduplication
-> formal Layer 1 screening
-> post-screening conditional-venue trigger review
-> backward and forward snowballing
-> FINAL SEARCH UPDATE WAVE
-> discovery and screening of newly identified records
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

## Final search update wave

After screening and snowballing, all conditional venues are reviewed again using, when available:

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

## Final closure criteria

`FINAL_SEARCH_UPDATE_COMPLETE` may be declared only when:

- the final automated-search update has been executed;
- snowballing has reached saturation as defined in protocol v1.7;
- every post-screening conditional trigger has been evaluated;
- every venue activated in the second wave has been collected;
- every new record has passed through discovery and screening;
- no conditional trigger remains pending;
- every material documentary conflict has been resolved;
- the final search date has been recorded;
- the candidate corpus and included corpus have been consolidated and deduplicated.

Final synthesis cannot begin before this milestone.

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

A002-R1 does not change:

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

`RecordedCommit` identifies the commit that introduced A002 before continuation of manual documentary collection and before any manual discovery classification. `RevisionRecordedCommit` identifies the commit that introduced the two-wave A002-R1 architecture before continuation of manual collection and before any discovery.
