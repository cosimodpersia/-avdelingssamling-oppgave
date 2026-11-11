import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from incident_lab.model import percentile, replay, validate_config, verify


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "kilder/konfigurasjon/runtime.json"
DATASET_PATH = ROOT / "kilder/replay.json"


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG_PATH.read_text())
        self.requests = json.loads(DATASET_PATH.read_text())["requests"]

    def test_baseline_reproduces_incident(self):
        result = replay(self.config, self.requests)
        self.assertEqual(result["summary"], {
            "request_count": 40,
            "success_rate": 0.1,
            "p95_elapsed_ms": 950,
            "max_elapsed_ms": 950,
            "upstream_attempts": 112,
            "attempts_per_request": 2.8,
        })
        self.assertFalse(verify(result["summary"])["passed"])

    def test_application_logs_match_replay(self):
        rows = [json.loads(line) for line in
                (ROOT / "kilder/logger/applikasjon.jsonl").read_text().splitlines()]
        observed = {row["request_id"]: row for row in rows
                    if row["release"] == self.config["release"]}
        for row in replay(self.config, self.requests)["requests"]:
            actual = observed[row["request_id"]]
            self.assertEqual(actual["status"], row["status"])
            self.assertEqual(actual["elapsed_ms"], row["elapsed_ms"])
            self.assertEqual(actual["attempt_count"], len(row["attempts"]))

    def test_upstream_logs_match_replay(self):
        rows = [json.loads(line) for line in
                (ROOT / "kilder/logger/arkivtjeneste.jsonl").read_text().splitlines()]
        observed = {(row["trace_id"], row["attempt"]): row for row in rows}
        for row in replay(self.config, self.requests)["requests"]:
            request = next(r for r in self.requests if r["request_id"] == row["request_id"])
            for attempt in row["attempts"]:
                actual = observed[(f'{self.config["release"]}-{row["request_id"]}',
                                   attempt["attempt"])]
                self.assertEqual(actual["status"], 200)
                self.assertEqual(actual["duration_ms"], request["upstream_latency_ms"])

    def test_completion_at_timeout_succeeds(self):
        result = replay(self.config, [{"request_id": "edge", "upstream_latency_ms": 250}])
        self.assertEqual(result["requests"][0]["status"], 200)
        self.assertEqual(result["summary"]["upstream_attempts"], 1)

    def test_no_backoff_after_last_attempt(self):
        result = replay(self.config, [{"request_id": "slow", "upstream_latency_ms": 3000}])
        self.assertEqual(result["summary"]["max_elapsed_ms"], 3 * 250 + 2 * 100)

    def test_one_attempt_has_no_backoff(self):
        self.config["dependency"]["max_attempts"] = 1
        result = replay(self.config, [{"request_id": "slow", "upstream_latency_ms": 3000}])
        self.assertEqual(result["summary"]["max_elapsed_ms"], 250)

    def test_inputs_are_not_mutated(self):
        original_config = copy.deepcopy(self.config)
        original_requests = copy.deepcopy(self.requests)
        replay(self.config, self.requests)
        self.assertEqual(self.config, original_config)
        self.assertEqual(self.requests, original_requests)

    def test_nearest_rank_percentile(self):
        self.assertEqual(percentile(list(range(1, 41)), 0.95), 38)

    def test_invalid_configuration_values(self):
        for name, values in {
            "timeout_ms": [0, 2001, True, 250.5, "250", None],
            "max_attempts": [0, 6, False, 1.5],
            "retry_backoff_ms": [-1, 1001, "100"],
        }.items():
            for value in values:
                with self.subTest(name=name, value=value):
                    config = copy.deepcopy(self.config)
                    config["dependency"][name] = value
                    with self.assertRaises(ValueError):
                        validate_config(config)

    def test_missing_fields_and_wrong_shapes(self):
        for config in [[], {}, {"service": "other"},
                       {"service": "document-flow", "dependency": []},
                       {"service": "document-flow", "dependency": {}}]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                validate_config(config)

    def test_empty_dataset_rejected(self):
        with self.assertRaises(ValueError):
            replay(self.config, [])

    def test_each_slo_is_enforced(self):
        passing = {
            "success_rate": 0.99, "p95_elapsed_ms": 1200,
            "max_elapsed_ms": 2500, "attempts_per_request": 1.10,
        }
        self.assertTrue(verify(passing)["passed"])
        for name, value in {
            "success_rate": 0.98, "p95_elapsed_ms": 1201,
            "max_elapsed_ms": 2501, "attempts_per_request": 1.11,
        }.items():
            with self.subTest(name=name):
                self.assertFalse(verify({**passing, name: value})["passed"])


class CommandTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "incident_lab", *map(str, args)],
            cwd=ROOT, capture_output=True, text=True,
        )

    def test_replay_outputs_json_and_hashes(self):
        result = self.run_cli("replay", "--config", CONFIG_PATH)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["inputs"]["config_sha256"],
                         hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest())
        self.assertEqual(output["inputs"]["dataset_sha256"],
                         hashlib.sha256(DATASET_PATH.read_bytes()).hexdigest())

    def test_baseline_verification_fails_and_writes_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested/result.json"
            result = self.run_cli("verify", "--config", CONFIG_PATH, "--output", path)
            self.assertEqual(result.returncode, 1, result.stderr)
            output = json.loads(path.read_text())
            self.assertFalse(output["verification"]["passed"])
            self.assertEqual(output, json.loads(result.stdout))

    def test_successful_verification_path(self):
        with tempfile.TemporaryDirectory() as directory:
            # A tiny independent dataset tests the command without solving the exercise.
            path = Path(directory) / "fast.json"
            path.write_text(json.dumps({"requests": [
                {"request_id": "fast", "upstream_latency_ms": 100}
            ]}))
            result = self.run_cli("verify", "--config", CONFIG_PATH, "--dataset", path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["verification"]["passed"])

    def test_missing_config_is_input_error(self):
        result = self.run_cli("replay", "--config", ROOT / "missing.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Error:", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_invalid_json_is_input_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{")
            result = self.run_cli("replay", "--config", path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
