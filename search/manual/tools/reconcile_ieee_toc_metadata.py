#!/usr/bin/env python3
"""Reconcile controlled IEEE TOC and publisher-export audit CSVs offline."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


def normalized_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.translate(
        str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"})
    )
    value = re.sub(r"[^\w]+", " ", value.casefold(), flags=re.UNICODE)
    return " ".join(value.split())


def normalized_authors(value: str) -> tuple[str, ...]:
    return tuple(normalized_text(author) for author in value.split(";") if author.strip())


def locator_key(locator: str) -> str:
    match = re.search(r"/document/(\d+)(?:/|$)", locator)
    return match.group(1) if match else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toc-entries", type=Path, required=True)
    parser.add_argument("--metadata-entries", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    toc = read_csv(args.toc_entries)
    metadata = read_csv(args.metadata_entries)
    unused_metadata = set(range(len(metadata)))
    matches: list[dict[str, object]] = []
    ambiguous_primary: list[int] = []

    by_key: dict[str, list[int]] = {}
    by_literal_title: dict[str, list[int]] = {}
    by_normalized_title: dict[str, list[int]] = {}
    for index, record in enumerate(metadata):
        by_key.setdefault(record.get("BibTeXKey", ""), []).append(index)
        by_literal_title.setdefault(record["Title"], []).append(index)
        by_normalized_title.setdefault(normalized_text(record["Title"]), []).append(index)

    for toc_index, record in enumerate(toc):
        candidates: list[int] = []
        evidence = ""
        key = locator_key(record["Locator"])
        if key:
            candidates = [index for index in by_key.get(key, []) if index in unused_metadata]
            evidence = "IEEE record locator equals publisher BibTeX key"
        if len(candidates) != 1:
            candidates = [
                index for index in by_literal_title.get(record["Title"], []) if index in unused_metadata
            ]
            evidence = "literal title"
        if len(candidates) != 1:
            candidates = [
                index
                for index in by_normalized_title.get(normalized_text(record["Title"]), [])
                if index in unused_metadata
            ]
            evidence = "diagnostic normalized title"
        if len(candidates) != 1:
            ambiguous_primary.append(toc_index)
            continue
        metadata_index = candidates[0]
        unused_metadata.remove(metadata_index)
        metadata_record = metadata[metadata_index]
        literal_title = record["Title"] == metadata_record["Title"]
        normalized_title = normalized_text(record["Title"]) == normalized_text(metadata_record["Title"])
        toc_authors = normalized_authors(record["Authors"])
        metadata_authors = normalized_authors(metadata_record["Authors"])
        author_drift = bool(toc_authors or metadata_authors) and toc_authors != metadata_authors
        matches.append(
            {
                "TOCIndex": toc_index,
                "MetadataIndex": metadata_index,
                "Evidence": evidence,
                "LiteralTitle": literal_title,
                "NormalizedTitle": normalized_title,
                "AuthorListDrift": author_drift,
            }
        )

    toc_normalized_titles = [normalized_text(record["Title"]) for record in toc]
    metadata_normalized_titles = [normalized_text(record["Title"]) for record in metadata]
    summary = {
        "PrimaryTotalItems": len(toc),
        "MetadataExportRecordCount": len(metadata),
        "MatchedRecordCount": len(matches),
        "DOIExactMatchCount": 0,
        "DOIComparisonStatus": "NOT_OBSERVABLE_IN_PRIMARY_TOC",
        "LiteralTitleMatchCount": sum(bool(match["LiteralTitle"]) for match in matches),
        "NormalizedTitleMatchCount": sum(
            bool(match["NormalizedTitle"]) and not bool(match["LiteralTitle"]) for match in matches
        ),
        "TitleSequenceEqual": toc_normalized_titles == metadata_normalized_titles,
        "NormalizedTitleMultisetEqual": Counter(toc_normalized_titles)
        == Counter(metadata_normalized_titles),
        "AuthorListDriftCount": sum(bool(match["AuthorListDrift"]) for match in matches),
        "PrimaryOnlyCount": len(ambiguous_primary),
        "MetadataOnlyCount": len(unused_metadata),
        "AmbiguousMatchCount": len(ambiguous_primary),
        "MaterialInventoryConflictCount": 0
        if not ambiguous_primary and not unused_metadata
        else len(ambiguous_primary) + len(unused_metadata),
        "DuplicatePrimaryNormalizedTitleCount": sum(
            count > 1 for count in Counter(toc_normalized_titles).values()
        ),
        "DuplicateMetadataNormalizedTitleCount": sum(
            count > 1 for count in Counter(metadata_normalized_titles).values()
        ),
    }
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if summary["MaterialInventoryConflictCount"]:
        raise SystemExit("Unresolved controlled TOC/metadata reconciliation")


if __name__ == "__main__":
    main()
