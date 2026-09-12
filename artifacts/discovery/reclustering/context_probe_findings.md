# Context probe (Phase 1D, TASK 9)

Rule honored: customer-side context ONLY (corpus contains customer messages
only, so any in-corpus prior turn is customer-side by construction).
AmazonHelp responses never entered any representation. Original corpus and
authoritative embeddings untouched — the probe embeds only a 300-row subset
with a modified input.

## Observational evidence (full 93,171, no new embeddings)

- 51% of conversations have a single KEEP customer turn; 49% (20,516 convs)
  have >=2.
- Only 23% of multi-turn conversations fully co-cluster; with >=2 clustered
  turns, only 16% co-cluster. Same-conversation turns SCATTER — the single
  message underdetermines intent.
- 38,413/49,621 noise points (77%) sit in multi-turn conversations: prior
  customer context EXISTS for most noise.
- Transitional/template clusters are 68–88% multi-turn vs 49% corpus-wide
  (c42: 76%, c114: 74%, c115: 81%, c116: 84%, c117: 88%, c124: 68%,
  c125: 77%) — the ambiguous cases are exactly the context-hungry ones.

## Controlled experiment (subset, new embeddings permitted by task)

- Subset: 300 thread-suspect messages (clusters 42/114–117/124/125 + noise
  thread sample) that HAVE a prior in-corpus customer turn.
  `context_probe/probe_subset.csv`.
- Inputs: solo = original `embedding_input`; augmented = `prev_customer_turn
  + " [SEP] " + message`. Same model
  (paraphrase-multilingual-MiniLM-L12-v2, offline cache), normalized.
- Validity: freshly computed solo vs authoritative solo mean cosine = 1.000.
- Test: cosine to own-conversation sibling centroid + rank vs 20 random
  conversation centroids (`probe_results.csv`, `probe_summary.json`).

| metric | solo | + customer context |
|---|---|---|
| mean cosine to own-conv centroid | 0.361 | 0.684 |
| mean rank (of 21) | 5.0 | 1.09 |
| wins | 2 | 171 (127 ties) |

Augmented is better-or-tied in 298/300. Effect is large and directional.

## Interpretation (with limits)

Context materially improves the representation of thread-dependent turns —
this is the expected "shared-tokens-with-siblings" effect, which is precisely
what intent discovery needs for fragments like "Both UPS + link" or "Still
pending". Limits: (a) subset is the EASY case (turns that HAVE a prior turn);
(b) 51% single-turn conversations gain nothing; (c) rank test is a proxy, not
a clustering run — it shows representational gain, not that a full
context-clustering would be better. No pipeline rebuild on this evidence
alone.

## Recommendation

Do NOT silently replace the corpus. DO run context-augmented discovery as a
SECOND VIEW in the next phase: re-embed (same model) only the ambiguous slice
(transitional/template/thread-turn/noise-thread, ~5–8k rows) as
prev-turn + message, cluster that slice separately, and use it to (1) resolve
thread turns, (2) split cluster 7's T4 veneer off its topical content.
Keep the solo-message taxonomy as the reference frame.
