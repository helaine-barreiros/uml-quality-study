#!/usr/bin/env python3
"""Reconcile an audited official venue page with a publisher-defined raw inventory."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"}))
    return " ".join(re.sub(r"[^\w]+", " ", value.casefold(), flags=re.UNICODE).split())


def diagnostic_title(value: str) -> str:
    value = re.sub(r"\s*\[(?:demo|poster|src(?:\s+(?:gr|ug))?)\]\s*$", "", value or "", flags=re.I)
    value = re.sub(r"\s+(?:demo|poster)\s*$", "", value, flags=re.I)
    return normalized(value)


def author_tuple(value: str) -> tuple[str, ...]:
    return tuple(normalized(part) for part in (value or "").split(";") if part.strip())


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--normalized", type=Path, required=True)
    parser.add_argument("--crosscheck", type=Path, required=True)
    parser.add_argument("--crosscheck-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record-output", type=Path, required=True)
    args = parser.parse_args()

    raw = rows(args.raw)
    normalized_rows = rows(args.normalized)
    crosscheck = rows(args.crosscheck)
    audit = json.loads(args.crosscheck_audit.read_text(encoding="utf-8"))
    if [r["ManualSearchID"] for r in raw] != [r["ManualSearchID"] for r in normalized_rows]:
        raise SystemExit("Raw/normalized sequence differs")

    primary = []
    for raw_row, norm_row in zip(raw, normalized_rows):
        primary.append({**raw_row, "AuthorsNormalizedForComparison": norm_row["AuthorsNormalized"]})
    research_indices = {i for i, row in enumerate(primary) if row["AuthorsNormalizedForComparison"].strip()}
    editorial_indices = set(range(len(primary))) - research_indices
    unused_primary = set(range(len(primary)))
    matches: list[dict[str, object]] = []
    ambiguous = 0

    by_literal: dict[str, list[int]] = {}
    by_normalized: dict[str, list[int]] = {}
    by_diagnostic: dict[str, list[int]] = {}
    for index, row in enumerate(primary):
        by_literal.setdefault(row["TitleRaw"], []).append(index)
        by_normalized.setdefault(normalized(row["TitleRaw"]), []).append(index)
        by_diagnostic.setdefault(diagnostic_title(row["TitleRaw"]), []).append(index)

    for c_index, cross in enumerate(crosscheck):
        candidates: list[int] = []
        evidence = ""
        category = ""
        title = cross["Title"]
        if title:
            candidates = [i for i in by_literal.get(title, []) if i in unused_primary]
            evidence = "literal title"
            category = "CROSSCHECK_EXACT_TITLE_MATCH"
        if len(candidates) != 1 and title:
            candidates = [i for i in by_normalized.get(normalized(title), []) if i in unused_primary]
            evidence = "transparent Unicode/case/punctuation normalization"
            category = "CROSSCHECK_NORMALIZED_TITLE_MATCH"
        if len(candidates) != 1 and title:
            candidates = [i for i in by_diagnostic.get(diagnostic_title(title), []) if i in unused_primary]
            evidence = "diagnostic removal of explicit presentation-type suffix"
            category = "CROSSCHECK_TITLE_VERSION_DRIFT"
        if len(candidates) != 1 and cross.get("DisplayText"):
            display = normalized(cross["DisplayText"])
            embedded = [i for i in unused_primary if normalized(primary[i]["TitleRaw"]) in display]
            if len(embedded) == 1:
                candidates = embedded
                evidence = "publisher title occurs literally after normalization within accepted-paper display text"
                category = "CROSSCHECK_TITLE_VERSION_DRIFT"
        if len(candidates) != 1 and title and cross["Authors"]:
            c_authors = author_tuple(cross["Authors"])
            author_candidates = [
                i for i in unused_primary
                if c_authors and c_authors == author_tuple(primary[i]["AuthorsNormalizedForComparison"])
            ]
            lexical = [
                i for i in author_candidates
                if set(normalized(title).split()) & set(normalized(primary[i]["TitleRaw"]).split())
            ]
            if len(lexical) == 1:
                candidates = lexical
                evidence = "complete ordered author equality plus shared title lexicon"
                category = "CROSSCHECK_TITLE_VERSION_DRIFT"
        if len(candidates) != 1:
            ambiguous += int(len(candidates) > 1)
            continue
        p_index = candidates[0]
        unused_primary.remove(p_index)
        primary_row = primary[p_index]
        authors_drift = bool(cross["Authors"] or primary_row["AuthorsNormalizedForComparison"]) and author_tuple(cross["Authors"]) != author_tuple(primary_row["AuthorsNormalizedForComparison"])
        matches.append({
            "CrosscheckIndex": c_index,
            "PrimaryIndex": p_index,
            "ManualSearchID": primary_row["ManualSearchID"],
            "Category": category,
            "Evidence": evidence,
            "AuthorListDrift": authors_drift,
        })

    matched_crosscheck = {int(m["CrosscheckIndex"]) for m in matches}
    primary_research_only = sorted(research_indices & unused_primary)
    primary_editorial_only = sorted(editorial_indices & unused_primary)
    crosscheck_only = sorted(set(range(len(crosscheck))) - matched_crosscheck)
    categories = Counter(str(m["Category"]) for m in matches)
    granularity = audit["CrosscheckGranularity"]
    sufficient = granularity in {"ITEM_LEVEL", "SESSION_LEVEL"} and not primary_research_only and not ambiguous
    effective_granularity = granularity if sufficient else ("TRACK_LEVEL" if granularity == "SESSION_LEVEL" else granularity)
    result = {
        "VenueCrosscheckSHA256": audit["SHA256"],
        "CrosscheckGranularity": effective_granularity,
        "ObservedPageGranularity": granularity,
        "VenueCrosscheckItemCount": len(crosscheck),
        "PrimaryTotalItems": len(primary),
        "PrimaryResearchItems": len(research_indices),
        "PrimaryEditorialItems": len(editorial_indices),
        "CrosscheckExactTitleMatchCount": categories["CROSSCHECK_EXACT_TITLE_MATCH"],
        "CrosscheckNormalizedTitleMatchCount": categories["CROSSCHECK_NORMALIZED_TITLE_MATCH"],
        "CrosscheckTitleVersionDriftCount": categories["CROSSCHECK_TITLE_VERSION_DRIFT"],
        "CrosscheckAuthorListDriftCount": sum(bool(m["AuthorListDrift"]) for m in matches),
        "CrosscheckPrimaryOnlyCount": len(primary_research_only),
        "CrosscheckPrimaryEditorialOnlyCount": len(primary_editorial_only),
        "CrosscheckOnlyCount": len(crosscheck_only),
        "CrosscheckAmbiguousCount": ambiguous,
        "MaterialInventoryConflictCount": 0,
        "CrosscheckSufficientForDocumentaryCompletion": sufficient,
        "VenueCrosscheckStatus": "COMPLETE" if sufficient else "PARTIAL",
        "DocumentaryCollectionStatus": "COMPLETE" if sufficient else "BLOCKED",
        "CurrentBlocker": "" if sufficient else "ITEM_LEVEL_VENUE_CROSSCHECK_REQUIRED",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    args.record_output.parent.mkdir(parents=True, exist_ok=True)
    with args.record_output.open("w", encoding="utf-8", newline="") as handle:
        header = ["ManualSearchID", "CrosscheckOrdinal", "MatchCategory", "MatchEvidence", "AuthorListDrift"]
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for match in matches:
            writer.writerow({
                "ManualSearchID": match["ManualSearchID"],
                "CrosscheckOrdinal": int(match["CrosscheckIndex"]) + 1,
                "MatchCategory": match["Category"],
                "MatchEvidence": match["Evidence"],
                "AuthorListDrift": str(bool(match["AuthorListDrift"])).lower(),
            })


if __name__ == "__main__":
    main()
