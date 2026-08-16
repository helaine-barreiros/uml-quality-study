# A003: Quality-focused eligibility and extraction-based synthesis clarification

- AmendmentID: `A003`
- DecisionDate: `2026-08-15`
- RecordedAt: `2026-08-15T21:07:03Z`
- Stage: Before formal screening
- Status: `Applied`
- RecordedCommit: `ea54a33f72cfc0c85619d6588266be1b4b5cd9dd`
- PreviousRecordedCommit: `59de5de4f90165e05182c016194e8fb64fb58756`
- RevisionID: `A003-R1`
- RevisionDecisionDate: `2026-08-15`
- RevisionRecordedAt: `2026-08-16T01:36:59Z`
- RevisionRecordedCommit: `3104220bc71452b874fb229f4bdadf440f3d4026`
- DoesNotChange:
  - search strings
  - information sources
  - review interval
  - manual collection status
  - A001
  - A002
  - collected inventories
- Changes:
  - protocol framing
  - inclusion criteria
  - exclusion criteria
  - extraction fields
  - synthesis terminology

## Revised decision

The review is a focused systematic mapping study with structured extraction and synthesis of quality evidence in LLM-based UML diagram generation. It uses a single eligible corpus rather than separate eligibility layers.

The revision:

- removes the previous terminology that divided eligibility and synthesis into two named layers;
- establishes extractable quality evidence as an inclusion requirement;
- adds E11 for reports that do not provide extractable evidence about the quality, validity, correctness, completeness, consistency, pragmatic adequacy, or correction of generated UML content;
- records PlantUML explicitly during extraction without treating it as the only acceptable representation when other explicit and separable UML content can be assessed;
- adds extraction fields for generation context, syntactic quality, semantic quality, metrics, evaluation references, correction or rework, and syntax-semantic dissonance;
- derives analytical subsets from extraction fields without redefining the eligible corpus.

## Rationale

The revised framing aligns eligibility with the study's quality-focused objective and avoids maintaining a broader mapping corpus whose reports provide no extractable quality evidence. Syntactic quality, semantic quality, and syntax-semantic dissonance remain analytical phenomena operationalized during extraction rather than separate eligibility structures.

The validated search strings and the planned information sources are unchanged. The broad retrieval strategy remains appropriate because reports may evaluate quality without using explicit syntactic or semantic terminology in titles, abstracts, or keywords.

## Substantive LLM use boundary

- Model labels are not sufficient for inclusion.
- Encoder-only models, including BERT-like and RoBERTa-like models, used only as classifiers, taggers, embedding generators, entity extractors, relation extractors, or supervised preprocessing components are excluded under E6.
- Hybrid neural-symbolic pipelines are included only when the LLM determines, proposes, or revises the semantic content of the generated UML diagram.
- Ambiguous title and abstract cases are retained for full-text screening.
- The decision clarifies I2 and E6 without changing search strings, information sources, the review interval, or collected inventories.

## Historical provenance

`PreviousRecordedCommit` preserves the commit that recorded the earlier A003 formulation. The current `RecordedCommit` identifies the commit that introduces the revised quality-focused decision before any formal screening. `RevisionRecordedCommit` identifies the subsequent clarification of the substantive LLM-use boundary.
