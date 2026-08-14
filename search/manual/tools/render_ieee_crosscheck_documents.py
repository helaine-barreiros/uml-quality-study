#!/usr/bin/env python3
"""Render RE/REW unit documents after offline venue-crosscheck reconciliation."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


def atomic_text(path: Path, content: str) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-dir", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--primary-source-id", required=True)
    parser.add_argument("--metadata-source-id", required=True)
    parser.add_argument("--crosscheck-source-id", required=True)
    parser.add_argument("--materialization-audit", type=Path, required=True)
    parser.add_argument("--metadata-audit", type=Path, required=True)
    parser.add_argument("--publisher-reconciliation", type=Path, required=True)
    parser.add_argument("--crosscheck-audit", type=Path, required=True)
    parser.add_argument("--crosscheck-reconciliation", type=Path, required=True)
    parser.add_argument("--primary-research-items", type=int, required=True)
    parser.add_argument("--primary-editorial-items", type=int, required=True)
    args = parser.parse_args()

    material = load(args.materialization_audit)
    metadata = load(args.metadata_audit)
    publisher = load(args.publisher_reconciliation)
    observed = load(args.crosscheck_audit)
    cross = load(args.crosscheck_reconciliation)
    complete = bool(cross["CrosscheckSufficientForDocumentaryCompletion"])
    unit_status = "IN_PROGRESS" if complete else "BLOCKED"
    doc_status = "COMPLETE" if complete else "BLOCKED"
    reconciliation_status = "COMPLETE" if complete else "BLOCKED"
    blocker = "" if complete else "ITEM_LEVEL_VENUE_CROSSCHECK_REQUIRED"
    total = int(material["RawRows"])
    if args.primary_research_items + args.primary_editorial_items != total:
        raise SystemExit("Research/editorial counts do not sum to raw rows")

    if complete:
        interpretation = (
            "The independent official item-level accepted-paper list covers every publisher research item. "
            "Publisher editorial records are legitimately primary-only, and crosscheck-only records belong to "
            "the broader event accepted-paper scope. The unit remains IN_PROGRESS because discovery is deferred."
        )
        request = f"""# Controlled evidence request — {args.unit_id}

- RequestStatus: `FULFILLED`
- CurrentEvidence: complete official publisher TOC, validated publisher BibTeX, and independent official item-level venue crosscheck
- MissingEvidence: none for documentary collection

The former venue-crosscheck request was fulfilled by controlled evidence recorded as `{args.crosscheck_source_id}`. Discovery remains deferred and no further evidence is requested by this file.
"""
    else:
        interpretation = (
            "The official page confirms the event track or sessions but does not enumerate every publisher research "
            "item. It is retained as a partial venue crosscheck and does not complete documentary reconciliation."
        )
        request = f"""# Controlled evidence request — {args.unit_id}

- CurrentEvidence: complete official publisher TOC, validated publisher BibTeX, and an official partial track/session page (`{args.crosscheck_source_id}`)
- MissingEvidence: complete item-level official venue crosscheck listing all proceedings papers
- ReasonRequired: the received track/session page leaves {cross['CrosscheckPrimaryOnlyCount']} publisher research items without item-level venue confirmation
- PreferredAcquisitionProcedure: save the complete official accepted-papers or detailed program page with all paper lists expanded; do not save cookies, HAR, tokens, credentials, or browser profiles
- ExpectedFilename: `official_item_level_venue_crosscheck.html`
- ExpectedLocalDestination: `.local-evidence/re/{args.unit_dir.parts[-2]}/{args.unit_dir.parts[-1]}/`
- ProhibitedContents: cookies, HAR files, tokens, credentials, browser profiles, session data, or redistributed licensed content

Do not reacquire the publisher TOC, BibTeX, or the partial page already recorded. The required evidence must enumerate the proceedings papers at item level.
"""

    readme = f"""# {args.title}

- ManualSearchUnitID: `{args.unit_id}`
- UnitStatus: `{unit_status}`
- DocumentaryCollectionStatus: `{doc_status}`
- PrimaryTOCStatus: `COMPLETE`
- RawInventoryStatus: `COMPLETE`
- ReconciliationStatus: `{reconciliation_status}`
- NormalizationStatus: `COMPLETE`
- VenueCrosscheckStatus: `{cross['VenueCrosscheckStatus']}`
- DiscoveryPhaseStatus: `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`
- CurrentBlocker: `{blocker}`

The complete publisher TOC defines the {total}-item documentary inventory, and publisher BibTeX supplies matched normalized metadata without defining membership. {interpretation} No discovery or screening was performed.

- [source manifest](source/source_manifest.csv)
- [controlled evidence request](source/controlled_evidence_request.md)
- [reconciliation report](source/reconciliation_report.md)
- [raw inventory](raw/inventory_raw.csv)
- [raw inventory audit](raw/inventory_audit.md)
- [normalized inventory](normalized/inventory.csv)
- [normalization audit](metadata/normalization_audit.md)
"""

    raw_audit = f"""# Raw inventory audit

- PrimaryHTMLSHA256: `{material['PrimaryHTMLSHA256']}`
- MetadataExportSHA256: `{material['MetadataExportSHA256']}`
- VenueCrosscheckSHA256: `{cross['VenueCrosscheckSHA256']}`
- CrosscheckGranularity: `{cross['CrosscheckGranularity']}`
- PrimaryTotalItems: `{total}`
- MetadataExportRecordCount: `{material['MetadataExportRecordCount']}`
- VenueCrosscheckItemCount: `{cross['VenueCrosscheckItemCount']}`
- RawRows: `{total}`
- NormalizedRows: `{material['NormalizedRows']}`
- MinSourceOrdinal: `1`
- MaxSourceOrdinal: `{total}`
- DuplicateManualSearchIDCount: `0`
- DuplicateSourceOrdinalCount: `0`
- InventorySourceID: `{args.primary_source_id}`
- ExtractionMethod: `audit_ieee_toc_html.pl offline structural extraction`
- CrosscheckExactTitleMatchCount: `{cross['CrosscheckExactTitleMatchCount']}`
- CrosscheckNormalizedTitleMatchCount: `{cross['CrosscheckNormalizedTitleMatchCount']}`
- CrosscheckTitleVersionDriftCount: `{cross['CrosscheckTitleVersionDriftCount']}`
- CrosscheckAuthorListDriftCount: `{cross['CrosscheckAuthorListDriftCount']}`
- CrosscheckPrimaryOnlyCount: `{cross['CrosscheckPrimaryOnlyCount']}`
- CrosscheckOnlyCount: `{cross['CrosscheckOnlyCount']}`
- CrosscheckAmbiguousCount: `{cross['CrosscheckAmbiguousCount']}`
- MaterialInventoryConflictCount: `{cross['MaterialInventoryConflictCount']}`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`
- VenueCrosscheckStatus: `{cross['VenueCrosscheckStatus']}`
- DocumentaryCollectionStatus: `{doc_status}`
- CurrentBlocker: `{blocker}`
- ControlledEvidenceCommittedCount: `0`
- RawInventorySHA256: `{material['RawInventorySHA256']}`

The venue crosscheck changes no raw membership row, ordinal, title, or locator. {interpretation}
"""

    norm_audit = f"""# Normalization audit

- NormalizedInventorySchema: `1`
- PrimaryHTMLSHA256: `{material['PrimaryHTMLSHA256']}`
- MetadataExportSHA256: `{material['MetadataExportSHA256']}`
- VenueCrosscheckSHA256: `{cross['VenueCrosscheckSHA256']}`
- CrosscheckGranularity: `{cross['CrosscheckGranularity']}`
- BibTeXParserVersion: `{metadata['BibTeXParserVersion']}`
- PrimaryTotalItems: `{total}`
- MetadataExportRecordCount: `{material['MetadataExportRecordCount']}`
- MatchedRecordCount: `{material['MatchedRecordCount']}`
- RawRows: `{total}`
- NormalizedRows: `{material['NormalizedRows']}`
- UniqueDOICount: `{int(metadata['DOICount']) - int(metadata['DuplicateDOICount'])}`
- DuplicateDOICount: `{metadata['DuplicateDOICount']}`
- BibTeXParseFailureCount: `{metadata['ParseFailureCount']}`
- CrosscheckExactTitleMatchCount: `{cross['CrosscheckExactTitleMatchCount']}`
- CrosscheckNormalizedTitleMatchCount: `{cross['CrosscheckNormalizedTitleMatchCount']}`
- CrosscheckTitleVersionDriftCount: `{cross['CrosscheckTitleVersionDriftCount']}`
- CrosscheckAuthorListDriftCount: `{cross['CrosscheckAuthorListDriftCount']}`
- CrosscheckPrimaryOnlyCount: `{cross['CrosscheckPrimaryOnlyCount']}`
- CrosscheckOnlyCount: `{cross['CrosscheckOnlyCount']}`
- CrosscheckAmbiguousCount: `{cross['CrosscheckAmbiguousCount']}`
- MaterialInventoryConflictCount: `{cross['MaterialInventoryConflictCount']}`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- CrossrefUsed: `false`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`
- VenueCrosscheckStatus: `{cross['VenueCrosscheckStatus']}`
- DocumentaryCollectionStatus: `{doc_status}`
- CurrentBlocker: `{blocker}`
- ControlledEvidenceCommittedCount: `0`
- NormalizationTimestamp: `{material['NormalizedAt']}`
- NormalizedInventorySHA256: `{material['NormalizedInventorySHA256']}`

The crosscheck did not modify normalized bibliographic values. Publisher metadata representation drift remains preserved without external correction. {interpretation}
"""

    report = f"""# {args.title} reconciliation report

## Unit and documentary status

- ManualSearchUnitID: `{args.unit_id}`
- DocumentaryCollectionStatus: `{doc_status}`
- CurrentBlocker: `{blocker}`

## Controlled sources

- PRIMARY_TOC: `{args.primary_source_id}` (`{material['PrimaryHTMLSHA256']}`)
- METADATA_SOURCE: `{args.metadata_source_id}` (`{material['MetadataExportSHA256']}`)
- VENUE_CROSSCHECK: `{args.crosscheck_source_id}` (`{cross['VenueCrosscheckSHA256']}`)

## Level 1 — PRIMARY_TOC × METADATA_SOURCE

- ReconciliationStatus: `COMPLETE`
- PrimaryTotalItems: `{total}`
- PrimaryResearchItems: `{args.primary_research_items}`
- PrimaryEditorialItems: `{args.primary_editorial_items}`
- MetadataExportRecordCount: `{material['MetadataExportRecordCount']}`
- DOIExactMatchCount: `{publisher['DOIExactMatchCount']}` (`DOIComparisonStatus={publisher['DOIComparisonStatus']}`)
- LiteralTitleMatchCount: `{publisher['LiteralTitleMatchCount']}`
- NormalizedTitleMatchCount: `{publisher['NormalizedTitleMatchCount']}`
- TitleVersionDriftCount: `0`
- AuthorListDriftCount: `{publisher['AuthorListDriftCount']}`
- PrimaryOnlyCount: `{publisher['PrimaryOnlyCount']}`
- MetadataOnlyCount: `{publisher['MetadataOnlyCount']}`
- AmbiguousMatchCount: `{publisher['AmbiguousMatchCount']}`
- MaterialInventoryConflictCount: `{publisher['MaterialInventoryConflictCount']}`

The publisher metadata export does not define membership or ordinals.

## Level 2 — PRIMARY_TOC × VENUE_CROSSCHECK

- ObservedPageGranularity: `{cross['ObservedPageGranularity']}`
- CrosscheckGranularity: `{cross['CrosscheckGranularity']}`
- VenueCrosscheckStatus: `{cross['VenueCrosscheckStatus']}`
- VenueCrosscheckItemCount: `{cross['VenueCrosscheckItemCount']}`
- CrosscheckExactTitleMatchCount: `{cross['CrosscheckExactTitleMatchCount']}`
- CrosscheckNormalizedTitleMatchCount: `{cross['CrosscheckNormalizedTitleMatchCount']}`
- CrosscheckTitleVersionDriftCount: `{cross['CrosscheckTitleVersionDriftCount']}`
- CrosscheckAuthorListDriftCount: `{cross['CrosscheckAuthorListDriftCount']}`
- CrosscheckPrimaryOnlyCount: `{cross['CrosscheckPrimaryOnlyCount']}`
- CrosscheckPrimaryEditorialOnlyCount: `{cross['CrosscheckPrimaryEditorialOnlyCount']}`
- CrosscheckOnlyCount: `{cross['CrosscheckOnlyCount']}`
- CrosscheckAmbiguousCount: `{cross['CrosscheckAmbiguousCount']}`
- MaterialInventoryConflictCount: `{cross['MaterialInventoryConflictCount']}`
- ReconciliationStatus: `{reconciliation_status}`

{interpretation} Orthographic, punctuation, presentation-suffix, and author-display differences are reported as drift rather than silently rewritten.

## Level 3 — documentary completion

- DocumentaryCollectionStatus: `{doc_status}`
- UnitStatus: `{unit_status}`
- RawInventoryStatus: `COMPLETE`
- NormalizationStatus: `COMPLETE`
- ReconciliationStatus: `{reconciliation_status}`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`

No discovery, screening, snowballing, or conditional-trigger review was executed.
"""

    atomic_text(args.unit_dir / "README.md", readme)
    atomic_text(args.unit_dir / "raw" / "inventory_audit.md", raw_audit)
    atomic_text(args.unit_dir / "metadata" / "normalization_audit.md", norm_audit)
    atomic_text(args.unit_dir / "source" / "reconciliation_report.md", report)
    atomic_text(args.unit_dir / "source" / "controlled_evidence_request.md", request)


if __name__ == "__main__":
    main()
