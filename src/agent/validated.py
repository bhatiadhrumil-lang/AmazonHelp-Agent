"""Validated intent classifier (Phase 3, TASK 19).

Drop-in replacement for ProvisionalClusterAdapter behind the SAME
IntentClassifier interface — orchestrator code is untouched; only the
injected implementation changes:
    SupportAgent(retriever=..., intent=ValidatedClassifier())
Exposes intent_id, calibrated confidence, alternatives, margin/entropy
uncertainty, and model version. Raises FileNotFoundError with a clear
message if no trained final_model exists (i.e. human labels pending).
"""
from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from agent.contracts import ConversationContext, IntentAlternative, IntentPrediction
from agent.intent import IntentClassifier
from eval.classify import OodThresholds, apply_ood, load_features

ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = ROOT / "artifacts/evaluation/final_model"


class ValidatedClassifier(IntentClassifier):
    name = "validated-human-labels"

    def __init__(self, model_dir: Path = MODEL_DIR,
                 tau: OodThresholds | None = None):
        import json
        cfg = json.loads((model_dir / "model_config.json").read_text())
        self.cfg = cfg
        self.version = f"{cfg['model']}-seed{cfg['seed']}"
        self.classes_ = np.load(model_dir / "classes.npy", allow_pickle=True)
        if cfg["model"] == "knn":
            from eval.classify import KnnIntent
            self.inner = KnnIntent()
            self.inner.X_ = np.load(model_dir / "knn_matrix.npy")
            self.inner.y_ = np.load(model_dir / "knn_labels.npy")
            self.inner.classes_ = self.classes_
            self._proba = self.inner.predict_proba
        else:
            self.clf = joblib.load(model_dir / "sklearn_model.pkl")
            self._proba = self.clf.predict_proba
        E = __import__("numpy").load(
            ROOT / "artifacts/discovery/embeddings/full/embeddings.npy",
            mmap_mode="r")
        self._E = E
        self.tau = tau or OodThresholds()
        self._encoder = None

    def _encode(self, text: str) -> np.ndarray:
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer
            from agent.retrieval import MODEL_NAME
            self._encoder = SentenceTransformer("sentence-transformers/" + MODEL_NAME)
        v = self._encoder.encode([text], show_progress_bar=False,
                                 normalize_embeddings=True)
        return np.asarray(v, dtype=np.float32)

    def predict(self, context: ConversationContext) -> IntentPrediction:
        from agent.context import ContextBuilder
        text = ContextBuilder.intent_text(context)
        if not text.strip():
            return IntentPrediction(intent_id="unknown_empty", confidence=0.0,
                                    source=self.name, is_provisional=False,
                                    kind="", ood=True,
                                    explanation="empty message")
        q = self._encode(text)
        P = np.asarray(self._proba(q), dtype=np.float64)[0]
        o = np.argsort(-P)
        top, second = float(P[o[0]]), float(P[o[1]]) if len(P) > 1 else 0.0
        # train-distance for OOD (cosine distance to nearest fitted row)
        train_dist = 0.0
        if hasattr(self, "inner") and hasattr(self.inner, "X_"):
            Xn = self.inner.X_.astype(np.float64)
            train_dist = float(1.0 - (Xn @ q.astype(np.float64)[0]).max())
        from eval.classify import PredOut
        pred = PredOut(intent=str(self.classes_[o[0]]), top_p=top,
                       second_p=second, margin=top - second, entropy=float(
                           -(P[P > 0] * np.log(P[P > 0])).sum()),
                       alternatives=[])
        final = apply_ood(pred, train_dist, self.tau)
        return IntentPrediction(
            intent_id=final, confidence=top, kind="",
            alternatives=[IntentAlternative(intent_id=str(self.classes_[i]),
                                            confidence=float(P[i])) for i in o[1:4]],
            source=f"{self.name}:{self.version}", is_provisional=False,
            ood=(final == "unknown"),
            explanation=(f"validated {self.cfg['model']} on human labels "
                         f"({len(self.classes_)} intents); margin={pred.margin:.3f}, "
                         f"entropy={pred.entropy:.3f}"))
