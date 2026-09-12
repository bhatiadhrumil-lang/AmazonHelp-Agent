"""Context builder (Phase 2, TASK 8).

Rules enforced here (not left to callers):
- Prior turns are CUSTOMER-SIDE only. AmazonHelp replies are never placed in
  `prior_customer_turns`; the full thread is preserved separately for audit.
- Bounded: at most `max_prior_turns` recent turns and `max_chars` total.
- Works with zero history (single message).
- The intent representation text (`intent_text`) excludes AmazonHelp content
  by construction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from agent.contracts import ConversationContext, ConversationTurn, IncomingMessage


@dataclass
class ContextConfig:
    max_prior_turns: int = 3
    max_chars: int = 1500


class ContextBuilder:
    def __init__(self, config: Optional[ContextConfig] = None):
        self.config = config or ContextConfig()

    def build(self, message: IncomingMessage,
              conversation_id: Optional[str] = None,
              prior_customer_texts: Optional[List[str]] = None,
              full_thread: Optional[List[ConversationTurn]] = None) -> ConversationContext:
        """Assemble a bounded, customer-side-only context.

        `prior_customer_texts`: oldest-first customer turns (excluding the
        current message). Only the most recent `max_prior_turns` are kept.
        """
        turns: List[ConversationTurn] = []
        budget = self.config.max_chars
        for t in reversed(prior_customer_texts or []):
            if len(turns) >= self.config.max_prior_turns:
                break
            t = (t or "").strip()
            if not t:
                continue
            if len(t) > budget:
                t = t[:budget]
            turns.append(ConversationTurn(author="customer", text=t))
            budget -= len(t)
            if budget <= 0:
                break
        turns.reverse()  # chronological
        return ConversationContext(
            conversation_id=conversation_id,
            current_message=message,
            prior_customer_turns=turns,
            full_thread=list(full_thread or []),
        )

    @staticmethod
    def intent_text(context: ConversationContext) -> str:
        """Text used for the intent representation: customer side only."""
        parts = [t.text for t in context.prior_customer_turns]
        parts.append(context.current_message.text)
        return "\n".join(p for p in parts if p and p.strip())
