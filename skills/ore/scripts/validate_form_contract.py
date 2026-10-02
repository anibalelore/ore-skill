#!/usr/bin/env python3
"""Validate an ORE form contract and authoritative option lists."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ore_state import StateError, validate_form_contract


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--expected", action="append", default=[], help="FIELD=JSON_FILE containing the authoritative ordered array")
    args = parser.parse_args()
    try:
        path = validate_form_contract(args.repo, args.contract)
        contract = json.loads(path.read_text(encoding="utf-8"))
        fields = {field["id"]: field for field in contract["fields"]}
        checked = []
        for raw in args.expected:
            if "=" not in raw:
                raise StateError(f"Invalid --expected '{raw}'; use FIELD=JSON_FILE")
            field_id, raw_path = raw.split("=", 1)
            if field_id not in fields:
                raise StateError(f"Unknown contract field: {field_id}")
            expected_path = Path(raw_path).resolve()
            expected = json.loads(expected_path.read_text(encoding="utf-8"))
            actual = fields[field_id].get("allowed_values")
            if not isinstance(expected, list):
                raise StateError(f"Authoritative list must be a JSON array: {expected_path}")
            if actual != expected:
                raise StateError(f"Authoritative values/order mismatch for field '{field_id}'")
            if len(actual) != len(set(json.dumps(item, sort_keys=True) for item in actual)):
                raise StateError(f"Duplicate authoritative option in field '{field_id}'")
            checked.append(field_id)
        print(json.dumps({"valid": True, "contract": str(path), "authoritative_fields": checked}, ensure_ascii=False))
        return 0
    except (StateError, OSError, json.JSONDecodeError) as exc:
        print(f"ORE form error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

