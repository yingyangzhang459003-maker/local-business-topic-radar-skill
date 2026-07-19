import importlib.util
import pathlib
import unittest


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


if __name__ == "__main__":
    unittest.main()
