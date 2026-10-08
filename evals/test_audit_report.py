"""Evidence and stopping invariants for the optional audit ledger."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "ore" / "scripts" / "validate_audit_report.py"
spec = importlib.util.spec_from_file_location("audit_report", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def ledger():
    return {
        "project": "Synthetic tenant API", "date": "2026-10-08 America/Denver",
        "scope": "Local synthetic API only; legal and live infrastructure not evaluated",
        "revision": "fixture-v2", "mode": "security", "iteration": 1,
        "stop_reason": "Scoped finding retested", "next_action": "Report uncovered database and legal checks",
        "controls": [{"id": "ADV-03", "status": "passed", "evidence": "Positive and cross-tenant negative tests"}],
        "tests": [
            {"id": "tenant-denial", "status": "passed", "revision": "fixture-v2", "evidence": "Tenant A cannot read B"},
            {"id": "tenant-sharing", "status": "passed", "revision": "fixture-v2", "evidence": "Allowed colleague can read A"},
        ],
        "findings": [{
            "id": "F-001", "controls": ["ADV-03"], "severity": "P1", "status": "resolved",
            "component": "Synthetic order handler", "evidence": "Baseline returned a foreign synthetic order",
            "risk": "Horizontal unauthorized access", "preconditions": "Authenticated unrelated tenant member",
            "impact": "Foreign order disclosure", "correction": "Enforce server membership before read",
            "side_effects": "Preserve authorized colleague sharing",
            "validation": {"retest": ["tenant-denial"], "regression": ["tenant-sharing"]},
        }],
    }


class AuditReportTests(unittest.TestCase):
    def test_current_retest_and_regression_allow_resolution(self):
        self.assertEqual(audit.validate_report(ledger()), [])

    def test_edit_alone_does_not_resolve(self):
        report = ledger()
        report["findings"][0]["validation"] = {"retest": [], "regression": []}
        self.assertTrue(audit.validate_report(report))
        report["findings"][0]["status"] = "fixed_unvalidated"
        report["controls"][0]["status"] = "failed"
        self.assertEqual(audit.validate_report(report), [])

    def test_failed_skipped_and_stale_tests_cannot_close(self):
        for key, value in (("status", "failed"), ("status", "not_run"), ("revision", "fixture-v1")):
            with self.subTest(key=key, value=value):
                report = ledger()
                report["tests"][0][key] = value
                self.assertTrue(audit.validate_report(report))

    def test_iteration_limit_including_bool(self):
        for value in (-1, 6, True, "5"):
            report = ledger()
            report["iteration"] = value
            self.assertTrue(audit.validate_report(report))
        for value in (0, 5):
            report = ledger()
            report["iteration"] = value
            self.assertEqual(audit.validate_report(report), [])

    def test_integral_coverage_requires_all_controls_and_reasons(self):
        report = ledger()
        report["mode"] = "audit"
        self.assertTrue(audit.validate_report(report))
        report["controls"] += [
            {"id": cid, "status": "not_evaluated", "evidence": "No authorized runtime evidence"}
            for cid in sorted(audit.CONTROL_IDS - {"ADV-03"})
        ]
        self.assertEqual(audit.validate_report(report), [])
        report["controls"][1]["evidence"] = ""
        self.assertTrue(audit.validate_report(report))

    def test_risk_acceptance_is_not_a_pass(self):
        report = ledger()
        finding = report["findings"][0]
        finding["status"] = "accepted_risk"
        self.assertTrue(audit.validate_report(report))
        finding["acceptance"] = {"owner": "Synthetic owner", "rationale": "Test exception", "scope": "Fixture only", "expires": "2026-10-09"}
        self.assertTrue(audit.validate_report(report))
        report["controls"][0]["status"] = "failed"
        self.assertEqual(audit.validate_report(report), [])

    def test_unknown_duplicate_and_malformed_links_fail(self):
        cases = []
        report = ledger()
        report["tests"].append(copy.deepcopy(report["tests"][0]))
        cases.append(report)
        report = ledger()
        report["findings"][0]["validation"]["retest"] = ["missing"]
        cases.append(report)
        report = ledger()
        report["controls"][0]["id"] = "ADV-99"
        cases.append(report)
        report = ledger()
        report["findings"][0]["controls"] = [{}]
        cases.append(report)
        for report in cases:
            self.assertTrue(audit.validate_report(report))
        self.assertTrue(audit.validate_report([]))

    def test_cli_accepts_valid_and_rejects_invalid_without_echoing_input(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ledger.json"
            path.write_text(json.dumps(ledger()), encoding="utf-8")
            good = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            path.write_text('{"synthetic-secret": invalid}', encoding="utf-8")
            bad = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertNotIn("synthetic-secret", bad.stderr)

    def test_malformed_enum_values_are_rejected_without_crashing(self):
        for value in ({}, [], None, True):
            for record, key in (("report", "mode"), ("controls", "status"), ("tests", "status"), ("findings", "severity"), ("findings", "status")):
                with self.subTest(value=value, record=record, key=key):
                    report = ledger()
                    target = report if record == "report" else report[record][0]
                    target[key] = value
                    self.assertTrue(audit.validate_report(report))

    def test_synthetic_tenant_audit_repair_and_reaudit(self):
        # Standalone authorized local case: demonstrates evidence provenance, not a real app audit.
        orders = {"order-a": {"tenant": "A", "value": "synthetic-a"}, "order-b": {"tenant": "B", "value": "synthetic-b"}}
        memberships = {"alice": {"A"}, "colleague": {"A"}, "bob": {"B"}}

        def baseline(user, order_id):
            return orders.get(order_id)

        self.assertEqual(baseline("alice", "order-b")["tenant"], "B")

        def repaired(user, order_id):
            order = orders.get(order_id)
            if order is None or order["tenant"] not in memberships.get(user, set()):
                return None
            return order

        for user, foreign in (("alice", "order-b"), ("bob", "order-a"), ("anonymous", "order-a")):
            self.assertIsNone(repaired(user, foreign))
        self.assertEqual(repaired("alice", "order-a")["value"], "synthetic-a")
        self.assertEqual(repaired("colleague", "order-a")["value"], "synthetic-a")
        self.assertEqual(audit.validate_report(ledger()), [])


if __name__ == "__main__":
    unittest.main()
