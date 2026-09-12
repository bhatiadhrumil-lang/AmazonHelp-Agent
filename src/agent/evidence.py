"""Evidence assessment (Phase 2, TASK 10).

Considers: case count, similarity mass, response agreement, direct
applicability signals, account-specific need, risk. Returns
sufficient/insufficient + reason + supporting ids + risk flags.

NO magic production thresholds. `AssessConfig` cutoffs are explicitly named
UNCALIBRATED placeholders for wiring only; calibration requires evaluation
data (future golden set). Qualitative rules dominate: weak/unsupported/
account-specific/risky -> insufficient.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from agent.contracts import EntitySet, EvidenceAssessment, IntentPrediction
from agent.retrieval import RetrievalHit

ACCOUNT_TYPES = {"ACCOUNT_PRIVATE"}
RISKY_WORDS = ["court", "lawsuit", "legal action", "fraud", "scam", "police",
               "hack", "suicide", "kill ", "threat"]


@dataclass
class AssessConfig:
    # UNCALIBRATED placeholders — wiring only, must be calibrated later.
    min_cases: int = 3
    min_top_similarity: float = 0.5
    min_mean_similarity: float = 0.4
    version: str = "v0-uncalibrated"


class EvidenceAssessor:
    def __init__(self, config: Optional[AssessConfig] = None):
        self.config = config or AssessConfig()

    def assess(self, query_text: str, intent: IntentPrediction,
              entities: EntitySet, hits: List[RetrievalHit]) -> EvidenceAssessment:
        c = self.config
        flags: List[str] = []
        missing: List[str] = []
        low = (query_text or "").lower()
        if any(w in low for w in RISKY_WORDS):
            flags.append("risky_language")
        if any(e.type in ACCOUNT_TYPES for e in entities.entities):
            flags.append("account_specific")
        if not (query_text or "").strip():
            return EvidenceAssessment(sufficient=False, confidence=0.0,
                                      missing_information=["message text"],
                                      risk_flags=flags, reason="empty message")
        if not hits:
            return EvidenceAssessment(sufficient=False, confidence=0.0,
                                      missing_information=["no retrieved cases"],
                                      risk_flags=flags + ["no_evidence"],
                                      reason="retrieval returned nothing")
        sims = [h.similarity for h in hits]
        top, mean = max(sims), sum(sims) / len(sims)
        ids = [h.case.customer_message_id for h in hits]
        # Response agreement: do top responses look like the same action?
        # Cheap proxy: share of non-empty responses + top-response dominance.
        nonempty = [h for h in hits if h.case.response_text.strip()]
        if len(nonempty) < 2:
            missing.append("too few usable historical responses")
        if top < c.min_top_similarity or mean < c.min_mean_similarity:
            missing.append(f"low similarity (top={top:.2f} mean={mean:.2f})")
        if len(hits) < c.min_cases:
            missing.append(f"only {len(hits)} cases (need {c.min_cases})")
        if intent.intent_id in ("unknown_empty", "megacluster_unclear",
                                "off_topic_chat", "transitional"):
            missing.append(f"unresolved intent ({intent.intent_id})")
            flags.append("unclear_intent")
        blocking = {"risky_language", "account_specific"} & set(flags)
        sufficient = not missing and not blocking
        reason = ("sufficient: cases agree and apply" if sufficient else
                  "insufficient: " + "; ".join(
                      ([f"blocking: {sorted(blocking)}"] if blocking else []) + missing))
        conf = round(max(0.0, min(1.0, (mean if sufficient else mean / 2))), 3)
        return EvidenceAssessment(
            sufficient=sufficient, confidence=conf, supporting_case_ids=ids,
            missing_information=missing, risk_flags=sorted(set(flags)),
            reason=reason)
