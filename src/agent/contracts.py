"""Runtime data contracts for the support agent (Phase 2, TASK 2).

Provider-independent dataclasses. All are JSON-serializable via
`to_dict()` (dataclasses.asdict). Confidence fields are UNCALIBRATED
placeholders unless stated; see evidence/router policy docs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional

Decision = Literal["AUTO", "CLARIFY", "ESCALATE"]


@dataclass
class IncomingMessage:
    message_id: str
    text: str
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConversationTurn:
    author: Literal["customer", "agent", "system"]
    text: str
    timestamp: Optional[str] = None


@dataclass
class ConversationContext:
    conversation_id: Optional[str]
    current_message: IncomingMessage
    # Customer-side turns only, most-recent-first, bounded by ContextBuilder.
    # AmazonHelp replies are NEVER placed here (see ContextBuilder).
    prior_customer_turns: List[ConversationTurn] = field(default_factory=list)
    # Full original thread (customer + agent), kept for audit, not for intent.
    full_thread: List[ConversationTurn] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IntentAlternative:
    intent_id: str
    confidence: float  # UNCALIBRATED 0..1, do not threshold in production


@dataclass
class IntentPrediction:
    intent_id: str  # provisional family key, e.g. "delivery_delay"
    confidence: float  # UNCALIBRATED 0..1
    alternatives: List[IntentAlternative] = field(default_factory=list)
    source: str = "provisional"  # adapter name that produced this
    explanation: str = ""
    is_provisional: bool = True
    # Taxonomy kind (intent / artifact / contextual / sentiment / ood).
    # Artifacts & context-dependent turns carry no standalone goal.
    kind: str = ""
    # Explicit unknown/OOD flag from a validated classifier (TASK 20).
    # Distinct from HDBSCAN noise; never set by the provisional adapter.
    ood: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Entity:
    type: str
    value: str
    normalized_value: Optional[str] = None
    confidence: float = 0.0  # UNCALIBRATED unless extractor documents otherwise
    source: str = "provisional"


@dataclass
class EntitySet:
    entities: List[Entity] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HistoricalEvidence:
    source_message_id: str
    conversation_id: str
    customer_text: str
    # Historical AmazonHelp reply: EVIDENCE ONLY, never auto-answer.
    historical_response: str
    similarity: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceAssessment:
    sufficient: bool
    confidence: float  # UNCALIBRATED qualitative score, do not threshold
    supporting_case_ids: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResponseDraft:
    text: str
    supporting_evidence_ids: List[str] = field(default_factory=list)
    grounded: bool = False  # True only if every claim traces to evidence/inputs
    provider: str = "stub"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RoutingDecision:
    decision: Decision
    reason: str = ""
    risk_flags: List[str] = field(default_factory=list)
    evidence_sufficient: bool = False
    policy_version: str = "v0-uncalibrated"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResult:
    incoming: IncomingMessage
    context: ConversationContext
    intent: IntentPrediction
    entities: EntitySet
    evidence: List[HistoricalEvidence]
    assessment: EvidenceAssessment
    routing: RoutingDecision
    draft: Optional[ResponseDraft] = None
    # Structured metadata only; never chain-of-thought.
    trace: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
