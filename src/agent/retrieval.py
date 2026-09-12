"""Historical-case retrieval (Phase 2, TASK 4 + TASK 5).

Backend choice: sklearn NearestNeighbors, brute force, cosine distance over
L2-normalized vectors.

WHY (documented per TASK 5):
- 93,171 x 384 exact search is milliseconds-scale; no ANN approximation
  error to characterize or version-pin.
- Zero new dependencies (sklearn already required; FAISS is NOT installed
  and would add a heavy native dep for no measured need).
- The authoritative `embeddings.npy` memmap is REUSED in place — never
  copied or regenerated. The persisted index is a small sidecar
  (config + id row-map); row alignment is explicit, never positional trust.
- Query embedding uses the same sentence-transformers model as Phase 1B;
  the query represents the CUSTOMER problem only (AmazonHelp reply text is
  never embedded into the query).

Layout: artifacts/retrieval/<index_name>/{config.json,row_map.npy}
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from agent.cases import CaseStore

ROOT = Path(__file__).resolve().parent.parent.parent
EMB_NPY = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
EMB_META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
RETR_DIR = ROOT / "artifacts/retrieval"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


@dataclass
class RetrievalConfig:
    backend: str = "sklearn_brute_cosine"
    model: str = MODEL_NAME
    top_k: int = 5  # engineering default, NOT a validated optimum
    normalize: bool = True

    def to_dict(self):
        return {"backend": self.backend, "model": self.model,
                "top_k": self.top_k, "normalize": self.normalize}


@dataclass
class RetrievalHit:
    case: object  # HistoricalCase
    similarity: float  # cosine, -1..1


class Retriever:
    def __init__(self, store: CaseStore, matrix: np.ndarray,
                 row_ids: List[str], config: RetrievalConfig):
        assert matrix.shape[0] == len(row_ids) == len(store)
        self.store = store
        self.matrix = matrix.astype(np.float32)  # L2-normalized rows
        self.row_ids = row_ids
        self.config = config
        self._nn = NearestNeighbors(n_neighbors=min(50, len(row_ids)),
                                    metric="cosine", algorithm="brute")
        self._nn.fit(self.matrix)
        self._encoder = None

    @classmethod
    def build(cls, config: Optional[RetrievalConfig] = None) -> "Retriever":
        config = config or RetrievalConfig()
        store = CaseStore.load()
        meta = pd.read_csv(EMB_META, usecols=["customer_message_id"],
                           keep_default_na=False)
        row_ids = [str(c) for c in meta["customer_message_id"]]
        E = np.load(EMB_NPY, mmap_mode="r")
        assert E.shape == (len(row_ids), 384), E.shape
        M = np.asarray(E).astype(np.float64)
        M /= (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)
        assert np.isfinite(M).all()
        # Explicit permutation: matrix row i <-> store.cases[i] <-> row_ids[i].
        # Never assumes episode order == embedding order.
        order = {cid: i for i, cid in enumerate(row_ids)}
        perm = [order[c.customer_message_id] for c in store.cases]
        return cls(store, M[np.array(perm)], [c.customer_message_id for c in store.cases], config)

    def save(self, name: str = "main") -> Path:
        d = RETR_DIR / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "config.json").write_text(json.dumps(
            {**self.config.to_dict(), "n_cases": len(self.store),
             "dim": int(self.matrix.shape[1])}, indent=2))
        np.save(d / "row_map.npy", np.array(self.row_ids))
        return d

    def _encode(self, texts: List[str]) -> np.ndarray:
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer
            self._encoder = SentenceTransformer("sentence-transformers/" + MODEL_NAME)
        v = self._encoder.encode(texts, batch_size=64, show_progress_bar=False,
                                 normalize_embeddings=True)
        return np.asarray(v, dtype=np.float32)

    def search(self, query_text: str, top_k: Optional[int] = None) -> List[RetrievalHit]:
        if not (query_text or "").strip():
            return []
        k = top_k or self.config.top_k
        q = self._encode([query_text])
        dist, idx = self._nn.kneighbors(q, n_neighbors=min(k, len(self.row_ids)))
        return [RetrievalHit(case=self.store.cases[int(i)],
                             similarity=float(1.0 - float(dist[0][j])))
                for j, i in enumerate(idx[0])]
