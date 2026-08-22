# Versioning

Three areas are versioned in parallel, with the same version names, because a collection is only
interpretable through the instrument that produced it and the protocol that governed it. Reading
`protocol/v3_0` beside `analysis/v1_7` is a mistake, and using one naming scheme across the three
areas is what makes that mistake visible.

```
protocol/<ver>/   the document: .tex, .bib, rendered .pdf/.html/.css, CHANGELOG,
                  build/ wrapper, analysis/scripts/{gera_pdf_protocolo.sh,verifica_protocolo.py}
analysis/<ver>/   the extraction layer: extraction/ codebooks and extracao.csv,
                  ficha_extracao.html, scripts/ that generate and verify it, scripts/aplicacoes/
search/<ver>/     the collection layer, symmetric across the two routes:
                  automated/source/   starting list, per-source exports, validation rounds
                  automated/records/  the worked list derived from it, and the decision log
                  manual/             venue plan, unit registry, logs, and the per venue-year
                                      provenance chain source -> raw -> normalized -> screening
                  scripts/            gate and second-reviewer generators, and the rendered
                                      gate pages, which screen the whole corpus and not one route
```

| Version | Protocol | Codebook | Collection | State |
|---|---|---|---|---|
| `v1_7` | 1870 lines, 57 pages | 64 fields, 23 line-number references | 986 records, 881 exclusions, 849 decisions | **frozen**, materialized from `HEAD` |
| `v2_0` | 1227 lines, 48 pages | 65 fields, 0 line-number references | same collection, no new decision | **frozen** at the close of the review of 2026-08-21 |
| `v3_0` | 1227 lines, 48 pages | 65 fields | same collection, 54 filter C1 decisions pending | **live** |

## Origin and worked list

`custom_automated_search_collection.ris` is the starting list: one unified export of Scopus, IEEE
Xplore, and ACM Digital Library, 986 records. It is the origin, and it does not change. Each
version holds its own copy of it under `source/` and derives its own worked list from it, which is
`records/custom_automated_search_collection.csv`, 986 records over 69 columns. The copies are
byte-identical today and share the digest `6657245d2407`; comparing that digest across versions is
how a version is shown to have started from the same place rather than from a re-run search.

The distinction matters because the worked list carries decisions and the origin does not. A
version can always be re-derived from `source/`; nothing can re-derive `source/`. The earlier and
narrower export `automated_search_collection.ris`, 636 records, is retained beside it for
provenance: the corpus of 986 comes from the custom list, whose count matches the corpus exactly.

`v1_7` is the lineage under which everything was actually executed. The codebook was born and
lived entirely inside it, from `b709a96` to `e910189`; `v2_0` inherited it and is where it was
reviewed. There is one collection, produced under `v1_7`, and it is carried forward rather than
recollected.

## Where a result belongs

Screening was executed once, under `v1_7`. The unified starting list, pre-pass D, and gates A, B
and C all produced their outcome there, and `search/v1_7/` is the only place that outcome exists:
the worked list, the decision log, and the rendered gate pages the reviewers actually answered.

`v2_0` is frozen and holds its own copy of the **origin** and none of the **result**: its
`automated/records/` carries an `INHERITED.md` instead of a worked list, because a version that did
not run the gates must not appear to have produced 986 outcomes.

`v3_0` is live, and a live version needs somewhere to write. Its `automated/records/` carries a
worked list seeded from v1_7's, in which every gate A and gate B outcome is inherited and every
decision taken after v1_7 closed is its own. The first of those is the filter C1 of `018_ACM`.
Reading is what inheritance permits; writing into `v1_7` is what it forbids, since that list must
keep saying what v1_7 produced. Diffing the two lists shows exactly what was decided since.

Inheritance is proved, not asserted. Screening decisions transfer between two versions only when
neither the eligibility criteria nor the gate structure differ, and against `v1_7` that is
machine-checkable: inclusion criteria I1 to I8, exclusion criteria E1 to E12, and the gate
structure D, A1 to A3, B0 to B5, C1 are identical in `v1_7` and `v3_0`. The operational boundary
that decides E6 differs only in modality and in the added rule that a deferred filter records its
code at the filter that owns it, never at Gate C; the data already conforms, since every gate B
code is stored in `gate_b_outcome`.

The day a version changes a criterion, that version re-screens: `INHERITED.md` is replaced by a
worked list of its own, derived from its `automated/source/`. Until then, re-screening would
reproduce the same 986 outcomes rather than test anything.

## Instruments read the protocol

`search/<ver>/scripts/criterios.py` parses the eligibility tables and the gate table out of that
version's `.tex`. The gate generators import it, so the criterion wording a reviewer reads is the
protocol's own, read at generation time, and each generator declares the filters and codes it uses
through `exige()`, which fails loudly when the protocol no longer defines one of them. The
second-reviewer sampling fraction is read from the protocol prose as well, replacing a `0.20`
written in the code beside a comment pointing at a v1.8 line number.

This was not cosmetic. The Gate B page claimed to show the literal wording of the protocol and
showed, for three of its four filters, the criterion belonging to a different code: B2 was
displaying E6's text, B3 was displaying E8's, and B4 was displaying E9's. The A004 migration had
renamed the outcome keys and left the hand-copied citations behind, and nothing checked the pairing
because nothing could. Reading from the protocol repairs it and makes the drift unrepresentable.

## Rules

- **Mutators are archive, not scripts.** `analysis/<ver>/scripts/aplicacoes/` holds the one-shot
  appliers that ran under that version, and they are never repointed when folders move. A mutator
  that no longer names the paths it actually wrote to has stopped being evidence of what it did.
  `v3_0` opens with that folder empty, and the emptiness is an assertion: no mutator has run under
  v3_0 yet.
- **A frozen version is byte-frozen.** Its scripts still reference the paths they referenced when
  they ran. Repointing them would make them stop being a record of what was executed.
- **Only the live version is maintained.** `v3_0` scripts read from `v3_0` folders. When `v4`
  opens, `v3_0` freezes as it stands and the new folder is repointed.
- **Opening a version records what it inherited.** Each `protocol/<ver>/CHANGELOG_<ver>.md` states
  the state at the moment of opening, so that inheritance is written and not assumed.

## Not versioned, and why

- `search/material/` (3.3 GB) holds what nobody re-derives: `pdfs/`, `pdfs.zip`, the dated
  `backups/`, and the retrieval caches. A published paper does not change with a protocol version
  and tripling it would cost about ten gigabytes. It was named `search/automated/` until it sat
  beside the version folders, each of which now has an `automated/` of its own; the name was the
  confusion, so it changed. **The `pdf_local_source` column stores `pdfs/<id>.pdf`, and that path
  now resolves against `search/material/`.** The data was not rewritten to follow a folder move.
- What the search *can* re-derive is versioned: the unified starting list, the per-source exports,
  and the six search validation logs of ACM, IEEE Xplore, and Scopus all live in each version's
  `automated/source/`.
- `protocol/amendments/`, `protocol/screening_manual_v*.md` and `protocol/screening_flow_v1.*`
  are cross-version: the amendments are the v1.x lineage record, and the manual in force is
  `screening_manual_v2.md` regardless of protocol version.
- `.local-evidence/` stays outside the repository, as it always has.

## Running the live version

```
bash analysis/scripts/gera_pdf_protocolo.sh            # renders v3_0; takes a version as argument
python3 protocol/v3_0/analysis/scripts/verifica_protocolo.py
python3 analysis/v3_0/scripts/gera_ficha_extracao.py
python3 analysis/v3_0/scripts/verifica_ficha.py
```
