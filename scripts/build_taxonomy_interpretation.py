"""Builds Phase 1C taxonomy interpretation artifacts.

Reads:
  - artifacts/discovery/taxonomy/_digest/cluster_digest.csv  (signal table)
  - scripts/cluster_interpretation_data.py                   (per-cluster reading)

Writes:
  - artifacts/discovery/taxonomy/cluster_interpretation.csv
  - artifacts/discovery/taxonomy/merge_candidates.csv
  - artifacts/discovery/taxonomy/split_candidates.csv

Every non-noise cluster 0-202 is assigned a preliminary family label, a
customer goal, confidence, coherence and a parent intent. Families
implemented as conversation artifacts are NOT treated as intents.
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cluster_interpretation_data import (  # noqa: E402
    CLUSTERS,
    FAMILIES,
    MERGE_GROUPS,
    SPLIT_CANDIDATES,
)

ROOT = Path(__file__).resolve().parent.parent
DIGEST_CSV = ROOT / "artifacts/discovery/taxonomy/_digest/cluster_digest.csv"
OUT_DIR = ROOT / "artifacts/discovery/taxonomy"


def main() -> None:
    digest = pd.read_csv(DIGEST_CSV, keep_default_na=False)
    digest = digest.sort_values("cluster_id").reset_index(drop=True)

    missing = sorted(set(digest["cluster_id"]) - set(CLUSTERS))
    if missing:
        raise SystemExit(f"ERROR: no interpretation record for clusters {missing}")

    rows = []
    for _, d in digest.iterrows():
        cid = int(d["cluster_id"])
        family_key, overrides = CLUSTERS[cid]
        fam = dict(FAMILIES[family_key])
        fam.update(overrides)
        rows.append({
            "cluster_id": cid,
            "cluster_size": int(d["size"]),
            "preliminary_label": fam["label"],
            "customer_goal": fam["goal"],
            "confidence": fam["conf"],
            "coherent": fam["coherent"],
            "possible_parent_intent": fam["parent"],
            "kind": fam["kind"],
            "family_key": family_key,
            "exact_dup_share": round(float(d["exact_dup_share"]), 3),
            "median_member_chars": float(d["median_member_chars"]),
            "url_share": round(float(d["url_share"]), 3),
            "multilingual_flag": d["multilingual_flag"],
            "merge_candidates": _merge_names(cid),
            "split_candidates": _split_names(cid),
            "reasoning": _reasoning(fam, d),
            "representative_examples": _examples(cid),
        })

    out = pd.DataFrame(rows).sort_values("cluster_id")
    out.to_csv(OUT_DIR / "cluster_interpretation.csv", index=False,
               encoding="utf-8", quoting=csv.QUOTE_MINIMAL)

    merge_rows = []
    for g in MERGE_GROUPS:
        sizes = digest[digest["cluster_id"].isin(g["member_clusters"])]["size"]
        merge_rows.append({
            "group_id": g["group_id"],
            "candidate_label": g["candidate_label"],
            "member_clusters": ";".join(str(c) for c in g["member_clusters"]),
            "n_clusters": len(g["member_clusters"]),
            "combined_size": int(sizes.sum()),
            "rationale": g["rationale"],
            "evidence": g["evidence"],
            "confidence": g["confidence"],
            "status": "proposed",
        })
    pd.DataFrame(merge_rows).to_csv(OUT_DIR / "merge_candidates.csv",
                                    index=False, encoding="utf-8")

    split_rows = []
    for s in SPLIT_CANDIDATES:
        size = digest.loc[digest["cluster_id"] == s["cluster_id"], "size"].iloc[0]
        split_rows.append({
            "cluster_id": s["cluster_id"],
            "size": int(size),
            "split_rationale": s["split_rationale"],
            "evidence": s["evidence"],
            "sub_themes_observed": s["sub_themes_observed"],
            "confidence": s["confidence"],
            "status": "proposed",
        })
    pd.DataFrame(split_rows).to_csv(OUT_DIR / "split_candidates.csv",
                                    index=False, encoding="utf-8")

    total = digest["size"].sum()
    clustered = out["cluster_size"].sum()
    print(f"cluster_interpretation.csv: {len(out)} rows | clustered points {clustered} / {total} (noise {total - clustered})")
    print(f"merge_candidates.csv: {len(merge_rows)} groups")
    print(f"split_candidates.csv: {len(split_rows)} clusters")


def _merge_names(cid: int) -> str:
    names = [g["group_id"] for g in MERGE_GROUPS if cid in g["member_clusters"]]
    return ";".join(names) if names else ""


def _split_names(cid: int) -> str:
    names = [str(s["cluster_id"]) for s in SPLIT_CANDIDATES if s["cluster_id"] == cid]
    return ";".join(names) if names else ""


def _reasoning(fam: dict, d) -> str:
    base = (f"{fam['conf'].capitalize()} confidence. "
            f"Family: {fam['label']}. Signials: "
            f"size={d['size']}, dup={d['exact_dup_share']}, "
            f"url_share={d['url_share']}.")
    return base


def _examples(cid: int) -> str:
    reps = pd.read_csv(ROOT / "artifacts/discovery/clustering/initial"
                       / f"cluster_{cid}_representatives.csv", keep_default_na=False)
    texts = reps["text"].astype(str).str.replace("\n", " ").str.replace("|", "/").tolist()
    return " ;; ".join(t[:160] for t in texts[:3])


if __name__ == "__main__":
    main()