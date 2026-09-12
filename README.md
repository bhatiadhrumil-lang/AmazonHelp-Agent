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
.venv/bin/pytest tests/          # 44 tests (20 discovery + 13 agent + 11 eval)
```

Reproduce the audit and pipeline (exact commands in `REPRODUCIBILITY.md`):

```bash
# 1A: full audit (raw data lives in archive.zip: twcs/twcs.csv)
.venv/bin/python src/data/conversation_quality_audit.py archive.zip \
  --out artifacts/conversation_audit/full_run_fixed
# 1B/1C/1D: see REPRODUCIBILITY.md §2 and scripts/*.py (each persists configs)
# Phase 2A agent demo:
PYTHONPATH=src .venv/bin/python -m agent.cli --message "Where is my order?"
# Phase 3 golden-candidate sampling (no labels assigned):
PYTHONPATH=src .venv/bin/python -m eval.sampling
# Phase 3 annotation (human labels golden_labels.csv):
PYTHONPATH=src .venv/bin/python -m eval.annotate --help
# Phase 3 intent evaluation (once golden_labels.csv exists):
PYTHONPATH=src .venv/bin/python -m eval.run_intent_eval
```

## Human Golden-Set Annotation (workflow v2)

**Why it exists**: the 203 HDBSCAN clusters are NOT ground truth. The only
authoritative intent labels will be human judgments on a 204-candidate sample
(`artifacts/evaluation/golden_candidates.csv`, 12-stratum, seed-documented).
These labels will train/evaluate the final classifier — nothing trains on
cluster IDs as intents.

**Current progress**: 6 / 204 labelled (annotator `dhrumil`); ~198 remain.
Progress is shown on every CLI start (`total | completed | remaining`).

**Command** (start or resume; Ctrl+C safe, never duplicates):
```bash
PYTHONPATH=src .venv/bin/python -m eval.annotate --annotator <name>
```
Options: `--limit N` (batch), `--seed`, `--labels-out <path>` (scratch smoke
tests only — never for real labels).

**Semantics**: the model suggestion (nearest-centroid family + alternatives,
same provisional model as the agent) is display-only context, marked NOT
GROUND TRUTH. The annotator decides via **[A]ccept / [C]hoose (numbered
catalog of the 73 real preliminary families + human-coined list) / [N]ew
(justified) / [U]ncertain**, then writes primary_goal, routing, verdict etc.
Accepting records a HUMAN-CONFIRMED label (`suggestion_outcome=accepted`);
nothing is ever auto-labelled.

**Recorded per row** (17 cols in `golden_labels.csv`): all prior fields plus
`model_suggestion`, `suggestion_outcome` (accepted/corrected/rejected/
uncertain), `annotated_at` (UTC). `candidate_id` doubles as case_id. Pre-v2
rows have blank auditability fields (honest, not backfilled).

**Validation**: enums via numbered menus; ESCALATE requires reason; CLARIFY
requires rationale; OOD forces verdict + explanation; new_intent requires
proposal notes; review screen before save (`-m eval.check_labels` verifies).

**Second opinions**: `needs_second_opinion` flag per row; ≥40 double-labels
planned; `-m eval.agreement` reports raw agreement + Cohen's kappa honestly.

**What remains before classifier training**: ~198 annotations → agreement →
final taxonomy → splits → train/evaluate/calibrate.

## Current status (Phase 3 — validation & classifier, IN PROGRESS)

- **Golden candidates**: `artifacts/evaluation/golden_candidates.csv`
  (204 rows, 12-stratum active-learning-style sample, seed-documented;
  label fields intentionally absent).
- **Human labeling**: BLOCKED — requires a human annotator with
  `artifacts/evaluation/LABELING_INSTRUCTIONS.md` (`PYTHONPATH=src
  .venv/bin/python -m eval.annotate --annotator <name>` writes validated
  rows to `golden_labels.csv`). No labels fabricated.
- **Built and tested (awaiting labels)**: annotation schema + disagreement
  codes, IAA calculator (raw + Cohen's kappa, ≥40 double-labels target),
  final-taxonomy builder, conversation-level splitter (leakage-checked),
  kNN + balanced-LogReg (+optional MLP) baselines on frozen 384D embeddings,
  sigmoid calibration + ECE/Brier, OOD wrapper (prob/margin/distance),
  context-vs-solo experiment, error-analysis builder, eval harness
  (`-m eval.run_intent_eval`), `ValidatedClassifier` drop-in behind the
  existing `IntentClassifier` interface, router OOD-flag plumbing.
- **Final taxonomy / trained classifier / calibration**: code paths built
  and pipeline-smoke-tested on synthetic labels in /tmp only (never reported
  as results); real training awaits human labels. Nothing trains on HDBSCAN
  labels as ground truth.

## Notes & constraints

- **Not built (by design, per phase rules)**: final intent classifier,
  response generator, escalation router, final golden set, frozen taxonomy.
- **Excluded from git** (GitHub 100MB limit; regenerable via
  `REPRODUCIBILITY.md`): `archive.zip`, full `embeddings.npy`, `.venv/`.
- Intent labels describe the **customer goal only** — never response behavior
  or routing. AmazonHelp reply texts are never used in discovery
  representations. HDBSCAN clusters/noise are treated as hypotheses, never
  ground truth.
