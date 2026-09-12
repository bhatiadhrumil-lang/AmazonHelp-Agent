"""Annotation copilot draft generator (MODEL RECOMMENDATIONS ONLY).

Writes to artifacts/evaluation/annotation_draft.csv + annotation_progress.json,
NEVER to golden_labels.csv. Human labels remain the only ground truth.

Usage:
  PYTHONPATH=src .venv/bin/python -m eval.copilot_draft [--limit N] [--force]

Resume-safe: existing draft rows are skipped unless --force is given.
Atomic: per-case append+flush, progress JSON via tmp+replace.
CSV-safe: QUOTE_MINIMAL, lineterminator newline, doublequote.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from eval.suggest import compute_suggestions, load_catalog

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
CAND = EVAL / "golden_candidates.csv"
LABELS = EVAL / "golden_labels.csv"
DRAFT = EVAL / "annotation_draft.csv"
PROGRESS = EVAL / "annotation_progress.json"
META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
EPISODES = ROOT / "artifacts/conversation_audit/full_run_fixed/customer_problem_episodes.csv"

DRAFT_FIELDNAMES = [
    "candidate_id", "model_suggestion", "suggested_intent_id",
    "suggested_intent_name", "primary_goal", "routing_expectation",
    "escalation_reason", "response_requirements", "ambiguity", "ood",
    "taxonomy_verdict", "taxonomy_notes", "entities",
    "needs_second_opinion", "confidence", "decision_summary", "why",
    "alternatives", "human_check", "generated_at", "status",
]

AUTO_FAMILIES = {
    "ack_thanks", "ack_done", "ack_willdo", "resolution_thanks",
    "empathy_farewell", "template_affirm", "template_neg", "template_time",
}
OOD_FAMILIES = {"off_topic_chat"}
CLARIFY_FAMILIES = {
    "delivery_estimate", "time_estimate_query", "next_step_guidance",
    "product_question", "region_mismatch", "stock_availability",
    "shipping_cost", "price_change", "contact_channel",
    "status_update_request",
}
CONTEXTUAL_FAMILIES = {
    "detail_provided", "status_update_request", "transitional",
    "time_estimate_query", "waiting_status", "megacluster_unclear",
}


def _bool_str(v: bool) -> str:
    return "true" if v else "false"


def build_recommendation(row, sugg, catalog_map, priors, hist_reply):
    fam = sugg.family
    display = sugg.display_name
    kind = catalog_map.get(fam, {}).get("kind", "")
    text = row["customer_text"] or ""
    txt = text.strip()
    low_margin = sugg.margin < 0.03
    low_sim = sugg.similarity < 0.5
    short = len(txt) < 30

    # --- taxonomy / ood / ambiguity ---
    if fam in OOD_FAMILIES:
        ood = True
        verdict = "ood"
        ambiguity = False
        needs_second = False
        confidence = "MEDIUM"
    elif fam == "megacluster_unclear":
        ood = False
        verdict = "ambiguous"
        ambiguity = True
        needs_second = True
        confidence = "LOW"
    elif fam == "transitional" and (short or low_margin):
        ood = False
        verdict = "context_dependent"
        ambiguity = True
        needs_second = True
        confidence = "LOW"
    elif low_margin or low_sim:
        ood = False
        verdict = "fits"
        ambiguity = short
        needs_second = True
        confidence = "LOW"
    else:
        ood = False
        verdict = "fits"
        ambiguity = False
        needs_second = fam in CONTEXTUAL_FAMILIES
        confidence = "MEDIUM" if fam in CONTEXTUAL_FAMILIES else "HIGH"
        if confidence == "HIGH" and sugg.margin < 0.06:
            confidence = "MEDIUM"

    # --- routing (conservative; never equate confidence with AUTO) ---
    if ood:
        routing = "auto_ok"
        esc_reason = ""
        resp_req = "Brief generic acknowledgement; no account action; must not request private details."
    elif fam in AUTO_FAMILIES and not ambiguity:
        routing = "auto_ok"
        esc_reason = ""
        resp_req = "Brief acknowledgement only; no order/account action; must not request private details publicly."
    elif fam in CLARIFY_FAMILIES and not ambiguity:
        routing = "clarify"
        esc_reason = ""
        resp_req = "Ask one safe clarifying question; must not request order IDs/payment/phone publicly; offer private handoff if needed."
    elif verdict in ("ambiguous", "context_dependent"):
        routing = "unsure"
        esc_reason = ""
        resp_req = "Insufficient context for safe auto-response; human must review priors before acting."
    else:
        routing = "escalate"
        esc_reason = "Requires private/order-specific investigation or human review; do not handle fully automatically from public message."
        resp_req = "Acknowledge and direct to private/secure channel; must not request order IDs/payment/phone publicly; must not promise outcome."

    # --- text fields (clearly marked as model draft) ---
    snippet = txt[:160].replace("\n", " ")
    primary_goal = f"DRAFT (verify): {display} — customer wrote: '{snippet}'"
    decision_summary = (
        f"Model-draft suggests {fam}; "
        f"{'OOD chatter, no support action' if ood else 'requires HUMAN verification before use as label'}."
    )
    why_bits = [
        f"Current message: '{snippet}'.",
        f"Model suggestion {fam} (sim={sugg.similarity}, margin={sugg.margin}) is NOT ground truth.",
        f"Cluster family={row.get('cluster_family','')} sampling={row.get('sampling_reason','')}.",
    ]
    if priors:
        why_bits.append(f"Priors considered ({len(priors)}): '{priors[-1][:120]}'.")
    else:
        why_bits.append("No prior in-corpus customer turns.")
    if hist_reply:
        why_bits.append("Historical reply treated as evidence only, not the answer.")
    why = " ".join(why_bits)
    alts = "; ".join(
        f"{a['family']} (sim={a['sim']}, {a['display']})"
        for a in (sugg.alternatives or [])
    ) or "(none)"
    human_check = (
        "In CLI verify: read MESSAGE alone first, then priors; "
        f"confirm/override intent {fam}; confirm routing {routing}; "
        "set entities (draft uses 0); decide second-opinion flag. "
        "You must press [s]ave in eval.annotate to create ground truth."
    )
    notes = (
        f"Model-draft from {fam}; margin={sugg.margin}, sim={sugg.similarity}. "
        "Human must confirm/correct. "
        + (f"Cluster={row.get('cluster_family','')}. " if row.get("cluster_family") else "")
        + ("Low-margin: alternatives close; review required. " if low_margin else "")
    )

    return {
        "candidate_id": row["candidate_id"],
        "model_suggestion": fam,
        "suggested_intent_id": fam,
        "suggested_intent_name": display,
        "primary_goal": primary_goal,
        "routing_expectation": routing,
        "escalation_reason": esc_reason,
        "response_requirements": resp_req,
        "ambiguity": _bool_str(bool(ambiguity)),
        "ood": _bool_str(bool(ood)),
        "taxonomy_verdict": verdict,
        "taxonomy_notes": notes,
        "entities": "0",
        "needs_second_opinion": "yes" if needs_second else "no",
        "confidence": confidence,
        "decision_summary": decision_summary,
        "why": why,
        "alternatives": alts,
        "human_check": human_check,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "model_recommendation",
    }


def load_done_draft(draft_path: Path) -> set:
    if not draft_path.exists():
        return set()
    done = set()
    with open(draft_path, "r", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("candidate_id"):
                done.add(r["candidate_id"])
    return done


def write_progress(total, done_n, last_id):
    tmp = PROGRESS.with_suffix(".tmp")
    payload = {
        "total_candidates": total,
        "draft_completed": done_n,
        "remaining": total - done_n,
        "last_candidate_id": last_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "draft_file": str(DRAFT.name),
        "golden_labels_file": str(LABELS.name),
        "note": "MODEL RECOMMENDATIONS ONLY — not human ground truth.",
    }
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.flush()
    tmp.replace(PROGRESS)


def main() -> None:
    ap = argparse.ArgumentParser(description="Copilot draft generator (model recs only)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true",
                    help="regenerate even if draft row exists")
    args = ap.parse_args()

    cand = pd.read_csv(CAND, keep_default_na=False)
    catalog = load_catalog()
    catalog_map = catalog.set_index("family_key").to_dict(orient="index")

    # priors + historical evidence (best-effort; missing => empty)
    try:
        meta = pd.read_csv(META, keep_default_na=False)
        by_conv = {
            k: v for k, v in
            meta.sort_values("created_dt").groupby("conversation_id")["text"].apply(list).items()
        }
    except Exception:
        by_conv = {}
    try:
        epi = pd.read_csv(EPISODES, keep_default_na=False)
        epi_small = epi.set_index("customer_message_id")["brand_parent_text"].to_dict()
    except Exception:
        epi_small = {}

    sugg = compute_suggestions(cand.embedding_index.astype(int).tolist())

    done = set() if args.force else load_done_draft(DRAFT)
    if args.force and DRAFT.exists():
        DRAFT.unlink()
        done = set()
    first_write = not DRAFT.exists()
    # ensure header exists
    if first_write:
        with open(DRAFT, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=DRAFT_FIELDNAMES,
                               quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
                               doublequote=True, extrasaction="raise")
            w.writeheader()
            f.flush()

    todo = cand[~cand.candidate_id.isin(done)].reset_index(drop=True)
    if args.limit:
        todo = todo.head(args.limit)
    print(f"Draft resume: {len(done)} existing, {len(todo)} to process, {len(cand)} total.")
    processed = 0
    with open(DRAFT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=DRAFT_FIELDNAMES,
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
                           doublequote=True, extrasaction="raise")
        for _, r in todo.iterrows():
            row = r.to_dict()
            s = sugg[int(row["embedding_index"])]
            thread = by_conv.get(row["conversation_id"], [])
            try:
                pos = thread.index(row["customer_text"])
                priors = thread[max(0, pos - 2):pos]
            except ValueError:
                priors = []
            hist = epi_small.get(row["customer_message_id"], "")
            rec = build_recommendation(row, s, catalog_map, priors, hist)
            w.writerow(rec)
            f.flush()
            processed += 1
            write_progress(len(cand), len(done) + processed, row["candidate_id"])
    print(f"Done. Wrote {processed} model recommendations to {DRAFT.name}.")


if __name__ == "__main__":
    main()
