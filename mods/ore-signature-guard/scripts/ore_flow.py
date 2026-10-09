#!/usr/bin/env python3
"""Read-only, evidence-based business flow contract and telemetry analysis."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

RELATION_STATUSES = {"confirmed", "inferred", "unverified", "contradictory", "not_applicable"}
CARDINALITIES = {"one-to-one", "one-to-many", "many-to-one", "many-to-many"}
GATES = ["BUSINESS_LIFECYCLE", "ENTITY_CONTINUITY", "WORKFLOW_RECOVERY", "DATA_CONTRACT", "CHANGE_IMPACT", "TESTS"]
TRANSITION_FIELDS = ("id", "source", "target", "event", "owner", "preconditions", "permissions",
                     "reused_fields", "transformations", "state_change", "side_effects", "errors",
                     "retry", "idempotency", "reconciliation", "cancellation", "recovery", "evidence")


def _time(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed


def validate_flow(document) -> list[str]:
    """Validate schema and references, returning errors rather than mutating input."""
    errors = []
    if not isinstance(document, dict):
        return ["flow must be an object"]
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(document.get("id"), str) or not document["id"]:
        errors.append("flow id is required")
    for name in ("entities", "relationships", "transitions", "executions"):
        if not isinstance(document.get(name), list) or any(not isinstance(item, dict) for item in document.get(name, [])):
            errors.append(f"{name} must be an array of objects")
    if errors:
        return errors
    entities = {}
    for entity in document["entities"]:
        identity = entity.get("id")
        if not isinstance(identity, str) or not identity or identity in entities:
            errors.append("entity IDs must be nonempty and globally distinct")
            continue
        entities[identity] = entity
        if not entity.get("type") or not entity.get("owner"):
            errors.append(f"entity {identity}: type and owner required")
        fields = entity.get("fields", {})
        if not isinstance(fields, dict):
            errors.append(f"entity {identity}: fields must be an object")
            continue
        for name, field in fields.items():
            if not isinstance(field, dict) or not all(key in field for key in ("value", "source", "version", "owner", "mode")):
                errors.append(f"field {identity}.{name}: value/source/version/owner/mode required")
                continue
            if not isinstance(field["mode"], str) or field["mode"] not in {"canonical", "reuse", "snapshot", "transformed"}:
                errors.append(f"field {identity}.{name}: invalid provenance mode")
            source = field["source"]
            if not isinstance(source, str) or "." not in source:
                errors.append(f"field {identity}.{name}: source must reference entity.field")
            if field["mode"] == "snapshot" and not field.get("reason"):
                errors.append(f"field {identity}.{name}: historical snapshot needs reason")
    for identity, entity in entities.items():
        for name, field in entity.get("fields", {}).items() if isinstance(entity.get("fields", {}), dict) else []:
            if isinstance(field, dict) and isinstance(field.get("source"), str) and "." in field["source"]:
                source_id, source_name = field["source"].rsplit(".", 1)
                if source_id not in entities or source_name not in entities[source_id].get("fields", {}):
                    errors.append(f"field {identity}.{name}: orphaned provenance {field['source']}")
    relation_ids = set()
    for relation in document["relationships"]:
        identity = relation.get("id")
        if not isinstance(identity, str) or not identity or identity in relation_ids:
            errors.append("relationship IDs must be distinct nonempty strings")
        relation_ids.add(identity if isinstance(identity, str) else "")
        status = relation.get("status")
        if not isinstance(status, str) or status not in RELATION_STATUSES:
            errors.append(f"relationship {identity}: invalid evidence classification")
        cardinality = relation.get("cardinality")
        if not isinstance(cardinality, str) or cardinality not in CARDINALITIES:
            errors.append(f"relationship {identity}: invalid cardinality")
        if isinstance(status, str) and status in {"confirmed", "inferred", "contradictory"} and not relation.get("evidence"):
            errors.append(f"relationship {identity}: evidence required")
        pairs = relation.get("pairs")
        if not isinstance(pairs, list):
            errors.append(f"relationship {identity}: pairs must be an array")
            continue
        sources, targets = Counter(), Counter()
        seen = set()
        for pair in pairs:
            if not isinstance(pair, list) or len(pair) != 2 or any(not isinstance(x, str) for x in pair):
                errors.append(f"relationship {identity}: invalid entity pair")
                continue
            source, target = pair
            if source not in entities or target not in entities:
                errors.append(f"relationship {identity}: orphaned entity pair {source}/{target}")
            elif entities[source]["type"] != relation.get("source_type") or entities[target]["type"] != relation.get("target_type"):
                errors.append(f"relationship {identity}: pair entity type mismatch")
            if tuple(pair) in seen:
                errors.append(f"relationship {identity}: duplicate pair")
            seen.add(tuple(pair))
            sources[source] += 1
            targets[target] += 1
        if isinstance(cardinality, str) and cardinality in {"one-to-one", "many-to-one"} and any(n > 1 for n in sources.values()):
            errors.append(f"relationship {identity}: source cardinality violated")
        if isinstance(cardinality, str) and cardinality in {"one-to-one", "one-to-many"} and any(n > 1 for n in targets.values()):
            errors.append(f"relationship {identity}: target cardinality violated")
    transitions = {}
    for transition in document["transitions"]:
        identity = transition.get("id")
        if not isinstance(identity, str) or not identity or identity in transitions:
            errors.append("transition IDs must be distinct nonempty strings")
            continue
        transitions[identity] = transition
        missing = [key for key in TRANSITION_FIELDS if key not in transition]
        if missing:
            errors.append(f"transition {identity}: missing {','.join(missing)}")
        if any(not isinstance(transition.get(key), str) or transition[key] not in entities for key in ("source", "target")):
            errors.append(f"transition {identity}: orphaned endpoint")
        for name in ("preconditions", "permissions", "reused_fields", "transformations", "side_effects", "evidence"):
            if name in transition and not isinstance(transition[name], list):
                errors.append(f"transition {identity}: {name} must be an array")
        for name in ("preconditions", "permissions"):
            if isinstance(transition.get(name), list) and any(not isinstance(x, str) for x in transition[name]):
                errors.append(f"transition {identity}: {name} must contain strings")
        if not transition.get("idempotency") or not transition.get("recovery") or not transition.get("evidence"):
            errors.append(f"transition {identity}: idempotency/recovery/evidence required")
        if "state_change" in transition and not isinstance(transition["state_change"], dict):
            errors.append(f"transition {identity}: state_change must be an object")
    execution_ids = set()
    for execution in document["executions"]:
        identity = execution.get("id")
        if not isinstance(identity, str) or not identity or identity in execution_ids:
            errors.append("execution IDs must be distinct nonempty strings")
        execution_ids.add(identity if isinstance(identity, str) else "")
        if not isinstance(execution.get("transition"), str) or execution["transition"] not in transitions:
            errors.append(f"execution {identity}: unknown transition")
        if not isinstance(execution.get("status"), str) or execution["status"] not in {"succeeded", "failed", "pending", "duplicate", "cancelled"}:
            errors.append(f"execution {identity}: invalid status")
        if "idempotency_key" in execution and not isinstance(execution["idempotency_key"], str):
            errors.append(f"execution {identity}: idempotency_key must be a string")
        for name in ("preconditions", "permissions"):
            if not isinstance(execution.get(name, []), list) or any(not isinstance(x, str) for x in execution.get(name, [])):
                errors.append(f"execution {identity}: {name} must contain strings")
        if not isinstance(execution.get("side_effect_count", 0), int) or isinstance(execution.get("side_effect_count", 0), bool) or execution.get("side_effect_count", 0) < 0:
            errors.append(f"execution {identity}: side_effect_count must be nonnegative integer")
        try:
            _time(execution["at"])
        except (KeyError, ValueError, TypeError, AttributeError):
            errors.append(f"execution {identity}: valid timezone timestamp required")
    telemetry = document.get("telemetry", {})
    if not isinstance(telemetry, dict):
        errors.append("telemetry must be an object")
    elif not isinstance(telemetry.get("observations", []), list) or any(not isinstance(x, dict) for x in telemetry.get("observations", [])):
        errors.append("telemetry observations must be an array of objects")
    else:
        for observation in telemetry.get("observations", []):
            if not isinstance(observation.get("entity"), str) or not isinstance(observation.get("kind"), str):
                errors.append("telemetry observation requires string entity/kind")
    balances = document.get("quantity_balances", [])
    if not isinstance(balances, list) or any(not isinstance(x, dict) for x in balances):
        errors.append("quantity_balances must be an array of objects")
    else:
        for balance in balances:
            for name in ("ordered", "produced", "rejected", "packaged", "shipped"):
                value = balance.get(name)
                if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                    errors.append(f"quantity balance: {name} must be a nonnegative number")
            if not balance.get("evidence"):
                errors.append("quantity balance requires evidence")
    return errors


def analyze_flow(document) -> dict:
    """Check supplied contracts and execution evidence; never infer links by name."""
    errors = validate_flow(document)
    result = {"valid": not errors, "errors": errors, "findings": [], "relationship_counts": {},
              "continuity_verified": False, "gates": {gate: "pending" for gate in GATES},
              "evidence_scope": "supplied flow model and execution records only"}
    if errors:
        return result
    findings = result["findings"]
    def add(code, subject, evidence, detail):
        findings.append({"code": code, "subject": subject, "evidence": evidence, "detail": detail})
    counts = Counter(relation["status"] for relation in document["relationships"])
    result["relationship_counts"] = {status: counts[status] for status in sorted(RELATION_STATUSES)}
    for relation in document["relationships"]:
        if relation["status"] not in {"confirmed", "not_applicable"}:
            add("relationship_not_verified", relation["id"], relation.get("evidence", []), relation["status"])
    entities = {entity["id"]: entity for entity in document["entities"]}
    for balance in document.get("quantity_balances", []):
        if not (balance["shipped"] <= balance["packaged"] <= balance["produced"] - balance["rejected"] <= balance["ordered"]):
            add("quantity_integrity", balance.get("id", document["id"]), balance["evidence"], "shipped <= packaged <= accepted production <= ordered violated")
    for identity, entity in entities.items():
        for name, field in entity.get("fields", {}).items():
            if field["mode"] == "reuse":
                origin, origin_name = field["source"].rsplit(".", 1)
                canonical = entities[origin]["fields"][origin_name]
                if field["value"] != canonical["value"] or field["version"] != canonical["version"]:
                    add("stale_field", f"{identity}.{name}", [field["source"]], "reused field differs from authorized source/version")
    executions = defaultdict(list)
    for execution in document["executions"]:
        executions[execution["transition"]].append(execution)
    seen_keys = {}
    for transition in document["transitions"]:
        records = sorted(executions[transition["id"]], key=lambda x: _time(x["at"]))
        success = False
        state = transition.get("state_change", {}).get("from") if isinstance(transition.get("state_change"), dict) else None
        for record in records:
            evidence = record.get("evidence", [])
            key = record.get("idempotency_key")
            if not key:
                add("missing_idempotency_key", record["id"], evidence, "execution cannot be reconciled safely")
            if record["status"] == "duplicate" and record.get("side_effect_count", 0):
                add("duplicate_side_effect", record["id"], evidence, "duplicate delivery caused a side effect")
            if record["status"] != "succeeded":
                continue
            success = True
            for field in ("preconditions", "permissions"):
                missing = set(transition[field]) - set(record.get(field, []))
                if missing:
                    add(f"missing_{field}", record["id"], evidence, ", ".join(sorted(missing)))
            if not evidence:
                add("missing_execution_evidence", record["id"], [], "success is not verified")
            if key:
                marker = (transition["id"], key)
                if marker in seen_keys and record.get("side_effect_count", 0):
                    add("duplicate_side_effect", record["id"], evidence, f"already succeeded in {seen_keys[marker]}")
                seen_keys[marker] = record["id"]
            if record.get("from_state") is not None and state is not None and record["from_state"] != state:
                add("out_of_order_transition", record["id"], evidence, f"expected {state}, observed {record['from_state']}")
            state = record.get("to_state", state)
        if transition.get("required", True) and not success:
            add("missing_transition", transition["id"], transition["evidence"], "no successful execution observed")
    if 'regulatory_transitions' in document:
        from ore_regulatory import transition as regulatory_transition
        checks = document['regulatory_transitions']
        if not isinstance(checks, list) or not checks:
            add('regulatory_contract_missing', document['id'], [], 'Regulatory transitions must be nonempty')
        else:
            for check in checks:
                try:
                    allowed = regulatory_transition(check['domain'], check['before'], check['after'], check.get('signature'))
                except (ValueError, KeyError, TypeError, AttributeError):
                    allowed = False
                if not allowed:
                    add('regulatory_transition_blocked', document['id'], [], 'Signature binding or access/protection precondition failed')
    verified = bool(document["transitions"]) and not findings
    result["continuity_verified"] = verified
    model_gates = {"BUSINESS_LIFECYCLE", "ENTITY_CONTINUITY", "WORKFLOW_RECOVERY", "DATA_CONTRACT"}
    result["gates"] = {gate: ("passed" if verified and gate in model_gates else "pending") for gate in GATES}
    # These statuses are local recommendations, not writes to ORE task gates.
    return result


def watch_flow(document, now_iso=None) -> dict:
    """Diagnose authorized observations without claiming unknown root causes."""
    analysis = analyze_flow(document)
    telemetry = document.get("telemetry", {}) if isinstance(document, dict) else {}
    if not analysis["valid"]:
        return {"connection": "invalid", "status": "invalid", "alerts": [], "errors": analysis["errors"]}
    if telemetry.get("connection") != "connected":
        return {"connection": "unavailable", "status": "no_telemetry", "alerts": [], "errors": []}
    try:
        current = _time(now_iso) if now_iso else datetime.now(timezone.utc)
    except (ValueError, TypeError, AttributeError):
        return {"connection": "connected", "status": "invalid", "alerts": [], "errors": ["invalid now timestamp"]}
    alerts = []
    seen = set()
    entities = {entity["id"] for entity in document["entities"]}
    for observation in telemetry.get("observations", []):
        record = observation.get("entity")
        kind = observation.get("kind")
        elapsed = None
        try:
            elapsed = (current - _time(observation["last_transition_at"])).total_seconds()
        except (KeyError, TypeError, ValueError, AttributeError):
            pass
        sla = observation.get("sla_seconds")
        if isinstance(sla, (int, float)) and not isinstance(sla, bool) and sla >= 0 and elapsed is not None and elapsed > sla and not observation.get("terminal", False):
            kind = "sla_exceeded"
        if record not in entities:
            kind = "orphaned_record"
        if kind not in {"sla_exceeded", "stuck", "unprocessed_event", "duplicate", "orphaned_record", "reconciliation_error", "incompatible_state", "integration_failure", "missing_transition"}:
            continue
        evidence = observation.get("evidence", [])
        if not evidence:
            continue  # An ungrounded suspicion is not an observed operational alert.
        marker = (record, kind)
        if marker in seen:
            continue
        seen.add(marker)
        alerts.append({"process": document["id"], "records": [record], "kind": kind,
                       "last_transition": observation.get("last_transition"), "elapsed_seconds": elapsed,
                       "evidence": evidence, "severity": observation.get("severity", "warning"),
                       "possible_cause": observation.get("cause") if observation.get("cause_evidence") else "unknown",
                       "cause_evidence": observation.get("cause_evidence", []),
                       "owner": observation.get("owner", "unassigned"),
                       "proposed_recovery": observation.get("recovery", "inspect evidence and reconcile before retry"),
                       "repair_key": f"{document['id']}:{record}:{kind}", "repair_executed": False})
    return {"connection": "connected", "status": "attention" if alerts else "observed", "alerts": alerts, "errors": []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "analyze", "watch"))
    parser.add_argument("file", type=Path)
    parser.add_argument("--now", help="Timezone-aware timestamp for reproducible telemetry analysis")
    args = parser.parse_args()
    try:
        document = json.loads(args.file.read_text(encoding="utf-8"))
        result = validate_flow(document) if args.command == "validate" else analyze_flow(document) if args.command == "analyze" else watch_flow(document, args.now)
    except (OSError, ValueError) as error:
        print(json.dumps({"errors": [str(error)]}))
        return 2
    print(json.dumps(result, indent=2))
    if args.command == "validate":
        return 1 if result else 0
    return 1 if result.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
