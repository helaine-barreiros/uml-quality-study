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

## Hallucination: an overclaim corrected, 2026-08-22

The protocol had stated that omission is not hallucination, anchoring on the natural language
generation split between faithfulness and completeness. That is true of that literature and false
of this corpus. Software engineering taxonomies of code-generation hallucination classify missing
functionality as hallucination under task requirement conflict, and report that category as the
most prevalent one across models. The claim was withdrawn.

What replaced it is not the opposite claim. The two literatures disagree about where hallucination
ends, and a terminological fault line between two bodies of work that both describe this phenomenon
is one of the findings this review exists to record, not an assumption it may settle in advance.
The protocol now states the disagreement and declines to resolve it.

The instrument separates the layers it separates everywhere else. A study that calls an omission a
hallucination has that label recorded verbatim in the original label field, and disagreement
between the native label and the normalized operation is data rather than error. The normalized
operation keeps `omission` apart from `unsupported addition` for a reason independent of the
dispute: an addition is counted against what was generated and an omission against what the
reference contains, so merging them would destroy the denominator this review exists to
reconstruct.

`intrinsic hallucination` and `extrinsic hallucination` were withdrawn as normalized values, and
their two taxonomy entries with them. That pair is the natural language generation cut. The cut
software engineering itself uses is what the deviation violates, and the instrument already carries
it in the violated reference field, so classifying by hallucination would have forced the review to
adopt one of the two boundaries for no gain.

The review does not deny the causal link between the model's failure and the artifact's deviation,
which other studies investigate. It declines to assert that link from artifact evidence, which is
the attribution `ResultAttribution` exists to qualify.

## Anchors added, 2026-08-22

Ten references, each attached to a claim that previously carried none. Metadata was fetched from
CrossRef and arXiv rather than written from memory, and where a preprint had a published version
the published one is cited.

| Claim in the protocol | Anchor |
| --- | --- |
| Faithfulness and completeness are complementary, so omission is not hallucination in NLG evaluation | Ji et al. 2023, ACM Computing Surveys; Maynez et al. 2020, ACL |
| Missing functionality is classified as hallucination under task requirement conflict, and is the most prevalent category | Zhang et al. 2025, PACMSE/ISSTA; Liu et al. 2024; Lee et al. 2025 |
| Software engineering classifies hallucination by what was violated, which is the cut the violated reference field already carries | Zhang et al. 2025; Lee et al. 2025 |
| `adequacy` names the semantic axis in natural language generation evaluation | Ji et al. 2023 |
| `defect` and `fault` carry the fault to failure chain of systems in operation | Avizìienis et al. 2004, IEEE TDSC |
| `nonconformity` is non-fulfilment of a requirement | ISO 9000:2015 |
| SQuaRE replaced `metric` with `measure` when it superseded ISO/IEC 9126 | ISO/IEC 25000:2014 with ISO/IEC 25020:2019 |
| Keeping the property apart from the procedure that assigns it a value is a long-standing requirement, not a distinction introduced here | Moody 2005, Data & Knowledge Engineering |
| `cross diagram consistency` in the sense of the UML consistency-management literature | Lucas, Molina and Toval 2009, IST |

The bibliography of v3.0 now holds 43 entries, every one of them cited and every citation resolved.
