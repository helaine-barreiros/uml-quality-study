# Reusable manual-search tools

These tools operate only on local files. They contain no known titles, DOIs, years, item counts, credentials, cookies, or network clients.

## `publish_inventory_csv.py`

Publisher-neutral CSV validation and atomic publication utility. It:

- parses CSV with Python's standard `csv` module;
- validates the complete header and every row's column count;
- records SHA-256 for the immutable raw inventory;
- writes to a temporary file in the destination directory;
- validates and hashes the temporary output before publication;
- uses `os.replace()` for atomic publication;
- verifies both the final-output hash and raw-inventory immutability;
- removes temporary output on failure.

Runtime dependency: Python 3 standard library (`argparse`, `csv`, `hashlib`, `os`, `pathlib`, `shutil`, `tempfile`). The exact Python runtime version must be recorded by the unit-specific normalization audit when the tool is used.

Example:

```text
python3 search/manual/tools/publish_inventory_csv.py \
  --candidate controlled/generated_inventory.csv \
  --destination search/manual/venues/models/<year>/<track>/normalized/inventory.csv \
  --raw-inventory search/manual/venues/models/<year>/<track>/raw/inventory_raw.csv \
  --expected-header '<complete schema header>'
```

## Supported formats and publishers

The current reusable layer supports UTF-8 CSV inventories independent of publisher. No reusable publisher-specific HTML, BibTeX, RIS, or proprietary CSV parser is asserted by this batch initialization. A publisher-specific parser may be added only after a complete controlled source is available and its structure can be validated without hardcoded bibliographic content.

## Limitations

The utility does not extract membership, reconcile venues, normalize metadata, or perform discovery or screening. It does not determine whether an export may be redistributed. Controlled source files remain under `.local-evidence/` and are never accepted as public output merely because they can be parsed.
