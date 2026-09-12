# AmazonHelp Conversation Quality Audit

Dataset rows: 2,811,774
AmazonHelp tweets: 169,840
AmazonHelp-connected root components: 82,534

## Component audit
| Status | Count | Share |
|---|---:|---:|
| KEEP | 42,408 | 51.38% |
| FLAG | 2,193 | 2.66% |
| EXCLUDE | 37,933 | 45.96% |

## Customer problem episodes
Direct customer -> AmazonHelp episodes: 100,503

| Status | Count | Share |
|---|---:|---:|
| KEEP | 93,171 | 92.70% |
| FLAG | 5,653 | 5.62% |
| EXCLUDE | 1,679 | 1.67% |

## Important methodology
- Short messages, multilingual signals, URLs, and acknowledgments are not blindly deleted at the raw-data stage.
- Component quality and episode quality are reported separately.
- The customer problem corpus for intent discovery should use the episode table, not AmazonHelp replies as clustering text.
- Historical AmazonHelp replies are retained separately for later response-evidence retrieval.
- Thresholds are configurable and should be validated by manual inspection before being frozen in the report.