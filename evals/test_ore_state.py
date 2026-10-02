import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "ore" / "scripts" / "ore_state.py"


class OreStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *args, "--repo", self.repo], text=True, capture_output=True)
        if ok and result.returncode:
            self.fail(result.stderr)
        return result

    def start(self):
        return self.run_cli(
            "start", "--title", "Fixture", "--objective", "Verify persistence",
            "--kind", "general",
            "--acceptance", "State resumes with the same verified progress",
            "--deliverable", "Baseline:20", "--deliverable", "Build:50", "--deliverable", "Verify:30",
            "--gate", "TESTS",
        )

    def test_resume_and_computed_progress(self):
        started = json.loads(self.start().stdout)
        result = self.run_cli(
            "update", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]),
            "--deliverable", "Baseline=done", "--evidence", "Baseline:repo inspected",
        )
        updated = json.loads(result.stdout)
        self.assertEqual(updated["progress"], 20)
        resumed = json.loads(self.run_cli("resume").stdout)
        self.assertEqual(resumed["task_id"], updated["task_id"])
        self.assertTrue((Path(self.repo) / ".ore" / "handoffs" / f"{updated['task_id']}.md").exists())

    def test_rejects_stale_window_update(self):
        started = json.loads(self.start().stdout)
        self.run_cli("checkpoint", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]), "--next", "Continue")
        conflict = self.run_cli(
            "update", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]), "--deliverable", "Baseline=done", ok=False
        )
        self.assertEqual(conflict.returncode, 2)
        self.assertIn("Revision conflict", conflict.stderr)

    def test_cannot_complete_with_open_work_or_gates(self):
        started = json.loads(self.start().stdout)
        result = self.run_cli("complete", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]), ok=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot complete", result.stderr)

    def test_weights_must_total_100(self):
        result = self.run_cli(
            "start", "--title", "Bad", "--objective", "Bad plan", "--kind", "general", "--acceptance", "Valid weights",
            "--deliverable", "Only:90", ok=False
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("total exactly 100", result.stderr)

    def test_progress_and_gate_closure_require_evidence(self):
        started = json.loads(self.start().stdout)
        progress = self.run_cli(
            "update", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]), "--deliverable", "Baseline=done", ok=False
        )
        self.assertIn("requires --evidence", progress.stderr)
        gate = self.run_cli(
            "update", "--task-id", started["task_id"], "--expect-revision", str(started["revision"]), "--gate", "TESTS=passed", ok=False
        )
        self.assertIn("requires evidence", gate.stderr)

    def test_successful_completion_requires_all_evidence(self):
        state = json.loads(self.start().stdout)
        state = json.loads(self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--deliverable", "Baseline=done", "--deliverable", "Build=done", "--deliverable", "Verify=done",
            "--evidence", "Baseline:inspected", "--evidence", "Build:implemented", "--evidence", "Verify:tests passed",
            "--gate", "SPEC_FIDELITY=passed", "--gate", "FORM_INTELLIGENCE=not_applicable", "--gate", "HANDOFF=passed", "--gate", "TESTS=passed",
            "--evidence", "SPEC_FIDELITY:criteria matched", "--evidence", "FORM_INTELLIGENCE:no material form in scope", "--evidence", "HANDOFF:handoff written", "--evidence", "TESTS:suite passed",
        ).stdout)
        self.assertEqual(state["progress"], 100)
        completed = json.loads(self.run_cli("complete", "--task-id", state["task_id"], "--expect-revision", str(state["revision"])).stdout)
        self.assertEqual(completed["status"], "complete")

    def test_rejects_unsafe_task_id(self):
        result = self.run_cli(
            "start", "--task-id", "../escaped", "--title", "Bad", "--objective", "Escape", "--kind", "general",
            "--acceptance", "Must not escape", "--deliverable", "Only:100", ok=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Task id must match", result.stderr)
        self.assertFalse((Path(self.repo) / ".ore" / "escaped.json").exists())

    def test_lists_and_resumes_named_tasks(self):
        first = json.loads(self.run_cli(
            "start", "--task-id", "task-a", "--title", "A", "--objective", "First", "--kind", "general",
            "--acceptance", "A exists", "--deliverable", "Only:100",
        ).stdout)
        self.run_cli(
            "start", "--task-id", "task-b", "--title", "B", "--objective", "Second", "--kind", "general",
            "--acceptance", "B exists", "--deliverable", "Only:100",
        )
        listed = json.loads(self.run_cli("list").stdout)
        self.assertEqual({item["id"] for item in listed["tasks"]}, {"task-a", "task-b"})
        resumed = json.loads(self.run_cli("resume", "--task-id", "task-a").stdout)
        self.assertEqual(resumed["task_id"], first["task_id"])

    def test_form_gate_requires_valid_contract(self):
        state = json.loads(self.start().stdout)
        result = self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--gate", "FORM_INTELLIGENCE=passed", "--evidence", "FORM_INTELLIGENCE:reviewed", ok=False,
        )
        self.assertIn("requires a validated --form-contract", result.stderr)

    def test_two_simultaneous_writers_cannot_both_commit(self):
        state = json.loads(self.start().stdout)
        base = [
            sys.executable, str(SCRIPT), "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--deliverable", "Baseline=done", "--evidence", "Baseline:verified", "--repo", self.repo,
        ]
        first = subprocess.Popen(base, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        second = subprocess.Popen(base, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = [first.communicate(), second.communicate()]
        codes = [first.returncode, second.returncode]
        self.assertEqual(sorted(codes), [0, 2], results)

    def test_gate_reopen_requires_fresh_evidence(self):
        state = json.loads(self.start().stdout)
        state = json.loads(self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--gate", "TESTS=passed", "--evidence", "TESTS:first run passed",
        ).stdout)
        state = json.loads(self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]), "--gate", "TESTS=failed",
        ).stdout)
        result = self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]), "--gate", "TESTS=passed", ok=False,
        )
        self.assertIn("requires evidence", result.stderr)

    def test_form_like_task_requires_form_kind(self):
        result = self.run_cli(
            "start", "--title", "Onboarding form", "--objective", "Build onboarding",
            "--kind", "general", "--acceptance", "Form works", "--deliverable", "Only:100", ok=False,
        )
        self.assertIn("--kind form", result.stderr)

    def test_mutation_requires_explicit_task_id(self):
        state = json.loads(self.start().stdout)
        result = self.run_cli(
            "update", "--expect-revision", str(state["revision"]),
            "--deliverable", "Baseline=done", "--evidence", "Baseline:verified", ok=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--task-id", result.stderr)

    def test_form_gate_records_exact_authoritative_list_proof(self):
        state = json.loads(self.run_cli(
            "start", "--task-id", "registration-form", "--title", "Registration form",
            "--objective", "Create company registration", "--kind", "form",
            "--acceptance", "Industry list remains exact", "--deliverable", "Form:100",
        ).stdout)
        expected = Path(self.repo) / "industries.json"
        expected.write_text(json.dumps(["Health", "Retail"]), encoding="utf-8")
        form_dir = Path(self.repo) / ".ore" / "forms"
        form_dir.mkdir(parents=True, exist_ok=True)
        contract = form_dir / "registration.json"
        contract.write_text(json.dumps({
            "id": "registration", "user_role": "owner", "job": "register", "canonical_entity": "Company",
            "fields": [{
                "id": "industry", "type": "enum", "required": True, "source": "user-supplied list",
                "authoritative": True, "allowed_values": ["Health", "Retail"],
                "client_validation": "membership", "server_validation": "membership",
                "error": "Choose an industry", "privacy": "non-sensitive",
            }],
            "states": ["draft", "submitted"],
            "accessibility": {"keyboard": True, "screen_reader": True, "text_scaling": True},
            "submission": {"idempotent": True},
            "test_cases": ["happy", "invalid", "server_error", "double_submit"],
        }), encoding="utf-8")
        updated = json.loads(self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--form-contract", ".ore/forms/registration.json",
            "--authoritative-list", "industry=industries.json",
            "--gate", "FORM_INTELLIGENCE=passed", "--evidence", "FORM_INTELLIGENCE:contract and exact list verified",
        ).stdout)
        self.assertEqual(updated["authoritative_lists_verified"][0]["field"], "industry")
        self.assertEqual(len(updated["authoritative_lists_verified"][0]["source_sha256"]), 64)
        self.assertEqual(len(updated["authoritative_lists_verified"][0]["contract_sha256"]), 64)

    def test_complete_rejects_form_tampering_after_gate(self):
        state = json.loads(self.run_cli(
            "start", "--task-id", "secure-form", "--title", "Secure form", "--objective", "Build form",
            "--kind", "form", "--acceptance", "Contract remains unchanged", "--deliverable", "Form:100",
        ).stdout)
        form_dir = Path(self.repo) / ".ore" / "forms"
        form_dir.mkdir(parents=True, exist_ok=True)
        contract = form_dir / "secure.json"
        value = {
            "id": "secure", "user_role": "owner", "job": "submit", "canonical_entity": "Record",
            "fields": [{
                "id": "name", "type": "text", "required": True, "source": "user",
                "client_validation": "non-empty", "server_validation": "non-empty",
                "error": "Enter a name", "privacy": "personal",
            }],
            "states": ["draft", "submitted"],
            "accessibility": {"keyboard": True, "screen_reader": True, "text_scaling": True},
            "submission": {"idempotent": True},
            "test_cases": ["happy", "invalid", "server_error", "double_submit"],
        }
        contract.write_text(json.dumps(value), encoding="utf-8")
        state = json.loads(self.run_cli(
            "update", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]),
            "--form-contract", ".ore/forms/secure.json",
            "--deliverable", "Form=done", "--evidence", "Form:implemented",
            "--gate", "FORM_INTELLIGENCE=passed", "--evidence", "FORM_INTELLIGENCE:validated",
            "--gate", "SPEC_FIDELITY=passed", "--evidence", "SPEC_FIDELITY:matched",
            "--gate", "HANDOFF=passed", "--evidence", "HANDOFF:written",
        ).stdout)
        value["fields"][0]["error"] = "Changed after approval"
        contract.write_text(json.dumps(value), encoding="utf-8")
        result = self.run_cli(
            "complete", "--task-id", state["task_id"], "--expect-revision", str(state["revision"]), ok=False,
        )
        self.assertIn("changed after gate approval", result.stderr)



if __name__ == "__main__":
    unittest.main()

