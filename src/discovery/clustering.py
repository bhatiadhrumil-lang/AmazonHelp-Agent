"""HDBSCAN clustering on saved UMAP coordinates.

Operates ONLY on persisted UMAP coordinates; no embeddings or UMAP are
regenerated. Rerunning with different parameters reuses the input artifact.
Label -1 is treated as noise/outlier and never given a business intent.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from discovery.config import HdbscanConfig, load_json, save_json


def load_coords(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"UMAP coords artifact not found: {path}")
    return np.load(path)


def cluster_hdbscan(coords_path: Path, out_dir: Path, cfg: HdbscanConfig):
    out_dir.mkdir(parents=True, exist_ok=True)
    coords = load_coords(coords_path)
    n, d = coords.shape

    import hdbscan

    print(f"[hdbscan] clustering {n:,} x {d} "
          f"(min_cluster_size={cfg.min_cluster_size}, min_samples={cfg.min_samples}, "
          f"metric={cfg.metric}, method={cfg.cluster_selection_method})")
    t0 = time.time()
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=cfg.min_cluster_size,
        min_samples=cfg.min_samples,
        metric=cfg.metric,
        cluster_selection_method=cfg.cluster_selection_method,
        prediction_data=cfg.prediction_data,
        gen_min_span_tree=True,
    )
    clusterer.fit(coords)
    labels = np.asarray(clusterer.labels_, dtype=np.int64)
    probs = np.asarray(clusterer.probabilities_, dtype=np.float64)
    outlier_scores = np.zeros(n, dtype=np.float64)
    if hasattr(clusterer, "outlier_scores_"):
        glosh = np.asarray(clusterer.outlier_scores_, dtype=np.float64)
        if glosh.shape == (n,):
            outlier_scores = glosh
    if outlier_scores.sum() == 0:
        outlier_scores = np.zeros(n, dtype=np.float64)
        for lab in np.unique(labels):
            mask = labels == lab
            cents = coords[mask].mean(axis=0) if lab >= 0 else np.nan
            if lab == -1:
                outlier_scores[mask] = np.linalg.norm(coords[mask] - coords[labels >= 0].mean(axis=0), axis=1)
            else:
                outlier_scores[mask] = np.linalg.norm(coords[mask] - cents, axis=1)
    if outlier_scores.sum() == 0:
        print("[hdbscan] WARNING outlier scoring unavailable; storing zeros")
    print(f"[hdbscan] fit in {time.time() - t0:.1f}s")

    if len(labels) != n or len(probs) != n:
        raise RuntimeError(f"label/prob length mismatch: labels={len(labels)} probs={len(probs)} coords={n}")

    np.save(out_dir / "labels.npy", labels)
    np.save(out_dir / "probabilities.npy", probs)
    np.save(out_dir / "outlier_scores.npy", outlier_scores)

    n_clusters = int(labels.max()) + 1 if (labels >= 0).any() else 0
    n_clustered_points = int((labels >= 0).sum())
    n_noise = int((labels == -1).sum())
    config = {
        "hdbscan": {
            "min_cluster_size": cfg.min_cluster_size,
            "min_samples": cfg.min_samples,
            "metric": cfg.metric,
            "cluster_selection_method": cfg.cluster_selection_method,
            "prediction_data": cfg.prediction_data,
        },
        "input_umap_coords": str(coords_path),
        "input_umap_config": load_json(Path(coords_path).parent / "umap_config.json")
        if (Path(coords_path).parent / "umap_config.json").exists()
        else None,
        "n_rows": int(n),
        "n_clusters": n_clusters,
        "n_clustered_points": n_clustered_points,
        "n_noise": n_noise,
        "noise_percentage": float(100 * n_noise / n) if n else 0.0,
    }
    save_json(out_dir / "hdbscan_config.json", config)

    # Descriptive cluster-size summary (not a quality claim).
    sizes = pd.Series(labels).value_counts().sort_index()
    rows = []
    for lab, size in sizes.items():
        name = "-1" if lab == -1 else str(int(lab))
        rows.append({"label": int(lab), "cluster_id": name, "size": int(size),
                     "share": float(size / n)})
    cluster_summary = pd.DataFrame(rows)
    cluster_summary.to_csv(out_dir / "cluster_size_summary.csv", index=False)

    print(f"[hdbscan] clusters={n_clusters} ({n_clustered_points:,} points) noise={n_noise} ({100*n_noise/n:.1f}%)")
    if n_clusters:
        nb = sizes[sizes.index != -1]
        print(f"[hdbscan] largest={nb.max()} smallest_non_noise={nb.min()} median={nb.median():.0f}")
    return out_dir


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("coords_path", type=Path)
    p.add_argument("--out", type=Path, default=Path("artifacts/discovery/clustering/initial"))
    p.add_argument("--min-cluster-size", type=int, default=30)
    p.add_argument("--min-samples", type=int, default=10)
    p.add_argument("--metric", default="euclidean")
    p.add_argument("--cluster-selection-method", default="eom")
    args = p.parse_args()

    cfg = HdbscanConfig(
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples,
        metric=args.metric,
        cluster_selection_method=args.cluster_selection_method,
    )
    cluster_hdbscan(args.coords_path, args.out, cfg)


if __name__ == "__main__":
    main()