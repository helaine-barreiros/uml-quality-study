# Protocol v2.0 changelog

Date: 2026-08-21
Applies to: `appendix_two_layer_mapping_protocol_v2_0.tex` only. The v1.7 `.tex` is not edited.

Amendments are not maintained for v2.0. The review is not in its reporting phase, and the
PRISMA amendment record is reopened when execution begins. This file is the working record of
what changed and why, and it is not an amendment.

## Terminology: attribute, deviation, and measure

- Added `Attributes, deviations, and measures`, a subsection of Operational definitions, stating
  the spine `attribute -> deviation -> reference -> unit -> indicator -> procedure -> aggregation`
  and assigning SQ1 the first link, SQ2 the second, and SQ3 the remainder. The chain already
  existed in the SQ3 synthesis subsection, uncited and starting one link too late; it is now
  anchored on ISO/IEC/IEEE 15939, ISO/IEC 25020, and SWEBOK v4.
- Stipulated `Inadequacy` in the glossary as the umbrella for a deviation on any of the three
  axes, excluding by name two readings already occupied: the negation of `pragmatic adequacy`,
  which is the use axis alone, and the `adequacy` of natural language generation evaluation,
  which is the semantic axis alone. `Defect`, `fault`, `anomaly`, and `nonconformity` are
  declined with stated reasons.
- Named the deviation per axis: nonconformity on L, invalidity and incompleteness on D,
  inadequacy in the strict sense on U. Anchored L and D on verification and validation.
- Restated syntax-semantic dissonance as the co-occurrence of conformity on L with deviation on
  D, computed from the axes rather than asserted as a further construct.
- Removed five deviation labels and two effort quantities from the `Normalized construct`
  vocabulary, which now admits attributes only, and aligned `SemanticQualityConstruct` with it.
  `unsupported addition` had been present verbatim in the SQ1 and the SQ2 vocabularies, twelve
  lines apart in one table.
- Wrote the duality rule and the asymmetry rule: a deviation reported without a named attribute
  leaves the attribute not reported, and that asymmetry is a finding of SQ1.
- Added seven standards to the bibliography.

## Title

- Single-sourced the title, which existed as three disagreeing strings. `\reviewtitle` now holds
  the review object, the chapter and the identification table derive from it.
- New title: `Quality constructs, deviations, and measures in LLM-generated UML diagrams: a
  systematic mapping study`. The previous title promised the quality of LLM-generated UML, which
  the review does not measure, contradicting the protocol's own limitation clause.

## Research questions

- **MQ4** asked for five objects and owned one. `evaluation dimensions` had no field at all,
  having been removed from field 26 as derived; `human roles` belong to SQ5, `automated
  procedures` to SQ3, and `open science practices` to MQ1. MQ4 is narrowed to the baseline
  condition, which is the only field it owns, and its traceability row follows. Nothing is lost
  from the review: every removed object is still asked by the question that owns its field.
- **SQ2** did not ask for the violated reference, although its traceability row required it and
  the codebook names that field as where syntax-semantic dissonance becomes observable. Added.
- **SQ3** claimed `evaluators`, which is SQ5's field, and named the reference `semantic
  references`, colliding with SQ2's violated reference. Now `evaluation references`, matching
  field 41, and the human evaluator is left to SQ5.

## Selection and gates, through Gate C

- Reconciled a contradiction stated twice on each side. The protocol held both that a filter
  undecidable at title and abstract is answered from the full text, and that C1 is the only
  exclusion available at Gate C, while full-text screening allowed any primary exclusion
  criterion. Resolution: a deferred filter remains a filter of its own gate. Full-text screening
  performs two distinct operations recorded in different fields, namely resolving deferred Gate A
  and Gate B filters at the filter that owns the criterion, and answering C1, which is reached
  only by reports that passed Gate B. This matches the recorded data, in which every B code lives
  in the gate B outcome field, and the extraction form, which offers only `ELEGIVEL` and `C1_E12`
  at C1.
- Repaired a truncated sentence introducing the Filter column, a `mus` for `must`, an `above` for
  `below` preceding the exclusion table, and a `must presented` for `must be presented`. Anchored
  the fixed-order invariant on the gate table instead of on the word `below`.

## Reviewers

- The identification table carried placeholders for review team, methodological supervisor, and
  domain adjudicator while `Researchers involved` named all five people with their roles. Same
  object, two places, one of them empty. The identification table now points to the roles table.
  The registration repository stays a placeholder, because it is a genuine open item and not a
  duplication.

## Sections restored to v2.0

- Added `Protocol validation`, `Threats to validity and mitigation`, and `Protocol validation
  checklist`, which v1.7 had and v2.0 did not. Validation is stated as a precondition for
  execution rather than as a report of it, and the checklist is split at the point that matters
  now: V01 to V09 before production screening, V10 to V14 before extraction.
- The threats table carries four rows that v1.7 did not: retrieval loss as an attrition stratum,
  pole confusion, stipulated terminology, and unit misalignment. The `Selective protocol change`
  row is rewritten around what v2.0 actually does, namely the version changelog plus executable
  locks, since amendments are not maintained.
- V02 is written so that it fails while a question names an object it does not own, which is the
  checklist counterpart of the `POSSE` lock.

## Two decisions taken

- **Reviewer role concentration.** The assignments in the roles table are kept, because they
  reflect what the researchers agreed to do, and the concentration is declared instead of hidden.
  Two rules make it auditable: validation is dated and completed before the activity it
  validates, so no rule is approved after its consequences are visible; and an adjudication that
  turns on a protocol rule names the validator who approved that rule. The UML domain validator
  holds no adjudication role and is therefore the independent check on codebook boundaries, UML
  carrier categories, and reference distinctions.
- **Attrition cut-off.** Written as an absolute date, 1 September 2026, replacing `is unchanged`,
  which referred to a value stated nowhere in v2.0. A text arriving after the cut-off is recorded
  with its arrival date and reported in the sensitivity analysis rather than folded into the
  corpus.

## Whole-document consistency pass

Six inconsistencies found by reading v2.0 as a unit and corrected.

- `Human involvement` was still a field of the mapping table. A005 had merged it into
  `HumanEvaluatorRole`, six of its seven values being that same vocabulary, and the codebook
  carried the merge while the protocol did not. Since MQ4 no longer asks for human roles, the row
  was also orphaned. Removed.
- `NotationFamily` existed in the codebook, owned by MQ2, and was absent from the protocol. Added
  to the mapping table. It keeps what filter B5 discards, namely which other notation the
  separable UML contribution stood beside, and it is what says against which definition of the
  language syntactic conformity was assessed.
- `Reported severity or task effect` existed in the codebook and was absent from the protocol,
  although the coding tuple makes severity its fourth dimension. Added, anchored on the tuple, and
  stated as left empty rather than imputed when no severity is reported.
- The three axis value lists were enumerated twice, in the axes table and again in the extraction
  form. The axes subsection states that repeating an enumeration is what lets two enumerations
  drift, and then repeated one. The extraction form now names the three fields in one row and
  points to the axes table.
- `eq:protocol_quality_spine` was a label nobody referenced. The metric catalogue now cites the
  equation rather than only the section.
- Hyphenation normalized where the document disagreed with itself: `LLM-based`, `well-formedness`,
  `co-occurrence`, `rule-based`, `full-text screening`.

After the pass, the field lists of the protocol and of the codebook correspond exactly: 63 rows
for 65 fields, the difference being the three axis fields collapsed into one row by design.

## Information sources restored

- `\section{Search process}` carried `\label{sec:protocol_sources}` from v1.7 while the 409 lines
  it labelled were gone. v2.0 went straight from the section heading into the Scopus string, so
  it named no sources, no seed set, and no citation-searching route, while three other places
  referred to routes it did not specify and V05 and V06 of the new checklist had nothing to be
  checked against.
- Added `Information sources` as the first subsection of Search process: the complementary-route
  rationale with its citations, a source table, the prespecified seed set SE1 to SE5, a citation
  searching procedure, and source contribution and retention analysis. It is adapted rather than
  copied: v2.0 already holds the search strings and the core venue table, so those are referenced
  and not repeated.
- The source table reports what was executed, namely Scopus, IEEE Xplore, ACM Digital Library,
  citation searching, and manual venue inspection, and marks Web of Science, ScienceDirect, and
  arXiv `Decision pending`. They were planned in v1.7 and did not contribute to the corpus of 986
  records, which is ACM 454, IEEE 283, and Scopus 249. Recording a decision that was never taken
  would have been worse than recording the gap.
- Restored the conditional venue rows and the promotion rule to the existing venue table, which
  v2.0 had reduced to the four core rows while V15 still referred to conditional activation.

## Codebook aligned to v2.0

- **Twenty-four line-number references removed from the extraction rules.** They pointed into
  v1.7, and they were already wrong there: the rule for field 47 cited `l. 185` for the
  language-semantics-task trichotomy, and by the current numbering `l. 185` is `Semantic
  completeness`. The three translation keys recorded for v1.7 had shifted every reference past
  line 117 without anything noticing, because nothing checks a line number. Every reference is now
  a named anchor: a section, a subsection, an operational definition, an enumeration, or an
  equation label. All seventeen distinct anchors are verified to exist in the `.tex`.
- Field 49 no longer claims to be outside the two extraction tables, which stopped being true when
  severity was added to the quality-evidence table.
- `participant` was a value of `HumanEvaluatorRole` that lived only in the codebook, because the
  A005 merge took it from the removed `Human involvement` row and the protocol never received it.
  Removing the duplicate row exposed it. Restored to the protocol.
- After the pass, no value admitted by the codebook is absent from the protocol rule for the same
  field, and no field is owned by a question that does not exist in v2.0.

## Full-text screening brought up to the rigour of title and abstract screening

Three gaps had the same shape: the protocol specified title and abstract screening far more
tightly than full-text screening, and full-text screening is what executes next.

- **A concordant `unclear` had no destination.** Only disagreement was handled, so two reviewers
  agreeing that they cannot decide left the report in limbo. It now has its own rule: retained,
  never excluded, referred to adjudication with the question that could not be answered; and if
  adjudication cannot resolve it either, retained with the residual uncertainty carried into
  extraction as a flag, so it is visible in the synthesis rather than settled by default. This
  matters most at C1, whose question is answered from reported results rather than from a claim.
- **No agreement was measured at full text.** It is now measured and reported separately from
  title and abstract, computed over the primary decision and, for exclusions, over the filter at
  which the exclusion was recorded, because agreeing that a report is ineligible while disagreeing
  about which filter excludes it is a disagreement about the criteria. Concordant `unclear`
  decisions are counted alongside the coefficient and never absorbed into it. Failing the
  threshold triggers revision of the eligibility manual rather than sample expansion, since every
  retained report is already dual screened.
- **Calibration is now performed twice, once per reading moment.** Whether a generation instance
  is identifiable is a question that title and abstract calibration never asks, so it cannot
  license full-text screening. Neither calibration substitutes for the other and each is dated.
  V09 was rewritten to require both.

## Two citations kept rather than removed

Both were orphaned in v2.0, and inspecting them reversed the decision to drop them.

- `Yang2024MultiStepDomainModeling` was the diagnostic false-negative that caused the ACM
  validation to **reject** restricting the UML block to title, abstract, and author keywords: an
  eligible model-generation study exposing no UML terminology in those fields. It is record
  `061_ACM`, retained, past Gate B, with full text. The fact is restored to the ACM search
  strategy, because without it the breadth of that query reads as arbitrary rather than as the
  concrete form of the rule that no filter may operate on the dependent variable.
- `Gheorghita2025Diagrams` is within scope, published in an Elsevier venue, and retrieved by no
  executed source. It is recorded in the source contribution analysis so that the coverage gap of
  the unactivated complementary sources is a named absence rather than a hypothesis.
- The bibliography now has no uncited entry.

## Verification

- Added `analysis/scripts/verifica_protocolo_v2.py`, 36 locks over v2.0. `verifica_protocolo.py`
  is unchanged and continues to verify v1.7. Four lock families are new, one per failure found on
  2026-08-21: `POLO` (the SQ1 and SQ2 vocabularies share no label), `POSSE` (every object named in
  a question text has a field with that owner in the codebook), `TITULO` (single-sourced), and
  `PORTAO_C` (E12 is the only exit, and deferring a filter does not move it to another gate).
- `POSSE` is the lock that would have caught MQ4. It grows when another object costs an error.

## Cross-references and rendering

- `\ref{sec:protocol_scope}` at the axes subsection resolved to the units table rather than to
  the operational definitions, because the v2.0 rewrite split one section into two and only the
  first kept a label. It resolved, so the build could not catch it. Added
  `\label{sec:protocol_definitions}` and repointed.
- Repaired the Introduction: five language errors, and a past tense that contradicted the
  declared `Prospective protocol` status.
- `gera_pdf_protocolo.sh` takes an optional base name, default unchanged, with one wrapper per
  base, so v1.7 and v2.0 both render.

## Open, not applied

- `verifica_protocolo.py` still verifies v1.7, with fourteen locks bound to v1.7 line numbers and
  a hardcoded line count. It does not verify v2.0.
- v2.0 has no protocol validation, threats to validity, or validation checklist section; v1.7
  has all three.
- `\providecommand{\partial}{\textit{Partially}}` is a silent no-op, `\partial` being already
  defined by LaTeX. Unused today.
