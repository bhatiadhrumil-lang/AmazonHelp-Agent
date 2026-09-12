# Leakage / duplicate / traceability checks (Phase 1C, TASK 11)

- Input meta rows: 93171 (embeddings_meta full, row-aligned with labels).
- Clustered (labels != -1): 43550; noise (labels == -1): 49621.
- Noise sample: 150 rows; validation candidates: 185 rows.

## Per-check results

| check | ok | detail |
|---|---|---|
| noise_sample rows all HDBSCAN-noise | True | n=150; labels present: [-1] |
| noise_sample ids are true noise (not clustered) | True | 0 rows not in labels==-1 |
| no duplicated (conversation_id, customer_message_id) in validation sample | True | duplicate rows=0 |
| all validation candidate ids exist in embeddings_meta (full) | True | missing ids=0 |
| validation cluster-source vs noise-source ids disjoint | True | overlap ids=0 |
| validation noise-source ids are HDBSCAN-noise | True | non-noise ids=0 |
| validation cluster-source ids are clustered | True | non-clustered ids=0 |
| no validation id repeated within the same source pick block | True | repeated-in-noise ids=0 |
| cross-cluster exact-duplicate texts (merge signal, not leakage) | True | 0 exact texts shared by >1 cluster (capped report to 10) |

## Cross-cluster exact duplicates (evidence for MERGES, NOT leakage)

A customer message belongs to exactly one cluster (HDBSCAN). The same *template* text appearing in several clusters is therefore a **merge signal** (the clusters are near-duplicate conversation-closure turns), not a data leak. Top examples:

| exact_text | n clusters | clusters |
|---|---|---|

## Notes
- All noise-sample rows verified to carry HDBSCAN label == -1 and to come from the noise point set.
- All validation candidates verify against embeddings_meta (full); nothing references a message id that does not exist in the pipeline.
- Cluster-source and noise-source validation rows are disjoint by construction and re-verified here.