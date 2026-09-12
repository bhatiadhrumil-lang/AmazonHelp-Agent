# AmazonHelp Conversation-Quality Audit — Reproducibility & Process Summary

This document records how the authoritative customer-problem corpus was produced for the
TWCS (Customers on Twitter) full dataset, the implementation bug found and fixed along the
way, and the verification that was performed. It also records the Phase 1B intent-discovery
pipeline (embeddings -> UMAP -> HDBSCAN -> cluster analysis).

## 1. Environment (reproducible)

Pinned via `pyproject.toml`, `uv.lock`, and `.python-version`:

- Python `3.12.13` (project requires `>=3.12,<3.13`) in `.venv/`
- `pandas 2.3.3`, `numpy 1.26.4`, `torch 2.14.0+cpu`, `sentence-transformers 6.0.1`,
  `transformers 5.17.0`, `umap-learn 0.5.12`, `hdbscan 0.8.44`, `scikit-learn 1.6.1`,
  `tqdm 4.70.1`, `pytest 9.1.1` (dev group)
- Package manager: `uv` (`uv sync`, `uv lock --check` both pass)
- Working dir: `/home/dhrumil/Desktop/agent-amazon`
- System default python is 3.14.4 — do **not** use it; always use `.venv/bin/python`.

## 2. Exact commands to reproduce

```bash
# Smoke test on a small subset (47,211 logical rows).
.venv/bin/python src/data/conversation_quality_audit.py \
  artifacts/smoke/smoke_subset.csv --out artifacts/conversation_audit/smoke_run_fixcheck

# Full audit on the complete TWCS dataset (inside archive.zip: twcs/twcs.csv).
.venv/bin/python src/data/conversation_quality_audit.py archive.zip \
  --out artifacts/conversation_audit/full_run_fixed
```

Outputs written to the `--out` directory:

- `conversation_components_audit.csv` — root-anchored components connected to AmazonHelp
- `customer_problem_episodes.csv` — one row per direct customer -> AmazonHelp interaction
- `audit_summary.json` — machine-readable counts/quantiles
- `AUDIT_REPORT.md` — human-readable report

Thresholds (all configurable via CLI flags): `--gap-flag-hours 72`,
`--long-conversation-flag 30`, `--very-long-conversation-exclude 150`,
`--min-customer-chars 1`.

## 3. Final results (full dataset, corrected run)

| Metric | Value |
|---|---:|
| Dataset rows | 2,811,774 |
| AmazonHelp tweets | 169,840 |
| AmazonHelp-connected components | 82,534 (KEEP 42,408 / FLAG 2,193 / EXCLUDE 37,933) |
| Direct customer -> AmazonHelp episodes | 100,503 (KEEP 93,171 / FLAG 5,653 / EXCLUDE 1,679) |
| Components with brand messages | 100% of 82,534 (defined by brand membership) |

Episode characteristics (full run): median text length 103 chars (p99 289);
components median 3 messages (p99 21).

Artifacts of the corrected full run: `artifacts/conversation_audit/full_run_fixed/`.

## 4. Bug found in `build_root_map`

The original root-map reconstruction silently **dropped 395 valid episodes** and produced
753 spurious components.

- Root cause: the vectorized pointer-jumping loop advanced every pointer by exactly **one
  ancestor hop per iteration** (it read the static `parent_sorted` array, not the evolving
  `ptr` array), but bounded itself with a hard `range(32)`. Reply chains in TWCS reach
  **hundreds of hops** (observed up to ~650); chains deeper than the cap were truncated to a
  mid-chain tweet, so a customer tweet and its AmazonHelp parent could resolve to **different
  roots** and the customer tweet was excluded from brand components entirely.
- Second defect (same family): when a tweet's parent ID was absent from the dataset, the
  "anchor" row was marked broken at its own ID while its descendants resolved to the absent
  parent ID — again splitting one chain across two roots.
- Fix (in `src/data/conversation_quality_audit.py`): the loop now iterates **until no active
  pointers remain** (capped at `n` as a pure safety net for pathological cycles) instead of a
  fixed 32 rounds; absent parents now anchor at the absent parent ID consistently for the
  whole chain. Semantics otherwise unchanged.

## 5. Verification

Independent naive-walk verification (separate script walking parent pointers one-by-one)
against the corrected full-run artifacts:

- `audit roots == naive brand roots`: 82,534 == 82,534, exact set equality
  (in-mine-not-audit 0, in-audit-not-mine 0)
- `episodes == naive direct candidates`: 100,503 == 100,503 (0 missing, 0 extras)
- Every `conversation_id` in the episode table belongs to the brand-root set

Recovery check vs the buggy run:

- buggy episodes 100,108, corrected 100,503 = **+395 exactly the previously missing
  candidates**, 0 removed; conversation 16882 (tweet 16887) confirmed as a recovered example.

Output validation:

- 0 duplicate `customer_message_id`; `episode_status` only in {KEEP, FLAG, EXCLUDE}
- All episodes have non-null timestamps and non-empty `brand_parent_text`
- `char_len` consistent with `text`; all required columns present in both tables
- Single-tweet synthetic unit tests pass: 700-deep and 650-deep chains, branch chains,
  absent-parent chains, parent cycles (break/open graph).

Smoke test on `artifacts/smoke/smoke_subset.csv` (47,211 rows) also matches the naive walk
exactly (components 1,233; episodes 1,830; 0 missing / 0 extras).

## 6. Process summary

1. Pinned the Python environment (`pyproject.toml`, `uv.lock`, `.python-version`).
2. Verified raw-dataset facts independently: 2,811,774 rows, 169,840 AmazonHelp, 0 duplicate
   tweet_ids, 3,862 parent refs to absent IDs, clean `created_at` parsing, chain depth up to ~650.
3. Ran the audit script on a smoke subset and confirmed reproducible baseline counts.
4. Ran the full audit -> found episode count (100,108) below the independently computed
   candidate count (100,503) -> 395 dropped.
5. Isolated root cause in `build_root_map` (one-hop pointer jumping truncated at 32 rounds;
   absent-parent anchor inconsistency), fixed both defects, and held the methodology fixed.
6. Re-ran smoke (matches naive walk exactly) and the full audit.
7. Verified the corrected full run against the independent naive walk (exact root-set and
   episode-set equality) and validated all output schemas/counts.

**Next step (not performed):** embeddings -> UMAP -> HDBSCAN on the episode corpus.

## 7. Phase 1B — intent-discovery pipeline

Locked configuration, exact commands, and artifact checksums for the discoverability pipeline.
Pipeline code lives in `src/discovery/` (`config.py`, `embeddings.py`,
`dimensionality_reduction.py`, `clustering.py`, `cluster_analysis.py`). Every stage operates
**only on persisted artifacts** and writes a self-describing JSON config next to its outputs.

### 7.1 Embeddings (`src/discovery/embeddings.py`)

- Input: `artifacts/conversation_audit/full_run_fixed/customer_problem_episodes.csv`, `status == KEEP`
  only (93,171 of 100,503 rows).
- Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, 384-dim, batch 64, CPU,
  float32, `normalize=True` (cosine-sim ready). Deterministic seed 42.
- Embedding input is *customer-side problem context only*: raw text is HTML-unescaped, leading
  `@AmazonHelp` stripped, whitespace collapsed. Mid-text `@AmazonHelp`/mentioned-handle references
  are kept; `parent_id` (brand reply) context is intentionally excluded from the input signal.
- Output: `artifacts/discovery/embeddings/full/` = `embeddings.npy` (93,171 x 384 float32),
  `embeddings_meta.csv` (row-aligned; `customer_message_id`/`conversation_id` order matches the
  KEEP subset), `config.json`, resume-safe `progress.json`.
- Verification: 0 non-finite values; `n_rows == 93,171`; meta row order matches the KEEP filter;
  rebuilt `embedding_input` reproduces the saved column exactly.
- Storage: 143 MB matrix + ~30 MB meta on disk; model peak RSS ~1.2 GiB on CPU.

### 7.2 UMAP (`src/discovery/dimensionality_reduction.py`)

- Command:
  `PYTHONPATH=src .venv/bin/python -m discovery.dimensionality_reduction artifacts/discovery/embeddings/full/embeddings.npy --out artifacts/discovery/umap/full`
- Config: `n_components=8, n_neighbors=30, metric=cosine, min_dist=0.1, random_state=42`.
- Output: `artifacts/discovery/umap/full/umap_coords.npy` (93,171 x 8 float32, all finite);
  `umap_config.json` records config + input SHA-256 `dfc88b72…6557d` + input shape.

### 7.3 HDBSCAN (`src/discovery/clustering.py`)

- Command:
  `PYTHONPATH=src .venv/bin/python -m discovery.clustering artifacts/discovery/umap/full/umap_coords.npy --out artifacts/discovery/clustering/initial`
- Config: `min_cluster_size=30, min_samples=10, metric=euclidean, cluster_selection_method=eom,
  prediction_data=True`.
- Result: **203 clusters** over 43,550 points; 49,621 noise (53.3%). Largest 12,267 (13.2%),
  median 74, smallest 30. Outlier scores = GLOSH (`outlier_scores_`); if unavailable they fall
  back to per-cluster centroid distance in UMAP space (never fabricated).
- Outputs: `labels.npy`, `probabilities.npy`, `outlier_scores.npy`, `cluster_size_summary.csv`,
  `hdbscan_config.json`.

### 7.4 Cluster analysis (`src/discovery/cluster_analysis.py`)

- Command:
  `PYTHONPATH=src .venv/bin/python -m discovery.cluster_analysis --cluster-dir artifacts/discovery/clustering/initial --coords artifacts/discovery/umap/full/umap_coords.npy --embeddings artifacts/discovery/embeddings/full/embeddings.npy --meta artifacts/discovery/embeddings/full/embeddings_meta.csv`
- Outputs: `cluster_summary.csv` (per-cluster size/share/median probability/mean GLOSH/
  intra-cluster cosine similarity), `cluster_<id>_representatives.csv` (up to 8 per cluster, chosen
  nearest centroid in UMAP space with embedding-space diversity via max-cosine < 0.90),
  `cluster_diagnostics.json` (noise %, size quantiles, mean inter-cluster centroid cosine),
  `CLUSTER_ANALYSIS.md` (full human-readable report with per-cluster examples).
- **Discipline:** clusters are referenced by number only (`Cluster N`). No final intent names
  ("delivery", "refund", …) are assigned in Phase 1B. Intra/inter cluster similarities are
  descriptive diagnostics only — they are **not** claims of labeling accuracy (unsupervised).

### 7.5 Determinism

- Embeddings and UMAP fix `random_state=42`. UMAP records the input SHA-256. HDBSCAN is
  deterministic given identical coordinates.
- Re-running the full audit with the current script deterministically reproduces
  `full_run_fixed` counts (100,503 episodes, 82,534 components, KEEP 93,171). See
  `artifacts/conversation_audit/<run>_verify/` for the verification run if present.

## 8. Phase 1B procedure (summary)

1. Locked dependencies (`torch`, `sentence-transformers`, `umap-learn`, `hdbscan`,
   `scikit-learn`, `tqdm`; `pytest` in dev group) via `pyproject.toml` + `uv.lock`; verified
   model + library imports in `.venv` (Python 3.12.13; do not use system 3.14.4).
2. Implemented `src/discovery/`: `config.py`, `embeddings.py`, `dimensionality_reduction.py`,
   `clustering.py`, `cluster_analysis.py`. Each stage consumes only persisted artifacts and
   writes self-describing JSON configs.
3. Confirmed embedding input is customer-side only (strip leading `@AmazonHelp`, unescape, trim;
   never `brand_parent_text`); validated on real KEEP rows (0 empty inputs, 93,171).
4. Estimated storage (~143 MB matrix) and RAM (~1.2 GiB model peak) against the 6.5 GiB box.
5. Smoke-tested embeddings (500 rows; 500 x 384, 0 non-finite, aligned meta) then ran the full
   93,171-row embedding wave on CPU (~3.9 h; resumed via `progress.json`).
6. Smoke-tested UMAP (500 -> 8d) then the full UMAP fit (93,171 x 8, all finite), recording the
   input SHA-256.
7. Ran HDBSCAN (min_cluster_size=30, min_samples=10, euclidean, eom, prediction_data): **203
   clusters**, 43,550 clustered points, 49,621 noise (53.3%). Fixed a reporting bug where
   `n_clusters` counted clustered *points* instead of distinct cluster ids.
8. Cluster analysis: per-cluster representatives (centroid-near + diversity-constrained),
   `cluster_summary.csv`, `cluster_diagnostics.json` (intra/inter-cluster cosine descriptives —
   not accuracy claims), and `CLUSTER_ANALYSIS.md`. No final intent names assigned (Cluster N).
9. Re-verified the Phase 1A `build_root_map` fix deterministically: fresh full run reproduces
   `full_run_fixed` exactly (100,503 episodes / 82,534 components, 0-set-diff; +395 vs the buggy
   backup, 0 removed).
10. Added ~20 unit tests (config round-trip, embedding transforms, HDBSCAN artifact contract,
    representative diversity, similarity helpers); all pass. No changes to authoritative audit
    artifacts (discovery writes only under `artifacts/discovery/`).

**Next phase (not started):** final intent taxonomy from the 203 clusters — naming, hierarchy,
and validation are deliberately left for a separate phase.