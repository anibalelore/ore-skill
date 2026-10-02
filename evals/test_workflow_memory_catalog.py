from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CORE = (ROOT / "skills" / "ore" / "SKILL.md").read_text(encoding="utf-8")
ROUTER = (ROOT / "skills" / "ore" / "references" / "specialist-routing.md").read_text(encoding="utf-8")
GATES = (ROOT / "skills" / "ore" / "references" / "quality-gates.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
STUDY = (ROOT / "skills" / "ore" / "references" / "workflow-memory-study.md").read_text(encoding="utf-8")

NEW_SKILLS = {
    "ore-business-lifecycle": {"BUSINESS_LIFECYCLE", "ENTITY_CONTINUITY", "WORKFLOW_RECOVERY"},
    "ore-organizational-memory": {"MEMORY_INTEGRITY", "KNOWLEDGE_PROMOTION"},
    "ore-context-efficiency": {"CONTEXT_EFFICIENCY", "TOKEN_ACCOUNTING"},
}


class WorkflowMemoryCatalogTests(unittest.TestCase):
    def test_new_skills_are_installable_and_routed_once(self) -> None:
        for name in NEW_SKILLS:
            skill = ROOT / "skills" / name / "SKILL.md"
            ui = ROOT / "skills" / name / "agents" / "openai.yaml"
            self.assertTrue(skill.exists(), name)
            self.assertTrue(ui.exists(), name)
            self.assertEqual(CORE.count(f"`${name}`"), 1, name)
            self.assertEqual(ROUTER.count(f"(`${name}`)"), 1, name)
            self.assertEqual(README.count(f"`${name}`"), 1, name)

    def test_skill_gates_are_declared_and_defined(self) -> None:
        for name, expected_gates in NEW_SKILLS.items():
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for gate in expected_gates:
                self.assertIn(f"`{gate}`", text, f"{name}:{gate}")
                self.assertRegex(GATES, rf"- `{re.escape(gate)}`:")

    def test_business_lifecycle_covers_continuity_failures(self) -> None:
        text = (ROOT / "skills" / "ore-business-lifecycle" / "SKILL.md").read_text(encoding="utf-8")
        required = [
            "canonical immutable identifier",
            "authoritative owner",
            "instead of asking for it again",
            "timeout-after-commit",
            "reconciliation",
            "correction propagation",
            "deletion propagation",
            "any process",
            "For illustration only",
            "These are examples, not a fixed model",
            "existing/duplicate entity",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_requested_sources_are_assessed(self) -> None:
        for source in (
            "alirezarezvani/claude-skills",
            "memory-graph/memory-graph",
            "valorisa/Claude-Skills",
            "Graphify-Labs/graphify",
        ):
            self.assertIn(source, STUDY)
        self.assertIn("not repository code or marketing claims", STUDY)
        self.assertIn("never auto-installs", STUDY)

    def test_graphify_is_bounded_in_change_impact(self) -> None:
        impact = (ROOT / "skills" / "ore-change-impact" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Graphify", impact)
        self.assertIn("no code graph can see", impact)
        self.assertIn("No tool, hook", impact)


if __name__ == "__main__":
    unittest.main()
