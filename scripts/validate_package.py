#!/usr/bin/env python3
"""Validate ORE package structure without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from build_mods import template, NATIVE_MODS

ROOT = Path(__file__).parents[1]
VERSION = "4.2.1-alpha.1"
BASE_MODS = {"ore-progress", "ore-guard", "ore-resume", "ore-gates", "ore-stale-window", "ore-departments"}
RUNTIME_MODS = {"ore-scope-lock", "ore-never-again", "ore-approval-ledger", "ore-autopilot",
    "ore-model-router",
    "ore-signature-guard", "ore-safeguards-monitor",
    "ore-smart-tests", "ore-context-sentinel", "ore-independent-review", "ore-contract-watch",
    "ore-worktree-manager", "ore-pr-pilot", "ore-preview-certifier", "ore-runtime-diagnostics",
    "ore-cost-controller", "ore-project-router", "ore-learning-lab", "ore-first-contact",
    "ore-visual-qa", "ore-flow-intelligence", "ore-flow-watch"}
EXPECTED_MODS = BASE_MODS | RUNTIME_MODS
EXPECTED_SKILLS = {
    "ore-adaptive-model-routing",
    "ore-fda-part11", "ore-ftc-safeguards",
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
    mods = ROOT / "mods"
    found_mods = {p.name for p in mods.glob("ore-*") if p.is_dir()}
    if found_mods != EXPECTED_MODS:
        fail(errors, f"mod set mismatch: {sorted(found_mods)}")
    canonical_reader = mods / "ore-progress/hooks/state.ts"
    for name in sorted(EXPECTED_MODS):
        folder = mods / name
        try:
            manifest = json.loads((folder / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            if manifest.get("name") != name or manifest.get("version") != VERSION:
                fail(errors, f"mod manifest mismatch: {name}")
            hooks = json.loads((folder / "hooks/hooks.json").read_text(encoding="utf-8"))
            if hooks.get("modules") != ["./register.ts"]:
                fail(errors, f"mod module mismatch: {name}")
            module = (folder / "hooks/register.ts").read_text(encoding="utf-8")
            if name in RUNTIME_MODS or name == 'ore-guard':
                if (folder / 'hooks/approval.ts').read_bytes() != (mods / 'sdk/approval.ts').read_bytes():
                    fail(errors, f'approval presenter differs from canonical source: {name}')
            forbidden = re.findall(r"\$\.(?:fs\.write|http\.\w+|model\.\w+|store\.\w+)", module)
            if name in BASE_MODS:
                forbidden += re.findall(r"\$\.process\.\w+", module)
            elif module != (mods / "sdk" / template(name)).read_text(encoding="utf-8"):
                fail(errors, f"runtime module differs from audited SDK: {name}")
            if name in RUNTIME_MODS - NATIVE_MODS - {"ore-worktree-manager"}:
                if (folder / 'requirements.txt').read_bytes() != (ROOT / 'skills/ore/requirements.txt').read_bytes():
                    fail(errors, f'vendored requirements differ from canonical source: {name}')
                for script in ("ore_state.py", "ore_runtime.py", "ore_flow.py", "ore_first_contact.py", "ore_regulatory.py", "ore_models.py"):
                    if (folder / "scripts" / script).read_bytes() != (ROOT / "skills/ore/scripts" / script).read_bytes():
                        fail(errors, f"vendored script differs from canonical source: {name}/{script}")
            if forbidden:
                fail(errors, f"unapproved mod calls in {name}: {forbidden}")
            if (folder / "hooks/state.ts").read_bytes() != canonical_reader.read_bytes():
                fail(errors, f"state reader differs from canonical reader: {name}")
            if not (folder / "tsconfig.json").is_file():
                fail(errors, f"missing mod tsconfig: {name}")
        except (OSError, ValueError) as exc:
            fail(errors, f"invalid mod {name}: {exc}")
    try:
        marketplace = json.loads((mods / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        entries = marketplace["plugins"]
        if {p["name"] for p in entries} != EXPECTED_MODS:
            fail(errors, "mods marketplace inventory mismatch")
        for entry in entries:
            if entry.get("source") != f"./{entry['name']}" or entry.get("version") != VERSION:
                fail(errors, f"mods marketplace entry mismatch: {entry['name']}")
    except (OSError, ValueError, KeyError) as exc:
        fail(errors, f"invalid mods marketplace: {exc}")
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
    for source in skills_root.rglob("*.md"):
        for relative in re.findall(r"\]\(([^)#]+\.md)\)", source.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", relative):
                continue
            target = source.parent / relative
            if not target.is_file():
                fail(errors, f"broken reference in {source.relative_to(ROOT)}: {relative}")

    required = [
        ROOT / 'requirements.txt',
        skills_root / 'ore' / 'requirements.txt',
        skills_root / "ore" / "scripts" / "ore_state.py",
        skills_root / "ore" / "references" / "durable-state.md",
        skills_root / "ore" / "references" / "form-intelligence.md",
        skills_root / "ore" / "references" / "legacy-agent-study.md",
        skills_root / "ore" / "references" / "department-agent-study.md",
        skills_root / "ore" / "references" / "workflow-memory-study.md",
        ROOT / "evals" / "test_ore_state.py",
        ROOT / "evals" / "test_mods_state.py",
        ROOT / "evals" / "test_form_contract.py",
        ROOT / "evals" / "test_legacy_agent_catalog.py",
        ROOT / "evals" / "test_department_agent_catalog.py",
        ROOT / "evals" / "test_workflow_memory_catalog.py",
        ROOT / "evals" / "behavioral-scenarios.md",
        skills_root / "ore" / "scripts" / "validate_form_contract.py",
        skills_root / "ore" / "scripts" / "validate_audit_report.py",
        skills_root / "ore" / "references" / "audit-controls.md",
        skills_root / "ore" / "references" / "audit-stack-playbooks.md",
        skills_root / "ore" / "references" / "audit-report.md",
        ROOT / "evals" / "test_audit_report.py",
    ]
    for path in required:
        if not path.exists():
            fail(errors, f"missing required artifact: {path.relative_to(ROOT)}")

    if errors:
        print("ORE package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ORE package validation passed: {len(EXPECTED_SKILLS)} skills, {len(EXPECTED_MODS)} mods, version {VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

