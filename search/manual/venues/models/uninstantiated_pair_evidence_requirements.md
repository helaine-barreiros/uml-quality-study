# Evidence requirements for uninstantiated MODELS pairs

The following pairs have evidence that publication occurred, but no official complete publisher proceedings locator was established during this batch. They are therefore not instantiated as `ManualSearchUnit` records.

## 2023 Main

- Official event evidence: `https://conf.researchr.org/track/models-2023/models-2023-technical-track`
- Observed evidence: the official track states that accepted papers are published by IEEE.
- Required before instantiation: an official IEEE conference-publication/volume page that identifies the complete 2023 Main proceedings and supplies a candidate complete `PRIMARY_TOC`.
- Prohibited substitution: individual article pages, DBLP, Crossref, Google Scholar, commercial catalogs, or other aggregators.

## 2025 Main

- Official event evidence: `https://conf.researchr.org/track/models-2025/models-2025-research-papers`
- Observed evidence: the official accepted-paper page links publisher article records, but it is not a publisher TOC.
- Required before instantiation: an official IEEE conference-publication/volume page that identifies the complete 2025 Main proceedings and supplies a candidate complete `PRIMARY_TOC`.
- Prohibited substitution: individual article pages, DOI-pattern inference, commercial catalogs, or aggregators.

## 2025 Companion

- Official event evidence: `https://conf.researchr.org/home/models-2025`
- Observed evidence: official IEEE article records identify publication in MODELS-C 2025, but an article record is not a complete proceedings TOC.
- Required before instantiation: an official IEEE conference-publication/volume page that identifies the complete 2025 Companion proceedings and supplies a candidate complete `PRIMARY_TOC`.
- Prohibited substitution: individual article pages, DOI-pattern inference, commercial catalogs, or aggregators.

No controlled destination or `ManualSearchUnitID` is assigned until the editorial identity is officially verified. Once verified, the unit-specific task must create its controlled-evidence request and use `.local-evidence/models/<year>/<track>/`.
