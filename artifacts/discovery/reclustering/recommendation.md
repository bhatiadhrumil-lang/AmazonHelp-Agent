# Next-taxonomy strategy recommendation (Phase 1D, TASK 10)

## Evidence ledger

1. Cluster 7 (12,267) is a UMAP-created basin, not a density cluster: raw
   384D is 98% diffuse; only stub-duplicate cores are dense. Density
   re-splitting tested in 4 spaces and rejected everywhere.
2. Global 15D/20D reruns change nothing semantically (megacluster 99.9%
   identical; small clusters stable; noise 53.26% -> ~52.2%; but merge
   families FRACTURE under dim_15). Dimensionality is not the lever.
3. Finer HDBSCAN only shreds (73–85% noise shards). Parameterization is not
   the lever either — production (30,10) is the sane setting.
4. Noise v2 (n=341): ~59% fits known themes, ~20% needs thread context, ~12%
   social/venting, ~4% fragments, ~5% genuinely novel. Noise is mostly
   recoverable material, not junk.
5. Context probe (n=300, controlled): +customer-context moves thread turns
   from rank 5.0 to rank 1.09 toward their conversation centroid (298/300
   better-or-tied). Context is the one lever with a large measured effect —
   but only for the ambiguous slice (~20% thread + transitional/template).

## Choice: Option D (hybrid), with C-flavored execution

- **Keep the existing global clustering as the reference** (Option A core):
  203 clusters stand; merge groups MG-01..MG-09 stand; small clusters are
  stable across every rerun. Do not rechurn the base.
- **Targeted re-discovery, not global re-clustering** (reject B): no global
  config improves on baseline semantically.
- **Hierarchical where it counts** (Option C locally): for cluster 7, split
  by NON-density means — seeded/topic-guided separation along the T1–T15
  candidate sub-intents from `cluster_7_analysis.md`, validated by reading,
  not by density thresholds. Expect a residual sentiment-veneer sub-cluster;
  that is a finding, not a failure.
- **Second-view context clustering for the ambiguous slice only** (TASK 9
  recommendation): prev-customer-turn + message inputs, same embedding model,
  ~5–8k rows (transitional/template/thread-turn/noise-thread), clustered
  separately; used to resolve thread turns and peel veneer off topics. Solo
  taxonomy stays the reference frame.
- **Noise triage, not noise forcing**: route v2 buckets — fits-theme to
  nearest-family review, thread-turns to the context view, social/venting to
  OOD, fragments to data-quality notes, rare/novel (~5%) to candidate new
  intents pending human validation.

## What this rules out

- Adopting dim_15/20 globally (B): costs compute, fractures merge families,
  fixes nothing.
- Density-splitting cluster 7 (any variant): falsified in 4 spaces.
- Full-corpus context rebuild now: premature; 51% single-turn convs gain
  nothing and the probe is a proxy, not a clustering run.
- Freezing the taxonomy now: NO — megacluster + noise triage + human
  validation must precede any freeze.
