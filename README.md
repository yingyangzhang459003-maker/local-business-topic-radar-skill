# Local Business Topic Radar Skill

Finds ten verified local content opportunities for a city-based business.

## What it does

Takes a business profile, runs a four-layer local scan, applies an evidence gate, scores candidates on a 100-point model, and returns Topic Card v1 results.

## What it does not do

It does not write full articles, auto-publish content, or invent merchant data.

## Install locally

```powershell
Copy-Item -Recurse .\skills\local-business-topic-radar "$HOME\.codex\skills\local-business-topic-radar"
```

## Example prompts

```text
使用 $local-business-topic-radar，为肇庆端州一家家庭餐厅寻找今天值得写的10个本地热点选题。
使用 $local-business-topic-radar，读取我的 business-profile.json，生成带信源、评分和有效期的 Top 10。
```

## Contracts

- [Business Profile v1](skills/local-business-topic-radar/references/business-profile-contract.md)
- [Topic Card v1](skills/local-business-topic-radar/references/topic-card-contract.md)

## Validate

```powershell
py -3 -m unittest discover -s tests -v
py -3 scripts/validate_contract.py
py -3 "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" 'skills\local-business-topic-radar'
```

## Handoff

After choosing a Topic Card, you can optionally pass it to `local-business-article-writer` to draft an article. This Skill remains independently usable for topic discovery.

## Privacy and safety

Do not store credentials or real private merchant data in this repository. Use the profile contract and examples without adding sensitive business information.

## License

Released under the [MIT License](LICENSE).
