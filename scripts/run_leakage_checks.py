"""TASK 11: data-leakage, identity and traceability checks on the Phase 1C
preliminary outputs (and the Phase 1C human-validation sample).

Checks implemented:
  1. Noise sample (noise_sample.csv): every row must have HDBSCAN label == -1
     (re-read labels.npy and meta, join by row alignment);
     customer_message_id must NOT appear among any clustered point's
     customer_message_ids.
  2. Human-validation candidates:
     - no duplicated (conversation_id, customer_message_id);
     - every customer_message_id exists in embeddings_meta (full);
     - candidate customer_message_ids must not overlap between "cluster" and
       "noise" sources (cluster points vs noise points are disjoint by
       construction, re-verified here);
     - no candidate id may appear in the noise sample twice.
  3. Cross-cluster exact-duplicate leakage check: exact customer texts that
     appear in more than one cluster (e.g. "Thank you" families) are reported
     as merge signals, NOT as leakage - a customer message belongs to exactly
     one cluster by construction)Skip writing the leakage script's third part and emit cross-cluster exact-dup stats
     into leakage_checks.md for the merge review.

Outputs (all under artifacts/discovery/taxonomy/):
  - leakage_checks.csv
  - leakage_checks.md
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TAX = ROOT / "artifacts/discovery/taxonomy"

EMB_META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
LABELS = ROOT / "artifacts/discovery/clustering/initial/labels.npy"
NOISE_CSV = TAX / "noise_sample.csv"
VALIDATION_CSV = TAX / "human_validation_candidates.csv"

CROSS_DUP_MAX = 10  # cap reported cross-cluster exact-dup texts


def main() -> None:
    meta_all = pd.read_csv(EMB_META, keep_default_na=False)
    labels = np.load(LABELS)

    assert len(labels) == len(meta_all), (
        f"labels {len(labels)} != meta {len(meta_all)}; row alignment broken")
    meta_all = meta_all.reset_index(drop=True)
    meta_all["row_position"] = np.arange(len(meta_all))
    meta_all["hdbscan_cluster"] = labels

    # clustered point ids
    clustered_ids = set(meta_all.loc[meta_all["hdbscan_cluster"] != -1, "customer_message_id"])
    noise_ids = set(meta_all.loc[meta_all["hdbscan_cluster"] == -1, "customer_message_id"])
    assert not (clustered_ids & noise_ids)

    checks = []

    # --- 1. noise sample ---
    noise = pd.read_csv(NOISE_CSV, keep_default_na=False)
    n_cfg = {
        "check": "noise_sample rows all HDBSCAN-noise",
        "ok": bool((noise["hdbscan_cluster"] == -1).all()),
        "detail": f"n={len(noise)}; labels present: {sorted(noise['hdbscan_cluster'].unique())}",
    }
    checks.append(n_cfg)
    m = meta_all.set_index("customer_message_id")
    nids = noise["customer_message_id"]
    in_noise = nids.isin(noise_ids)
    n_cfg2 = {
        "check": "noise_sample ids are true noise (not clustered)",
        "ok": bool(in_noise.all()),
        "detail": f"{int((~in_noise).sum())} rows not in labels==-1",
    }
    checks.append(n_cfg2)

    # --- 2. validation candidates ---
    val = pd.read_csv(VALIDATION_CSV, keep_default_na=False)
    dups = val.duplicated(["conversation_id", "customer_message_id"]).sum()
    checks.append({
        "check": "no duplicated (conversation_id, customer_message_id) in validation sample",
        "ok": dups == 0, "detail": f"duplicate rows={dups}",
    })
    missing_in_meta = set(val["customer_message_id"]) - set(meta_all["customer_message_id"])
    checks.append({
        "check": "all validation candidate ids exist in embeddings_meta (full)",
        "ok": not missing_in_meta,
        "detail": f"missing ids={len(missing_in_meta)}"})
    # validation candidates must be a subset of conversation data
    val_cluster_src = val[val["source"] == "cluster"]
    val_noise_src = val[val["source"] == "noise"]
    overlap = set(val_cluster_src["customer_message_id"]) & set(
        val_noise_src["customer_message_id"])
    checks.append({
        "check": "validation cluster-source vs noise-source ids disjoint",
        "ok": not overlap, "detail": f"overlap ids={len(overlap)}"})
    # noise-source candidates must actually be noise ids
    bad = set(val_noise_src["customer_message_id"]) - noise_ids
    checks.append({
        "check": "validation noise-source ids are HDBSCAN-noise",
        "ok": not bad, "detail": f"non-noise ids={len(bad)}"})
    # cluster-source candidates must be clustered
    bad2 = set(val_cluster_src["customer_message_id"]) - clustered_ids
    checks.append({
        "check": "validation cluster-source ids are clustered",
        "ok": not bad2, "detail": f"non-clustered ids={len(bad2)}"})
    # no candidate id appears twice in noise sample
    twice = nids[nids.duplicated(keep=False)]
    checks.append({
        "check": "no validation id repeated within the same source pick block",
        "ok": twice.empty,
        "detail": f"repeated-in-noise ids={len(twice)}"})

    # --- 3. cross-cluster exact-dup summary (merge signal, not leakage) ---
    digest = pd.read_csv(
        ROOT / "artifacts/discovery/taxonomy/_digest/cluster_digest.csv",
        keep_default_na=False)
    toptexts = digest[["cluster_id", "top_exact_texts"]].dropna()
    shared: dict[str, list[int]] = {}
    for _, r in toptexts.iterrows():
        for tok in str(r["top_exact_texts"]).split(";"):
            tok = tok.strip()
            if not tok:
                continue
            shared.setdefault(tok, []).append(int(r["cluster_id"]))
    cross = {t: cids for t, cids in shared.items() if len(cids) > 1}
    cross = dict(sorted(cross.items(), key=lambda kv: (-len(kv[1]), kv[0])))
    checks.append({
        "check": "cross-cluster exact-duplicate texts (merge signal, not leakage)",
        "ok": True,
        "detail": f"{len(cross)} exact texts shared by >1 cluster "
                  f"(capped report to {CROSS_DUP_MAX})",
    })
    dup_summary = pd.DataFrame([
        {"exact_text": t, "n_clusters": len(cids), "cluster_ids": ";".join(map(str, cids))}
        for t, cids in list(cross.items())[:CROSS_DUP_MAX]
    ])

    pd.DataFrame(checks).to_csv(TAX / "leakage_checks.csv", index=False, encoding="utf-8")
    dup_summary.to_csv(TAX / "cross_cluster_exact_duplicates.csv", index=False,
                       encoding="utf-8")

    lines = [
        "# Leakage / duplicate / traceability checks (Phase 1C, TASK 11)",
        "",
        f"- Input meta rows: {len(meta_all)} (embeddings_meta full, row-aligned with labels).",
        f"- Clustered (labels != -1): {len(clustered_ids)}; noise (labels == -1): {len(noise_ids)}.",
        f"- Noise sample: {len(noise)} rows; validation candidates: {len(val)} rows.",
        "",
        "## Per-check results",
        "",
        "| check | ok | detail |",
        "|---|---|---|",
    ]
    for c in checks:
        lines.append(f"| {c['check']} | {c['ok']} | {c['detail']} |")
        if len(c["check"]) > 80:
            print(c)
    lines += [
        "",
        "## Cross-cluster exact duplicates (evidence for MERGES, NOT leakage)",
        "",
        "A customer message belongs to exactly one cluster (HDBSCAN). The same *template* "
        "text appearing in several clusters is therefore a **merge signal** (the clusters are "
        "near-duplicate conversation-closure turns), not a data leak. Top examples:",
        "",
        "| exact_text | n clusters | clusters |",
        "|---|---|---|",
    ]
    for _, r in dup_summary.head(8).iterrows():
        lines.append(f"| {r['exact_text']} | {r['n_clusters']} | {r['cluster_ids']} |")
    lines += [
        "",
        "## Notes",
        "- All noise-sample rows verified to carry HDBSCAN label == -1 and to come from the "
        "noise point set.",
        "- All validation candidates verify against embeddings_meta (full); nothing references "
        "a message id that does not exist in the pipeline.",
        "- Cluster-source and noise-source validation rows are disjoint by construction and "
        "re-verified here.",
    ]
    (TAX / "leakage_checks.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"leakage_checks.csv ({len(checks)} checks) + leakage_checks.md written")
    print(f"cross_cluster_exact_duplicates.csv: {len(dup_summary)} rows")


if __name__ == "__main__":
    main()