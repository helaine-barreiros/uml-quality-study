# Normalization audit

- NormalizedInventorySchema: `1`
- PrimaryHTMLSHA256: `26596910e8cd5114f6b4cb259b4fafc87bd90858ba5dfcf1f497e083980cfd48`
- MetadataExportSHA256: `5c612c3ab0fcaa29c3e6e0aed799110f30c83184dbb01792f5fdaad5624b9ba1`
- BibTeXParserVersion: `1.05`
- PrimaryTotalItems: `18`
- MetadataExportRecordCount: `18`
- MatchedRecordCount: `18`
- RawRows: `18`
- NormalizedRows: `18`
- UniqueDOICount: `18`
- DuplicateDOICount: `0`
- DuplicateDisplayedTitleGroupCount: `1`
- BibTeXParseFailureCount: `0`
- LiteralTitleMatchCount: `17`
- NormalizedTitleMatchCount: `1`
- TitleRepresentationDriftCount: `1`
- AuthorListDriftCount: `0`
- AbstractAvailableControlledCount: `13`
- KeywordsAvailableControlledCount: `12`
- AbstractTextCommittedCount: `0`
- KeywordTextCommittedCount: `0`
- CrossrefUsed: `false`
- DiscoveryDataRows: `0`
- CandidateCountPopulated: `false`
- VenueCrosscheckStatus: `REQUIRED`
- DocumentaryCollectionStatus: `BLOCKED`
- CurrentBlocker: `OFFICIAL_VENUE_CROSSCHECK_REQUIRED`
- ControlledEvidenceCommittedCount: `0`
- NormalizationTimestamp: `2026-08-15T00:14:58Z`
- NormalizedInventorySHA256: `82f3a6cd7aef3fa1e5a23d115d1c478ba2f30ad7bc5362486b54e2ad2ec6440f`

Validated publisher BibTeX is sufficient to populate normalized metadata for safely matched raw members. Title or author-list differences are preserved as metadata-representation drift and do not automatically create a material inventory conflict. No publisher abstract or keyword text is present in the public CSV.

Two distinct publisher records share the same displayed title. Because the complete normalized TOC and export title sequences are equal, the two occurrences were deterministically paired by their occurrence ordinal. Both distinct DOI values are preserved; no records were merged.
