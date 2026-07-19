import datetime
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit


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

PROFILE_LIST_FIELDS = (
    "products_services", "business_strengths", "forbidden_claims"
)
PROFILE_STRING_FIELDS = tuple(
    field for field in PROFILE_REQUIRED if field not in PROFILE_LIST_FIELDS
)

TOPIC_LIST_FIELDS = ("search_keywords", "risk_notes")
TOPIC_STRING_FIELDS = tuple(
    field for field in TOPIC_REQUIRED
    if field not in TOPIC_LIST_FIELDS + ("sources", "score")
)

SOURCE_REQUIRED = ("title", "url", "published_at")
ISO_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


def _missing(data, required):
    return [f"missing field: {field}" for field in required if field not in data]


def _is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_strings(data, fields, prefix=""):
    errors = []
    for field in fields:
        if field in data and not _is_non_empty_string(data[field]):
            errors.append(f"{prefix}{field} must be a non-empty string")
    return errors


def _validate_string_lists(data, fields):
    errors = []
    for field in fields:
        if field not in data:
            continue
        value = data[field]
        if not isinstance(value, list):
            errors.append(f"{field} must be a list")
            continue
        for index, item in enumerate(value):
            if not _is_non_empty_string(item):
                errors.append(f"{field}[{index}] must be a non-empty string")
    return errors


def _is_iso_date(value):
    if not isinstance(value, str) or not ISO_DATE_PATTERN.fullmatch(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_direct_http_url(value):
    if not _is_non_empty_string(value) or any(char.isspace() for char in value):
        return False
    if value.strip().casefold() in {"同上", "same as above"}:
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc and parsed.hostname)


def validate_business_profile(data):
    if not isinstance(data, dict):
        return ["business profile must be an object"]
    errors = _missing(data, PROFILE_REQUIRED)
    errors.extend(_validate_strings(data, PROFILE_STRING_FIELDS))
    errors.extend(_validate_string_lists(data, PROFILE_LIST_FIELDS))
    if "profile_version" in data and data["profile_version"] != "1.0":
        errors.append("profile_version must be 1.0")
    return errors


def validate_topic_card(data):
    if not isinstance(data, dict):
        return ["topic card must be an object"]
    errors = _missing(data, TOPIC_REQUIRED)
    errors.extend(_validate_strings(data, TOPIC_STRING_FIELDS))
    errors.extend(_validate_string_lists(data, TOPIC_LIST_FIELDS))
    if "contract_version" in data and data["contract_version"] != "1.0":
        errors.append("contract_version must be 1.0")

    for field in ("generated_at", "valid_until"):
        if field in data and not _is_iso_date(data[field]):
            errors.append(f"{field} must be a valid ISO date YYYY-MM-DD")

    sources = data.get("sources")
    if "sources" in data and not isinstance(sources, list):
        errors.append("sources must be a list")
    elif isinstance(sources, list) and not sources:
        errors.append("sources must contain at least one source")
    elif isinstance(sources, list):
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"sources[{index}] must be an object")
                continue
            for field in SOURCE_REQUIRED:
                if field not in source:
                    errors.append(f"sources[{index}] missing field: {field}")
            errors.extend(
                _validate_strings(source, SOURCE_REQUIRED, f"sources[{index}].")
            )
            if "url" in source and not _is_direct_http_url(source["url"]):
                errors.append(
                    f"sources[{index}].url must be a full direct http(s) URL"
                )
            if "published_at" in source and not _is_iso_date(source["published_at"]):
                errors.append(
                    f"sources[{index}].published_at must be a valid ISO date YYYY-MM-DD"
                )

    score = data.get("score")
    if isinstance(score, dict):
        for field in SCORE_FIELDS + ("total",):
            if field not in score:
                errors.append(f"score missing field: {field}")

        for field in SCORE_FIELDS + ("total",):
            if field in score and (
                not isinstance(score[field], int) or isinstance(score[field], bool)
            ):
                errors.append(f"score.{field} must be an integer")

        for field, maximum in SCORE_MAX.items():
            value = score.get(field)
            if isinstance(value, int) and not isinstance(value, bool):
                if not 0 <= value <= maximum:
                    errors.append(f"score.{field} must be between 0 and {maximum}")

        valid_components = all(
            field in score
            and isinstance(score[field], int)
            and not isinstance(score[field], bool)
            for field in SCORE_FIELDS
        )
        if valid_components:
            calculated = sum(score[field] for field in SCORE_FIELDS)
            if (
                isinstance(score.get("total"), int)
                and not isinstance(score.get("total"), bool)
                and score["total"] != calculated
            ):
                errors.append(f"score.total must equal {calculated}")
        if (
            isinstance(score.get("total"), int)
            and not isinstance(score.get("total"), bool)
            and score["total"] < 70
        ):
            errors.append("score.total must be at least 70")
    elif "score" in data:
        errors.append("score must be an object")
    return errors


def _validate_file(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["invalid JSON"]
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
