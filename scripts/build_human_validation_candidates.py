"""TASK 10: build a deterministic PROPOSED human-validation sample (~205 rows).

Selection criteria (each candidate carries its sampling_reason):
  1. common/megacluster: 1 rep (highest-probability) from the 30 largest clusters
     (incl. the cluster-7 megacluster for heterogeneity review).
  2. small_cluster: 1 rep from each cluster with size <= 40.
  3. ambiguous/uncertain: 1 rep from every cluster whose interpretation has
     confidence != high or coherent != yes.
  4. merge_group: 1 rep from every cluster that belongs to a merge candidate group.
  5. split_cluster: 3 reps (probability-ranked slots 0,2,4) from each split candidate.
  6. noise: stratified sample from the classified noise sample (larger for the
     'fits_cluster_theme' bucket, smaller for thread-turn / off-topic / fragment).
  7. multilingual: any example whose text is non-English per the word-boundary
     heuristic is tagged language=<lang> and counted; no extra add is needed
     because cluster reps already include many non-English texts.

Traceability: example_id, conversation_id, customer_message_id, text,
preliminary_intent, source_cluster, sampling_reason, language, agent_help_reply=False.
No duplicate (conversation_id, customer_message_id) pairs in the output.

Output: artifacts/discovery/taxonomy/human_validation_candidates.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TAX = ROOT / "artifacts/discovery/taxonomy"
REPS_DIR = ROOT / "artifacts/discovery/clustering/initial"

LANGS = {
    "es": ("de",),  # placeholder replaced below
}

# real word-boundary language heuristics (re-use of digest heuristics)
LANG_WORDS = {
    "es": [r"\b(gracias|por|que|pero|todo|envío|entrega|he|les|mándo|mando|estoy|porque|así|para|perdón|cómo)\b"],
    "de": [r"\b(bitte|danke|und|auch|sehr|schon|nicht|mein|ich)\b"],
    "fr": [r"\b(merci|pour|pas|une|votre|nom|vous|bonjour|oui|non|mais|faire|est)\b"],
    "pt": [r"\b(obrigado|obrigada|para|mas|você|que|não|sim|estou|não)\b"],
    "it": [r"\b(grazie|pero|che|non|si|ecco|sono)\b"],
    "hi": [r"\b(kya|hai|na|bhi|aap|apne|koi|mene|hme|hai|kar)\b"],
}
LANG_RE = {lang: re.compile("|".join(pat), re.IGNORECASE) for lang, pat in LANG_WORDS.items()}


def detect_lang(text: str) -> str:
    text = text.lower()
    for lang, rx in LANG_RE.items():
        if rx.search(text):
            return lang
    return "en"


def main() -> None:
    interp = pd.read_csv(TAX / "cluster_interpretation.csv", keep_default_na=False)
    interp = interp.set_index("cluster_id")
    merge = pd.read_csv(TAX / "merge_candidates.csv", keep_default_na=False)
    split = pd.read_csv(TAX / "split_candidates.csv", keep_default_na=False)
    noise = pd.read_csv(TAX / "noise_sample_classified.csv", keep_default_na=False)

    def rep_examples(cid: int, slots):
        f = REPS_DIR / f"cluster_{cid}_representatives.csv"
        d = pd.read_csv(f, keep_default_na=False).sort_values("probability", ascending=False)
        picks = []
        for s in slots:
            if s < len(d):
                row = d.iloc[s]
                picks.append((row["customer_message_id"], row["conversation_id"], row["text"],
                              int(row["probability"] > 0), cid))
        return picks

    rows = []
    seen = set()

    def add(cid, reason, cmsg, conv, text):
        layer = (cid, cmsg)
        if layer in seen:
            return None
        seen.add(layer)
        row = interp.loc[cid]
        lang = detect_lang(str(text))
        rows.append({
            "example_id": f"HV-{len(rows) + 1:04d}",
            "conversation_id": conv,
            "customer_message_id": cmsg,
            "text": text,
            "preliminary_intent": row["preliminary_label"],
            "source_cluster": cid,
            "source": "cluster",
            "sampling_reason": reason,
            "language": lang,
            "agent_help_reply": "False",
        })

    # 1. common / megacluster - 30 largest clusters, rep slot 0
    top = interp["cluster_size"].nlargest(30).index
    for cid in top:
        for cmsg, conv, text, _, _ in rep_examples(cid, [0]):
            add(cid, "common_cluster", cmsg, conv, text)

    # 2. small clusters (size <= 40)
    small = interp[interp["cluster_size"] <= 40].index
    for cid in small:
        for cmsg, conv, text, _, _ in rep_examples(cid, [0]):
            add(cid, "small_cluster", cmsg, conv, text)

    # 3. ambiguous / uncertain
    amb = interp[(interp["confidence"] != "high") | (interp["coherent"] != "yes")].index
    for cid in amb:
        for cmsg, conv, text, _, _ in rep_examples(cid, [0]):
            add(cid, "ambiguous_or_uncertain", cmsg, conv, text)

    # 4. merge groups - 1 rep per member cluster
    for _, g in merge.iterrows():
        for cid in [int(c) for c in str(g["member_clusters"]).split(";")]:
            for cmsg, conv, text, _, _ in rep_examples(cid, [0]):
                add(cid, f"merge_group_{g['group_id']}", cmsg, conv, text)

    # 5. split candidates - several reps each (varied slots)
    for _, s in split.iterrows():
        cid = int(s["cluster_id"])
        for cmsg, conv, text, _, _ in rep_examples(cid, [0, 2, 4]):
            add(cid, f"split_candidate_{cid}", cmsg, conv, text)

    # 6. noise - stratified across buckets
    strat = {
        "fits_cluster_theme": 20,
        "thread_turn": 8,
        "offtopic_social": 8,
        "data_fragment": 2,
        "novel_or_unclear": 1,
    }
    for bucket, n in strat.items():
        sub = noise[noise["bucket"] == bucket].head(n)
        for _, r in sub.iterrows():
            key = ("noise", r["customer_message_id"])
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "example_id": f"HV-{len(rows) + 1:04d}",
                "conversation_id": r["conversation_id"],
                "customer_message_id": r["customer_message_id"],
                "text": r["text"],
                "preliminary_intent": "NOISE-UNCERTAIN",
                "source_cluster": -1,
                "source": "noise",
                "sampling_reason": f"noise_{bucket}",
                "language": detect_lang(r["text"]),
                "agent_help_reply": "False",
            })

    out = pd.DataFrame(rows)
    dup = out.duplicated(["conversation_id", "customer_message_id"]).sum()
    if dup:
        raise SystemExit(f"ERROR duplicate examples: {dup}")
    out.to_csv(TAX / "human_validation_candidates.csv", index=False, encoding="utf-8")

    lang_counts = out["language"].value_counts().to_dict()
    n_multi = sum(v for k, v in lang_counts.items() if k != "en")
    print(f"human_validation_candidates.csv: {len(out)} examples | duplicates={dup}")
    print(f"non-English examples: {n_multi} ({n_multi / len(out):.0%})")
    print(f"language counts: {lang_counts}")
    print(out["source"].value_counts().to_dict())
    print("sampling_reason counts:")
    print(out["sampling_reason"].value_counts().head(20).to_string())


if __name__ == "__main__":
    main()