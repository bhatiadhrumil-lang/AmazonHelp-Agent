# AmazonHelp Conversation Quality Audit

Dataset rows: 47,211
AmazonHelp tweets: 2,930
AmazonHelp-connected root components: 1,245

## Component audit
| Status | Count | Share |
|---|---:|---:|
| KEEP | 653 | 52.45% |
| FLAG | 62 | 4.98% |
| EXCLUDE | 530 | 42.57% |

## Customer problem episodes
Direct customer -> AmazonHelp episodes: 1,821

| Status | Count | Share |
|---|---:|---:|
| KEEP | 1,696 | 93.14% |
| FLAG | 105 | 5.77% |
| EXCLUDE | 20 | 1.10% |

## Important methodology
- Short messages, multilingual signals, URLs, and acknowledgments are not blindly deleted at the raw-data stage.
- Component quality and episode quality are reported separately.
- The customer problem corpus for intent discovery should use the episode table, not AmazonHelp replies as clustering text.
- Historical AmazonHelp replies are retained separately for later response-evidence retrieval.
- Thresholds are configurable and should be validated by manual inspection before being frozen in the report.