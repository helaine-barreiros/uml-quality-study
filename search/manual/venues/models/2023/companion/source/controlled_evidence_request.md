# Controlled evidence request

- ManualSearchUnitID: `MSU-MODELS-2023-COMPANION`
- Publisher: IEEE
- Official proceedings URL: `https://ieeexplore.ieee.org/document/10350807`
- Observed access error: the public publication page returned HTTP 202 with an empty body; the metadata endpoint returned HTTP 418.
- Exact controlled files required: complete IEEE proceedings TOC/export that establishes every record in the publication and an unmodified publisher metadata export when separately available.
- Preferred export format: publisher-generated CSV or RIS covering the complete proceedings, together with a complete saved publication/TOC HTML representation.
- Required acquisition procedure: human-authenticated institutional access; save unmodified bytes; calculate size and SHA-256; record retrieval time in UTC; verify that the export covers the full publication.
- Prohibited contents: credentials, cookies, tokens, browser profiles, HAR files, session information, article PDFs, full text, or unauthorized source redistribution.
- Expected local destination: `.local-evidence/models/2023/companion/publisher_primary_toc.html` and `.local-evidence/models/2023/companion/publisher_primary_toc.csv` (or `.ris`).
- Notes: do not commit controlled evidence; the complete publisher TOC/export must define membership.
