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
