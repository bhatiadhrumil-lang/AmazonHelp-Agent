# Golden-candidate sampling report

Produced 204 candidates (seed 20240517).

## Stratum counts

| reason | n |
|---|---|
| common_confident | 24 |
| common_boundary | 24 |
| rare_cluster | 16 |
| low_probability_boundary | 14 |
| noise_diverse | 14 |
| split_cluster7 | 12 |
| common_random | 12 |
| multilingual | 12 |
| short_message | 10 |
| contextual_turn | 10 |
| safety_sensitive | 8 |
| ood_candidate | 8 |
| noise_near_cluster | 8 |
| ordinary_random | 4 |
| merge_MG-09 | 2 |
| merge_MG-08 | 2 |
| split_c139 | 2 |
| split_c143 | 2 |
| split_c156 | 2 |
| merge_MG-07 | 2 |
| merge_MG-06 | 2 |
| merge_MG-05 | 2 |
| merge_MG-04 | 2 |
| merge_MG-03 | 2 |
| merge_MG-02 | 2 |
| merge_MG-01 | 2 |
| split_c42 | 1 |
| split_c122 | 1 |
| split_c184 | 1 |
| split_c59 | 1 |

## Method

12-stratum active-learning-style coverage (common/confident+boundary+random, rare, low-probability, merge, split, noise, contextual, short, multilingual, OOD, safety, ordinary). Uncertainty proxy = centroid similarity margin. Dedup by row; label fields intentionally absent — labels are collected by the annotation tool into golden_labels.csv.
