# AmazonHelp-Agent

Customer-support **intent discovery** on the **TWCS (Customer Support on Twitter)**
dataset, focused on **@AmazonHelp** conversations. Hiver SDE Intern take-home:
turn ~2.8M raw tweets into an evidence-backed understanding of what customers
contact AmazonHelp about, build a provisional support agent on top of it, and
put human-validated labels behind the whole pipeline before anything is called
"final".

> **Status in one line**: discovery (1A–1D) and the provisional Phase-2A agent
> are **complete and verified**; Phase-3 human validation is **in progress**
> (83/204 golden examples labelled); the *final* intent classifier, calibrated
> routing/response thresholds, and frozen taxonomy are **not yet built — by
> design**, pending the golden set.

---

## Assignment requirements & implementation status

> ⚠️ **No standalone assignment-spec file exists in this repo.** The phases below
> are reconstructed from the `Phase N` / `TASK N` references embedded in the
> source and `docs/`. Every claim below was verified against code and tests, not
> assumed. Legend: ✅ done & verified · 🟡 in progress · 🔲 built & tested but blocked on inputs · ❌ not built.

| # | Requirement (reconstructed) | Status | Evidence |
|---|---|---|---|
| 1A | Conversation-quality audit: rebuild customer→AmazonHelp episodes, filter to genuine problem episodes (KEEP corpus) | ✅ | `src/data/conversation_quality_audit.py`; `artifacts/conversation_audit/full_run_fixed/`; `REPRODUCIBILITY.md` §2–5 |
| 1B | Embeddings → UMAP → HDBSCAN discovery pipeline, fully reproducible | ✅ | `src/discovery/*` (config, embeddings, UMAP, HDBSCAN, cluster analysis); `artifacts/discovery/**`; `REPRODUCIBILITY.md` §7–8 |
| 1C | Interpret every cluster; produce preliminary taxonomy + merge/split candidates + noise analysis + human-validation pool | ✅ | `cluster_interpretation.csv` (203 rows, 73 families), `preliminary_taxonomy.csv/.md`, `noise_analysis.md`, `human_validation_candidates.csv` (185) |
| 1D | Stress-test weak spots (12,267-pt megacluster, 53% noise); deliver evidence-backed strategy | ✅ | `artifacts/discovery/reclustering/recommendation.md`, `cluster_7/`, `global_umap_compare/`, `validation_strategy_v2.md` |
| 2A | Agent foundation: retrieval over KEEP corpus + provisional intent/entities/evidence/router/response + local CLI demo | ✅ (provisional, **uncalibrated**) | `src/agent/*`; `docs/agent_architecture.md`; CLI demo verified below |
| 3 | Golden-candidate sampling (labels never come from cluster IDs) | ✅ | `golden_candidates.csv` (204 rows, seed-documented), `sampling_report.md` |
| 3 | Human golden labels | 🟡 **83 / 204** (annotator `dhrumil`, 36 intents) | `golden_labels.csv`; `-m eval.check_labels` → **VALID** |
| 3 | Inter-annotator agreement (≥40 double-labels, raw + Cohen's κ) | ❌ 0 double-labels so far | `-m eval.agreement` |
| 3 | Final taxonomy built from human labels | 🔲 blocked on labels | `src/eval/taxonomy_builder.py` |
| 3 | Conversation-level, leakage-checked train/val/test splits | 🔲 built, needs labels | `src/eval/splits.py` |
| 3 | Classifier baselines (kNN / balanced-LogReg / MLP) + sigmoid calibration + OOD wrapper + eval harness | 🔲 built, pipeline-smoke-tested on **synthetic** labels only | `src/eval/classify.py`, `run_intent_eval.py`; `tests/` |
| 3 | Context-vs-solo experiment (1-turn vs +prev customer turn) | 🔲 blocked on splits | `src/eval/context_exp.py` |
| 3 | Final trained + calibrated classifier (`ValidatedClassifier`) | 🔲 blocked on labels | `src/eval/train_final.py`, `src/agent/validated.py` |
| — | Production-calibrated agent thresholds + frozen taxonomy | ❌ by design (gate: golden validation) | `docs/agent_architecture.md` |

---

## Architecture

The Phase-2A agent (`docs/agent_architecture.md`) is a **pipeline of swappable
components** wired at runtime; nothing in it claims production readiness.

```
IncomingMessage (+ optional prior customer turns)
  -> ContextBuilder          customer-side only, bounded (3 turns / 1500 chars)
  -> IntentClassifier        PROVISIONAL nearest-centroid over 203 clusters
  -> EntityExtractor         PROVISIONAL patterns (URL/EMAIL/PHONE/MONEY/CARRIER/...)
  -> Retriever               sklearn brute-force cosine over 93,171 existing 384D rows
  -> EvidenceAssessor        sufficient/insufficient + reason + risk flags
  -> DecisionRouter          AUTO / CLARIFY / ESCALATE (configurable, uncalibrated)
  -> ResponseGenerator       stub: grounded-only templated draft, or safe handoff
  -> AgentResult (+ structured trace, no chain-of-thought)
```

| Module (`src/agent/`) | Owns | Never does |
|---|---|---|
| `contracts.py` | All dataclass schemas, JSON-serializable | Logic |
| `cases.py` | KEEP-only store, id→embedding-row join | Assumes row order |
| `retrieval.py` | Exact cosine search, query encoding (customer text only) | Embeds replies into queries |
| `intent.py` | `IntentClassifier` interface + provisional adapter | Claims validated accuracy |
| `context.py` | Bounded customer-side context; `intent_text()` | Includes agent replies in intent text |
| `entities.py` | `EntityExtractor` interface + pattern v0 | Invents order-ID regex; requests secrets |
| `evidence.py` | Sufficiency verdict + reason + flags | Hard-codes production thresholds |
| `respond.py` | `ResponseGenerator` interface + refusing stub | Unrestricted chat; invented policy |
| `router.py` | AUTO/CLARIFY/ESCALATE + versioned policy | Arbitrary production cutoffs |
| `agent.py` | Orchestration + fail-safe guards | Exposes chain-of-thought |
| `cli.py` | Local demo (`python -m agent.cli`) | Internal details |
| `validated.py` | Post-training drop-in for the intent classifier | Runs without a trained `final_model/` |

Key distinctions (see `docs/agent_architecture.md` for the full text):

- **Intent confidence ≠ evidence sufficiency** — separate components; a confident
  intent with weak evidence can never AUTO, and strong evidence with an
  artifact/contextual/ood/sentiment intent can never AUTO.
- **Historical replies are evidence idioms** ("support previously said X in a
  similar case", quoted with source ids), never presented as the correct answer.
- **Everything carries `provisional` / `v0-uncalibrated` flags** — confidence
  numbers are wiring-only until calibrated on golden data.
- **Component replacement is injection-based**: implement the relevant interface
  and pass it to `SupportAgent(...)`; no other file changes. Router/assessor
  cutoffs live in exactly two dataclasses.

---

## Implemented features

### Completed & verified
- Phase 1A: full corpus audit (2,811,774 rows → 100,503 direct episodes → 93,171
  KEEP), with smoke + full runs, reproducible commands, and a documented bug fix
  (`build_root_map` dropped 395 episodes; fixed + re-verified, `REPRODUCIBILITY.md` §4–5).
- Phase 1B: resume-safe 384D embedding generation (customer text only) with
  memmap + alignment sidecar; UMAP 8D; HDBSCAN `mcs=30, ms=10` → 203 clusters;
  per-cluster representative selection (diverse, centroid-near) + diagnostics.
- Phase 1C: per-cluster interpretation → 73 intent families (`cluster_interpretation.csv`),
  merge groups MG-01..MG-09, split candidates, noise classification (n=341), a
  185-row human-validation candidate pool, exact-duplicate/leakage checks.
- Phase 1D: controlled re-clustering experiments (4 representation spaces, global
  15D/20D, finer HDBSCAN, customer-context probe n=300) → **Option D (hybrid)**
  recommendation; `validation_strategy_v2.md` defines the golden sampling strata.
- Phase 2A: full agent foundation with **fail-safe guarantees** — any component
  exception, empty/garbage input, weak or conflicting evidence, account-private
  content, or OOD → CLARIFY/ESCALATE, never a fabricated AUTO answer.
- Phase 3 tooling: 204-candidate stratified sampler, annotation CLI (workflow v2),
  copilot drafts (204/204 model recs), deterministic review queue (P1–P5), label
  schema + validation, IAA calculator, splits, classifier baselines + calibration
  + OOD + eval harness, context experiment, taxonomy builder, error analysis,
  final-model trainer, `ValidatedClassifier` drop-in.
- Now verified this pass: `pytest` 56/57, `check_labels` VALID, agent CLI demo AUTO.

### Provisional (built, honestly labeled — not production-ready)
- Intent: nearest-family-centroid over 203 clusters; confidence = raw cosine (**uncalibrated**).
- Entities: pattern-based v0 (URL/EMAIL/PHONE/MONEY/CARRIER + marketplaces); no
  fabricated order-id regex; account-private content is never solicited and always escalates.
- Response: grounded-only stub; refuses to draft without sufficient evidence.
- Routing: qualitative safety rules on top of `v0-uncalibrated` cutoffs.

### Not yet implemented / blocked
- Remaining 121 human labels; second-annotator double-labels (IAA); final
  taxonomy; real (non-synthetic) splits and eval runs; trained + calibrated
  `final_model/`; calibrated agent thresholds; frozen taxonomy.

---

## Dataset documentation

Raw data ships as **`archive.zip`** (GitHub 100MB limit; **regenerable / git-ignored**):
`twcs/twcs.csv` (516.5 MB; 2,811,774 rows) + `sample.csv`. It is the public
**TWCS — Customer Support on Twitter** dataset, filtered here to `@AmazonHelp`.

| Column | Meaning |
|---|---|
| `tweet_id` | Unique tweet id (message id) |
| `author_id` | Author handle (e.g. `AmazonHelp`, or a customer) |
| `inbound` | True = customer→brand direction |
| `created_at` | Timestamp (`%a %b %d %H:%M:%S %z %Y`) |
| `text` | Tweet text |
| `response_tweet_id` | Reply tweet (id or empty) |
| `in_response_to_tweet_id` | Parent tweet this replies to (id or empty) |

Derived corpora (all under `artifacts/`, git-ignored where too large):

| Corpus | Rows | Where |
|---|---|---|
| AmazonHelp-connected components | 82,534 (KEEP 42,408 / FLAG 2,193 / EXCLUDE 37,933) | `conversation_audit/full_run_fixed/conversation_components_audit.csv` |
| Direct customer→AmazonHelp episodes | 100,503 (KEEP 93,171 / FLAG 5,653 / EXCLUDE 1,679) | `…/customer_problem_episodes.csv` |
| **KEEP corpus (working set)** | 93,171 | episodes CSV filtered to `KEEP` |
| Embeddings | 93,171 × 384 float32 | `discovery/embeddings/full/embeddings.npy` (+ `embeddings_meta.csv` alignment) |
| UMAP coords | 93,171 × 8 | `discovery/umap/full/umap_coords.npy` |
| HDBSCAN labels | 203 clusters / 49,621 noise (53.26%) | `discovery/clustering/initial/labels.npy` etc. |
| Retrieval index | 93,171 × 384 cosine index + 73 provisional centroids | `retrieval/main/`, `retrieval/provisional_centroids.npy` |
| Golden candidates | 204 rows (labels absent by design) | `evaluation/golden_candidates.csv` |

Representation hygiene (enforced in code + tests): embeddings/query inputs are
**customer text only** — AmazonHelp replies, parent text, and downstream
resolution are never included; cluster IDs are **hypotheses, never ground truth**.

---

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
| Taxonomy families (preliminary) | 73 |
| Golden candidates / human-labelled | 204 / **83** (36 intents) |
| Retrieval index cases × dim | 93,171 × 384 |
| Tests | **56 / 57 passing** (1 stale assertion, see *Current status*) |

---

## Headline findings (Phase 1D)

- **Cluster 7 is a UMAP-created basin, not a density cluster**: in raw 384D
  space it is 98% diffuse (only stub-duplicate cores are dense). Density
  re-splitting was falsified in 4 representation spaces.
- **Dimensionality is not the lever**: global 15D/20D reruns reproduce the
  megacluster at 99.9% overlap, cut noise by only ~1pt, and *fracture* the clean
  merge families. Baseline stands.
- **Noise is mostly recoverable, not junk** (n=341 sample): ~59% matches known
  intent themes, ~20% needs thread context, ~12% social/venting, ~4% fragments,
  ~5% genuinely novel.
- **Customer-side context is the one large-effect lever**: adding the prior
  customer turn moves thread-dependent messages from rank 5.0 → 1.09 toward their
  conversation centroid (298/300 better-or-tied, n=300 controlled probe;
  AmazonHelp replies never used).
- **Recommendation: hybrid (Option D)** — keep the 203-cluster baseline; split
  cluster 7 by non-density (seeded/topic-guided) means; run a second-view context
  clustering on the ambiguous slice only; triage noise by bucket. Taxonomy is
  **not frozen**; human validation is the next step.

---

## Repository layout

```
src/
  data/conversation_quality_audit.py   # Phase 1A audit (full + smoke)
  discovery/                           # Phase 1B pipeline (config, embeddings,
                                       # UMAP, HDBSCAN, cluster analysis)
  agent/                               # Phase 2A agent foundation (contracts,
                                       # context, retrieval, intent, entities,
                                       # evidence, router, respond, agent, cli,
                                       # validated) + docs/agent_architecture.md
  eval/                                # Phase 3 validation tooling (sampling,
                                       # schema, annotate, copilot_draft,
                                       # build_review_queue, check_labels,
                                       # agreement, splits, classify,
                                       # run_intent_eval, train_final,
                                       # context_exp, taxonomy_builder, errors)
scripts/                               # Phase 1C/1D builders (digest, taxonomy,
                                       # noise sampling, re-clustering experiments,
                                       # leakage checks)
tests/                                 # 57 tests (agent, eval, discovery)
docs/                                  # agent_architecture.md
REPRODUCIBILITY.md                     # full reproduction guide + process summary
artifacts/
  conversation_audit/                  # 1A outputs + AUDIT_REPORT.md
  discovery/                           # embeddings, umap, clustering, taxonomy, reclustering
  retrieval/                           # cosine index + provisional centroids
  evaluation/                          # golden candidates/labels, drafts, review
                                       # queue, LABELING instructions, sampling report
archive.zip                            # TWCS dataset (git-ignored)
```

---

## Setup & reproduction

Requires Python 3.12 (`uv` recommended; system Python here is 3.14 — don't use it):

```bash
uv sync                          # creates .venv, installs pinned deps (torch CPU index)
.venv/bin/pytest tests/ -q       # 57 tests (see "Current status" 1-failure note)
```

Reproduce the audit and pipeline (exact commands in `REPRODUCIBILITY.md`):

```bash
# 1A: smoke audit (47,211-row subset)
.venv/bin/python src/data/conversation_quality_audit.py \
  artifacts/smoke/smoke_subset.csv --out artifacts/conversation_audit/smoke_run_fixcheck
# 1A: full audit (raw data lives in archive.zip: twcs/twcs.csv)
.venv/bin/python src/data/conversation_quality_audit.py archive.zip \
  --out artifacts/conversation_audit/full_run_fixed
# 1B/1C/1D: see REPRODUCIBILITY.md §7 and scripts/*.py (each persists configs)
```

Phase 2A agent demo (verified — returns AUTO with evidence on this query):

```bash
PYTHONPATH=src .venv/bin/python -m agent.cli --message "Where is my order? It said arriving today."
PYTHONPATH=src .venv/bin/python -m agent.cli --message "Where is my order?" --json   # machine-readable trace
# options: --conversation-id C, --prior "earlier turn", --top-k N
```

Phase 3 commands (annotation tooling works now; eval pipeline shows BLOCKED until labels + splits exist):

```bash
PYTHONPATH=src .venv/bin/python -m eval.annotate --annotator <name>       # human labels -> golden_labels.csv
PYTHONPATH=src .venv/bin/python -m eval.copilot_draft                     # 204/204 model recs (never labels)
PYTHONPATH=src .venv/bin/python -m eval.build_review_queue                # P1-P5 review order
PYTHONPATH=src .venv/bin/python -m eval.check_labels                      # schema/consistency validator
PYTHONPATH=src .venv/bin/python -m eval.agreement                         # IAA (once ≥2 annotators)
PYTHONPATH=src .venv/bin/python -m eval.run_intent_eval --model logreg    # BLOCKED until golden_labels.csv + label_splits.csv
PYTHONPATH=src .venv/bin/python -m eval.errors <eval_dir>                 # error_analysis.md from an eval run
```

---

## Human golden-set annotation (workflow v2)

**Why it exists**: the 203 HDBSCAN clusters are **NOT ground truth**. The only
authoritative intent labels are human judgments on a 204-candidate sample
(`artifacts/evaluation/golden_candidates.csv`, 12-stratum, seed-documented).
These labels train/evaluate the final classifier — nothing trains on cluster IDs
as intents.

**Current progress**: **83 / 204** human-labelled (annotator `dhrumil`, 36 distinct
intents); 121 remain. Progress is shown on every CLI start (`total | completed | remaining`).

**Command** (start or resume; Ctrl+C safe, never duplicates):
```bash
PYTHONPATH=src .venv/bin/python -m eval.annotate --annotator <name>
```
Options: `--limit N` (batch), `--seed`, `--labels-out <path>` (scratch smoke
tests only — never for real labels).

**Semantics**: the model suggestion (nearest-centroid family + alternatives, same
provisional model as the agent) and the draft MODEL RECOMMENDATION
(`annotation_draft.csv`) are display-only assistance, marked NOT GROUND TRUTH.
The annotator decides via **A / C / N / U**:
A = accept the displayed model recommendation (`suggestion_outcome=accepted`);
C = correct to a different existing intent (`corrected`); N = new intent
(justified, notes required); U = uncertain/context-dependent. Nothing is ever
auto-labelled without pressing **A + Y**.

**Recorded per row** (17 cols in `golden_labels.csv`): all prior fields plus
`model_suggestion`, `suggestion_outcome`, `annotated_at` (UTC). Pre-v2 rows have
blank auditability fields (honest, not backfilled). `candidate_id` doubles as case_id.

**Validation**: enums via numbered menus; ESCALATE requires reason; CLARIFY
requires rationale; OOD forces verdict + explanation; new_intent requires proposal
notes; FINAL REVIEW before save. `-m eval.check_labels` verifies → currently
**VALID (83 rows, 1 annotator, 36 intents; outcomes: accepted 65 / corrected 11 /
legacy-blank 7)**.

**Annotation copilot**: `src/eval/copilot_draft.py` writes model-only drafts to
`annotation_draft.csv` (+ `annotation_progress.json`) and **never** touches
`golden_labels.csv`. Current draft: 204 / 204 model recommendations
(status=`model_recommendation`). Run/resume:
`PYTHONPATH=src .venv/bin/python -m eval.copilot_draft [--limit N] [--force]`.
CSV uses QUOTE_MINIMAL so commas/quotes/multiline round-trip (test-verified).

**Human-review queue**: `src/eval/build_review_queue.py` builds
`annotation_review_queue.csv` + `annotation_review_summary.json` — review order
only, never changes labels. Priority rules (deterministic, tie-break
`candidate_id`): P5 taxonomy/ambiguity attention; P4 needs_second_opinion=yes;
P3 confidence LOW; P2 MEDIUM/fallback; P1 HIGH+fits+unambiguous (fastest first).
⚠️ The committed summary was generated at **9 verified**; regenerate with the
command above after label progress (now 83). `eval.annotate` follows this queue
when present; the human still explicitly A/C/N/U + save.

**Second opinions**: `needs_second_opinion` flag per row; ≥40 double-labels
planned; `-m eval.agreement` reports raw agreement + Cohen's κ honestly
(currently 0 double-labelled).

---

## Current status (Phase 3 — validation & classifier, IN PROGRESS)

- **Golden candidates**: `artifacts/evaluation/golden_candidates.csv` (204 rows,
  12-stratum active-learning-style sample, seed-documented; label fields
  intentionally absent).
- **Human labeling**: **83 / 204** done (`golden_labels.csv`, annotator
  `dhrumil`, 36 intents; `check_labels` VALID). Labels are genuine human
  judgments — nothing is auto-fabricated. Routing expectations so far:
  clarify 6 / escalate 61 / auto_ok 16; taxonomy verdicts: fits 81 /
  context_dependent 1 / new_intent 1.
- **Built & tested (awaiting more labels)**: annotation schema + disagreement
  codes, IAA calculator (raw + Cohen's κ), final-taxonomy builder,
  conversation-level splitter (leakage-checked), kNN + balanced-LogReg (+optional
  MLP) baselines on frozen 384D embeddings, sigmoid calibration + ECE/Brier, OOD
  wrapper (prob/margin/distance), context-vs-solo experiment, error-analysis
  builder, eval harness, `ValidatedClassifier` drop-in behind the existing
  `IntentClassifier` interface, router OOD-flag plumbing.
- **Pipeline smoke-tested on synthetic labels only** (in `/tmp`, never reported
  as results): `run_intent_eval` for knn+logreg, splits, taxonomy builder. Real
  numbers await human labels — nothing has been reported as an accuracy result.
- **Tests**: 56 / 57 pass. ⚠️ `tests/test_eval.py::test_existing_human_labels_unchanged`
  currently **fails**: it hardcodes the original 9 golden labels, but the file now
  has 83 (labeling progressed). It is a **stale regression assertion, not a
  product bug** — it must be relaxed (e.g. `.assert len(rows) >= 9` and the
  original 9 ⊆ ids) as annotation continues.
- **Final taxonomy / trained classifier / calibrated routing**: code paths built;
  real training awaits labels + splits. Nothing trains on HDBSCAN labels as
  ground truth.

---

## Remaining work (priority order)

1. **Relax the stale 9-label test assertion** so the suite is green again
   (currently 56/57). ⚠️ Out of scope of a README-only change; needs a one-line
   test edit.
2. **Finish human annotation 83 → 204** (121 left) via `eval.annotate`,
   following the regenerated review queue; refresh
   `annotation_review_queue.csv` / `annotation_review_summary.json`.
3. **Second annotator + IAA**: ≥40 double-labels; run `eval.agreement`
   (raw + Cohen's κ); resolve disagreement cases
   (`agreement_disagreements.csv`).
4. **Final taxonomy**: `eval.taxonomy_builder` on consolidated labels
   (fold in human new-intent / merge / split / context-dependent / megacluster
   proposals).
5. **Splits**: `eval.splits` (conversation-level, leakage-checked) →
   `label_splits.csv`.
6. **Evaluate baselines**: `eval.run_intent_eval --model {knn,logreg,mlp}` →
   metrics, report, confusion matrix, per-intent, reliability, config.
7. **Context experiment**: `eval.context_exp` (message-only vs +prev-turn) on
   the held-out test split.
8. **Error analysis + iteration**: `eval.errors <eval_dir>`; iterate taxonomy /
   features on the confusion evidence.
9. **Train final classifier**: `eval.train_final` →
   `artifacts/evaluation/final_model/` consumed by `ValidatedClassifier`.
10. **Calibrate the agent**: fit `AssessConfig` / `RouterPolicy` cutoffs on
   golden evidence, bump versions (`docs/agent_architecture.md` §Replacing).
11. **Ship-ready pass**: copy-edit response drafts, freeze taxonomy (only after
    validation), and (optionally) wire a runtime
    `Retriever`/`ValidatedClassifier` outside the CLI.

---

## Notes & constraints

- **Not built (by design, per phase rules)**: *final* calibrated intent
  classifier, calibrated response draft generator, calibrated escalation router,
  frozen taxonomy, complete golden set. The agent's classifier/responder/router
  exist in **provisional form** and are honest about it.
- **Excluded from git** (GitHub 100MB limit; regenerable via
  `REPRODUCIBILITY.md`): `archive.zip`, full `embeddings.npy`, `.venv/`.
- Intent labels describe the **customer goal only** — never response behavior or
  routing. AmazonHelp reply texts are never used in discovery representations.
  HDBSCAN clusters/noise are treated as hypotheses, never ground truth.
- Agent safety: no chain-of-thought exposure; account-private content escalates;
  no response is ever drafted without grounded evidence.