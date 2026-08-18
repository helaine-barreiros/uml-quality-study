# A006: Objective and question realignment with the thesis reference model

- AmendmentID: `A006`
- DecisionDate: `2026-08-18`
- RecordedAt: `2026-08-18T00:00:00-03:00`
- Stage: After screening, during construction of the extraction instrument and before the extraction pilot begins
- Status: `Sections 2, 3 and 9 applied; Sections 4, 5 and 6 are open`
- PreviousRecordedCommit: `e2fe3ee74c75edc64f6a7697f40b6a92d2f28060`
- RecordedCommit: `b1f4c08dda8f383dad80f72cd85ac2b8e37efe30`
- Section9Commit: `c2f23b2`
- ExternalSource: Barreiros, H. S. L.; Barreiros, E. S.; Farias Junior, I. H.; Rodrigues, C. M. O. *A Reference Model for Contextualized LLM Software Artifact Generation*. Manuscript, 2026-08-18, 66 pp. The designed artefact of the thesis, read in full on 2026-08-18.
- DoesNotChange:
  - search strings
  - information sources
  - review interval
  - temporal and language scope
  - the screening gate structure established by A004
  - inclusion or exclusion criteria
  - any recorded screening decision
  - any extraction field
  - A001, A002, A003, A004
- Changes:
  - the general objective (l. 73), twice: once in Section 2 and once in Section 9
  - expected contribution (vi) (l. 83)
  - the overarching research question (l. 94)
  - custody of the two decisions left open by A005 sections 6 and 7

## Why this amendment exists, and why it is separate from A005

A005 reconciled the extraction instrument against itself. This amendment does
something different: it realigns the **objective and the questions** against the
artefact they must serve, which is the reference model that the thesis designs.

The reference model was read in full for the first time on 2026-08-18. Two facts
in it change how the review must be read.

**First, the review is the reference model's missing foundation.** The model
derives its five concerns from *"a literature analysis"* resting on four
third-party secondary studies about LLM4SE in general (RM section 3.3.1). Its
own Limitations section states that it establishes conceptual articulation and
analytical inspectability, and **not** that the proposed specialization improves
quality or reduces correction effort. That section is the empirical agenda this
review must equip.

**Second, the three quality axes of this review are the three dimensions of the
model.** `QualityAxisL` is the artefact technical contract, `QualityAxisD` is
domain knowledge, `QualityAxisU` is intended engineering use. Both descend from
Lindland and Krogstie, so the correspondence is not a coincidence; but until now
the axes were an instrument of stratification with no declared warrant. They are
the projection of the thesis artefact onto the corpus.

## 1. Five deliverables the review owes the thesis

Recorded here because the rest of this amendment, and the ones that follow,
are argued against them.

| # | Deliverable | What in the model it serves |
|---|---|---|
| 1 | empirical grounding for the five model concerns | RM section 3.3.1, today second-hand and about a different object |
| 2 | a named vocabulary of deviations | `D` and `Rep` inside the evidence package, which have no typology |
| 3 | the empirical content of the evidence package | the evaluation function, today a list of possibilities |
| 4 | the technical contract for UML, empirically | the five compartments of the artefact contract |
| 5 | baselines and effect measures | the comparison conditions and the correction-effort measure named in RM section 8 |

## 2. The general objective (applied)

Three defects were found in l. 73, each against evidence.

| # | Defect | Evidence |
|---|---|---|
| 1 | one missing dimension: the objective says *syntactic and semantic*, while the instrument carries **three** axes | l. 73 against fields 28-30 |
| 2 | the missing object: **inadequacy does not appear in the objective**, although the taxonomy is contribution (iii), the primary product of SQ2, and deliverable 2 | l. 73 against l. 80 and l. 113 |
| 3 | the purpose is generic: the constitutive function is written at l. 63 and does not reach l. 73 | l. 63 against l. 73 |

Defect 1 is the **fourth occurrence** of the structural pattern that organizes
A005: the same object specified twice in sections written without reconciliation.
The three earlier ones were the inadequacy tuple, the human evaluator, and the
SQ1 construct list.

The objective now has three clauses, so that each can be checked separately:
map the studies; synthesize how they characterize, operationalize, measure and
report **syntactic, semantic and pragmatic** quality, **the inadequacies they
report**, and the dissonance evidence; and establish the constructs, deviation
categories, units, references, reliability practices, baselines and correction
effort measures required by the subsequent thesis stages.

Every deliverable in Section 1 has an anchor in the new text, and no anchor is
left unused.

## 3. Expected contribution (vi) (applied)

The old (vi) was the only link to the thesis and asserted nothing checkable.
The new one names the six categories the thesis will draw on, and adds a second
half that is not decoration: **an explicit record of the categories for which the
literature offers no precedent**. A measured absence is a result. If the corpus
turns out to have no precedent for measuring correction effort on UML, that is a
finding of the review and a direct warrant for the design of the next study, not
a hole in it.

## 4. Open: the SQ1 construct list

Transferred from A005 section 6, where it was recorded without a decision.

The construct list in the SQ1 question (l. 112, l. 1358) does not match the list
in the field that normalizes constructs (l. 1519): `rendering validity` and
`correction effort` are missing from the field, `understandability / readability
/ clarity` is missing from the question, and the question says `UML conformity`
where the field says `UML syntactic conformity`.

**The reference model changes the argument.** The two constructs missing from the
field are the two the thesis will most need: the model's demonstration emits
**PlantUML** that is rendered, and RM section 8 names **correction effort** as
the measure that later work must take. Losing them at extraction would lose the
two measures the empirical stage depends on. This favours the union, which is
option 1 in A005 section 6; option 2, removing the enumeration from the question,
remains open on its own merits and is not settled here.

## 5. Open: the reach of SQ6, with the sign reversed

Transferred from A005 section 7, **and its proposal is withdrawn.**

A005 proposed that SQ6 keep only the use axis, on the ground that seven of its
ten data items already belong to MQ3. Reading SQ6 (l. 117) against the reference
model reverses this. SQ6 is the only question that asks how requirements,
technical specifications, domain knowledge, UML instructions, prompts, examples,
tools, retrieval and feedback are **supplied as generation context**. That is
domain knowledge plus the technical contract plus artefact-ready knowledge, which
is the central proposition of the thesis artefact. MQ3 asks which **mechanism**;
SQ6 asks which **knowledge, and how structured**. The model itself draws exactly
this line: no technique is the specialization, techniques instantiate
responsibilities.

**What the detailed reading then exposed, and what is actually open.** The two
fields that *are* domain knowledge and the technical contract on the input side
already exist in the codebook, and both are owned by MQ3:

| Field | Owner today |
|---|---|
| 19 `DomainKnowledgeProvided` | MQ3 |
| 20 `UMLTechnicalInstructionProvided` | MQ3 |

SQ6 owns only fields 56-60. Under the *one datum, one owning question* rule
applied in A005 section 4, **SQ6 asks for what it cannot read.** The likely
resolution is to move fields 19 and 20 to SQ6, which would also leave MQ3
aligned with the specialization mechanisms and SQ6 aligned with the knowledge
supplied. Not applied: it moves data ownership, and ownership is decided once,
after the questions are settled.

## 6. Open: the values of axis L

Transferred from A005 section 7. l. 1348 gives the axis three values while the
corresponding field has nine, so a study whose only evidence is a renderer run or
PlantUML parseability has no axis L value to record. The proposal is to add
`rendering validity` to the axis. The reference model strengthens it for the same
reason as Section 4: its generated artefact is PlantUML code that is rendered, so
rendering is a genuine step of the technical contract, not a marginal one.

## 7. Consequences declared, not left to be discovered

- **The ORQ (l. 94) carries defect 1.** It still says *syntactic quality,
  semantic quality, and syntax-semantic dissonance*. The objective and the
  overarching question must not disagree; this is the next decision, and it is
  not taken here. **Taken in Section 9, on the same day.**
- **Contribution (v) and contribution (vi) do not overlap.** (v) is what the
  literature reported; (vi) is what the thesis can adopt.
- **The disclaimer at l. 86 stands unchanged.**

## 8. What this amendment does not touch

No eligibility criterion changes. l. 68 requires every included report to provide
extractable evidence about the quality of generated UML content; adding the
pragmatic dimension to the **objective** neither loosens nor tightens it, because
pragmatic evidence was already extractable through axis U and fields 56-60.
**No record is rescreened, and none of the 881 exclusions is revisited.**

No extraction field changes. The seven categories named in the third clause of
the objective already exist in the instrument; the clause names them, it does not
create them. The extraction file is still empty, so Sections 4 to 6 can be
settled at zero recoding cost.

## 9. The overarching question, and a second edit to the objective (applied)

Recorded as Section 9 rather than inserted after Section 2 so that the numbering
of the open Sections 4, 5 and 6 does not move; they are referred to by number in
the decision log and in A005.

### 9.1 The fifth occurrence of the structural pattern

l. 61 already says the study *"synthesizes how they define, classify, measure,
and validate diagram quality and inadequacies"*. l. 73 and l. 94, written later,
say `characterize, operationalize, measure, report` and drop inadequacies
altogether. **The older text is the correct one**; the newer text lost two verbs
and one object. This is the same defect as the four before it, with the sign
reversed: not two sections that disagree about a list, but two sections where the
later one silently narrowed the earlier.

### 9.2 Five defects of the ORQ

| # | Defect | Evidence |
|---|---|---|
| 1 | two dimensions where the instrument has three | l. 94 against fields 28-30 |
| 2 | inadequacy absent, although it is contribution (iii) and the primary product of SQ2 | l. 94 against l. 80 and l. 113 |
| 3 | `classify` missing, so SQ2 hangs under no verb of the ORQ | l. 94 against l. 61 and l. 113 |
| 4 | `validate` missing, so SQ5 hangs under no verb of the ORQ | l. 94 against l. 61 and l. 116 |
| 5 | generation context only implicit, so SQ6 barely fits | l. 94 against l. 117 |

The test applied was mechanical: pass all eleven questions under the ORQ and see
which ones do not descend from it. **SQ2, SQ5 and SQ6 did not pass cleanly.**

### 9.3 What deliberately did not enter the ORQ

Clause (c) of the objective — establishing the constructs, categories, units,
references, reliability practices, baselines and correction effort measures for
the later thesis stages — is **purpose, not a question answerable from the
corpus**. It stays in the objective and does not become part of the ORQ.

This is symmetric with the rule applied in A005 section 4: MQ5 owns no extraction
field because it is computed. An objective may state a purpose that no question
asks, in the same way that a question may exist that no field answers directly.

### 9.4 The applied text

l. 94 now asks how primary studies have used LLMs on UML diagram content from
textual requirements or explicit textual domain descriptions, **under which
generation context**, and how they **characterize, classify, operationalize,
measure, validate, and report** the **syntactic, semantic, and pragmatic**
quality of that content, **its reported inadequacies**, and the evidence of
syntax-semantic dissonance.

Every element of the ORQ has an owning question, and no question is left without
an ancestor in it: generation context to SQ6 and MQ3, `classify` to SQ2,
`validate` to SQ5, the three dimensions to SQ1, SQ3 and SQ4, inadequacies to SQ2,
dissonance to MQ2.

### 9.5 The cost, declared

l. 73 had to be edited a second time, on the same day, to carry `classify` and
`validate`. Editing only the ORQ would have made the objective and the
overarching question disagree — **reproducing, one day after diagnosing it, the
very pattern this amendment documents**. The two lines were changed together, so
l. 61, l. 73 and l. 94 now state the same verbs.

No eligibility criterion, no extraction field and no screening decision changes.
The `.tex` still has 1860 lines, so every line reference recorded anywhere
remains valid.
