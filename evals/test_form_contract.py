import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "ore" / "scripts" / "validate_form_contract.py"


class FormContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        (self.repo / ".ore" / "forms").mkdir(parents=True)
        self.expected = self.repo / "industries.json"
        self.expected.write_text(json.dumps(["Health", "Retail", "Energy"]), encoding="utf-8")
        self.contract = self.repo / ".ore" / "forms" / "onboarding.json"

    def tearDown(self):
        self.temp.cleanup()

    def write_contract(self, values):
        value = {
            "id": "onboarding", "user_role": "owner", "job": "create company", "canonical_entity": "Company",
            "fields": [{
                "id": "industry", "type": "enum", "required": True, "source": "user-supplied list",
                "allowed_values": values, "client_validation": "membership", "server_validation": "membership",
                "error": "Choose a listed industry", "privacy": "non-sensitive",
            }],
            "states": ["draft", "submitted"],
            "accessibility": {"keyboard": True, "screen_reader": True, "text_scaling": True},
            "submission": {"idempotent": True},
            "test_cases": ["happy", "invalid", "server_error", "double_submit"],
        }
        self.contract.write_text(json.dumps(value), encoding="utf-8")

    def run_validator(self):
        return subprocess.run([
            sys.executable, str(SCRIPT), "--repo", str(self.repo),
            "--contract", str(self.contract), "--expected", f"industry={self.expected}",
        ], text=True, capture_output=True)

    def test_exact_authoritative_list_passes(self):
        self.write_contract(["Health", "Retail", "Energy"])
        self.assertEqual(self.run_validator().returncode, 0)

    def test_reordered_or_replaced_list_fails(self):
        self.write_contract(["Retail", "Health", "Other"])
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertIn("values/order mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()

