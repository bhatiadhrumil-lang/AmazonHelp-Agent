# Updated merge/split analysis (Phase 1D, TASK 8)

Originals preserved untouched under `artifacts/discovery/taxonomy/`
(`merge_candidates.csv`, `split_candidates.csv`, `cluster_interpretation.csv`).
This file records DELTAS under the tested configurations. Taxonomy is NOT
finalized.

## Merge candidates under dim_15 (same families?)

Each Phase 1C merge group's members were located in the dim_15 labeling:

| group | n | dim_15 top clusters | reading |
|---|---|---|---|
| MG-01 thanks (19 clusters) | 1559 | -1: 244, 104: 192, +rest scattered | FRAGMENTS: dim_15 splits the cleanest high-dup family |
| MG-02 will-do/done (8) | 666 | 75: 174, 136: 102, +rest | fragments |
| MG-03 short answers (8) | 942 | -1: 201, 142: 199, +rest | fragments |
| MG-04 waiting nudges (2) | 138 | 163: 86, 164: 35 | splits in two |
| MG-05 no-response (3) | 1016 | 22: 543, 188: 261 | splits in two |
| MG-06 details-provided (14) | 2203 | 11: 478, 48: 376, +rest | fragments |
| MG-07 link issues (4) | 253 | 54: 132, 53: 47 | splits in two |
| MG-08 carrier id (5) | 345 | 88: 112, 94: 94 | splits in two |
| MG-09 status ask (4) | 597 | 18: 272, 29: 204 | splits in two |

Every merge group stays *nearby* (members land in 2–4 adjacent dim_15
clusters, not scattered randomly), confirming the families are real — but
dim_15 does NOT consolidate them; it fractures them further while also
dropping 15–25% of each family into noise. Net: dim_15 is WORSE for the
merge side. Recommendation: keep Phase 1C merge groups as stated; do not
re-derive merges from dim_15/20.

## Split candidates under dim_15/20

- Split candidate 7 (12,267): CONFIRMED UNSPLITTABLE by density in every
  tested space (see `cluster_7/recluster_results.md`). dim_15/20 reproduce it
  at 12,271 points, 99.9% overlap. Status stays `proposed`, method changes to
  non-density treatment (TASK 10).
- Split candidates 59 (URL-attachments), 42 (transitional), 122 (emoji
  chatter), 156→151 (Prime), 139→93 (support quality), 184, 143: all persist
  as recognizable clusters in dim_15 (151/93 verified by reading; the rest by
  size correspondence). No split candidate is resolved by the new configs;
  none is refuted either. All statuses unchanged.

## Interpretation delta

No per-cluster interpretation is rewritten in this phase (TASK 8 says do not
finalize). Two annotations for the next taxonomy pass:
1. Cluster 7's `possible_parent_intent` ("Needs re-clustering") should become
   "Mixed basin — hierarchical/seeded split required; density split tested
   and rejected".
2. dim_15 clusters 151 (Prime) and 93 (support quality) corroborate families
   `prime_*` and `complaint_service_quality` — raise their confidence, do not
   renumber anything.
