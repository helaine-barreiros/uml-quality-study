#!/usr/bin/env python3
"""Validate and atomically publish a documentary-inventory CSV.

The tool is publisher-neutral, performs no network access, and never writes to
the raw inventory passed through --raw-inventory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
from pathlib import Path
import shutil
import tempfile


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    width = len(rows[0])
    for ordinal, row in enumerate(rows, start=1):
        if len(row) != width:
            raise ValueError(
                f"column-count mismatch in {path} at CSV row {ordinal}: "
                f"expected {width}, observed {len(row)}"
            )
    return rows[0], rows[1:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--raw-inventory", required=True, type=Path)
    parser.add_argument("--expected-header", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidate = args.candidate.resolve()
    destination = args.destination.resolve()
    raw_inventory = args.raw_inventory.resolve()
    if destination == raw_inventory:
        raise ValueError("destination must not be the raw inventory")

    raw_before = sha256(raw_inventory)
    expected_header = next(csv.reader([args.expected_header]))
    candidate_header, _ = read_csv(candidate)
    if candidate_header != expected_header:
        raise ValueError("candidate header does not match --expected-header")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, prefix=f".{destination.name}.",
            suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            with candidate.open("rb") as source:
                shutil.copyfileobj(source, temporary)
            temporary.flush()
            os.fsync(temporary.fileno())

        temporary_header, _ = read_csv(temporary_path)
        if temporary_header != expected_header:
            raise ValueError("temporary output failed header validation")
        temporary_hash = sha256(temporary_path)
        if sha256(raw_inventory) != raw_before:
            raise RuntimeError("raw inventory changed during validation")

        os.replace(temporary_path, destination)
        temporary_path = None
        if sha256(destination) != temporary_hash:
            raise RuntimeError("final output hash differs after atomic publication")
        if sha256(raw_inventory) != raw_before:
            raise RuntimeError("raw inventory changed after publication")
        print(f"PublishedSHA256={temporary_hash}")
        print(f"RawInventorySHA256={raw_before}")
        return 0
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
