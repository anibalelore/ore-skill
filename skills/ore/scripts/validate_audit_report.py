#!/usr/bin/env python3
"""Validate an ORE audit ledger; does not scan applications or verify evidence truth."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CONTROL_IDS = frozenset(
    [f"SEC-{i:02d}" for i in range(1, 10)]
    + [f"LEG-{i:02d}" for i in range(1, 21)]
    + [f"ADV-{i:02d}" for i in range(1, 8)]
)
MODES = {"audit", "security", "compliance", "accessibility", "fix", "loop", "report"}
CONTROL_STATUSES = {"passed", "failed", "not_applicable", "not_evaluated", "out_of_scope"}
FINDING_STATUSES = {"suspected", "confirmed", "fixed_unvalidated", "resolved", "accepted_risk"}


def validate_report(report: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be an object"]

    def required_text(obj: dict, keys: tuple[str, ...], where: str) -> None:
        for key in keys:
            if not isinstance(obj.get(key), str) or not obj[key].strip():
                errors.append(f"{where}.{key} must be nonempty text")

    required_text(report, ("project", "date", "scope", "revision", "stop_reason", "next_action"), "report")
    if not isinstance(report.get("mode"), str) or report["mode"] not in MODES:
        errors.append("unknown audit mode")
    iteration = report.get("iteration")
    if type(iteration) is not int or not 0 <= iteration <= 5:
        errors.append("iteration must be an integer from 0 to 5")

    def records(key: str) -> list[dict]:
        value = report.get(key)
        if not isinstance(value, list):
            errors.append(f"{key} must be an array")
            return []
        valid = []
        seen = set()
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f"{key}[{index}] must be an object")
                continue
            identity = item.get("id")
            if not isinstance(identity, str) or not identity.strip():
                errors.append(f"{key}[{index}].id must be nonempty text")
                continue
            if identity in seen:
                errors.append(f"duplicate {key} ID: {identity}")
                continue
            seen.add(identity)
            valid.append(item)
        return valid

    controls = records("controls")
    control_map = {item["id"]: item for item in controls}
    for item in controls:
        if item["id"] not in CONTROL_IDS:
            errors.append(f"unknown control: {item['id']}")
        if not isinstance(item.get("status"), str) or item["status"] not in CONTROL_STATUSES:
            errors.append(f"invalid control status: {item['id']}")
        required_text(item, ("evidence",), item["id"])
    if report.get("mode") == "audit" and set(control_map) != CONTROL_IDS:
        errors.append("integral audit must record all 36 controls")

    tests = records("tests")
    test_map = {item["id"]: item for item in tests}
    for item in tests:
        if not isinstance(item.get("status"), str) or item["status"] not in {"passed", "failed", "not_run"}:
            errors.append(f"invalid test status: {item['id']}")
        required_text(item, ("evidence", "revision"), item["id"])

    for finding in records("findings"):
        identity = finding["id"]
        required_text(finding, ("component", "evidence", "risk", "preconditions", "impact", "correction", "side_effects"), identity)
        if not isinstance(finding.get("severity"), str) or finding["severity"] not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"invalid severity: {identity}")
        status = finding.get("status")
        if not isinstance(status, str) or status not in FINDING_STATUSES:
            errors.append(f"invalid finding status: {identity}")
            status = "invalid"
        linked = finding.get("controls")
        if not isinstance(linked, list) or not linked or any(not isinstance(cid, str) or cid not in control_map for cid in linked):
            errors.append(f"{identity} must link to recorded controls")
        elif status in {"confirmed", "fixed_unvalidated", "accepted_risk"}:
            if any(control_map[cid].get("status") != "failed" for cid in linked):
                errors.append(f"{identity}: unresolved finding requires failed linked controls")
        validation = finding.get("validation")
        if not isinstance(validation, dict):
            errors.append(f"{identity}.validation must be an object")
            continue
        for phase in ("retest", "regression"):
            refs = validation.get(phase)
            if not isinstance(refs, list) or any(not isinstance(ref, str) or ref not in test_map for ref in refs):
                errors.append(f"{identity}.{phase} must reference recorded tests")
                continue
            if status == "resolved":
                if not refs:
                    errors.append(f"{identity}: resolved requires {phase} evidence")
                for ref in refs:
                    check = test_map[ref]
                    if check.get("status") != "passed" or check.get("revision") != report.get("revision"):
                        errors.append(f"{identity}: {phase} must pass at current revision")
        if status == "accepted_risk":
            acceptance = finding.get("acceptance")
            if not isinstance(acceptance, dict):
                errors.append(f"{identity}: accepted risk requires owner, rationale, scope and expiry")
            else:
                required_text(acceptance, ("owner", "rationale", "scope", "expires"), identity + ".acceptance")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        # Parser exceptions can include input text: never echo potentially sensitive content.
        print("ORE audit ledger unreadable or invalid JSON", file=sys.stderr)
        return 2
    errors = validate_report(report)
    if errors:
        print("ORE audit ledger invalid:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("ORE audit ledger structure and evidence links valid; evidence truth not assessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
