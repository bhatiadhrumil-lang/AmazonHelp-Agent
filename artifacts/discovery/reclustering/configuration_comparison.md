# Configuration comparison (Phase 1D, TASK 6 — diagnostic only)

Source tables: `global_umap_compare/comparison.csv`,
`cluster_7/experiments_summary.csv`, `cluster_7/global_subset_experiments.csv`,
`cluster_7/emb384_experiments.csv`. Statistics below are DIAGNOSTIC, not
accuracy. No winner is chosen on noise/cluster-count grounds (see TASK 10).

## Global UMAP dimensionality (same 93,171x384 embeddings, HDBSCAN 30/10/eom)

| configuration | umap_dim | n_neighbors | min_cluster_size | min_samples | clusters | noise_points | noise_pct | largest_cluster | median_cluster_size |
|---|---|---|---|---|---|---|---|---|---|
| baseline_8d_30_10 (Phase 1B, reused) | 8 | 30 | 30 | 10 | 203 | 49621 | 53.26 | 12267 | ~72* |
| dim_15 | 15 | 30 | 30 | 10 | 205 | 48690 | 52.26 | 12271 | 74 |
| dim_20 | 20 | 30 | 30 | 10 | 195 | 48613 | 52.18 | 12271 | 78 |

*median recomputed from cluster_size_summary.csv if needed; ~70s in all runs.

Reading: dims barely move anything — cluster count 195–205, noise 52–53%,
megacluster persists at 12,271 points (99.9% = old cluster 7). Small clusters
are stable (e.g. all 35 of old cluster 0 land in one dim-15 cluster).
Dimensionality is NOT the lever.

## Cluster-7-only experiments (12,267 points)

| experiment | space | clusters | noise | note |
|---|---|---|---|---|
| exp_{8,15,20}d x {(30,10),(20,5),(50,20)} (9 runs) | fresh UMAP on subset | 2 | 0–9 | one blob + splinter; UMAP local renormalization collapses |
| g8_eom_30_10 / g8_eom_20_5 | global-8D subset | 2 | 199 / 401 | one basin + 65-pt splinter at production thresholds |
| g8_eom_10_5 | global-8D subset | 68 | 8937 (73%) | density shredding, unusable |
| g8_leaf_30_10 / g8_leaf_20_5 | global-8D subset | 25 / 44 | ~85% noise | fragmenting, unusable |
| e384_euc_30_10 / e384_euc_50_10 | raw 384D L2-norm | 4 / 3 | ~98% noise | only stub-duplicate cores dense |

## Internal-metric policy

No silhouette/DBCV numbers are reported: with 53% noise and a dominant mixed
basin, internal metrics reward either the status quo or the shredding
configurations, both of which fail the semantic question. Coherence is judged
by reading messages (TASK 7), not by index values.
