# MODELS 2024 Main Reconciliation Report

## Unit

ManualSearchUnitID: `MSU-MODELS-2024-MAIN`

## Sources

- PRIMARY_TOC: `SRC-MODELS-2024-MAIN-ACM-TOC-HUMAN-20260811`; <https://dl.acm.org/doi/proceedings/10.1145/3640310>; retrieved `2026-08-11T21:29:05Z`; controlled HTML snapshot SHA-256 `7efdf33b0bb911988956d08f45f902c693ac046949ea570a049e116055702f8e`.
- VENUE_CROSSCHECK: `SRC-MODELS-2024-MAIN-RESEARCHR-TECHNICAL`; <https://conf.researchr.org/track/models-2024/models-2024-technical-track>; retrieved `2026-08-11T21:29:05Z`. Only the Technical Track **Accepted Papers** section was inspected.
- METADATA_SOURCE: `SRC-MODELS-2024-MAIN-ACM-BIBTEX-HUMAN-20260811`; publisher-generated bulk BibTeX from the same ACM proceedings page; retrieved `2026-08-11T21:29:05Z`; controlled snapshot SHA-256 `950537197d9a5d4313ec49b8b1f71a8d5b1175a5b87f4d0117b4f364f56ea86f`.

The earlier automated PRIMARY_TOC attempt (`SRC-MODELS-2024-MAIN-ACM-TOC`) returned HTTP 403 and remains recorded in the source manifest. The controlled HTML is the membership-defining evidence; neither BibTeX nor Researchr was used to create or alter raw membership.

## Documentary counts

- PRIMARY_TOC TotalRawItems: 27
- PRIMARY_TOC FrontMatterItems: 1
- PRIMARY_TOC ResearchArticleItems: 26
- VENUE_CROSSCHECK AcceptedPaperItems: 26
- BibTeXMetadataEntries: 26

The PRIMARY_TOC front-matter item is not compared with Accepted Papers because the latter is a research-paper list. It remains part of the documentary inventory.

## ACM HTML × ACM BibTeX integrity

- DOI set equality: true
- DOI sequence equality: true
- Title sequence equality: true
- HTML duplicate DOI count: 0
- BibTeX duplicate DOI count: 0

This integrity check validates the publisher metadata export against the 26 HTML research-article entries. It does not make BibTeX a membership source.

## ACM research articles × MODELS Accepted Papers

- DOIExactMatchCount: 6
- LiteralTitleMatchCount: 22
- NormalizedTitleMatchCount: 1
- TitleVersionDriftCount: 3
- AuthorListDriftCount: 12
- AmbiguousMatchCount: 0
- PrimaryOnlyResearchArticleCount: 0
- VenueCrosscheckOnlyPaperCount: 0
- MaterialInventoryConflictCount: 0

The diagnostic categories overlap: each DOI exact match in this comparison also has a literal-title match. `NormalizedTitleMatch` uses only Unicode-dash, punctuation, whitespace, and case diagnostics; it does not overwrite either observed title. The three title-version drifts have independent official author and lexical evidence described below, so they do not raise a material documentary-membership conflict.

`AuthorListDrift` is a metadata-presentation diagnostic only. It records a truncation, ordering, or name-form difference among the three official representations; it does not define membership and does not, by itself, imply `MaterialInventoryConflict`.

## Record-level reconciliation

| ManualSearchID | ACMTitleRaw | ACMDOI | ResearchrTitleRaw | ResearchrDOI | MatchEvidence | ReconciliationClass | InventoryConflict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MS-MODELS-2024-MAIN-0002 | Partial Bidirectionalization of Model Transformation Languages | 10.1145/3640310.3674083 | Partial Bidirectionalization of Model Transformation Languages |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0003 | Text2VQL: Teaching a Model Query Language to Open-Source Language Models with ChatGPT | 10.1145/3640310.3674091 | Text2VQL: Teaching a Model Query Language to Open-Source Language Models with ChatGPT |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0004 | 10 years of Model Federation with Openflexo: Challenges and Lessons Learned | 10.1145/3640310.3674084 | 10 years of Model Federation with Openflexo: Challenges and Lessons Learned |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0005 | EditQL: A Textual Query Language for Evolving Models | 10.1145/3640310.3674101 | EditQL: A Textual Query Language for Evolving Models | 10.1145/3640310.3674101 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0006 | Model Everything but with Intellectual Property Protection - The Deltachain Approach | 10.1145/3640310.3674086 | Model Everything but with Intellectual Property Protection—The Deltachain Approach |  | normalized title (Unicode dash/punctuation) | NormalizedTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0007 | AlloyASG: Alloy Predicate Code Representation as a Compact Structurally Balanced Graph | 10.1145/3640310.3674088 | AlloyASG: Alloy Predicate Code Representation as a Compact Structurally Balanced Graph |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0008 | Product Lines of Graphical Modelling Languages | 10.1145/3640310.3674082 | Product Lines of Graphical Modelling Languages |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0009 | Tree-Based versus Hybrid Graphical-Textual Model Editors: An Empirical Study of Testing Specifications | 10.1145/3640310.3674102 | Tree-Based versus Hybrid Graphical-Textual Model Editors: An Empirical Study of Testing Specifications | 10.1145/3640310.3674102 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0010 | Modeling Languages for Automotive Digital Twins: A Survey Among the German Automotive Industry | 10.1145/3640310.3674100 | Modeling Languages for Digital Twins: A Survey Among the German Automotive Industry |  | visible author sequence and lexical title correspondence; see drift details | TitleVersionDrift | No |  |
| MS-MODELS-2024-MAIN-0011 | Advancing Domain-Specific High-Integrity Model-Based Tools: Insights and Future Pathways | 10.1145/3640310.3674094 | Advancing Domain-Specific High-Integrity Model-Based Tools: Insights and Future Pathways | 10.1145/3640310.3674094 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0012 | A Comparative Analysis of Energy Consumption Between Visual Scripting models and C++ in Unreal Engine: Raising Awareness on the importance of Green MDD | 10.1145/3640310.3674099 | A Comparative Analysis of Energy Consumption Between Visual Scripting models and C++ in Unreal Engine: Raising Awareness on the importance of Green MDD |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0013 | Extensions and Scalability Experiments of a Generic Model-Driven Architecture for Variability Model Reasoning | 10.1145/3640310.3674090 | Extensions and Scalability Experiments of a Generic Model-Driven Architecture for Variability Model Reasoning |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0014 | Automated Derivation of UML Sequence Diagrams from User Stories: Unleashing the Power of Generative AI vs. a Rule-Based Approach | 10.1145/3640310.3674081 | Automated Derivation of UML Sequence Diagrams from User Stories: Unleashing the Power of Generative AI vs. Rule-Based Approach |  | visible author sequence and lexical title correspondence; see drift details | TitleVersionDrift | No |  |
| MS-MODELS-2024-MAIN-0015 | AI-Driven Consistency of SysML Diagrams | 10.1145/3640310.3674079 | AI-Driven Consistency of SysML Diagrams |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0016 | Toward Intelligent Generation of Tailored Graphical Concrete Syntax | 10.1145/3640310.3674085 | Toward Intelligent Generation of Tailored Graphical Concrete Syntax | 10.1145/3640310.3674085 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0017 | Enhancing Automata Learning with Statistical Machine Learning: A Network Security Case Study | 10.1145/3640310.3674087 | Enhancing Automata Learning with Statistical Machine Learning: A Network Security Case Study |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0018 | ModelMate: A recommender for textual modeling languages based on pre-trained language models | 10.1145/3640310.3674089 | ModelMate: A recommender for textual modeling languages based on pre-trained language models | 10.1145/3640310.3674089 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0019 | Towards Runtime Monitoring for Responsible Machine Learning using Model-driven Engineering | 10.1145/3640310.3674092 | Towards Runtime Monitoring for Responsible Machine Learning using Model-driven Engineering | 10.1145/3640310.3674092 | DOI exact; literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0020 | A DSL for Testing LLMs for Fairness and Bias | 10.1145/3640310.3674093 | A DSL for Testing LLMs for Fairness and Bias |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0021 | Give me some REST: A Controlled Experiment to Study Effects and Perception of Model-Driven Engineering with a Domain-Specific Language | 10.1145/3640310.3674080 | Give me some REST: A Controlled Experiment to Study Effects and Perception of Model-Driven Engineering with a Domain-Specific Language |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0022 | EpiMDE: A-Model Driven Engineering Platform for Epidemiological Modeling | 10.1145/3640310.3674104 | EpiMDE: A Model Driven Engineering Platform for Epidemiological Modeling |  | visible author sequence and lexical title correspondence; see drift details | TitleVersionDrift | No |  |
| MS-MODELS-2024-MAIN-0023 | Mutation Testing of Java Bytecode: A Model-Driven Approach | 10.1145/3640310.3674103 | Mutation Testing of Java Bytecode: A Model-Driven Approach |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0024 | Towards Automated Test Scenario Generation for Assuring COLREGs Compliance of Autonomous Surface Vehicles | 10.1145/3640310.3674098 | Towards Automated Test Scenario Generation for Assuring COLREGs Compliance of Autonomous Surface Vehicles |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0025 | AutoMW: Model-based Automated Medical Writing | 10.1145/3640310.3674096 | AutoMW: Model-based Automated Medical Writing |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0026 | Requirement-Driven Generation of Distributed Ledger Architectures | 10.1145/3640310.3674097 | Requirement-Driven Generation of Distributed Ledger Architectures |  | literal title | LiteralTitleMatch | No |  |
| MS-MODELS-2024-MAIN-0027 | Meta-Modelling Kindness | 10.1145/3640310.3674095 | Meta-Modelling Kindness |  | literal title | LiteralTitleMatch | No |  |

## Author-list drift details

| ManualSearchID | ACM HTML visible authors | ACM HTML additional-author indicator | ACM BibTeX complete authors | Researchr authors | Interpretation |
| --- | --- | --- | --- | --- | --- |
| MS-MODELS-2024-MAIN-0004 | Jean-Christophe Bach; Antoine Beugnard; Joël Champeau; Fabien Dagnat | 2 | Jean-Christophe Bach; Antoine Beugnard; Joël Champeau; Fabien Dagnat; Sylvain Guérin; Salvador Martínez | Jean-Christophe Bach; Antoine Beugnard; Joel Champeau; Fabien Dagnat; Sylvain Guérin; Salvador Martínez | HTML truncation; BibTeX and Researchr present the same complete ordered list, apart from diacritic rendering. |
| MS-MODELS-2024-MAIN-0009 | Ionut Predoaia; James Harbin; Simos Gerasimou; Christina Vasiliou | 2 | Ionut Predoaia; James Harbin; Simos Gerasimou; Christina Vasiliou; Dimitris Kolovos; Antonio García-Domínguez | Ionut Predoaia; James Harbin; Simos Gerasimou; Christina Vasiliou; Dimitris Kolovos; Antonio Garcia-Dominguez | HTML truncation; BibTeX and Researchr present the same complete ordered list, apart from diacritic rendering. |
| MS-MODELS-2024-MAIN-0010 | Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann | 4 | Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann; Christer Neimöck; Christian Seiler; Anne Koziolek; Andreas Wortmann | Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann; Christer Neimöck; Christian Seiler | HTML truncation; the first five visible HTML authors align with the first five BibTeX and Researchr authors. BibTeX contains nine authors, whereas Researchr presents seven; this is recorded as metadata-presentation drift and does not make paper identity ambiguous. |
| MS-MODELS-2024-MAIN-0011 | Qurat ul ain Ali; Dimitris Kolovos; Antonio Garcia-Dominguez; Michael Bennett | 2 | Qurat ul ain Ali; Dimitris Kolovos; Antonio Garcia-Dominguez; Michael Bennett; Joe Newton; Piotr Zacharzewski | Qurat Ul Ain Ali; Dimitris Kolovos; Antonio Garcia-Dominguez; Michael Bennett; Joe Newton; Piotr Zacharzewski | HTML truncation; BibTeX and Researchr present the same complete ordered list, with capitalization variation. |
| MS-MODELS-2024-MAIN-0012 | Javier Verón; Carlos Pérez; Coral Calero; MaÂngeles Moraga; Francisca Pérez | 1 | Javier Verón; Carlos Pérez; Coral Calero; MaÂngeles Moraga; Francisca Pérez; Carlos Cetina | Javier Verón Mérida; Carlos Pérez; Coral Calero; Mª Angeles Moraga; Francisca Pérez; Carlos Cetina | HTML truncation plus name-form differences in Researchr; the ordered documentary correspondence remains clear. |
| MS-MODELS-2024-MAIN-0014 | Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran | 3 | Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran; Chanchal Roy; Banani Roy; Kevin Schneider | Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran; Chanchal K. Roy; Banani Roy; Kevin Schneider | HTML truncation; BibTeX omits the middle initial shown by Researchr for Chanchal K. Roy. |
| MS-MODELS-2024-MAIN-0015 | Bastien Sultan; Ludovic Apvrille | none | Bastien Sultan; Ludovic Apvrille | Ludovic Apvrille; Bastien Sultan | Researchr reverses the displayed order; author membership is otherwise the same. |
| MS-MODELS-2024-MAIN-0016 | Meriem Ben Chaaben; Oussama Ben Sghaier; Mouna Dhaouadi; Nafisa Elrasheed | 5 | Meriem Ben Chaaben; Oussama Ben Sghaier; Mouna Dhaouadi; Nafisa Elrasheed; Ikram Darif; Imen Jaoua; Bentley Oakes; Eugene Syriani; Mohammad Hamdaqa | Meriem Ben Chaaben; Oussama Ben Sghaier; Mouna Dhaouadi; Nafisa Elrasheed; Ikram Darif; Imen Jaoua; Bentley Oakes; Eugene Syriani; Mohammad Hamdaqa | HTML truncation; BibTeX and Researchr present the same complete ordered list. |
| MS-MODELS-2024-MAIN-0018 | Carlos Durá Costa; José Antonio Hernández López; Jesús Sánchez Cuadrado | none | Carlos Durá Costa; José Antonio Hernández López; Jesús Sánchez Cuadrado | Carlos Durá; José Antonio Hernández López; Jesús Sánchez Cuadrado | Researchr presents a shortened form of the first author's name. |
| MS-MODELS-2024-MAIN-0022 | Bruno Curzi-Laliberté; Marios Fokaefs; Michalis Famelis; Mohammad Hamdaqa | none | Bruno Curzi-Laliberté; Marios Fokaefs; Michalis Famelis; Mohammad Hamdaqa | Bruno Curzi-Laliberté; Marios-Eleftherios Fokaefs; Michalis Famelis; Mohammad Hamdaqa | Researchr presents an expanded form of Marios Fokaefs's name. |
| MS-MODELS-2024-MAIN-0025 | Asha Rajbhoj; Ajim Pathan; Tanay Sant; Vinay Kulkarni; Padmalata Nistala | 3 | Asha Rajbhoj; Ajim Pathan; Tanay Sant; Vinay Kulkarni; Padmalata Nistala; Rajesh Pandey; Sabarinathan Narasimhan; Geetha Thiagarajan | Asha Rajbhoj; Ajim Pathan; Tanay Sant; Vinay Kulkarni; Padmalata Nistala; Rajesh Pandey; Sabarinathan Narasimhan; Geetha Thiagarajan | HTML truncation; BibTeX and Researchr present the same complete ordered list. |
| MS-MODELS-2024-MAIN-0026 | Noor Mohammed Sabr Al-Gburi; András Földvári; Kristóf Marussy; Oszkár Semeráth | 1 | Noor Mohammed Sabr Al-Gburi; András Földvári; Kristóf Marussy; Oszkár Semeráth; Imre Kocsis | Noor Mohammed Sabr Al-Gburi; András Földvári; Kristóf Marussy; Oszkár Semeráth; Imre Kocsis | HTML truncation; BibTeX and Researchr present the same complete ordered list. |

## Title-version drift details

### MS-MODELS-2024-MAIN-0010

- ACM final title: `Modeling Languages for Automotive Digital Twins: A Survey Among the German Automotive Industry`
- Researchr accepted-paper title: `Modeling Languages for Digital Twins: A Survey Among the German Automotive Industry`
- ACM HTML visible authors: Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann; additional-author indicator: `+ 4`.
- ACM BibTeX complete authors: Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann; Christer Neimöck; Christian Seiler; Anne Koziolek; Andreas Wortmann.
- Researchr accepted-paper authors: Jérôme Pfeiffer; Dominik Fuchß; Thomas Kühn; Robin Liebhart; Dirk Neumann; Christer Neimöck; Christian Seiler.
- DOI: ACM `10.1145/3640310.3674100`; no DOI is displayed in the Researchr Accepted Papers record.
- Evidence: shared ordered visible authors and the same lexical title frame identify one paper.
- Interpretation: the added `Automotive` qualifier is treated as final-title evolution, not a change in documentary membership.

### MS-MODELS-2024-MAIN-0014

- ACM final title: `Automated Derivation of UML Sequence Diagrams from User Stories: Unleashing the Power of Generative AI vs. a Rule-Based Approach`
- Researchr accepted-paper title: `Automated Derivation of UML Sequence Diagrams from User Stories: Unleashing the Power of Generative AI vs. Rule-Based Approach`
- ACM HTML visible authors: Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran; additional-author indicator: `+ 3`.
- ACM BibTeX complete authors: Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran; Chanchal Roy; Banani Roy; Kevin Schneider.
- Researchr accepted-paper authors: Munima Jahan; Mohammad Mahdi Hassan; Reza Golpayegani; Golshid Ranjbaran; Chanchal K. Roy; Banani Roy; Kevin Schneider.
- DOI: ACM `10.1145/3640310.3674081`; no DOI is displayed in the Researchr Accepted Papers record.
- Evidence: identical ordered author list and title differing only by the article `a`.
- Interpretation: the wording difference is treated as final-title evolution, not a change in documentary membership.

### MS-MODELS-2024-MAIN-0022

- ACM final title: `EpiMDE: A-Model Driven Engineering Platform for Epidemiological Modeling`
- Researchr accepted-paper title: `EpiMDE: A Model Driven Engineering Platform for Epidemiological Modeling`
- ACM HTML visible authors: Bruno Curzi-Laliberté; Marios Fokaefs; Michalis Famelis; Mohammad Hamdaqa; additional-author indicator: none.
- ACM BibTeX complete authors: Bruno Curzi-Laliberté; Marios Fokaefs; Michalis Famelis; Mohammad Hamdaqa.
- Researchr accepted-paper authors: Bruno Curzi-Laliberté; Marios-Eleftherios Fokaefs; Michalis Famelis; Mohammad Hamdaqa.
- DOI: ACM `10.1145/3640310.3674104`; no DOI is displayed in the Researchr Accepted Papers record.
- Evidence: identical ordered author list and title differing by the publisher-side hyphenation after `A`.
- Interpretation: the wording difference is treated as final-title evolution, not a change in documentary membership.
