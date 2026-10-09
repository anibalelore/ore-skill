import importlib.util
from pathlib import Path
import unittest
import functools
import threading
import tempfile
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "skills" / "ore" / "scripts" / "ore_first_contact.py"
spec = importlib.util.spec_from_file_location("ore_first_contact", SCRIPT)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


class FirstContactTests(unittest.TestCase):
    def scenario(self, **changes):
        data = dict(url="http://127.0.0.1:8080", goal="Find support", environment="isolated_test",
                    isolated_environment_confirmed=True, synthetic_accounts_confirmed=True, authorized=True)
        data.update(changes)
        return data

    def test_only_explicit_isolated_loopback(self):
        self.assertEqual(fc.validate_scenario(self.scenario()), [])
        for changes in ({"url": "https://production.example.com"}, {"environment": "production"},
                        {"synthetic_accounts_confirmed": False}, {"url": "http://127.0.0.1.evil.test"},
                        {"url": "http://user:secret@localhost"}, {"authorized": False}, {"url": None}):
            with self.subTest(changes=changes):
                self.assertTrue(fc.validate_scenario(self.scenario(**changes)))

    def test_no_implementation_answers(self):
        for field in ("selectors", "source", "steps", "routes", "answers"):
            self.assertTrue(fc.validate_scenario(self.scenario(**{field: []})))

    def test_budgets_and_profiles(self):
        self.assertTrue(fc.validate_scenario(self.scenario(max_actions=999)))
        self.assertTrue(fc.validate_scenario(self.scenario(retention_hours=25)))
        self.assertTrue(fc.validate_scenario(self.scenario(profile="stereotype")))
        self.assertTrue(fc.validate_scenario(self.scenario(max_actions=True)))

    def test_missing_browser_has_no_fake_attempts(self):
        with patch.object(fc.importlib.util, "find_spec", return_value=None):
            prepared = fc.prepare_session(self.scenario())
            result = fc.run_session(self.scenario(), "Support available")
        self.assertEqual(prepared["status"], "blocked")
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["attempts"], 0)
        self.assertFalse(result["goal_verified"])

    def test_observed_and_imported_evidence(self):
        for provenance in ("playwright", "imported_observation"):
            result = fc.summarize_session(dict(provenance=provenance, outcome="completed", goal_observed=True,
                                               actions=[{"action": "click", "observed": "Support available"}]))
            self.assertTrue(result["goal_verified"])
        result = fc.summarize_session(dict(provenance="invented", outcome="completed", goal_observed=True,
                                          actions=[{"action": "click"}]))
        self.assertFalse(result["goal_verified"])

    def test_failed_recovery_is_not_success(self):
        result = fc.summarize_session(dict(provenance="playwright", outcome="abandoned", goal_observed=False,
                                          actions=[{"action": "failed"}, {"action": "retry", "observed": "Still unavailable"}]))
        self.assertEqual(result["status"], "unverified")
        self.assertFalse(result["goal_verified"])
        self.assertFalse(fc.summarize_session(dict(provenance="playwright", outcome="completed", goal_observed=True, actions=[]))["goal_verified"])

    def test_sensitive_fields_are_redacted(self):
        result = fc.redact({"password": "hidden", "authorization": "bearer abc", "observed": "alice@example.com token=abc 4111111111111111"})
        self.assertNotIn("hidden", str(result))
        self.assertNotIn("alice@", str(result))
        self.assertNotIn("abc", str(result))
        self.assertNotIn("4111111111111111", str(result))

    def test_visible_action_selection_has_no_source(self):
        elements = [{"role": "button", "name": "Buy now"}, {"role": "link", "name": "Support"}, {"role": "link", "name": "About"}]
        self.assertEqual(fc.choose_action(elements, "Find support", set())["name"], "Support")
        self.assertEqual(fc.choose_action(elements, "Find support", {("link", "Support")})["name"], "About")

    def test_ancient_or_malformed_import_is_not_verified(self):
        self.assertFalse(fc.summarize_session({})["goal_verified"])
        with self.assertRaises(ValueError):
            fc.summarize_session({"actions": ["fake"]})

    def test_malformed_and_unknown_contract(self):
        self.assertEqual(fc.run_session([], "done")["attempts"], 0)
        self.assertTrue(fc.validate_scenario(self.scenario(internal_url="hint")))
        self.assertEqual(fc.summarize_session({"retention_hours": "forever"})["retention_hours"], 24)

    def test_network_policy_rejects_redirects_mutations_and_other_ports(self):
        start = "http://127.0.0.1:8080"
        self.assertTrue(fc.request_allowed(start, start + "/help", "GET"))
        for target, method in ((start + "/pay", "POST"), ("https://example.com", "GET"),
                               ("http://127.0.0.1:8081", "GET"), ("http://localhost:8080", "GET"),
                               ("ws://127.0.0.1:8080", "GET")):
            self.assertFalse(fc.request_allowed(start, target, method))

    def test_screenshot_consent_and_ore_path_rejection(self):
        self.assertTrue(fc.validate_scenario(self.scenario(capture_screenshots=True)))
        self.assertTrue(fc.validate_scenario(self.scenario(artifact_directory=".ore/replays")))
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(fc.validate_scenario(self.scenario(artifact_directory=directory, capture_screenshots=True,
                                                                synthetic_screen_capture_confirmed=True)), [])

    def test_scoped_expiry_cleanup_preserves_unrelated_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prefix = "ore-first-contact-" + "a" * 32
            screenshot = root / (prefix + "-00.png")
            screenshot.write_bytes(b"expired synthetic image")
            unrelated = root / "keep.png"
            unrelated.write_bytes(b"keep")
            manifest = root / (prefix + ".json")
            manifest.write_text(json.dumps(dict(artifact_prefix=prefix, expires_at_epoch=1,
                                                artifact_files=[screenshot.name, "keep.png", "../escape.png"])))
            removed = fc.cleanup_artifacts(directory, current_time=2)
            self.assertEqual(len(removed), 2)
            self.assertTrue(unrelated.exists())
            self.assertFalse(screenshot.exists())

    def test_cleanup_keeps_unexpired_and_invalid_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = "ore-first-contact-" + "b" * 32
            manifest = Path(directory) / (prefix + ".json")
            manifest.write_text(json.dumps(dict(artifact_prefix=prefix, expires_at_epoch=100, artifact_files=[])))
            self.assertEqual(fc.cleanup_artifacts(directory, current_time=2), [])
            self.assertTrue(manifest.exists())
            manifest.write_text("corrupt")
            self.assertEqual(fc.cleanup_artifacts(directory, current_time=200), [])

    def test_real_local_black_box_exploration(self):
        self.assertIsNotNone(importlib.util.find_spec("playwright"),
                             'Required Playwright missing: pip install -r requirements.txt; python -m playwright install chromium')
        fixtures = Path(__file__).parent / "fixtures" / "first-contact"
        server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(SimpleHTTPRequestHandler, directory=str(fixtures)))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                result = fc.run_session(self.scenario(url=f"http://127.0.0.1:{server.server_port}", artifact_directory=directory,
                                                      capture_screenshots=True, synthetic_screen_capture_confirmed=True), "Support available")
                self.assertNotEqual(result['status'], 'blocked', result.get('limitation'))
                self.assertTrue(result["goal_verified"])
                self.assertEqual(result["actions"][1]["name"], "Support")
                self.assertEqual(len(result["artifact_files"]), 2)
                self.assertTrue(Path(result["evidence_manifest"]).is_file())
                for name in result["artifact_files"]:
                    self.assertEqual((Path(directory) / name).read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
