"""Context-vs-solo classification experiment (Phase 3, TASK 17).

On the SAME held-out labelled rows that have a prior in-corpus customer turn,
compares A) message-only (existing embedding row) vs B) prev-turn + message
(freshly computed, same model, customer-side only). Trains LogReg once on
train-split solo features; evaluates both representations on the eligible
test rows. Reports accuracy/macro-F1 delta + per-row table.
AmazonHelp replies never enter either representation.
BLOCKED until golden_labels.csv + label_splits.csv exist.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from eval.classify import LogRegIntent, load_features

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"


def main() -> None:
    for req in ["golden_labels.csv", "label_splits.csv", "golden_candidates.csv"]:
        if not (EVAL / req).exists():
            print(f"BLOCKED: {req} missing — human labels pending.")
            raise SystemExit(2)
    splits = pd.read_csv(EVAL / "label_splits.csv", keep_default_na=False)
    cand = pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)
    lab = splits.merge(cand[["candidate_id", "embedding_index"]], on="candidate_id")
    meta = pd.read_csv(META, keep_default_na=False)
    prev = meta.sort_values(["conversation_id", "created_dt"]).groupby(
        "conversation_id")["embedding_input"].shift(1)
    meta = meta.assign(prev_input=prev.values)
    lab = lab.merge(meta[["customer_message_id", "embedding_input", "prev_input"]],
                    left_on="candidate_id", right_on="customer_message_id", how="left",
                    suffixes=("", "_m"))
    # candidate_id IS customer_message_id by construction; align anyway
    tr = lab[lab.split == "train"]
    te = lab[(lab.split == "test") & lab.prev_input.notna()].copy()
    print(f"train rows: {len(tr)} | test rows with prior turn: {len(te)}")
    if len(te) == 0:
        print("no eligible test rows; nothing to compare.")
        return
    clf = LogRegIntent().fit(load_features(tr.embedding_index.to_numpy()),
                             tr.intent_id.to_numpy())
    Xa = load_features(te.embedding_index.to_numpy())
    solo_pred = clf.classes_[clf.predict_proba(Xa).argmax(axis=1)]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    Xb = m.encode((te.prev_input + " [SEP] " + te.embedding_input).tolist(),
                  show_progress_bar=False, normalize_embeddings=True).astype(np.float32)
    ctx_pred = clf.classes_[clf.predict_proba(Xb).argmax(axis=1)]
    y = te.intent_id.to_numpy()
    rep = pd.DataFrame({
        "candidate_id": te.candidate_id, "true": y, "pred_solo": solo_pred,
        "pred_ctx": ctx_pred,
        "solo_ok": solo_pred == y, "ctx_ok": ctx_pred == y})
    rep.to_csv(EVAL / "context_experiment_rows.csv", index=False)
    print(f"solo: acc={accuracy_score(y, solo_pred):.4f} "
          f"macroF1={f1_score(y, solo_pred, average='macro', zero_division=0):.4f}")
    print(f"ctx : acc={accuracy_score(y, ctx_pred):.4f} "
          f"macroF1={f1_score(y, ctx_pred, average='macro', zero_division=0):.4f}")
    print(f"rows where ctx fixes solo: {int(((~rep.solo_ok) & rep.ctx_ok).sum())}, "
          f"breaks: {int((rep.solo_ok & (~rep.ctx_ok)).sum())}")


if __name__ == "__main__":
    main()
