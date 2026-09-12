# Human-validation candidate strategy v2 (Phase 1D, TASK 11)

NO final golden set is created in this phase. This updates the SAMPLING
STRATEGY for the eventual 150–250 hand-labelled examples, incorporating what
re-clustering taught us. Phase 1C's `human_validation_candidates.csv` (185
rows) remains valid as a candidate pool; the strata below say how to draw and
top up from it.

## Strata (with source)

1. Common intents (delivery delay, tracking, refund status, Prime, contact
   channel): largest clusters; ~60 picks. Source: cluster_interpretation
   top-size families.
2. Rare intents (contest, review policy, affiliate, invoice-only, business
   account, Twitch-vs-Prime): ~20 picks. Source: small clusters + noise v2
   rare/novel bucket (N2-083/152/162/173/179/186/202/224/235/249/250/253/
   257/258/264/275/302).
3. Merge boundaries: 2–3 picks per merge group at member-cluster edges
   (nearest-to-other-member texts), MG-01..MG-09: ~25 picks.
4. Split boundaries: cluster-7 T1–T15 candidate sub-intents, 3–4 picks each
   from the C7 diverse sample: ~40 picks. Plus stub-bridge texts
   ("@AmazonHelp Amazon logistics" et al.) as explicit boundary cases.
5. Noise: fits-theme (nearest-to-cluster-boundary points), 15 picks.
6. Contextual: thread-turn messages WITH and WITHOUT resolvable context
   (paired: message alone vs message + prev customer turn), from
   `context_probe/probe_subset.csv`: ~20 picks (10 pairs).
7. Multilingual: ES/FR/DE/IT/PT carriers of T1–T8 goals (NOT English-only
   intents): ~20 picks. Phase 1C pool already has es 18 / fr 6 / hi 3 /
   de 2 — top up IT/PT and DE.
8. OOD: off-topic/social clusters 70/109/122 + noise social bucket: ~10 picks.
9. Difficult/adversarial: veneer-heavy messages (angry + real goal), stubs,
   sarcasm, mixed-goal messages: ~15 picks.

Total guidance ~225 slots; final 150–250 drawn with de-duplication on
(customer_message_id) and conversation spread (no >2 per conversation).

## Labelling protocol notes (for the future golden pass, not now)

- Label the CUSTOMER GOAL, never the response action; sentiment and
  conversation-artifact tags are separate axes (kind=artifact/sentiment/ood
  already in interpretation schema — reuse them).
- Thread-turn items are labelled WITH their customer-side context shown;
  record whether the label was resolvable without it.
- Cluster-7 sub-intent labels stay CANDIDATE until inter-annotator agreement
  is measured on stratum 4.
