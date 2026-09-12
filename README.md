# AmazonHelp-Agent

Customer-support intent discovery on the **TWCS (Customer Support on Twitter)**
dataset, focused on **@AmazonHelp** conversations. Hiver SDE Intern take-home
assignment — discovery phases (no intent classifier, response generator, or
escalation router is built in this repo state).

## What this project does

Turns ~2.8M raw tweets into a structured, evidence-backed understanding of
what customers contact AmazonHelp about:

1. **Phase 1A — Data-quality audit**: rebuilds customer → AmazonHelp
   conversation episodes from the raw dump, filters to genuine problem
   episodes (the KEEP corpus).
2. **Phase 1B — Embeddings → UMAP → HDBSCAN**: embeds the KEEP corpus,
   reduces dimensionality, and clusters into candidate intent groups.
3. **Phase 1C — Cluster interpretation + preliminary taxonomy**: every
   cluster is read and interpreted from real customer messages; merge/split
   candidates, noise analysis, and a human-validation candidate pool are
   produced. Taxonomy stays explicitly *preliminary*.
4. **Phase 1D — Re-clustering investigation**: stress-tests the weak spots
   (a 12,267-point megacluster, 53% noise) with controlled UMAP/HDBSCAN
   experiments and a customer-context probe, ending in an evidence-backed
   strategy recommendation.

## Key numbers (verified)

| Stage | Result |
|---|---|
| Full TWCS rows | 2,811,774 |
| AmazonHelp tweets / connected components | 169,840 / 82,534 |
| Direct customer → AmazonHelp episodes | 100,503 |
| KEEP episodes (working corpus) | 93,171 |
| Embedding model | `paraphrase-multilingual-MiniLM-L12-v2` (384D) |
| UMAP → HDBSCAN (`mcs=30`, `ms=10`) | 8D → **203 clusters**, 43,550 clustered |
| HDBSCAN noise | 49,621 (53.26%) |
| Largest cluster | cluster 7: 12,267 pts (mixed basin, see 1D findings) |
| Tests | 20 passing (`tests/`) |

## Headline findings (Phase 1D)

- **Cluster 7 is a UMAP-created basin, not a density cluster**: in raw 384D
  space it is 98% diffuse (only stub-duplicate cores are dense). Density
  re-splitting was falsified in 4 representation spaces.
- **Dimensionality is not the lever**: global 15D/20D reruns reproduce the
  megacluster at 99.9% overlap, cut noise by only ~1pt, and *fracture* the
  clean merge families. Baseline stands.
- **Noise is mostly recoverable, not junk** (n=341 sample): ~59% matches
  known intent themes, ~20% needs thread context, ~12% social/venting,
  ~4% fragments, ~5% genuinely novel.
- **Customer-side context is the one large-effect lever**: adding the prior
  customer turn moves thread-dependent messages from rank 5.0 → 1.09 toward
  their conversation centroid (298/300 better-or-tied, n=300 controlled
  probe, AmazonHelp replies never used).
- **Recommendation: hybrid (Option D)** — keep the 203-cluster baseline;
  split cluster 7 by non-density (seeded/topic-guided) means; run a
  second-view context clustering on the ambiguous slice only; triage noise
  by bucket. Taxonomy is **not frozen**; human validation is the next step.

## Repository layout

```
src/
  data/conversation_quality_audit.py   # Phase 1A audit (full + smoke)
  discovery/                           # Phase 1B pipeline (config, embeddings,
                                       # UMAP, HDBSCAN, cluster analysis)
scripts/                               # Phase 1C/1D builders (digest, taxonomy,
                                       # noise sampling, re-clustering experiments,
                                       # leakage checks)
tests/                                 # 20 tests (config, embeddings, clustering)
artifacts/
  conversation_audit/                  # 1A outputs + AUDIT_REPORT.md
  discovery/
    embeddings/full/                   # 93,171×384 embeddings + meta
    umap/full/                         # 8D coords + config
    clustering/initial/                # labels, probabilities, reps, analysis
    taxonomy/                          # 1C outputs (interpretation, merges,
                                       # splits, taxonomy, noise, candidates)
    reclustering/                      # 1D experiments + findings + recommendation
REPRODUCIBILITY.md                     # full reproduction guide + process summary
```

## Setup & reproduction

Requires Python 3.12 (`uv` recommended; system Python here is 3.14 — don't use it):

```bash
uv sync                          # creates .venv, installs pinned deps
.venv/bin/pytest tests/          # 20 tests
```

Reproduce the audit and pipeline (exact commands in `REPRODUCIBILITY.md`):

```bash
# 1A: full audit (raw data lives in archive.zip: twcs/twcs.csv)
.venv/bin/python src/data/conversation_quality_audit.py archive.zip \
  --out artifacts/conversation_audit/full_run_fixed
# 1B/1C/1D: see REPRODUCIBILITY.md §2 and scripts/*.py (each persists configs)
```

## Notes & constraints

- **Not built (by design, per phase rules)**: final intent classifier,
  response generator, escalation router, final golden set, frozen taxonomy.
- **Excluded from git** (GitHub 100MB limit; regenerable via
  `REPRODUCIBILITY.md`): `archive.zip`, full `embeddings.npy`, `.venv/`.
- Intent labels describe the **customer goal only** — never response behavior
  or routing. AmazonHelp reply texts are never used in discovery
  representations. HDBSCAN clusters/noise are treated as hypotheses, never
  ground truth.
