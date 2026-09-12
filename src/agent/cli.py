"""Local CLI demo (Phase 2, TASK 15).

Usage (repo root):
    PYTHONPATH=src .venv/bin/python -m agent.cli --message "Where is my order?"
    PYTHONPATH=src .venv/bin/python -m agent.cli --message "..." --conversation-id C --prior "earlier turn"

Prints INTENT / ENTITIES / TOP HISTORICAL CASES / EVIDENCE / DECISION /
REASON / DRAFT. Provisional pieces are labeled as such.
"""
from __future__ import annotations

import argparse
import json

from agent.agent import SupportAgent
from agent.contracts import ConversationTurn, IncomingMessage
from agent.retrieval import Retriever


def main() -> None:
    ap = argparse.ArgumentParser(description="Support agent local demo (provisional)")
    ap.add_argument("--message", required=True)
    ap.add_argument("--message-id", default="cli-1")
    ap.add_argument("--conversation-id", default=None)
    ap.add_argument("--prior", action="append", default=[],
                    help="prior customer turn, oldest first; repeat flag")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    agent = SupportAgent(retriever=Retriever.build())
    res = agent.run(IncomingMessage(message_id=args.message_id, text=args.message),
                    conversation_id=args.conversation_id,
                    prior_customer_texts=args.prior, top_k=args.top_k)
    if args.json:
        print(json.dumps(res.to_dict(), indent=2)[:6000])
        return
    print(f"MESSAGE : {res.incoming.text}")
    print(f"INTENT  : {res.intent.intent_id} (conf={res.intent.confidence:.3f}, "
          f"source={res.intent.source}, provisional={res.intent.is_provisional})")
    print(f"  alts  : {[(a.intent_id, round(a.confidence, 3)) for a in res.intent.alternatives]}")
    print(f"ENTITIES: {[(e.type, e.value) for e in res.entities.entities] or 'none'}")
    print("TOP HISTORICAL CASES:")
    for ev in res.evidence[:5]:
        print(f"  sim={ev.similarity:.3f} id={ev.source_message_id}")
        print(f"    cust: {ev.customer_text[:130]}")
        print(f"    resp: {ev.historical_response[:130]}")
    print(f"EVIDENCE: sufficient={res.assessment.sufficient} "
          f"conf={res.assessment.confidence} reason={res.assessment.reason}")
    print(f"DECISION: {res.routing.decision}")
    print(f"REASON  : {res.routing.reason}")
    print(f"DRAFT   : {(res.draft.text if res.draft else '')[:600]}")
    print(f"TRACE   : {res.trace}")


if __name__ == "__main__":
    main()
