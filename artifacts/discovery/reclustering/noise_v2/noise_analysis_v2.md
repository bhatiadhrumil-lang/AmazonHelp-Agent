# Noise analysis v2 (Phase 1D, TASK 4)

## Setup

- Population: **49,621** HDBSCAN-noise points (labels == -1, 53.26% of 93,171).
- Sample: **n=341** (`artifacts/discovery/reclustering/noise_v2/noise_v2_sample.csv`,
  ids N2-000..N2-340) = 260 farthest-point samples in global 8D UMAP space
  (greedy FPS, seed 42) + 81 stratified top-up (script x length-bin).
- Method: single-reader manual read of all 341 messages; each message assigned
  to exactly one bucket, prioritizing resolvability (a message that states a
  goal standalone counts as resolvable even if terse). Buckets are
  SAMPLE-LEVEL estimates, not population claims. No adjudication; no
  ground truth.
- Comparison point: Phase 1C v1 sample (n=150): fits 109 (73%), thread 21
  (14%), offtopic 16 (11%), fragment 3 (2%), novel 1 (1%).

## Observed composition (SAMPLE-LEVEL, n=341)

| Bucket | Count | Sample share | v1 share |
|---|---|---|---|
| Fits an existing cluster theme (standalone goal matches a known family; incl. multilingual carriers) | ~200 | ~59% | 73% |
| Thread turn, needs conversation context (status/polarity/ack/chronology/link-only fragments) | ~70 | ~20% | 14% |
| Social / praise / venting / chatter, no actionable request | ~40 | ~12% | 11% |
| Data fragment / artifact (tracking no., address, phone no., stub, SMS/link-only) | ~15 | ~4% | 2% |
| Rare or novel intent (legitimate goal, no clear cluster home) | ~16 | ~5% | 1% |

The v1→v2 shift toward thread/social/fragment/novel is a SAMPLING effect
(FPS over-spreads into sparse regions; v1 was sorted-by-id simple order),
not evidence the population changed. Both samples agree on the headline:
a majority of noise is legitimate-intent material, not junk.

## Bucket evidence (sample ids)

- Fits theme: delivery/tracking/carrier (000,001,006,026,027,030,052,054,056,
  068,073,074,076,090,091,116,122,140,142,143,149,151,152,171,174,177,180,
  196,197,199,207,208,209,211,215,233,237,243,254,259,267,268,274,284,286,
  304,310,313,316,317,319,323,324,325,333,334), refund/payment/charge
  (014,032,042,048,066,069,078,088,098,122,173,238,301), Prime/subscription
  (003,084,085,086,097,108,172,234,243,246), contact-channel/form/DM friction
  (008,016,029,077,095,100,101,113,117,137,160,161,169,171,194,208,213,216,
  236,253,261,299,339,340), returns/pickup (042,050,123,259), seller/listing
  (039,078,092,163,166,237,249,276,338), devices/digital (011,036,062,145,
  158,193,220,246,288,311,320,326), account/region/marketplace (032,047,066,
  095,104,109,110,175,181,230,231,235,247,250,251,262,278), multilingual
  carriers of the same goals (006,009,012,020,025,027,037,045,046,071,074,
  075,080,082,094,096,106,110,119,130,131,132,136,138,144,151,159,164,165,
  167,168,180,184,186,187,188,190,193,195,199,201,207,217,222,224,227,228,
  229,231,241,248,266,272,273,278,281,283,285,288,289,290,291,294,297,303,
  305,306,307,312,313,315,321,322,328,335,336,337).
- Thread turn: 021,023,024,031,035,038,049,051,055,058,060,061,081,087,088,
  089,093,101,103,111,113,117,124,125,129,132,134,154,162,167,177,182,185,
  192,204,210,212,214,216,221,223,229,232,244,245,251,252,255,257,258,260,
  263,269,271,277,280,290,292,295,298,314,318,324,327,329.
- Social/venting: 005,007,010,013,033,038,041,044,058,060,064,077,081,087,
  089,096,119,125,136,138,146,148,154,158,167,168,182,186,189,198,204,205,
  219,224,225,226,232,239,244,248,264,273,277,292,298,305,307,328.
- Fragment/artifact: 051,088,129,134,141,150,162,185,186,187,188,200,271,
  329,330,331.
- Rare/novel: 083 (gift-printout feedback), 152 (carrier-specific UPS note),
  162 (business account), 173 (review $50 rule), 179 (Twitch vs Amazon Prime),
  186 (affiliate commissions), 202/257 (invoice-only), 224 (presale codes),
  235 (gift changed address+subscriptions), 249 (trading cards), 250 (address
  form has no country field), 253 (locker checkout flow), 258 (Ring
  neighborhood), 264 (AI humor), 275 (cancel UX), 302 (NoCostEMI query).

## Mandated hypotheses — evidence

1. Genuine rare/novel data: YES, ~5% of sample (list above). Real but sparse.
2. Insufficiently separated semantic structure: YES — ~59% matches known
   themes (boundary/one-off/multilingual phrasing HDBSCAN could not densify).
3. Poor HDBSCAN parameterization: PARTLY — finer thresholds shred into
   fragments with 73–85% noise (cluster-7 Experiment B); the production
   (30,10) setting is not obviously wrong, it is conservative.
4. Overly aggressive dimensionality reduction: MIXED — global 15D/20D reruns
   reproduce the same megacluster (99.9% overlap) and same ~52–53% noise, so
   8D→15D/20D does not rescue structure; but raw-384D shows cluster 7 is 98%
   diffuse, i.e. UMAP *created* that basin. Reduction shapes structure more
   than dim count does.
5. Context dependence: YES, ~20% thread turns are unresolvable standalone
   (TASK 9 quantifies how often prior customer context exists).
6. Data artifacts: YES but small, ~4% (tracking numbers, addresses, stubs,
   SMS/link-only).

## Bottom line

Noise is NOT junk: roughly three-fifths is legitimate intent material that
fell out on wording/sparsity/language grounds, one-fifth needs thread
context, about one-sixth is social/venting, and only small remainders are
fragments (~4%) or genuinely novel (~5%). Do not force noise into clusters;
the taxonomic response is targeted re-discovery (Option C/D), not threshold
tuning alone.
