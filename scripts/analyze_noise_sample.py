"""TASK 6: classify the noise sample and write noise_analysis.md.

The 150 rows in artifacts/discovery/taxonomy/noise_sample.csv were read and
hand-classified into buckets:
  - "fits_cluster_theme": noise point that matches an already-clustered intent
    theme (near-hit / boundary point). Most common.
  - "thread_turn": short reply/status word that is only meaningful in the
    surrounding conversation (ack, status fragment, chronology answer).
  - "offtopic_social": casual/social/vent/rhetorical chatter (incl. some OOD).
  - "data_fragment": half-templated short platform fragment.
  - "novel_or_unclear": genuinely unusual combination or ambiguous.

Bucket counts are SAMPLE-LEVEL (n=150, seed=42) and must NOT be extrapolated
to the 49,621 noise population.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_CSV = ROOT / "artifacts/discovery/taxonomy/noise_sample.csv"
OUT_CSV = ROOT / "artifacts/discovery/taxonomy/noise_sample_classified.csv"
OUT_MD = ROOT / "artifacts/discovery/taxonomy/noise_analysis.md"

BUCKETS = {
    "fits_cluster_theme": (
        "Matches an existing cluster theme (near-hit / boundary point)",
        "Delivery, refund, contact-channel, form, driver, seller, device, pre-order, etc. - the "
        "underlying customer goal matches one of the 203 clusters' themes; the point simply fell "
        "into the noise set (small size, boundary, mixed-language, or one-off wording).",
    ),
    "thread_turn": (
        "Conversation-thread turn (meaningful only with context)",
        "Short acknowledgements, status words, polarity/chronology answers, channel-switch statements. "
        "As standalone tweets they carry almost no intent; the intent lives in the rest of the thread.",
    ),
    "offtopic_social": (
        "Off-topic / social / venting chatter",
        "Casual banter, emoji talk, jokes, positive praise, rhetorical venting, or out-of-domain "
        "content (non-Amazon products, living-room chit-chat).",
    ),
    "data_fragment": (
        "Data / format fragment (status token, tag, code)",
        "Almost token-level texts (e.g. 'Delivered', 'Lp Collect', 'En cours de livraison').",
    ),
    "novel_or_unclear": (
        "Novel combination or genuinely unclear",
        "Unusual combinations (e.g. messaging failure with business impact) that do not clearly "
        "match any single cluster theme.",
    ),
}

CATEGORY = {}
# sample position -> bucket key (hand-classified from reading every row)
_ASSIGN = """
0 fits_cluster_theme
1 fits_cluster_theme
2 fits_cluster_theme
3 fits_cluster_theme
4 fits_cluster_theme
5 fits_cluster_theme
6 fits_cluster_theme
7 thread_turn
8 offtopic_social
9 fits_cluster_theme
10 fits_cluster_theme
11 fits_cluster_theme
12 offtopic_social
13 fits_cluster_theme
14 fits_cluster_theme
15 offtopic_social
16 fits_cluster_theme
17 fits_cluster_theme
18 fits_cluster_theme
19 fits_cluster_theme
20 fits_cluster_theme
21 thread_turn
22 fits_cluster_theme
23 fits_cluster_theme
24 fits_cluster_theme
25 fits_cluster_theme
26 fits_cluster_theme
27 fits_cluster_theme
28 offtopic_social
29 fits_cluster_theme
30 fits_cluster_theme
31 fits_cluster_theme
32 fits_cluster_theme
33 fits_cluster_theme
34 fits_cluster_theme
35 fits_cluster_theme
36 fits_cluster_theme
37 fits_cluster_theme
38 offtopic_social
39 offtopic_social
40 fits_cluster_theme
41 fits_cluster_theme
42 fits_cluster_theme
43 fits_cluster_theme
44 fits_cluster_theme
45 fits_cluster_theme
46 fits_cluster_theme
47 fits_cluster_theme
48 fits_cluster_theme
49 fits_cluster_theme
50 fits_cluster_theme
51 thread_turn
52 fits_cluster_theme
53 fits_cluster_theme
54 fits_cluster_theme
55 fits_cluster_theme
56 thread_turn
57 fits_cluster_theme
58 fits_cluster_theme
59 thread_turn
60 fits_cluster_theme
61 fits_cluster_theme
62 fits_cluster_theme
63 fits_cluster_theme
64 fits_cluster_theme
65 fits_cluster_theme
66 thread_turn
67 fits_cluster_theme
68 fits_cluster_theme
69 fits_cluster_theme
70 thread_turn
71 offtopic_social
72 fits_cluster_theme
73 thread_turn
74 fits_cluster_theme
75 offtopic_social
76 fits_cluster_theme
77 thread_turn
78 fits_cluster_theme
79 fits_cluster_theme
80 fits_cluster_theme
81 fits_cluster_theme
82 thread_turn
83 fits_cluster_theme
84 thread_turn
85 fits_cluster_theme
86 fits_cluster_theme
87 thread_turn
88 fits_cluster_theme
89 fits_cluster_theme
90 fits_cluster_theme
91 fits_cluster_theme
92 thread_turn
93 fits_cluster_theme
94 fits_cluster_theme
95 thread_turn
96 thread_turn
97 offtopic_social
98 fits_cluster_theme
99 fits_cluster_theme
100 fits_cluster_theme
101 fits_cluster_theme
102 fits_cluster_theme
103 offtopic_social
104 thread_turn
105 offtopic_social
106 fits_cluster_theme
107 fits_cluster_theme
108 fits_cluster_theme
109 fits_cluster_theme
110 fits_cluster_theme
111 fits_cluster_theme
112 fits_cluster_theme
113 offtopic_social
114 fits_cluster_theme
115 fits_cluster_theme
116 fits_cluster_theme
117 fits_cluster_theme
118 offtopic_social
119 offtopic_social
120 fits_cluster_theme
121 fits_cluster_theme
122 fits_cluster_theme
123 fits_cluster_theme
124 offtopic_social
125 fits_cluster_theme
126 thread_turn
127 fits_cluster_theme
128 thread_turn
129 fits_cluster_theme
130 fits_cluster_theme
131 fits_cluster_theme
132 fits_cluster_theme
133 data_fragment
134 fits_cluster_theme
135 data_fragment
136 thread_turn
137 fits_cluster_theme
138 fits_cluster_theme
139 fits_cluster_theme
140 fits_cluster_theme
141 fits_cluster_theme
142 fits_cluster_theme
143 thread_turn
144 offtopic_social
145 thread_turn
146 novel_or_unclear
147 data_fragment
148 fits_cluster_theme
149 fits_cluster_theme
"""


def main() -> None:
    sample = pd.read_csv(SAMPLE_CSV, keep_default_na=False)
    assigns = {}
    for line in _ASSIGN.strip().splitlines():
        pos, bucket = line.split()
        assigns[int(pos)] = bucket

    missing = set(range(len(sample))) - set(assigns)
    extra = set(assigns) - set(range(len(sample)))
    if missing or extra:
        raise SystemExit(f"classification mismatch missing={missing} extra={extra}")

    # classification keys are the display order 0..149 (row order in the CSV)
    sample["bucket"] = list(assigns[k] for k in range(len(sample)))
    sample.to_csv(OUT_CSV, index=False, encoding="utf-8")

    counts = sample["bucket"].value_counts()
    total = len(sample)

    lines = [
        "# Noise analysis (Phase 1C, TASK 6)",
        "",
        "## Setup",
        "",
        f"- Population: **49,621** points with HDBSCAN label == -1 (53.3% of 93,171 embedded messages).",
        f"- Sample: **{total}** rows, seed=42, drawn after sorting by `customer_message_id` "
        "(so it is reproducible regardless of meta file row order).",
        f"- Source rows: `artifacts/discovery/taxonomy/noise_sample.csv` (raw text) and "
        f"`noise_sample_classified.csv` (with the `bucket` column).",
        "",
        "## Sampled composition (SAMPLE-LEVEL n=150, not a population estimate)",
        "",
        "| Bucket | Count | Share of sample |",
        "|---|---|---|",
    ]
    for bucket, _ in BUCKETS.items():
        n = int(counts.get(bucket, 0))
        lines.append(f"| {BUCKETS[bucket][0]} | {n} | {n / total:.0%} |")
    lines.append(f"| **Total** | **{total}** | **100%** |")

    lines += ["", "## Bucket meanings", ""]
    for bucket, (title, desc) in BUCKETS.items():
        lines += [f"### {title}", "", desc, ""]

    lines += ["", "## Working hypotheses (must be validated by humans)", ""]
    lines += [
        "1. The majority of sampled noise points fit an already-clustered intent theme "
        "**at the level of customer goal** (delivery, refund, contact-channel, form, driver, "
        "seller, pre-order, device, etc.). They are clustered-out mostly for surface-form or "
        "scale reasons: one-off wording, multilingual code-switching, boundary placement, or "
        "attachments/URLs dominating the text.",
        "2. A substantial minority are **thread-turn artefacts** (short ack/status/polarity "
        "replies). These are not standalone intents and should be handled by the conversation "
        "layer, not by intent triage.",
        "3. A small slice is **off-topic/social/OOD** chatter with no support goal.",
        "4. A very small slice is **token-level fragments** (status words, locker codes) and "
        "**novel/unclear** one-offs.",
        "",
        "> No percentage statements about the full noise population are made from this sample. "
        "If noise is later used for OOD detection, a far larger stratified sample plus human "
        "review is required.",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD.name}")
    for bucket, (title, _) in BUCKETS.items():
        print(f"  {bucket}: {counts.get(bucket, 0)}")


if __name__ == "__main__":
    main()