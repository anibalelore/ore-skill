"""Synthetic acceptance tests: no production app or real payment is exercised."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/ore/scripts/ore_flow.py"
spec = importlib.util.spec_from_file_location("ore_flow", SCRIPT)
flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)


class FlowTests(unittest.TestCase):
    def fixture(self, name="factory"):
        return json.loads((ROOT / f"evals/fixtures/flows/{name}.json").read_text(encoding="utf-8"))

    def codes(self, document):
        return {item["code"] for item in flow.analyze_flow(document)["findings"]}

    def test_factory_existing_customer_two_products_partial_batches_and_shipping(self):
        doc = self.fixture()
        self.assertEqual(doc["entities"][1]["fields"]["products"]["value"], ["juice", "water"])
        doc["quantity_balances"] = [{"id": "juice", "ordered": 120, "produced": 90, "rejected": 20, "packaged": 65, "shipped": 40, "evidence": ["synthetic:counts"]}]
        self.assertTrue(flow.analyze_flow(doc)["continuity_verified"])
        doc["quantity_balances"][0]["shipped"] = 80
        self.assertIn("quantity_integrity", self.codes(doc))

    def test_marketplace_multivendor_payment_relations(self):
        doc = self.fixture("marketplace")
        self.assertTrue(flow.analyze_flow(doc)["continuity_verified"])
        relation = next(x for x in doc["relationships"] if x["id"] == "payment-sellers")
        self.assertEqual(len(relation["pairs"]), 2)
        self.assertEqual(relation["cardinality"], "many-to-many")

    def test_creation_retry_is_idempotent_and_duplicate_side_effect_fails(self):
        doc = self.fixture()
        self.assertNotIn("duplicate_side_effect", self.codes(doc))
        doc["executions"][-2]["side_effect_count"] = 1
        self.assertIn("duplicate_side_effect", self.codes(doc))

    def test_corrected_quantity_requires_versioned_propagation_or_snapshot(self):
        doc = self.fixture()
        doc["entities"][1]["fields"]["quantity"].update(value=100, version=2)
        self.assertIn("stale_field", self.codes(doc))
        doc["entities"][2]["fields"]["quantity"].update(value=100, version=2)
        self.assertNotIn("stale_field", self.codes(doc))
        doc["entities"][2]["fields"]["quantity"].update(value=120, version=1, mode="snapshot", reason="accepted commercial terms")
        self.assertNotIn("stale_field", self.codes(doc))

    def test_quality_restriction_and_permissions_block_verified_completion(self):
        doc = self.fixture()
        doc["executions"][5]["preconditions"] = []
        doc["executions"][5]["permissions"] = []
        self.assertIn("missing_preconditions", self.codes(doc))
        self.assertIn("missing_permissions", self.codes(doc))
        self.assertFalse(flow.analyze_flow(doc)["continuity_verified"])

    def test_logistics_failure_detected_and_idempotent_recovery(self):
        doc = self.fixture()
        execution = next(x for x in doc["executions"] if x["transition"] == "dispatch")
        execution.update(status="failed", side_effect_count=0)
        self.assertIn("missing_transition", self.codes(doc))
        recovered = copy.deepcopy(execution)
        recovered.update(id="dispatch-recovery", status="succeeded", at="2026-01-01T01:00:00Z", side_effect_count=1)
        doc["executions"].append(recovered)
        self.assertTrue(flow.analyze_flow(doc)["continuity_verified"])
        retry = copy.deepcopy(recovered)
        retry.update(id="dispatch-recovery-retry", status="duplicate", side_effect_count=0)
        doc["executions"].append(retry)
        self.assertTrue(flow.analyze_flow(doc)["continuity_verified"])

    def test_unverified_inferred_contradictory_links_cannot_pass(self):
        for status in ("inferred", "unverified", "contradictory"):
            doc = self.fixture()
            doc["relationships"][0]["status"] = status
            self.assertFalse(flow.analyze_flow(doc)["continuity_verified"])

    def test_identity_cardinality_and_orphaned_provenance(self):
        doc = self.fixture()
        doc["entities"].append(copy.deepcopy(doc["entities"][0]))
        self.assertTrue(flow.validate_flow(doc))
        doc = self.fixture()
        doc["relationships"][4]["cardinality"] = "one-to-one"
        self.assertTrue(flow.validate_flow(doc))
        doc = self.fixture()
        doc["entities"][2]["fields"]["quantity"]["source"] = "missing.quantity"
        self.assertTrue(flow.validate_flow(doc))

    def test_marketplace_cancel_refund_out_of_order_and_settlement_dispute(self):
        doc = self.fixture("marketplace")
        refund = next(x for x in doc["transitions"] if x["id"] == "refund")
        doc["executions"].append({"id": "refund-ok", "transition": refund["id"], "status": "succeeded", "at": "2026-01-02T00:00:00Z", "idempotency_key": "refund-1", "preconditions": ["refund_approved"], "permissions": ["operate"], "evidence": ["synthetic:refund"], "side_effect_count": 1})
        self.assertTrue(flow.analyze_flow(doc)["continuity_verified"])
        settlement = next(x for x in doc["executions"] if x["transition"] == "settle")
        settlement["preconditions"].remove("no_dispute")
        self.assertIn("missing_preconditions", self.codes(doc))
        settlement["from_state"] = "cancelled"
        self.assertIn("out_of_order_transition", self.codes(doc))

    def test_watch_sla_dedup_unknown_cause_and_no_telemetry(self):
        doc = self.fixture()
        self.assertEqual(flow.watch_flow(doc)["status"], "no_telemetry")
        observation = {"entity": "shipping-1", "kind": "stuck", "last_transition": "ship-partial", "last_transition_at": "2026-01-01T00:00:00Z", "sla_seconds": 60, "evidence": ["synthetic:log"], "cause": "network failure"}
        doc["telemetry"] = {"connection": "connected", "observations": [observation, copy.deepcopy(observation)]}
        result = flow.watch_flow(doc, "2026-01-01T01:00:00Z")
        self.assertEqual(len(result["alerts"]), 1)
        self.assertEqual(result["alerts"][0]["elapsed_seconds"], 3600)
        self.assertEqual(result["alerts"][0]["possible_cause"], "unknown")
        self.assertFalse(result["alerts"][0]["repair_executed"])
        observation["cause_evidence"] = ["synthetic:network-trace"]
        self.assertEqual(flow.watch_flow(doc, "2026-01-01T01:00:00Z")["alerts"][0]["possible_cause"], "network failure")

    def test_read_only_determinism_invalid_inputs_and_cli(self):
        doc = self.fixture()
        before = copy.deepcopy(doc)
        self.assertEqual(flow.analyze_flow(doc), flow.analyze_flow(doc))
        flow.watch_flow(doc)
        self.assertEqual(doc, before)
        for value in (None, [], {}, {"schema_version": 1, "id": "bad", "entities": "invalid"}):
            self.assertFalse(flow.analyze_flow(value)["valid"])
        result = subprocess.run([sys.executable, str(SCRIPT), "analyze", str(ROOT / "evals/fixtures/flows/factory.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["continuity_verified"])


if __name__ == "__main__":
    unittest.main()
