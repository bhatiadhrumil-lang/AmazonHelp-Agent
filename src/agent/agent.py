"""Agent orchestrator (Phase 2, TASK 13 + TASK 14).

Flow: context -> intent -> entities -> retrieval -> assessment -> routing
-> response (draft for AUTO/CLARIFY, safe-handoff text for ESCALATE).

Safe-failure rules (TASK 14): ANY component exception -> ESCALATE with the
error class recorded; empty input, no hits, weak/conflicting evidence route
to CLARIFY/ESCALATE per router policy — never a hallucinated answer. Trace
holds structured metadata only, never chain-of-thought.
"""
from __future__ import annotations

from typing import List, Optional

from agent.context import ContextBuilder, ContextConfig
from agent.contracts import (AgentResult, ConversationTurn, EvidenceAssessment,
                             HistoricalEvidence, IncomingMessage,
                             IntentPrediction, ResponseDraft, RoutingDecision)
from agent.entities import EntityExtractor, ProvisionalPatternExtractor
from agent.evidence import AssessConfig, EvidenceAssessor
from agent.intent import IntentClassifier, ProvisionalClusterAdapter
from agent.respond import ResponseGenerator, StubGenerator
from agent.retrieval import RetrievalConfig, Retriever
from agent.router import DecisionRouter, RouterPolicy


def _safe_escalate(message: IncomingMessage, context, reason: str,
                   err: Optional[str] = None) -> AgentResult:
    trace: dict = {"failed_safe": True, "reason": reason}
    if err:
        trace["error_class"] = err
    intent = IntentPrediction(intent_id="unknown_error", confidence=0.0,
                              source="orchestrator-guard", is_provisional=True,
                              explanation=reason)
    from agent.contracts import EntitySet
    assessment = EvidenceAssessment(
        sufficient=False, confidence=0.0, missing_information=[reason],
        risk_flags=["orchestrator_guard"], reason=reason)
    routing = RoutingDecision(decision="ESCALATE", reason=reason,
                              risk_flags=["orchestrator_guard"],
                              evidence_sufficient=False)
    draft = ResponseDraft(
        text=("Something went wrong on our side, so I'm handing this to a "
              "human specialist rather than guessing. Sorry for the trouble."),
        grounded=False, provider="orchestrator-guard")
    return AgentResult(incoming=message, context=context, intent=intent,
                       entities=EntitySet(), evidence=[], assessment=assessment,
                       routing=routing, draft=draft, trace=trace)


class SupportAgent:
    """Main agent service. Swap components via constructor (all provisional)."""

    def __init__(self,
                 retriever: Retriever,
                 intent: Optional[IntentClassifier] = None,
                 entities: Optional[EntityExtractor] = None,
                 assessor: Optional[EvidenceAssessor] = None,
                 router: Optional[DecisionRouter] = None,
                 responder: Optional[ResponseGenerator] = None,
                 contexts: Optional[ContextBuilder] = None):
        self.retriever = retriever
        self.intent = intent or ProvisionalClusterAdapter()
        self.entities = entities or ProvisionalPatternExtractor()
        self.assessor = assessor or EvidenceAssessor()
        self.router = router or DecisionRouter()
        self.responder = responder or StubGenerator()
        self.contexts = contexts or ContextBuilder()

    def run(self, message: IncomingMessage,
            conversation_id: Optional[str] = None,
            prior_customer_texts: Optional[List[str]] = None,
            full_thread: Optional[List[ConversationTurn]] = None,
            top_k: Optional[int] = None) -> AgentResult:
        trace: dict = {"components": {}}
        try:
            context = self.contexts.build(
                message, conversation_id, prior_customer_texts, full_thread)
        except Exception as e:  # noqa: BLE001 - guard must not throw
            return _safe_escalate(message, None, "context build failed",
                                  type(e).__name__)
        try:
            from agent.context import ContextBuilder as CB
            intent = self.intent.predict(context)
            trace["components"]["intent"] = {
                "source": intent.source, "intent": intent.intent_id,
                "provisional": intent.is_provisional}
            ents = self.entities.extract(context)
            trace["components"]["entities"] = [e.type for e in ents.entities]
            hits = self.retriever.search(CB.intent_text(context), top_k=top_k)
            trace["components"]["retrieval"] = {
                "n_hits": len(hits),
                "top_sim": round(hits[0].similarity, 3) if hits else 0.0}
            assessment = self.assessor.assess(
                context.current_message.text, intent, ents, hits)
            routing = self.router.route(context, intent, ents, hits, assessment)
            trace["components"]["routing"] = routing.decision
            if routing.decision == "ESCALATE":
                draft = ResponseDraft(
                    text=(f"I don't have enough verified information to "
                          f"resolve this safely ({routing.reason}). A human "
                          f"specialist will take it from here."),
                    grounded=False, provider="orchestrator-handoff")
            else:
                draft = self.responder.generate(
                    context, intent, ents, hits, assessment)
            trace["policy"] = {
                "assess": self.assessor.config.version,
                "router": self.router.policy.version}
            from agent.contracts import AgentResult as AR
            return AR(incoming=message, context=context, intent=intent,
                      entities=ents,
                      evidence=[HistoricalEvidence(
                          source_message_id=h.case.customer_message_id,
                          conversation_id=h.case.conversation_id,
                          customer_text=h.case.customer_text,
                          historical_response=h.case.response_text,
                          similarity=round(h.similarity, 4),
                          metadata=h.case.metadata) for h in hits],
                      assessment=assessment, routing=routing, draft=draft,
                      trace=trace)
        except Exception as e:  # noqa: BLE001
            return _safe_escalate(message, context, "pipeline failure",
                                  type(e).__name__)
