# Controlled evidence request

- ManualSearchUnitID: `MSU-MODELS-2022-COMPANION`
- Publisher: Association for Computing Machinery
- Official proceedings URL: `https://dl.acm.org/doi/proceedings/10.1145/3550356`
- Observed access error: public automated retrieval returned HTTP 403 and did not expose the complete TOC.
- Exact controlled files required: complete publisher proceedings TOC representation and, when available, a publisher-generated structured metadata export from the same proceedings.
- Preferred export format: saved complete HTML plus publisher-generated BibTeX; RIS or CSV is acceptable only when publisher-generated and complete.
- Required acquisition procedure: human-authenticated institutional access; save the unmodified source bytes; calculate size and SHA-256; record retrieval time in UTC; place files only at the destinations below.
- Prohibited contents: credentials, cookies, tokens, browser profiles, HAR files, session information, article PDFs, full text, or any source whose acquisition/retention is not authorized.
- Expected local destination: `.local-evidence/models/2022/companion/publisher_primary_toc.html` and `.local-evidence/models/2022/companion/publisher_primary_toc.bib` (or the corresponding `.ris`/`.csv`).
- Notes: do not commit controlled evidence; the publisher TOC must define membership and the structured export must not independently create membership.
