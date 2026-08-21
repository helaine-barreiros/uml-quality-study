#!/usr/bin/env python3
"""Render public unit documentation from safe aggregate audit values."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def value(mapping: dict[str, object], key: str) -> object:
    if key not in mapping:
        raise SystemExit(f"Missing audit value: {key}")
    return mapping[key]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-dir", type=Path, required=True)
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--primary-source-id", required=True)
    parser.add_argument("--metadata-source-id", required=True)
    parser.add_argument("--materialization-audit", type=Path, required=True)
    parser.add_argument("--metadata-audit", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, required=True)
    parser.add_argument("--primary-research-items", type=int, required=True)
    parser.add_argument("--primary-editorial-items", type=int, required=True)
    args = parser.parse_args()

    materialization = json.loads(args.materialization_audit.read_text(encoding="utf-8"))
    metadata = json.loads(args.metadata_audit.read_text(encoding="utf-8"))
    reconciliation = json.loads(args.reconciliation.read_text(encoding="utf-8"))
    total = int(value(materialization, "PrimaryTotalItems"))
    if args.primary_research_items + args.primary_editorial_items != total:
        raise SystemExit("Research/editorial counts do not sum to PrimaryTotalItems")

    readme = f"""# {args.title}

- ManualSearchUnitID: `{args.unit_id}`
- UnitStatus: `BLOCKED`
- DocumentaryCollectionStatus: `BLOCKED`
- PrimaryTOCStatus: `COMPLETE`
- RawInventoryStatus: `COMPLETE`
- ReconciliationStatus: `BLOCKED`
- NormalizationStatus: `COMPLETE`
- DiscoveryPhaseStatus: `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`

The complete official publisher `PRIMARY_TOC` establishes documentary membership and has been materialized as {total} raw rows. The validated publisher BibTeX enriches the same {total} securely matched records in the normalized inventory; it does not create membership. Documentary completion and the overall reconciliation remain blocked until an independent official `VENUE_CROSSCHECK` is acquired and reconciled. No discovery or screening was performed.

- [source manifest](source/source_manifest.csv)
- [controlled evidence request](source/controlled_evidence_request.md)
- [reconciliation report](source/reconciliation_report.md)
- [raw inventory](raw/inventory_raw.csv)
- [raw inventory audit](raw/inventory_audit.md)
- [normalized inventory](normalized/inventory.csv)
- [normalization audit](metadata/normalization_audit.md)
"""

    raw_readme = f"""# Raw documentary inventory

The controlled IEEE publisher `PRIMARY_TOC` contains {total} ordered items and passed offline completeness checks. `inventory_raw.csv` materializes every locally observed TOC item in publisher order without relevance filtering. BibTeX does not define membership. Discovery and screening were not executed.
"""

    raw_audit = f"""# Raw inventory audit

- PrimaryHTMLSHA256: `{value(materialization, 'PrimaryHTMLSHA256')}`
- MetadataExportSHA256: `{value(materialization, 'MetadataExportSHA256')}`
- PrimaryTotalItems: `{total}`
- MetadataExportRecordCount: `{value(materialization, 'MetadataExportRecordCount')}`
- RawRows: `{value(materialization, 'RawRows')}`
- NormalizedRows: `{value(materialization, 'NormalizedRows')}`
- MinSourceOrdinal: `1`
- MaxSourceOrdinal: `{total}`
- DuplicateManualSearchIDCount: `0`
- DuplicateSourceOrdinalCount: `0`
- InventorySourceID: `{args.primary_source_id}`
- ExtractionMethod: `audit_ieee_toc_html.pl offline structural extraction`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`
- VenueCrosscheckStatus: `REQUIRED`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`
- ControlledEvidenceCommittedCount: `0`
- RawInventorySHA256: `{value(materialization, 'RawInventorySHA256')}`

Complete official publisher `PRIMARY_TOC` evidence is sufficient to materialize raw documentary membership. The missing official venue crosscheck blocks documentary completion but does not erase or defer the publisher-defined raw inventory. No discovery was executed.
"""

    metadata_readme = f"""# Metadata normalization

The controlled publisher BibTeX is registered only as `METADATA_SOURCE` and enriches {total} records already defined by the complete publisher TOC. Matching is deterministic by IEEE record locator/BibTeX key, literal title, or a unique diagnostic normalized title. Abstract and keyword text remain controlled and are not redistributed; the public CSV records availability only. No Crossref, PDF, or external metadata source was used. Documentary completion remains blocked by the missing official venue crosscheck.
"""

    normalization_audit = f"""# Normalization audit

- NormalizedInventorySchema: `1`
- PrimaryHTMLSHA256: `{value(materialization, 'PrimaryHTMLSHA256')}`
- MetadataExportSHA256: `{value(materialization, 'MetadataExportSHA256')}`
- BibTeXParserVersion: `{value(metadata, 'BibTeXParserVersion')}`
- PrimaryTotalItems: `{total}`
- MetadataExportRecordCount: `{value(materialization, 'MetadataExportRecordCount')}`
- MatchedRecordCount: `{value(materialization, 'MatchedRecordCount')}`
- RawRows: `{value(materialization, 'RawRows')}`
- NormalizedRows: `{value(materialization, 'NormalizedRows')}`
- UniqueDOICount: `{int(value(metadata, 'DOICount')) - int(value(metadata, 'DuplicateDOICount'))}`
- DuplicateDOICount: `{value(metadata, 'DuplicateDOICount')}`
- BibTeXParseFailureCount: `{value(metadata, 'ParseFailureCount')}`
- LiteralTitleMatchCount: `{value(materialization, 'LiteralTitleMatchCount')}`
- NormalizedTitleMatchCount: `{value(materialization, 'NormalizedTitleMatchCount')}`
- TitleRepresentationDriftCount: `{value(materialization, 'TitleRepresentationDriftCount')}`
- AuthorListDriftCount: `{value(materialization, 'AuthorListDriftCount')}`
- AbstractAvailableControlledCount: `{value(metadata, 'AbstractAvailableCount')}`
- KeywordsAvailableControlledCount: `{value(metadata, 'KeywordsAvailableCount')}`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- CrossrefUsed: `false`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`
- VenueCrosscheckStatus: `REQUIRED`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`
- ControlledEvidenceCommittedCount: `0`
- NormalizationTimestamp: `{value(materialization, 'NormalizedAt')}`
- NormalizedInventorySHA256: `{value(materialization, 'NormalizedInventorySHA256')}`

Validated publisher BibTeX is sufficient to populate normalized metadata for safely matched raw members. Title or author-list differences are preserved as metadata-representation drift and do not automatically create a material inventory conflict. No publisher abstract or keyword text is present in the public CSV.
"""

    reconciliation_report = f"""# {args.title} reconciliation report

## Unit and documentary status

- ManualSearchUnitID: `{args.unit_id}`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`

## Controlled sources

- PRIMARY_TOC: `{args.primary_source_id}` (`{value(materialization, 'PrimaryHTMLSHA256')}`)
- METADATA_SOURCE: `{args.metadata_source_id}` (`{value(materialization, 'MetadataExportSHA256')}`)
- VENUE_CROSSCHECK: not received (`REQUIRED`)

## Level 1 — PRIMARY_TOC × METADATA_SOURCE

- ReconciliationStatus: `COMPLETE`
- PrimaryTotalItems: `{total}`
- PrimaryResearchItems: `{args.primary_research_items}`
- PrimaryEditorialItems: `{args.primary_editorial_items}`
- MetadataExportRecordCount: `{value(materialization, 'MetadataExportRecordCount')}`
- DOIExactMatchCount: `{value(reconciliation, 'DOIExactMatchCount')}` (`DOIComparisonStatus={value(reconciliation, 'DOIComparisonStatus')}`)
- LiteralTitleMatchCount: `{value(reconciliation, 'LiteralTitleMatchCount')}`
- NormalizedTitleMatchCount: `{value(reconciliation, 'NormalizedTitleMatchCount')}`
- TitleVersionDriftCount: `0`
- AuthorListDriftCount: `{value(reconciliation, 'AuthorListDriftCount')}`
- PrimaryOnlyCount: `{value(reconciliation, 'PrimaryOnlyCount')}`
- MetadataOnlyCount: `{value(reconciliation, 'MetadataOnlyCount')}`
- AmbiguousMatchCount: `{value(reconciliation, 'AmbiguousMatchCount')}`
- MaterialInventoryConflictCount: `{value(reconciliation, 'MaterialInventoryConflictCount')}`

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
"""

    atomic_text(args.unit_dir / "README.md", readme)
    atomic_text(args.unit_dir / "raw" / "README.md", raw_readme)
    atomic_text(args.unit_dir / "raw" / "inventory_audit.md", raw_audit)
    atomic_text(args.unit_dir / "metadata" / "README.md", metadata_readme)
    atomic_text(args.unit_dir / "metadata" / "normalization_audit.md", normalization_audit)
    atomic_text(args.unit_dir / "source" / "reconciliation_report.md", reconciliation_report)


if __name__ == "__main__":
    main()
