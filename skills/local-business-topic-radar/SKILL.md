---
name: local-business-topic-radar
description: Use when a user needs current local content topics for a city-based business, including local events, city news, policy changes, consumer concerns, seasonal opportunities, or industry trends that must be verified, scored, and converted into structured topic cards.
---

# Local Business Topic Radar

## Purpose

Find ten timely, verifiable topics that local customers care about and that connect naturally to the merchant's industry. Stop at topic cards; do not write full articles.

## Required input

Read a Business Profile v1. If it is unavailable, ask only for city, district, industry, business name, target customers, products or services, business strengths, content goal, conversion action, and forbidden claims. Never invent missing merchant facts.

Read `references/business-profile-contract.md` when validating or creating a profile.

## Research workflow

1. Establish today's date and the requested time window.
2. Scan local official sources, local media and life signals, platform discussions, then national industry signals with a provable local bridge.
3. Use Agent Reach when installed. Otherwise use the runtime's current web-search tools.
4. Keep source title, URL, and publication date. Require a primary source for policy, regulation, price, admissions, medical, and financial claims.
5. Reject unverified claims and unrelated traffic before scoring.

Read `references/source-strategy.md` for source selection and `references/compliance-rules.md` for regulated claims.

## Rank and select

Score every surviving candidate with `references/scoring-model.md`. Exclude totals below 70. Prefer useful local demand over raw national popularity. Do not force a merchant connection.

## Output contract

Return exactly ten ranked Topic Card Contract v1 cards using `references/output-template.md`. Each card must include dated sources, local relevance, customer pain, a natural business connection, keywords, writing angle, CTA, validity window, score breakdown, and risk notes. Write every source as a separate object with its direct URL repeated in the `url` field; never use the Chinese shorthand U+540C U+4E0A ("same as above"), the English phrase "same as above", or a linked title in place of that field.

Read `references/topic-card-contract.md` before emitting or validating cards.

## Stop conditions

- Missing merchant facts: ask only for the missing required fields.
- Insufficient evidence: mark the candidate as failing the fact threshold and exclude it.
- Expired event: refresh it or replace it.
- Forced business connection: reject it.
- Fewer than ten qualified candidates: report the actual qualified count instead of padding with weak topics.

After selection, tell the user that any card can be passed to `local-business-article-writer`, while keeping this Skill independently usable.
