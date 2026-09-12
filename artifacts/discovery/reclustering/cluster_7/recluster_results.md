# Cluster 7 re-clustering results (Phase 1D, TASK 3)

Subset: 12,267 points (initial cluster 7), ORIGINAL 384D embeddings, no recompute.
All experiments persisted under `artifacts/discovery/reclustering/cluster_7/`.

## Experiment A — fresh UMAP on subset (dims 8/15/20) x HDBSCAN (30,10)/(20,5)/(50,20)

Result (all 9 runs, `experiments_summary.csv`): **2 clusters, ~0 noise**,
largest ~12,199 + splinter ~68. UMAP re-fit on the subset re-normalizes to
local neighborhoods and collapses everything into one blob regardless of
target dimension or density threshold. Script: `scripts/recluster_cluster_7.py`
(note: initial run failed with FileNotFoundError — script used
`parent.parent.parent` for repo root instead of `parent.parent`; fixed, reran).

## Experiment B — HDBSCAN on GLOBAL 8D coords restricted to cluster 7

(`global_subset_experiments.csv`)

| experiment | clusters | noise | top sizes |
|---|---|---|---|
| g8_eom_30_10 (production thresholds) | 2 | 199 | 12003, 65 |
| g8_eom_20_5 | 2 | 401 | 11801, 65 |
| g8_eom_10_5 | 68 | 8937 (73%) | 857, 252, 228, ... |
| g8_leaf_30_10 | 25 | 10398 (85%) | 300, 247, 159, ... |
| g8_leaf_20_5 | 44 | 10270 (84%) | 152, 134, 129, ... |

At production thresholds the subset is one basin + splinter in global 8D
space. Finer thresholds fragment into dozens of shards with 73–85% noise —
not usable sub-intents, just density shredding.

## Experiment C — HDBSCAN on raw 384D (L2-normalized, euclidean = cosine order)

(`emb384_experiments.csv`; cosine metric unavailable in this sklearn BallTree —
`ValueError: Unrecognized metric 'cosine'` — so used euclidean on
L2-normalized vectors, which preserves cosine ordering. Bug documented, worked around.)

| experiment | clusters | noise |
|---|---|---|
| e384_euc_30_10 | 4 | 12002 (97.8%) |
| e384_euc_50_10 | 3 | 11989 (97.7%) |

The only dense cores in native embedding space are **stub-duplicate groups**:
core 0 = marketplace stubs ("@AmazonHelp Amazon.in" 17x, "Por Amazon" 13x,
"Amazon.de" 5x); core 1 = carrier stubs ("@AmazonHelp Amazon Logistics" 19x x2
casings); core 2 = Spanish "Vendido (y enviado) por Amazon" variants;
core 3 = "Amazon shipping" variants. The remaining ~12,000 points are diffuse —
no density structure at all.

## Conclusion

Cluster 7 is **not a density cluster in embedding space**; it is a basin
**created by the 8D UMAP compression**, glued by stub texts and the shared
"@AmazonHelp + Amazon/prime/delivery/refund/support" surface form (see
`cluster_7_analysis.md`). Density-based re-splitting of cluster 7 alone
cannot work in any tested space:

- re-UMAP on subset collapses (local renormalization),
- global-8D subset is one basin at sane thresholds,
- raw 384D is 98% diffuse.

Re-clustering cluster 7 by density is therefore **not justified**. The viable
paths are: (a) a higher-D GLOBAL representation that never forms the basin
(TESTED in TASK 5), or (b) downstream non-density treatment (seeded/topic
split or manual consolidation — TASK 10, Option C/D territory). The 68-point
splinter seen in Experiments A/B was not pursued: it is a density crumb, not
a customer goal.
