"""Decision router (Phase 2, TASK 12): AUTO / CLARIFY / ESCALATE.

Semantics:
- AUTO: enough evidence AND no blocking risk to draft a safe response.
- CLARIFY: a small amount of extra customer info may safely resolve it.
- ESCALATE: the AI should not fully resolve; always carries a reason.

Policy is configurable (`RouterPolicy`, versioned). Cutoffs are explicitly
UNCALIBRATED placeholders — calibration needs evaluation data. Qualitative
safety rules take precedence over any score.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from agent.contracts import (ConversationContext, EntitySet, EvidenceAssessment,
                             IntentPrediction, RoutingDecision)
from agent.retrieval import RetrievalHit


@dataclass
class RouterPolicy:
    # UNCALIBRATED placeholders — wiring only.
    min_evidence_confidence: float = 0.5
    min_top_similarity: float = 0.5
    # Ask for clarification only when the message is this short AND intent unclear.
    clarify_max_chars: int = 60
    unclear_intents: frozenset = frozenset(
        {"unknown_empty", "megacluster_unclear", "off_topic_chat",
         "transitional", "template_affirm", "template_neg"})
    version: str = "v0-uncalibrated"


class DecisionRouter:
    def __init__(self, policy: Optional[RouterPolicy] = None):
        self.policy = policy or RouterPolicy()

    def route(self, context: ConversationContext, intent: IntentPrediction,
              entities: EntitySet, hits: List[RetrievalHit],
              assessment: EvidenceAssessment) -> RoutingDecision:
        p = self.policy
        # 1. Hard safety escalations (never AUTO).
        hard = [f for f in assessment.risk_flags
                if f in ("risky_language", "account_specific")]
        if hard:
            return RoutingDecision(
                decision="ESCALATE",
                reason=f"blocking risk flags: {hard}; needs human/private handling",
                risk_flags=assessment.risk_flags,
                evidence_sufficient=False, policy_version=p.version)
        if not (context.current_message.text or "").strip():
            return RoutingDecision(
                decision="ESCALATE", reason="empty message; nothing to act on",
                risk_flags=["empty_input"], evidence_sufficient=False,
                policy_version=p.version)
        top = max([h.similarity for h in hits], default=0.0)
        # 2. Only kind=="intent" may AUTO. OOD never resolves here —
        #    via taxonomy kind OR the validated classifier's explicit flag.
        if intent.kind == "ood" or intent.ood or intent.intent_id == "unknown":
            return RoutingDecision(
                decision="ESCALATE",
                reason=(f"intent kind=ood ({intent.intent_id}); out of support domain"),
                risk_flags=assessment.risk_flags + ["out_of_domain"],
                evidence_sufficient=False, policy_version=p.version)
        # 3. Artifact/contextual/sentiment intents carry no standalone goal:
        #    even with surface-matching retrieval, ask for the missing context.
        if intent.kind in ("artifact", "contextual", "sentiment") and not assessment.risk_flags:
            if len((context.current_message.text or "").strip()) <= max(p.clarify_max_chars, 120):
                return RoutingDecision(
                    decision="CLARIFY",
                    reason=(f"intent kind={intent.kind} ({intent.intent_id}) has no "
                            f"standalone goal; need thread context"),
                    risk_flags=assessment.risk_flags,
                    evidence_sufficient=False, policy_version=p.version)
        # 2. Weak/unsupported evidence -> ESCALATE (never hallucinate).
        if not assessment.sufficient:
            # 3. Narrow CLARIFY band: short message + unclear intent + no
            #    blocking risk, where one customer detail could resolve it.
            short = len((context.current_message.text or "").strip()) <= p.clarify_max_chars
            if (short and intent.intent_id in p.unclear_intents
                    and not assessment.risk_flags):
                return RoutingDecision(
                    decision="CLARIFY",
                    reason=(f"short ambiguous message (intent={intent.intent_id}); "
                            f"one clarifying customer detail may resolve it"),
                    risk_flags=assessment.risk_flags,
                    evidence_sufficient=False, policy_version=p.version)
            return RoutingDecision(
                decision="ESCALATE", reason=f"insufficient evidence: {assessment.reason}",
                risk_flags=assessment.risk_flags, evidence_sufficient=False,
                policy_version=p.version)
        # 4. AUTO only with sufficient evidence + confidence/mass placeholders met.
        if (assessment.confidence >= p.min_evidence_confidence
                and top >= p.min_top_similarity):
            return RoutingDecision(
                decision="AUTO",
                reason=(f"evidence sufficient ({len(assessment.supporting_case_ids)} cases, "
                        f"top sim={top:.2f}); no blocking risk"),
                risk_flags=assessment.risk_flags, evidence_sufficient=True,
                policy_version=p.version)
        return RoutingDecision(
            decision="ESCALATE",
            reason="evidence marked sufficient but below AUTO placeholders; escalating safely",
            risk_flags=assessment.risk_flags, evidence_sufficient=False,
            policy_version=p.version)
