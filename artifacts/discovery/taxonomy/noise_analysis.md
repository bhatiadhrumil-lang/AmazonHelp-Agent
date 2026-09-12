# Noise analysis (Phase 1C, TASK 6)

## Setup

- Population: **49,621** points with HDBSCAN label == -1 (53.3% of 93,171 embedded messages).
- Sample: **150** rows, seed=42, drawn after sorting by `customer_message_id` (so it is reproducible regardless of meta file row order).
- Source rows: `artifacts/discovery/taxonomy/noise_sample.csv` (raw text) and `noise_sample_classified.csv` (with the `bucket` column).

## Sampled composition (SAMPLE-LEVEL n=150, not a population estimate)

| Bucket | Count | Share of sample |
|---|---|---|
| Matches an existing cluster theme (near-hit / boundary point) | 109 | 73% |
| Conversation-thread turn (meaningful only with context) | 21 | 14% |
| Off-topic / social / venting chatter | 16 | 11% |
| Data / format fragment (status token, tag, code) | 3 | 2% |
| Novel combination or genuinely unclear | 1 | 1% |
| **Total** | **150** | **100%** |

## Bucket meanings

### Matches an existing cluster theme (near-hit / boundary point)

Delivery, refund, contact-channel, form, driver, seller, device, pre-order, etc. - the underlying customer goal matches one of the 203 clusters' themes; the point simply fell into the noise set (small size, boundary, mixed-language, or one-off wording).

### Conversation-thread turn (meaningful only with context)

Short acknowledgements, status words, polarity/chronology answers, channel-switch statements. As standalone tweets they carry almost no intent; the intent lives in the rest of the thread.

### Off-topic / social / venting chatter

Casual banter, emoji talk, jokes, positive praise, rhetorical venting, or out-of-domain content (non-Amazon products, living-room chit-chat).

### Data / format fragment (status token, tag, code)

Almost token-level texts (e.g. 'Delivered', 'Lp Collect', 'En cours de livraison').

### Novel combination or genuinely unclear

Unusual combinations (e.g. messaging failure with business impact) that do not clearly match any single cluster theme.


## Working hypotheses (must be validated by humans)

1. The majority of sampled noise points fit an already-clustered intent theme **at the level of customer goal** (delivery, refund, contact-channel, form, driver, seller, pre-order, device, etc.). They are clustered-out mostly for surface-form or scale reasons: one-off wording, multilingual code-switching, boundary placement, or attachments/URLs dominating the text.
2. A substantial minority are **thread-turn artefacts** (short ack/status/polarity replies). These are not standalone intents and should be handled by the conversation layer, not by intent triage.
3. A small slice is **off-topic/social/OOD** chatter with no support goal.
4. A very small slice is **token-level fragments** (status words, locker codes) and **novel/unclear** one-offs.

> No percentage statements about the full noise population are made from this sample. If noise is later used for OOD detection, a far larger stratified sample plus human review is required.