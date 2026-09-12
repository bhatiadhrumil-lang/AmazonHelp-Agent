"""Reproducible intent evaluation harness (Phase 3, TASK 13+14+22).

`PYTHONPATH=src .venv/bin/python -m eval.run_intent_eval --model logreg`
Loads FROZEN label_splits.csv (train/val only for fitting+calibration;
test read exactly once at report time), trains the named baseline, applies
sigmoid calibration on validation, evaluates on the held-out test set, and
persists machine-readable metrics + human-readable report + confusion matrix
+ per-intent table + reliability data + config metadata under
artifacts/evaluation/eval_<model>_<timestamp>/.

Needs no 2.8M-row data: only embeddings.npy rows + label CSVs.
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_recall_fscore_support)

from eval.classify import (KnnIntent, LogRegIntent, MlpIntent, apply_ood,
                           brier_score, load_features, OodThresholds)

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_DEFAULT = ROOT / "artifacts/evaluation"


def reliability(proba: np.ndarray, y_true: np.ndarray, classes: np.ndarray,
                n_bins: int = 10) -> list:
    idx = np.array([np.where(classes == v)[0][0] for v in y_true])
    conf = proba.max(axis=1)
    correct = (proba.argmax(axis=1) == idx)
    edges = np.linspace(0, 1, n_bins + 1)
    out = []
    for b in range(n_bins):
        m = (conf > edges[b]) & (conf <= edges[b + 1])
        if m.sum():
            out.append({"bin": [round(float(edges[b]), 2), round(float(edges[b + 1]), 2)],
                        "n": int(m.sum()),
                        "mean_conf": round(float(conf[m].mean()), 4),
                        "accuracy": round(float(correct[m].mean()), 4)})
    return out


def ece(rel: list) -> float:
    n = sum(b["n"] for b in rel)
    return round(sum(b["n"] / n * abs(b["mean_conf"] - b["accuracy"]) for b in rel), 4) if n else 0.0


def main(eval_dir=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["knn", "logreg", "mlp"], default="logreg")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--eval-dir", default=None,
                    help="override eval dir (pipeline smoke tests only)")
    args = ap.parse_args()
    EVAL = Path(args.eval_dir) if args.eval_dir or eval_dir else EVAL_DEFAULT
    for req in ["golden_labels.csv", "label_splits.csv"]:
        if not (EVAL / req).exists():
            print(f"BLOCKED: {req} missing — human labels/splits pending.")
            raise SystemExit(2)
    splits = pd.read_csv(EVAL / "label_splits.csv", keep_default_na=False)
    cand = pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)
    lab = splits.merge(cand[["candidate_id", "embedding_index"]], on="candidate_id")
    tr, va, te = (lab[lab.split == s] for s in ("train", "val", "test"))
    Xtr, ytr = load_features(tr.embedding_index.to_numpy()), tr.intent_id.to_numpy()
    Xva, yva = load_features(va.embedding_index.to_numpy()), va.intent_id.to_numpy()
    Xte, yte = load_features(te.embedding_index.to_numpy()), te.intent_id.to_numpy()
    base = {"knn": KnnIntent(), "logreg": LogRegIntent(seed=args.seed),
            "mlp": MlpIntent(seed=args.seed)}[args.model]
    base.fit(Xtr, ytr)
    # calibration on VALIDATION only (Platt/sigmoid). FrozenEstimator wraps the
    # already-fitted model so CV calibrates without refitting the base model.
    from sklearn.frozen import FrozenEstimator
    if args.model == "knn":
        from sklearn.base import BaseEstimator, ClassifierMixin

        class KNNWrap(ClassifierMixin, BaseEstimator):
            def __init__(self, inner): self.inner = inner
            def fit(self, X, y):
                self.classes_ = self.inner.classes_
                return self
            def predict(self, X): return self.inner.predict(X)
            def predict_proba(self, X): return self.inner.predict_proba(X)
        frozen = FrozenEstimator(KNNWrap(base).fit(Xva, yva))
    else:
        frozen = FrozenEstimator(base.clf)
    cal = CalibratedClassifierCV(frozen, method="sigmoid", cv=2)
    cal.fit(Xva, yva)
    Pte = cal.predict_proba(Xte)
    pred = cal.classes_[Pte.argmax(axis=1)]
    prec, rec, f1, sup = precision_recall_fscore_support(yte, pred, zero_division=0)
    rel = reliability(Pte, yte, cal.classes_)
    per = pd.DataFrame({"intent": cal.classes_, "precision": prec.round(4),
                        "recall": rec.round(4), "f1": f1.round(4), "support": sup})
    metrics = {
        "model": args.model, "seed": args.seed,
        "n_train": len(tr), "n_val": len(va), "n_test": len(te),
        "accuracy": round(float(accuracy_score(yte, pred)), 4),
        "macro_f1": round(float(f1_score(yte, pred, average="macro", zero_division=0)), 4),
        "weighted_f1": round(float(f1_score(yte, pred, average="weighted", zero_division=0)), 4),
        "brier": brier_score(Pte, cal.classes_, yte),
        "ece_10bin": ece(rel),
        "classes": cal.classes_.tolist(),
    }
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = EVAL / f"eval_{args.model}_{ts}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    per.to_csv(out / "per_intent.csv", index=False)
    pd.DataFrame(confusion_matrix(yte, pred), index=cal.classes_,
                 columns=cal.classes_).to_csv(out / "confusion_matrix.csv")
    (out / "reliability.json").write_text(json.dumps(rel, indent=2))
    (out / "config.json").write_text(json.dumps(
        {"model": args.model, "seed": args.seed, "calibration": "sigmoid_prefit_on_val",
         "splits": "label_splits.csv (frozen)", "test_touched_once": True}, indent=2))
    with open(out / "report.md", "w") as f:
        f.write(f"# Intent eval: {args.model}\n\n")
        for k, v in metrics.items():
            f.write(f"- {k}: {v}\n")
        f.write("\nMacro F1 is the headline metric (support task, imbalanced).\n")
    print(json.dumps(metrics, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
