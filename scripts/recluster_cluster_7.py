"""TASK 3: re-cluster ONLY cluster 7 on the ORIGINAL 384D embeddings.

Matrix: UMAP n_components in {8,15,20} x HDBSCAN (min_cluster_size, min_samples)
in {(30,10),(20,5),(50,20)} = 9 experiments. UMAP fixed: n_neighbors=30,
min_dist=0.1, metric=cosine, random_state=42. HDBSCAN fixed: eom, euclidean.

Persists per experiment under artifacts/discovery/reclustering/cluster_7/exp_<u>d_<mcs>_<ms>/:
  config.json, umap_coords.npy, labels.npy, probabilities.npy, run_summary.json
Plus experiments_summary.csv at the cluster_7 level.
Original clustering is never touched.
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts/discovery/reclustering/cluster_7"
EMB = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
LABELS = ROOT / "artifacts/discovery/clustering/initial/labels.npy"

UMAP_DIMS = [8, 15, 20]
HDBSCAN_GRID = [(30, 10), (20, 5), (50, 20)]

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lab = np.load(LABELS)
    idx7 = np.flatnonzero(lab == 7)
    E = np.load(EMB, mmap_mode="r")
    X = np.asarray(E[idx7]).astype(np.float32)
    assert X.shape == (12267, 384), X.shape
    assert np.isfinite(X).all()
    rows, summaries = [], []
    for ud in UMAP_DIMS:
        t0 = time.time()
        coords = UMAP(n_components=ud, n_neighbors=30, min_dist=0.1,
                      metric="cosine", random_state=42).fit_transform(X)
        ut = time.time() - t0
        assert np.isfinite(coords).all()
        for mcs, ms in HDBSCAN_GRID:
            name = f"exp_{ud}d_{mcs}_{ms}"
            d = OUT / name
            d.mkdir(exist_ok=True)
            t1 = time.time()
            cl = HDBSCAN(min_cluster_size=mcs, min_samples=ms,
                         cluster_selection_method="eom", metric="euclidean",
                         prediction_data=True)
            labels = cl.fit_predict(coords)
            ht = time.time() - t1
            assert len(labels) == len(idx7)
            assert set(np.unique(labels)) <= set(range(-1, labels.max() + 1))
            n_cl = int((labels != -1).max() + 1) if (labels != -1).any() else 0
            n_cl = len(set(labels.tolist()) - {-1})
            n_noise = int((labels == -1).sum())
            sizes = sorted(((labels[labels != -1] == k).sum() for k in set(labels.tolist()) - {-1}), reverse=True)
            np.save(d / "umap_coords.npy", coords.astype(np.float32))
            np.save(d / "labels.npy", labels.astype(np.int64))
            np.save(d / "probabilities.npy", cl.probabilities_.astype(np.float32))
            cfg = {"scope": "cluster_7_only", "n_points": len(idx7),
                   "corpus_rows": idx7.tolist() if False else "see corpus_row_map.npy",
                   "umap": {"n_components": ud, "n_neighbors": 30, "min_dist": 0.1,
                            "metric": "cosine", "random_state": 42},
                   "hdbscan": {"min_cluster_size": mcs, "min_samples": ms,
                               "cluster_selection_method": "eom", "metric": "euclidean"},
                   "umap_seconds": round(ut, 1), "hdbscan_seconds": round(ht, 1)}
            np.save(d / "corpus_row_map.npy", idx7.astype(np.int64))
            (d / "config.json").write_text(json.dumps(cfg, indent=2))
            summ = {"experiment": name, "umap_dim": ud, "min_cluster_size": mcs,
                    "min_samples": ms, "n_clusters": n_cl, "n_noise": n_noise,
                    "noise_pct": round(100 * n_noise / len(idx7), 2),
                    "largest": int(sizes[0]) if sizes else 0,
                    "median_size": float(np.median(sizes)) if sizes else 0.0,
                    "umap_s": round(ut, 1), "hdbscan_s": round(ht, 1)}
            (d / "run_summary.json").write_text(json.dumps(summ, indent=2))
            summaries.append(summ)
            print(name, summ, flush=True)
    pd.DataFrame(summaries).to_csv(OUT / "experiments_summary.csv", index=False)
    print("wrote", OUT / "experiments_summary.csv")

if __name__ == "__main__":
    main()
