"""Final-model training (Phase 3). Trains the configured baseline on
train+val human labels with the FROZEN config, persists to
artifacts/evaluation/final_model/ for ValidatedClassifier. BLOCKED until
labels+splits exist. Test split is never read here.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from eval.classify import KnnIntent, LogRegIntent, MlpIntent, load_features

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["knn", "logreg", "mlp"], default="logreg")
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()
    for req in ["label_splits.csv", "golden_candidates.csv"]:
        if not (EVAL / req).exists():
            print(f"BLOCKED: {req} missing.");
            raise SystemExit(2)
    splits = pd.read_csv(EVAL / "label_splits.csv", keep_default_na=False)
    assert "test" in set(splits.split), "refusing to train without a held-out test split"
    cand = pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)
    lab = splits.merge(cand[["candidate_id", "embedding_index"]], on="candidate_id")
    fit = lab[lab.split.isin(["train", "val"])]
    X = load_features(fit.embedding_index.to_numpy())
    y = fit.intent_id.to_numpy()
    model = {"knn": KnnIntent(), "logreg": LogRegIntent(seed=args.seed),
             "mlp": MlpIntent(seed=args.seed)}[args.model]
    model.fit(X, y)
    d = EVAL / "final_model"
    d.mkdir(parents=True, exist_ok=True)
    if args.model == "knn":
        np.save(d / "knn_matrix.npy", model.X_)
        np.save(d / "knn_labels.npy", model.y_)
        np.save(d / "classes.npy", model.classes_)
    else:
        joblib.dump(model.clf, d / "sklearn_model.pkl")
        np.save(d / "classes.npy", model.classes_)
    (d / "model_config.json").write_text(json.dumps(
        {"model": args.model, "seed": args.seed, "n_fit": len(fit),
         "classes": sorted(set(y.tolist())), "features": "frozen-384d",
         "note": "fit on train+val only; test untouched"}, indent=2))
    print(f"saved final_model ({args.model}, n={len(fit)})")


if __name__ == "__main__":
    main()
