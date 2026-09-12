"""Golden-candidate sampling (Phase 3, TASK 2+3).

Active-learning-style, 12-stratum coverage for maximum information per human
label. Uses ONLY existing artifacts (labels, probabilities, outliers,
centroids, taxonomy CSVs, prior sample files). NEVER assigns labels — the
`human_*` fields do not exist here; labels are collected separately by the
annotation tool.

Output: artifacts/evaluation/golden_candidates.csv + sampling_config.json
+ sampling_report.md
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
EMB = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
LABELS = ROOT / "artifacts/discovery/clustering/initial/labels.npy"
PROB = ROOT / "artifacts/discovery/clustering/initial/probabilities.npy"
OUTL = ROOT / "artifacts/discovery/clustering/initial/outlier_scores.npy"
INTERP = ROOT / "artifacts/discovery/taxonomy/cluster_interpretation.csv"
MERGE = ROOT / "artifacts/discovery/taxonomy/merge_candidates.csv"
CENT = ROOT / "artifacts/retrieval/provisional_centroids.npy"
CENT_MAP = ROOT / "artifacts/retrieval/provisional_centroids_map.json"
C7SAMPLE = ROOT / "artifacts/discovery/reclustering/cluster_7/c7_diverse_sample.csv"
N2SAMPLE = ROOT / "artifacts/discovery/reclustering/noise_v2/noise_v2_sample.csv"

SEED = 20240517
RISKY_RE = re.compile(r"\b(court|lawsuit|legal action|sue you|fraud|scam|police|"
                       r"hacked?|threat|kill|consumer forum|fir\b)", re.IGNORECASE)


def script_acc(t: str) -> bool:
    return bool(re.search(r"[àâäéèêëîïôöùûüÿçñßæœ¡¿]", t.lower()))


def main() -> None:
    rng = np.random.default_rng(SEED)
    EVAL.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, keep_default_na=False)
    L = np.load(LABELS); P = np.load(PROB); O = np.load(OUTL)
    assert len(meta) == len(L) == 93171
    interp = pd.read_csv(INTERP, keep_default_na=False)
    fam = dict(zip(interp.cluster_id.astype(int), interp.family_key))
    kind = dict(zip(interp.cluster_id.astype(int), interp.kind))
    size = dict(zip(interp.cluster_id.astype(int), interp.cluster_size.astype(int)))
    meta = meta.assign(cluster=L, prob=P, outlier=O,
                       family=[fam.get(int(c), "noise") if int(c) != -1 else "noise" for c in L],
                       kind=[kind.get(int(c), "noise") if int(c) != -1 else "noise" for c in L],
                       nchars=meta["text"].str.len())
    # uncertainty proxy: centroid similarity margin (lower = more uncertain)
    cents = np.load(CENT).astype(np.float64)
    cids = json.loads(CENT_MAP.read_text())["cluster_ids"]
    E = np.load(EMB, mmap_mode="r")
    Xn = np.asarray(E).astype(np.float64)
    Xn /= (np.linalg.norm(Xn, axis=1, keepdims=True) + 1e-12)
    S = Xn @ cents.T
    part = np.argpartition(-S, 2, axis=1)[:, :2]
    top2 = np.take_along_axis(S, part, axis=1)
    meta = meta.assign(margin=(top2[:, 0] - top2[:, 1]),
                       nearest_centroid=[cids[i] for i in part[:, 0]])
    meta = meta.reset_index(drop=False).rename(columns={"index": "embedding_index"})

    picked: dict = {}  # row_pos -> reason

    def take(mask, n: int, reason: str, order: Optional[str] = None):
        if n <= 0:
            return
        cand = meta[mask & ~meta.index.isin(picked.keys())]
        if order == "uncertain":
            cand = cand.sort_values(["margin", "outlier"], ascending=[True, False])
        elif order == "confident":
            cand = cand.sort_values(["prob"], ascending=False)
        elif order == "random":
            cand = cand.sample(frac=1.0, random_state=rng.integers(1 << 30))
        for i in cand.head(n).index:
            picked[i] = reason

    clustered = meta.cluster != -1
    # 1. common intents (60): top-12 families x (2 confident + 2 uncertain + 1 random)
    topfam = meta[clustered].groupby("family").size().sort_values(ascending=False).head(12).index
    for f in topfam:
        m = clustered & (meta.family == f)
        take(m, 2, "common_confident", "confident")
        take(m, 2, "common_boundary", "uncertain")
        take(m, 1, "common_random", "random")
    # 2. rare (16): clusters size<60 round-robin
    rare_clusters = [c for c, s in size.items() if s < 60]
    rng.shuffle(rare_clusters)
    for j in range(16):
        take(meta.cluster == rare_clusters[j % len(rare_clusters)], 1, "rare_cluster", "random")
    # 3. boundary (14): lowest prob clustered
    take(clustered, 14, "low_probability_boundary", "uncertain")
    # 4. merge (18): 2 per group from distinct members
    mc = pd.read_csv(MERGE, keep_default_na=False)
    for _, r in mc.iterrows():
        members = [int(x) for x in str(r["member_clusters"]).split(";")]
        for mem in list(rng.choice(members, size=min(2, len(members)), replace=False)):
            take(meta.cluster == int(mem), 1, f"merge_{r['group_id']}", "uncertain")
    # 5. split (24): 12 reuse C7 diverse sample + 12 across other split candidates
    c7 = pd.read_csv(C7SAMPLE, keep_default_na=False)
    for cid in c7.sample(min(12, len(c7)), random_state=SEED)["customer_message_id"]:
        hit = meta[meta.customer_message_id == cid]
        for i in hit.index:
            if i not in picked:
                picked[i] = "split_cluster7"
    for c in [59, 42, 122, 139, 143, 156, 184]:
        take(meta.cluster == c, 2 if c in (156, 139, 143) else 1,
             f"split_c{c}", "uncertain")
    # 6. noise (22): 14 reuse N2 + 8 fresh low-outlier noise (most cluster-like)
    n2 = pd.read_csv(N2SAMPLE, keep_default_na=False)
    for cid in n2.sample(min(14, len(n2)), random_state=SEED)["customer_message_id"]:
        hit = meta[meta.customer_message_id == cid]
        for i in hit.index:
            if i not in picked:
                picked[i] = "noise_diverse"
    nz = meta[~clustered].sort_values("outlier", ascending=True)
    take(~clustered, 8, "noise_near_cluster", None)
    # 7. contextual (10): artifact/contextual-kind template clusters
    take(clustered & meta.kind.isin(["artifact", "contextual"]), 10, "contextual_turn", "uncertain")
    # 8. short (10)
    take(meta.nchars < 60, 10, "short_message", "random")
    # 9. multilingual (12)
    acc = meta.text.map(script_acc)
    take(acc, 12, "multilingual", "random")
    # 10. OOD (8)
    take(clustered & (meta.kind == "ood"), 8, "ood_candidate", "random")
    # 11. safety-sensitive (8)
    take(meta.text.str.contains(RISKY_RE, na=False), 8, "safety_sensitive", "random")
    # 12. ordinary top-up to 204
    take(pd.Series(True, index=meta.index), 204 - len(picked), "ordinary_random", "random")

    rows = meta.loc[sorted(picked)].copy()
    out = pd.DataFrame({
        "candidate_id": [f"GC-{i + 1:03d}" for i in range(len(rows))],
        "source_episode_id": rows["customer_message_id"].values,
        "customer_message_id": rows["customer_message_id"].values,
        "conversation_id": rows["conversation_id"].values,
        "customer_text": rows["text"].values,
        "cluster_id": rows["cluster"].values,
        "cluster_family": rows["family"].values,
        "sampling_reason": [picked[i] for i in rows.index],
        "embedding_index": rows["embedding_index"].values,
        "cluster_probability": rows["prob"].round(4).values,
        "outlier_score": rows["outlier"].round(4).values,
        "centroid_margin": rows["margin"].round(4).values,
    })
    out.to_csv(EVAL / "golden_candidates.csv", index=False)
    cfg = {"seed": SEED, "target": 204, "produced": len(out),
           "strata": pd.Series(list(picked.values())).value_counts().to_dict(),
           "inputs": {"meta": str(META), "labels": str(LABELS),
                      "centroids": str(CENT), "c7sample": str(C7SAMPLE),
                      "n2sample": str(N2SAMPLE)},
           "note": "Candidates only. No labels assigned here."}
    (EVAL / "sampling_config.json").write_text(json.dumps(cfg, indent=2))
    with open(EVAL / "sampling_report.md", "w") as f:
        f.write("# Golden-candidate sampling report\n\n")
        f.write(f"Produced {len(out)} candidates (seed {SEED}).\n\n")
        f.write("## Stratum counts\n\n| reason | n |\n|---|---|\n")
        for k, v in cfg["strata"].items():
            f.write(f"| {k} | {v} |\n")
        f.write("\n## Method\n\n12-stratum active-learning-style coverage "
                "(common/confident+boundary+random, rare, low-probability, "
                "merge, split, noise, contextual, short, multilingual, OOD, "
                "safety, ordinary). Uncertainty proxy = centroid similarity "
                "margin. Dedup by row; label fields intentionally absent — "
                "labels are collected by the annotation tool into "
                "golden_labels.csv.\n")
    print(f"candidates: {len(out)}")
    print(pd.Series(list(picked.values())).value_counts().to_string())


if __name__ == "__main__":
    main()
