# A005: Extraction instrument reconciliation and inadequacy coding design

- AmendmentID: `A005`
- DecisionDate: `2026-08-18`
- RecordedAt: `2026-08-18T00:00:00-03:00`
- Stage: After screening, during construction of the extraction instrument and before the extraction pilot begins
- Status: `Applied; Sections 6 and 7 transferred to A006`
- PreviousRecordedCommit: `73e8b8335422c55c3c8597149e91edc84981046f`
- RecordedCommit: `e2fe3ee74c75edc64f6a7697f40b6a92d2f28060`
- HeaderCorrection: On 2026-08-18 two header fields were corrected, and only the header was touched. `RecordedCommit` still carried its placeholder although the commit exists and is verifiable. `Status` changed because Sections 6 and 7, left open here, passed to the custody of A006. The text of Sections 6 and 7 is preserved exactly as recorded, including the SQ6 proposal that A006 withdraws: the record of a proposal that was later reversed is evidence, not an error to be erased.
- DoesNotChange:
  - search strings
  - information sources
  - review interval
  - temporal and language scope
  - the screening gate structure established by A004
  - inclusion or exclusion criteria
  - any recorded screening decision
  - A001, A002, A003, A004
- Changes:
  - the value lists of three extraction fields in the Inadequacy facet
  - the composition of the extraction table: one field added, one field removed
  - the design of the inadequacy coding codebook
  - the reading of the question-to-data traceability table

## Summary

A004 closed the eligibility question. This amendment records what was found while
building the instrument that reads the eligible corpus, and it exists because the
protocol text was already changed once without an amendment to cover it.

The unifying finding is structural, and it is the reason to expect more of the
same: **the protocol specifies the same object twice, in two sections written
without reconciliation.** The extraction table (l. 1513-1548) and the coding and
taxonomy section (l. 1594-1634) both describe the inadequacy tuple, and they do
not agree. The evaluation facet names the human evaluator twice, at l. 1495 and
l. 1536, with two different value lists. The construct list in the SQ1 question
does not match the construct list in the field that normalizes it.

| | Decision | Effect | Status |
|---|---|---|---|
| 1 | five divergent value lists resolved | both sections now state the same vocabulary | applied, `26f1619` |
| 2 | severity gains a field | the fifth tuple dimension becomes extractable | applied, `a6ca93d` |
| 3 | the duplicated evaluator field is merged | one field, not two, for the same datum | applied, `ac22fda` |
| 4 | one datum, one owning question | the traceability table is read field by field | applied, `ac22fda` |
| 5 | the coding codebook is a second artefact | carriers are an attribute, not a code | applied, `d1a3110` |
| 6 | the SQ1 construct list | not decided | open |
| 7 | the reach of SQ6 and the values of axis L | not decided | open |

## 1. Five divergent value lists in the Inadequacy facet

The two sections gave different vocabularies for the same three fields. Each case
was decided on its merits, with the evidence recorded, rather than by electing one
section as authoritative; the extraction table won one of the five.

| Field | Adopted | Ground |
|---|---|---|
| Violated reference | `concrete representation`, not `concrete syntax` | l. 181 reserves "syntax" for the abstract level, and l. 180 states that textual validity does not establish UML conformity. The pair concrete/abstract syntax would suggest a continuity between the two levels that this review exists to show is broken |
| Violated reference | `cross diagram consistency`, not `cross model` | the textual evidence is tied one to one; the merit decides, since what is violated is consistency between diagrams of a single model |
| Violated reference | `intended engineering task` | l. 185, the operational definition of Inadequacy, names the trichotomy "language, semantic, or task reference". "engineering" disambiguates from the `GenerationTask` field |
| Discrepancy operation | `emergent category`, not `other` | "other" instructs the coder to discard; "emergent category" instructs the coder to open a code, which is the inductive arm required by l. 1597 and l. 1625. Selecting it now obliges a free-text label |
| UML carrier | the full list of eleven, including `transition` and `message` | l. 113 forbids erasing diagram specific distinctions, and l. 1668 promises a two-level taxonomy that seven values cannot populate |

**Both sections were changed**, so that the contradiction is resolved rather than
displaced to whichever section is read second.

## 2. Severity gains a field

l. 1616 makes severity or consequence the fourth dimension of the inadequacy
tuple. Neither extraction table provided a field for it, so the tuple could not
be recorded whole.

The field is **open, not closed**, on a literal reading of l. 1616: severity is
*preserved* when the study reports a severity scale or task effect. It is
preserved, not classified. A closed list would invent a scale the study does not
have, and would defeat the instruction to record the native vocabulary before
normalizing.

It sits **inside** the repetition group, not at the end of the table, because a
tail position would detach severity from the inadequacy it qualifies.

## 3. The duplicated evaluator field is merged

l. 1495 (`Human involvement`, Evaluation facet) and l. 1536 (`HumanEvaluatorRole`,
Evaluation facet) ask for the same datum. Six of the seven values of the first are
the same vocabulary as the second. Keeping both would have the extractor record
the same thing twice, with no rule saying which column the counts should read.

`HumanEvaluatorRole` survives: it is the more complete list, it carries the
missing-data codes, and it sits beside the reliability field.

**One value required judgement and is recorded as such.** `participant` existed
only in the deleted field and is not a synonym of any surviving value: it marked
a human as the **subject** of a study, never as an evaluator. Deleting it would
lose the only record that a human was involved when the task and actor field is
empty. It is carried over with an explicit exclusion rule: `participant` never
counts toward the independence of the assessment in SQ5.

## 4. One datum, one owning question

The traceability table (l. 133-143) states which data each question requires, at
the level of the facet. Reading it field by field showed twelve fields marked
with two questions each.

The defect was not disproportion but **conflation**: the column mixed "is data
for" with "defines the subset of", which are different relations. l. 1373-1376
makes the analytical subsets conditional on the quality axes, and l. 1360 says
the subsets are *computed* from those axes.

- Each field now has exactly **one** owning question.
- The subset relation gets its own column.
- The three axis fields and the result attribution field are **instruments of the
  review, not answers to any question**, and own no question. Here an empty value
  is an assertion, not a gap.

Two consequences are declared rather than left to be discovered:

- **MQ5 owns no field, and that is correct.** l. 137 states that its data are
  combined categories from MQ2 to MQ4, and l. 1380 states that it is computed.
- **Losing a field is not losing a question.** MQ4 owns one field; its synthesis
  product is now declaredly derived from fields owned by MQ1, SQ3 and SQ5.

## 5. The coding codebook is a second artefact

Step 2 of the coding procedure (l. 1624) applies the initial deductive dimensions
to a pilot subset, so those dimensions must exist as a written codebook before the
pilot runs. It is a different artefact from the extraction codebook: one says which
fields to fill, the other says what each value means.

- **Fourteen codes, not twenty-five.** Among the eight attributes l. 1634 requires
  of every code is "allowed UML carriers". If the carrier were itself a code, that
  attribute would be circular. The carrier is an **attribute**. l. 1668 confirms
  it by making the specific level a cross tabulation derived from extraction.
- **The example paradox.** l. 1634 requires a positive and a negative example of
  every code; the codebook must exist before step 2 (l. 1624); and the examples are
  only produced by step 4 (l. 1626), which runs after. Every example is therefore
  marked `construido` or `corpus`, with the rule that **no constructed example
  survives into the stable version**. `emergent category` has no constructed
  example at all: inventing one would propose the new category before the data.
- **History in a separate long file**, because l. 1631 and l. 1803 require knowing
  *which studies to recode*, which needs each change recorded against what was
  already coded.
- **Single source.** Duplicating a vocabulary across two files is the defect that
  produced Section 1. A guard halts generation of the extraction sheet if the
  taxonomy diverges from the fields it defines.

## 6. Open: the SQ1 construct list

This is the **sixth divergence** of the same structural kind, and it is recorded
here without a decision.

The construct list in the SQ1 question (l. 112, l. 1358) does not match the list
in the field that normalizes constructs (l. 1519).

- missing from the field: `rendering validity`, `correction effort`
- missing from the question: `understandability / readability / clarity`
- the question says `UML conformity` where the field says `UML syntactic conformity`

Two ways out, neither adopted:

1. take the union in the field, leaving the question untouched;
2. remove the enumeration from the question altogether, on the ground that a
   question that enumerates its own answers **selects on the dependent variable**,
   which is the failure A004 removed from eligibility. The list belongs to the
   normalization scheme, not to the question.

## 7. Open: the reach of SQ6 and the values of axis L

Also recorded without decision.

**SQ6.** Seven of its ten data items already belong to MQ3. The decisive objection
is not repetition but **base**: l. 1376 gives SQ6 a restricted subset while MQ3
covers the whole corpus, so the same datum would be reported over two different
denominators. The proposal is that SQ6 keep only the use axis.

**Axis L.** l. 1348 gives the axis three values while the corresponding field has
nine. A study whose only evidence is a renderer run, or PlantUML parseability, has
no axis L value to record. The proposal is to add `rendering validity` to the axis.

Both change the text of a question or of an axis definition, so neither is applied
here.

## 8. Declared deviations from the protocol's own plan

These are not changes to the protocol. They are requirements the protocol makes
that the plan in execution does not yet meet, declared so that they are not
discovered later.

1. **Single extractor in the pilot.** l. 1558 requires two independent extractors
   on the interpretive quality fields. The pilot runs with one, so it does **not**
   close V10 on its own: either a second pass follows, or this becomes a further
   amendment and is reported.
2. **Double coding is corpus-wide.** l. 1638 opens with "two reviewers
   independently code **all** inadequacy data from included studies". This is the
   whole corpus, not the pilot, and the plan in execution covers none of it. It is
   made practicable by reading "inadequacy data" as the five fields of the
   inadequacy group, not all sixty-four fields.
   - The consensus code is stored separately, as l. 1638 requires, by recording it
     under its own extractor identity. **The hazard this creates**: each datum may
     exist in three rows, so any count that does not filter by extractor triples.
     The rule is that synthesis reads only the consensus, agreement reads only the
     two reviewers, and no analysis reads all three.
   - The statistic per field follows from l. 1638 itself: Cohen's kappa for the
     mutually exclusive nominal fields, Krippendorff's alpha where categories are
     multiple or data are missing by construction.
   - **What actually blocks it, and is open:** agreement presupposes that the two
     reviewers are describing the **same units**. l. 1638 says at which levels to
     measure but never how to align units, and two reviewers reading one study may
     record five inadequacies and seven. Without an alignment rule no contingency
     table exists and no coefficient is computable. The choice **must be made
     before** the two passes; made afterwards, it selects the result it measures.
     This holds V09.

## 9. What this amendment does not touch

No screening decision changes. The eligible corpus, the exclusion codes and the
recorded justifications are untouched, and no record is rescreened. The extraction
file is empty, which is why this reconciliation was done now: l. 1558 makes a
material revision of the form trigger a retrospective revision, and l. 1631
requires recoding when a category or boundary moves. At zero extracted rows both
cost nothing; after the pilot they would cost ten studies.

## 10. Correspondence with the protocol tables

The instrument no longer maps one to one onto the protocol tables by position,
because Section 2 adds a field and Section 3 removes one. The two cancel past the
inserted field, so the correspondence is three clean segments rather than a
shifting offset, and it is derived from the codebook rather than written by hand.

The instrument holds sixty-four fields: sixty-three of the protocol's, plus one
this amendment adds.
