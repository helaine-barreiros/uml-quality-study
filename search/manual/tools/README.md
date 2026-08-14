# Controlled-evidence intake tools

These tools operate only on local files and contain no titles, DOIs, years, cardinalities, credentials, cookies, or network clients.

## `audit_bibtex_export.pl`

Parses a local BibTeX export with `BibTeX::Parser 1.05`, requires `parse_ok` for every entry, emits a controlled metadata CSV without abstract or keyword text, and reports hashes, missing fields, duplicates, availability counts, entry types, and grouped publisher values. Dependencies: Perl, `BibTeX::Parser 1.05`, `Text::CSV`, `Unicode::Normalize`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

## `audit_pdf_zip.py`

Tests ZIP integrity with Python's standard `zipfile`, hashes every member in-stream, detects duplicate names, and invokes `pdfinfo` on temporary PDF bytes to collect only technical metadata. It never invokes `pdftotext`, OCR, or a network service. The complete member-level report is controlled evidence and must not be committed.

## `validate_controlled_intake.py`

Validates the public intake and gap CSV structures, required row counts, and identifier uniqueness without opening controlled evidence. It uses Python's standard library only.

The evidence-audit tools write only to paths supplied by arguments. For this intake, all detailed outputs belong under `.local-evidence/`; only aggregate, non-textual audit results may be published.

## Evidence-register boundary

Unit `source_manifest.csv` files are reserved for sources used in the documentary pipeline: `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE`, and official HTML `AUXILIARY_NAVIGATION` pages. Controlled PDF ZIPs are not source-manifest entries. They remain recorded in `controlled_evidence_intake_log.csv` and aggregate controlled-evidence audits as `CONTROLLED_FULLTEXT_PACKAGE` evidence only. A ZIP cannot create documentary membership or authorize raw or normalized inventory population.
