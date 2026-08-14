# Controlled-evidence intake tools

These tools operate only on local files and contain no titles, DOIs, years, cardinalities, credentials, cookies, or network clients.

## `audit_bibtex_export.pl`

Parses a local BibTeX export with `BibTeX::Parser 1.05`, requires `parse_ok` for every entry, emits a controlled metadata CSV without abstract or keyword text, and reports hashes, missing fields, duplicates, availability counts, entry types, and grouped publisher values. Dependencies: Perl, `BibTeX::Parser 1.05`, `Text::CSV`, `Unicode::Normalize`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

The parser also supports IEEE bulk BibTeX files that concatenate otherwise valid entries as `}@TYPE`. It inserts only the missing lexical line boundary in memory, records the insertion count, preserves the source bytes, and still delegates integral parsing to `BibTeX::Parser 1.05`.

## `audit_ieee_toc_html.pl`

Audits local saved IEEE Xplore and IEEE Computer Society Digital Library proceedings pages. It extracts only bibliographic display fields needed for documentary auditing, compares the locally materialized item count with the page's `Showing … of …` marker, and emits controlled item-level CSV plus a JSON summary. It never executes JavaScript or accesses the network. Dependencies: Perl, `HTML::TreeBuilder 5.07`, `Text::CSV`, `Unicode::Normalize`, `Encode`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

Supported saved-page structures are the IEEE Xplore `List-results-items` proceedings view and the IEEE CSDL `article-list-item` proceedings view. A page without a matching complete cardinality marker is reported as partial and must not define membership.

Runtime versions used for the RE/REW intake were Perl `5.40.1`, `BibTeX::Parser 1.05`, `HTML::TreeBuilder 5.07`, `Text::CSV 2.06`, `Unicode::Normalize 1.32`, `Digest::SHA 6.04`, `Getopt::Long 2.57`, `JSON::PP 4.16`, and `Encode 3.21`.

## `reconcile_ieee_toc_metadata.py`

Reconciles controlled item CSVs produced by the IEEE TOC auditor and BibTeX auditor. Matching uses an IEEE record locator/BibTeX key when available, then literal title, then a transparent diagnostic title normalization. The script reports title-set, order, author-list drift, ambiguity, and material-conflict counts. It uses Python's standard library only and never uses metadata-export order to define documentary order.

The RE/REW intake used Python `3.13.7` for this reconciliation step.

## `audit_pdf_zip.py`

Tests ZIP integrity with Python's standard `zipfile`, hashes every member in-stream, detects duplicate names, and invokes `pdfinfo` on temporary PDF bytes to collect only technical metadata. It never invokes `pdftotext`, OCR, or a network service. The complete member-level report is controlled evidence and must not be committed.

## `validate_controlled_intake.py`

Validates the public intake and gap CSV structures, required row counts, and identifier uniqueness without opening controlled evidence. It uses Python's standard library only.

The evidence-audit tools write only to paths supplied by arguments. For this intake, all detailed outputs belong under `.local-evidence/`; only aggregate, non-textual audit results may be published.

## Evidence-register boundary

Unit `source_manifest.csv` files are reserved for sources used in the documentary pipeline: `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE`, and official HTML `AUXILIARY_NAVIGATION` pages. Controlled PDF ZIPs are not source-manifest entries. They remain recorded in `controlled_evidence_intake_log.csv` and aggregate controlled-evidence audits as `CONTROLLED_FULLTEXT_PACKAGE` evidence only. A ZIP cannot create documentary membership or authorize raw or normalized inventory population.
