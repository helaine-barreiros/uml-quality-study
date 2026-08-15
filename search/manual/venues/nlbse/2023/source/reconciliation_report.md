# NLBSE 2023 reconciliation report

## Unit and documentary status

- ManualSearchUnitID: `MSU-NLBSE-2023`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`

## Controlled sources

- PRIMARY_TOC: `SRC-NLBSE-2023-PUBLISHER-TOC-HUMAN-20260815` (`98ddf02568836f53e91b742ad0810f132fe7cd2dd630c8fc32be90a9f57c79fe`)
- METADATA_SOURCE: `SRC-NLBSE-2023-PUBLISHER-BIBTEX-HUMAN-20260815` (`6eab8834b30df0ba6982396f22558b81c1d1228e1f22153c193827e568efdc49`)
- VENUE_CROSSCHECK: not received (`REQUIRED`)

## Level 1 — PRIMARY_TOC × METADATA_SOURCE

- ReconciliationStatus: `COMPLETE`
- PrimaryTotalItems: `20`
- PrimaryResearchItems: `20`
- PrimaryEditorialItems: `0`
- MetadataExportRecordCount: `20`
- DOIExactMatchCount: `0` (`DOIComparisonStatus=NOT_OBSERVABLE_IN_PRIMARY_TOC`)
- LiteralTitleMatchCount: `19`
- NormalizedTitleMatchCount: `1`
- TitleVersionDriftCount: `0`
- AuthorListDriftCount: `0`
- PrimaryOnlyCount: `0`
- MetadataOnlyCount: `0`
- AmbiguousMatchCount: `0`
- MaterialInventoryConflictCount: `0`

All publisher TOC items match exactly one publisher BibTeX record. The export order differs from the membership-defining TOC order and was not used for ordinals. Non-literal title representations and author-list display differences are preserved diagnostically and are not silently corrected.

## Level 2 — PRIMARY_TOC × VENUE_CROSSCHECK

- ReconciliationStatus: `BLOCKED`
- VenueCrosscheckStatus: `REQUIRED`
- VenueCrosscheckItemCount: `0`
- CrosscheckOnlyCount: `0` (not evaluated because the source is absent)

The missing independent official venue crosscheck is a process blocker, not a material inventory conflict by itself.

## Level 3 — documentary completion

- DocumentaryCollectionStatus: `BLOCKED`
- RawInventoryStatus: `COMPLETE`
- NormalizationStatus: `COMPLETE`
- ReconciliationStatus: `BLOCKED`
- DiscoveryDataRows: `0`

Complete official publisher `PRIMARY_TOC` evidence is sufficient to materialize raw membership, and validated publisher BibTeX is sufficient to populate matched normalized metadata. Documentary completion remains blocked until an independent official venue crosscheck is acquired and reconciled, or a later explicit methodological decision justifies its absence.
