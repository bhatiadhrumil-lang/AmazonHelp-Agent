"""Golden-label annotation CLI, workflow v2 (human-in-the-loop, fast, auditable).

Same command as before:
    PYTHONPATH=src .venv/bin/python -m eval.annotate --annotator <name>

Per item the annotator sees: message, prior CUSTOMER turns, historical reply
(marked evidence-only), cluster context, and the MODEL SUGGESTION — NOT
GROUND TRUTH (nearest-centroid family + alternatives, same model as agent).

Decision flow: [A]ccept suggestion / [C]hoose existing intent (numbered
catalog) / [N]ew intent (justified) / [U]ncertain. Acceptance is recorded as
a HUMAN-CONFIRMED label with outcome='accepted' — never auto-generated.

Safety: append + flush per saved row (Ctrl+C safe), done-set prevents
duplicates, progress header on start/resume, --labels-out routes output to a
scratch file for smoke tests (production default = golden_labels.csv).
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd

from eval.schema import (DISAGREEMENT_CODES, ROUTING_EXPECTATIONS,
                         SUGGESTION_OUTCOMES, GoldenLabel)
from eval.suggest import (Suggestion, compute_suggestions, human_coined_intents,
                          load_catalog)

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL = ROOT / "artifacts/evaluation"
CAND = EVAL / "golden_candidates.csv"
LABELS_DEFAULT = EVAL / "golden_labels.csv"
META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"
EPISODES = ROOT / "artifacts/conversation_audit/full_run_fixed/customer_problem_episodes.csv"

ROUTING_MENU = [("1", "auto_ok"), ("2", "clarify"), ("3", "escalate"), ("4", "unsure")]
VERDICT_MENU = [(str(i + 1), v) for i, v in enumerate(DISAGREEMENT_CODES)]
UNCERTAIN_VERDICTS = ("ambiguous", "context_dependent", "ood")
ENTITY_TYPES = ["URL", "EMAIL", "PHONE_LIKE", "MONEY_AMOUNT", "CARRIER",
                "MARKETPLACE", "ACCOUNT_PRIVATE", "ORDER_CONTEXT", "OTHER"]


# ---------- pure helpers (unit-tested) ----------

def progress_counts(cand: pd.DataFrame, labels_path: Path,
                    annotator: str) -> Tuple[int, int, int]:
    """(total, completed_by_annotator, remaining)."""
    done: Set[str] = set()
    if labels_path.exists():
        d = pd.read_csv(labels_path, keep_default_na=False)
        done = set(d[d.annotator == annotator].candidate_id)
    total = len(cand)
    completed = len(done & set(cand.candidate_id))
    return total, completed, total - completed


def load_done(labels_path: Path) -> Set[Tuple[str, str]]:
    if not labels_path.exists():
        return set()
    d = pd.read_csv(labels_path, keep_default_na=False)
    return set(zip(d["candidate_id"], d["annotator"]))


def next_todo(cand: pd.DataFrame, done: Set[Tuple[str, str]],
              annotator: str, seed: int, limit: int) -> pd.DataFrame:
    todo = cand[~cand.candidate_id.isin(
        {c for c, a in done if a == annotator})]
    todo = todo.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return todo.head(limit) if limit else todo


def append_record(labels_path: Path, lab: GoldenLabel) -> None:
    first_write = not labels_path.exists()
    with open(labels_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=GoldenLabel.fieldnames())
        if first_write:
            w.writeheader()
        w.writerow(lab.to_dict())
        f.flush()


def derive_outcome(choice: str, final_intent: str,
                   suggestion: Suggestion) -> str:
    if choice == "A":
        return "accepted"
    if choice == "U":
        return "uncertain"
    if choice == "N":
        return "rejected"
    return "accepted" if final_intent == suggestion.family else "corrected"


def record_to_label(candidate_id: str, annotator: str, intent_id: str,
                    intent_name: str, primary_goal: str, entities: list,
                    routing: str, esc_reason: str, resp_req: str,
                    ambiguity: bool, ood: bool, verdict: str, notes: str,
                    second: bool, suggestion: Suggestion,
                    outcome: str) -> GoldenLabel:
    return GoldenLabel(
        candidate_id=candidate_id, annotator=annotator,
        intent_id=intent_id.strip().replace(" ", "_").lower(),
        intent_name=intent_name, primary_goal=primary_goal, entities=entities,
        routing_expectation=routing, escalation_reason=esc_reason,
        response_requirements=resp_req, ambiguity=ambiguity, ood=ood,
        taxonomy_verdict=verdict, taxonomy_notes=notes,
        needs_second_opinion=second, model_suggestion=suggestion.family,
        suggestion_outcome=outcome,
        annotated_at=datetime.now(timezone.utc).isoformat())


# ---------- interactive helpers ----------

def ask(prompt: str, default: str = "") -> str:
    return input(f"{prompt} [{default}]: ").strip() or default


def ask_menu(prompt: str, options: List[Tuple[str, str]], default: str) -> str:
    print(f"{prompt}")
    for key, val in options:
        print(f"  [{key}] {val}")
    valid = {k: v for k, v in options}
    while True:
        raw = input(f"choice [{default}]: ").strip() or default
        if raw in valid:
            return valid[raw]
        print(f"  enter one of: {sorted(valid)}")


def ask_yes_no(prompt: str, default: str = "n") -> bool:
    return (input(f"{prompt} (y/n) [{default}]: ").strip() or default).lower().startswith("y")


def choose_existing(catalog: pd.DataFrame,
                    coined: pd.DataFrame) -> Tuple[str, str]:
    filt = ask("filter catalog (substring, blank = show all)", "")
    sub = catalog
    if filt:
        sub = catalog[catalog.family_key.str.contains(filt, case=False)
                      | catalog.preliminary_label.str.contains(filt, case=False)]
    rows = sub.reset_index(drop=True)
    for i, r in rows.iterrows():
        print(f"  [{i + 1}] {r['family_key']} — {r['preliminary_label']}")
    if len(coined):
        print("  Human-coined so far (reuse to avoid duplicates):")
        for _, r in coined.iterrows():
            print(f"    {r['intent_id']} — {r['intent_name']} (x{r['n']})")
    while True:
        raw = ask(f"number 1-{len(rows)} (or 'coined:<id>' / blank=resheet)")
        if raw.startswith("coined:"):
            cid = raw.split(":", 1)[1]
            hit = coined[coined.intent_id == cid]
            if len(hit):
                return hit.iloc[0]["intent_id"], hit.iloc[0]["intent_name"]
            print("  unknown coined id");
            continue
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(rows):
                r = rows.iloc[idx]
                return r["family_key"], r["preliminary_label"]
        except ValueError:
            pass
        print("  invalid choice")


def main() -> None:
    ap = argparse.ArgumentParser(description="Golden-label annotation CLI (v2)")
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--labels-out", default=str(LABELS_DEFAULT),
                    help="output CSV (default: golden_labels.csv; use a scratch path for smoke tests)")
    args = ap.parse_args()
    labels_path = Path(args.labels_out)

    cand = pd.read_csv(CAND, keep_default_na=False)
    total, completed, remaining = progress_counts(cand, labels_path, args.annotator)
    print(f"Annotator: {args.annotator}")
    print(f"{total} total | {completed} completed | {remaining} remaining")
    catalog = load_catalog()
    coined = human_coined_intents()
    sugg = compute_suggestions(cand.embedding_index.astype(int).tolist())
    meta = pd.read_csv(META, keep_default_na=False)
    epi = pd.read_csv(EPISODES, keep_default_na=False)
    epi_small = epi.set_index("customer_message_id")["brand_parent_text"].to_dict()
    by_conv = {k: v for k, v in
               meta.sort_values("created_dt").groupby("conversation_id")["text"].apply(list).items()}
    done = load_done(labels_path)
    todo = next_todo(cand, done, args.annotator, args.seed, args.limit)
    if len(todo) == 0:
        print("Nothing left to label.");
        return
    saved = 0
    try:
        for _, r in todo.iterrows():
            s = sugg[int(r["embedding_index"])]
            print("\n" + "=" * 70)
            print(f"[{r['candidate_id']}] reason={r['sampling_reason']} "
                  f"cluster={r['cluster_id']} family={r['cluster_family']}")
            print(f"MESSAGE: {r['customer_text']}")
            thread = by_conv.get(r["conversation_id"], [])
            try:
                pos = thread.index(r["customer_text"])
                priors = thread[max(0, pos - 2):pos]
            except ValueError:
                priors = []
            if priors:
                print("PRIOR CUSTOMER CONTEXT:")
                for p in priors:
                    print(f"  < {p[:200]}")
            else:
                print("(no prior in-corpus customer turns)")
            resp = epi_small.get(r["customer_message_id"], "")
            if resp:
                print(f"HISTORICAL REPLY [evidence only, NOT the answer]: {resp[:300]}")
            print(f"CLUSTER CONTEXT: family={r['cluster_family']} "
                  f"prob={r['cluster_probability']} margin={r['centroid_margin']}")
            print("MODEL SUGGESTION — NOT GROUND TRUTH:")
            print(f"  intent: {s.family}  (provisional, sim={s.similarity}, margin={s.margin})")
            print(f"  reason/context: nearest-centroid family; display='{s.display_name}'")
            for a in s.alternatives:
                print(f"    alt: {a['family']} (sim={a['sim']})")
            choice = ask_menu("Your decision", [("A", "Accept suggestion (you reviewed & confirm)"),
                                                ("C", "Choose existing intent"),
                                                ("N", "New intent (justify)"),
                                                ("U", "Uncertain / context-dependent")], "A")
            # map menu value back to letter
            choice = {"Accept suggestion (you reviewed & confirm)": "A",
                      "Choose existing intent": "C",
                      "New intent (justify)": "N",
                      "Uncertain / context-dependent": "U"}[choice]
            if choice == "A":
                intent_id, intent_name = s.family, s.display_name
                intent_name = ask("intent_name (Enter = suggestion display)", intent_name)
                verdict = ask_menu("taxonomy_verdict", VERDICT_MENU, "1")
            elif choice == "C":
                intent_id, intent_name = choose_existing(catalog, coined)
                verdict = ask_menu("taxonomy_verdict", VERDICT_MENU, "1")
            elif choice == "N":
                intent_id = ask("new intent_id (snake_case)").strip().replace(" ", "_").lower()
                intent_name = ask("new intent_name")
                print("verdict forced toward new_intent (change only with justification):")
                verdict = ask_menu("taxonomy_verdict", VERDICT_MENU, "4")
            else:
                intent_id, intent_name = "uncertain", "Uncertain — needs adjudication"
                verdict = ask_menu("taxonomy_verdict",
                                   [(k, v) for k, v in VERDICT_MENU
                                    if v in UNCERTAIN_VERDICTS], "6")
            primary_goal = ask("primary_goal (WHAT does the customer want?)")
            routing = ask_menu("routing_expectation", ROUTING_MENU, "4")
            esc_reason, resp_req = "", ""
            if routing == "escalate":
                esc_reason = ask("escalation_reason (REQUIRED for escalate)")
                while not esc_reason.strip():
                    print("  escalation_reason is required for ESCALATE");
                    esc_reason = ask("escalation_reason (REQUIRED for escalate)")
                resp_req = ask("response_requirements (blank ok)")
            elif routing == "clarify":
                resp_req = ask("clarification rationale/requirements (REQUIRED for clarify)")
                while not resp_req.strip():
                    print("  a concise clarification rationale is required for CLARIFY");
                    resp_req = ask("clarification rationale/requirements (REQUIRED for clarify)")
                esc_reason = ask("escalation_reason (blank ok)", "")
            else:
                if routing == "auto_ok":
                    print("  (escalation_reason defaults to blank for AUTO)")
                esc_reason = ask("escalation_reason (blank ok)", "")
                resp_req = ask("response_requirements (blank ok)", "")
            ambiguity = ask_yes_no("ambiguity?", "n")
            ood = ask_yes_no("ood?", "n")
            notes = ""
            if choice == "N" or verdict == "new_intent":
                notes = ask("taxonomy_notes (REQUIRED: describe the proposal)")
                while not notes.strip():
                    print("  taxonomy_notes required for new_intent");
                    notes = ask("taxonomy_notes (REQUIRED: describe the proposal)")
            elif ood:
                notes = ask("taxonomy_notes (REQUIRED: OOD explanation)")
                while not notes.strip():
                    print("  OOD requires a taxonomy_notes explanation");
                    notes = ask("taxonomy_notes (REQUIRED: OOD explanation)")
                verdict = "ood"
            else:
                notes = ask("taxonomy_notes (blank ok)", "")
            if ood and verdict != "ood":
                print("  (verdict forced to 'ood' because ood=true)");
                verdict = "ood"
            second = ask_yes_no("needs_second_opinion?", "n")
            n_ent = ask("how many entities? (0 = none, quick)", "0")
            entities = []
            try:
                for _ in range(int(n_ent or 0)):
                    print(f"  known types: {', '.join(ENTITY_TYPES)}")
                    et = ask("  entity type")
                    ev = ask("  entity value")
                    entities.append({"type": et, "value": ev})
            except ValueError:
                pass
            outcome = derive_outcome(choice, intent_id.strip().replace(" ", "_").lower(), s)
            lab = record_to_label(
                r["candidate_id"], args.annotator, intent_id, intent_name,
                primary_goal, entities, routing, esc_reason, resp_req,
                ambiguity, ood, verdict, notes, second, s, outcome)
            errs = lab.validate()
            if errs:
                print("INVALID (fix now): " + "; ".join(errs))
                # minimal repair loop: re-ask only the failing dimensions
                for e in errs:
                    if "escalation_reason" in e or "escalation" in e:
                        lab.escalation_reason = ask("escalation_reason (REQUIRED)")
                    elif "clarif" in e or "response_requirements" in e:
                        lab.response_requirements = ask("response_requirements (REQUIRED)")
                    elif "taxonomy_notes" in e or "new_intent" in e or "OOD" in e:
                        lab.taxonomy_notes = ask("taxonomy_notes (REQUIRED)")
                    elif "intent_id" in e:
                        lab.intent_id = ask("intent_id (snake_case)").strip().replace(" ", "_").lower()
                    elif "primary_goal" in e:
                        lab.primary_goal = ask("primary_goal (WHAT does the customer want?)")
                    elif "verdict" in e:
                        lab.taxonomy_verdict = ask_menu("taxonomy_verdict", VERDICT_MENU, "1")
                    elif "routing" in e:
                        lab.routing_expectation = ask_menu("routing_expectation", ROUTING_MENU, "4")
                errs = lab.validate()
                if errs:
                    print("STILL INVALID — discarding this item (not saved): " + "; ".join(errs))
                    continue
            print(f"REVIEW: intent={lab.intent_id} routing={lab.routing_expectation} "
                  f"verdict={lab.taxonomy_verdict} outcome={lab.suggestion_outcome}")
            if ask("save? [s]ave / [r]edo", "s").lower().startswith("r"):
                print("  discarded, moving on (re-run to relabel this item)");
                continue
            append_record(labels_path, lab)
            done.add((r["candidate_id"], args.annotator))
            saved += 1
            print(f"saved ({saved} this session)")
    except KeyboardInterrupt:
        print(f"\nInterrupted. Saved {saved} this session. Resume with the same command.")
    print(f"\nDone. Saved {saved}. Labels live in {labels_path}. Validate with: "
          f"PYTHONPATH=src .venv/bin/python -m eval.check_labels")


if __name__ == "__main__":
    main()
