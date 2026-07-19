# Scoring Model

Score every candidate before it becomes a formal Topic Card.

| Field | Meaning | Maximum |
|---|---|---:|
| `local_relevance` | Direct city or district impact | 20 |
| `industry_relevance` | Natural connection to the merchant industry | 20 |
| `timeliness` | Freshness and remaining action window | 15 |
| `customer_demand` | Strength of the target customer's need | 15 |
| `search_value` | Local keyword and query value | 10 |
| `conversion_value` | Natural path to inquiry, visit, save, or share | 10 |
| `source_reliability` | Quality and date of evidence | 5 |
| `compliance_safety` | Absence of unsupported or prohibited claims | 5 |

Use whole integers. `total` must equal the eight-component sum. Reject totals below 70; do not repair a weak candidate by inflating its score.
