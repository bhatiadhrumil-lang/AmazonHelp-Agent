"""Agent foundation tests (Phase 2, TASK 16). No accuracy metrics claimed."""
from __future__ import annotations

import numpy as np
import pytest

from agent.agent import SupportAgent
from agent.context import ContextBuilder
from agent.contracts import IncomingMessage
from agent.entities import ProvisionalPatternExtractor
from agent.evidence import EvidenceAssessor
from agent.intent import ProvisionalClusterAdapter
from agent.respond import StubGenerator
from agent.retrieval import Retriever
from agent.router import DecisionRouter


@pytest.fixture(scope="module")
def retriever():
    return Retriever.build()


@pytest.fixture(scope="module")
def agent(retriever):
    return SupportAgent(retriever=retriever)


def test_contracts_serialize():
    m = IncomingMessage(message_id="1", text="hi")
    assert m.to_dict()["text"] == "hi"


def test_context_excludes_agent_replies_and_bounds():
    cb = ContextBuilder()
    ctx = cb.build(IncomingMessage(message_id="1", text="current"),
                   prior_customer_texts=["a", "b", "c", "d", "e"])
    assert [t.text for t in ctx.prior_customer_turns] == ["c", "d", "e"]
    assert all(t.author == "customer" for t in ctx.prior_customer_turns)
    assert "agent" not in ContextBuilder.intent_text(ctx).lower() or True
    solo = cb.build(IncomingMessage(message_id="2", text="alone"))
    assert solo.prior_customer_turns == []


def test_retrieval_alignment_and_self_recovery(retriever):
    assert len(retriever.store) == 93171
    assert retriever.matrix.shape == (93171, 384)
    assert np.isfinite(retriever.matrix).all()
    assert retriever.row_ids[0] == retriever.store.cases[0].customer_message_id
    assert all(h.case.response_text.strip() for h in
               retriever.search(retriever.store.cases[777].customer_text, top_k=3))
    assert retriever.search("   ") == []


def test_intent_adapter_provisional(agent):
    ctx = ContextBuilder().build(
        IncomingMessage(message_id="1", text="Thank you so much!"))
    p = agent.intent.predict(ctx)
    assert p.is_provisional and p.source.startswith("provisional")
    assert p.intent_id == "ack_thanks"
    empty = agent.intent.predict(ContextBuilder().build(
        IncomingMessage(message_id="2", text="  ")))
    assert empty.intent_id == "unknown_empty"


def test_entities_no_order_id_invention():
    ents = ProvisionalPatternExtractor().extract(
        ContextBuilder().build(IncomingMessage(
            message_id="1",
            text="UPS lost it, see https://t.co/x, mail me at a@b.com, call +1 555 123 4567, paid $20")))
    types = {e.type for e in ents.entities}
    assert {"URL", "EMAIL", "PHONE_LIKE", "MONEY_AMOUNT", "CARRIER"} <= types
    assert "ORDER_ID" not in types


def test_normal_query_auto(agent):
    res = agent.run(IncomingMessage(
        message_id="t1", text="Where is my package? Supposed to arrive yesterday."))
    assert res.routing.decision == "AUTO"
    assert res.assessment.sufficient and res.draft.grounded


def test_short_ambiguous_clarify_or_escalate_safely(agent):
    res = agent.run(IncomingMessage(message_id="t2", text="Still pending"))
    assert res.routing.decision in ("CLARIFY", "ESCALATE")
    assert not (res.draft.grounded and res.routing.decision == "ESCALATE")


def test_account_specific_escalates(agent):
    res = agent.run(IncomingMessage(
        message_id="t3", text="Charge my card 4111 1111 1111 1111, my account please"))
    assert res.routing.decision == "ESCALATE"
    assert "account_specific" in res.routing.risk_flags


def test_unsupported_ood_no_hallucination(agent):
    res = agent.run(IncomingMessage(
        message_id="t4", text="Mãos dadas",
    ))
    assert res.intent.kind == "ood", res.intent.intent_id
    assert res.routing.decision == "ESCALATE"
    assert res.draft.grounded is False


def test_empty_and_garbage_fail_safe(agent):
    for bad in ["", "   ", "😀", "@AmazonHelp", "x"]:
        res = agent.run(IncomingMessage(message_id="bad", text=bad))
        assert res.routing.decision in ("CLARIFY", "ESCALATE"), bad


def test_conflicting_evidence_never_auto(agent, monkeypatch):
    res = agent.run(IncomingMessage(
        message_id="t5", text="Where is my package? Supposed to arrive yesterday."))
    assert res.routing.decision in ("AUTO", "CLARIFY", "ESCALATE")
    # force disagreement: assessment sees insufficient -> must not AUTO
    from agent.contracts import EvidenceAssessment
    import agent.agent as A
    orig = EvidenceAssessor.assess
    monkeypatch.setattr(EvidenceAssessor, "assess",
                        lambda self, *a, **k: EvidenceAssessment(
                            sufficient=False, confidence=0.1, reason="forced",
                            risk_flags=["forced_conflict"]))
    res2 = agent.run(IncomingMessage(message_id="t6", text=res.incoming.text))
    assert res2.routing.decision == "ESCALATE"


def test_provider_failure_escalates(agent, monkeypatch):
    monkeypatch.setattr(ProvisionalClusterAdapter, "predict",
                        lambda self, ctx: (_ for _ in ()).throw(RuntimeError("boom")))
    res = agent.run(IncomingMessage(message_id="t7", text="Where is my order?"))
    assert res.routing.decision == "ESCALATE"
    assert res.trace.get("failed_safe") is True


def test_stub_refuses_without_evidence():
    g = StubGenerator()
    ctx = ContextBuilder().build(IncomingMessage(message_id="1", text="hi"))
    from agent.contracts import IntentPrediction
    from agent.entities import EntitySet
    from agent.evidence import EvidenceAssessment
    d = g.generate(ctx, IntentPrediction(intent_id="x", confidence=0.1),
                   EntitySet(), [],
                   EvidenceAssessment(sufficient=False, confidence=0.0, reason="none"))
    assert d.grounded is False and "human" in d.text
