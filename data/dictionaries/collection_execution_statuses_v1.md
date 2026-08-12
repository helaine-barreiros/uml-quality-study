# Collection execution statuses v1

- CollectionExecutionStatusSchema: `1`

## UnitStatus

The existing global states are `PENDING`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`. `COMPLETE` continues to require every protocol v1.7 completion condition, including discovery, candidate and discovery-status counts, source preservation, conflict reconciliation, and full auditability.

## DocumentaryCollectionStatus

Allowed values are `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

`COMPLETE` requires an established `PRIMARY_TOC`, a registered source manifest, a complete raw inventory, completed documentary reconciliation, resolution of all material conflicts, and a materialized and audited normalized inventory.

## Component status

`PrimaryTOCStatus`, `RawInventoryStatus`, `ReconciliationStatus`, and `NormalizationStatus` use `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, and `NOT_APPLICABLE`.

## DiscoveryPhaseStatus

Allowed values are `NOT_STARTED`, `DEFERRED_BY_A002`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

`DEFERRED_BY_A002` means: Discovery is intentionally prohibited while the documentary-collection gate remains closed.

## ActivationStatus

Allowed values are `ACTIVE`, `PENDING_TRIGGER_REVIEW`, `ACTIVATED`, and `NOT_ACTIVATED`.

## UnitInstantiationStatus

Allowed values are `NOT_STARTED`, `PARTIAL`, `COMPLETE`, and `PENDING_SCOPE_RESOLUTION`.

## Information-source execution statuses

Information-source execution uses `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, `VALIDATED`, `NOT_FORMALLY_RECORDED`, `DECISION_PENDING`, `DEFERRED_PROTOCOL_SEQUENCE`, and `NOT_APPLICABLE` where applicable. `VALIDATED` denotes validation of a source-specific strategy and does not mean that its production search was executed.
