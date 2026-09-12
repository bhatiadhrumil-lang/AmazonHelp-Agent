"""Response generation interface + safe stub (Phase 2, TASK 11).

`ResponseGenerator` is the stable provider-independent interface. `StubGenerator`
is the ONLY implementation in this phase: templated, grounded-only, refuses
when evidence is insufficient. It never invents policy, capability, or facts.

To plug a real LLM provider later: implement `ResponseGenerator.generate`
with the same signature, set `provider` name, keep the grounding contract
(every factual claim traces to inputs/evidence; else grounded=False).
"""
from __future__ import annotations

from typing import List, Optional

from agent.contracts import (ConversationContext, EntitySet, EvidenceAssessment,
                             IntentPrediction, ResponseDraft)
from agent.retrieval import RetrievalHit


class ResponseGenerator:
    provider: str = "base"

    def generate(self, context: ConversationContext, intent: IntentPrediction,
                 entities: EntitySet, hits: List[RetrievalHit],
                 assessment: EvidenceAssessment) -> ResponseDraft:
        raise NotImplementedError


class StubGenerator(ResponseGenerator):
    """Safe templated stub. Grounded exclusively in retrieved evidence."""

    provider = "stub-v0"

    def generate(self, context: ConversationContext, intent: IntentPrediction,
                 entities: EntitySet, hits: List[RetrievalHit],
                 assessment: EvidenceAssessment) -> ResponseDraft:
        if not assessment.sufficient or not hits:
            return ResponseDraft(
                text=("I don't have enough verified information to resolve "
                      "this safely. I've flagged your message for a human "
                      "support specialist who can help further."),
                supporting_evidence_ids=[], grounded=False, provider=self.provider)
        usable = [h for h in hits
                  if h.case.customer_message_id in assessment.supporting_case_ids
                  and h.case.response_text.strip()][:3]
        if not usable:
            return ResponseDraft(
                text=("I found related past cases but none with a usable "
                      "recorded response, so I can't draft a grounded reply. "
                      "A human specialist will follow up."),
                supporting_evidence_ids=[], grounded=False, provider=self.provider)
        ids = [h.case.customer_message_id for h in usable]
        excerpt = usable[0].case.response_text.strip().replace("\n", " ")[:280]
        return ResponseDraft(
            text=(f"Based on {len(usable)} similar past case(s) handled by "
                  f"support (provisional intent: {intent.intent_id}): "
                  f"a previous support reply in a similar situation said: "
                  f"\"{excerpt}\" "
                  f"[PROVISIONAL DRAFT — verify before sending; "
                  f"evidence: {', '.join(ids)}]"),
            supporting_evidence_ids=ids, grounded=True, provider=self.provider)
