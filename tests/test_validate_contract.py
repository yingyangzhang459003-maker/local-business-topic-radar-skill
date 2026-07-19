import importlib.util
import json
import pathlib
import tempfile
import unittest
from urllib.parse import urlsplit


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_contract", ROOT / "scripts" / "validate_contract.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_profile():
    return {
        "profile_version": "1.0",
        "city": "肇庆",
        "district": "端州",
        "industry": "教育培训",
        "business_name": "端州成长学习中心（示例）",
        "target_customers": "初中生家长",
        "products_services": ["初中晚辅"],
        "business_strengths": ["本地校区"],
        "content_goal": "建立信任并促进咨询",
        "conversion_action": "预约到店咨询",
        "forbidden_claims": ["保证提分"]
    }


def valid_topic_card():
    return {
        "contract_version": "1.0",
        "topic_id": "zhaoqing-education-20260716-01",
        "generated_at": "2026-07-16",
        "city": "肇庆",
        "district": "端州",
        "industry": "教育培训",
        "title": "肇庆暑期公共活动增加，初中家庭如何安排学习节奏",
        "hot_event": "肇庆公布暑期公共文化活动安排",
        "sources": [{
            "title": "肇庆暑期公共文化活动安排（示例）",
            "url": "https://example.com/zhaoqing-summer",
            "published_at": "2026-07-16"
        }],
        "why_local_people_care": "家庭需要协调活动、出行与学习安排",
        "target_customer": "肇庆初中生家长",
        "customer_pain_point": "暑期安排容易失衡",
        "business_connection": "机构可提供时间规划方法，不承诺效果",
        "search_keywords": ["肇庆暑期活动", "初中暑假规划"],
        "writing_angle": "从家庭时间管理切入",
        "recommended_cta": "收藏规划清单",
        "valid_until": "2026-07-23",
        "score": {
            "local_relevance": 18,
            "industry_relevance": 18,
            "timeliness": 13,
            "customer_demand": 12,
            "search_value": 8,
            "conversion_value": 8,
            "source_reliability": 5,
            "compliance_safety": 5,
            "total": 87
        },
        "risk_notes": []
    }


class BusinessProfileTests(unittest.TestCase):
    def test_valid_profile_has_no_errors(self):
        self.assertEqual(validator.validate_business_profile(valid_profile()), [])

    def test_missing_city_is_reported(self):
        profile = valid_profile()
        del profile["city"]
        self.assertIn("missing field: city", validator.validate_business_profile(profile))

    def test_wrong_profile_version_is_reported(self):
        profile = valid_profile()
        profile["profile_version"] = "2.0"
        self.assertIn("profile_version must be 1.0", validator.validate_business_profile(profile))

    def test_top_level_value_must_be_an_object(self):
        self.assertEqual(
            validator.validate_business_profile([]),
            ["business profile must be an object"],
        )

    def test_required_string_must_not_be_empty(self):
        profile = valid_profile()
        profile["city"] = "   "
        self.assertIn(
            "city must be a non-empty string",
            validator.validate_business_profile(profile),
        )

    def test_array_field_must_be_a_list(self):
        profile = valid_profile()
        profile["products_services"] = "初中晚辅"
        self.assertIn(
            "products_services must be a list",
            validator.validate_business_profile(profile),
        )

    def test_array_elements_must_be_non_empty_strings(self):
        profile = valid_profile()
        profile["business_strengths"] = ["本地校区", 123, ""]
        errors = validator.validate_business_profile(profile)
        self.assertIn("business_strengths[1] must be a non-empty string", errors)
        self.assertIn("business_strengths[2] must be a non-empty string", errors)


class TopicCardTests(unittest.TestCase):
    def test_valid_topic_card_has_no_errors(self):
        self.assertEqual(validator.validate_topic_card(valid_topic_card()), [])

    def test_empty_sources_are_rejected(self):
        card = valid_topic_card()
        card["sources"] = []
        self.assertIn("sources must contain at least one source", validator.validate_topic_card(card))

    def test_score_total_must_equal_breakdown(self):
        card = valid_topic_card()
        card["score"]["total"] = 99
        self.assertIn("score.total must equal 87", validator.validate_topic_card(card))

    def test_formal_topic_must_score_at_least_70(self):
        card = valid_topic_card()
        card["score"]["local_relevance"] = 0
        card["score"]["total"] = 69
        self.assertIn("score.total must be at least 70", validator.validate_topic_card(card))

    def test_score_component_must_not_exceed_maximum(self):
        card = valid_topic_card()
        card["score"]["local_relevance"] = 21
        card["score"]["total"] = 90
        self.assertIn(
            "score.local_relevance must be between 0 and 20",
            validator.validate_topic_card(card)
        )

    def test_top_level_value_must_be_an_object(self):
        self.assertEqual(
            validator.validate_topic_card("not an object"),
            ["topic card must be an object"],
        )

    def test_required_string_must_not_be_empty(self):
        card = valid_topic_card()
        card["title"] = ""
        self.assertIn(
            "title must be a non-empty string",
            validator.validate_topic_card(card),
        )

    def test_generated_at_must_be_a_valid_iso_calendar_date(self):
        card = valid_topic_card()
        card["generated_at"] = "2026-02-30"
        self.assertIn(
            "generated_at must be a valid ISO date YYYY-MM-DD",
            validator.validate_topic_card(card),
        )

    def test_valid_until_must_use_exact_iso_date_format(self):
        card = valid_topic_card()
        card["valid_until"] = "2026-7-23"
        self.assertIn(
            "valid_until must be a valid ISO date YYYY-MM-DD",
            validator.validate_topic_card(card),
        )

    def test_topic_array_field_must_be_a_list(self):
        card = valid_topic_card()
        card["search_keywords"] = "肇庆暑期活动"
        self.assertIn(
            "search_keywords must be a list",
            validator.validate_topic_card(card),
        )

    def test_topic_array_elements_must_be_non_empty_strings(self):
        card = valid_topic_card()
        card["risk_notes"] = [False, ""]
        errors = validator.validate_topic_card(card)
        self.assertIn("risk_notes[0] must be a non-empty string", errors)
        self.assertIn("risk_notes[1] must be a non-empty string", errors)

    def test_source_must_be_an_object(self):
        card = valid_topic_card()
        card["sources"] = [42]
        self.assertIn(
            "sources[0] must be an object",
            validator.validate_topic_card(card),
        )

    def test_source_title_must_not_be_empty(self):
        card = valid_topic_card()
        card["sources"][0]["title"] = "   "
        self.assertIn(
            "sources[0].title must be a non-empty string",
            validator.validate_topic_card(card),
        )

    def test_source_url_must_be_a_full_direct_http_url(self):
        for value in (
            "同上",
            "same as above",
            "/local/path",
            "ftp://example.com/item",
            "https://[",
        ):
            with self.subTest(value=value):
                card = valid_topic_card()
                card["sources"][0]["url"] = value
                self.assertIn(
                    "sources[0].url must be a full direct http(s) URL",
                    validator.validate_topic_card(card),
                )

    def test_source_date_must_be_a_valid_iso_calendar_date(self):
        card = valid_topic_card()
        card["sources"][0]["published_at"] = "2025-13-01"
        self.assertIn(
            "sources[0].published_at must be a valid ISO date YYYY-MM-DD",
            validator.validate_topic_card(card),
        )

    def test_score_must_be_an_object(self):
        card = valid_topic_card()
        card["score"] = []
        self.assertIn("score must be an object", validator.validate_topic_card(card))

    def test_every_score_field_must_be_present(self):
        card = valid_topic_card()
        del card["score"]["search_value"]
        self.assertIn(
            "score missing field: search_value",
            validator.validate_topic_card(card),
        )

    def test_score_components_must_be_integers_and_bool_is_invalid(self):
        card = valid_topic_card()
        card["score"]["timeliness"] = True
        self.assertIn(
            "score.timeliness must be an integer",
            validator.validate_topic_card(card),
        )

    def test_valid_integer_components_are_bounds_checked_independently(self):
        card = valid_topic_card()
        card["score"]["local_relevance"] = 21
        card["score"]["timeliness"] = "current"
        errors = validator.validate_topic_card(card)
        self.assertIn("score.local_relevance must be between 0 and 20", errors)
        self.assertIn("score.timeliness must be an integer", errors)

    def test_score_total_must_be_an_integer_and_bool_is_invalid(self):
        card = valid_topic_card()
        card["score"]["total"] = True
        self.assertIn(
            "score.total must be an integer",
            validator.validate_topic_card(card),
        )

    def test_malformed_nested_values_return_errors_instead_of_raising(self):
        card = valid_topic_card()
        card["sources"] = [None, {"title": [], "url": {}, "published_at": False}]
        card["score"] = {"local_relevance": "high"}
        errors = validator.validate_topic_card(card)
        self.assertIn("sources[0] must be an object", errors)
        self.assertIn("score.local_relevance must be an integer", errors)


class FileValidationTests(unittest.TestCase):
    def test_malformed_json_returns_an_error_instead_of_raising(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir) / "topic-card-broken.json"
            path.write_text("{broken", encoding="utf-8")
            errors = validator._validate_file(path)
        self.assertEqual(errors, ["invalid JSON"])

    def test_json_with_non_object_top_level_returns_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir) / "business-profile-broken.json"
            path.write_text(json.dumps([]), encoding="utf-8")
            errors = validator._validate_file(path)
        self.assertEqual(errors, ["business profile must be an object"])

    def test_committed_topic_sources_do_not_use_reserved_example_domains(self):
        reserved_hosts = {"example.com", "example.net", "example.org"}
        for path in sorted((ROOT / "examples").glob("topic-card-*.json")):
            with self.subTest(path=path.name):
                card = json.loads(path.read_text(encoding="utf-8"))
                hosts = {urlsplit(source["url"]).hostname for source in card["sources"]}
                self.assertTrue(hosts.isdisjoint(reserved_hosts))


if __name__ == "__main__":
    unittest.main()
