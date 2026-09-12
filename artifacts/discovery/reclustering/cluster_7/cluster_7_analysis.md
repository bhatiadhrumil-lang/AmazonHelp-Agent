# Cluster 7 deep analysis (Phase 1D, TASK 2)

- Cluster: 7 (initial HDBSCAN, `min_cluster_size=30, min_samples=10`, 8D UMAP)
- Size: **12,267 points** (28.2% of clustered corpus; 13.2% of all 93,171)
- Phase 1C label: `megacluster_unclear` (coherent=no, confidence=low)
- Method: diverse sample of **n=268** = 220 farthest-point samples in the existing
  8D UMAP space (greedy FPS on standardized coords, seed 7) + 48 stratified
  top-up (script x length-bin). Sample file:
  `artifacts/discovery/reclustering/cluster_7/c7_diverse_sample.csv`
  (columns: sample_id C7-000..C7-267, corpus_row for traceability, script,
  lenbin, customer_message_id, conversation_id, created_dt, text).
- Deliberately NOT centroid-nearest: FPS forces coverage of the cluster's full
  occupied volume.

## Bulk signals (full 12,267, measured)

- Length: mean 140 chars vs corpus mean 113; median 138; p10/p90 = 55/253;
  min 20, max 322 (corpus max is also 322 — short-message corpus by construction).
- Exact-duplicate share: **0.019** (only ~2% of members share an exact text) —
  NOT a duplicate-driven cluster. Top dups are stubs like
  "@AmazonHelp Amazon logistics" (19x), "@AmazonHelp Amazon.in" (17x),
  "@AmazonHelp Por Amazon" (13x): carrier/marketplace-name-only messages.
- `has_url` share 0.069 (vs higher in URL-driven clusters like 59 at 0.99).
- `is_acknowledgment_like` share 0.0 — no pure thanks/closure content.
- Script: 11,355 latin_plain / 912 latin_acc in full cluster (7.4% accented).
  CJK/Arabic/Devanagari/Cyrillic scripts ~0 in cluster 7 (multilingual = ES/FR/DE/IT/PT, not non-Latin scripts).
- Date range 2015-06 → 2017-12, same as corpus; no time-slice artifact.

## What the 268 samples show (SAMPLE-LEVEL, n=268 — not cluster-wide claims)

Buckets below are my manual read of each sampled message. A message can carry
a support-experience veneer *plus* an underlying topic; I bucketed by the
underlying actionable goal first, veneer second.

| # | Theme (underlying customer goal) | Sample count | Sample share | Example sample_ids |
|---|---|---|---|---|
| T1 | Delivery problems: delay, missed window, tracking, address/driver, carrier-specific (esp. Amazon Logistics/AMZL), failed delivery | ~95 | ~35% | C7-000,005,007,024,029,030,046,054,061,066,071,072,100,111,113,128,139,142-146,156,171,175,182,185,196,204,208,209,212,220,224,226,232-234,239,242,244,247,249 |
| T2 | Prime membership: charges, benefit/delivery promise, cancellation, Prime Day/promise mismatch | ~27 | ~10% | C7-002,036,050,055,115,127,168,178,179,191,209,228,229,237,249,250,266,267 |
| T3 | Refund / compensation / payment flows: refund delay, wrong destination, double charge, gift-card, EMI glitch | ~27 | ~10% | C7-008,019,038,045,055,062,078,088,113,147,151,164,168,183,184,187,205,262,265 |
| T4 | Support-experience complaint as the *primary* content: long wait, no reply, contradictory reps, channel switching, form/DM friction | ~30 (overlaps T1–T3) | ~11% net-new | C7-001,003,018,031,048,053,058,063,096,102,116,133,148,156,163,172,184,195,200,205,216,221,223 |
| T5 | Third-party seller / counterfeit / listing integrity | ~16 | ~6% | C7-016,028,086,100,132,149,155,164,211,242,255,260,266 |
| T6 | Returns / pickups / rescheduling | ~11 | ~4% | C7-053,067,111,145,236,254 (+029 pickup) |
| T7 | Devices / apps / digital: Kindle, Fire, Alexa/Echo, Prime Video, Amazon app, Music | ~22 | ~8% | C7-010,012,014,049,057,064,124,153,174,177,190,197,202,213,225,227,253,259 |
| T8 | Region / marketplace / account / cross-border (incl. first-order help, login, marketplace mismatch) | ~22 | ~8% | C7-009,035,039,043,074,080,095,104,108,121,130,131,141,157,160,162,188,194,199,211,231,235,240,243,250,257 |
| T9 | Social / praise / venting / chatter with no actionable request | ~30 | ~11% | C7-011,034,040,041,081,082,089-093,097,101,122,124,136,138,150,152,201,207,210,215,222,245,246,248,252,263 |
| T10 | Contest / quiz | ~1 | <1% | C7-042 |
| T11 | Non-English carrying any of T1–T9 (ES/FR/DE/IT/PT; slightly oversampled by design via latin_acc stratum) | ~45 (overlap) | ~17% of sample | C7-007,010,013,015,017,021,023,035,040,051,052,056,060,068,073,075,076,098,105,107,108,110,121,123,136,140,141,160,161,167,170,176,180-182,190,193,201,203,212,215,224,232,236,240,242,245,246,254,261,264 |

## Candidate sub-intents (for re-clustering validation)

1. delivery_delay_missed_window, 2. carrier_specific_logistics (AMZL-first),
   3. tracking_status_query, 4. address_driver_failed_delivery,
   5. prime_charge_benefit_cancel, 6. refund_status_destination,
   7. payment_charge_dispute, 8. support_waiting_no_reply,
   9. contradictory_support_channel_friction, 10. third_party_seller_counterfeit,
   11. return_pickup_reschedule, 12. device_app_digital_help,
   13. region_marketplace_account, 14. social_praise_chatter (OOD-adjacent),
   15. venting_no_actionable_request (sentiment).

## Why HDBSCAN merged them (evidence)

- Shared surface form: nearly every message contains "@AmazonHelp" + ("Amazon"
  / "prime" / "delivery" / "refund" / "support") with ~100–180 chars. In 8D
  UMAP this surface similarity collapses distinct topics into one basin.
- Sentiment veneer is cross-cutting: anger/impatience words co-occur with all
  of T1–T8, so density connects across topics instead of separating by them.
- Short stubs ("@AmazonHelp Amazon logistics", marketplace names like
  "Amazon.in", "Amazon.de", "Por Amazon") act as bridges: they are near every
  topic in embedding space and glue the basin together.
- Low exact-dup (0.019) rules out the trivial explanation; this is semantic
  collapse, not duplication.

## Is re-clustering justified?

**Yes.** The sample contains multiple (≥10) distinct, actionable customer
goals (T1–T8), each with dozens of sample witnesses. Re-clustering ONLY
cluster 7 on the original 384D embeddings with higher UMAP dimensionality
(15D/20D) and varied HDBSCAN density thresholds is justified. Expectation to
test: topic vocabulary (carrier names, refund, Prime, seller, device words)
separates in higher-D space; the sentiment veneer + stubs may still form one
residual sub-cluster, which is itself an informative outcome. Context
dependence is moderate (T4/template-ish turns exist but most samples state
their goal standalone), so re-clustering without context is the right first
step; context experiment (TASK 9) stays separate.
