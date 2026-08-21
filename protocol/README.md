# protocol/

One folder per protocol version, each self-contained. A version folder renders and verifies
without reaching outside itself, except for the codebook, which is an instrument over the data
and is deliberately shared.

```
protocol/
├── v1_7/ v2_0/ v3_0/                 one folder per version, identical layout
│   ├── appendix_two_layer_mapping_protocol_<ver>.tex     the source
│   ├── appendix_two_layer_mapping_protocol_<ver>.bib     frozen with the version
│   ├── appendix_two_layer_mapping_protocol_<ver>.{pdf,html,css}   generated, versioned
│   ├── CHANGELOG_<ver>.md
│   ├── build/protocol_standalone.tex                     render wrapper; the rest is ignored
│   └── analysis/scripts/
│       ├── gera_pdf_protocolo.sh                         pinned to this version, no arguments
│       └── verifica_protocolo.py                         locks specific to this version
├── amendments/                       A001 to A008, the v1.x lineage; v2.0 onward keeps a changelog
├── screening_manual_v1.md            first-pass record only, not for screening
├── screening_manual_v2.md            the manual in force
└── screening_flow_v1.{puml,svg,png}
```

Rendering, from the repository root:

```
bash analysis/scripts/gera_pdf_protocolo.sh          # defaults to v3_0
bash analysis/scripts/gera_pdf_protocolo.sh v2_0
bash protocol/v2_0/analysis/scripts/gera_pdf_protocolo.sh    # equivalent
```

The top-level script is a dispatcher that forwards to the version folder. The generated
`.pdf`, `.html`, and `.css` are versioned artifacts: if the `.tex` changes and they do not, the
diff says so. The build aborts on an unresolved citation or cross-reference.

Verifying:

```
python3 protocol/v3_0/analysis/scripts/verifica_protocolo.py
```

Locks are specific to a version because they assert content, not form. v3_0 carries 36, including
four families that exist because each one caught a real failure: `POLO` (the SQ1 and SQ2
vocabularies share no label), `POSSE` (every object named in a question text has a field owned by
that question), `TITULO` (single-sourced), and `PORTAO_C` (E12 is the only exit at Gate C, and
deferring a filter does not move it to another gate).

| Version | Lines | Pages | State |
|---|---|---|---|
| v1_7 | 1870 | 57 | superseded; kept for the amendment record and the search validation rounds |
| v2_0 | 1227 | 48 | frozen at the close of the whole-document review of 2026-08-21 |
| v3_0 | 1227 | 48 | live |

The codebook is not versioned by protocol version and lives at `analysis/extraction/`. Its
extraction rules cite the protocol by named anchor rather than by line number, so they stay true
across a version boundary without edit.
