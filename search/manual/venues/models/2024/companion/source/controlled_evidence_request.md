# Controlled evidence request

- ManualSearchUnitID: `MSU-MODELS-2024-COMPANION`
- Publisher: Association for Computing Machinery
- Official proceedings URL: `https://dl.acm.org/doi/proceedings/10.1145/3652620`
- Observed access error: public automated retrieval returned HTTP 403 and did not expose the complete TOC.
- Exact controlled files required: complete publisher proceedings TOC representation and a publisher-generated structured metadata export from the same proceedings when available.
- Preferred export format: saved complete HTML plus publisher-generated BibTeX; RIS or CSV is acceptable only when publisher-generated and complete.
- Required acquisition procedure: human-authenticated institutional access; save unmodified bytes; calculate size and SHA-256; record retrieval time in UTC; place files only at the destinations below.
- Prohibited contents: credentials, cookies, tokens, browser profiles, HAR files, session information, article PDFs, full text, or unauthorized source redistribution.
- Expected local destination: `.local-evidence/models/2024/companion/publisher_primary_toc.html` and `.local-evidence/models/2024/companion/publisher_primary_toc.bib` (or `.ris`/`.csv`).
- Notes: do not commit controlled evidence; publisher HTML defines membership and any structured export is metadata-only unless independently demonstrated to represent the complete TOC.
