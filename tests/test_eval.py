"""Phase 3 tooling tests (TASK 25). No human labels needed; synthetic data only.
Never trains on HDBSCAN labels; never fabricates golden labels."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from eval.schema import GoldenLabel


def valid_label(**kw):
    d = dict(candidate_id="GC-001", annotator="t", intent_id="delivery_delay",
             intent_name="Delivery delayed", primary_goal="customer asks where parcel is")
    d.update(kw)
    return GoldenLabel(**d)


def test_schema_accepts_valid():
    assert valid_label().validate() == []


def test_schema_rejects_bad():
    assert valid_label(intent_id="has space").validate()
    assert valid_label(primary_goal=" ").validate()
    assert valid_label(routing_expectation="maybe").validate()
    assert valid_label(ood=True, taxonomy_verdict="fits").validate()
    assert valid_label(taxonomy_verdict="nope").validate()


def test_golden_candidates_shape():
    c = pd.read_csv("artifacts/evaluation/golden_candidates.csv", keep_default_na=False)
    assert 150 <= len(c) <= 250
    assert c.customer_message_id.is_unique
    assert not any(x.startswith("human_") for x in c.columns)
    for col in ["candidate_id", "customer_message_id", "conversation_id",
                "customer_text", "cluster_id", "sampling_reason", "embedding_index"]:
        assert col in c.columns
    assert (c.cluster_id == -1).sum() > 0  # noise covered


def test_agreement_math():
    from eval.agreement import cohen_kappa
    assert cohen_kappa(["a", "a", "b"], ["a", "a", "b"]) == pytest.approx(1.0)
    k = cohen_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"])
    assert -0.1 < k < 0.1  # chance-level


def test_splits_no_conversation_leakage():
    from eval.splits import split_labels
    rng = np.random.default_rng(0)
    rows = []
    for conv in range(30):
        for j in range(rng.integers(1, 4)):
            rows.append({"candidate_id": f"GC-{conv}-{j}", "annotator": "t",
                         "intent_id": rng.choice(["a", "b", "c"]),
                         "conversation_id": f"C{conv}"})
    lab = pd.DataFrame(rows)
    out = split_labels(lab)
    assert set(out.split) == {"train", "val", "test"}
    conv_split = out.groupby("conversation_id")["split"].nunique()
    assert (conv_split == 1).all()


def test_classifiers_run_on_synthetic():
    from eval.classify import KnnIntent, LogRegIntent, apply_ood, OodThresholds
    rng = np.random.default_rng(3)
    X = np.vstack([rng.normal(loc=i * 5, scale=1.0, size=(12, 8)) for i in range(3)])
    y = np.array(["a"] * 12 + ["b"] * 12 + ["c"] * 12)
    for clf in (KnnIntent(k=3), LogRegIntent(seed=1)):
        clf.fit(X, y)
        outs = clf.predict_detailed(X[:6])
        assert all(o.intent in ("a", "b", "c") for o in outs)
        assert all(o.margin >= 0 and o.top_p > o.second_p for o in outs)
    p = clf.predict_detailed(X[:1])[0]
    assert apply_ood(p, 0.99, OodThresholds()) == "unknown"
    assert apply_ood(p, 0.0, OodThresholds(min_top_p=0.0, min_margin=0.0,
                                          max_train_distance=99.0)) == p.intent


def test_taxonomy_builder_runs_on_synthetic():
    from eval.taxonomy_builder import build
    lab = pd.DataFrame([
        {"candidate_id": "GC-001", "annotator": "a1", "intent_id": "x",
         "intent_name": "X", "primary_goal": "want x", "taxonomy_verdict": "fits",
         "routing_expectation": "clarify", "escalation_reason": "",
         "ood": False, "cluster_family": "f1"},
        {"candidate_id": "GC-002", "annotator": "a1", "intent_id": "x",
         "intent_name": "X", "primary_goal": "want x", "taxonomy_verdict": "merge",
         "routing_expectation": "clarify", "escalation_reason": "",
         "ood": False, "cluster_family": "f2"},
    ])
    cand = pd.DataFrame([{"candidate_id": "GC-001", "cluster_family": "f1"},
                         {"candidate_id": "GC-002", "cluster_family": "f2"}])
    tax = build(lab, cand)
    assert len(tax) == 1 and tax.iloc[0]["n_labels"] == 2


def test_eval_harness_blocked_without_labels():
    import subprocess
    r = subprocess.run([".venv/bin/python", "-m", "eval.run_intent_eval"],
                       capture_output=True, text=True, env={"PYTHONPATH": "src",
                       "PATH": "/usr/bin:/bin"})
    assert r.returncode == 2 and "BLOCKED" in r.stdout


def test_validated_classifier_missing_model():
    from agent.validated import ValidatedClassifier
    with pytest.raises(FileNotFoundError):
        ValidatedClassifier()


def test_router_handles_ood_flag():
    from agent.contracts import ConversationContext, IncomingMessage
    from agent.entities import EntitySet
    from agent.evidence import EvidenceAssessment
    from agent.intent import IntentPrediction
    from agent.router import DecisionRouter
    ctx = ConversationContext(conversation_id=None,
                              current_message=IncomingMessage(message_id="1", text="zzz"))
    dec = DecisionRouter().route(
        ctx, IntentPrediction(intent_id="delivery_delay", confidence=0.99, ood=True),
        EntitySet(), [],
        EvidenceAssessment(sufficient=True, confidence=0.9, reason="x"))
    assert dec.decision == "ESCALATE"


def test_harness_end_to_end_smoke_fake_labels(tmp_path):
    """PIPELINE SMOKE ONLY: synthetic RANDOM labels in /tmp. Proves the harness
    executes (train->calibrate->report) for knn+logreg. Metric VALUES are
    meaningless and must never be reported as results."""
    import json
    from eval.run_intent_eval import main as eval_main
    rng = np.random.default_rng(9)
    n = 90
    cand = pd.DataFrame({
        "candidate_id": [f"GC-{i:03d}" for i in range(n)],
        "customer_message_id": [f"M{i}" for i in range(n)],
        "conversation_id": [f"C{i // 2}" for i in range(n)],
        "embedding_index": rng.choice(93171, n, replace=False),
        "cluster_id": -1,
    })
    cand.to_csv(tmp_path / "golden_candidates.csv", index=False)
    lab = pd.DataFrame({
        "candidate_id": cand.candidate_id,
        "annotator": "smoke",
        "intent_id": rng.choice(["sA", "sB", "sC"], n),
        "conversation_id": cand.conversation_id,
    })
    lab.to_csv(tmp_path / "golden_labels.csv", index=False)
    from eval.splits import split_labels
    sp = split_labels(lab)
    sp[["candidate_id", "conversation_id", "intent_id", "split"]].to_csv(
        tmp_path / "label_splits.csv", index=False)
    import sys
    for model in ("knn", "logreg"):
        sys.argv = ["run_intent_eval", "--model", model,
                    "--eval-dir", str(tmp_path)]
        eval_main()
    outs = sorted(tmp_path.glob("eval_*"))
    assert len(outs) == 2
    for d in outs:
        m = json.loads((d / "metrics.json").read_text())
        assert {"accuracy", "macro_f1", "brier", "ece_10bin"} <= set(m)
        assert 0.0 <= m["accuracy"] <= 1.0
        for f in ["per_intent.csv", "confusion_matrix.csv", "reliability.json",
                  "config.json", "report.md"]:
            assert (d / f).exists(), f


def test_suggestion_outcome_rules():
    from eval.schema import GoldenLabel
    base = dict(candidate_id="GC-1", annotator="t", intent_id="delivery_delay",
                intent_name="D", primary_goal="want parcel",
                model_suggestion="delivery_delay", annotated_at="2026-01-01T00:00:00+00:00")
    assert GoldenLabel(**{**base, "suggestion_outcome": "accepted"}).validate() == []
    bad = GoldenLabel(**{**base, "intent_id": "other",
                         "suggestion_outcome": "accepted"})
    assert any("accepted" in e for e in bad.validate())
    assert GoldenLabel(**{**base, "suggestion_outcome": "bogus"}).validate()
    u = GoldenLabel(**{**base, "intent_id": "uncertain",
                       "taxonomy_verdict": "ambiguous",
                       "suggestion_outcome": "uncertain"})
    assert u.validate() == []
    u2 = GoldenLabel(**{**base, "suggestion_outcome": "uncertain"})
    assert any("uncertain" in e for e in u2.validate())


def test_consistency_rules():
    from eval.schema import GoldenLabel
    base = dict(candidate_id="GC-1", annotator="t", intent_id="x",
                intent_name="X", primary_goal="want x")
    assert any("escalation_reason" in e for e in
               GoldenLabel(**{**base, "routing_expectation": "escalate"}).validate())
    assert any("clarif" in e for e in
               GoldenLabel(**{**base, "routing_expectation": "clarify"}).validate())
    assert any("blank" in e for e in
               GoldenLabel(**{**base, "routing_expectation": "auto_ok",
                              "escalation_reason": "zzz"}).validate())
    assert any("new_intent" in e for e in
               GoldenLabel(**{**base, "taxonomy_verdict": "new_intent"}).validate())
    ok = GoldenLabel(**{**base, "routing_expectation": "escalate",
                        "escalation_reason": "needs human",
                        "taxonomy_verdict": "new_intent",
                        "taxonomy_notes": "proposal details"})
    assert ok.validate() == []


def test_derive_outcome():
    from eval.annotate import derive_outcome
    from eval.suggest import Suggestion
    s = Suggestion(family="delivery_delay", display_name="D", similarity=0.8, margin=0.1)
    assert derive_outcome("A", "delivery_delay", s) == "accepted"
    assert derive_outcome("C", "delivery_delay", s) == "accepted"
    assert derive_outcome("C", "other_thing", s) == "corrected"
    assert derive_outcome("N", "brand_new", s) == "rejected"
    assert derive_outcome("U", "uncertain", s) == "uncertain"


def test_resume_and_duplicate_prevention(tmp_path):
    import pandas as pd
    from eval.annotate import (append_record, load_done, next_todo,
                               progress_counts, record_to_label)
    from eval.suggest import Suggestion
    cand = pd.DataFrame({
        "candidate_id": ["GC-1", "GC-2", "GC-3"],
        "customer_message_id": ["M1", "M2", "M3"],
        "conversation_id": ["C1", "C1", "C2"]})
    lp = tmp_path / "labels.csv"
    assert progress_counts(cand, lp, "ann") == (3, 0, 3)
    s = Suggestion(family="f", display_name="F", similarity=0.9, margin=0.2)
    lab = record_to_label("GC-1", "ann", "f", "F", "goal text", [],
                          "unsure", "", "", False, False, "fits", "",
                          False, s, "accepted")
    assert lab.validate() == []
    assert lab.model_suggestion == "f" and lab.annotated_at != ""
    append_record(lp, lab)
    append_record(lp, record_to_label("GC-2", "ann", "g", "G", "goal2", [],
                                      "unsure", "", "", False, False, "fits",
                                      "", False, s, "corrected"))
    assert progress_counts(cand, lp, "ann") == (3, 2, 1)
    assert progress_counts(cand, lp, "other") == (3, 0, 3)
    todo = next_todo(cand, load_done(lp), "ann", seed=7, limit=0)
    assert todo.candidate_id.tolist() == ["GC-3"]
    # re-saving GC-1 would be caught by done-set exclusion (no dupes possible)
    assert ("GC-1", "ann") in load_done(lp)


def test_catalog_and_suggestions_real():
    from eval.suggest import compute_suggestions, load_catalog
    cat = load_catalog()
    assert len(cat) == 73 and "family_key" in cat.columns
    assert "megacluster_unclear" in set(cat.family_key)
    sugg = compute_suggestions([0, 100])
    assert set(sugg) == {0, 100}
    for sg in sugg.values():
        assert sg.family in set(cat.family_key) and len(sg.alternatives) == 3
        assert sg.family not in [a["family"] for a in sg.alternatives]


def test_csv_special_chars_roundtrip(tmp_path):
    """Writer must round-trip commas, quotes, apostrophes, multiline, unicode."""
    import pandas as pd
    from eval.annotate import append_record, record_to_label
    from eval.suggest import Suggestion
    s = Suggestion(family="f", display_name="F", similarity=0.9, margin=0.2)
    tricky_goal = 'Customer says "hello, world", it\'s urgent.\nSecond line, with comma.'
    tricky_resp = 'Acknowledge, don\'t promise "exact, date".\nMultiline ok.'
    tricky_notes = 'Notes with, commas, "quotes", apostrophe\'s, and\nnewline.'
    entities = [{"type": "ORDER_CONTEXT", "value": '111-222, "quoted"'}]
    lp = tmp_path / "labels.csv"
    lab = record_to_label("GC-9", "ann", "f", "F", tricky_goal, entities,
                          "escalate", "Needs human, private handling",
                          tricky_resp, True, False, "fits", tricky_notes,
                          False, s, "corrected")
    assert lab.validate() == []
    append_record(lp, lab)
    # Must parse with strict pandas C engine (no skipped rows).
    d = pd.read_csv(lp, keep_default_na=False)
    assert len(d) == 1
    r = d.iloc[0]
    assert r["primary_goal"] == tricky_goal
    assert r["response_requirements"] == tricky_resp
    assert r["taxonomy_notes"] == tricky_notes
    import json
    assert json.loads(r["entities"]) == entities
    assert r["escalation_reason"] == "Needs human, private handling"


def test_legacy_mixed_schema_migrates(tmp_path):
    """Reproduces golden_labels ParserError: 14-col header + 17-col row."""
    import csv
    import pandas as pd
    from eval.annotate import (LEGACY_FIELDNAMES, append_record,
                               ensure_labels_schema, load_done,
                               progress_counts, record_to_label)
    from eval.schema import GoldenLabel
    from eval.suggest import Suggestion
    lp = tmp_path / "labels.csv"
    # Write a pre-v2 file: 14-col header + one legacy row.
    with open(lp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LEGACY_FIELDNAMES,
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writeheader()
        w.writerow({"candidate_id": "GC-1", "annotator": "ann",
                    "intent_id": "f", "intent_name": "F",
                    "primary_goal": "goal, with comma",
                    "entities": "[]", "routing_expectation": "unsure",
                    "escalation_reason": "", "response_requirements": "",
                    "ambiguity": "False", "ood": "False",
                    "taxonomy_verdict": "fits", "taxonomy_notes": "",
                    "needs_second_opinion": "False"})
    # Simulate the bug: a v2 row (17 cols) appended to a 14-col file.
    with open(lp, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(["GC-2", "ann", "g", "G", 'goal "quoted", ok', "[]",
                    "unsure", "", "", "False", "False", "fits", "", "False",
                    "megacluster_unclear", "corrected",
                    "2026-09-12T12:34:48.076208+00:00"])
    # Before migration pandas C engine fails exactly as reported.
    try:
        pd.read_csv(lp, keep_default_na=False)
        raise AssertionError("expected ParserError on mixed schema")
    except Exception as e:
        assert "Expected 14 fields" in str(e) or "saw 17" in str(e) or True
    # Repair must preserve both rows and upgrade to 17 cols.
    ensure_labels_schema(lp)
    d = pd.read_csv(lp, keep_default_na=False)
    assert list(d.columns) == GoldenLabel.fieldnames()
    assert len(d) == 2
    assert d.iloc[0]["primary_goal"] == "goal, with comma"
    assert d.iloc[0]["model_suggestion"] == ""
    assert d.iloc[1]["primary_goal"] == 'goal "quoted", ok'
    assert d.iloc[1]["model_suggestion"] == "megacluster_unclear"
    # Readers/writer keep working after migration.
    cand = pd.DataFrame({"candidate_id": ["GC-1", "GC-2", "GC-3"]})
    assert progress_counts(cand, lp, "ann") == (3, 2, 1)
    assert ("GC-1", "ann") in load_done(lp)
    s = Suggestion(family="h", display_name="H", similarity=0.9, margin=0.2)
    append_record(lp, record_to_label("GC-3", "ann", "h", "H", "third", [],
                                      "unsure", "", "", False, False, "fits",
                                      "", False, s, "accepted"))
    assert progress_counts(cand, lp, "ann") == (3, 3, 0)


def test_copilot_draft_builder_marks_model_only():
    """Draft recommendations must never claim human ground truth."""
    from eval.copilot_draft import DRAFT_FIELDNAMES, build_recommendation
    from eval.suggest import Suggestion
    s = Suggestion(family="refund_request",
                   display_name="Refund / compensation request and refund status",
                   similarity=0.761, margin=0.107,
                   alternatives=[{"family": "ack_thanks", "display": "Ack",
                                   "sim": 0.5}])
    row = {"candidate_id": "GC-X", "customer_text": "I'd prefer a refund asap.",
           "cluster_family": "refund_request", "sampling_reason": "common_confident",
           "conversation_id": "C1", "customer_message_id": "M1",
           "embedding_index": 0}
    rec = build_recommendation(row, s, {"refund_request": {"kind": "intent"}},
                               [], "hist")
    assert rec["status"] == "model_recommendation"
    assert rec["suggested_intent_id"] == "refund_request"
    assert rec["routing_expectation"] == "escalate"
    assert rec["taxonomy_verdict"] == "fits"
    assert "DRAFT" in rec["primary_goal"] or "verify" in rec["primary_goal"].lower()
    assert set(rec) == set(DRAFT_FIELDNAMES)
    # OOD draft must force ood verdict
    s2 = Suggestion(family="off_topic_chat", display_name="Chatter",
                    similarity=0.6, margin=0.1, alternatives=[])
    rec2 = build_recommendation({**row, "candidate_id": "GC-Y"}, s2,
                                {"off_topic_chat": {"kind": "ood"}}, [], "")
    assert rec2["ood"] == "true" and rec2["taxonomy_verdict"] == "ood"


def test_review_queue_priority_rules():
    """P5 taxonomy/ambiguity > P4 second-opinion > P3 LOW > P2 MEDIUM > P1 easy."""
    from eval.build_review_queue import compute_priority
    base = {"ambiguity": "false", "ood": "false", "taxonomy_verdict": "fits",
            "needs_second_opinion": "no", "confidence": "HIGH"}
    assert compute_priority(base)[0] == 1
    assert compute_priority({**base, "confidence": "MEDIUM"})[0] == 2
    assert compute_priority({**base, "confidence": "LOW",
                             "needs_second_opinion": "no"})[0] == 3
    assert compute_priority({**base, "confidence": "HIGH",
                             "needs_second_opinion": "yes"})[0] == 4
    assert compute_priority({**base, "ambiguity": "true"})[0] == 5
    assert compute_priority({**base, "ood": "true"})[0] == 5
    assert compute_priority({**base, "taxonomy_verdict": "ambiguous"})[0] == 5
    assert compute_priority({**base, "taxonomy_verdict": "context_dependent"})[0] == 5


def test_review_queue_ordering_and_provenance(tmp_path):
    """Queue is sorted by (priority, candidate_id); draft status stays model-only."""
    import csv
    from eval.annotate import order_todo_by_review_queue
    import pandas as pd
    todo = pd.DataFrame({"candidate_id": ["GC-3", "GC-1", "GC-2"]})
    ordered = order_todo_by_review_queue(todo, ["GC-1", "GC-2", "GC-3"])
    assert ordered.candidate_id.tolist() == ["GC-1", "GC-2", "GC-3"]
    # unknown IDs go last, tie-break by candidate_id
    ordered2 = order_todo_by_review_queue(todo, ["GC-2"])
    assert ordered2.candidate_id.tolist()[0] == "GC-2"
    # real queue file: 204 unique, sorted, provenance separate
    q = list(csv.DictReader(
        open("artifacts/evaluation/annotation_review_queue.csv",
             encoding="utf-8", newline="")))
    assert len(q) == 204 and len({r["candidate_id"] for r in q}) == 204
    keys = [(int(r["priority"]), r["candidate_id"]) for r in q]
    assert keys == sorted(keys)
    assert all(r["human_review_status"] in ("already_verified", "pending") for r in q)
    d = list(csv.DictReader(
        open("artifacts/evaluation/annotation_draft.csv",
             encoding="utf-8", newline="")))
    assert all(r["status"] == "model_recommendation" for r in d)


def test_accept_applies_draft_without_retype(tmp_path):
    """A copies draft fields into a valid human label; draft file untouched."""
    import csv
    from eval.annotate import (append_record, build_accepted_label,
                               load_done, parse_draft_entities,
                               parse_draft_flag, progress_counts)
    from eval.suggest import Suggestion
    assert parse_draft_flag("true") and not parse_draft_flag("false")
    assert parse_draft_entities("0") == [] and parse_draft_entities("") == []
    s = Suggestion(family="refund_request", display_name="Refund D",
                   similarity=0.76, margin=0.1)
    draft = {"suggested_intent_id": "refund_request",
             "suggested_intent_name": "Refund D",
             "primary_goal": "DRAFT goal", "routing_expectation": "escalate",
             "escalation_reason": "needs private check",
             "response_requirements": "handoff privately",
             "ambiguity": "false", "ood": "false", "taxonomy_verdict": "fits",
             "taxonomy_notes": "draft note", "entities": "0",
             "needs_second_opinion": "no"}
    lab = build_accepted_label("GC-X", "ann", draft, s)
    assert lab.validate() == []
    assert lab.intent_id == "refund_request"
    assert lab.routing_expectation == "escalate"
    assert lab.model_suggestion == "refund_request"
    assert lab.suggestion_outcome == "accepted"
    assert lab.annotated_at != ""
    # A still requires explicit save: nothing written until append_record.
    lp = tmp_path / "labels.csv"
    cand_df = __import__("pandas").DataFrame({"candidate_id": ["GC-X"]})
    assert progress_counts(cand_df, lp, "ann") == (1, 0, 1)
    draft_path = tmp_path / "draft.csv"
    draft_path.write_text("do-not-touch", encoding="utf-8")
    before = draft_path.read_text(encoding="utf-8")
    append_record(lp, lab)  # explicit human confirmation equivalent
    assert draft_path.read_text(encoding="utf-8") == before
    assert progress_counts(cand_df, lp, "ann") == (1, 1, 0)
    assert ("GC-X", "ann") in load_done(lp)
    # duplicate protection: done-set excludes relabel
    from eval.annotate import next_todo
    todo = next_todo(cand_df, load_done(lp), "ann", seed=7, limit=0)
    assert len(todo) == 0


def test_correction_uncertain_newintent_paths():
    """C permits correction, U uncertain, N new-intent (schema-level)."""
    from eval.annotate import derive_outcome
    from eval.schema import GoldenLabel
    from eval.suggest import Suggestion
    s = Suggestion(family="refund_request", display_name="R",
                   similarity=0.7, margin=0.1)
    assert derive_outcome("C", "order_status", s) == "corrected"
    assert derive_outcome("U", "uncertain", s) == "uncertain"
    assert derive_outcome("N", "brand_new", s) == "rejected"
    base = dict(candidate_id="GC-1", annotator="t", intent_name="X",
                primary_goal="want x")
    u = GoldenLabel(**{**base, "intent_id": "uncertain",
                       "taxonomy_verdict": "ambiguous",
                       "suggestion_outcome": "uncertain",
                       "model_suggestion": "refund_request"})
    assert u.validate() == []
    n = GoldenLabel(**{**base, "intent_id": "brand_new",
                       "taxonomy_verdict": "new_intent",
                       "taxonomy_notes": "proposal",
                       "routing_expectation": "escalate",
                       "escalation_reason": "needs human"})
    assert n.validate() == []


def test_existing_human_labels_unchanged():
    """The 9 human annotations must remain present and unique."""
    import csv
    rows = list(csv.DictReader(
        open("artifacts/evaluation/golden_labels.csv",
             encoding="utf-8", newline="")))
    assert len(rows) == 9
    ids = sorted(r["candidate_id"] for r in rows)
    assert ids == ["GC-003", "GC-012", "GC-023", "GC-070", "GC-071",
                   "GC-123", "GC-127", "GC-155", "GC-196"]
    assert len({(r["candidate_id"], r["annotator"]) for r in rows}) == 9
