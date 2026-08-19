# A007: Extraction provenance and the baseline condition

- AmendmentID: `A007`
- DecisionDate: `2026-08-19`
- RecordedAt: `2026-08-19T00:00:00-03:00`
- Stage: After screening, during construction of the extraction instrument and before the extraction pilot begins
- Status: `Applied`
- PreviousRecordedCommit: `b6fd0b81675218bb4c50dbd3b6f41d3a90816473`
- RecordedCommit: `PENDING`
- Scope: Step 5 of the six-step refinement ordered by the primary reviewer: what the review owes the thesis, objective, ORQ, subquestions, **extractions**, methods. Steps 1 to 4 closed with A006.
- DoesNotChange:
  - search strings
  - information sources
  - review interval
  - temporal and language scope
  - the screening gate structure established by A004
  - inclusion or exclusion criteria
  - any recorded screening decision
  - the number of extraction fields, which stays at 64
  - the ordinal of any extraction field, which stays 1 to 64 unchanged
  - the questions, which stay at 12 as left by A006
- Changes:
  - a provenance column in the extraction codebook, and the matching column in the extraction data file
  - the composition of one extraction field, in place and without renumbering
  - one row of the mapping and generation context extraction table in the protocol

## Summary

A006 closed the questions. This amendment records what changed in the
**extractions** once the questions were settled, and it is deliberately small.
The instruction that governs it is the primary reviewer's own: do not lose focus
and do not get lost in process. Two movements were applied; everything else that
the measurement suggested was deferred to the pilot, and Section 4 says what and
why.

| | Decision | Effect | Status |
| --- | --- | --- | --- |
| 1 | Record the provenance of every field | 8 of 64 fields stop being a search in the paper | Applied |
| 2 | Field 26 becomes `BaselineCondition` | the review's fifth deliverable gains a carrier; a duplication is removed | Applied |
| 3 | Stop here; the rest waits for the pilot | no field is added or removed on speculation | Applied |

## Section 1. Method

The two movements were not proposed from reading the instrument alone. Fill
rates were measured on the master CSV restricted to the 57 records that have
text, because a field that another column already answers for every study is not
a field the extractor should spend a reading on.

| Column of the master CSV | Filled, of 57 |
| --- | --- |
| `PY`, `T2`, `TY`, `AU`, `KW`, `PB`, `DB`, `UR` | 57 |
| `gate_b_outcome`, `gate_b_notes` | 57 |
| `DO` | 53 |
| `AD` | 50 |
| `N1`, `M3` | 48 |
| `C1` | 3 |
| `attr_saida`, `attr_tarefa`, `attr_entrada`, `attr_modelo`, `eixo_L`, `eixo_D`, `eixo_U` | 0 |

The last row is the control. Those columns are empty by design, they are filled
by this very extraction, and they show that the measurement distinguishes *the
datum already exists* from *the datum is not there yet*.

## Section 2. Movement 1, the provenance of a field

**Defect.** The codebook told the extractor what each field means and what values
it admits, and said nothing about **where the value comes from**. Every field
therefore read as an instruction to search the paper. Eight of the 64 are not.

**Applied.** The codebook gained the column `origem`, with three values, and the
extraction data file gained the matching column `procedencia`, so the provenance
travels with the datum into the analysis and is not merely an instruction on a
screen.

| `origem` | Fields | What it asserts |
| --- | --- | --- |
| `lido` | 56 | read in the paper |
| `conferido` | 4 | the value already exists; check it and correct it if it diverges |
| `derivado` | 4 | the value follows from another field of this same form |

The eight, and the source of each:

| Field | Provenance |
| --- | --- |
| Year, venue, publication type, status | `PY`, `T2`, `TY`, `M3` of the master CSV |
| Authors and affiliations | `AU`, `AD`, `C1` of the master CSV; only `C1` needs reading, at 3 of 57 |
| SubstantiveLLMUseDecision | it is the Gate B decision, already in `gate_b_outcome`, 57 of 57 |
| BoundaryDecisionRationale | already in `gate_b_notes`, 57 of 57 |
| PlantUMLGenerated | from `OutputRepresentation` |
| SyntacticEvidenceAvailable | from axis L: not absent is yes |
| SemanticEvidenceAvailable | from axis D: not absent is yes |
| CorrectionOrReworkEvidence | from any recorded correction measure, or axis U equal to rework |

**Nothing was removed.** A derived field is still recorded, still exported, and
still auditable; what changes is that the extractor is told not to go looking for
it, and that `unclear` is the only value they set by hand on the four derived
ones. The removal of a field would be a claim about the literature. This is a
claim about the extraction procedure, and only that.

**Cost.** The form now shows a provenance badge and a warning box before the
extraction rule, because a warning printed after the reading instruction arrives
too late. The verifier gained four locks: the provenance vocabulary is closed at
three values, exactly eight fields are not `lido`, the form carries the
provenance field by field, and the form states in words that the field is not to
be searched in the paper.

## Section 3. Movement 2, field 26 becomes the baseline condition

**Defect.** Field 26 was named `Dimensions and baselines`, typed `composto`, not
repeatable, and it was the *only* field owned by MQ4. It fused two objects, and
the protocol names this failure mode itself at l. 1354 and l. 1356: a fused
question yields a fused code, and the distinction becomes unrecoverable.

**What the two halves turned out to be.**

| Half of field 26 | Verdict |
| --- | --- |
| reported quality dimensions | **derived.** Axes L, D and U say which dimensions the study assessed, and the normalized construct field partitions its vocabulary into the three dimensions. This is the **sixth occurrence** of the structural pattern: the same object specified twice, in two sections written without reconciliation. |
| comparison conditions, human baseline, rule based baseline, no baseline | **the only carrier of deliverable 5**, baselines and effect measures, which the review owes the thesis reference model. Without it there is no way to say what the literature measures against. |

**Applied.** Field 26 *became* `BaselineCondition`: closed, repeatable, still
owned by MQ4, still at ordinal 26. Values:

> no baseline; human-authored model; rule-based or deterministic tool; another
> LLM; another version or configuration of the same LLM; ablation of the
> generation context; published benchmark or gold standard; other.

Repeatable because a study compares against more than one baseline, and
deliverable 5 needs the list and not a single label.

**`no baseline` is not `not reported`.** `no baseline` is the study that declares
it compares against nothing; `NAO_REPORTADO` is the study that does not say. The
value list deliberately omits the string `not reported` so that the form's own
absence-code rule supplies `NAO_REPORTADO` beside it instead of producing two
spellings of one thing. A verifier lock holds this apart.

**A cheaper route than the one first approved.** The movement was first approved
in a *new field* variant, adding `BaselineCondition` beside field 26. Placing a
new field at its correct semantic position would have renumbered fields 27 to 64
into 28 to 65, invalidating the field numbers written into A005, A006, the
decision log and the working notes over the preceding two days, and requiring a
**field-number** translation key alongside the line-number one, plus a third
line-number key for a 1862 to 1863 shift. The redundancy of the first half was
found while preparing that change and was reported before anything was executed;
the primary reviewer then approved the substitution instead. The result is the
one that was approved, at a much smaller process cost: **64 fields, ordinals
untouched, the `.tex` still at 1862 lines, no new translation key.**

**Cost.** One row of the mapping table replaced in place, at l. 1496. The row now
lists the closed vocabulary and states that quality dimensions are not recorded
there, so the removal is legible in the protocol and not only here. One line of
the generator that still referred to the old field name was corrected. The
verifier gained five locks: the field exists exactly once, the fused name has not
come back, the field is closed and repeatable and owned by MQ4, the `no
baseline` and `not reported` distinction survives, and no quality dimension has
crept back into the value list.

## Section 4. What was measured and deliberately not changed

Three findings were surfaced by the same measurement and are **not** acted on
here. Each is a hypothesis about the instrument that only extraction can test,
and changing the instrument on a hypothesis is what produced the defects that
A005 and A006 had to undo.

| Finding | Why it waits |
| --- | --- |
| MQ3 owns 11 fields while MQ4 owns 1 | the disproportion may be correct: technical configuration genuinely has more dimensions than evaluation design. Ten studies will show whether the 11 are all filled. |
| Fields 35 and 36 duplicate axes 28 and 29 | they are already marked `derivado` by Movement 1, so the duplication now carries a label. Whether to delete them is a question the pilot answers by showing whether the derivation ever fails. |
| Field 23 | its value list was not checked against the master CSV in this step and is left alone rather than changed unverified. |

## Section 5. Verification

- Codebook: 64 fields, ordinals contiguous 1 to 64, unchanged.
- `.tex`: 1862 lines before and after; PDF and HTML regenerated at 57 pages.
- No third line-reference translation key, and no field-number translation key.
- Instrument verifier: zero failures, including the nine locks added here.
- Zero rescreening and zero recoding: no admitted value of any screening decision
  changed, and the extraction data file is still empty apart from its header.
