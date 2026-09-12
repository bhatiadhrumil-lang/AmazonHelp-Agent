"""Entity extraction interface (Phase 2, TASK 9) — PROVISIONAL.

Design rules honored:
- Entities are DATA-DRIVEN: every extractor below fires only on patterns
  observed in the corpus (URLs, carrier/marketplace names from cluster
  readings, money/phone/email surface forms). No Amazon order-ID regex is
  included — the data does not justify one (order ids appear as redacted
  tokens/links, not plain patterns).
- No sensitive/private account data is requested. Anything account-specific
  is surfaced as an `ACCOUNT_REFERENCE` flag entity so the router can
  escalate to a private handoff — the value is never solicited publicly.
- `EntityExtractor` is the stable interface; implementations are swappable.
"""
from __future__ import annotations

import re
from typing import List

from agent.contracts import ConversationContext, Entity, EntitySet

# Observed in cluster readings / noise samples (case-insensitive).
CARRIERS = ["amazon logistics", "amzl", "ups", "fedex", "usps", "dhl",
            "hermes", "yodel", "royal mail", "canada post", "lasership",
            "aramax", "bluedart", "chronopost", "colissimo", "tnt",
            "intelcom", "india post"]
MARKETPLACES = ["amazon.in", "amazon.de", "amazon.es", "amazon.fr",
                "amazon.it", "amazon.ca", "amazon.com.mx", "amazon.com.au",
                "amazon.co.uk", "amazon.ae", "amazon.com"]
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
MONEY_RE = re.compile(r"(?:rs\.?|inr|₹|\$|€|£)\s?[\d,]+(?:\.\d{1,2})?",
                      re.IGNORECASE)
ACCOUNT_PRIVATE_RE = re.compile(
    r"\b(my|mine|our)\b.{0,40}\b(account|password|login|card\b|payment details|"
    r"address|phone number|ssn|social security)\b",
    re.IGNORECASE)
ORDER_CONTEXT_RE = re.compile(
    r"\b(my|mine|our)\b.{0,30}\b(order|package|parcel|delivery|refund|return|item)\b",
    re.IGNORECASE)


class EntityExtractor:
    name: str = "base"

    def extract(self, context: ConversationContext) -> EntitySet:
        raise NotImplementedError


class ProvisionalPatternExtractor(EntityExtractor):
    """PROVISIONAL regex/lexicon extractor. Precision over recall."""

    name = "provisional-patterns-v0"

    def extract(self, context: ConversationContext) -> EntitySet:
        text = context.current_message.text or ""
        low = text.lower()
        ents: List[Entity] = []
        for m in URL_RE.findall(text):
            ents.append(Entity(type="URL", value=m, confidence=1.0, source=self.name))
        for m in EMAIL_RE.findall(text):
            ents.append(Entity(type="EMAIL", value=m, confidence=0.9, source=self.name))
        for m in PHONE_RE.findall(text):
            digits = re.sub(r"\D", "", m)
            if 7 <= len(digits) <= 15:
                ents.append(Entity(type="PHONE_LIKE", value=m.strip(),
                                   normalized_value=digits, confidence=0.6,
                                   source=self.name))
        for m in MONEY_RE.findall(text):
            ents.append(Entity(type="MONEY_AMOUNT", value=m.strip(), confidence=0.7,
                               source=self.name))
        for c in CARRIERS:
            if c in low:
                ents.append(Entity(type="CARRIER", value=c, confidence=0.8,
                                   source=self.name))
        for mp in MARKETPLACES:
            if mp in low:
                ents.append(Entity(type="MARKETPLACE", value=mp, confidence=0.9,
                                   source=self.name))
        if ACCOUNT_PRIVATE_RE.search(text):
            ents.append(Entity(type="ACCOUNT_PRIVATE",
                               value="message references private account/payment/credential data",
                               confidence=0.7, source=self.name))
        elif ORDER_CONTEXT_RE.search(text):
            # Own-order context is normal support content, NOT a blocking flag.
            ents.append(Entity(type="ORDER_CONTEXT",
                               value="message references the caller's own order/delivery",
                               confidence=0.7, source=self.name))
        return EntitySet(entities=ents)
