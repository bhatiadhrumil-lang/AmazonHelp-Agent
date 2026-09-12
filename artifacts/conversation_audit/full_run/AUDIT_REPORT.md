# AmazonHelp Conversation Quality Audit

Dataset rows: 2,811,774
AmazonHelp tweets: 169,840
AmazonHelp-connected root components: 83,286

## Component audit
| Status | Count | Share |
|---|---:|---:|
| KEEP | 42,422 | 50.94% |
| FLAG | 2,197 | 2.64% |
| EXCLUDE | 38,667 | 46.43% |

## Customer problem episodes
Direct customer -> AmazonHelp episodes: 100,108

| Status | Count | Share |
|---|---:|---:|
| KEEP | 92,784 | 92.68% |
| FLAG | 5,647 | 5.64% |
| EXCLUDE | 1,677 | 1.68% |

## Important methodology
- Short messages, multilingual signals, URLs, and acknowledgments are not blindly deleted at the raw-data stage.
- Component quality and episode quality are reported separately.
- The customer problem corpus for intent discovery should use the episode table, not AmazonHelp replies as clustering text.
- Historical AmazonHelp replies are retained separately for later response-evidence retrieval.
- Thresholds are configurable and should be validated by manual inspection before being frozen in the report.