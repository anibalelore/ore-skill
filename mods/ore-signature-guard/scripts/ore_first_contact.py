#!/usr/bin/env python3
"""Bounded, black-box browser exploration of explicitly isolated local fixtures.

This module never writes ORE state. Evidence must be imported by ore_state.py.
"""
from __future__ import annotations

import argparse
import functools
import importlib.util
import json
import re
import threading
import time
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

PROFILES = {
    "new": {"max_actions": 12, "delay_ms": 100, "viewport": [1280, 800]},
    "impatient": {"max_actions": 5, "delay_ms": 0, "viewport": [1280, 800]},
    "expert": {"max_actions": 16, "delay_ms": 0, "viewport": [1280, 800]},
    "low_experience": {"max_actions": 8, "delay_ms": 300, "viewport": [1280, 800]},
    "mobile": {"max_actions": 12, "delay_ms": 100, "viewport": [390, 844]},
    "limited_connectivity": {"max_actions": 8, "delay_ms": 700, "viewport": [1280, 800]},
    "accessibility": {"max_actions": 12, "delay_ms": 100, "viewport": [1280, 800]},
    "unauthorized": {"max_actions": 8, "delay_ms": 100, "viewport": [1280, 800]},
}
FORBIDDEN = re.compile(r"\b(pay|purchase|checkout|buy|send|publish|deploy|delete|transfer)\b", re.I)
SECRET_KEYS = re.compile(r"password|secret|token|credential|authorization|cookie|email|phone", re.I)


def redact(value):
    """Redact known sensitive keys and credential-like text before evidence export."""
    if isinstance(value, dict):
        return {k: "[REDACTED]" if SECRET_KEYS.search(k) else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        value = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED EMAIL]", value)
        value = re.sub(r"(?i)(password|token|secret|api[_-]?key)\s*[:=]\s*\S+", r"\1=[REDACTED]", value)
        value = re.sub(r"\b\d{13,19}\b", "[REDACTED NUMBER]", value)
    return value


def local_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and parsed.hostname in {"127.0.0.1", "localhost", "::1"} and not parsed.username and not parsed.password
    except (ValueError, TypeError):
        return False


def request_allowed(start_url, target_url, method):
    """Fail closed for mutations and redirects outside the exact local origin."""
    if not local_url(start_url) or not local_url(target_url) or method not in {"GET", "HEAD"}:
        return False
    try:
        start, target = urlparse(start_url), urlparse(target_url)
        return (start.scheme, start.hostname, start.port) == (target.scheme, target.hostname, target.port)
    except ValueError:
        return False


def validate_scenario(data) -> list[str]:
    if not isinstance(data, dict):
        return ["Scenario must be an object."]
    errors = []
    allowed = {"url", "goal", "environment", "isolated_environment_confirmed", "synthetic_accounts_confirmed",
               "authorized", "profile", "max_actions", "timeout_seconds", "retention_hours", "synthetic_fields"}
    allowed.update({"artifact_directory", "capture_screenshots", "synthetic_screen_capture_confirmed"})
    if set(data) - allowed:
        errors.append("Unknown scenario fields are rejected; only the documented contract is accepted.")
    if not local_url(data.get("url")):
        errors.append("Only loopback HTTP(S) URLs are supported; staging and production are rejected.")
    if data.get("environment") != "isolated_test":
        errors.append("environment must be isolated_test.")
    for field in ("isolated_environment_confirmed", "synthetic_accounts_confirmed", "authorized"):
        if data.get(field) is not True:
            errors.append(f"{field} must be explicitly true.")
    if not isinstance(data.get("goal"), str) or not data["goal"].strip():
        errors.append("A user-facing goal is required.")
    if data.get("profile", "new") not in PROFILES:
        errors.append("Unknown simulation profile.")
    if any(key in data for key in ("selectors", "source", "steps", "routes", "answers")):
        errors.append("Explorer scenarios cannot supply implementation details or completion steps.")
    for field, upper in (("max_actions", 30), ("timeout_seconds", 60), ("retention_hours", 24)):
        value = data.get(field, 12 if field == "max_actions" else 30 if field == "timeout_seconds" else 24)
        if type(value) is not int or not 1 <= value <= upper:
            errors.append(f"{field} must be an integer between 1 and {upper}.")
    if not isinstance(data.get("synthetic_fields", {}), dict):
        errors.append("synthetic_fields must map visible labels to synthetic test data.")
    if "capture_screenshots" in data and type(data["capture_screenshots"]) is not bool:
        errors.append("capture_screenshots must be a boolean.")
    if data.get("capture_screenshots") and (data.get("synthetic_screen_capture_confirmed") is not True or not data.get("artifact_directory")):
        errors.append("Screenshots require artifact_directory and explicit synthetic_screen_capture_confirmed.")
    if data.get("artifact_directory"):
        try:
            artifact_path(data["artifact_directory"])
        except (TypeError, ValueError, OSError) as error:
            errors.append(str(error))
    return errors


def artifact_path(value):
    """Resolve links before checking that artifacts cannot enter ORE state."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("artifact_directory must be a nonempty path")
    target = Path(value).resolve()
    if any(part.casefold() == ".ore" for part in target.parts):
        raise ValueError("Artifacts must be outside .ore")
    return target


def cleanup_artifacts(directory, current_time=None):
    """Delete only expired files listed by an adapter-owned, well-formed manifest."""
    root = artifact_path(str(directory))
    current_time = time.time() if current_time is None else current_time
    removed = []
    if not root.is_dir():
        return removed
    for manifest in root.glob("ore-first-contact-*.json"):
        if manifest.is_symlink():
            continue
        try:
            saved = json.loads(manifest.read_text(encoding="utf-8"))
            prefix = saved.get("artifact_prefix", "")
            if not re.fullmatch(r"ore-first-contact-[a-f0-9]{32}", prefix) or manifest.name != prefix + ".json":
                continue
            expiry = saved.get("expires_at_epoch")
            if type(expiry) not in {int, float} or expiry > current_time:
                continue
            for name in saved.get("artifact_files", []):
                if isinstance(name, str) and re.fullmatch(re.escape(prefix) + r"-\d{2}\.png", name):
                    candidate = root / name
                    if candidate.is_file() and not candidate.is_symlink() and candidate.resolve().parent == root:
                        candidate.unlink()
                        removed.append(name)
            manifest.unlink()
            removed.append(manifest.name)
        except (OSError, ValueError, TypeError):
            continue
    return removed


def prepare_session(scenario) -> dict:
    errors = validate_scenario(scenario)
    available = importlib.util.find_spec("playwright") is not None
    return {"schema_version": 1, "status": "invalid" if errors else "ready" if available else "blocked",
            "errors": errors, "attempts": 0, "browser_available": available,
            "limitation": None if available else "Playwright is not installed; no browser results were simulated.",
            "profile_parameters": PROFILES.get(scenario.get("profile", "new"), {}) if isinstance(scenario, dict) else {}}


def summarize_session(evidence) -> dict:
    if not isinstance(evidence, dict):
        raise ValueError("Evidence must be an object")
    actions = evidence.get("actions", [])
    if not isinstance(actions, list) or any(not isinstance(a, dict) for a in actions):
        raise ValueError("actions must be a list of observed action objects")
    observed = evidence.get("provenance") in {"playwright", "imported_observation"}
    outcome = evidence.get("outcome", "unverified")
    verified = observed and evidence.get("goal_observed") is True and outcome == "completed" and bool(actions)
    retention = evidence.get("retention_hours", 24)
    if type(retention) is not int or not 1 <= retention <= 24:
        retention = 24
    return redact({"schema_version": 1, "status": "completed" if verified else "blocked" if outcome == "blocked" else "unverified",
                   "attempts": len(actions), "goal_verified": verified, "actions": actions[-30:],
                   "findings": evidence.get("findings", []), "limitation": evidence.get("limitation"),
                   "provenance": evidence.get("provenance", "unknown"),
                   "trust": "imported observations are external assertions, not independently verified" if evidence.get("provenance") == "imported_observation" else "local browser observation",
                   "elapsed_seconds": evidence.get("elapsed_seconds"), "retention_hours": retention})


def choose_action(elements, goal, visited):
    """Use only visible names and roles; never source, internal routes, or selectors."""
    words = set(re.findall(r"[a-z]{3,}", goal.lower())) - {"the", "with", "want", "please"}
    candidates = [(len(words & set(re.findall(r"[a-z]{3,}", e["name"].lower()))), e)
                  for e in elements if e["name"] and (e["role"], e["name"]) not in visited and not FORBIDDEN.search(e["name"])]
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1] if candidates else None


def run_session(scenario, success_visible=None) -> dict:
    prepared = prepare_session(scenario)
    evidence = {"provenance": "playwright", "outcome": "blocked", "actions": [], "goal_observed": False,
                "findings": [], "retention_hours": scenario.get("retention_hours", 24) if isinstance(scenario, dict) else 24}
    if prepared["status"] != "ready":
        evidence["limitation"] = prepared["errors"] or prepared["limitation"]
        return summarize_session(evidence)
    from playwright.sync_api import sync_playwright
    started = time.monotonic()
    profile = PROFILES[scenario.get("profile", "new")]
    limit = scenario.get("max_actions", profile["max_actions"])
    visited = set()
    artifact_directory = artifact_path(scenario["artifact_directory"]) if scenario.get("artifact_directory") else None
    artifact_prefix = "ore-first-contact-" + uuid.uuid4().hex
    artifact_files = []
    if artifact_directory:
        try:
            artifact_directory.mkdir(parents=True, exist_ok=True)
            cleanup_artifacts(artifact_directory)
        except OSError as error:
            evidence["limitation"] = f"Artifact storage unavailable: {type(error).__name__}"
            return summarize_session(evidence)
    def capture(page):
        if not artifact_directory or not scenario.get("capture_screenshots") or len(artifact_files) >= 30:
            return None
        name = f"{artifact_prefix}-{len(artifact_files):02d}.png"
        # Mask all inputs, not just passwords. Other page text remains operator-trusted synthetic data.
        page.screenshot(path=str(artifact_directory / name), full_page=False,
                        mask=[page.locator("input, textarea, [contenteditable=true]")], mask_color="#000000")
        artifact_files.append(name)
        return name
    try:
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(headless=True)
            context = browser.new_context(viewport=dict(zip(("width", "height"), profile["viewport"])), service_workers="block")
            # Block all off-origin traffic, including redirects, before navigating.
            def route_request(route):
                if request_allowed(scenario["url"], route.request.url, route.request.method):
                    route.continue_()
                else:
                    route.abort()
            context.route("**/*", route_request)
            if not hasattr(context, "route_web_socket"):
                raise RuntimeError("Playwright with WebSocket routing is required for isolated exploration")
            context.route_web_socket("**/*", lambda socket: socket.close())
            page = context.new_page()
            page.on("popup", lambda popup: popup.close())
            page.set_default_timeout(3000)
            page.goto(scenario["url"], wait_until="domcontentloaded")
            evidence["actions"].append({"action": "open", "observed": "local application opened"})
            screenshot = capture(page)
            if screenshot:
                evidence["actions"][-1]["screenshot"] = screenshot
            evidence["outcome"] = "abandoned"
            for _ in range(limit):
                if time.monotonic() - started > scenario.get("timeout_seconds", 30):
                    evidence["findings"].append({"observed": "time budget exhausted"})
                    break
                body = page.locator("body").inner_text()[:8000]
                if success_visible and success_visible in body:
                    evidence.update(outcome="completed", goal_observed=True)
                    break
                # Accessible roles provide discovered handles; none are supplied by the scenario.
                elements = []
                for role in ("button", "link", "textbox"):
                    for index, locator in enumerate(page.get_by_role(role).all()):
                        if not locator.is_visible():
                            continue
                        name = locator.get_attribute("aria-label") or locator.inner_text() or locator.get_attribute("placeholder") or ""
                        if role == "textbox" and not name:
                            name = locator.evaluate("el => el.labels?.[0]?.innerText || ''")
                        elements.append({"role": role, "name": name.strip(), "index": index})
                choice = choose_action(elements, scenario["goal"], visited)
                if not choice:
                    evidence["findings"].append({"observed": "no unvisited permitted visible action", "interpretation": "goal may be difficult to discover"})
                    break
                visited.add((choice["role"], choice["name"]))
                target = page.get_by_role(choice["role"]).nth(choice["index"])
                try:
                    if choice["role"] == "textbox":
                        data = scenario.get("synthetic_fields", {}).get(choice["name"])
                        if data is None:
                            continue
                        target.fill(str(data))
                        action = "fill synthetic field"
                    else:
                        target.click()
                        action = "click"
                    evidence["actions"].append({"action": action, "role": choice["role"], "name": choice["name"], "observed": redact(page.locator("body").inner_text()[:2000])})
                    screenshot = capture(page)
                    if screenshot:
                        evidence["actions"][-1]["screenshot"] = screenshot
                except Exception as error:
                    evidence["actions"].append({"action": "failed", "name": choice["name"], "error": type(error).__name__})
                    evidence["findings"].append({"observed": "interaction failed; exploration continued within budget"})
                page.wait_for_timeout(profile["delay_ms"])
            # Check final action too, without feeding the evaluator criterion to exploration.
            if success_visible and success_visible in page.locator("body").inner_text():
                evidence.update(outcome="completed", goal_observed=True)
            browser.close()
    except Exception as error:
        evidence["limitation"] = f"Browser unavailable or execution failed: {type(error).__name__}"
        evidence["outcome"] = "blocked"
    evidence["elapsed_seconds"] = round(time.monotonic() - started, 3)
    result = summarize_session(evidence)
    if artifact_directory:
        result.update(artifact_prefix=artifact_prefix, artifact_files=artifact_files,
                      expires_at_epoch=time.time() + result["retention_hours"] * 3600)
        manifest = artifact_directory / (artifact_prefix + ".json")
        try:
            manifest.write_text(json.dumps(redact(result), indent=2), encoding="utf-8")
            result["evidence_manifest"] = str(manifest)
        except OSError as error:
            result["limitation"] = f"Artifact manifest could not be saved: {type(error).__name__}"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "prepare", "summary", "run", "demo", "cleanup"])
    parser.add_argument("file", nargs="?")
    parser.add_argument("--success-visible", help="Independent evaluator criterion; never given to action selection")
    parser.add_argument("--artifact-directory", help="Demo screenshot exports; explicitly synthetic fixture only")
    args = parser.parse_args()
    if args.command == "cleanup":
        if not args.file:
            parser.error("artifact directory is required")
        result = {"removed": cleanup_artifacts(args.file)}
    elif args.command == "demo":
        fixture = Path(__file__).resolve().parents[3] / "evals" / "fixtures" / "first-contact"
        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(fixture))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = run_session({"url": f"http://127.0.0.1:{server.server_port}", "goal": "Find support and open the help page",
                                  "environment": "isolated_test", "isolated_environment_confirmed": True,
                                  "synthetic_accounts_confirmed": True, "authorized": True,
                                  **({"artifact_directory": args.artifact_directory, "capture_screenshots": True,
                                      "synthetic_screen_capture_confirmed": True} if args.artifact_directory else {})}, "Support available")
        finally:
            server.shutdown()
            server.server_close()
    else:
        if not args.file:
            parser.error("file is required")
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        result = {"errors": validate_scenario(data)} if args.command == "validate" else prepare_session(data) if args.command == "prepare" else summarize_session(data) if args.command == "summary" else run_session(data, args.success_visible)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
