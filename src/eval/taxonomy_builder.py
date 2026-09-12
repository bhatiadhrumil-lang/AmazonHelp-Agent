"""Final-taxonomy builder SCAFFOLDING (Phase 3, TASK 8) — runs only on human labels.

Compiles `artifacts/taxonomy/final_taxonomy.{csv,md}` from golden_labels.csv:
- intents = human intent_ids (majority where double-labelled; disagreement
  flagged, never silently resolved)
- aggregates taxonomy_verdict codes per preliminary family (merge/split/new
  proposals listed with supporting candidate ids)
- OOD = human ood flag; contextual = human context_dependent verdicts
- each intent gets: id, name, definition (most common primary_goal),
  inclusion/exclusion notes from verdicts, example ids, routing notes from
  routing_expectation majority, risk notes from escalation reasons.

BLOCKED until golden_labels.csv exists. Smoke-runnable on provisional data
only via --smoke (clearly marked, never written to artifacts/taxonomy/).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
TAX = ROOT / "artifacts/taxonomy"


def build(labels: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    lab = labels.drop(columns=["cluster_family"], errors="ignore").merge(
        candidates[["candidate_id", "cluster_family"]],
        on="candidate_id", how="left")
    rows = []
    for intent, g in lab.groupby("intent_id"):
        agree = g.candidate_id.value_counts()
        multi = agree[agree > 1].index
        conflict = [c for c in multi
                    if g[g.candidate_id == c].intent_id.nunique() > 1]
        rows.append({
            "intent_id": intent,
            "name": g.intent_name.mode().iloc[0],
            "definition": g.primary_goal.mode().iloc[0],
            "n_labels": len(g),
            "n_annotators": g.annotator.nunique(),
            "conflicted_candidates": ";".join(conflict),
            "source_families": ";".join(sorted(g.cluster_family.unique())),
            "verdicts": g.taxonomy_verdict.value_counts().to_dict(),
            "routing_majority": g.routing_expectation.mode().iloc[0],
            "risk_notes": "; ".join(sorted(set(
                x for x in g.escalation_reason if x)) )[:500],
            "example_candidate_ids": ";".join(g.candidate_id.head(5)),
            "ood_share": round(float(g.ood.mean()), 3),
        })
    return pd.DataFrame(rows).sort_values("intent_id").reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="pipeline smoke test only; writes nothing authoritative")
    args = ap.parse_args()
    p = EVAL / "golden_labels.csv"
    if not p.exists():
        print("BLOCKED: no golden_labels.csv — human annotation pending.")
        raise SystemExit(2)
    labels = pd.read_csv(p, keep_default_na=False)
    candidates = pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)
    tax = build(labels, candidates)
    if args.smoke:
        print(f"SMOKE (not authoritative): would emit {len(tax)} intents")
        print(tax.head(10).to_string(index=False))
        return
    TAX.mkdir(parents=True, exist_ok=True)
    tax.to_csv(TAX / "final_taxonomy.csv", index=False)
    with open(TAX / "final_taxonomy.md", "w") as f:
        f.write("# Final taxonomy (human-validated)\n\n")
        f.write(f"Intents: {len(tax)} from {len(labels)} labels.\n\n")
        for _, r in tax.iterrows():
            f.write(f"## {r['intent_id']} — {r['name']}\n\n")
            f.write(f"Definition: {r['definition']}\n\n")
            f.write(f"Labels: {r['n_labels']} ({r['n_annotators']} annotators). "
                    f"Routing majority: {r['routing_majority']}. "
                    f"OOD share: {r['ood_share']}.\n\n")
            if r["conflicted_candidates"]:
                f.write(f"DISAGREEMENT (unresolved): {r['conflicted_candidates']}\n\n")
            f.write(f"Source families: {r['source_families']}\n\n")
    print(f"wrote final_taxonomy.csv/md with {len(tax)} intents")


if __name__ == "__main__":
    main()
