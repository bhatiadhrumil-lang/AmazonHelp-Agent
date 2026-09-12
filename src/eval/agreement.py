"""Inter-annotator agreement (Phase 3, TASK 7).

Compares double-labelled candidates on intent_id: raw agreement + Cohen's
kappa (with the standard observed/expected formulation over the union label
set). Reports per-item disagreements for analysis. Run:
PYTHONPATH=src .venv/bin/python -m eval.agreement
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"


def cohen_kappa(a: list, b: list) -> float:
    a = np.array(a);
    b = np.array(b)
    labels = sorted(set(a) | set(b))
    po = float((a == b).mean())
    pe = sum(float((a == l).mean() * (b == l).mean()) for l in labels)
    return (po - pe) / (1 - pe) if pe < 1.0 else 1.0


def main() -> None:
    p = EVAL / "golden_labels.csv"
    if not p.exists():
        print("BLOCKED: no golden_labels.csv yet.")
        return
    d = pd.read_csv(p, keep_default_na=False)
    wide = d.pivot_table(index="candidate_id", columns="annotator",
                         values="intent_id", aggfunc="first")
    multi = wide[wide.notna().sum(axis=1) >= 2]
    print(f"double-labelled candidates: {len(multi)} (target >= 40)")
    if len(multi) == 0:
        return
    anns = list(wide.columns)
    rows = []
    for x, y in combinations(anns, 2):
        sub = multi[[x, y]].dropna()
        if len(sub) == 0:
            continue
        k = cohen_kappa(sub[x].tolist(), sub[y].tolist())
        rows.append({"a": x, "b": y, "n": len(sub),
                     "raw": round(float((sub[x] == sub[y]).mean()), 4),
                     "kappa": round(k, 4)})
    rep = pd.DataFrame(rows)
    rep.to_csv(EVAL / "agreement_report.csv", index=False)
    print(rep.to_string(index=False))
    # disagreement cases for analysis
    dis = multi[multi.nunique(axis=1, dropna=True) > 1]
    dis_out = []
    for cid, r in dis.iterrows():
        dis_out.append({"candidate_id": cid,
                        **{f"label_{a}": r[a] for a in anns if pd.notna(r[a])}})
    pd.DataFrame(dis_out).to_csv(EVAL / "agreement_disagreements.csv", index=False)
    print(f"disagreements: {len(dis_out)} (see agreement_disagreements.csv)")
    with open(EVAL / "agreement_report.md", "w") as f:
        f.write("# Inter-annotator agreement\n\n")
        f.write(f"Double-labelled: {len(multi)}\n\n")
        f.write(rep.to_markdown(index=False))
        f.write(f"\n\nDisagreement cases: {len(dis_out)}\n")


if __name__ == "__main__":
    main()
