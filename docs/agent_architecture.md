# Agent architecture (Phase 2, TASK 18)

## Data flow

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

## Module responsibilities (`src/agent/`)

| Module | Owns | Never does |
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

## Key distinctions

- **Intent confidence vs evidence sufficiency**: separate fields, separate
  components. A confident intent with weak evidence cannot AUTO; strong
  evidence with an artifact/contextual/ood/sentiment intent cannot AUTO.
  Only `kind == "intent"` + sufficient evidence + placeholder bars may AUTO.
- **Historical response role**: retrieved replies are *evidence idioms*
  ("support previously said X in a similar case"), quoted with source ids in
  stub drafts. Never presented as the correct answer.
- **Provisional vs final**: every adapter/extractor/assessor/router/governor
  carries `provisional` flags or `v0-uncalibrated` versions. Confidence
  numbers are wiring-only until calibrated on golden data.

## Replacing components

- **Classifier**: implement `IntentClassifier.predict(context)` (load any
  label space; `intent_id` is a free string, taxonomy is NOT imported by the
  agent — the adapter loads `cluster_interpretation.csv` itself). Inject via
  `SupportAgent(intent=...)`. No other file changes.
- **Response provider**: implement `ResponseGenerator.generate(...)` keeping
  the grounding contract (`grounded=True` only if every claim traces to
  inputs/evidence). Inject via `SupportAgent(responder=...)`.
- **Routing calibration**: fit `AssessConfig`/`RouterPolicy` cutoffs on the
  future golden set; bump `version`; thresholds live in exactly two
  dataclasses, nowhere else.

## Research-artifact preservation (TASK 19)

Untouched: `embeddings.npy` (sha256-verified), `umap_coords.npy`,
`labels.npy`, audit CSVs, `taxonomy/` outputs. New artifacts only under
`artifacts/retrieval/` (index sidecar + provisional centroids) and
`artifacts/agent/` (reserved for runtime logs, currently empty by design).
No golden set created (TASK 20).
