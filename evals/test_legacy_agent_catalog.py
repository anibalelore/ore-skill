import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILLS = {
    "ore-product-architecture": {"ARCHITECTURE_FIT", "CONTRACT_COMPATIBILITY"},
    "ore-backend-data": {"DATA_CONTRACT", "MIGRATION_SAFETY"},
    "ore-quality-engineering": {"TESTS", "ACCESSIBILITY", "LOCALIZATION", "PERFORMANCE", "RESILIENCE"},
    "ore-security-privacy": {"SECURITY_PRIVACY"},
    "ore-delivery-operations": {"RELEASE", "OBSERVABILITY", "ROLLBACK"},
    "ore-code-health": {"CODE_HEALTH", "DOCUMENTATION", "DEPENDENCY_HEALTH", "LEARNING_CAPTURE"},
}


class HistoricalAgentCatalogTests(unittest.TestCase):
    def test_specialists_are_routed_and_have_matching_quality_gates(self):
        routing = (ROOT / "skills/ore/references/specialist-routing.md").read_text(encoding="utf-8")
        gates = (ROOT / "skills/ore/references/quality-gates.md").read_text(encoding="utf-8")

        for skill, required_gates in SKILLS.items():
            with self.subTest(skill=skill):
                body = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"${skill}", routing)
                self.assertIn("legacy-agent-study.md", body)
                declared = set(re.findall(r"`([A-Z][A-Z_]+)`", body))
                self.assertTrue(required_gates <= declared)
                for gate in required_gates:
                    self.assertIn(f"`{gate}`", gates)

    def test_external_sources_are_references_not_runtime_dependencies(self):
        study = (ROOT / "skills/ore/references/legacy-agent-study.md").read_text(encoding="utf-8")
        self.assertIn("Repositories are not bundled, installed or executed automatically.", study)
        self.assertIn("CC BY/CC BY-SA material is reference-only", study)
        self.assertIn("AGPL code such as Renovate", study)

        dependency_manifests = [
            ROOT / "pyproject.toml",
            ROOT / "package.json",
        ]
        self.assertFalse(any(path.exists() for path in dependency_manifests))
        # Browser execution is now an explicit requirement; study repositories
        # must still not become implicitly installed runtime dependencies.
        requirements = (ROOT / 'skills/ore/requirements.txt').read_text(encoding='utf-8')
        packages = {line.split('==', 1)[0] for line in requirements.splitlines()
                    if line.strip() and not line.startswith('#')}
        self.assertEqual(packages, {'playwright'})

    def test_behavioral_evals_cover_every_historical_lead(self):
        scenarios = (ROOT / "evals/behavioral-scenarios.md").read_text(encoding="utf-8")
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"${skill}", scenarios)


if __name__ == "__main__":
    unittest.main()
