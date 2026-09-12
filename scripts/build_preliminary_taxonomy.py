"""TASK 8: build the PRELIMINARY intent taxonomy from cluster interpretations.

Reads artifacts/discovery/taxonomy/cluster_interpretation.csv (203 clusters).
Aggregates by possible_parent_intent and by kind (intent/artifact/sentiment/
contextual/ood). Writes:
  - preliminary_taxonomy.csv  (parent-intent level, PRELIMINARY - for humans)
  - preliminary_taxonomy.md   (narrative + counts + caveats)

This taxonomy is EMERGENT (derived from the 203 clusters), not a preset list.
It does NOT claim accuracy or ground truth; human validation precedes any use.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTERP_CSV = ROOT / "artifacts/discovery/taxonomy/cluster_interpretation.csv"
OUT_CSV = ROOT / "artifacts/discovery/taxonomy/preliminary_taxonomy.csv"
OUT_MD = ROOT / "artifacts/discovery/taxonomy/preliminary_taxonomy.md"

KIND_NOTE = {
    "intent": "cluster appears to express a real customer goal",
    "artifact": "conversation-closure / template turn - NOT an intent; needs the conversation layer",
    "sentiment": "venting / accusation - NOT a goal; carries an underlying issue elsewhere in the thread",
    "contextual": "reading depends on the rest of the thread",
    "ood": "out-of-domain / off-topic chatter",
}


def main() -> None:
    df = pd.read_csv(INTERP_CSV, keep_default_na=False)
    total_points = int(df["cluster_size"].sum())

    agg = (
        df.groupby(["possible_parent_intent", "kind"])
        .agg(
            n_clusters=("cluster_id", "count"),
            n_points=("cluster_size", "sum"),
            member_families=("family_key", lambda s: ";".join(sorted(s))),
            member_clusters=("cluster_id", lambda s: ";".join(str(c) for c in sorted(s))),
        )
        .reset_index()
        .sort_values("n_points", ascending=False)
    )
    agg["share_of_clustered"] = (agg["n_points"] / total_points).round(4)
    agg.to_csv(OUT_CSV, index=False, encoding="utf-8")

    intents = agg[agg["kind"] == "intent"]

    lines = [
        "# Preliminary intent taxonomy (Phase 1C, TASK 8) - DRAFT FOR HUMAN VALIDATION",
        "",
        f"- Built from **203 clusters** / **43,550 clustered points** (49,621 noise excluded from "
        "taxonomy for now).",
        "- **PRELIMINARY and emergent.** Number of leaves (below) is what the clusters suggest; it "
        "is not a preset target and will change after human review.",
        "- **Not a truth claim.** These are evidence-based readings of cluster representative "
        "messages. HDBSCAN clusters are not ground truth, and no accuracy statement is made.",
        "",
        "## Top-level view (by kind)",
        "",
        "| kind | label | n clusters | n points | share of clustered |",
        "|---|---|---|---|---|",
    ]
    for kind, note in KIND_NOTE.items():
        sub = agg[agg["kind"] == kind]
        lines.append(
            f"| {kind} | {note} | {sub['n_clusters'].sum()} | {sub['n_points'].sum()} | "
            f"{sub['n_points'].sum() / total_points:.1%} |"
        )
    lines += ["", "## Intent area map (PRELIMINARY, emementary groupings)", ""]
    lines += ["| possible_parent_intent | n clusters | n points | share | kind | member families |",
              "|---|---|---|---|---|---|"]
    for _, r in agg.iterrows():
        lines.append(
            f"| {r['possible_parent_intent']} | {r['n_clusters']} | {r['n_points']} | "
            f"{r['share_of_clustered']:.1%} | {r['kind']} | {r['member_families']} |"
        )
    lines = [ln.replace("emementary", "emergent") for ln in lines]

    lines += ["", "## Reading notes", ""]
    lines += [
        "### 1. Bigger than expected share of *non-intent* clusters",
        f"Only **{int(intents['n_clusters'].sum())}** of the 203 clusters are read as expressing "
        "a customer goal; the rest are conversation-closure artifacts, sentiment/venting, "
        "thread-contextual turns, or OOD chatter. In this Twitter-DM support data the social layer "
        "is big: a human validator should confirm this before designing triage.",
        "",
        "### 2. Delivery & shipping dominates the customer-goal volume",
        "Tracking/delay/date/carrier/driver/misdelivery/damage/speed clusters together are the "
        "largest *intent* family by clustered points (several clusters >1000: e.g. cluster 7's "
        "megacluster, 156, 146, 198). Delivery sub-themes need the split review in split_candidates.csv.",
        "",
        "### 3. Orders & fulfilment (refund/replacement/return) is the second large block",
        "Refund and replacement status clusters (189, 183, 187) plus return-pickup (46, 188) are "
        "frequent. Note the distinction kept between *refund request/status* (goal) and the "
        "historical *response* (how AmazonHelp replied) - response behaviour is intentionally NOT "
        "encoded in the labels.",
        "",
        "### 4. Conversation-closure and waiting/status clusters dominate the *artifact* half",
        f"{int(agg[agg['kind'] == 'artifact']['n_clusters'].sum())} clusters are acknowledgments, "
        "commitments, polarity/date answers or status waits (incl. clusters 0-6, 110-135, 158-159). "
        "These are merge candidates (see merge_candidates.csv).",
        "",
        "### 5. What is NOT in the taxonomy",
        "- 49,621 noise points - sampled and classified separately (see noise_analysis.md);",
        "- No named 'AUTO-CLARIFY-ESCALATE' decisions anywhere - automation policy is a separate "
        "concern from intents and was not derived here;",
        "- No cluster renamed as a *final* intent - every label carries 'Likely/Conversation/…' "
        "style wording pending human validation.",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD.name}")
    print(f"preliminary_taxonomy.csv: {len(agg)} parent/kind rows | clustered points {total_points}")


if __name__ == "__main__":
    main()