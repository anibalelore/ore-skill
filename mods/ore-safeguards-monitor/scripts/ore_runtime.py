"""Pure ORE runtime governance contracts. Persistence belongs to ore_state.py."""
from __future__ import annotations

import copy
import fnmatch
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import PurePosixPath

VERSION = 1
MODULES = {
    "ore-model-router",
    "ore-signature-guard", "ore-safeguards-monitor",
    "ore-scope-lock", "ore-never-again", "ore-approval-ledger", "ore-autopilot",
    "ore-smart-tests", "ore-context-sentinel", "ore-independent-review", "ore-contract-watch",
    "ore-worktree-manager", "ore-pr-pilot", "ore-preview-certifier", "ore-runtime-diagnostics",
    "ore-cost-controller", "ore-project-router", "ore-learning-lab", "ore-first-contact",
    "ore-visual-qa", "ore-flow-intelligence", "ore-flow-watch",
}
GOVERNANCE_ACTIONS = {"scope", "rule", "revoke-rule", "exception", "approval", "revoke-approval", "model-policy", "model-decision"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    require(isinstance(value, str), "Timestamp must be an ISO string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp must include a timezone")
    return parsed


def project_id(repo):
    return hashlib.sha256(str(repo).encode("utf-8")).hexdigest()


def relative_path(value):
    require(isinstance(value, str) and bool(value) and len(value) <= 500, "Path must be nonempty and bounded")
    normalized = value.replace("\\", "/")
    require(not normalized.startswith("/") and ":" not in normalized and ".." not in normalized.split("/"), "Paths must be repository-relative without traversal")
    normalized = str(PurePosixPath(normalized))
    require(not normalized.lower().startswith(".ore/") and normalized.lower() != ".ore", ".ore is reserved for the state writer")
    return normalized


def bounded_text(value, name, maximum=1000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= maximum, f"{name} must be a bounded nonempty string")
    require(not any(ord(c) < 32 for c in value if c not in "\n\t"), f"{name} contains control characters")
    return value


def initial_governance(project):
    return {"schema_version": VERSION, "project": project, "revision": 0, "rules": [], "approvals": [], "exceptions": [], "events": []}


def validate_governance(data, project):
    require(isinstance(data, dict) and data.get("schema_version") == VERSION and data.get("project") == project, "Invalid or foreign project governance")
    require(type(data.get("revision")) is int and data["revision"] >= 0, "Invalid governance revision")
    for name in ("rules", "approvals", "exceptions", "events"):
        require(isinstance(data.get(name), list) and all(isinstance(x, dict) for x in data[name]), f"Invalid governance {name}")
    for name in ("rules", "approvals", "exceptions"):
        seen = set()
        for record in data[name]:
            identifier = bounded_text(record.get("id"), "record id", 96)
            require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", identifier)), "Invalid record id")
            require(identifier not in seen and record.get("project") == project, "Duplicate or foreign governance record")
            seen.add(identifier)
            require(record.get("status") in {"active", "revoked", "replaced"}, "Invalid record status")
            if record.get("expires_at"):
                timestamp(record["expires_at"])
            if name == "rules":
                require(record.get("kind") in {"allow-paths", "forbid-paths", "review"}, "Invalid rule kind")
                require(isinstance(record.get("paths"), list) and bool(record["paths"]), "Invalid rule paths")
                for value in record["paths"]:
                    relative_path(value)
            if name == "exceptions":
                relative_path(record.get("path"))
                bounded_text(record.get("rule_id"), "exception rule")
            if name == "approvals":
                for key in ("operation", "scope", "environment", "owner", "evidence"):
                    bounded_text(record.get(key), key)
                timestamp(record.get("expires_at"))
                require(record.get("grants_native_permissions") is False, "Invalid approval privileges")
    if 'routing' in data:
        from ore_models import validate_routing
        validate_routing(data['routing'])
    return data


def valid_now(record, now):
    return record.get("status") == "active" and (not record.get("expires_at") or timestamp(record["expires_at"]) > timestamp(now))


def apply_governance(data, action, payload, project, now, confirmed):
    """Return a new revision. Approval records never grant native privileges."""
    validate_governance(data, project)
    require(confirmed is True, "Durable governance changes require explicit confirmation")
    require(action in GOVERNANCE_ACTIONS - {'model-policy', 'model-decision'} and isinstance(payload, dict), "Invalid governance action")
    result = copy.deepcopy(data)
    owner = bounded_text(payload.get("owner"), "owner", 200)
    evidence = bounded_text(payload.get("evidence"), "evidence")
    identifier = bounded_text(payload.get("id"), "id", 96)
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", identifier)), "Invalid record id")
    if action in {"scope", "rule"}:
        paths = payload.get("paths")
        require(isinstance(paths, list) and 0 < len(paths) <= 100, "Scope/rule paths are required")
        paths = [relative_path(p) for p in paths]
        kind = payload.get("kind", "allow-paths" if action == "scope" else "forbid-paths")
        require(kind in {"allow-paths", "forbid-paths", "review"}, "Rule kind must be executable path restriction or explicit review")
        record = {"id": identifier, "description": bounded_text(payload.get("description"), "description"), "project": project,
                  "paths": paths, "kind": kind, "owner": owner, "evidence": evidence, "approved_at": now,
                  "status": "active", "enforcement": "review" if kind == "review" else "block", "exceptions_allowed": payload.get("exceptions_allowed") is True}
        if payload.get("expires_at"):
            require(timestamp(payload["expires_at"]) > timestamp(now), "Expiry must be in the future")
            record["expires_at"] = payload["expires_at"]
        existing = next((r for r in result["rules"] if r["id"] == identifier), None)
        require(existing is None, "Rule id already exists; revoke or replace explicitly")
        if payload.get("replaces"):
            prior = next((r for r in result["rules"] if r["id"] == payload["replaces"] and r["status"] == "active"), None)
            require(prior is not None, "Replaced rule is not active")
            prior["status"] = "replaced"
            prior["replaced_by"] = identifier
        result["rules"].append(record)
    elif action in {"revoke-rule", "revoke-approval"}:
        collection = "rules" if action == "revoke-rule" else "approvals"
        record = next((r for r in result[collection] if r["id"] == identifier), None)
        require(record is not None, "Record does not exist")
        record.update(status="revoked", revoked_at=now, revoked_by=owner)
    elif action == "approval":
        require(not any(r["id"] == identifier for r in result["approvals"]), "Approval id already exists")
        expiry = payload.get("expires_at")
        require(timestamp(expiry) > timestamp(now), "Approval expiry must be in the future")
        result["approvals"].append({"id": identifier, "project": project, "owner": owner, "evidence": evidence,
            "operation": bounded_text(payload.get("operation"), "operation", 200), "scope": bounded_text(payload.get("scope"), "scope"),
            "environment": bounded_text(payload.get("environment"), "environment", 100), "approved_at": now, "expires_at": expiry,
            "status": "active", "grants_native_permissions": False})
    else:
        rule = next((r for r in result["rules"] if r["id"] == payload.get("rule_id") and valid_now(r, now)), None)
        require(rule is not None and rule.get("exceptions_allowed"), "Rule does not allow exceptions")
        path = relative_path(payload.get("path"))
        require(not any(r["id"] == identifier for r in result["exceptions"]), "Exception id already exists")
        require(timestamp(payload.get("expires_at")) > timestamp(now), "Exception expiry must be in the future")
        result["exceptions"].append({"id": identifier, "rule_id": rule["id"], "path": path, "project": project, "owner": owner,
            "evidence": evidence, "expires_at": payload["expires_at"], "status": "active"})
    result["revision"] += 1
    envelope = {"schema_version": 1, "id": f"{project[:12]}-{result['revision']}", "correlation_id": identifier,
                "origin": "ore_state.py", "project": project, "kind": f"governance.{action}", "at": now,
                "permission": "explicit-user-confirmation", "data_class": "project-metadata", "record_id": identifier}
    result["events"].append(envelope)
    return result


def check_paths(governance, paths, now):
    violations, reviews = [], []
    for raw in paths:
        path = relative_path(raw)
        for rule in governance.get("rules", []):
            if not valid_now(rule, now):
                continue
            applies = any(fnmatch.fnmatchcase(path, pattern) for pattern in rule["paths"])
            exempt = any(e.get("rule_id") == rule["id"] and e.get("path") == path and valid_now(e, now) for e in governance.get("exceptions", []))
            if exempt:
                continue
            if rule["kind"] == "review" and applies:
                reviews.append({"path": path, "rule": rule["id"]})
            if (rule["kind"] == "allow-paths" and not applies) or (rule["kind"] == "forbid-paths" and applies):
                violations.append({"path": path, "rule": rule["id"]})
    return {"allowed": not violations, "violations": violations, "review_required": reviews}


def autopilot(task, payload):
    """Bounded controller state, never executes a plan or changes model settings."""
    steps = payload.get("steps", [])
    require(isinstance(steps, list) and 0 < len(steps) <= 5 and all(isinstance(s, str) and 0 < len(s) <= 500 for s in steps), "Autopilot needs 1..5 explicit steps")
    attempts = payload.get("attempts", 0)
    require(type(attempts) is int and 0 <= attempts <= 5, "Invalid attempt budget")
    stop = "blocked" if task.get("blockers") else "budget-exhausted" if attempts >= len(steps) else "no-verified-progress" if payload.get("no_progress") is True else "awaiting-approved-execution"
    return {"state": stop, "next_action": steps[attempts] if attempts < len(steps) else None, "remaining": max(0, len(steps)-attempts), "executes_model_turns": False}


def smart_tests(payload):
    changed, mappings = payload.get("changed_paths", []), payload.get("mappings", [])
    require(isinstance(changed, list) and isinstance(mappings, list), "Test map needs changed_paths and mappings")
    selected, uncovered = set(), []
    for path in changed:
        path = relative_path(path)
        matches = [m for m in mappings if isinstance(m, dict) and any(fnmatch.fnmatchcase(path, p) for p in m.get("paths", []))]
        if not matches:
            uncovered.append(path)
        for match in matches:
            selected.update(match.get("tests", []))
    broad = payload.get("broad_tests", [])
    require(isinstance(broad, list) and all(isinstance(t, str) for t in broad), "broad_tests must be test identifiers")
    if uncovered or payload.get("coverage_complete") is not True:
        selected.update(broad)
    require_broad = bool(uncovered) or payload.get("coverage_complete") is not True
    critical = payload.get("critical_tests", [])
    require(isinstance(critical, list) and all(isinstance(t, str) for t in critical), "critical_tests must be test identifiers")
    selected.update(critical)
    return {"selected": sorted(selected), "uncovered": uncovered, "broad_required": require_broad,
            "blocked": require_broad and not broad, "executed": False}


def contract_watch(payload):
    before, after = payload.get("before"), payload.get("after")
    require(isinstance(before, dict) and isinstance(after, dict), "Contract comparison needs before and after objects")
    changes = [{"field": key, "before": value, "after": after.get(key), "breaking": key not in after or after[key] != value} for key, value in before.items() if after.get(key) != value or key not in after]
    changes += [{"field": k, "before": None, "after": v, "breaking": False} for k, v in after.items() if k not in before]
    return {"changes": changes, "consumers": payload.get("consumers", []), "compatibility_tests_required": bool(changes), "coverage_verified": False}


def independent_review(payload):
    identity = payload.get("candidate")
    require(isinstance(identity, str) and bool(identity), "Review requires immutable candidate identity")
    separate = bool(payload.get("reviewer")) and payload.get("reviewer") != payload.get("implementer") and payload.get("independence_evidence")
    findings = payload.get("findings", [])
    require(isinstance(findings, list), "Findings must be an array")
    return {"candidate": identity, "status": "blocked" if not separate or not payload.get("evidence") else "rejected" if findings else "review-recorded",
            "independence": "declared-with-evidence" if separate else "not-established", "findings": findings, "promotion_authorized": False}


def learning_comparison(payload):
    a, b = payload.get("baseline"), payload.get("candidate")
    require(isinstance(a, dict) and isinstance(b, dict), "Comparison needs baseline and candidate")
    keys = ("task", "artifact", "environment", "model", "settings", "acceptance", "gates", "counter_source", "includes_retries", "includes_subagents")
    comparable = all(k in a and k in b and a[k] == b[k] for k in keys) and a.get("passed") is True and b.get("passed") is True and a.get("includes_retries") is True and a.get("includes_subagents") is True
    actual = comparable and a.get("counter_source") in {"measured-host", "provider-usage"} and all(type(x.get("tokens")) is int and x["tokens"] >= 0 for x in (a,b)) and a["tokens"] > 0
    return {"comparable": bool(comparable), "tokens_saved": a["tokens"]-b["tokens"] if actual else None,
            "demonstrated": bool(actual and a["tokens"] > b["tokens"]), "policy_changed": False}


def diagnostics(payload):
    observations = payload.get("observations", [])
    require(isinstance(observations, list), "Observations must be an array")
    return {"status": "connected" if observations else "no-evidence", "findings": [
        {"component": o.get("component"), "evidence": o.get("evidence"), "message": o.get("message"), "cause": "unverified"}
        for o in observations if isinstance(o, dict) and o.get("level") in {"error","critical"} and o.get("evidence")], "repairs_executed": 0}


def evaluate(mod, payload, task):
    require(mod in MODULES and isinstance(payload, dict), "Invalid runtime module/payload")
    if mod in {"ore-signature-guard", "ore-safeguards-monitor"}:
        from ore_regulatory import evaluate_file
        result = evaluate_file(payload.get('_repo'), payload.get('contract'))
        expected = 'FDA_PART11_APPLICABILITY' if mod == 'ore-signature-guard' else 'FTC_SAFEGUARDS_APPLICABILITY'
        require(expected in result['gates'], 'Regulatory contract belongs to another module')
        return result
    functions = {"ore-autopilot": lambda p: autopilot(task,p), "ore-smart-tests": smart_tests,
        "ore-contract-watch": contract_watch, "ore-independent-review": independent_review,
        "ore-learning-lab": learning_comparison, "ore-runtime-diagnostics": diagnostics}
    if mod in functions:
        return functions[mod](payload)
    if mod in {"ore-first-contact","ore-visual-qa","ore-preview-certifier"}:
        from ore_first_contact import prepare_session, summarize_session, run_session
        if mod == "ore-first-contact" and payload.get("run_browser") is True:
            return run_session(payload.get("scenario"), payload.get("success_visible"))
        return summarize_session(payload) if "actions" in payload else prepare_session(payload)
    if mod in {"ore-flow-intelligence", "ore-flow-watch"}:
        from ore_flow import analyze_flow, watch_flow
        return analyze_flow(payload) if mod == "ore-flow-intelligence" else watch_flow(payload)
    if mod == "ore-context-sentinel":
        return {"task_id": task["id"], "revision": task["revision"], "objective": task["objective"], "next_action": task.get("next_action"), "blockers": task["blockers"], "context_counters": "host-only"}
    if mod == "ore-pr-pilot":
        return {"title": task["title"], "body": f"{task['objective']}\n\nValidation: {task.get('last_validation') or 'Not recorded'}\n\nBlockers: {'; '.join(task['blockers']) or 'None'}", "published": False}
    if mod in {"ore-scope-lock", "ore-never-again", "ore-approval-ledger"}:
        raise ValueError("Use explicit governance action, not evaluate")
    raise ValueError("This module is implemented by native read-only diagnostics, not artifact evaluation")
