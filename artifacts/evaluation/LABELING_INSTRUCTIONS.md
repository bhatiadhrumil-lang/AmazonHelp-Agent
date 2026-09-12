# Golden-label annotation instructions (workflow v2 — fast, structured, auditable)

You will label ~204 customer messages to @AmazonHelp (6 done, ~198 remain).
Your labels become the authoritative ground truth. Cluster IDs and model
suggestions are context ONLY — never copy them blindly.

## Starting / resuming (same command)

```bash
PYTHONPATH=src .venv/bin/python -m eval.annotate --annotator <your-name>
```

On start you will see e.g. `204 total | 6 completed | 198 remaining`.
Ctrl+C is safe (every save is flushed); re-running resumes automatically and
never duplicates a saved annotation. `--limit N` does a batch; `--labels-out`
routes output to a scratch file (testing only — never for real labels).

## The fast flow (per item)

1. Read MESSAGE, prior customer turns, and the historical reply (evidence only).
2. Read the MODEL SUGGESTION — NOT GROUND TRUTH (nearest-centroid family +
   alternatives, same provisional model as the agent).
3. Decide with one key:
   - **[A] Accept** — you reviewed and confirm the suggestion (recorded as a
     HUMAN-CONFIRMED label, outcome=accepted; you still write primary_goal etc.).
   - **[C] Choose existing** — numbered catalog of the 73 real preliminary
     families (filter by substring) plus human-coined intents so far.
   - **[N] New intent** — only when justified; taxonomy_notes REQUIRED.
   - **[U] Uncertain** — verdict limited to ambiguous/context_dependent/ood.
4. Numbered menus for routing (1=auto_ok 2=clarify 3=escalate 4=unsure) and
   taxonomy verdict (1=fits 2=merge 3=split 4=new_intent 5=ood 6=ambiguous
   7=context_dependent).
5. Defaults are shown and enforced: AUTO→escalation blank; ESCALATE→reason
   required; CLARIFY→clarification rationale required; OOD→verdict forced to
   ood + explanation required.
6. Entities: `0` for none (quick); otherwise type+value pairs.
7. **Review screen → [s]ave / [r]edo.** Only [s]ave writes the record, with a
   UTC timestamp and the suggestion outcome (accepted/corrected/rejected/
   uncertain) that distinguishes YOUR decision from the model's suggestion.

## How to label (unchanged rules)

1. the customer message (the thing you label),
2. up to 2 PRIOR customer turns from the same conversation (context; may be absent),
3. the historical AmazonHelp reply — EVIDENCE about what happened, NOT the answer,
4. cluster/family context + MODEL SUGGESTION — NOT GROUND TRUTH (a nearest-centroid guess).

## How to label

1. Read the customer message first, alone. Ask: **WHAT DOES THE CUSTOMER WANT?**
2. If it is uninterpretable alone, read the prior customer turns. If still
   uninterpretable, set `taxonomy_verdict=ambiguous` (or `context_dependent`
   if the context resolved it) and say so in notes.
3. NEVER label "what AmazonHelp happened to reply". A refund reply to a
   delivery complaint is still a delivery complaint.
4. `intent_id`: stable snake_case (`delivery_delay`). Reuse an existing id
   when the goal matches; coin a new one only when nothing fits (with
   `taxonomy_verdict=new_intent`).
5. `routing_expectation`: your judgment — could a careful agent auto-resolve
   this (`auto_ok`), does it need one clarifying question (`clarify`), or
   must a human take it (`escalate`)? If escalation, say why.
6. `response_requirements`: constraints a correct reply must honor
   (e.g. "must not promise a date", "must not request card details publicly").
7. Mark `ood=true` (+ verdict `ood`) for non-support requests (chatter,
   jokes, praise with no ask, news commentary).
8. Mark `ambiguity=true` whenever you hesitated; set `needs_second_opinion`
   for the hard ones — at least ~40 items will be double-labelled for
   agreement measurement.

## Taxonomy feedback codes (`taxonomy_verdict`)

- `fits` — an existing preliminary intent covers it.
- `merge` — two preliminary intents should be one (name both in notes).
- `split` — carve a distinct new intent out of a broad one (describe it).
- `new_intent` — nothing covers it; your `intent_id` is the proposal.
- `ood` / `ambiguous` / `context_dependent` — as above.

One annotation never rewrites the taxonomy alone; the taxonomy builder
aggregates these codes across annotators. Be honest about disagreement —
hidden disagreement is worse than low agreement.
