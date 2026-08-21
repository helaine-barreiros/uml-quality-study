# NLBSE 2024 reconciliation report

## Unit and documentary status

- ManualSearchUnitID: `MSU-NLBSE-2024`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`

## Controlled sources

- PRIMARY_TOC: `SRC-NLBSE-2024-PUBLISHER-TOC-HUMAN-20260815` (`a3d19db19a2adc6548340938972cab6ac83a36d696464351010a9f9c2880f66b`)
- METADATA_SOURCE: `SRC-NLBSE-2024-PUBLISHER-BIBTEX-HUMAN-20260815` (`a5875e5cef8e612575462ffc66494558721900222214c989098a306d0077f7ed`)
- VENUE_CROSSCHECK: not received (`REQUIRED`)

## Level 1 — PRIMARY_TOC × METADATA_SOURCE

- ReconciliationStatus: `COMPLETE`
- PrimaryTotalItems: `17`
- PrimaryResearchItems: `16`
- PrimaryEditorialItems: `1`
- MetadataExportRecordCount: `16`
- DOIExactMatchCount: `16` (`DOIComparisonStatus=OBSERVED_WHERE_REPORTED_IN_PRIMARY_TOC`)
- LiteralTitleMatchCount: `15`
- NormalizedTitleMatchCount: `1`
- TitleVersionDriftCount: `0`
- AuthorListDriftCount: `2`
- PrimaryOnlyCount: `0`
- MetadataOnlyCount: `0`
- AmbiguousMatchCount: `0`
- MaterialInventoryConflictCount: `0`

All 16 publisher research items match exactly one publisher BibTeX record by DOI. The front-matter member is legitimately present only in the PRIMARY_TOC and remains without `MetadataSourceID`. The membership-defining TOC order controls ordinals. Non-literal title representations and author-list display differences are preserved diagnostically and are not silently corrected.

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
