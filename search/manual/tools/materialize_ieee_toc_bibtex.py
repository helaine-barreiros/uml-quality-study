#!/usr/bin/env python3
"""Materialize raw and normalized inventories from audited local IEEE evidence.

The complete publisher TOC defines membership and order.  The publisher
BibTeX export only enriches records that match deterministically.  Inputs are
local controlled evidence; this program has no network client.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


RAW_HEADER = [
    "ManualSearchID", "ManualSearchUnitID", "SourceOrdinal", "InventorySourceID",
    "SourceRecordLocator", "TitleRaw", "AuthorsRaw", "DOIRaw", "VenueRaw",
    "YearRaw", "VolumeTrackIssueRaw", "PublisherRecordURLRaw", "RetrievedAt",
    "ExtractionMethod", "Notes",
]

NORMALIZED_HEADER = [
    "ManualSearchID", "ManualSearchUnitID", "SourceOrdinal", "InventorySourceID",
    "MetadataSourceID", "TitleRaw", "TitleNormalized", "AuthorsRaw",
    "AuthorsNormalized", "DOIRaw", "DOINormalized", "VenueRaw", "VenueNormalized",
    "YearRaw", "YearNormalized", "VolumeTrackIssue", "PublisherRecordURL",
    "MetadataSourceURL", "Publisher", "PublisherAddress", "ISBN", "Pages",
    "NumPages", "PublicationLocation", "Series", "AbstractRaw",
    "AbstractAvailability", "AbstractSourceURL", "AuthorKeywordsRaw",
    "AuthorKeywordsAvailability", "FullTextURL", "RetrievedAt", "NormalizedAt",
    "InventoryConflict", "CrossrefSnapshotPath", "PDFStatus", "PDFSHA256", "Notes",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            fail(f"Missing CSV header: {path}")
        return reader.fieldnames, list(reader)


def clean(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value or "").split())


def normalized_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.translate(
        str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"})
    )
    value = re.sub(r"[^\w]+", " ", value.casefold(), flags=re.UNICODE)
    return " ".join(value.split())


def normalized_authors(value: str) -> tuple[str, ...]:
    return tuple(normalized_text(part) for part in (value or "").split(";") if part.strip())


def locator_key(locator: str) -> str:
    match = re.search(r"/document/(\d+)(?:/|$)", locator or "")
    return match.group(1) if match else ""


def normalize_doi(value: str) -> str:
    value = (value or "").strip()
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = re.sub(r"^https?://doi\.org/", "", value, flags=re.I)
    return value.lower()


def atomic_write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
            writer.writeheader()
            for row in rows:
                if set(row) != set(header):
                    fail(f"Output field mismatch for {path}")
                writer.writerow(row)
        parsed_header, parsed_rows = read_csv(temp_path)
        if parsed_header != header or len(parsed_rows) != len(rows):
            fail(f"Temporary CSV validation failed: {path}")
        expected_hash = sha256(temp_path)
        os.replace(temp_path, path)
        if sha256(path) != expected_hash:
            fail(f"Final CSV hash verification failed: {path}")
        return expected_hash
    finally:
        if temp_path.exists():
            temp_path.unlink()


def manifest_source(rows: list[dict[str, str]], source_id: str, role: str) -> dict[str, str]:
    matches = [row for row in rows if row["SourceID"] == source_id]
    if len(matches) != 1:
        fail(f"Expected exactly one manifest source {source_id}")
    if matches[0]["SourceRole"] != role:
        fail(f"Unexpected role for {source_id}: {matches[0]['SourceRole']}")
    return matches[0]


def match_records(toc: list[dict[str, str]], metadata: list[dict[str, str]]) -> list[tuple[dict[str, str], dict[str, str] | None, str]]:
    research_toc = [row for row in toc if row.get("IsEditorial", "false").casefold() != "true"]
    unused = set(range(len(metadata)))
    research_matches: dict[str, tuple[dict[str, str], str]] = {}
    by_key: dict[str, list[int]] = {}
    by_doi: dict[str, list[int]] = {}
    by_literal: dict[str, list[int]] = {}
    by_normalized: dict[str, list[int]] = {}
    for index, row in enumerate(metadata):
        by_key.setdefault(row["BibTeXKey"], []).append(index)
        by_doi.setdefault(normalize_doi(row["DOI"]), []).append(index)
        by_literal.setdefault(row["Title"], []).append(index)
        by_normalized.setdefault(normalized_text(row["Title"]), []).append(index)
    for research_position, toc_row in enumerate(research_toc):
        candidates: list[int] = []
        evidence = ""
        doi = normalize_doi(toc_row.get("DOI", ""))
        if doi:
            candidates = [index for index in by_doi.get(doi, []) if index in unused]
            evidence = "publisher DOI exact match"
        key = locator_key(toc_row["Locator"])
        if len(candidates) != 1 and key:
            candidates = [index for index in by_key.get(key, []) if index in unused]
            evidence = "IEEE record locator equals publisher BibTeX key"
        if len(candidates) != 1:
            candidates = [index for index in by_literal.get(toc_row["Title"], []) if index in unused]
            evidence = "literal title"
        if len(candidates) != 1:
            candidates = [
                index for index in by_normalized.get(normalized_text(toc_row["Title"]), [])
                if index in unused
            ]
            evidence = "diagnostic normalized title"
        if len(candidates) != 1 and research_position in unused:
            if normalized_text(toc_row["Title"]) == normalized_text(metadata[research_position]["Title"]):
                candidates = [research_position]
                evidence = "equal complete sequence and duplicate occurrence ordinal"
        if len(candidates) != 1:
            fail(f"Ambiguous or missing metadata match for TOC ordinal {toc_row['EntryOrdinal']}: {toc_row['Title']}")
        index = candidates[0]
        unused.remove(index)
        research_matches[toc_row["EntryOrdinal"]] = (metadata[index], evidence)
    if unused:
        fail(f"Unmatched publisher metadata records: {len(unused)}")
    return [
        (row, *research_matches[row["EntryOrdinal"]])
        if row.get("IsEditorial", "false").casefold() != "true"
        else (row, None, "editorial item present only in PRIMARY_TOC")
        for row in toc
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--id-prefix", required=True)
    parser.add_argument("--year", required=True)
    parser.add_argument("--venue", required=True)
    parser.add_argument("--volume-track-issue", default="")
    parser.add_argument("--extraction-tool", default="")
    parser.add_argument("--primary-source-id", required=True)
    parser.add_argument("--metadata-source-id", required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--primary-html", type=Path, required=True)
    parser.add_argument("--metadata-bib", type=Path, required=True)
    parser.add_argument("--toc-entries", type=Path, required=True)
    parser.add_argument("--metadata-entries", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--normalized-output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()

    _, manifest = read_csv(args.source_manifest)
    primary_source = manifest_source(manifest, args.primary_source_id, "PRIMARY_TOC")
    metadata_source = manifest_source(manifest, args.metadata_source_id, "METADATA_SOURCE")
    actual_primary_hash = sha256(args.primary_html)
    actual_metadata_hash = sha256(args.metadata_bib)
    if actual_primary_hash != primary_source["SHA256"]:
        fail("PRIMARY_TOC SHA-256 differs from source manifest")
    if actual_metadata_hash != metadata_source["SHA256"]:
        fail("METADATA_SOURCE SHA-256 differs from source manifest")

    toc_header, toc = read_csv(args.toc_entries)
    metadata_header, metadata = read_csv(args.metadata_entries)
    base_toc_header = ["EntryOrdinal", "Title", "Authors", "Year", "Pages", "Locator"]
    acm_toc_header = ["EntryOrdinal", "ItemType", "Title", "Authors", "DOI", "Year", "Pages", "Locator", "Section", "IsEditorial"]
    if toc_header not in (base_toc_header, acm_toc_header):
        fail("Unexpected audited TOC entries schema")
    required_metadata = {
        "BibTeXKey", "DOI", "Title", "Authors", "Year", "Booktitle", "Series", "ISBN",
        "Publisher", "Location", "Pages", "NumPages", "URL", "AbstractAvailability",
        "KeywordsAvailability", "ParseStatus",
    }
    if not required_metadata.issubset(metadata_header):
        fail("Unexpected audited metadata entries schema")
    if any(row["ParseStatus"] != "PARSE_OK" for row in metadata):
        fail("Publisher metadata contains a parse failure")
    research_toc = [row for row in toc if row.get("IsEditorial", "false").casefold() != "true"]
    if len(research_toc) != len(metadata):
        fail(f"Research TOC/metadata cardinality mismatch: {len(research_toc)} != {len(metadata)}")
    if [int(row["EntryOrdinal"]) for row in toc] != list(range(1, len(toc) + 1)):
        fail("TOC ordinals are not unique and sequential")
    doi_values = [normalize_doi(row["DOI"]) for row in metadata]
    if any(not value for value in doi_values) or len(set(doi_values)) != len(doi_values):
        fail("Publisher metadata DOI values are missing or duplicated")

    reconciliation = json.loads(args.reconciliation.read_text(encoding="utf-8"))
    if reconciliation["MaterialInventoryConflictCount"] != 0:
        fail("Material inventory conflict recorded by controlled reconciliation")
    matches = match_records(toc, metadata)
    if sum(metadata_row is not None for _, metadata_row, _ in matches) != reconciliation["MatchedRecordCount"]:
        fail("Match count differs from controlled reconciliation")

    normalized_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    raw_rows: list[dict[str, str]] = []
    normalized_rows: list[dict[str, str]] = []
    match_evidence_counts: Counter[str] = Counter()
    author_drift_count = 0
    title_representation_count = 0
    for ordinal, (toc_row, metadata_row, evidence) in enumerate(matches, 1):
        manual_id = f"{args.id_prefix}-{ordinal:04d}"
        match_evidence_counts[evidence] += 1
        editorial = metadata_row is None
        title_drift = not editorial and toc_row["Title"] != metadata_row["Title"]
        author_drift = not editorial and normalized_authors(toc_row["Authors"]) != normalized_authors(metadata_row["Authors"])
        title_representation_count += int(title_drift)
        author_drift_count += int(author_drift)
        raw_notes = "Complete controlled publisher PRIMARY_TOC membership row; discovery was not executed."
        raw_row = {
            "ManualSearchID": manual_id,
            "ManualSearchUnitID": args.unit_id,
            "SourceOrdinal": str(ordinal),
            "InventorySourceID": args.primary_source_id,
            "SourceRecordLocator": toc_row["Locator"],
            "TitleRaw": toc_row["Title"],
            "AuthorsRaw": toc_row["Authors"],
            "DOIRaw": toc_row.get("DOI", ""),
            "VenueRaw": args.venue,
            "YearRaw": toc_row["Year"] or args.year,
            "VolumeTrackIssueRaw": args.volume_track_issue,
            "PublisherRecordURLRaw": toc_row["Locator"],
            "RetrievedAt": primary_source["RetrievedAt"],
            "ExtractionMethod": (
                args.extraction_tool
                or ("audit_acm_toc_html.pl" if "ItemType" in toc_row else "audit_ieee_toc_html.pl")
            ) + " offline structural extraction",
            "Notes": raw_notes,
        }
        notes = ([f"Matched to publisher BibTeX by {evidence}."] if not editorial else ["Editorial item retained from PRIMARY_TOC without inferred metadata record."])
        if title_drift:
            notes.append("TOC/BibTeX title representation drift preserved; no external correction applied.")
        if author_drift:
            notes.append("TOC/BibTeX author-list representation drift preserved; no external correction applied.")
        notes.append("Discovery was not executed.")
        normalized_row = {
            "ManualSearchID": manual_id,
            "ManualSearchUnitID": args.unit_id,
            "SourceOrdinal": str(ordinal),
            "InventorySourceID": args.primary_source_id,
            "MetadataSourceID": "" if editorial else args.metadata_source_id,
            "TitleRaw": toc_row["Title"],
            "TitleNormalized": clean(toc_row["Title"] if editorial else metadata_row["Title"]),
            "AuthorsRaw": toc_row["Authors"],
            "AuthorsNormalized": clean(toc_row["Authors"] if editorial else metadata_row["Authors"]),
            "DOIRaw": toc_row.get("DOI", ""),
            "DOINormalized": "" if editorial else normalize_doi(metadata_row["DOI"]),
            "VenueRaw": args.venue,
            "VenueNormalized": args.venue if editorial else clean(metadata_row["Booktitle"]),
            "YearRaw": toc_row["Year"] or args.year,
            "YearNormalized": args.year if editorial else clean(metadata_row["Year"]),
            "VolumeTrackIssue": args.volume_track_issue,
            "PublisherRecordURL": toc_row["Locator"],
            "MetadataSourceURL": "" if editorial else metadata_row["URL"],
            "Publisher": "" if editorial else clean(metadata_row["Publisher"]),
            "PublisherAddress": "",
            "ISBN": "" if editorial else metadata_row["ISBN"],
            "Pages": toc_row["Pages"] if editorial else metadata_row["Pages"],
            "NumPages": "" if editorial else metadata_row["NumPages"],
            "PublicationLocation": "" if editorial else clean(metadata_row["Location"]),
            "Series": "" if editorial else clean(metadata_row["Series"]),
            "AbstractRaw": "",
            "AbstractAvailability": "NOT_APPLICABLE" if editorial else metadata_row["AbstractAvailability"],
            "AbstractSourceURL": "" if editorial or metadata_row["AbstractAvailability"] != "AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED" else metadata_row["URL"],
            "AuthorKeywordsRaw": "",
            "AuthorKeywordsAvailability": "NOT_APPLICABLE" if editorial else metadata_row["KeywordsAvailability"],
            "FullTextURL": "",
            "RetrievedAt": primary_source["RetrievedAt"],
            "NormalizedAt": normalized_at,
            "InventoryConflict": "false",
            "CrossrefSnapshotPath": "",
            "PDFStatus": "",
            "PDFSHA256": "",
            "Notes": " ".join(notes),
        }
        raw_rows.append(raw_row)
        normalized_rows.append(normalized_row)

    raw_hash = atomic_write_csv(args.raw_output, RAW_HEADER, raw_rows)
    normalized_hash = atomic_write_csv(args.normalized_output, NORMALIZED_HEADER, normalized_rows)
    _, reread_raw = read_csv(args.raw_output)
    _, reread_normalized = read_csv(args.normalized_output)
    raw_ids = [row["ManualSearchID"] for row in reread_raw]
    normalized_ids = [row["ManualSearchID"] for row in reread_normalized]
    if raw_ids != normalized_ids or len(set(raw_ids)) != len(raw_ids):
        fail("Raw/normalized ManualSearchID invariant failed")
    if [row["SourceOrdinal"] for row in reread_raw] != [str(i) for i in range(1, len(toc) + 1)]:
        fail("Published raw SourceOrdinal invariant failed")
    if any(row["InventorySourceID"] != args.primary_source_id for row in reread_raw + reread_normalized):
        fail("InventorySourceID invariant failed")
    if any(row["MetadataSourceID"] not in ("", args.metadata_source_id) for row in reread_normalized):
        fail("MetadataSourceID invariant failed")
    if any(row["AbstractRaw"] or row["AuthorKeywordsRaw"] or row["FullTextURL"] for row in reread_normalized):
        fail("Controlled text/full-text publication invariant failed")
    if any(row["InventoryConflict"] != "false" for row in reread_normalized):
        fail("Unexpected inventory conflict flag")

    audit = {
        "UnitID": args.unit_id,
        "PrimaryHTMLSHA256": actual_primary_hash,
        "MetadataExportSHA256": actual_metadata_hash,
        "PrimaryTotalItems": len(toc),
        "MetadataExportRecordCount": len(metadata),
        "MatchedRecordCount": sum(metadata_row is not None for _, metadata_row, _ in matches),
        "RawRows": len(reread_raw),
        "NormalizedRows": len(reread_normalized),
        "RawInventorySHA256": raw_hash,
        "NormalizedInventorySHA256": normalized_hash,
        "NormalizedAt": normalized_at,
        "LiteralTitleMatchCount": reconciliation["LiteralTitleMatchCount"],
        "NormalizedTitleMatchCount": reconciliation["NormalizedTitleMatchCount"],
        "TitleRepresentationDriftCount": title_representation_count,
        "AuthorListDriftCount": author_drift_count,
        "MaterialInventoryConflictCount": 0,
        "MatchEvidenceCounts": dict(sorted(match_evidence_counts.items())),
        "DiscoveryDataRows": 0,
        "CandidateCountPopulated": False,
        "VenueCrosscheckStatus": "REQUIRED",
        "DocumentaryCollectionStatus": "BLOCKED",
        "CurrentBlocker": "OFFICIAL_VENUE_CROSSCHECK_REQUIRED",
        "ControlledEvidenceCommittedCount": 0,
    }
    args.audit_output.parent.mkdir(parents=True, exist_ok=True)
    args.audit_output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
