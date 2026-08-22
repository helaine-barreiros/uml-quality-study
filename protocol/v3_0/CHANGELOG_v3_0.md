# Protocol v3.0 changelog

Date: 2026-08-21
Opened from: `appendix_two_layer_mapping_protocol_v2_0.tex` as reviewed on 2026-08-21.

v3.0 opens with no change to the method. It is v2.0 at the point where the whole-document review
closed, with the version identity advanced so that further work does not overwrite the reviewed
state. `CHANGELOG_v2_0.md` remains the record of how v2.0 reached that point and is not restated
here.

## Inherited state, verified at the moment of opening

- 1227 lines, 48 rendered pages, no unresolved citation or cross-reference.
- 36 locks in `analysis/scripts/verifica_protocolo_v3.py`, all passing.
- Protocol and codebook correspond field by field, with no divergent admitted value.
- Every field is owned by a question that exists; MQ5 has no field by design.
- The SQ1 and SQ2 normalization vocabularies are disjoint.
- The codebook cites the protocol by named anchor and never by line number; all seventeen distinct
  anchors resolve.
- The bibliography has no uncited entry.

## Why the codebook is not forked

The codebook is not versioned alongside the protocol, and this is the first version boundary where
that costs nothing. Its extraction rules reference the protocol by named anchor rather than by
line number, so they remain true for v3.0 without edit. Forking it would create two sources of
truth for the same 65 fields and the same recorded decisions, and freezing a state for
reproducibility is the work of a commit, not of a filename suffix.

## Open on arrival

- V08 and V09 are `Pending`. V09 now requires two dated calibrations, one per reading moment, and
  full-text agreement reported separately.
- Web of Science, ScienceDirect, and arXiv carry `Decision pending` and are declared as a threat.
  A named case, `Gheorghita2025Diagrams`, is within scope and retrieved by no executed source.
- 54 of the 58 reports with full text have no filter C1 decision.
- The registration repository identifier is unset.

## Second vocabulary pass, 2026-08-21

The first pass separated attribute, deviation and measure. A re-reading of v3.0 against the
software engineering quality vocabulary found five residues of the same family, all applied.

- **One name for level one.** `quality dimension` survived in three places, so the level had four
  names at once: construct, attribute, dimension, and the axes. It is gone. The spine subsection
  now states that this review calls the extracted attributes *quality constructs*, that *attribute*
  is the measurement standards' term for the same level, and that *dimension* is not a third name:
  a dimension is one of the three axes and nothing else.
- **The protocol stopped using the term it declines.** `defect` was declined in the operational
  definitions and then used technically three times, twice in the limitation passages a reviewer
  reads most closely. Those now say *inadequacy* or *deviation*; the two mentions that decline the
  term remain, and one figurative use became *flaw*.
- **The primary framework's own words are in the text.** Lindland's `feasible validity`,
  `feasible completeness` and `feasible comprehension` appeared zero times while the framework was
  cited four times. The two central inadequacy categories, omitting required domain elements and
  introducing unsupported content, are now stated as the negative poles of that pair rather than
  asserted as a mapping, so the claim is checkable against a thirty-year-old citation.
- **The pragmatic partition is defined.** `understandability`, `readability` and `clarity` were
  admitted values with no definition anywhere, in a vocabulary whose purpose is to normalize. Each
  now has a glossary row distinguished by the object it predicates: the interpreter, the
  representation, and the statement. A diagram can be readable, understood by one interpreter, and
  still unclear because a second reads it otherwise.
- **`measure` where the review speaks, `metric` where the study does.** The 2502n series retired
  *metric* when it superseded ISO/IEC 9126, and the protocol cites 25020 while naming its own level
  *metric*. The facet, the repetition group, the SQ3 product and the synthesis subsection are now
  *measure*. The field names that record what a primary study reported keep *metric*, because that
  is the studies' word and this review registers native vocabulary before normalizing it; renaming
  those would have imposed the normalized term on native-vocabulary fields, against the rule that
  governs the whole extraction. Where both appear, *metric* is the study speaking and *measure* is
  the review.

The `LACUNA` lock broke on the renamed SQ3 subsection and was updated, which is the behaviour it
exists for.
