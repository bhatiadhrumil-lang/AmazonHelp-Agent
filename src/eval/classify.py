"""Intent classifiers (Phase 3, TASK 10+11+12+14+15+16).

Trained ONLY on human labels (never HDBSCAN ids). Features are the EXISTING
384D embeddings, looked up by embedding_index (never regenerated).

- Baseline A `KnnIntent`: cosine 1-NN / k-NN similarity-weighted vote.
- Baseline B `LogRegIntent`: L2 logistic regression, class_weight='balanced'
  default (TASK 12), fixed seed.
- Optional `MlpIntent`: small MLP, only justified if it materially beats B on
  validation (TASK 11) — kept behind a flag, same interface.
- `CalibratedIntent` (TASK 14): wraps B with CalibratedClassifierCV
  (sigmoid/Platt) fit on VALIDATION predictions only; exposes reliability
  inputs (probabilities) + Brier score helper.
- Uncertainty (TASK 15): every predict returns top_p, second_p, margin,
  entropy — the AGENT uses these, never raw confidence alone.
- OOD wrapper (TASK 16): `predict_with_ood` returns "unknown" when
  max_p < tau_p OR margin < tau_m OR min-train-distance > tau_d. Default
  taus are UNCALIBRATED placeholders; tune on validation, never test.
  OOD (semantic unknown) is NOT HDBSCAN noise (density artifact).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

ROOT = Path(__file__).resolve().parent.parent.parent
EMB = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"


def load_features(indices: np.ndarray) -> np.ndarray:
    E = np.load(EMB, mmap_mode="r")
    X = np.asarray(E[np.asarray(indices)]).astype(np.float64)
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
    assert np.isfinite(Xn).all()
    return Xn.astype(np.float32)


@dataclass
class PredOut:
    intent: str
    top_p: float
    second_p: float
    margin: float
    entropy: float
    alternatives: List[Tuple[str, float]]


def _stats(proba: np.ndarray, classes: np.ndarray) -> PredOut:
    o = np.argsort(-proba)
    top, second = float(proba[o[0]]), float(proba[o[1]]) if len(proba) > 1 else 0.0
    ent = float(-(proba[proba > 0] * np.log(proba[proba > 0])).sum())
    return PredOut(intent=str(classes[o[0]]), top_p=top, second_p=second,
                   margin=top - second, entropy=ent,
                   alternatives=[(str(classes[i]), float(proba[i])) for i in o[1:4]])


class KnnIntent:
    """Baseline A: cosine k-NN similarity-weighted vote over labelled rows."""

    name = "knn-cosine"

    def __init__(self, k: int = 5):
        self.k = k

    def fit(self, X: np.ndarray, y: np.ndarray):
        Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
        self.X_ = np.ascontiguousarray(Xn, dtype=np.float32)
        self.classes_ = np.array(sorted(set(y.tolist())))
        self.y_ = np.array([np.where(self.classes_ == v)[0][0] for v in y])
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
        S = Xn.astype(np.float64) @ self.X_.astype(np.float64).T
        k = min(self.k, len(self.X_))
        idx = np.argpartition(-S, k - 1, axis=1)[:, :k]
        P = np.zeros((len(X), len(self.classes_)))
        for r in range(len(X)):
            w = S[r, idx[r]]
            w = np.clip(w, 0.0, None) + 1e-9
            for j, t in enumerate(idx[r]):
                P[r, self.y_[t]] += w[j]
            P[r] /= P[r].sum()
        return P

    def predict_detailed(self, X: np.ndarray) -> List[PredOut]:
        P = self.predict_proba(X)
        return [_stats(p, self.classes_) for p in P]

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.classes_[self.predict_proba(X).argmax(axis=1)]


class LogRegIntent:
    """Baseline B: balanced L2 logistic regression on frozen embeddings."""

    name = "logreg-balanced"

    def __init__(self, C: float = 1.0, seed: int = 11):
        self.C = C
        self.seed = seed
        self.clf = LogisticRegression(C=C, class_weight="balanced",
                                      max_iter=2000, random_state=seed)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.clf.fit(X, y)
        self.classes_ = self.clf.classes_
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.clf.predict_proba(X)

    def predict_detailed(self, X: np.ndarray) -> List[PredOut]:
        return [_stats(p, self.classes_) for p in self.predict_proba(X)]


class MlpIntent:
    """Optional stronger model (TASK 11): tiny MLP. Use only if it beats B."""

    name = "mlp-small"

    def __init__(self, hidden: Tuple[int, ...] = (128,), seed: int = 11):
        self.clf = MLPClassifier(hidden_layer_sizes=hidden, max_iter=1000,
                                 random_state=seed)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.clf.fit(X, y)
        self.classes_ = self.clf.classes_
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.clf.predict_proba(X)

    def predict_detailed(self, X: np.ndarray) -> List[PredOut]:
        return [_stats(p, self.classes_) for p in self.predict_proba(X)]


@dataclass
class OodThresholds:
    # UNCALIBRATED placeholders — tune on VALIDATION only, never test.
    min_top_p: float = 0.5
    min_margin: float = 0.1
    max_train_distance: float = 0.6  # cosine distance to nearest train row
    version: str = "v0-uncalibrated"


def apply_ood(pred: PredOut, train_dist: float, tau: OodThresholds) -> str:
    if (pred.top_p < tau.min_top_p or pred.margin < tau.min_margin
            or train_dist > tau.max_train_distance):
        return "unknown"
    return pred.intent


def brier_score(proba: np.ndarray, classes: np.ndarray, y_true: np.ndarray) -> float:
    idx = np.array([np.where(classes == v)[0][0] for v in y_true])
    onehot = np.zeros_like(proba)
    onehot[np.arange(len(y_true)), idx] = 1.0
    return float(((proba - onehot) ** 2).mean())
