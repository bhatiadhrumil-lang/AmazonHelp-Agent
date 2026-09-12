"""Build deterministic human-review queue from model drafts (read-only on drafts).

Reads:
  artifacts/evaluation/annotation_draft.csv (204 MODEL RECOMMENDATIONS ONLY)
  artifacts/evaluation/golden_labels.csv (human ground truth, read-only)
Writes:
  artifacts/evaluation/annotation_review_queue.csv
  artifacts/evaluation/annotation_review_summary.json

Priority rules (deterministic, transparent; tie-break by candidate_id):
  P5 if ambiguity==true OR ood==true OR taxonomy_verdict in
      (ambiguous, new_intent, merge, split, context_dependent)
  elif needs_second_opinion==yes -> P4
  elif confidence==LOW -> P3
  elif confidence==MEDIUM -> P2
  elif confidence==HIGH and verdict==fits and ambiguity==false
       and ood==false and second==no -> P1
  else -> P2 (fallback, never silent)

Priority is REVIEW ORDER ONLY and never changes the label.
human_review_status = already_verified iff candidate_id in golden_labels.csv,
else pending. HIGH model confidence never implies human verification.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
DRAFT = EVAL / "annotation_draft.csv"
LABELS = EVAL / "golden_labels.csv"
QUEUE = EVAL / "annotation_review_queue.csv"
SUMMARY = EVAL / "annotation_review_summary.json"

QUEUE_FIELDNAMES = [
    "priority", "priority_reason", "candidate_id",
    "model_intent_id", "model_intent_name", "model_confidence",
    "routing_expectation", "ambiguity", "ood", "taxonomy_verdict",
    "needs_second_opinion", "human_review_status", "human_decision",
    "human_notes",
]

TAXONOMY_P5 = {"ambiguous", "new_intent", "merge", "split", "context_dependent"}


def compute_priority(rec: dict) -> tuple[int, str]:
    amb = rec.get("ambiguity", "false") == "true"
    ood = rec.get("ood", "false") == "true"
    verdict = rec.get("taxonomy_verdict", "fits")
    second = rec.get("needs_second_opinion", "no") == "yes"
    conf = rec.get("confidence", "MEDIUM")
    if amb or ood or verdict in TAXONOMY_P5:
        reasons = []
        if amb:
            reasons.append("ambiguity=true")
        if ood:
            reasons.append("ood=true")
        if verdict in TAXONOMY_P5:
            reasons.append(f"verdict={verdict}")
        return 5, "taxonomy/ambiguity attention: " + ", ".join(reasons)
    if second:
        return 4, "needs second opinion"
    if conf == "LOW":
        return 3, "low model confidence / weak similarity"
    if conf == "MEDIUM":
        return 2, "medium confidence, normal review"
    if (conf == "HIGH" and verdict == "fits" and not amb
            and not ood and not second):
        return 1, "high-confidence fits, fastest verification"
    return 2, "fallback medium review"


def main() -> None:
    if not DRAFT.exists():
        raise FileNotFoundError(f"missing draft: {DRAFT} (run copilot_draft first)")
    with open(DRAFT, "r", newline="", encoding="utf-8") as f:
        drafts = list(csv.DictReader(f))
    if len(drafts) != 204 or len({r["candidate_id"] for r in drafts}) != 204:
        raise ValueError(
            f"draft must contain 204 unique IDs, found {len(drafts)} rows / "
            f"{len({r['candidate_id'] for r in drafts})} unique")
    human_map: dict[str, str] = {}
    if LABELS.exists():
        with open(LABELS, "r", newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                human_map.setdefault(r["candidate_id"], r.get("intent_id", ""))
    rows = []
    for rec in drafts:
        pri, reason = compute_priority(rec)
        cid = rec["candidate_id"]
        verified = cid in human_map
        rows.append({
            "priority": str(pri),
            "priority_reason": reason,
            "candidate_id": cid,
            "model_intent_id": rec["suggested_intent_id"],
            "model_intent_name": rec["suggested_intent_name"],
            "model_confidence": rec["confidence"],
            "routing_expectation": rec["routing_expectation"],
            "ambiguity": rec["ambiguity"],
            "ood": rec["ood"],
            "taxonomy_verdict": rec["taxonomy_verdict"],
            "needs_second_opinion": rec["needs_second_opinion"],
            "human_review_status": "already_verified" if verified else "pending",
            "human_decision": human_map[cid] if verified else "",
            "human_notes": "",
        })
    rows.sort(key=lambda r: (int(r["priority"]), r["candidate_id"]))
    tmp = QUEUE.with_suffix(".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=QUEUE_FIELDNAMES,
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
                           doublequote=True, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)
        f.flush()
    tmp.replace(QUEUE)
    summary = {
        "total_candidates": len(rows),
        "already_verified": sum(1 for r in rows if r["human_review_status"] == "already_verified"),
        "pending": sum(1 for r in rows if r["human_review_status"] == "pending"),
        "by_priority": dict(Counter(r["priority"] for r in rows)),
        "by_confidence": dict(Counter(r["model_confidence"] for r in rows)),
        "by_verdict": dict(Counter(r["taxonomy_verdict"] for r in rows)),
        "ambiguity_true": sum(1 for r in rows if r["ambiguity"] == "true"),
        "ood_true": sum(1 for r in rows if r["ood"] == "true"),
        "second_opinion_yes": sum(1 for r in rows if r["needs_second_opinion"] == "yes"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "REVIEW ORDER ONLY — model recommendations are not human ground truth.",
        "priority_rules": (
            "P5: ambiguity/ood/verdict in ambiguous,new_intent,merge,split,context_dependent; "
            "P4: needs_second_opinion=yes; P3: confidence LOW; P2: MEDIUM/fallback; "
            "P1: HIGH+fits+unambiguous+not ood+no second opinion; tie-break candidate_id."
        ),
    }
    stmp = SUMMARY.with_suffix(".tmp")
    with open(stmp, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.flush()
    stmp.replace(SUMMARY)
    print(f"Wrote {len(rows)} queue rows to {QUEUE.name}; "
          f"{summary['already_verified']} verified, {summary['pending']} pending.")


if __name__ == "__main__":
    main()
