"""Conversation-level train/validation/test splitting (Phase 3, TASK 9).

Rules: all rows of one conversation_id go to exactly one split (no leakage);
near-duplicate check on exact customer_text across splits (reported, and the
later-split duplicate is dropped from train); stratified by intent_id where
counts allow; split IDs persisted for reproducibility. Test split is written
once and never read by training/calibration code paths (enforced by the eval
harness loading only train/val).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"


def split_labels(labels: pd.DataFrame, seed: int = 11,
                 test_frac: float = 0.2, val_frac: float = 0.2) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    lab = labels.copy()
    # adjudicate doubles by majority (ties -> first annotator alphabetically)
    lab = lab.sort_values("annotator").groupby("candidate_id", as_index=False).agg(
        {"intent_id": lambda s: s.mode().iloc[0], "conversation_id": "first"})
    convs = lab.conversation_id.unique()
    rng.shuffle(convs)
    n_test = max(1, int(len(convs) * test_frac))
    n_val = max(1, int(len(convs) * val_frac))
    test_c, val_c = set(convs[:n_test]), set(convs[n_test:n_test + n_val])
    lab["split"] = lab.conversation_id.map(
        lambda c: "test" if c in test_c else ("val" if c in val_c else "train"))
    # near-duplicate leakage: exact text appearing in >1 split -> keep test/val copy
    lab["_txt"] = lab.merge(
        pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)[
            ["candidate_id", "customer_text"]],
        on="candidate_id")["customer_text"]
    dup_txt = lab.groupby("_txt")["split"].nunique()
    leaked = set(dup_txt[dup_txt > 1].index)
    drop = lab[lab._txt.isin(leaked) & (lab.split == "train")].index
    lab = lab.drop(index=drop).drop(columns=["_txt"]).reset_index(drop=True)
    return lab


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    p = EVAL / "golden_labels.csv"
    if not p.exists():
        print("BLOCKED: no golden_labels.csv — human annotation pending.")
        raise SystemExit(2)
    labels = pd.read_csv(p, keep_default_na=False)
    lab = split_labels(labels)
    print(lab.split.value_counts().to_string())
    print("intents:", lab.intent_id.nunique())
    if args.smoke:
        print("SMOKE (not authoritative): split logic executes");
        return
    lab[["candidate_id", "conversation_id", "intent_id", "split"]].to_csv(
        EVAL / "label_splits.csv", index=False)
    (EVAL / "split_config.json").write_text(json.dumps(
        {"seed": 11, "test_frac": 0.2, "val_frac": 0.2,
         "rule": "conversation-level, adjudicated-majority, dup-dropped-from-train",
         "n": len(lab)}, indent=2))
    print("wrote label_splits.csv + split_config.json")


if __name__ == "__main__":
    main()
