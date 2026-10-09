#!/usr/bin/env python3
"""Deterministic, repository-local state for ORE tasks."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
TASK_STATUSES = {"active", "blocked", "complete"}
GATE_STATUSES = {"pending", "passed", "failed", "blocked", "not_applicable"}
TASK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,95}$")


class StateError(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (result[:48] or "task")


def safe_task_id(value: str) -> str:
    if not TASK_ID_PATTERN.fullmatch(value):
        raise StateError("Task id must match [a-z0-9][a-z0-9-]{0,95}")
    return value


def paths(repo: str) -> tuple[Path, Path, Path]:
    root = Path(repo).resolve()
    ore = root / ".ore"
    return ore, ore / "active.json", ore / "tasks"


@contextlib.contextmanager
def repo_lock(repo: str):
    """Serialize read-check-write across processes on Windows and POSIX."""
    ore, _, _ = paths(repo)
    ore.mkdir(parents=True, exist_ok=True)
    lock_path = ore / "state.lock"
    with lock_path.open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError as exc:
        raise StateError(f"State file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StateError(f"Invalid JSON state: {path}: {exc}") from exc


def validate_form_contract(repo: str, value: str) -> Path:
    root = Path(repo).resolve()
    forms_root = (root / ".ore" / "forms").resolve()
    candidate = (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    try:
        candidate.relative_to(forms_root)
    except ValueError as exc:
        raise StateError("Form contracts must stay under .ore/forms/") from exc
    contract = load_json(candidate)
    required = {"id", "user_role", "job", "canonical_entity", "fields", "states", "accessibility", "submission", "test_cases"}
    missing = sorted(required - contract.keys())
    if missing:
        raise StateError(f"Form contract missing keys: {missing}")
    if not isinstance(contract["fields"], list) or not contract["fields"]:
        raise StateError("Form contract must contain at least one field")
    field_keys = {"id", "type", "required", "source", "client_validation", "server_validation", "error", "privacy"}
    for index, field in enumerate(contract["fields"]):
        absent = sorted(field_keys - field.keys())
        if absent:
            raise StateError(f"Form field {index} missing keys: {absent}")
    if not isinstance(contract["states"], list) or not contract["states"]:
        raise StateError("Form contract states must be a non-empty list")
    accessibility = contract["accessibility"]
    if not isinstance(accessibility, dict) or not all(accessibility.get(key) is True for key in ("keyboard", "screen_reader", "text_scaling")):
        raise StateError("Form accessibility must explicitly cover keyboard, screen_reader, and text_scaling")
    submission = contract["submission"]
    if not isinstance(submission, dict) or submission.get("idempotent") is not True:
        raise StateError("Form submission must declare idempotent=true")
    cases = set(contract["test_cases"]) if isinstance(contract["test_cases"], list) else set()
    required_cases = {"happy", "invalid", "server_error", "double_submit"}
    if not required_cases.issubset(cases):
        raise StateError(f"Form test_cases must include {sorted(required_cases)}")
    return candidate


def verify_authoritative_list(repo: str, contract_path: Path, raw: str) -> dict:
    if "=" not in raw:
        raise StateError(f"Invalid authoritative list '{raw}'; use FIELD=JSON_FILE")
    field_id, list_value = raw.split("=", 1)
    root = Path(repo).resolve()
    list_path = (root / list_value).resolve() if not Path(list_value).is_absolute() else Path(list_value).resolve()
    try:
        relative = list_path.relative_to(root)
    except ValueError as exc:
        raise StateError("Authoritative list must be stored inside the workspace") from exc
    contract = load_json(contract_path)
    fields = {field["id"]: field for field in contract["fields"]}
    if field_id not in fields:
        raise StateError(f"Unknown contract field: {field_id}")
    expected = load_json(list_path)
    actual = fields[field_id].get("allowed_values")
    if not isinstance(expected, list):
        raise StateError("Authoritative list must be a JSON array")
    if actual != expected:
        raise StateError(f"Authoritative values/order mismatch for field '{field_id}'")
    return {
        "contract": str(contract_path.relative_to(root)).replace("\\", "/"),
        "field": field_id,
        "source": str(relative).replace("\\", "/"),
        "source_sha256": hashlib.sha256(list_path.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
    }


def verify_form_integrity(task: dict, repo: str) -> None:
    root = Path(repo).resolve()
    for relative in task.get("form_contracts", []):
        contract_path = validate_form_contract(repo, relative)
        expected_digest = task.get("form_contract_digests", {}).get(relative)
        current_digest = hashlib.sha256(contract_path.read_bytes()).hexdigest()
        if not expected_digest or current_digest != expected_digest:
            raise StateError(f"Form contract changed after gate approval: {relative}")
    for proof in task.get("authoritative_lists_verified", []):
        source_path = root / proof["source"]
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != proof["source_sha256"]:
            raise StateError(f"Authoritative list changed after gate approval: {proof['source']}")
        refreshed = verify_authoritative_list(repo, root / proof["contract"], f"{proof['field']}={proof['source']}")
        if refreshed["contract_sha256"] != proof["contract_sha256"]:
            raise StateError(f"Form contract changed after list verification: {proof['contract']}")


def active_task(repo: str, task_id: str | None = None) -> tuple[dict, Path]:
    _, active_path, task_dir = paths(repo)
    if task_id is None:
        pointer = load_json(active_path)
        if not isinstance(pointer, dict):
            raise StateError("Active state must be a JSON object")
        task_id = pointer.get("task_id")
    if not task_id:
        raise StateError(f"Invalid active pointer: {active_path}")
    task_id = safe_task_id(task_id)
    task_path = task_dir / f"{task_id}.json"
    task = load_json(task_path)
    if not isinstance(task, dict):
        raise StateError("Task state must be a JSON object")
    return task, task_path


def parse_deliverables(values: list[str]) -> list[dict]:
    result = []
    seen = set()
    for value in values:
        try:
            name, raw_weight = value.rsplit(":", 1)
            weight = int(raw_weight)
        except (ValueError, TypeError) as exc:
            raise StateError(f"Invalid deliverable '{value}'; use Name:weight") from exc
        name = name.strip()
        if not name or name in seen or weight <= 0:
            raise StateError(f"Invalid or duplicate deliverable: {value}")
        seen.add(name)
        result.append({"name": name, "weight": weight, "completion": 0, "status": "pending", "evidence": []})
    if not result or sum(item["weight"] for item in result) != 100:
        raise StateError("Deliverable weights must total exactly 100")
    return result


def progress(task: dict) -> int:
    raw = sum(item["weight"] * item["completion"] / 100 for item in task["deliverables"])
    return int(round(raw))


def assert_revision(task: dict, expected: int | None) -> None:
    if expected is not None and task.get("revision") != expected:
        raise StateError(
            f"Revision conflict: expected {expected}, current {task.get('revision')}. "
            "Resume and reconcile before writing."
        )


def event(task: dict, kind: str, detail: str) -> None:
    task.setdefault("events", []).append({"at": now(), "kind": kind, "detail": detail})


def save_task(repo: str, task: dict, task_path: Path) -> None:
    task["progress"] = progress(task)
    task["updated_at"] = now()
    task["revision"] = int(task.get("revision", 0)) + 1
    atomic_json(task_path, task)
    write_handoff(repo, task)


def write_handoff(repo: str, task: dict) -> None:
    ore, _, _ = paths(repo)
    handoff = ore / "handoffs" / f"{task['id']}.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    completed = [item["name"] for item in task["deliverables"] if item["completion"] == 100]
    open_gates = [f"{name}: {gate['status']}" for name, gate in task["gates"].items() if gate["status"] not in {"passed", "not_applicable"}]
    lines = [
        f"# ORE handoff — {task['title']}",
        "",
        f"- Task: `{task['id']}`",
        f"- Revision: {task['revision']}",
        f"- Status: {task['status']}",
        f"- Progress: {task['progress']}%",
        f"- Objective: {task['objective']}",
        f"- Acceptance: {'; '.join(task.get('acceptance_criteria', [])) or 'Not recorded'}",
        f"- Completed: {', '.join(completed) if completed else 'None verified'}",
        f"- Roles: {', '.join(task['roles']) if task['roles'] else 'None assigned'}",
        *([f"- Active specialist: {task['active_specialist']['department']} -> {task['active_specialist']['specialist']} (domain lead: {task['active_specialist']['domain_lead']})"] if task.get("active_specialist") else []),
        f"- Active files: {', '.join(task.get('active_files', [])) if task.get('active_files') else 'None recorded'}",
        f"- Last validation: {task.get('last_validation') or 'None recorded'}",
        f"- Decisions: {'; '.join(item['detail'] for item in task['decisions']) if task['decisions'] else 'None'}",
        f"- Open questions: {'; '.join(task.get('open_questions', [])) if task.get('open_questions') else 'None'}",
        f"- Open gates: {', '.join(open_gates) if open_gates else 'None'}",
        f"- Blockers: {'; '.join(task['blockers']) if task['blockers'] else 'None'}",
        f"- Next action: {task.get('next_action') or 'Not recorded'}",
        "",
        "Repository evidence overrides this handoff if they disagree.",
    ]
    handle, temp_name = tempfile.mkstemp(prefix=f".{handoff.name}.", suffix=".tmp", dir=handoff.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("\n".join(lines) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, handoff)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def cmd_start(args: argparse.Namespace) -> dict:
    with repo_lock(args.repo):
        ore, active_path, task_dir = paths(args.repo)
        task_id = safe_task_id(args.task_id) if args.task_id else f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S%f')}-{slug(args.title)}"
        task_path = task_dir / f"{task_id}.json"
        if task_path.exists():
            raise StateError(f"Task already exists: {task_id}")
        stamp = now()
        form_signal = re.search(r"\b(forms?|formularios?|wizard|onboarding|checkout|data[- ]entry|survey|encuesta|registration|registro|settings? editor|upload flow|application)\b", f"{args.title} {args.objective}", re.IGNORECASE)
        if form_signal and args.kind != "form":
            raise StateError("Form-like task detected; start it with --kind form")
        gate_names = list(dict.fromkeys(args.gate))
        if args.risk in {"L3", "L4", "L5"}:
            gate_names.append("INDEPENDENT_REVIEW")
        gates = {name: {"required": True, "status": "pending", "evidence": []} for name in dict.fromkeys(gate_names)}
        task = {
            "schema_version": SCHEMA_VERSION,
            "id": task_id,
            "title": args.title,
            "objective": args.objective,
            "kind": args.kind,
            "acceptance_criteria": args.acceptance,
            "risk": args.risk,
            "status": "active",
            "created_at": stamp,
            "updated_at": stamp,
            "revision": 1,
            "progress": 0,
            "deliverables": parse_deliverables(args.deliverable),
            "gates": gates,
            "roles": [],
            "decisions": [],
            "open_questions": [],
            "form_contracts": [],
            "form_contract_digests": {},
            "authoritative_lists_verified": [],
            "blockers": [],
            "active_files": [],
            "last_validation": None,
            "next_action": args.next or "Establish repository baseline",
            "events": [{"at": stamp, "kind": "started", "detail": args.objective}],
        }
        atomic_json(task_path, task)
        atomic_json(active_path, {"schema_version": SCHEMA_VERSION, "task_id": task_id, "updated_at": stamp})
        write_handoff(args.repo, task)
        return task


def parse_completion(raw: str) -> tuple[str, int, str]:
    try:
        name, value = raw.rsplit("=", 1)
    except ValueError as exc:
        raise StateError(f"Invalid deliverable update '{raw}'; use Name=value") from exc
    value = value.strip().lower()
    named = {"pending": 0, "in_progress": 1, "done": 100, "blocked": 0}
    if value in named:
        return name.strip(), named[value], value
    try:
        amount = int(value)
    except ValueError as exc:
        raise StateError(f"Invalid completion '{value}'; use 0..100 or a named status") from exc
    if not 0 <= amount <= 100:
        raise StateError("Completion must be between 0 and 100")
    return name.strip(), amount, "done" if amount == 100 else ("pending" if amount == 0 else "in_progress")


def parse_evidence(values: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for raw in values:
        if ":" not in raw:
            raise StateError(f"Invalid evidence '{raw}'; use Subject:evidence")
        subject, detail = raw.split(":", 1)
        if not subject.strip() or not detail.strip():
            raise StateError(f"Invalid evidence '{raw}'")
        result.setdefault(subject.strip(), []).append(detail.strip())
    return result


def cmd_update(args: argparse.Namespace) -> dict:
    with repo_lock(args.repo):
        task, task_path = active_task(args.repo, args.task_id)
        assert_revision(task, args.expect_revision)
        evidence = parse_evidence(args.evidence)
        identity = (args.active_specialist, args.department, args.domain_lead)
        if any(identity):
            if not all(identity):
                raise StateError("Active specialist requires --active-specialist, --department, and --domain-lead")
            if not re.fullmatch(r"\$?ore-[a-z0-9-]+", args.active_specialist):
                raise StateError("Active specialist must be an ORE skill name")
            specialist = {
                "specialist": args.active_specialist.lstrip("$"),
                "department": args.department,
                "domain_lead": args.domain_lead,
                "revision": task["revision"] + 1,
            }
            previous = task.get("active_specialist", {})
            if any(previous.get(key) != specialist[key] for key in ("specialist", "department", "domain_lead")):
                task["active_specialist"] = specialist
                task.setdefault("events", []).append({"at": now(), "kind": "specialist_changed", **specialist})
        for raw_path in args.form_contract:
            resolved = validate_form_contract(args.repo, raw_path)
            relative = str(resolved.relative_to(Path(args.repo).resolve())).replace("\\", "/")
            if relative not in task["form_contracts"]:
                task["form_contracts"].append(relative)
            if task["gates"]["FORM_INTELLIGENCE"]["status"] == "passed":
                task["gates"]["FORM_INTELLIGENCE"]["status"] = "pending"
                event(task, "gate_invalidated", "FORM_INTELLIGENCE: form contract changed")
        for raw_list in args.authoritative_list:
            if not task["form_contracts"]:
                raise StateError("--authoritative-list requires a validated --form-contract")
            contract_path = Path(args.repo).resolve() / task["form_contracts"][-1]
            proof = verify_authoritative_list(args.repo, contract_path, raw_list)
            task["authoritative_lists_verified"] = [
                item for item in task["authoritative_lists_verified"]
                if not (item["contract"] == proof["contract"] and item["field"] == proof["field"])
            ]
            task["authoritative_lists_verified"].append(proof)
            if task["gates"]["FORM_INTELLIGENCE"]["status"] == "passed":
                task["gates"]["FORM_INTELLIGENCE"]["status"] = "pending"
                event(task, "gate_invalidated", "FORM_INTELLIGENCE: authoritative list proof changed")
        for gate_name in args.add_gate:
            if gate_name in task["gates"]:
                raise StateError(f"Gate already exists: {gate_name}")
            task["gates"][gate_name] = {"required": True, "status": "pending", "evidence": []}
        deliverables = {item["name"]: item for item in task["deliverables"]}
        for raw in args.deliverable:
            name, amount, status = parse_completion(raw)
            if name not in deliverables:
                raise StateError(f"Unknown deliverable: {name}")
            previous = deliverables[name]["completion"]
            if amount < previous and not args.allow_regression:
                raise StateError(f"Completion cannot decrease for '{name}' without --allow-regression")
            item_evidence = evidence.pop(name, [])
            if amount > previous and not item_evidence:
                raise StateError(f"Progress increase for '{name}' requires --evidence '{name}:...'")
            deliverables[name]["completion"] = amount
            deliverables[name]["status"] = status
            deliverables[name]["evidence"].extend(item_evidence)
            event(task, "deliverable", f"{name}={amount}%")
        for raw in args.gate:
            if "=" not in raw:
                raise StateError(f"Invalid gate update '{raw}'; use NAME=status")
            name, status = (part.strip() for part in raw.rsplit("=", 1))
            if name not in task["gates"]:
                raise StateError(f"Unknown gate: {name}")
            if status not in GATE_STATUSES:
                raise StateError(f"Invalid gate status: {status}")
            gate_evidence = evidence.pop(name, [])
            if status in {"passed", "not_applicable"} and not gate_evidence:
                raise StateError(f"Closing gate '{name}' requires evidence or a not-applicable reason")
            from ore_regulatory import GATES as REGULATORY_GATES, evaluate_file
            if name in REGULATORY_GATES and status in {"passed", "not_applicable"}:
                proofs = []
                reports = []
                for contract in gate_evidence:
                    try:
                        report = evaluate_file(args.repo, contract)
                        if name not in report['gates'] or report['gates'][name]['status'] != status:
                            raise ValueError('Requested gate outcome is not verified by contract')
                        proofs.extend(report['dependencies'])
                        reports.append(report['gates'][name])
                    except (OSError, ValueError, KeyError, TypeError) as error:
                        raise StateError(f'Regulatory gate blocked: {error}') from error
                task['gates'][name]['regulatory_proofs'] = proofs
                task['gates'][name]['regulatory_controls'] = reports
            if name == "FORM_INTELLIGENCE" and status == "passed" and not task["form_contracts"]:
                raise StateError("FORM_INTELLIGENCE requires a validated --form-contract")
            if name == "FORM_INTELLIGENCE" and status == "not_applicable" and task.get("kind") == "form":
                raise StateError("FORM_INTELLIGENCE cannot be not_applicable for a form task")
            if name == "FORM_INTELLIGENCE" and status == "passed":
                for relative in task["form_contracts"]:
                    contract_path = validate_form_contract(args.repo, relative)
                    contract = load_json(contract_path)
                    required_fields = {
                        field["id"] for field in contract["fields"]
                        if field.get("authoritative") is True or field.get("source") == "user-supplied list"
                    }
                    proved = {
                        item["field"] for item in task["authoritative_lists_verified"]
                        if item["contract"] == relative
                    }
                    if not required_fields.issubset(proved):
                        raise StateError(f"Unverified authoritative form lists: {sorted(required_fields - proved)}")
                    task["form_contract_digests"][relative] = hashlib.sha256(contract_path.read_bytes()).hexdigest()
            task["gates"][name]["status"] = status
            task["gates"][name]["evidence"].extend(gate_evidence)
            event(task, "gate", f"{name}={status}")
        if evidence:
            raise StateError(f"Evidence subjects were not updated: {', '.join(evidence)}")
        if args.next:
            task["next_action"] = args.next
        for role in args.role:
            if role not in task["roles"]:
                task["roles"].append(role)
        for decision in args.decision:
            task["decisions"].append({"at": now(), "detail": decision})
        for question in args.question:
            if question not in task["open_questions"]:
                task["open_questions"].append(question)
        for question in args.resolve_question:
            if question in task["open_questions"]:
                task["open_questions"].remove(question)
        if args.file:
            task["active_files"] = list(dict.fromkeys(args.file))
        if args.validation:
            task["last_validation"] = args.validation
        if args.blocker:
            task["blockers"].extend(args.blocker)
            task["status"] = "blocked"
        elif task["status"] == "blocked" and args.clear_blockers:
            task["blockers"] = []
            task["status"] = "active"
        save_task(args.repo, task, task_path)
        return task


def cmd_checkpoint(args: argparse.Namespace) -> dict:
    with repo_lock(args.repo):
        task, task_path = active_task(args.repo, args.task_id)
        assert_revision(task, args.expect_revision)
        if args.next:
            task["next_action"] = args.next
        event(task, "checkpoint", args.note or task["next_action"])
        save_task(args.repo, task, task_path)
        return task


def cmd_complete(args: argparse.Namespace) -> dict:
    with repo_lock(args.repo):
        task, task_path = active_task(args.repo, args.task_id)
        assert_revision(task, args.expect_revision)
        incomplete = [item["name"] for item in task["deliverables"] if item["completion"] != 100]
        open_gates = [name for name, gate in task["gates"].items() if gate["required"] and gate["status"] not in {"passed", "not_applicable"}]
        if incomplete or open_gates or task["blockers"]:
            raise StateError(f"Cannot complete; incomplete={incomplete}, open_gates={open_gates}, blockers={task['blockers']}")
        from ore_regulatory import GATES as REGULATORY_GATES, evidence as verify_regulatory_evidence
        for gate_name, gate in task['gates'].items():
            if gate_name in REGULATORY_GATES and gate['status'] in {'passed', 'not_applicable'}:
                if not gate.get('regulatory_proofs'):
                    raise StateError('Regulatory gate has no verified evidence')
                for proof in gate['regulatory_proofs']:
                    try:
                        verify_regulatory_evidence(Path(args.repo).resolve(), dict(proof, owner='state-writer',
                            validation='completion digest recheck', limitations=[], at=now()))
                    except (OSError, ValueError) as error:
                        raise StateError(f'Regulatory evidence changed: {error}') from error
        if task["gates"].get("FORM_INTELLIGENCE", {}).get("status") == "passed":
            verify_form_integrity(task, args.repo)
        task["status"] = "complete"
        task["next_action"] = args.next or "No in-scope action remains"
        event(task, "completed", task["next_action"])
        save_task(args.repo, task, task_path)
        return task


def cmd_resume(args: argparse.Namespace) -> dict:
    with repo_lock(args.repo):
        task, _ = active_task(args.repo, args.task_id)
        if task.get("schema_version") != SCHEMA_VERSION:
            raise StateError(f"Unsupported schema version: {task.get('schema_version')}")
        if args.task_id:
            _, active_path, _ = paths(args.repo)
            atomic_json(active_path, {"schema_version": SCHEMA_VERSION, "task_id": task["id"], "updated_at": now()})
        return task


def cmd_list(args: argparse.Namespace) -> dict:
    _, _, task_dir = paths(args.repo)
    tasks = []
    if task_dir.exists():
        for path in sorted(task_dir.glob("*.json")):
            task = load_json(path)
            tasks.append({key: task.get(key) for key in ("id", "title", "status", "progress", "revision", "updated_at")})
    return {"tasks": tasks}


def output(task: dict) -> None:
    if "runtime_result" in task or "governance" in task:
        print(json.dumps(task, ensure_ascii=False))
        return
    if "tasks" in task:
        print(json.dumps(task, ensure_ascii=False))
        return
    summary = {
        "task_id": task["id"],
        "status": task["status"],
        "progress": task["progress"],
        "revision": task["revision"],
        "title": task["title"],
        "objective": task["objective"],
        "kind": task.get("kind", "general"),
        "acceptance_criteria": task.get("acceptance_criteria", []),
        "deliverables": task["deliverables"],
        "gates": task["gates"],
        "roles": task["roles"],
        **({"active_specialist": task["active_specialist"]} if task.get("active_specialist") else {}),
        "decisions": task["decisions"],
        "open_questions": task.get("open_questions", []),
        "form_contracts": task.get("form_contracts", []),
        "authoritative_lists_verified": task.get("authoritative_lists_verified", []),
        "blockers": task["blockers"],
        "active_files": task.get("active_files", []),
        "last_validation": task.get("last_validation"),
        "next_action": task.get("next_action"),
        "open_gates": [name for name, gate in task["gates"].items() if gate["status"] not in {"passed", "not_applicable"}],
    }
    print(json.dumps(summary, ensure_ascii=False))


def cmd_runtime(args: argparse.Namespace) -> dict:
    """Explicit optional runtime operations; this module remains the only writer."""
    from ore_runtime import (MODULES, GOVERNANCE_ACTIONS, apply_governance,
                             evaluate, initial_governance, project_id, validate_governance)
    try:
        if args.mod not in MODULES:
            raise StateError("Unknown runtime module")
        payload = json.loads(args.payload)
        if not isinstance(payload, dict) or len(args.payload) > 1_000_000:
            raise StateError("Runtime payload must be a bounded JSON object")
        root = Path(args.repo).resolve()
        # Read-only evaluations neither create .ore nor acquire its creating lock.
        if args.action == "evaluate":
            task, _ = active_task(args.repo, args.task_id)
            assert_revision(task, args.expect_revision)
            if args.mod in {"ore-scope-lock", "ore-never-again", "ore-approval-ledger"}:
                from ore_runtime import check_paths, valid_now
                target = root / ".ore" / "governance.json"
                if not target.exists():
                    return {"runtime_result": {"enabled": False}, "revision": task["revision"]}
                try:
                    data = validate_governance(load_json(target), project_id(root))
                except (StateError, ValueError, TypeError, KeyError):
                    return {"runtime_result": {"enabled": False}, "revision": task["revision"]}
                if args.mod == "ore-approval-ledger":
                    result = {"revision": data["revision"], "approvals": [r for r in data["approvals"] if valid_now(r, now())], "grants_native_permissions": False}
                elif "paths" in payload:
                    if not isinstance(payload["paths"], list) or not payload["paths"]:
                        raise StateError("Path review needs a nonempty list")
                    relative = []
                    for value in payload["paths"]:
                        if not isinstance(value, str) or not value or value.startswith(("~", "//", "\\\\")) or re.match(r"^[A-Za-z]:(?![\\/])", value):
                            return {"runtime_result": {"allowed": False, "violations": ["Path spelling cannot be safely resolved"]}, "revision": task["revision"]}
                        resolved = (root / value).resolve()
                        try:
                            relative.append(resolved.relative_to(root).as_posix())
                        except ValueError:
                            return {"runtime_result": {"allowed": False, "violations": ["Path resolves outside the repository"]}, "revision": task["revision"]}
                    result = check_paths(data, relative, now())
                    result["governance_revision"] = data["revision"]
                else:
                    result = {"revision": data["revision"], "rules": data["rules"], "exceptions": data["exceptions"],
                              "metrics": {"active_rules": sum(valid_now(r, now()) for r in data["rules"]),
                                          "replaced_rules": sum(r.get("status") == "replaced" for r in data["rules"]),
                                          "active_exceptions": sum(valid_now(r, now()) for r in data["exceptions"]),
                                          "prevented_incidents": None, "rule_hits": None}}
                return {"runtime_result": result, "revision": task["revision"]}
            if args.mod in {'ore-signature-guard', 'ore-safeguards-monitor'}:
                payload['_repo'] = str(root)
            return {"runtime_result": evaluate(args.mod, payload, task), "revision": task["revision"]}
        if args.action not in GOVERNANCE_ACTIONS or not args.confirmed:
            raise StateError("Governance writes require an explicit confirmed action")
        allowed = {"ore-scope-lock": {"scope", "exception"},
                   "ore-never-again": {"rule", "revoke-rule", "exception"},
                   "ore-approval-ledger": {"approval", "revoke-approval"}}
        if args.action not in allowed.get(args.mod, set()):
            raise StateError("Action does not belong to this governance module")
        with repo_lock(args.repo):
            task, _ = active_task(args.repo, args.task_id)
            assert_revision(task, args.expect_revision)
            current, _ = active_task(args.repo)
            if current["id"] != task["id"] or task["status"] == "complete":
                raise StateError("Governance requires the current active unfinished task")
            target = root / ".ore" / "governance.json"
            identity = project_id(root)
            data = load_json(target) if target.exists() else initial_governance(identity)
            validate_governance(data, identity)
            if data["revision"] != args.expect_governance_revision:
                raise StateError("Governance revision conflict; reload before confirming")
            updated = apply_governance(data, args.action, payload, identity, now(), True)
            updated["events"][-1]["task_id"] = task["id"]
            updated["events"][-1]["task_revision"] = task["revision"]
            if args.action == "approval":
                updated["approvals"][-1]["task_id"] = task["id"]
            atomic_json(target, updated)
            return {"governance": updated, "revision": task["revision"]}
    except (ValueError, TypeError, KeyError) as exc:
        raise StateError(str(exc)) from exc


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", required=True)
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    runtime = commands.add_parser("runtime", parents=[common])
    runtime.add_argument("--task-id", required=True)
    runtime.add_argument("--expect-revision", type=int, required=True)
    runtime.add_argument("--expect-governance-revision", type=int, default=0)
    runtime.add_argument("--mod", required=True)
    runtime.add_argument("--action", default="evaluate")
    runtime.add_argument("--payload", required=True)
    runtime.add_argument("--confirmed", action="store_true")
    runtime.set_defaults(func=cmd_runtime)

    start = commands.add_parser("start", parents=[common])
    start.add_argument("--title", required=True)
    start.add_argument("--objective", required=True)
    start.add_argument("--kind", choices=["general", "form"], required=True)
    start.add_argument("--acceptance", action="append", required=True)
    start.add_argument("--task-id")
    start.add_argument("--risk", choices=[f"L{i}" for i in range(6)], default="L2")
    start.add_argument("--deliverable", action="append", required=True)
    start.add_argument("--gate", action="append", default=["SPEC_FIDELITY", "FORM_INTELLIGENCE", "HANDOFF"])
    start.add_argument("--next")
    start.set_defaults(func=cmd_start)

    resume = commands.add_parser("resume", parents=[common])
    resume.add_argument("--task-id")
    resume.set_defaults(func=cmd_resume)

    list_tasks = commands.add_parser("list", parents=[common])
    list_tasks.set_defaults(func=cmd_list)

    update = commands.add_parser("update", parents=[common])
    update.add_argument("--task-id", required=True)
    update.add_argument("--expect-revision", type=int, required=True)
    update.add_argument("--deliverable", action="append", default=[])
    update.add_argument("--gate", action="append", default=[])
    update.add_argument("--add-gate", action="append", default=[])
    update.add_argument("--evidence", action="append", default=[])
    update.add_argument("--next")
    update.add_argument("--role", action="append", default=[])
    update.add_argument("--active-specialist")
    update.add_argument("--department")
    update.add_argument("--domain-lead")
    update.add_argument("--decision", action="append", default=[])
    update.add_argument("--question", action="append", default=[])
    update.add_argument("--resolve-question", action="append", default=[])
    update.add_argument("--form-contract", action="append", default=[])
    update.add_argument("--authoritative-list", action="append", default=[])
    update.add_argument("--file", action="append", default=[])
    update.add_argument("--validation")
    update.add_argument("--blocker", action="append", default=[])
    update.add_argument("--clear-blockers", action="store_true")
    update.add_argument("--allow-regression", action="store_true")
    update.set_defaults(func=cmd_update)

    checkpoint = commands.add_parser("checkpoint", parents=[common])
    checkpoint.add_argument("--task-id", required=True)
    checkpoint.add_argument("--expect-revision", type=int, required=True)
    checkpoint.add_argument("--next")
    checkpoint.add_argument("--note")
    checkpoint.set_defaults(func=cmd_checkpoint)

    complete = commands.add_parser("complete", parents=[common])
    complete.add_argument("--task-id", required=True)
    complete.add_argument("--expect-revision", type=int, required=True)
    complete.add_argument("--next")
    complete.set_defaults(func=cmd_complete)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        output(args.func(args))
        return 0
    except StateError as exc:
        print(f"ORE state error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
