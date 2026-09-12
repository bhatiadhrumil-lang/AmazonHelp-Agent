"""Provisional intent adapter (Phase 2, TASK 7) — PROVISIONAL, not validated.

Interface `IntentClassifier.predict(context) -> IntentPrediction` is stable;
this implementation (nearest family centroid in 384D customer-embedding
space) can be replaced without touching the agent. Taxonomy labels are loaded
from `cluster_interpretation.csv` at runtime — never hard-coded.

Method: cosine of the query embedding to each HDBSCAN cluster centroid
(mean of member 384D embeddings, L2-normalized); the winning cluster's
family_key becomes the intent; next-best distinct families become
alternatives. Confidence is raw cosine similarity: UNCALIBRATED, never a
production threshold.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from agent.contracts import ConversationContext, IntentAlternative, IntentPrediction

ROOT = Path(__file__).resolve().parent.parent.parent
EMB_NPY = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
LABELS = ROOT / "artifacts/discovery/clustering/initial/labels.npy"
INTERP = ROOT / "artifacts/discovery/taxonomy/cluster_interpretation.csv"
CENT_DIR = ROOT / "artifacts/retrieval"


class IntentClassifier:
    """Stable interface. Replace the implementation, not the callers."""

    name: str = "base"

    def predict(self, context: ConversationContext) -> IntentPrediction:
        raise NotImplementedError


class ProvisionalClusterAdapter(IntentClassifier):
    """PROVISIONAL nearest-centroid adapter over the Phase 1B clustering."""

    name = "provisional-centroid-384d"

    def __init__(self):
        interp = pd.read_csv(INTERP, keep_default_na=False)
        self.family_of: Dict[int, str] = dict(
            zip(interp["cluster_id"].astype(int), interp["family_key"]))
        self.kind_of: Dict[int, str] = dict(
            zip(interp["cluster_id"].astype(int), interp["kind"]))
        cent_path = CENT_DIR / "provisional_centroids.npy"
        map_path = CENT_DIR / "provisional_centroids_map.json"
        if cent_path.exists() and map_path.exists():
            self.centroids = np.load(cent_path)
            self.cluster_ids = json.loads(map_path.read_text())["cluster_ids"]
        else:
            E = np.load(EMB_NPY, mmap_mode="r")
            L = np.load(LABELS)
            ids, vecs = [], []
            for k in sorted(set(L.tolist()) - {-1}):
                v = np.asarray(E[L == k]).astype(np.float64).mean(axis=0)
                v /= (np.linalg.norm(v) + 1e-12)
                ids.append(int(k))
                vecs.append(v)
            self.centroids = np.stack(vecs).astype(np.float32)
            self.cluster_ids = ids
            np.save(cent_path, self.centroids)
            map_path.write_text(json.dumps({"cluster_ids": ids}))
        self._encoder = None

    def _encode(self, text: str) -> np.ndarray:
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer
            from agent.retrieval import MODEL_NAME
            self._encoder = SentenceTransformer("sentence-transformers/" + MODEL_NAME)
        v = self._encoder.encode([text], show_progress_bar=False,
                                 normalize_embeddings=True)
        return np.asarray(v, dtype=np.float32)[0]

    def predict(self, context: ConversationContext) -> IntentPrediction:
        text = context.current_message.text or ""
        if not text.strip():
            return IntentPrediction(intent_id="unknown_empty", confidence=0.0,
                                    source=self.name, is_provisional=True,
                                    explanation="empty message; no intent attempted")
        q = self._encode(text).astype(np.float64)
        sims = self.centroids.astype(np.float64) @ q
        order = np.argsort(-sims)
        best = int(self.cluster_ids[int(order[0])])
        fam = self.family_of[best]
        alts, seen = [], {fam}
        for o in order[1:]:
            f = self.family_of[int(self.cluster_ids[int(o)])]
            if f not in seen:
                seen.add(f)
                alts.append(IntentAlternative(
                    intent_id=f, confidence=float(sims[int(o)])))
            if len(alts) == 3:
                break
        return IntentPrediction(
            intent_id=fam, confidence=float(sims[int(order[0])]),
            alternatives=alts, source=self.name, is_provisional=True,
            kind=self.kind_of[best],
            explanation=(f"nearest of 203 cluster centroids: cluster {best} "
                         f"(kind={self.kind_of[best]}); similarity is uncalibrated"))
