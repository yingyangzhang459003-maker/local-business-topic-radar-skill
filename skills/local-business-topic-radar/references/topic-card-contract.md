# Topic Card Contract v1

## Purpose

Topic Card v1 is the handoff contract from the local topic radar to the local article writer. A card represents one current, sourced, locally relevant writing opportunity; it is not a finished article.

## Required fields

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | Must equal `1.0`. |
| `topic_id` | string | Stable unique identifier for this generated topic. |
| `generated_at` | string | ISO date `YYYY-MM-DD`. |
| `city` | string | Target city. |
| `district` | string | Target district, county, or `全市`. |
| `industry` | string | Merchant industry. |
| `title` | string | Proposed local article title. |
| `hot_event` | string | Verified event, change, concern, or seasonal signal. |
| `sources` | array of source objects | At least one source object. |
| `why_local_people_care` | string | Explicit local relevance. |
| `target_customer` | string | Local audience for this topic. |
| `customer_pain_point` | string | Concrete need or decision tension. |
| `business_connection` | string | Natural, non-forced merchant connection. |
| `search_keywords` | array of strings | Local search phrases. |
| `writing_angle` | string | Recommended editorial angle. |
| `recommended_cta` | string | One bounded reader action. |
| `valid_until` | string | ISO date after which freshness must be rechecked. |
| `score` | score object | Eight components plus calculated total. |
| `risk_notes` | array of strings | Compliance, freshness, or evidence warnings; may be empty. |

## Source object

Every object in `sources` contains:

| Field | Type | Rule |
|---|---|---|
| `title` | string | Human-readable source title. |
| `url` | string | Direct source URL. |
| `published_at` | string | ISO date `YYYY-MM-DD`. |

Prefer primary or authoritative sources for policy, regulation, price, admissions, medical, financial, safety, and other high-risk claims.

## Score object

| Field | Maximum |
|---|---:|
| `local_relevance` | 20 |
| `industry_relevance` | 20 |
| `timeliness` | 15 |
| `customer_demand` | 15 |
| `search_value` | 10 |
| `conversion_value` | 10 |
| `source_reliability` | 5 |
| `compliance_safety` | 5 |

Each component is an integer from zero through its maximum. `total` is required, equals the exact sum of the eight components, and must be at least 70 for a formal Topic Card.

## Freshness and compatibility

- Recheck sources and material facts after `valid_until`; never present stale details as current.
- Producers emit contract version `1.0` only.
- Consumers must not silently accept an unsupported version. The article writer may offer a direct-title fallback only after naming which structured fields will be lost.
- Never invent missing sources, scores, merchant facts, dates, or risk notes.
