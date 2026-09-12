"""Cluster analysis: representative examples + descriptive diagnostics.

Reads labels/probabilities/outlier scores from the clustering run, the UMAP
coordinates, the embedding matrix, and the embedding metadata sidecar, and
produces per-cluster representative examples plus descriptive diagnostics.

Representative strategy: start from the point closest to the cluster centroid
in UMAP space, then greedily add nearby-to-centroid points that are diverse in
embedding space (differs from the already-selected points), up to n_rep per
cluster. Clusters are referenced by number only -- NO final intent names are
assigned at this stage.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from discovery.config import load_json, save_json


def _pairwise_embedding_norms(X: np.ndarray) -> np.ndarray:
    """Row 2-norms for cosine similarity, handling the -1 label row."""
    return np.linalg.norm(X, axis=1, keepdims=True)


def select_representatives(
    coords: np.ndarray,
    embeddings: np.ndarray,
    indices: np.ndarray,
    n_rep: int,
    diversity_cosine: float = 0.90,
    seed: int = 42,
) -> list[int]:
    """Select diverse centroid-near representatives among `indices` (row ids).

    `indices` are the absolute row ids of one cluster. Returns a list of row ids.
    """
    rng = np.random.default_rng(seed)
    rows = np.asarray(indices)

    if len(rows) <= n_rep:
        return rows.tolist()

    cent = coords[rows].mean(axis=0)
    d = np.linalg.norm(coords[rows] - cent, axis=1)
    order = np.argsort(d)

    # Embedding row norms for cosine similarity.
    emb = embeddings[rows]
    norms = np.maximum(np.linalg.norm(emb, axis=1, keepdims=True), 1e-12)
    embn = emb / norms

    selected = []
    selected_sets = []
    used = set()
    for rank in order:
        if len(selected) >= n_rep:
            break
        if rank in used:
            continue
        cand = embn[rank]
        # Diversity: cosine similarity to any already-selected must stay below
        # the threshold, otherwise it is a near-duplicate of a chosen point.
        if any(float(cand @ s) > diversity_cosine for s in selected_sets):
            continue
        selected.append(int(rows[rank]))
        selected_sets.append(cand)
        used.add(rank)

    # If diversity filter starved the selection, top up with centroid-nearest
    # points not yet chosen.
    for rank in order:
        if len(selected) >= n_rep:
            break
        if rank not in used:
            selected.append(int(rows[rank]))
            used.add(rank)
    return selected


def intra_cluster_similarity(embeddings: np.ndarray, indices: np.ndarray, sample: int = 300, seed: int = 42) -> float:
    """Mean pairwise cosine similarity of a (capped) sample. Descriptive only."""
    idx = np.asarray(indices)
    if len(idx) < 2:
        return float("nan")
    if len(idx) > sample:
        idx = np.random.default_rng(seed).choice(idx, size=sample, replace=False)
    X = embeddings[idx]
    norms = np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)
    Xn = X / norms
    sims = Xn @ Xn.T
    tri = np.triu(sims, k=1)
    if tri.size == 0:
        return float("nan")
    return float(tri[tri != 0].mean())


def analyze_clusters(
    cluster_dir: Path,
    coords_path: Path,
    embeddings_path: Path,
    meta_path: Path,
    n_rep: int = 8,
    out_dir: Path | None = None,
):
    cluster_dir = Path(cluster_dir)
    out_dir = out_dir or cluster_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    labels = np.load(cluster_dir / "labels.npy")
    probs = np.load(cluster_dir / "probabilities.npy") if (cluster_dir / "probabilities.npy").exists() else np.ones_like(labels, dtype=float)
    outlier_scores = np.load(cluster_dir / "outlier_scores.npy") if (cluster_dir / "outlier_scores.npy").exists() else np.zeros_like(labels, dtype=float)
    coords = np.load(coords_path)
    embeddings = np.load(embeddings_path, mmap_mode="r")
    meta = pd.read_csv(meta_path)

    n = len(labels)
    if len(coords) != n or len(meta) != n:
        raise RuntimeError(f"alignment mismatch: labels={n} coords={len(coords)} meta={len(meta)}")

    n_clusters = int(labels.max()) + 1 if (labels >= 0).any() else 0
    rows = []
    for lab in range(n_clusters):
        mask = labels == lab
        idx = np.flatnonzero(mask)
        reps = select_representatives(coords, embeddings, idx, n_rep=n_rep)
        rep_df = meta.iloc[reps].copy()
        rep_df["cluster_id"] = lab
        rep_df["probability"] = probs[reps]
        rep_df["outlier_score"] = outlier_scores[reps]
        rep_df["customer_message_id"] = rep_df["customer_message_id"].astype("int64")
        rep_df["conversation_id"] = rep_df["conversation_id"].astype("int64")
        # order columns sensibly
        col_order = ["cluster_id", "customer_message_id", "conversation_id",
                     "probability", "outlier_score", "text"]
        rep_df = rep_df[[c for c in col_order if c in rep_df.columns]]
        rep_df.to_csv(out_dir / f"cluster_{lab}_representatives.csv", index=False)

        rows.append({
            "cluster_id": lab,
            "size": int(mask.sum()),
            "share": float(mask.sum() / n),
            "median_probability": float(np.median(probs[mask])),
            "mean_outlier_score": float(np.mean(outlier_scores[mask])),
            "intra_cluster_cosine": intra_cluster_similarity(embeddings, idx),
            "representative_customer_message_ids": ";".join(str(int(x)) for x in meta.iloc[reps]["customer_message_id"].tolist()),
        })

    summary = pd.DataFrame(rows)
    summary.to_csv(out_dir / "cluster_summary.csv", index=False)

    # Inter-cluster centroid similarity (embedding space).
    inter = {}
    if n_clusters > 1:
        centroids = np.array([
            np.mean(embeddings[labels == lab], axis=0) for lab in range(n_clusters)
        ])
        norms = np.maximum(np.linalg.norm(centroids, axis=1, keepdims=True), 1e-12)
        cn = centroids / norms
        sim_matrix = cn @ cn.T
        inter["mean_inter_cluster_cosine"] = float(
            (sim_matrix[np.triu_indices(n_clusters, k=1)].mean())
            if n_clusters > 1 else float("nan")
        )
        inter["min_inter_cluster_cosine"] = float(sim_matrix[np.triu_indices(n_clusters, k=1)].min())
        inter["max_inter_cluster_cosine"] = float(sim_matrix[np.triu_indices(n_clusters, k=1)].max())
    else:
        inter = {"mean_inter_cluster_cosine": float("nan")}

    diag = {
        "n_rows": n,
        "n_clusters": n_clusters,
        "n_noise": int((labels == -1).sum()),
        "noise_percentage": float(100 * (labels == -1).sum() / n) if n else 0.0,
        "largest_cluster_size": int(summary["size"].max()) if n_clusters else 0,
        "smallest_non_noise_cluster_size": int(summary["size"].min()) if n_clusters else 0,
        "median_cluster_size": float(summary["size"].median()) if n_clusters else float("nan"),
        "cluster_size_quantiles": {
            str(q): float(summary["size"].quantile(q)) for q in [0.5, 0.75, 0.9, 0.95, 0.99]
        } if n_clusters else {},
        **inter,
    }
    save_json(out_dir / "cluster_diagnostics.json", diag)

    # Human-readable report. Tentative observations only; no final intent names.
    lines = ["# Cluster Analysis (initial HDBSCAN run)",
             "",
             f"Rows analyzed: {n:,}",
             f"Non-noise clusters: {n_clusters:,}",
             f"Noise points (label -1): {diag['n_noise']:,} ({diag['noise_percentage']:.1f}%)",
             "",
             "## Cluster size summary",
             "| cluster_id | size | share | median_probability | intra_cluster_cosine |",
             "|---|---:|---:|---:|---:|"]
    for _, r in summary.iterrows():
        lines.append(f"| {int(r.cluster_id)} | {int(r['size']):,} | {r.share:.3%} | {r.median_probability:.3f} | {r.intra_cluster_cosine:.3f} |")
    lines += ["",
              "## Representative examples per cluster",
              "",
              "Representatives are chosen near the cluster centroid in UMAP space, "
              "with diversity enforced in embedding space (no near-duplicate reps). "
              "Full representative tables (cluster_<id>_representatives.csv) contain "
              "customer_message_id, conversation_id, probability, and original text.",
              ""]
    for lab in range(n_clusters):
        rep_df = pd.read_csv(out_dir / f"cluster_{lab}_representatives.csv")
        lines.append(f"### Cluster {lab}")
        for _, r in rep_df.iterrows():
            lines.append(f"- id={int(r.customer_message_id)} conv={int(r.conversation_id)} "
                         f"p={r.probability:.2f} :: {str(r.text)[:100]}")
        lines.append("")
    lines += ["",
              "> **Note:** these are tentative, unsupervised groupings. Cluster IDs are not "
              "business intents. No intent names ('delivery', 'refund', ...) are assigned yet.",
              ]
    lines += ["",
              "## Diagnostics",
              json.dumps(diag, indent=2, default=str),
              ]
    (out_dir / "CLUSTER_ANALYSIS.md").write_text("\n".join(lines))
    print(f"[cluster_analysis] wrote {out_dir / 'CLUSTER_ANALYSIS.md'} "
          f"and {out_dir / 'cluster_summary.csv'}")
    return out_dir


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cluster-dir", type=Path, required=True, help="dir with labels.npy etc.")
    p.add_argument("--coords", type=Path, required=True, help="umap_coords.npy")
    p.add_argument("--embeddings", type=Path, required=True, help="embeddings.npy")
    p.add_argument("--meta", type=Path, required=True, help="embeddings_meta.csv")
    p.add_argument("--n-rep", type=int, default=8)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    analyze_clusters(args.cluster_dir, args.coords, args.embeddings, args.meta,
                     n_rep=args.n_rep, out_dir=args.out)


if __name__ == "__main__":
    main()