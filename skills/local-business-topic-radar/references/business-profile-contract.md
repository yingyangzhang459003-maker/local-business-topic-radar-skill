# Business Profile Contract v1

## Purpose

Business Profile v1 is the shared merchant-input contract for the local topic radar and article writer. It contains only facts supplied or approved by the user.

## Required fields

| Field | Type | Rule |
|---|---|---|
| `profile_version` | string | Must equal `1.0`. |
| `city` | string | Non-empty operating city. |
| `district` | string | Non-empty district, county, or `全市` for city-wide scope. |
| `industry` | string | Merchant's real industry. |
| `business_name` | string | Real name in private use; clearly fictional name in public examples. |
| `target_customers` | string | Primary local customer group. |
| `products_services` | array of strings | Products or services that may be mentioned. |
| `business_strengths` | array of strings | Verifiable strengths, not unsupported superlatives. |
| `content_goal` | string | Desired content outcome. |
| `conversion_action` | string | One natural next action for the reader. |
| `forbidden_claims` | array of strings | Claims or topics the workflow must not make. |

## Validation and missing data

- Every field is required, including arrays that are intentionally empty.
- `products_services`, `business_strengths`, and `forbidden_claims` must be arrays.
- Ask only for missing required fields. Never invent merchant facts.
- Do not silently upgrade or downgrade `profile_version`.

## Privacy

Real merchant profiles remain in the user's private project or runtime input. Public repositories contain fictional examples only and must not contain credentials, private contacts, customer data, or unpublished operating data.
