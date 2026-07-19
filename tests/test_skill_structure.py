import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "local-business-topic-radar"
SKILL_FILE = SKILL_DIR / "SKILL.md"
OUTPUT_TEMPLATE = SKILL_DIR / "references" / "output-template.md"


class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter_has_valid_name_and_description(self):
        lines = SKILL_FILE.read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(lines), 4)
        self.assertEqual(lines[0], "---")
        self.assertIn("---", lines[1:])

        closing_index = lines[1:].index("---") + 1
        metadata = {}
        for line in lines[1:closing_index]:
            key, separator, value = line.partition(":")
            self.assertEqual(separator, ":", f"invalid frontmatter line: {line}")
            metadata[key.strip()] = value.strip()

        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], SKILL_DIR.name)
        self.assertRegex(metadata["name"], r"^[a-z0-9-]{1,63}$")
        self.assertTrue(metadata["description"])
        self.assertFalse(re.search(r"[<>]", metadata["description"]))

    def test_output_instructions_forbid_padding_when_fewer_than_ten_qualify(self):
        required_instruction = (
            "Provide exactly ten numbered Topic Cards only when ten candidates qualify. "
            "If fewer than ten qualify under the stop conditions, provide the actual "
            "qualified count and never pad the list with weak topics."
        )
        template = OUTPUT_TEMPLATE.read_text(encoding="utf-8")
        skill = SKILL_FILE.read_text(encoding="utf-8")
        self.assertIn(required_instruction, template)
        self.assertIn(required_instruction, skill)


if __name__ == "__main__":
    unittest.main()
