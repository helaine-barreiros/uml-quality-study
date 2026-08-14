#!/usr/bin/env python3
"""Validate public controlled-evidence intake tables without protected text."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if not reader.fieldnames:
            raise SystemExit(f"missing header: {path}")
        for number, row in enumerate(rows, 2):
            if None in row:
                raise SystemExit(f"invalid column count at {path}:{number}")
        return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake-log", required=True, type=Path)
    parser.add_argument("--gap-log", required=True, type=Path)
    parser.add_argument("--unit-registry", type=Path)
    args = parser.parse_args()

    evidence = read_csv(args.intake_log)
    gaps = read_csv(args.gap_log)
    if len(evidence) != 22:
        raise SystemExit(f"expected 22 evidence rows, found {len(evidence)}")
    ids = [row["EvidenceID"] for row in evidence]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate EvidenceID")
    if len(gaps) != 10:
        raise SystemExit(f"expected 10 gap rows, found {len(gaps)}")
    pairs = [(row["Year"], row["TrackType"]) for row in gaps]
    if len(pairs) != len(set(pairs)):
        raise SystemExit("duplicate year/track gap row")
    if args.unit_registry:
        units = read_csv(args.unit_registry)
        unit_ids = [row["ManualSearchUnitID"] for row in units]
        if len(unit_ids) != len(set(unit_ids)):
            raise SystemExit("duplicate ManualSearchUnitID")
    print(f"EvidenceRows={len(evidence)}")
    print(f"GapRows={len(gaps)}")
    print("CSVStructureValid=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
