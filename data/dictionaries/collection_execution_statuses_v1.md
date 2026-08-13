# Collection execution statuses v1

- CollectionExecutionStatusSchema: `1`

## UnitStatus

The existing global unit states are `PENDING`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`. `COMPLETE` continues to require every protocol v1.7 completion condition, including discovery, candidate and discovery-status counts, source preservation, conflict reconciliation, and full auditability.

## DocumentaryCollectionStatus

Allowed values are `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

`COMPLETE` requires an established `PRIMARY_TOC`, a registered source manifest, a complete raw inventory, completed documentary reconciliation, resolution of all material conflicts, and a materialized and audited normalized inventory.

## Component status

`PrimaryTOCStatus`, `RawInventoryStatus`, `ReconciliationStatus`, and `NormalizationStatus` use `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, and `NOT_APPLICABLE`.

## DiscoveryPhaseStatus

Allowed values are `NOT_STARTED`, `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

`DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED` means: Discovery is intentionally prohibited until the pre-discovery documentary collection wave has been formally closed by an auditable decision.

## GlobalCollectionPhase

Allowed values are `PRE_DISCOVERY_DOCUMENTARY_COLLECTION`, `DISCOVERY_AND_SCREENING`, `FINAL_SEARCH_UPDATE`, and `CLOSED`.

## PreDiscoveryCollectionStatus

Allowed values are `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

## PreDiscoveryClosureStatus

Allowed values are `NOT_READY`, `READY_FOR_DECISION`, `CLOSED`, and `BLOCKED`.

## PostScreeningTriggerReviewStatus

Allowed values are `DEFERRED_PROTOCOL_SEQUENCE`, `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

Review starts only after initial screening and the first snowballing cycle. It may be reopened during `FINAL_SEARCH_UPDATE`. `COMPLETE` means only that all evidence available in the current iteration was evaluated; new evidence may return it to `IN_PROGRESS`.

## FinalSearchUpdateStatus

Allowed values are `DEFERRED_PROTOCOL_SEQUENCE`, `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.

## FinalUpdateIterationStatus

Allowed values are `NOT_STARTED`, `IN_PROGRESS`, `STABLE`, `REOPENED`, and `BLOCKED`.

`STABLE` means: A complete final-update iteration produced no new eligible primary study, no new conditional-venue activation, no pending conditional trigger, no pending citation record, and no unresolved material documentary conflict.

`REOPENED` means: A previously completed iteration was reopened because new evidence, a newly included Layer 1 study, a new citation record, or a newly activated conditional venue required further identification work.

## FinalSearchClosureStatus

Allowed values are `NOT_READY`, `READY_FOR_DECISION`, `CLOSED`, and `BLOCKED`.

`CLOSED` may be assigned only by an auditable human decision after a `STABLE` iteration.

## RequirementStatus

Allowed values are `REQUIRED`, `DECISION_REQUIRED`, `CONDITIONAL_IF_RETAINED`, `REQUIRED_FOR_SNOWBALLING`, and `NOT_APPLICABLE`.

## DecisionStatus

The values used by `information_source_execution_log.csv` are `RETAINED_CORE`, `RETAINED_COMPLEMENTARY`, `PROVISIONAL_DECISION_PENDING`, `CITATION_DISCOVERY_ONLY`, `COVERAGE_VALIDATION`, and `COMPLEMENTARY_SEARCH`.

## TriggerReviewStatus

Allowed values are `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, and `DEFERRED_PROTOCOL_SEQUENCE`.

## ConditionalActivationDecision

Allowed values are `PENDING_TRIGGER_REVIEW`, `ACTIVATED`, and `NOT_ACTIVATED`.

## ActivationStatus

Allowed values are `ACTIVE`, `PENDING_TRIGGER_REVIEW`, `ACTIVATED`, and `NOT_ACTIVATED`.

## UnitInstantiationStatus

Allowed values are `NOT_STARTED`, `PARTIAL`, `COMPLETE`, and `PENDING_SCOPE_RESOLUTION`.

## Information-source execution statuses

Information-source execution uses `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, `VALIDATED`, `NOT_FORMALLY_RECORDED`, `DECISION_PENDING`, `DEFERRED_PROTOCOL_SEQUENCE`, and `NOT_APPLICABLE` where applicable. `VALIDATED` denotes validation of a source-specific strategy and does not mean that its production search was executed.
