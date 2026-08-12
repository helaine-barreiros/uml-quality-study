# Amendment A001 — normalized-inventory schema

- AmendmentID: `A001`
- DecisionDate: `2026-08-12`
- RecordedAt: `2026-08-12T15:05:32Z`
- Stage: Before first normalized inventory population
- Status: `Applied`
- FirstDataCommit: `5f66001b77a697be7e92029d4a70a95decfc719a`

## Decision

Expand the normalized-inventory schema to preserve structured publisher metadata, explicit metadata-source provenance, processing time, and the distinction between controlled metadata availability and public redistribution.

## Rationale

The original normalized placeholder did not provide explicit fields for `MetadataSourceID` or several structured publisher metadata elements already available in the authoritative publisher-generated BibTeX.

## Scope and non-changes

A001 does not change:

- research questions;
- review interval;
- automated search strategies;
- manual-search membership rules;
- eligibility criteria;
- documentary universe;
- Layer 1 or Layer 2 definitions;
- screening procedure;
- synthesis procedure.

A001 applies prospectively to metadata normalization and does not reinterpret or modify the raw inventory generated under protocol v1.7.

The amendment was recorded in the commit immediately preceding the first population of the normalized inventory (`5f66001b77a697be7e92029d4a70a95decfc719a`).

Raw records remain immutable. Every normalized record must reference an existing `ManualSearchID`, and metadata sources cannot create membership. Controlled or licensed textual content is not automatically redistributed in the public repository.
