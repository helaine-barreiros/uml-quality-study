# NLBSE 2025 reconciliation report

## Unit and documentary status

- ManualSearchUnitID: `MSU-NLBSE-2025`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`

## Controlled sources

- PRIMARY_TOC: `SRC-NLBSE-2025-PUBLISHER-TOC-HUMAN-20260815` (`26596910e8cd5114f6b4cb259b4fafc87bd90858ba5dfcf1f497e083980cfd48`)
- METADATA_SOURCE: `SRC-NLBSE-2025-PUBLISHER-BIBTEX-HUMAN-20260815` (`5c612c3ab0fcaa29c3e6e0aed799110f30c83184dbb01792f5fdaad5624b9ba1`)
- VENUE_CROSSCHECK: not received (`REQUIRED`)

## Level 1 — PRIMARY_TOC × METADATA_SOURCE

- ReconciliationStatus: `COMPLETE`
- PrimaryTotalItems: `18`
- PrimaryResearchItems: `18`
- PrimaryEditorialItems: `0`
- MetadataExportRecordCount: `18`
- DOIExactMatchCount: `0` (`DOIComparisonStatus=NOT_OBSERVABLE_IN_PRIMARY_TOC`)
- LiteralTitleMatchCount: `17`
- NormalizedTitleMatchCount: `1`
- TitleVersionDriftCount: `0`
- AuthorListDriftCount: `0`
- PrimaryOnlyCount: `0`
- MetadataOnlyCount: `0`
- AmbiguousMatchCount: `0`
- MaterialInventoryConflictCount: `0`

All publisher TOC items match exactly one publisher BibTeX record. The complete normalized title sequence is equal, but only the membership-defining TOC controls ordinals. Non-literal title representations and author-list display differences are preserved diagnostically and are not silently corrected.

One displayed title occurs twice in both complete sequences and represents two records with distinct DOI values. Equal complete title sequence plus occurrence ordinal disambiguated the pair without merging or externally correcting either record.

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
