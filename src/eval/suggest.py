"""Model-suggestion engine + intent catalog for annotation (NOT ground truth).

Suggestions come from the SAME provisional nearest-centroid model the agent
uses: cosine of the candidate's EXISTING 384D embedding row against the 73
family centroids persisted under artifacts/retrieval/. No new embeddings, no
new model, deterministic. A suggestion is display-only context; the human's
choice is recorded separately with an explicit outcome
(accepted/corrected/rejected/uncertain).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
INTERP = ROOT / "artifacts/discovery/taxonomy/cluster_interpretation.csv"
EMB = ROOT / "artifacts/discovery/embeddings/full/embeddings.npy"
CENT = ROOT / "artifacts/retrieval/provisional_centroids.npy"
CENT_MAP = ROOT / "artifacts/retrieval/provisional_centroids_map.json"
LABELS = ROOT / "artifacts/evaluation/golden_labels.csv"


@dataclass
class Suggestion:
    family: str
    display_name: str
    similarity: float
    margin: float  # top1 - top2, low = uncertain
    alternatives: List[Dict[str, object]] = field(default_factory=list)


def load_catalog() -> pd.DataFrame:
    """Numbered intent catalog from the REAL preliminary taxonomy artifacts.

    One row per family_key with its preliminary label as display name.
    Provisional names are shown as-is and NEVER presented as final taxonomy.
    """
    interp = pd.read_csv(INTERP, keep_default_na=False)
    cat = interp[["family_key", "preliminary_label", "kind"]].drop_duplicates(
        "family_key").sort_values("family_key").reset_index(drop=True)
    return cat


def human_coined_intents() -> pd.DataFrame:
    """Intent ids previously coined by human annotators (avoid re-coinage)."""
    if not LABELS.exists():
        return pd.DataFrame(columns=["intent_id", "intent_name", "n"])
    d = pd.read_csv(LABELS, keep_default_na=False)
    g = d.groupby(["intent_id", "intent_name"]).size().reset_index(name="n")
    return g.sort_values("intent_id").reset_index(drop=True)


def compute_suggestions(embedding_indices: List[int]) -> Dict[int, Suggestion]:
    """Nearest-centroid suggestion per embedding row. Pure function of
    existing artifacts; deterministic.
    Mirrors the agent's ProvisionalClusterAdapter exactly: nearest CLUSTER
    centroid wins and its family becomes the suggestion; alternatives are the
    next distinct families."""
    cents = np.load(CENT).astype(np.float64)
    cids = json.loads(CENT_MAP.read_text())["cluster_ids"]
    cat = load_catalog().set_index("family_key")
    interp = pd.read_csv(INTERP, keep_default_na=False)
    fam_of = dict(zip(interp.cluster_id.astype(int), interp.family_key))
    E = np.load(EMB, mmap_mode="r")
    X = np.asarray(E[np.array(embedding_indices)]).astype(np.float64)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
    S = X @ cents.T
    order = np.argsort(-S, axis=1)
    out: Dict[int, Suggestion] = {}
    for pos, row in enumerate(embedding_indices):
        o = order[pos]
        top, second = float(S[pos, o[0]]), float(S[pos, o[1]])
        fam = fam_of[int(cids[int(o[0])])]
        seen = {fam}
        alts = []
        for i in o[1:]:
            f = fam_of[int(cids[int(i)])]
            if f not in seen:
                seen.add(f)
                alts.append({"family": f,
                             "display": str(cat.loc[f, "preliminary_label"]),
                             "sim": round(float(S[pos, i]), 3)})
            if len(alts) == 3:
                break
        out[int(row)] = Suggestion(
            family=fam,
            display_name=str(cat.loc[fam, "preliminary_label"]),
            similarity=round(top, 3), margin=round(top - second, 3),
            alternatives=alts)
    return out
