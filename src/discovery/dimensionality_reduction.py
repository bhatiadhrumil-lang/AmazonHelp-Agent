"""UMAP dimensionality reduction on saved embeddings.

Operates ONLY on a persisted embedding artifact; embeddings are never
regenerated here. Supports multiple experiments without overwriting:
each run writes to its own output directory and records the exact
configuration plus a checksum of the input artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from discovery.config import UmapConfig, load_json, save_json


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while b := f.read(1 << 20):
            h.update(b)
    return h.hexdigest()


def load_embeddings(emb_path: Path):
    if not emb_path.exists():
        raise FileNotFoundError(f"embedding artifact not found: {emb_path}")
    return np.load(emb_path, mmap_mode="r")


def reduce_umap(
    emb_path: Path,
    out_dir: Path,
    cfg: UmapConfig,
    limit: int | None = None,
):
    out_dir.mkdir(parents=True, exist_ok=True)
    X = load_embeddings(emb_path)
    if limit is not None:
        X = X[:limit]
    n, d = X.shape

    import umap.umap_ as umap_

    reducer = umap_.UMAP(
        n_components=cfg.n_components,
        n_neighbors=cfg.n_neighbors,
        metric=cfg.metric,
        min_dist=cfg.min_dist,
        random_state=cfg.random_state,
        verbose=False,
    )
    print(f"[umap] fitting {n:,} x {d} -> {cfg.n_components}d "
          f"(n_neighbors={cfg.n_neighbors}, metric={cfg.metric}, min_dist={cfg.min_dist}, seed={cfg.random_state})")
    t0 = time.time()
    coords = reducer.fit_transform(X)
    print(f"[umap] fit in {time.time() - t0:.1f}s -> {coords.shape}")

    if not np.isfinite(coords).all():
        raise RuntimeError("UMAP produced non-finite coordinates")

    coords_path = out_dir / "umap_coords.npy"
    np.save(coords_path, coords.astype(np.float32))

    config = {
        "umap": {
            "n_components": cfg.n_components,
            "n_neighbors": cfg.n_neighbors,
            "metric": cfg.metric,
            "min_dist": cfg.min_dist,
            "random_state": cfg.random_state,
        },
        "input_embeddings": str(emb_path),
        "input_embeddings_sha256": sha256_of(emb_path),
        "input_embeddings_shape": [int(n), int(d)],
    }
    save_json(out_dir / "umap_config.json", config)
    print(f"[umap] WROTE {coords_path}")
    print(f"[umap] config -> {out_dir / 'umap_config.json'}")
    return coords_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("emb_path", type=Path, help="embeddings.npy artifact")
    p.add_argument("--out", type=Path, default=Path("artifacts/discovery/umap/experiment1"))
    p.add_argument("--n-components", type=int, default=8)
    p.add_argument("--n-neighbors", type=int, default=30)
    p.add_argument("--metric", default="cosine")
    p.add_argument("--min-dist", type=float, default=0.1)
    p.add_argument("--random-state", type=int, default=42)
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()

    cfg = UmapConfig(
        n_components=args.n_components,
        n_neighbors=args.n_neighbors,
        metric=args.metric,
        min_dist=args.min_dist,
        random_state=args.random_state,
    )
    reduce_umap(args.emb_path, args.out, cfg, limit=args.limit)


if __name__ == "__main__":
    main()