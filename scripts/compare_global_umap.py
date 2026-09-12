"""TASK 5: controlled global UMAP dimensionality comparison.

Same 93,171 x 384 embedding matrix (never regenerated). UMAP fixed params
(n_neighbors=30, min_dist=0.1, metric=cosine, random_state=42), only
n_components varies in {15, 20} (8D baseline = original Phase 1B run, reused
as-is). HDBSCAN fixed at production config (30, 10, eom, euclidean).

Persists under artifacts/discovery/reclustering/global_umap_compare/dim_<n>/:
  config.json, umap_coords.npy, labels.npy, probabilities.npy, run_summary.json
Plus comparison.csv at the global_umap_compare level (includes the 8D baseline
row read from the original artifacts).
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts/discovery/reclustering/global_umap_compare"
EMB = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
BASE_CFG = ROOT / "artifacts/discovery/clustering/initial/hdbscan_config.json"

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    E = np.load(EMB, mmap_mode="r")
    assert E.shape == (93171, 384) and np.isfinite(E).all()
    X = np.asarray(E).astype(np.float32)
    rows = []
    base = json.loads(BASE_CFG.read_text())
    rows.append({"experiment": "baseline_8d_30_10", "umap_dim": 8,
                 "min_cluster_size": 30, "min_samples": 10,
                 "n_clusters": base["n_clusters"], "n_noise": base["n_noise"],
                 "noise_pct": round(base["noise_percentage"], 2),
                 "note": "original Phase 1B artifacts, not recomputed"})
    for ud in [15, 20]:
        name = f"dim_{ud}"
        d = OUT / name
        d.mkdir(exist_ok=True)
        t0 = time.time()
        coords = UMAP(n_components=ud, n_neighbors=30, min_dist=0.1,
                      metric="cosine", random_state=42).fit_transform(X)
        ut = time.time() - t0
        assert np.isfinite(coords).all(), name
        t1 = time.time()
        cl = HDBSCAN(min_cluster_size=30, min_samples=10,
                     cluster_selection_method="eom", metric="euclidean",
                     prediction_data=True)
        labels = cl.fit_predict(coords)
        ht = time.time() - t1
        n_cl = len(set(labels.tolist()) - {-1})
        n_noise = int((labels == -1).sum())
        sizes = sorted(((labels[labels != -1] == k).sum()
                        for k in set(labels.tolist()) - {-1}), reverse=True)
        med = float(np.median(sizes)) if sizes else 0.0
        np.save(d / "umap_coords.npy", coords.astype(np.float32))
        np.save(d / "labels.npy", labels.astype(np.int64))
        np.save(d / "probabilities.npy", cl.probabilities_.astype(np.float32))
        cfg = {"experiment": name, "input_embeddings": str(EMB),
               "umap": {"n_components": ud, "n_neighbors": 30, "min_dist": 0.1,
                        "metric": "cosine", "random_state": 42},
               "hdbscan": {"min_cluster_size": 30, "min_samples": 10,
                           "cluster_selection_method": "eom", "metric": "euclidean"},
               "umap_seconds": round(ut, 1), "hdbscan_seconds": round(ht, 1)}
        (d / "config.json").write_text(json.dumps(cfg, indent=2))
        summ = {"experiment": name, "umap_dim": ud, "min_cluster_size": 30,
                "min_samples": 10, "n_clusters": n_cl, "n_noise": n_noise,
                "noise_pct": round(100 * n_noise / len(labels), 2),
                "largest": int(sizes[0]) if sizes else 0,
                "median_size": med,
                "umap_s": round(ut, 1), "hdbscan_s": round(ht, 1)}
        (d / "run_summary.json").write_text(json.dumps(summ, indent=2))
        rows.append({**summ, "note": "fresh run, same embeddings"})
        print(summ, flush=True)
    pd.DataFrame(rows).to_csv(OUT / "comparison.csv", index=False)
    print("wrote", OUT / "comparison.csv")

if __name__ == "__main__":
    main()
