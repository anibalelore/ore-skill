#!/usr/bin/env python3
"""Validate ORE package structure without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
VERSION = "2.3.0"
EXPECTED_SKILLS = {
    "ore",
    "ore-android",
    "ore-ios",
    "ore-flutter",
    "ore-mobile-design",
    "ore-web-engineering",
    "ore-creative-web",
    "ore-search-discovery",
    "ore-form-workflows",
    "ore-business-lifecycle",
    "ore-product-architecture",
    "ore-backend-data",
    "ore-quality-engineering",
    "ore-security-privacy",
    "ore-delivery-operations",
    "ore-code-health",
    "ore-organizational-memory",
    "ore-context-efficiency",
    "ore-change-impact",
    "ore-ai-engineering",
    "ore-data-analytics",
    "ore-platform-cloud",
    "ore-developer-experience",
    "ore-product-discovery",
    "ore-compliance-governance",
    "ore-release-certification",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if "TODO" in text:
        fail(errors, f"unfinished TODO: {path.relative_to(ROOT)}")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}
    values = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def main() -> int:
    errors: list[str] = []
    skills_root = ROOT / "skills"
    found = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if found != EXPECTED_SKILLS:
        fail(errors, f"skill set mismatch: expected={sorted(EXPECTED_SKILLS)}, found={sorted(found)}")

    for name in sorted(EXPECTED_SKILLS):
        skill = skills_root / name
        skill_md = skill / "SKILL.md"
        ui = skill / "agents" / "openai.yaml"
        if not skill_md.exists():
            fail(errors, f"missing {skill_md.relative_to(ROOT)}")
            continue
        meta = frontmatter(skill_md, errors)
        if meta.get("name") != name:
            fail(errors, f"name mismatch in {skill_md.relative_to(ROOT)}")
        text = skill_md.read_text(encoding="utf-8")
        if f'version: "{VERSION}"' not in text:
            fail(errors, f"version mismatch in {skill_md.relative_to(ROOT)}")
        if not ui.exists():
            fail(errors, f"missing {ui.relative_to(ROOT)}")
        else:
            ui_text = ui.read_text(encoding="utf-8")
            if "TODO" in ui_text:
                fail(errors, f"unfinished TODO: {ui.relative_to(ROOT)}")
            if f"${name}" not in ui_text:
                fail(errors, f"default prompt does not invoke ${name}: {ui.relative_to(ROOT)}")
            short = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', ui_text, re.MULTILINE)
            if not short or not 25 <= len(short.group(1)) <= 64:
                fail(errors, f"short_description must be 25-64 characters: {ui.relative_to(ROOT)}")

    for manifest in (ROOT / "plugin.json", ROOT / ".codex-plugin" / "plugin.json"):
        try:
            value = json.loads(manifest.read_text(encoding="utf-8"))
            if value.get("version") != VERSION:
                fail(errors, f"manifest version mismatch: {manifest.relative_to(ROOT)}")
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"invalid manifest {manifest.relative_to(ROOT)}: {exc}")

    core = skills_root / "ore" / "SKILL.md"
    core_text = core.read_text(encoding="utf-8")
    for relative in re.findall(r"\]\(([^)#]+\.md)\)", core_text):
        target = core.parent / relative
        if not target.exists():
            fail(errors, f"broken core reference: {relative}")

    required = [
        skills_root / "ore" / "scripts" / "ore_state.py",
        skills_root / "ore" / "references" / "durable-state.md",
        skills_root / "ore" / "references" / "form-intelligence.md",
        skills_root / "ore" / "references" / "legacy-agent-study.md",
        skills_root / "ore" / "references" / "department-agent-study.md",
        skills_root / "ore" / "references" / "workflow-memory-study.md",
        ROOT / "evals" / "test_ore_state.py",
        ROOT / "evals" / "test_form_contract.py",
        ROOT / "evals" / "test_legacy_agent_catalog.py",
        ROOT / "evals" / "test_department_agent_catalog.py",
        ROOT / "evals" / "test_workflow_memory_catalog.py",
        ROOT / "evals" / "behavioral-scenarios.md",
        skills_root / "ore" / "scripts" / "validate_form_contract.py",
    ]
    for path in required:
        if not path.exists():
            fail(errors, f"missing required artifact: {path.relative_to(ROOT)}")

    if errors:
        print("ORE package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ORE package validation passed: {len(EXPECTED_SKILLS)} skills, version {VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

