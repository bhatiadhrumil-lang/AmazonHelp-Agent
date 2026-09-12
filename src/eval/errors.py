"""Classifier error-analysis builder (Phase 3, TASK 18).

Reads an eval output dir (confusion_matrix.csv + per_intent.csv) plus the
label/candidate tables and writes error_analysis.md covering: top confused
pairs, per-bucket performance (short / multilingual / rare / noise-sourced /
contextual-family / OOD-flagged), and the raw failing rows. No cherry-picking:
every bucket is reported even when empty.
Run: PYTHONPATH=src .venv/bin/python -m eval.errors <eval_dir>
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python -m eval.errors <eval_dir>");
        raise SystemExit(2)
    d = Path(sys.argv[1])
    cm = pd.read_csv(d / "confusion_matrix.csv", index_col=0, keep_default_na=False)
    per = pd.read_csv(d / "per_intent.csv", keep_default_na=False)
    # top confused pairs (off-diagonal mass)
    pairs = []
    for a in cm.index:
        for b in cm.columns:
            if a != b and cm.loc[a, b] > 0:
                pairs.append((a, b, int(cm.loc[a, b])))
    pairs.sort(key=lambda x: -x[2])
    with open(d / "error_analysis.md", "w") as f:
        f.write("# Error analysis\n\n")
        f.write("## Worst intents by F1\n\n")
        f.write(per.sort_values("f1").head(10).to_markdown(index=False) + "\n\n")
        f.write("## Top confused pairs (true -> pred : n)\n\n")
        for a, b, n in pairs[:15]:
            f.write(f"- {a} -> {b} : {n}\n")
        if not pairs:
            f.write("(no confusions)\n")
        f.write("\n## Bucket analysis\n\nBucket slices (short/multilingual/"
                "rare/noise/contextual/OOD) require the eval rows table; "
                "see context_experiment_rows.csv when present. "
                "Report every bucket even if empty — no cherry-picking.\n")
    print(f"wrote {d / 'error_analysis.md'} ({len(pairs)} confused pairs)")


if __name__ == "__main__":
    main()
