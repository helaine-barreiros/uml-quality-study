# Controlled-evidence intake tools

These tools operate only on local files and contain no titles, DOIs, years, cardinalities, credentials, cookies, or network clients.

## `audit_bibtex_export.pl`

Parses a local BibTeX export with `BibTeX::Parser 1.05`, requires `parse_ok` for every entry, emits a controlled metadata CSV without abstract or keyword text, and reports hashes, missing fields, duplicates, availability counts, entry types, and grouped publisher values. Dependencies: Perl, `BibTeX::Parser 1.05`, `Text::CSV`, `Unicode::Normalize`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

The parser also supports IEEE bulk BibTeX files that concatenate otherwise valid entries as `}@TYPE`. It inserts only the missing lexical line boundary in memory, records the insertion count, preserves the source bytes, and still delegates integral parsing to `BibTeX::Parser 1.05`.

## `audit_ieee_toc_html.pl`

Audits local saved IEEE Xplore and IEEE Computer Society Digital Library proceedings pages. It extracts only bibliographic display fields needed for documentary auditing, compares the locally materialized item count with the page's `Showing … of …` marker, and emits controlled item-level CSV plus a JSON summary. It never executes JavaScript or accesses the network. Dependencies: Perl, `HTML::TreeBuilder 5.07`, `Text::CSV`, `Unicode::Normalize`, `Encode`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

Supported saved-page structures are the IEEE Xplore `List-results-items` proceedings view and the IEEE CSDL `article-list-item` proceedings view. A page without a matching complete cardinality marker is reported as partial and must not define membership.

Runtime versions used for the RE/REW intake were Perl `5.40.1`, `BibTeX::Parser 1.05`, `HTML::TreeBuilder 5.07`, `Text::CSV 2.06`, `Unicode::Normalize 1.32`, `Digest::SHA 6.04`, `Getopt::Long 2.57`, `JSON::PP 4.16`, and `Encode 3.21`.

## `audit_acm_toc_html.pl`

Audits a locally saved ACM proceedings page without network access. It reads only the locally materialized `tableOfContent`, preserves an explicitly offered front-matter item, extracts ordered bibliographic display fields without retaining abstract text, rejects incomplete research records, duplicate DOI values, and locally visible load-more controls, and emits controlled item-level CSV plus a JSON summary. The expected year is supplied as an argument and must be observable in the controlled HTML. Dependencies are Perl, `HTML::TreeBuilder`, `Text::CSV`, `Unicode::Normalize`, `Encode`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

## `reconcile_ieee_toc_metadata.py`

Reconciles controlled item CSVs produced by the IEEE TOC auditor and BibTeX auditor. Matching uses an IEEE record locator/BibTeX key when available, then literal title, then a transparent diagnostic title normalization. The script reports title-set, order, author-list drift, ambiguity, and material-conflict counts. It uses Python's standard library only and never uses metadata-export order to define documentary order.

The RE/REW intake used Python `3.13.7` for this reconciliation step.

The reconciler also accepts the extended ACM TOC audit schema. It matches an observable DOI before title evidence, excludes explicitly marked editorial records from the required metadata cardinality, and retains those records as publisher-only membership. When a complete publisher TOC and export contain repeated identical display titles in the same verified sequence, the duplicate occurrence ordinal is used only to disambiguate the corresponding repeated records.

## `materialize_ieee_toc_bibtex.py`

Materializes raw and normalized inventories from previously audited local IEEE TOC and BibTeX evidence. The tool validates the original controlled-file hashes against the unit source manifest, requires a complete one-to-one deterministic reconciliation, preserves TOC order as documentary membership, uses BibTeX only for matched metadata enrichment, validates both produced CSVs, and publishes them atomically. It uses Python's standard library only and has no network client. Venue, unit identifiers, source identifiers, paths, and expected documentary context are supplied as arguments; no year, title, DOI, or cardinality is hardcoded.

## `render_ieee_unit_documents.py`

Renders the public per-unit README, raw audit, normalization audit, and three-level reconciliation report from safe aggregate audit JSON. Research/editorial counts and all unit context are passed as arguments; the renderer does not inspect or redistribute controlled textual fields. Output files are published atomically.

## `audit_researchr_crosscheck.pl`

Audits a locally saved official Researchr conference page without network access. It recognizes item-level accepted-paper lists and session/program track pages, extracts titles, author displays, track labels, and local record locators into controlled CSV, and emits only aggregate structural metrics in JSON. The tool does not treat a session or track page as complete by itself; coverage is decided by reconciliation with the publisher-defined raw inventory. Dependencies: Perl, `HTML::TreeBuilder 5.07`, `Text::CSV 2.06`, `Unicode::Normalize`, `Encode`, `Digest::SHA`, `Getopt::Long`, and `JSON::PP`.

## `reconcile_venue_crosscheck.py`

Compares controlled official-event entries with an already materialized publisher raw inventory. Matching uses literal title, transparent normalization, explicit presentation-suffix normalization, or combined ordered-author and lexical evidence. The tool reports aggregate coverage and keeps record-level mappings in controlled storage. A session page is sufficient only when every publisher research item is accounted for without ambiguity; editorial-only primary records and clearly out-of-scope program events are reported separately. Python standard library only; no network access.

## `render_ieee_crosscheck_documents.py`

Renders unit status, raw audit, normalization audit, reconciliation report, and the remaining controlled-evidence request from the aggregate publisher and venue-crosscheck audit JSON. It never opens licensed source HTML or textual metadata and does not alter raw or normalized CSVs. Output documentation is published atomically.

## `audit_pdf_zip.py`

Tests ZIP integrity with Python's standard `zipfile`, hashes every member in-stream, detects duplicate names, and invokes `pdfinfo` on temporary PDF bytes to collect only technical metadata. It never invokes `pdftotext`, OCR, or a network service. The complete member-level report is controlled evidence and must not be committed.

## `validate_controlled_intake.py`

Validates the public intake and gap CSV structures, required row counts, and identifier uniqueness without opening controlled evidence. It uses Python's standard library only.

The evidence-audit tools write only to paths supplied by arguments. For this intake, all detailed outputs belong under `.local-evidence/`; only aggregate, non-textual audit results may be published.

## Evidence-register boundary

Unit `source_manifest.csv` files are reserved for sources used in the documentary pipeline: `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE`, and official HTML `AUXILIARY_NAVIGATION` pages. Controlled PDF ZIPs are not source-manifest entries. They remain recorded in `controlled_evidence_intake_log.csv` and aggregate controlled-evidence audits as `CONTROLLED_FULLTEXT_PACKAGE` evidence only. A ZIP cannot create documentary membership or authorize raw or normalized inventory population.
