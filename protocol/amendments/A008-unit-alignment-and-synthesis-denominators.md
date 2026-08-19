# A008: Unit alignment for coding, and a denominator for every synthesis

- AmendmentID: `A008`
- DecisionDate: `2026-08-19`
- RecordedAt: `2026-08-19T00:00:00-03:00`
- Stage: After the extraction instrument was closed by A007, and before the extraction pilot begins
- Status: `Applied`
- PreviousRecordedCommit: `76a764a29a2f1d0b45c3b2e7f8a1d6c4e9b03571`
- RecordedCommit: `e908ba0`
- Scope: Step 6 of the six-step refinement ordered by the primary reviewer: what the review owes the thesis, objective, ORQ, subquestions, extractions, **methods**. Steps 1 to 5 closed with A006 and A007. This amendment closes the sequence.
- DoesNotChange:
  - search strings, information sources, review interval, temporal and language scope
  - the screening gate structure, the inclusion or exclusion criteria, and any recorded screening decision
  - the questions, which stay at 12 as left by A006
  - the extraction fields, which stay at 64 with their ordinals as left by A007
  - the analytical subsets table, which is quoted here and not edited
- Changes:
  - the coding reliability subsection, which now separates unitization from classification
  - one subsection of the Synthesis Plan, split into two
  - one bullet of the descriptive mapping list

## Summary

The method was written **twice**: in the synthesis-procedure column of the
traceability table, one row per question, and in the Synthesis Plan, seven
subsections. This is the same structural pattern that A005, A006 and A007 each
had to undo. Comparing the two writings mechanically produced five findings.
Three were applied. Two were deferred, and the deferral is held by a lock rather
than by a sentence.

| | Finding | Decision | Status |
| --- | --- | --- | --- |
| 1 | Coding reliability has no unit-alignment rule | applied: unitization is separated from classification | Applied |
| 2 | SQ5 has no synthesis subsection | deferred to the end of the pilot, held by a lock | Deferred |
| 3 | MQ5 has no synthesis subsection | deferred to the end of the pilot, held by a lock | Deferred |
| 4 | One subsection fuses SQ6 and SQ7, which have different denominators | applied: split, each declaring its own denominator | Applied |
| 5 | One bullet still names the field A007 removed | applied: re-anchored on the axes | Applied |

## Section 1. Method

The two writings of the method were extracted and compared, and the product name
of each question was then searched **inside** the Synthesis Plan. The search is
the evidence; the reading only interprets it.

```
gap analysis / under investigated / concentration   -> ABSENT from the Synthesis Plan
credibility / adjudication / evaluator training     -> ABSENT from the Synthesis Plan
"gap analysis"       occurs only at l. 138 and l. 1382
"credibility matrix" occurs only at l. 143
"appraisal" inside the Synthesis Plan: only l. 1695, as a sensitivity stratum
```

The line numbers in this block are the ones **before** the edits of this
amendment. Section 6 gives the key.

Twelve questions against seven subsections. Four questions map one-to-one, four
mapping questions share the descriptive subsection, two questions share one
fused subsection, and two questions have no subsection at all.

## Section 2. Finding 1, the unit-alignment rule

**Defect.** The protocol required two reviewers to independently code *all*
inadequacy data and to compute Cohen kappa and Krippendorff alpha over the
principal dimensions of the inadequacy tuple. But an inadequacy is a
**repeatable field of free enumeration**. Reviewer A may enumerate five
inadequacies in a study and reviewer B seven. Without a rule that pairs the
items, there is no contingency table, and a coefficient computed over unpaired
enumerations reports **how much each reviewer found**, not how far they agree on
category boundaries. Elsewhere the protocol assigned "the feasibility of unit
level extraction" to the pilot, which treats the matter as a question of
*feasibility* and not as a *procedure*.

**Applied.** Coding an inadequacy is now stated as two operations, and only the
second carries a coefficient.

| Operation | Who | Measured how |
| --- | --- | --- |
| unitization: enumerate the reported inadequacies in the study's own vocabulary | both reviewers, then **reconciled** by discussion and adjudication | reported as the count of items added, removed and merged on each side |
| classification: assign normalized categories and tuple dimensions | both reviewers, **independently**, over the reconciled list | Cohen kappa, Krippendorff alpha |

**Why the order matters, and why now.** The rule is fixed *before* the two
independent passes. Aligning units afterwards would let each reviewer's
classification decide which items are held to have been reported at all, which
is the contamination the independence was there to prevent. This is what blocked
validation item V09.

## Section 3. Finding 4, one denominator per synthesis

**Defect.** A single subsection carried "generation context, pragmatic adequacy,
and rework". A006 had already split SQ6 from SQ7 precisely because they are
different questions, and the analytical subsets table gives them **different
denominators**: SQ6 runs over the whole eligible corpus, SQ7 only over studies
for which axis U is not absent. Writing both in one subsection installs the
denominator trap inside the synthesis plan itself. This is the **seventh
occurrence** of the pattern of specifying one object twice, or here of merging
two objects once.

**Applied.** Two subsections, each stating its own denominator in its first
sentence and stating why. The reason is not decoration: reporting SQ6 over the
SQ7 subset would describe the supply of domain knowledge over the minority of
studies that also measured use, and running SQ7 over the whole corpus would read
the silence of studies that never measured use as an absence of effect.

The inferential-status classification of context factors moved to the SQ7
subsection, because the traceability table assigns inferential status to SQ7 and
assigns to SQ6 only what knowledge is supplied.

## Section 4. Finding 5, a bullet outliving its field

The descriptive mapping list still planned "evaluation dimension by diagram
type". A007 removed reported quality dimensions from the extraction as
**derived**: they are given by the three evidence axes and by the dimension
partition of the normalized construct. The bullet pointed at a field that no
longer exists. It was re-anchored on the axes, in place, without shifting any
line.

## Section 5. Findings 2 and 3, deferred and held by a lock

MQ5 has no subsection although its product is the gap map, and SQ5 has no
subsection although its product is the credibility matrix. Both are **deferred to
the end of the extraction pilot**, and neither is deferred by a promise.

| | What decides it | Why not now |
| --- | --- | --- |
| MQ5 | which combinations of diagram type, configuration and evaluation practice actually occur | with zero of fifty-seven studies extracted, writing the subsection would choose the cells before seeing the table |
| SQ5 | which appraisal domains the literature actually reports | the columns of the credibility matrix are those domains |

**The lock.** `analysis/scripts/verifica_protocolo.py` computes the set of
questions whose product is not named anywhere in the Synthesis Plan and asserts
that the set is **exactly** `{MQ5, SQ5}`. The assertion is an equality, so it
fails on both sides: it fails if a third gap appears, and it fails when MQ5 or
SQ5 is covered. Covering one of them therefore *requires* editing the lock, and
editing the lock requires recording the decision. A deferral written only as
prose is the thing this review has repeatedly had to undo.

**A third finding was surfaced and also deferred, without a lock of its own.**
The SQ5 gap has a second half that is procedural rather than substantive: the
protocol lets the adjudicator resolve "appraisal disagreements", which
presupposes two appraisers, but the methodological appraisal appears in no
reviewer responsibility row. It is the same kind of defect as finding 1 and it is
cheap to fix, but the primary reviewer reconfirmed the original scope of this
step, so it was not applied. It is recorded here so that it is found again.

## Section 6. Line-reference translation key

The `.tex` went from **1862 to 1870** lines. This is the **third** key. Apply the
three in order: `CORRECAO_REFERENCIA` of 2026-08-17 for v1.7 to v1.8, then that
of 2026-08-18 for 1860 to 1862, then this one.

| Old line | New line |
| --- | --- |
| up to 1640 | unchanged |
| 1641 to 1689 | add 4 |
| 1690 to 1862 | add 8 |

The content of old l. 1640 now spans **1640 to 1644**, and the content of old
l. 1689 to 1691 now spans **1693 to 1699**.

Frequently cited references, translated: the analytical subsets table stays at
l. 1375-1378; the pilot rule stays at l. 1560; the inadequacy tuple stays at
l. 1601-1620; coding reliability keeps its heading at l. 1638 and its body grows
from l. 1640 to l. 1640-1644; the Synthesis Plan moves from l. 1642-1695 to
l. 1646-1703; the reviewer roles table moves from l. 1697-1719 to l. 1705-1727.

## Section 7. Verification

- `.tex`: 1862 to 1870 lines; PDF and HTML regenerated at 57 pages.
- Protocol verifier `analysis/scripts/verifica_protocolo.py`: zero failures, 14
  locks, including the gap equality.
- Instrument verifier: zero failures, unchanged by this amendment.
- Zero rescreening and zero recoding. No extraction field, no question, and no
  admitted value of any screening decision changed.
- The six-step refinement ordered by the primary reviewer is closed.
