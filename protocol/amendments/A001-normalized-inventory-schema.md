# Amendment A001 — normalized-inventory schema

- AmendmentID: `A001`
- Date: `2026-08-11`
- Stage: Before first normalized inventory population

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

Raw records remain immutable. Every normalized record must reference an existing `ManualSearchID`, and metadata sources cannot create membership. Controlled or licensed textual content is not automatically redistributed in the public repository.
