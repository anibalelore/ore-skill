import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
AGENTS = {
    "ore-change-impact": {"CHANGE_IMPACT", "CONTRACT_COMPATIBILITY", "TESTS"},
    "ore-ai-engineering": {"AI_EVALUATION", "AI_SAFETY", "OBSERVABILITY", "COST_CAPACITY"},
    "ore-data-analytics": {"DATA_QUALITY", "DATA_LINEAGE", "DATA_CONTRACT", "SECURITY_PRIVACY"},
    "ore-platform-cloud": {"INFRASTRUCTURE_PLAN", "PLATFORM_SAFETY", "COST_CAPACITY", "OBSERVABILITY", "ROLLBACK"},
    "ore-developer-experience": {"DEVELOPER_EXPERIENCE", "DOCUMENTATION", "BUILD_STATIC", "TESTS"},
    "ore-product-discovery": {"DISCOVERY_EVIDENCE", "EXPERIMENT_INTEGRITY"},
    "ore-compliance-governance": {"COMPLIANCE_EVIDENCE", "AUDIT_TRACEABILITY", "SECURITY_PRIVACY"},
    "ore-release-certification": {"RELEASE_CERTIFICATION", "PROVENANCE", "CHANGE_IMPACT", "RELEASE", "ROLLBACK"},
}


class DepartmentAgentCatalogTests(unittest.TestCase):
    def test_agents_have_central_routes_gates_and_external_basis(self):
        core = (ROOT / "skills/ore/SKILL.md").read_text(encoding="utf-8")
        routing = (ROOT / "skills/ore/references/specialist-routing.md").read_text(encoding="utf-8")
        gate_catalog = (ROOT / "skills/ore/references/quality-gates.md").read_text(encoding="utf-8")

        for agent, required_gates in AGENTS.items():
            with self.subTest(agent=agent):
                body = (ROOT / "skills" / agent / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"${agent}", core)
                self.assertIn(f"${agent}", routing)
                self.assertIn("department-agent-study.md", body)
                declared = set(re.findall(r"`([A-Z][A-Z_]+)`", body))
                self.assertTrue(required_gates <= declared)
                for gate in required_gates:
                    self.assertIn(f"`{gate}`", gate_catalog)

    def test_readme_lists_every_agent_once_in_departments(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        department_section = readme.split("## Agent departments", 1)[1].split(
            "ORE routes only", 1
        )[0]
        all_agents = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        for agent in all_agents:
            with self.subTest(agent=agent):
                self.assertEqual(department_section.count(f"`${agent}`"), 1)

    def test_study_uses_multiple_primary_sources_without_bundling_them(self):
        study = (ROOT / "skills/ore/references/department-agent-study.md").read_text(encoding="utf-8")
        urls = set(re.findall(r"https://(?:github\.com|docs\.github\.com)/[^) ]+", study))
        self.assertGreaterEqual(len(urls), 20)
        self.assertIn("No repository is cloned, installed, executed or vendored", study)
        self.assertIn("MPL-2.0", study)
        self.assertIn("CC BY 4.0", study)
        self.assertIn("Community Specification License", study)

    def test_release_certifier_is_separate_from_implementation_authority(self):
        certification = (ROOT / "skills/ore-release-certification/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("never certifies its own implementation work", certification)
        self.assertIn("never performs production promotion", certification)
        self.assertIn("immutable candidate", certification)
        self.assertIn("tied to the exact candidate", certification)


if __name__ == "__main__":
    unittest.main()
