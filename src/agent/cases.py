"""Historical support-case store (Phase 2, TASK 3).

Joins the audit's KEEP episodes (customer text + AmazonHelp response) to the
embedding row map by customer_message_id (explicit join — meta row order is
NOT assumed to match episode order).

Customer text and AmazonHelp response stay SEPARATE fields; the response is
historical evidence, never an auto-answer.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
EPISODES = ROOT / "artifacts/conversation_audit/full_run_fixed/customer_problem_episodes.csv"
EMB_META = ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv"


@dataclass
class HistoricalCase:
    customer_message_id: str
    conversation_id: str
    customer_text: str
    response_text: str  # historical AmazonHelp reply — evidence only
    created_dt: str
    embedding_row: int  # row index into embeddings.npy / retrieval matrix
    metadata: dict


class CaseStore:
    """KEEP-only episodes with embedding-row mapping. Built once, read-only."""

    def __init__(self, cases: List[HistoricalCase]):
        self.cases = cases
        self.by_id: Dict[str, HistoricalCase] = {c.customer_message_id: c for c in cases}
        assert len(self.by_id) == len(cases), "duplicate customer_message_id"

    @classmethod
    def load(cls, episodes_csv: Path = EPISODES,
             emb_meta_csv: Path = EMB_META) -> "CaseStore":
        ep = pd.read_csv(episodes_csv, keep_default_na=False)
        keep = ep[ep["episode_status"] == "KEEP"].copy()
        if len(keep) == 0:
            raise ValueError("no KEEP episodes — refusing to build an empty store")
        meta = pd.read_csv(emb_meta_csv, usecols=["customer_message_id"],
                           keep_default_na=False)
        row_of = {cid: i for i, cid in enumerate(meta["customer_message_id"])}
        missing = [c for c in keep["customer_message_id"] if c not in row_of]
        if missing:
            raise ValueError(f"{len(missing)} KEEP ids lack embedding rows")
        cases = [
            HistoricalCase(
                customer_message_id=str(r["customer_message_id"]),
                conversation_id=str(r["conversation_id"]),
                customer_text=str(r["text"]),
                response_text=str(r["brand_parent_text"]),
                created_dt=str(r["created_dt"]),
                embedding_row=int(row_of[r["customer_message_id"]]),
                metadata={"author_id": str(r.get("author_id", "")),
                          "reply_gap_minutes": str(r.get("reply_gap_minutes", ""))},
            )
            for _, r in keep.iterrows()
        ]
        return cls(cases)

    def get(self, customer_message_id: str) -> Optional[HistoricalCase]:
        return self.by_id.get(str(customer_message_id))

    def __len__(self) -> int:
        return len(self.cases)
