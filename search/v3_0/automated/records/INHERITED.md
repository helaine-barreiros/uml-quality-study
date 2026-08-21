# Inherited result

No screening was executed under v3_0. The worked list and the decision log live in
`search/v1_7/automated/records/`, where they were produced, and are read from there.

Inheritance is claimed, so it is proved rather than asserted. Screening decisions transfer between
two versions only when neither the eligibility criteria nor the gate structure differ. Against
v1_7 that holds, and it is machine-checkable:

| Compared | v1_7 vs v3_0 |
| --- | --- |
| Inclusion criteria I1 to I8 | identical |
| Exclusion criteria E1 to E12 | identical |
| Gate structure D, A1 to A3, B0 to B5, C1 | identical |
| Operational boundary for substantive LLM use | differs in modality only, plus the rule that a deferred filter records its code at the filter that owns it and never at Gate C |

The one substantive difference is where a deferred decision is recorded, and the data already
conforms to it: every gate B code is stored in `gate_b_outcome` and none in `gate_c_outcome`.
No record changes outcome under v3_0. Re-screening would reproduce the same 986 outcomes rather than
test anything.

If a future version does change a criterion, this file is replaced by a re-screened worked list.
A blank sheet is derivable from `../source/custom_automated_search_collection.ris`.
