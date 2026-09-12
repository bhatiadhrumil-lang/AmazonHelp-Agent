"""Build a per-cluster evidence digest for the manual cluster audit.

Reads ONLY persisted artifacts (labels, embeddings meta, cluster summaries,
representatives). Computes descriptive signals per cluster that a human/LLM
can use to judge coherence, template domination, multilingual composition,
and artifact status -- without regenerating anything.

Outputs under artifacts/discovery/taxonomy/_digest/:
  cluster_digest.csv   (one row per non-noise cluster with computed signals)
  cluster_digest.md    (human-readable digest incl. the 8 representatives)
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

CLUSTER_DIR = "artifacts/discovery/clustering/initial"
META = "artifacts/discovery/embeddings/full/embeddings_meta.csv"

# Rough multilingual signal: presence of any of these stopwords in lowercased text.
LANG = {
    "es": {"que", "por", "para", "dónde", "donde", "puede", "hola", "gracias", "quiero", "estoy", "tengo", "un", "una", "mi", "no", "si", "pedido"},
    "de": {"ich", "nicht", "bitte", "mein", "meine", "habe", "war", "ist", "danke", "heute", "sie", "nur", "da", "es", "der", "die", "das", "ein", "eine"},
    "fr": {"ceci", "je", "vous", "pas", "mes", "mon", "ma", "retour", "commande", "bonjour", "merci", "avez", "pu", "une", "des", "les", "que", "qui", "est"},
    "hi": {"ऑर्डर", "डिलीवरी", "नहीं", "मेरा", "कृपया"},
}


def _clean(x):
    return str(x).lower()


def lang_flags(texts: pd.Series) -> dict[str, float]:
    """Fraction of messages containing a word-boundary exact stopword for es/de/fr/he."""
    lo = texts.map(_clean)
    flags = {k: 0.0 for k in LANG}
    for key, words in LANG.items():
        pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b")
        mask = lo.apply(lambda s: bool(pat.search(s)))
        flags[key] = float(mask.mean())
    return flags


def build_digest(cluster_dir: Path, meta_path: Path, out_dir: Path, n_rep: int = 8):
    cluster_dir = Path(cluster_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    labels = np.load(cluster_dir / "labels.npy")
    meta = pd.read_csv(meta_path)
    n_clusters = int(labels.max()) + 1 if (labels >= 0).any() else 0

    rows = []
    reps_rows = []
    for lab in range(n_clusters):
        mask = labels == lab
        idx = np.flatnonzero(mask)
        m = meta.iloc[idx].copy()

        texts = m["text"].fillna("")
        exact = Counter(texts)
        dup_share = float(texts[texts.isin([t for t, c in exact.items() if c > 1])].count() / len(texts))

        top_texts = "; ".join(f"{t[:80]!r} (x{c})" for t, c in exact.most_common(3))

        rep_path = cluster_dir / f"cluster_{lab}_representatives.csv"
        reps = pd.read_csv(rep_path) if rep_path.exists() else pd.DataFrame(
            columns=["customer_message_id", "conversation_id", "probability", "outlier_score", "text"]
        )

        subs = []
        for _, r in reps.iterrows():
            subs.append({
                "cluster_id": lab,
                "customer_message_id": r["customer_message_id"],
                "conversation_id": r["conversation_id"],
                "probability": r["probability"],
                "outlier_score": r["outlier_score"],
                "text": str(r["text"])[:220],
            })
        reps_rows.extend(subs)

        row = {
            "cluster_id": lab,
            "size": int(mask.sum()),
            "median_member_chars": float(np.median([len(str(t)) for t in texts])),
            "url_share": float(m["has_url"].mean()) if "has_url" in m else float("nan"),
            "ack_share": float(m["is_acknowledgment_like"].mean()) if "is_acknowledgment_like" in m else float("nan"),
            "exact_dup_share": dup_share,
            "top_exact_texts": top_texts,
        }
        flags = lang_flags(texts)
        the_text = " ".join(str(t) for t in texts.head(60))
        row["multilingual_flag"] = "yes" if sum(flags.values()) >= 0.15 else "no"
        row["es_share"] = round(flags["es"], 3)
        row["de_share"] = round(flags["de"], 3)
        row["fr_share"] = round(flags["fr"], 3)
        row["hi_share"] = round(flags["hi"], 3)
        rows.append(row)

    digest = pd.DataFrame(rows)
    digest.to_csv(out_dir / "cluster_digest.csv", index=False)
    pd.DataFrame(reps_rows).to_csv(out_dir / "cluster_representatives_digest.csv", index=False)
    print(f"[digest] {len(digest)} clusters -> {out_dir/'cluster_digest.csv'} + reps digest")
    return digest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cluster-dir", default=CLUSTER_DIR)
    p.add_argument("--meta", default=META)
    p.add_argument("--out", default="artifacts/discovery/taxonomy/_digest")
    args = p.parse_args()
    build_digest(Path(args.cluster_dir), Path(args.meta), Path(args.out))


if __name__ == "__main__":
    main()