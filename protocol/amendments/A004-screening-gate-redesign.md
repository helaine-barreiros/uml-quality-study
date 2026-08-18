# A004: Screening gate redesign and eligibility criteria realignment

- AmendmentID: `A004`
- DecisionDate: `2026-08-17`
- RecordedAt: `2026-08-17T00:00:00-03:00`
- Stage: During screening, after Gates A and B were completed over the automated corpus and before Gate C reading begins
- Status: `Applied`
- PreviousRecordedCommit: `18505cbaae3318a5076abea76b8d8899758ae352`
- RecordedCommit: `73e8b8335422c55c3c8597149e91edc84981046f`
- AppliedOn: `2026-08-17`
- HeaderCorrection: Both fields above were corrected on 2026-08-18. `RecordedCommit` had never been filled in after the placeholder was written, and `Status` still read "Approved, application pending" although every item of Section 8 was completed on 2026-08-17. Only the header was touched; no decision, rationale or table in this amendment was altered. The correction is recorded in the decision log.
- DoesNotChange:
  - search strings
  - information sources
  - review interval
  - temporal and language scope
  - manual collection status
  - A001
  - A002
  - the recorded exclusion decisions of the automated corpus (see Section 6)
- Changes:
  - the screening gate structure
  - inclusion criteria
  - exclusion criteria
  - the status of full-text unavailability
  - extraction fields
  - the definition of the analytical subsets

## Summary

This amendment records five design decisions, referred to during deliberation as
alpha, beta, gamma, delta and epsilon. Together they restructure screening so
that each decision point has exactly one question, one inclusion criterion and
one exclusion criterion, and so that no eligibility filter operates on the
review's own dependent variable.

| | Decision | Effect |
|---|---|---|
| alpha | E11 is withdrawn | evidence of quality becomes a three-axis extraction variable |
| beta | E10 is withdrawn; E7 is split | the notation-mixture clause returns to Gate B; separability of the generation instance becomes the single Gate C exclusion |
| gamma | E5 is withdrawn | full-text unavailability becomes attrition, not exclusion |
| delta | I1 and I5 are split; I6 is withdrawn | the inclusion table is realigned one-to-one with the exclusion table |
| epsilon | numbering regime | exclusion codes are frozen; inclusion codes are renumbered in filter order |

## 1. Alpha: quality evidence ceases to be an eligibility filter

A003 established extractable quality evidence as an inclusion requirement and
introduced E11. This amendment withdraws E11 and, by delta, the corresponding
I6.

### Rationale

The review's own research questions do not all require quality evidence. MQ1,
MQ2 and MQ3 are descriptive and answerable without it. MQ4 asks what is reported
across the mapped studies, so absence is itself an answer. **MQ5 asks which
combinations remain under investigated**: a gap analysis run over a corpus that
was filtered by evidence reporting would report the review's own filter as a gap
in the literature. The protocol already states, in the paragraph following the
criteria tables, that the review does not define a second eligibility layer and
that analytical subsets are classified during data extraction; E11 contradicted
that sentence.

Three operational arguments reinforce the decision. E11 was the only graded
criterion with no stated threshold, and therefore the worst candidate for
inter-rater agreement. It was the only criterion requiring exhaustive reading
before it could be applied, giving it the worst possible cost profile: read the
whole text, then discard it. And filtering by outcome reporting is a habit of
systematic reviews of effects, imported into a mapping study where it does not
belong.

### Replacement

Quality evidence is recorded during extraction on three axes, derived from the
protocol's operational definitions, and never collapsed into a single scale:

| Axis | Krogstie relation | Values |
|---|---|---|
| **L** language | model to language | `ausente`, `validade_textual`, `conformidade_uml` |
| **D** domain | model to domain | `ausente`, `alegada`, `requisitos_fonte`, `modelo_referencia`, `julgamento_especialista`, `rubrica` |
| **U** use | model to interpreter and use | `ausente`, `alegada`, `compreensao`, `atividade_engenharia`, `retrabalho` |

The three axes are kept separate because folding pragmatic adequacy into the
domain axis would repeat the failure that produced the E6 dump: a fused question
yields a fused code and the distinction becomes unrecoverable.

The evaluative subset is now defined rather than presumed:

| Questions | Subset |
|---|---|
| MQ1 to MQ5 | the whole eligible corpus |
| SQ1 to SQ3 | `D` is not `ausente` |
| **SQ4** | `L` is not `ausente` **and** `D` is not `ausente` |
| SQ6 | `U` is not `ausente` |

SQ4 asks to what extent the reported evidence distinguishes syntactic from
semantic quality. Under E11 that subset was assumed; under the axes it is
computed. Procedure, reliability and validity information goes to SQ5 extraction
fields, not to the axes.

## 2. Beta: separability is decided in two places, for two different reasons

E7 as published contains two clauses: the output is not UML, and no separable
UML result is reported, the latter illustrated by C4, ER, BPMN, SysML,
architecture sketches and Mermaid. E10 covered a different mixture: UML results
that cannot be separated from other generated artifacts, tasks or outputs.

The two are not the same. E7's second clause is mixture with **another
notation**, decidable from title and abstract. E10 is mixture with **other
artifacts or tasks**, decidable only from results in the full text.

E10 also carried alpha's defect: it required exhaustive reading before it could
be applied.

### Decision

- The notation-mixture clause returns to Gate B as filter **B5**, with code
  **E7b**.
- E10 is withdrawn. Its content is split into filter **C1**, "is there an
  identifiable generation instance?", which becomes the **only exclusion at Gate
  C**, plus an extraction attribute `atribuicao do resultado`, with values
  `atribuivel_ao_uml`, `agregado_com_outros_artefatos` and `nao_reportado`.

The consequence is accepted explicitly: the eligible corpus becomes essentially
determined at Gate B, and Gate C becomes a classification table with a single
exit. This trades corpus volume for fidelity of the map.

## 3. Gamma: full-text unavailability becomes attrition

E5 is withdrawn as an exclusion criterion. Reports whose full text is not
obtained after the documented access procedure of Section 10 of
`screening_manual_v1.md` are placed in a stratum named **"identificado, nao
recuperado"**. They do not receive `excluded=true` and they do not receive an
exclusion code.

### Rationale

Every other criterion predicates something of the report: its year, its type,
its object, the role of the model, its separability. E5 predicates something of
the reviewer's access within a time window. Reporting "excluded by E5: 53" reads
as "53 ineligible", when the correct statement is "53 eligible reports I could
not read". PRISMA 2020 already separates the two into distinct boxes: *Reports
not retrieved* precedes and is disjoint from *Reports excluded, with reasons*.

The decisive argument is empirical. Among the 137 reports retained after Gates A
and B, 84 have full text and 53 do not, and the loss is systematic in three
dimensions:

| Dimension | Observed pattern |
|---|---|
| Access model | **zero** OPEN records among the 53 (50 CLOSED); 42 OPEN among the 84 |
| Type and source | journal 25/30 (83%) vs conference 58/105 (55%); ACM 96%, Scopus 55%, IEEE 40% |
| Recency | 2024: 79% retrieved; 2025: 53%; 2026: 62% |

The recency bias is the most damaging, because the object of the review is a
fast-moving literature and the most recent slice is the most informative about
model families and prompting strategies. An exclusion code would hide all three
asymmetries.

### Mitigation and coverage

52 of the 53 have abstracts, so the stratum is labelled rather than a bare count.

| Questions | Base |
|---|---|
| MQ1 | the 137 retained |
| MQ2, MQ3 | the 84 with text, with a **sensitivity check** against the 52 abstracts |
| MQ4, MQ5, SQ1 to SQ6 | the 84 only |

The cut-off date of 2026-09-01 is unchanged. Its verb changes from *exclude* to
**close the stratum**: on that date nothing is excluded, the stratum stops
receiving new texts and is counted and characterized.

## 4. Delta: the two criteria tables are realigned

Three defects were found.

**I1 fused three independent predicates** (complete report, primary study,
temporal and language scope) whose negative counterparts were already separate
as E1, E2 and E4. The negation of I1 is a disjunction mapping to three distinct
codes, so I1 was the complement of no single criterion. Two reviewers marking
"I1 yes" agree on a conjunction, and disagreement on any component is invisible
to the agreement statistic.

**I6 was the positive form of E11** and was left dangling by alpha. Retained, it
would have kept the evidence filter alive on the positive side.

**I5 fused two predicates**, "includes explicit UML content" and "is separable",
whose negative side beta had already split.

### Decision

- I1 splits into three criteria; I5 splits into two; I6 is withdrawn.
- The separability criterion is evaluated at **two moments without receiving a
  separate code for each**: at B5 from title and abstract, and at C1 from the
  full text. The moment is recorded in the gate outcome field, not in the code.
  Creating a code per reading moment would inflate the table without
  discriminating power.
- E3 keeps no positive counterpart, being a property of the set rather than of
  the report, consistent with PRISMA's *records removed before screening*.
- B0 receives no counterpart of its own: it is the conjunction of I4, I5 and I7,
  it absolves but does not condemn.

## 5. Epsilon: numbering regime

The cost of renumbering is asymmetric between the two tables, so the two sides
take different decisions.

Among the 849 recorded exclusions, the codes withdrawn by this amendment, E5,
E10 and E11, have **zero records**. Withdrawing them rewrites nothing. All 561
recorded E7 decisions are the first clause: 539 carry outcome `B1_E7` with a
scan declaring the complete absence of UML, and 22 carry `B3_E7`. The inventory
has no inclusion-criterion column, so no I code was ever written to any record.

### Decision

**Exclusion side, frozen.** E1, E2, E3, E4, E6, E7, E8 and E9 keep their codes
and meanings. E5, E10 and E11 leave the table and remain as declared gaps marked
"withdrawn in A004". Bare `E7` from now on always denotes the first clause, so
the 561 recorded decisions stand without rewriting; the sibling clause is
`E7b`, whose suffix preserves its provenance as a clause of the published E7.
The C1 criterion receives a **new number, E12**, rather than a suffix or the
vacated E10: its statement changed from a negative aggregate ("results cannot be
separated") to a positive verifiable question ("is there an identifiable
generation instance?"). A new statement gets a new code.

A protocol that renumbers erases the trace of its own amendment. The gap is
informative, renumbering would trade the auditability of 849 field-by-field
justifications for cosmetics, and the code does not need to carry location
because the `gate_x_outcome` field already does.

**Inclusion side, renumbered** at zero cost, in **filter order** rather than
historical order.

## 6. Resulting gate structure

| Gate | Filter | Question | Inclusion | Exclusion |
|---|---|---|---|---|
| — | **D** | is it a duplicate or a less complete member of a publication family? | — | E3 |
| A | **A1** | is it within the temporal and language scope? | I1 | E4 |
| A | **A2** | is it a complete scientific report? | I2 | E1 |
| A | **A3** | is it a primary study? | I3 | E2 |
| B | **B0** | does the LLM generate or alter the UML content? | I4 and I5 and I7 | — |
| B | **B1** | does the **generated result** include UML content? | I7 | E7 |
| B | **B2** | is it produced or altered? | I5 | E8 |
| B | **B3** | is the input textual? | I6 | E9 |
| B | **B4** | what is the role of the model? | I4 | E6 |
| B | **B5** | is UML separable from other notations? | I8 | E7b |
| C | **C1** | is there an identifiable generation instance? | I8 | E12 |

D is a corpus-level pre-pass, reported as *records removed before screening*.
A3 routes non-primary reports to a materialized background pile rather than
discarding them. B0 fast-paths clear cases but, when negative, forces descent to
B1 to B4 so that the recorded code always comes from a named filter; this is the
structural fix for the failure that produced the E6 dump.

Filters B1 to B4 are recorded as **attributes even when B0 absolves**, without
power to exclude. This front-loads three of the review's incommensurability
dimensions (diagram types, source specifications, model families) at low cost.
Two accompanying rules: screening attributes are provisional and live in fields
separate from extraction, and **attributes do not enter the agreement
calculation**, which covers only B0 and the named criterion.

### Inclusion criteria, renumbered

| Code | Criterion | Pair |
|---|---|---|
| I1 | The report is within the temporal and language scope of the review. | E4 |
| I2 | The report is a complete scientific report. | E1 |
| I3 | The report is a primary study. | E2 |
| I4 | The study uses at least one LLM as a substantive component of the diagram generation process. | E6 |
| I5 | The task produces, transforms, completes, repairs, refines, or revises UML diagram content. | E8 |
| I6 | The source input includes textual software requirements, user stories, scenarios, specifications, problem statements, or explicit textual domain descriptions. | E9 |
| I7 | The generated result includes explicit UML diagram content, such as PlantUML code, another textual UML representation, XMI, a rendered UML diagram, or another representation from which UML content can be assessed. | E7 |
| I8 | The UML diagram content is separable, both from other notations and from other generated artifacts, tasks or outputs. | E7b, C1 |

### Exclusion criteria after the amendment

| Code | Status |
|---|---|
| E1, E2, E3, E4, E6, E7, E8, E9 | unchanged in code and meaning |
| E7b | new; the notation-mixture clause of published E7, evaluated at B5 |
| E12 | new; the identifiable-generation-instance criterion, heir of E10, evaluated at C1 |
| E5 | withdrawn; replaced by the attrition stratum of Section 3 |
| E10 | withdrawn; split into C1 and the `atribuicao do resultado` attribute |
| E11 | withdrawn; replaced by the three extraction axes of Section 1 |

## 7. Relation to A003

This amendment partially reverses A003. A003 established extractable quality
evidence as an inclusion requirement and introduced E11; Section 1 above
withdraws both. The substantive LLM use boundary recorded in A003, together with
its later revision, is unchanged and remains in force, as does the single-corpus
framing that replaced the two named eligibility layers.

The reversal is recorded rather than silently absorbed. A003 was decided before
formal screening; the present decision follows the completion of Gates A and B
over 986 records, which supplied the empirical arguments of Sections 3 and 5
that were not available in 2026-08-15.

## 8. Application

- ~~Rewrite the criteria tables of the protocol appendix~~ **done, 2026-08-17.**
  The appendix moves to version 1.8. It gains a screening gate structure section
  carrying the table of Section 6; the inclusion table renumbered I1--I8 in
  filter order with a filter column and a pairing column; the exclusion table
  restricted to the operative codes, with E7 narrowed to its first clause and
  E7b and E12 added; a separate table of withdrawn codes kept as declared gaps;
  a section on attrition; and the axes and analytical subsets. Residual
  references to I6, E5, E10 and E11 elsewhere in the appendix were also
  corrected, including the sentence that made quality evidence an eligibility
  matter after retrieval and the validation checklist item V04.
- ~~Update `screening_manual_v1.md`~~ **done, 2026-08-17.** A new
  `screening_manual_v2.md` carries the structure of Section 6; v1 is preserved
  unrewritten as the record of the first pass, for the same reason the exclusion
  codes were frozen rather than renumbered.
- ~~Add the axis fields and the `atribuicao do resultado` attribute to the
  extraction form~~ **done, 2026-08-17.** They enter the quality-evidence
  extraction table of the appendix as `QualityAxisL`, `QualityAxisD`,
  `QualityAxisU` and `ResultAttribution`, and the master sheet as `eixo_L`,
  `eixo_D`, `eixo_U` and `atribuicao_resultado`, born empty because they are
  extraction fields and not screening fields.
- ~~Re-examine the 22 records with outcome `B3_E7`~~ **done, 2026-08-17.** All 22
  are inverted-direction cases in which UML is the input and the output is Java,
  OCL, Rebeca models, test cases, use case descriptions or teaching exercises.
  None is E7b; all remain E7. The check exposed a wording defect in filter B1,
  corrected above: the question predicates the **generated result**, not the mere
  presence of UML in the study, otherwise a reviewer would answer "yes" for a
  UML-to-Java study.
- ~~Flag as first test cases of B5 the six retained records that name UML
  together with another notation~~ **revised, 2026-08-17.** Three of the six
  original candidates have since been decided and are no longer retained:
  `051_ACM` was recoded to E3 as a member of publication family FAM-C-003,
  `797_SCOPUS` became the single E7b of the corpus, and `825_SCOPUS` left at B1
  by E7 because its generated result is not UML at all. A fresh scan of the 105
  retained records for UML named alongside BPMN, SysML, C4, Mermaid, ER or
  ArchiMate returns **nine** test cases: `018_ACM`, `467_IEEE`, `538_IEEE`,
  `769_SCOPUS`, `791_SCOPUS`, `812_SCOPUS`, `866_SCOPUS`, `880_SCOPUS`,
  `918_SCOPUS`. Six of these were absent from the original list. The gate B note
  of `018_ACM` already states the B5 question verbatim, asking whether the
  behaviour models it evaluates are treated by its authors as UML diagrams or as
  exclusively SysML constructs.
- ~~Carry out the impact analysis~~ **done, 2026-08-17.** The amendment changes
  no recorded exclusion. No record in the corpus rests on a withdrawn code:
  E5, E10 and E11 appear zero times in `exclusion_criteria`, which is what the
  withdrawal predicted, since E5 was never applied, E10 only ever produced the
  `CANDIDATO_E10` flag on retained records, and E11 was always an extraction
  concern. The narrowing of E7 was tested against the 579 records that carry it:
  twelve name another notation in title, abstract or keywords, and all twelve
  remain E7 rather than E7b, because in none of them does UML appear in the
  **generated result** — the other notation is either the sole output, as in
  `568_IEEE` for ER and `171_ACM` for BPMN, or UML sits in the input, as in
  `815_SCOPUS`. E7b therefore keeps the single member it was created for. The
  ten records still flagged `CANDIDATO_E10` are rerouted to C1 and to the
  `atribuicao_resultado` attribute rather than to an exclusion. Withdrawn codes
  survive as narrative in notes written before the amendment — E10 in 18 records,
  E11 in 63, I6 in 44 — which is a record of how the decision was reasoned at the
  time and is not corrected, for the same reason the codes were frozen rather
  than renumbered.

The deliberation for each decision, with method, evidence, discussion and
decision, is recorded in `search/automated/screening_decision_log.csv` under
event type `DECISAO_DESENHO`.
