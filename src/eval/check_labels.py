"""Label file validator (Phase 3). Run: PYTHONPATH=src .venv/bin/python -m eval.check_labels"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from eval.schema import GoldenLabel

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"


def main() -> bool:
    p = EVAL / "golden_labels.csv"
    if not p.exists():
        print("BLOCKED: no golden_labels.csv yet — human annotation pending.")
        return False
    d = pd.read_csv(p, keep_default_na=False)
    cand = pd.read_csv(EVAL / "golden_candidates.csv", keep_default_na=False)
    ok = True
    unknown = set(d.candidate_id) - set(cand.candidate_id)
    if unknown:
        print(f"FAIL: {len(unknown)} labels reference unknown candidates");
        ok = False
    for i, r in d.iterrows():
        try:
            ents = json.loads(r["entities"]) if r["entities"] else []
        except Exception:
            print(f"FAIL row {i}: bad entities JSON");
            ok = False
            continue
        # New auditability columns are optional (pre-v2 rows lack them).
        get = lambda c: r[c] if c in d.columns and str(r[c]) != "" else ""
        lab = GoldenLabel(candidate_id=r["candidate_id"], annotator=r["annotator"],
                          intent_id=r["intent_id"], intent_name=r["intent_name"],
                          primary_goal=r["primary_goal"], entities=ents,
                          routing_expectation=r["routing_expectation"],
                          escalation_reason=r["escalation_reason"],
                          response_requirements=r["response_requirements"],
                          ambiguity=bool(r["ambiguity"]), ood=bool(r["ood"]),
                          taxonomy_verdict=r["taxonomy_verdict"],
                          taxonomy_notes=r["taxonomy_notes"],
                          needs_second_opinion=bool(r["needs_second_opinion"]),
                          model_suggestion=str(get("model_suggestion")),
                          suggestion_outcome=str(get("suggestion_outcome")),
                          annotated_at=str(get("annotated_at")))
        errs = lab.validate()
        if errs:
            print(f"FAIL row {i} ({r['candidate_id']}): {errs}");
            ok = False
    dup = d.duplicated(["candidate_id", "annotator"]).sum()
    if dup:
        print(f"FAIL: {dup} duplicate (candidate, annotator) rows");
        ok = False
    print(f"labels: {len(d)} rows, {d.annotator.nunique()} annotators, "
          f"{d.candidate_id.nunique()} candidates, intents: {d.intent_id.nunique()}")
    if "suggestion_outcome" in d.columns:
        print("suggestion outcomes: "
              + str(d["suggestion_outcome"].replace("", "(unrecorded pre-v2)").value_counts().to_dict()))
    print("VALID" if ok else "INVALID")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
