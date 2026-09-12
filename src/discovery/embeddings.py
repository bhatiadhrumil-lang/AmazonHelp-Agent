"""Embedding generation for customer problem episodes.

Given the audit's `customer_problem_episodes.csv`, this module:

1. Keeps ONLY rows with `episode_status == "KEEP"`.
2. Builds a controlled `embedding_input` from the customer message `text`
   (NEVER AmazonHelp's reply text / `brand_parent_text`).
3. Encodes with a configurable sentence-transformers backend.
4. Persists the embedding matrix as an `.npy` memmap plus a metadata sidecar
   that realigns every embedding row to its original episode record.

Resume-safety: batches are processed strictly in row order and `progress.json`
records how many rows are already embedded. Re-running skips completed rows.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from discovery.config import EmbeddingConfig, load_json, save_json

EMBEDDING_COL = "embedding_input"

# Columns copied into the metadata sidecar (lean; no AmazonHelp reply text).
META_COLS = [
    "customer_message_id",
    "conversation_id",
    "author_id",
    "created_dt",
    "text",
    "parent_id",
    "reply_gap_minutes",
    "has_url",
    "is_acknowledgment_like",
    "episode_status",
    EMBEDDING_COL,
]


def url_sha(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def build_embedding_input(text_series: pd.Series) -> pd.Series:
    """Controlled embedding representation of the customer problem.

    Documented transformation (see REPRODUCIBILITY.md):
    * HTML-unescape entities (the audit source contains ``&amp;`` etc.).
    * Strip a leading ``@AmazonHelp`` mention (systematic reply prefix).
    * Collapse and trim whitespace.
    The resulting string contains ONLY the customer's own message text.
    AmazonHelp replies, parent text, timestamps and downstream resolution
    information are NEVER included.
    """
    def _clean(x: str) -> str:
        if not isinstance(x, str):
            x = "" if pd.isna(x) else str(x)
        s = html.unescape(x)
        s = re.sub(r"^\s*@AmazonHelp\b", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    return text_series.map(_clean)


def load_episodes(path: Path, status: str = "KEEP") -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in ["customer_message_id", "text", "episode_status"] if c not in df.columns]
    if missing:
        raise ValueError(f"episodes CSV missing columns: {missing}")
    df = df[df.episode_status == status].copy()
    df = df.sort_values("customer_message_id").reset_index(drop=True)
    return df


def _load_backend(cfg: EmbeddingConfig):
    if cfg.backend == "sentence_transformers":
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(
            cfg.model,
            device=cfg.device,
        )
    raise ValueError(f"Unknown embedding backend: {cfg.backend!r}")


def ensure_embedding_matrix(path: Path, n: int, dim: int, dtype: np.dtype):
    from numpy.lib.format import open_memmap

    if path.exists():
        existing = np.load(path, mmap_mode="r")
        if existing.shape != (n, dim) or existing.dtype != dtype:
            raise ValueError(
                f"Existing {path} has shape {existing.shape} dtype {existing.dtype}; "
                f"expected {(n, dim)} {dtype}. Refusing to overwrite a mismatched matrix."
            )
        return open_memmap(str(path), mode="r+", dtype=dtype, shape=(n, dim))
    path.parent.mkdir(parents=True, exist_ok=True)
    return open_memmap(str(path), mode="w+", dtype=dtype, shape=(n, dim))


def generate_embeddings(
    episodes_csv: Path,
    out_dir: Path,
    cfg: EmbeddingConfig,
    limit: int | None = None,
    seed: int = 42,
):
    """Generate and persist embeddings for KEEP episodes. Resume-safe."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_episodes(episodes_csv)
    if limit is not None:
        df = df.head(limit).reset_index(drop=True)

    df[EMBEDDING_COL] = build_embedding_input(df["text"])

    n = len(df)
    dim = 384  # replaced below from the model itself
    dtype = np.float32 if cfg.dtype == "float32" else np.float64

    # Reject any empty embedding inputs up front so alignment never drifts.
    empties = df[EMBEDDING_COL].eq("")
    if empties.any():
        raise ValueError(f"{int(empties.sum())} KEEP episodes have empty embedding input")

    meta_path = out_dir / "embeddings_meta.csv"
    config_path = out_dir / "config.json"
    progress_path = out_dir / "progress.json"
    npy_path = out_dir / "embeddings.npy"

    # Metadata sidecar is written once, aligned to the same rows.
    df[META_COLS].to_csv(meta_path, index=False)

    backend = _load_backend(cfg)
    get_dim = getattr(backend, "get_embedding_dimension", None) or backend.get_sentence_embedding_dimension
    _dim = get_dim()
    if _dim:
        dim = _dim

    strict_dtype = np.dtype(dtype)
    arr = ensure_embedding_matrix(npy_path, n, dim, strict_dtype)

    progress = load_json(progress_path) if progress_path.exists() else {"completed": 0}
    completed = int(progress.get("completed", 0))
    if completed > n:
        raise ValueError(f"progress {completed} > rows {n}; inconsistent artifact state")
    if completed == n and n > 0:
        print(f"[embeddings] all {n} rows already embedded; nothing to do")
        return out_dir, df

    save_json(config_path, {"embedding": asdict_cfg(cfg), "seed": seed, "limit": limit,
                            "source": str(episodes_csv), "model_dim": dim})

    texts = df[EMBEDDING_COL].tolist()
    start = completed
    print(f"[embeddings] generating from row {start} to {n} (batch={cfg.batch_size}) on {cfg.device}")
    batches = list(range(start, n, cfg.batch_size))
    for idx, i in enumerate(tqdm(batches, desc="embedding")):
        j = min(i + cfg.batch_size, n)
        batch_texts = texts[i:j]
        vecs = backend.encode(
            batch_texts,
            batch_size=cfg.batch_size,
            normalize_embeddings=cfg.normalize,
            show_progress_bar=False,
        )
        if not np.isfinite(vecs).all():
            raise RuntimeError(f"non-finite embeddings in batch rows {i}:{j}")
        arr[i:j] = vecs.astype(dtype).reshape(j - i, dim)
        arr.flush()
        save_json(progress_path, {"completed": j})
        if idx % 50 == 0:
            print(f"[embeddings] {j:,}/{n:,} ({100*j/n:.1f}%)", flush=True)

    arr.flush()
    save_json(progress_path, {"completed": n})

    # Final validation.
    data = np.load(npy_path, mmap_mode="r")
    if data.shape != (n, dim):
        raise RuntimeError(f"saved embeddings shape {data.shape} != expected {(n, dim)}")
    if not np.isfinite(data[:]).all():
        raise RuntimeError("saved embeddings contain non-finite values")
    meta = pd.read_csv(meta_path)
    if len(meta) != n:
        raise RuntimeError(f"metadata rows {len(meta)} != embedding rows {n}")

    print(f"[embeddings] WROTE {n:,} x {dim} {dtype} -> {npy_path}")
    print(f"[embeddings] metadata -> {meta_path}")
    return out_dir, df


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("episodes_csv", type=Path)
    p.add_argument("--out", type=Path, default=Path("artifacts/discovery/embeddings/full"))
    p.add_argument("--model", default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--device", default="cpu")
    p.add_argument("--no-normalize", action="store_true")
    p.add_argument("--dtype", default="float32")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    cfg = EmbeddingConfig(
        model=args.model,
        batch_size=args.batch_size,
        device=args.device,
        normalize=not args.no_normalize,
        dtype=args.dtype,
    )
    t0 = time.time()
    generate_embeddings(args.episodes_csv, args.out, cfg, limit=args.limit, seed=args.seed)
    print(f"[embeddings] completed in {time.time() - t0:.1f}s")


def asdict_cfg(cfg: EmbeddingConfig) -> dict:
    from dataclasses import asdict

    return asdict(cfg)


if __name__ == "__main__":
    main()