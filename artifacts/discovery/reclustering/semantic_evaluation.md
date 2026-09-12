# Semantic evaluation (Phase 1D, TASK 7)

Question asked: "Which configuration gives the most useful customer-goal
structure?" — judged by reading messages, NOT by metrics.

## dim_15 megacluster 10 (n=12,271; 99.9% = old cluster 7)

30-message random sample: delivery delay/tracking/signature (multiple),
refund/cashback, Prime promise, third-party seller, support friction,
multilingual (FR/ES) carriers of the same goals. Verdict: SAME MIX as old
cluster 7 — coherent=no. Higher-D global UMAP does not fix the megacluster.

## dim_15 cluster 151 (n=1,979) — Prime membership & delivery promise

12-message sample: uniformly Prime-charge/benefit/cancel + Prime delivery
promise complaints ("pay for prime membership", "cancelled my Prime
subscription", "Prime Mitgliedschaft", "NOT a prime customer"). Verdict:
coherent=yes, actionable=yes. Matches old cluster 156 (n=1,967) grown
slightly (+1919 of its members overlap). A keeper intent family.

## dim_15 cluster 93 (n=1,577) — support-experience quality

12-message sample: uniformly complaints about support itself (contradictory /
useless / slow customer service, DE/FR carriers included). Verdict:
coherent=yes as a *sentiment/experience* family, actionable only for
service-quality analytics — NOT a customer goal per se (cf. TASK 9 rule:
keep intent separate from response behavior). Matches old cluster 139
(n=1,521). Keeper as sentiment family, not as intent.

## Cross-config verdict

| Aspect | 8D baseline | 15D | 20D |
|---|---|---|---|
| Megacluster dissolved? | no (7: 12,267) | no (10: 12,271) | no (12: 12,271) |
| Small-cluster stability | — | high (c0 intact, 156→151, 139→93) | high (156→157) |
| Noise | 53.26% | 52.26% | 52.18% |
| Most useful structure | baseline taxonomy stands | same +1pt noise gain, no semantic gain | same |

No configuration is semantically superior: 15D/20D cost ~250s UMAP each for
~1pt noise reduction and zero interpretability gain. The useful-structure
differences are nil; keep the Phase 1B/1C baseline as the reference and treat
the megacluster + noise as discovery problems (TASK 10, Option D).
Fragment configs (eom_10_5, leaf) were rejected without full reads: 73–85%
noise with shard sizes <300 cannot yield stable intents.
