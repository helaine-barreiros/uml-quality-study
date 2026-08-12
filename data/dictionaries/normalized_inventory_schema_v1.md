# Normalized inventory schema v1

`NormalizedInventorySchema = 1`

The normalized inventory preserves raw documentary evidence alongside deterministic metadata enrichment. `InventorySourceID` is the source that defined documentary membership; `MetadataSourceID` is the source used for metadata enrichment. They must not be conflated.

| Field | Definition |
| --- | --- |
| ManualSearchID | Stable identifier copied from the raw documentary inventory. |
| ManualSearchUnitID | Identifier of the venue × year × volume/track unit, copied from raw. |
| SourceOrdinal | Observed position in the membership-defining documentary source, copied from raw. |
| InventorySourceID | Source that defined documentary membership, copied from raw. |
| MetadataSourceID | Source used for metadata enrichment; it cannot create membership. |
| TitleRaw | Title exactly as observed in raw inventory. |
| TitleNormalized | Deterministically decoded and whitespace-normalized publisher title, or deterministic normalization of `TitleRaw` where metadata does not apply. |
| AuthorsRaw | Authors exactly as observed in raw inventory. |
| AuthorsNormalized | Complete ordered author list from `MetadataSourceID`; source order is preserved, individual authors are separated by the literal delimiter `; `, and no external identity correction is performed. |
| DOIRaw | DOI exactly as observed in raw inventory. |
| DOINormalized | DOI after deterministic prefix removal, trimming, and lowercasing. |
| VenueRaw | Venue exactly as observed in raw inventory. |
| VenueNormalized | Deterministically decoded and whitespace-normalized metadata-source venue. |
| YearRaw | Year exactly as observed in raw inventory. |
| YearNormalized | Deterministically normalized metadata-source year. |
| VolumeTrackIssue | Volume, track, proceedings, or issue copied from raw inventory. |
| PublisherRecordURL | Publisher record URL copied from raw inventory. |
| MetadataSourceURL | Explicit record URL from the metadata source, when reported. |
| Publisher | Publisher reported by metadata source. |
| PublisherAddress | Publisher address reported by metadata source. |
| ISBN | ISBN reported by metadata source. |
| Pages | Page range reported by metadata source. |
| NumPages | Number of pages reported by metadata source. |
| PublicationLocation | Publication location reported by metadata source. |
| Series | Series reported by metadata source. |
| AbstractRaw | Publicly redistributed abstract text. Empty when controlled text is not redistributed. |
| AbstractAvailability | Availability status for abstract text. |
| AbstractSourceURL | Explicit metadata-source URL associated with the record. |
| AuthorKeywordsRaw | Publicly redistributed publisher author keywords. Empty when controlled text is not redistributed. |
| AuthorKeywordsAvailability | Availability status for publisher author keywords. |
| FullTextURL | Full-text URL, if separately recorded; not inferred from a bibliographic record URL. |
| RetrievedAt | Original raw-inventory extraction timestamp, copied unchanged from raw. |
| NormalizedAt | UTC ISO-8601 timestamp of normalization execution. |
| InventoryConflict | `true` only for a documented contradiction that challenges documentary identity; otherwise `false`. |
| CrossrefSnapshotPath | Path to a Crossref snapshot, if used; empty when Crossref is not used. |
| PDFStatus | Status of a separately acquired PDF, if any. |
| PDFSHA256 | SHA-256 of a separately acquired PDF, if any. |
| Notes | Concise, source-grounded descriptive notes about normalization. |

## Availability enums

The present schema permits exactly these values for `AbstractAvailability` and `AuthorKeywordsAvailability`:

| Value | Meaning |
| --- | --- |
| AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED | Metadata exists in controlled project evidence, but its textual value is not included in the public normalized CSV. |
| NOT_REPORTED_BY_SOURCE | The expected field is absent from the metadata source. |
| NOT_APPLICABLE | The field does not apply to the documentary item, for example front matter. |

New values require explicit reporting before use.

## Null representation

- An empty CSV cell represents a value that was not populated.
- An empty cell must not be interpreted as evidence that the source explicitly reported an empty string.
- For `AbstractAvailability` and `AuthorKeywordsAvailability`, the enum explains why the textual field is empty.
- `NOT_APPLICABLE` and `NOT_REPORTED_BY_SOURCE` remain semantically distinct.
