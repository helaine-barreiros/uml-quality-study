# Controlled evidence request — MSU-REFSQ-2025

- ManualSearchUnitID: `MSU-REFSQ-2025`
- CurrentEvidence: Partial Springer book page 1 with 20 local cards, validated aggregate publisher BibTeX with 29 records, and official session-level REFSQ research-track program evidence.
- MissingEvidence: Complete official Springer PRIMARY_TOC with every TOC page and every front-matter and chapter item locally materialized.
- ReasonRequired: The received page exposes uncaptured page 2 and cannot establish complete documentary membership. BibTeX and program records cannot infer the missing membership or its publisher order.
- PreferredAcquisitionProcedure: Open the specific Springer book page, save every TOC pagination page or use an official all-chapters view that locally materializes the complete ordered TOC, and preserve the canonical book URL. If the browser cannot capture all pages together, save each page separately without cookies, HAR files, tokens, or browser profiles.
- ExpectedFilename: `publisher_primary_toc_complete.html` or `publisher_primary_toc_page_001.html`, `publisher_primary_toc_page_002.html`, and any further observed pages.
- ExpectedLocalDestination: `.local-evidence/refsq/2025/`
- ProhibitedContents: Credentials, cookies, HAR files, tokens, browser profiles, abstracts, keywords, PDFs, or full text are not requested.
- Notes: Do not reacquire the BibTeX or research-track page already validated.
