# Records of v3_0

Two layers, and the split is the point.

**Inherited.** Screening was executed once, under `v1_7`: pre-pass D and gates A, B and C over the
986 records of the starting list. That result was produced there and is frozen there. The worked
list here was seeded from it, and every gate A and gate B outcome in it is v1_7's, not this
version's. Inheritance is legitimate because neither the eligibility criteria nor the gate
structure differ between the two versions, which is machine-checkable: inclusion criteria I1 to I8,
exclusion criteria E1 to E12, and the gate structure D, A1 to A3, B0 to B5, C1 are identical.

**Own.** This version is live, so it also needs somewhere to write. Decisions taken from the point
v3_0 opened are recorded here and not in `v1_7`, which must keep saying what v1_7 produced. The
first of them is the filter C1 of `018_ACM`, the first decision of the extraction pilot, applied by
`analysis/v3_0/scripts/aplicacoes/aplica_c1_018.py`.

Comparing this list against `search/v1_7/automated/records/` therefore shows exactly what was
decided after v1_7 closed, which is the reason the two are kept apart rather than merged.

`backups/` holds the dated copy each mutator writes before touching the list.
