"""Human annotation schema (Phase 3, TASK 5+6).

A golden record captures WHAT THE CUSTOMER WANTS (never "what AmazonHelp
replied"). Taxonomy feedback uses explicit disagreement codes — one
annotation never silently rewrites the taxonomy; the taxonomy builder
aggregates codes across annotators.

Labels live in artifacts/evaluation/golden_labels.csv (created by the
annotation CLI), keyed by candidate_id. The candidates file stays label-free.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

# TASK 6 disagreement codes: how this label relates to the preliminary taxonomy.
DISAGREEMENT_CODES = (
    "fits",              # an existing preliminary intent fits
    "merge",             # two preliminary intents should be one (name both in notes)
    "split",             # this case needs a distinct new intent carved out
    "new_intent",        # no preliminary intent covers it; propose one
    "ood",               # out-of-domain / unsupported request
    "ambiguous",         # cannot decide even with context shown
    "context_dependent", # decidable only with the shown thread context
)

ROUTING_EXPECTATIONS = ("auto_ok", "clarify", "escalate", "unsure")

# Auditability: how the human's final label relates to the model suggestion.
# accepted = final intent == suggestion; corrected = chose a different
# existing intent; rejected = coined new / went OOD-uncertain against the
# suggestion; uncertain = could not decide (verdict ambiguous/context_dependent/ood).
SUGGESTION_OUTCOMES = ("accepted", "corrected", "rejected", "uncertain")


@dataclass
class GoldenLabel:
    candidate_id: str
    annotator: str
    # --- core label: WHAT DOES THE CUSTOMER WANT? ---
    intent_id: str            # stable snake_case, e.g. "delivery_delay"
    intent_name: str          # human-readable, e.g. "Delivery delayed"
    primary_goal: str         # one sentence in the annotator's own words
    # --- structured extras ---
    entities: List[Dict[str, str]] = field(default_factory=list)  # {type,value}
    routing_expectation: str = "unsure"  # one of ROUTING_EXPECTATIONS
    escalation_reason: str = ""
    response_requirements: str = ""  # what a correct reply MUST/ MUST NOT do
    ambiguity: bool = False
    ood: bool = False
    # --- TASK 6 taxonomy feedback ---
    taxonomy_verdict: str = "fits"  # one of DISAGREEMENT_CODES
    taxonomy_notes: str = ""  # e.g. "merge delivery_delay+delivery_tracking"
    # --- audit ---
    needs_second_opinion: bool = False
    # --- auditability (added in workflow v2; empty on pre-v2 rows) ---
    # case_id is an alias of candidate_id (kept as one column to avoid duplication).
    model_suggestion: str = ""  # family key suggested, "" if none recorded
    suggestion_outcome: str = ""  # one of SUGGESTION_OUTCOMES, "" if unrecorded
    annotated_at: str = ""  # ISO-8601 UTC timestamp, "" if unrecorded

    def validate(self) -> List[str]:
        errs = []
        if not self.intent_id or " " in self.intent_id:
            errs.append("intent_id must be non-empty snake_case")
        if not self.primary_goal.strip():
            errs.append("primary_goal required")
        if self.routing_expectation not in ROUTING_EXPECTATIONS:
            errs.append(f"routing_expectation must be one of {ROUTING_EXPECTATIONS}")
        if self.taxonomy_verdict not in DISAGREEMENT_CODES:
            errs.append(f"taxonomy_verdict must be one of {DISAGREEMENT_CODES}")
        if self.ood and self.taxonomy_verdict != "ood":
            errs.append("ood=True requires taxonomy_verdict='ood'")
        if self.taxonomy_verdict == "new_intent" and not self.taxonomy_notes.strip():
            errs.append("taxonomy_verdict='new_intent' requires taxonomy_notes describing the proposal")
        if self.routing_expectation == "escalate" and not self.escalation_reason.strip():
            errs.append("routing_expectation='escalate' requires escalation_reason")
        if self.routing_expectation == "clarify" and not self.response_requirements.strip():
            errs.append("routing_expectation='clarify' requires response_requirements "
                        "(state the clarifying question/rationale)")
        if self.routing_expectation == "auto_ok" and self.escalation_reason.strip():
            errs.append("routing_expectation='auto_ok' must leave escalation_reason blank")
        if self.suggestion_outcome and self.suggestion_outcome not in SUGGESTION_OUTCOMES:
            errs.append(f"suggestion_outcome must be one of {SUGGESTION_OUTCOMES}")
        if self.suggestion_outcome == "accepted":
            if not self.model_suggestion:
                errs.append("outcome 'accepted' needs a recorded model_suggestion")
            elif self.intent_id != self.model_suggestion:
                errs.append("outcome 'accepted' requires intent_id == model_suggestion")
        if self.suggestion_outcome == "uncertain" and self.taxonomy_verdict not in (
                "ambiguous", "context_dependent", "ood"):
            errs.append("outcome 'uncertain' requires verdict ambiguous/context_dependent/ood")
        if self.annotated_at:
            from datetime import datetime
            try:
                datetime.fromisoformat(self.annotated_at)
            except ValueError:
                errs.append("annotated_at must be ISO-8601")
        for e in self.entities:
            if "type" not in e or "value" not in e:
                errs.append("each entity needs type and value")
        return errs

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        import json
        d["entities"] = json.dumps(self.entities)
        return d

    @classmethod
    def fieldnames(cls) -> List[str]:
        return ["candidate_id", "annotator", "intent_id", "intent_name",
                "primary_goal", "entities", "routing_expectation",
                "escalation_reason", "response_requirements", "ambiguity",
                "ood", "taxonomy_verdict", "taxonomy_notes",
                "needs_second_opinion", "model_suggestion",
                "suggestion_outcome", "annotated_at"]
