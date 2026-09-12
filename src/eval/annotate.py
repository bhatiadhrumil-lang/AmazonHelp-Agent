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
import json
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
REVIEW_QUEUE = EVAL / "annotation_review_queue.csv"
REVIEW_DRAFT = EVAL / "annotation_draft.csv"

ROUTING_MENU = [("1", "auto_ok"), ("2", "clarify"), ("3", "escalate"), ("4", "unsure")]
VERDICT_MENU = [(str(i + 1), v) for i, v in enumerate(DISAGREEMENT_CODES)]
UNCERTAIN_VERDICTS = ("ambiguous", "context_dependent", "ood")
ENTITY_TYPES = ["URL", "EMAIL", "PHONE_LIKE", "MONEY_AMOUNT", "CARRIER",
                "MARKETPLACE", "ACCOUNT_PRIVATE", "ORDER_CONTEXT", "OTHER"]

# Pre-v2 header (14 cols) lacks the v2 auditability columns. New header is
# GoldenLabel.fieldnames() (17 cols). Files written before v2 must be migrated
# (blank audit fields, honest not backfilled) instead of appending 17-col rows
# to a 14-col file, which breaks pandas CSV parsing.
LEGACY_FIELDNAMES = [c for c in GoldenLabel.fieldnames()
                     if c not in ("model_suggestion", "suggestion_outcome",
                                  "annotated_at")]
AUDIT_FIELDNAMES = ("model_suggestion", "suggestion_outcome", "annotated_at")


def ensure_labels_schema(labels_path: Path) -> None:
    """Migrate a pre-v2 or mixed-schema labels file to the 17-col schema.

    - Missing file/empty file: no-op (caller writes a fresh header).
    - Header already 17-col: pad any short (14-col) data rows with blanks.
    - Header legacy 14-col: rewrite header to 17-col; rows with 14 fields get
      blank audit fields, rows already carrying 17 fields keep their values.
    - Uses csv module with QUOTE_MINIMAL so commas/quotes/newlines round-trip.
    - Atomic via temp file + replace; preserves all existing rows exactly.
    """
    if not labels_path.exists() or labels_path.stat().st_size == 0:
        return
    with open(labels_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return
        rows = list(reader)
    current = GoldenLabel.fieldnames()
    if header == current:
        needs_pad = any(len(r) != len(current) for r in rows)
        if not needs_pad:
            return
        fixed_rows = []
        for r in rows:
            if len(r) == len(LEGACY_FIELDNAMES):
                fixed_rows.append(r + ["", "", ""])
            elif len(r) == len(current):
                fixed_rows.append(r)
            else:
                raise ValueError(
                    f"refusing to migrate {labels_path}: row has {len(r)} "
                    f"fields, expected 14 or 17 (candidate={r[0] if r else '?'})")
        tmp = labels_path.with_suffix(".tmp")
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL,
                           lineterminator="\n", doublequote=True)
            w.writerow(current)
            w.writerows(fixed_rows)
        tmp.replace(labels_path)
        return
    if header == LEGACY_FIELDNAMES:
        fixed_rows = []
        for r in rows:
            if len(r) == len(LEGACY_FIELDNAMES):
                fixed_rows.append(r + ["", "", ""])
            elif len(r) == len(current):
                fixed_rows.append(r)
            else:
                raise ValueError(
                    f"refusing to migrate {labels_path}: row has {len(r)} "
                    f"fields, expected 14 or 17 (candidate={r[0] if r else '?'})")
        tmp = labels_path.with_suffix(".tmp")
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL,
                           lineterminator="\n", doublequote=True)
            w.writerow(current)
            w.writerows(fixed_rows)
        tmp.replace(labels_path)
        return
    raise ValueError(f"unknown labels header in {labels_path}: {header}")


# ---------- pure helpers (unit-tested) ----------

def progress_counts(cand: pd.DataFrame, labels_path: Path,
                    annotator: str) -> Tuple[int, int, int]:
    """(total, completed_by_annotator, remaining)."""
    done: Set[str] = set()
    if labels_path.exists():
        ensure_labels_schema(labels_path)
        d = pd.read_csv(labels_path, keep_default_na=False)
        done = set(d[d.annotator == annotator].candidate_id)
    total = len(cand)
    completed = len(done & set(cand.candidate_id))
    return total, completed, total - completed


def load_done(labels_path: Path) -> Set[Tuple[str, str]]:
    if not labels_path.exists():
        return set()
    ensure_labels_schema(labels_path)
    d = pd.read_csv(labels_path, keep_default_na=False)
    return set(zip(d["candidate_id"], d["annotator"]))


def next_todo(cand: pd.DataFrame, done: Set[Tuple[str, str]],
               annotator: str, seed: int, limit: int) -> pd.DataFrame:
    todo = cand[~cand.candidate_id.isin(
        {c for c, a in done if a == annotator})]
    todo = todo.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return todo.head(limit) if limit else todo


def load_review_order() -> List[str] | None:
    """Deterministic P1->P5 queue order if the review queue exists."""
    if not REVIEW_QUEUE.exists():
        return None
    order: List[str] = []
    with open(REVIEW_QUEUE, "r", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("candidate_id"):
                order.append(r["candidate_id"])
    return order or None


def load_draft_map() -> Dict[str, Dict[str, str]]:
    """candidate_id -> draft recommendation (read-only assistance)."""
    if not REVIEW_DRAFT.exists():
        return {}
    out: Dict[str, Dict[str, str]] = {}
    with open(REVIEW_DRAFT, "r", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["candidate_id"]] = r
    return out


def order_todo_by_review_queue(todo: pd.DataFrame,
                               order: List[str] | None) -> pd.DataFrame:
    """Reorder todo to follow the review queue; unknown IDs go last."""
    if not order:
        return todo
    rank = {cid: i for i, cid in enumerate(order)}
    tmp = todo.copy()
    tmp["_qrank"] = tmp.candidate_id.map(lambda c: rank.get(c, 10**9))
    tmp = tmp.sort_values(["_qrank", "candidate_id"]).drop(columns=["_qrank"])
    return tmp.reset_index(drop=True)


def append_record(labels_path: Path, lab: GoldenLabel) -> None:
    ensure_labels_schema(labels_path)
    first_write = (not labels_path.exists()
                   or labels_path.stat().st_size == 0)
    with open(labels_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=GoldenLabel.fieldnames(),
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\n",
                           doublequote=True, extrasaction="raise")
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


def parse_draft_flag(v: str) -> bool:
    """Parse draft 'true'/'false' or 'yes'/'no' to bool (pure, unit-tested)."""
    return str(v).strip().lower() in ("true", "yes", "1", "y")


def parse_draft_entities(v: str) -> list:
    """Draft entities are '0'/'' for none; otherwise JSON list (pure)."""
    s = (v or "").strip()
    if s in ("", "0", "[]"):
        return []
    try:
        val = json.loads(s)
        return val if isinstance(val, list) else []
    except Exception:
        return []


def build_accepted_label(candidate_id: str, annotator: str,
                         draft: Dict[str, str],
                         suggestion: Suggestion) -> GoldenLabel:
    """A-path: copy draft recommendation into a human label (pure, unit-tested).

    Provenance: model_suggestion=suggestion.family; outcome accepted iff the
    accepted intent equals the suggestion, else corrected. generated_at from
    the draft is NOT reused; annotated_at is fresh human-save time.
    Does NOT touch annotation_draft.csv.
    """
    intent_id = (draft.get("suggested_intent_id") or suggestion.family).strip(
        ).replace(" ", "_").lower()
    intent_name = draft.get("suggested_intent_name") or suggestion.display_name
    final = intent_id
    outcome = "accepted" if final == suggestion.family else "corrected"
    # Uncertain drafts accepted via A still record an auditable outcome:
    # keep corrected/accepted mapping above; U-path uses 'uncertain' instead.
    return record_to_label(
        candidate_id, annotator, intent_id, intent_name,
        draft.get("primary_goal", ""),
        parse_draft_entities(draft.get("entities", "0")),
        draft.get("routing_expectation", "unsure") or "unsure",
        draft.get("escalation_reason", "") or "",
        draft.get("response_requirements", "") or "",
        parse_draft_flag(draft.get("ambiguity", "false")),
        parse_draft_flag(draft.get("ood", "false")),
        draft.get("taxonomy_verdict", "fits") or "fits",
        draft.get("taxonomy_notes", "") or "",
        parse_draft_flag(draft.get("needs_second_opinion", "no")),
        suggestion, outcome)


def _menu_default_key(options: List[Tuple[str, str]], value: str,
                      fallback: str) -> str:
    for k, v in options:
        if v == value:
            return k
    return fallback


def print_final_review(lab: GoldenLabel) -> None:
    print("FINAL REVIEW (human verification of model recommendation):")
    print(f"  intent: {lab.intent_id} ({lab.intent_name})")
    print(f"  goal: {lab.primary_goal[:220]}")
    print(f"  routing: {lab.routing_expectation} "
          f"ambiguity={lab.ambiguity} ood={lab.ood} "
          f"verdict={lab.taxonomy_verdict} second={lab.needs_second_opinion}")
    print(f"  provenance: suggestion={lab.model_suggestion} "
          f"outcome={lab.suggestion_outcome} (accepted by human on save)")


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
    review_order = load_review_order()
    draft_map = load_draft_map()
    if review_order is not None:
        todo = order_todo_by_review_queue(todo, review_order)
        print(f"Review queue: {REVIEW_QUEUE.name} (P1 easy first, P5 careful last)")
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
            d = draft_map.get(r["candidate_id"])
            if d:
                print("MODEL RECOMMENDATION (assistance only, NOT ground truth):")
                print(f"  intent: {d['suggested_intent_id']} "
                      f"confidence={d['confidence']} routing={d['routing_expectation']} "
                      f"ambiguity={d['ambiguity']} ood={d['ood']} "
                      f"taxonomy={d['taxonomy_verdict']} second={d['needs_second_opinion']}")
                print(f"  WHY: {d['why'][:400]}")
                print(f"  ALTERNATIVES: {d['alternatives'][:300]}")
                print("  HUMAN DECISION: [use A/C/N/U menus below; you must save explicitly]")
            choice = ask_menu("Your decision  [A=accept recommendation, C=correct, N=new, U=uncertain]", [("A", "Accept suggestion (you reviewed & confirm)"),
                                                ("C", "Choose existing intent"),
                                                ("N", "New intent (justify)"),
                                                ("U", "Uncertain / context-dependent")], "A")
            # map menu value back to letter
            choice = {"Accept suggestion (you reviewed & confirm)": "A",
                      "Choose existing intent": "C",
                      "New intent (justify)": "N",
                      "Uncertain / context-dependent": "U"}[choice]
            draft = draft_map.get(r["candidate_id"], {})
            if choice == "A":
                # FAST PATH: A = human-verified acceptance of the draft.
                # No retyping; one concise review + explicit Y/n confirmation.
                if draft:
                    lab = build_accepted_label(
                        r["candidate_id"], args.annotator, draft, s)
                else:
                    lab = record_to_label(
                        r["candidate_id"], args.annotator, s.family,
                        s.display_name,
                        f"Accepted suggestion {s.family}", [], "unsure",
                        "", "", False, False, "fits", "", False, s,
                        derive_outcome("A", s.family, s))
                print_final_review(lab)
                errs = lab.validate()
                if errs:
                    print("INVALID draft-derived label (fix via C/U/N on rerun): "
                          + "; ".join(errs))
                    continue
                if not ask_yes_no("Save this human decision?", "y"):
                    print("  discarded, moving on (re-run to relabel this item)");
                    continue
                append_record(labels_path, lab)
                done.add((r["candidate_id"], args.annotator))
                saved += 1
                print(f"saved ({saved} this session)")
                continue
            if choice == "C":
                intent_id, intent_name = choose_existing(catalog, coined)
                dflt_verdict = _menu_default_key(
                    VERDICT_MENU, draft.get("taxonomy_verdict", "fits"), "1")
                verdict = ask_menu("taxonomy_verdict", VERDICT_MENU, dflt_verdict)
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
            # Correction/uncertain paths: prefill from draft so Enter keeps values.
            primary_goal = ask("primary_goal (WHAT does the customer want?)",
                               draft.get("primary_goal", ""))
            dflt_routing = _menu_default_key(
                ROUTING_MENU, draft.get("routing_expectation", "unsure"), "4")
            routing = ask_menu("routing_expectation", ROUTING_MENU, dflt_routing)
            esc_reason, resp_req = "", ""
            if routing == "escalate":
                esc_reason = ask("escalation_reason (REQUIRED for escalate)",
                                 draft.get("escalation_reason", ""))
                while not esc_reason.strip():
                    print("  escalation_reason is required for ESCALATE");
                    esc_reason = ask("escalation_reason (REQUIRED for escalate)")
                resp_req = ask("response_requirements (blank ok)",
                               draft.get("response_requirements", ""))
            elif routing == "clarify":
                resp_req = ask("clarification rationale/requirements (REQUIRED for clarify)",
                               draft.get("response_requirements", ""))
                while not resp_req.strip():
                    print("  a concise clarification rationale is required for CLARIFY");
                    resp_req = ask("clarification rationale/requirements (REQUIRED for clarify)")
                esc_reason = ask("escalation_reason (blank ok)", "")
            else:
                if routing == "auto_ok":
                    print("  (escalation_reason defaults to blank for AUTO)")
                esc_reason = ask("escalation_reason (blank ok)", "")
                resp_req = ask("response_requirements (blank ok)",
                               draft.get("response_requirements", ""))
            ambiguity = ask_yes_no(
                "ambiguity?",
                "y" if parse_draft_flag(draft.get("ambiguity", "false")) else "n")
            ood = ask_yes_no(
                "ood?",
                "y" if parse_draft_flag(draft.get("ood", "false")) else "n")
            notes = ""
            if choice == "N" or verdict == "new_intent":
                notes = ask("taxonomy_notes (REQUIRED: describe the proposal)",
                            draft.get("taxonomy_notes", ""))
                while not notes.strip():
                    print("  taxonomy_notes required for new_intent");
                    notes = ask("taxonomy_notes (REQUIRED: describe the proposal)")
            elif ood:
                notes = ask("taxonomy_notes (REQUIRED: OOD explanation)",
                            draft.get("taxonomy_notes", ""))
                while not notes.strip():
                    print("  OOD requires a taxonomy_notes explanation");
                    notes = ask("taxonomy_notes (REQUIRED: OOD explanation)")
                verdict = "ood"
            else:
                notes = ask("taxonomy_notes (blank ok)",
                            draft.get("taxonomy_notes", ""))
            if ood and verdict != "ood":
                print("  (verdict forced to 'ood' because ood=true)");
                verdict = "ood"
            second = ask_yes_no(
                "needs_second_opinion?",
                "y" if parse_draft_flag(draft.get("needs_second_opinion", "no")) else "n")
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
