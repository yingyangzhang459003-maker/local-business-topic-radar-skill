import json
import pathlib
import sys


PROFILE_REQUIRED = (
    "profile_version", "city", "district", "industry", "business_name",
    "target_customers", "products_services", "business_strengths",
    "content_goal", "conversion_action", "forbidden_claims"
)

TOPIC_REQUIRED = (
    "contract_version", "topic_id", "generated_at", "city", "district",
    "industry", "title", "hot_event", "sources", "why_local_people_care",
    "target_customer", "customer_pain_point", "business_connection",
    "search_keywords", "writing_angle", "recommended_cta", "valid_until",
    "score", "risk_notes"
)

SCORE_MAX = {
    "local_relevance": 20,
    "industry_relevance": 20,
    "timeliness": 15,
    "customer_demand": 15,
    "search_value": 10,
    "conversion_value": 10,
    "source_reliability": 5,
    "compliance_safety": 5,
}

SCORE_FIELDS = tuple(SCORE_MAX)


def _missing(data, required):
    return [f"missing field: {field}" for field in required if field not in data]


def validate_business_profile(data):
    errors = _missing(data, PROFILE_REQUIRED)
    if data.get("profile_version") != "1.0":
        errors.append("profile_version must be 1.0")
    for field in ("products_services", "business_strengths", "forbidden_claims"):
        value = data.get(field)
        if field in data and not isinstance(value, list):
            errors.append(f"{field} must be a list")
    return errors


def validate_topic_card(data):
    errors = _missing(data, TOPIC_REQUIRED)
    if data.get("contract_version") != "1.0":
        errors.append("contract_version must be 1.0")
    sources = data.get("sources")
    if sources is not None and (not isinstance(sources, list) or not sources):
        errors.append("sources must contain at least one source")
    elif isinstance(sources, list):
        for index, source in enumerate(sources):
            for field in ("title", "url", "published_at"):
                if field not in source:
                    errors.append(f"sources[{index}] missing field: {field}")
    score = data.get("score")
    if isinstance(score, dict):
        for field in SCORE_FIELDS + ("total",):
            if field not in score:
                errors.append(f"score missing field: {field}")
        if all(isinstance(score.get(field), int) for field in SCORE_FIELDS):
            for field, maximum in SCORE_MAX.items():
                if not 0 <= score[field] <= maximum:
                    errors.append(f"score.{field} must be between 0 and {maximum}")
            calculated = sum(score[field] for field in SCORE_FIELDS)
            if score.get("total") != calculated:
                errors.append(f"score.total must equal {calculated}")
        if isinstance(score.get("total"), int) and score["total"] < 70:
            errors.append("score.total must be at least 70")
    elif score is not None:
        errors.append("score must be an object")
    return errors


def _validate_file(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if path.name.startswith("business-profile-"):
        return validate_business_profile(data)
    if path.name.startswith("topic-card-"):
        return validate_topic_card(data)
    return ["unsupported example filename"]


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    example_files = sorted((root / "examples").glob("*.json"))
    if not example_files:
        print("no example files found", file=sys.stderr)
        return 1
    failed = False
    for path in example_files:
        errors = _validate_file(path)
        if errors:
            failed = True
            print(f"FAIL {path.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
