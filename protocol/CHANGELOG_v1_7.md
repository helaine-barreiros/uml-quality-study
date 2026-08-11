# Protocol v1.7 changelog

Date: 2026-08-11

## Manual-search provenance and auditability
- Defined four source roles: `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE`, and `AUXILIARY_NAVIGATION`.
- Established `PRIMARY_TOC` as the source that defines initial documentary membership of each manual-search unit.
- Formalized the provenance chain:
  `PRIMARY_TOC/source evidence -> source_manifest.csv -> raw/inventory_raw.csv -> normalized/inventory.csv -> screening/discovery.csv`.
- Added source-manifest requirements including retrieval timestamp, permissible local snapshot, SHA-256, content type, and notes.
- Formalized an immutable raw documentary inventory containing every item in the documentary universe before relevance decisions.
- Moved assignment of `ManualSearchID` to raw-inventory materialization and required stable propagation across normalized, discovery, and screening layers.
- Restricted metadata services such as Crossref to enrichment of already identified records; they do not silently redefine documentary membership.
- Added explicit `InventoryConflict` handling for discrepancies revealed by cross-check or metadata sources.
- Strengthened unit states to `PENDING`, `IN_PROGRESS`, `COMPLETE`, and `BLOCKED`.
- Strengthened `COMPLETE` so unresolved material inventory conflicts prevent unit completion.
- Expanded manual-search audit outputs to include source manifests, raw inventories, normalized inventories, discovery logs, candidate sets, and coverage comparisons.
- Strengthened licensing guidance for snapshots, licensed database exports, publisher pages, and copyrighted full text.
- Clarified the distinction between controlled preservation of licensed raw search exports and their conditional redistribution in the public replication package.
- Corrected the protocol-validation checklist numbering and added a dedicated provenance-chain validation item.
- No change was made to research questions, eligibility criteria, analytical layers, or the final review interval.

## References
No new bibliography entry was required. The new provenance controls cite PRISMA-S (Rethlefsen et al., 2021) and Petersen et al. (2015), both already present in the protocol bibliography.
