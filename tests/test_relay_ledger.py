from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.relay_ledger import (
    RelayLedger,
    RelayRoundSummary,
    LedgerStep,
    all_step_ids,
    is_valid_step_id,
    stop_reason_valid,
)
from scripts.relay_constants import STOP_MAX_ROUNDS


class RelayLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "relay.jsonl"
        self.session_id = "n1-ledger-test"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_record_step_appends_jsonl(self) -> None:
        ledger = RelayLedger(self.log_path, self.session_id)
        step = ledger.record_step(
            round=1,
            step_id="1_locate_conversation",
            status="ok",
            detail="found tab",
        )
        self.assertEqual(step.round, 1)
        self.assertEqual(step.status, "ok")

        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        parsed = json.loads(lines[0])
        self.assertEqual(parsed["event"], "relay_step")
        self.assertEqual(parsed["session_id"], self.session_id)

    def test_record_step_with_error(self) -> None:
        ledger = RelayLedger(self.log_path, self.session_id)
        step = ledger.record_step(
            round=2,
            step_id="9_send_message",
            status="error",
            error="send button not found",
        )
        self.assertEqual(step.status, "error")
        self.assertIsNotNone(step.error)

    def test_write_round_summary(self) -> None:
        ledger = RelayLedger(self.log_path, self.session_id)
        summary = RelayRoundSummary(
            round=1,
            envelope="env-abc",
            stop_reason=None,
            steps_completed=14,
            errors=0,
        )
        ledger.write_round_summary(summary)

        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        parsed = json.loads(lines[0])
        self.assertEqual(parsed["event"], "relay_round_summary")
        self.assertEqual(parsed["round"], 1)

    def test_multiple_rounds_in_same_ledger(self) -> None:
        ledger = RelayLedger(self.log_path, self.session_id)
        ledger.record_step(round=1, step_id="1_locate_conversation", status="ok")
        ledger.record_step(round=1, step_id="2_capture_url", status="ok")
        ledger.write_round_summary(
            RelayRoundSummary(round=1, stop_reason=STOP_MAX_ROUNDS, steps_completed=2)
        )
        ledger.record_step(round=2, step_id="1_locate_conversation", status="ok")

        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 4)

        events = [json.loads(line)["event"] for line in lines]
        self.assertEqual(
            events,
            ["relay_step", "relay_step", "relay_round_summary", "relay_step"],
        )

    def test_ledger_creates_parent_directory(self) -> None:
        deep_path = Path(self.temp_dir.name) / "sub" / "deep" / "relay.jsonl"
        ledger = RelayLedger(deep_path, self.session_id)
        ledger.record_step(round=1, step_id="1_locate_conversation", status="ok")
        self.assertTrue(deep_path.exists())

    def test_step_to_dict_excludes_empty_fields(self) -> None:
        step = LedgerStep(round=1, step_id="1_locate_conversation", status="ok")
        d = step.to_dict()
        self.assertNotIn("error", d)
        self.assertNotIn("duration_ms", d)

    def test_all_fourteen_step_ids_valid(self) -> None:
        for step_id in all_step_ids():
            self.assertTrue(is_valid_step_id(step_id), f"{step_id!r} should be valid")


class RelayRoundSummaryTests(unittest.TestCase):
    def test_summary_to_dict(self) -> None:
        summary = RelayRoundSummary(
            round=3,
            envelope="env-xyz",
            stop_reason=STOP_MAX_ROUNDS,
            steps_completed=10,
            errors=2,
        )
        d = summary.to_dict()
        self.assertEqual(d["round"], 3)
        self.assertEqual(d["stop_reason"], STOP_MAX_ROUNDS)
        self.assertEqual(d["steps_completed"], 10)
        self.assertEqual(d["errors"], 2)


if __name__ == "__main__":
    unittest.main()
