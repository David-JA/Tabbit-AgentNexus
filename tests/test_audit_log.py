from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_log import append_event, write_session_summary


class AuditLogTests(unittest.TestCase):
    def test_append_event_writes_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"
            payload = append_event(log_path, "n1-test", "context_pack_built", bytes_total=12)
            self.assertEqual(payload["session_id"], "n1-test")
            lines = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            parsed = json.loads(lines[0])
            self.assertEqual(parsed["bytes_total"], 12)

    def test_write_session_summary_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            summary_path = Path(temp_dir) / "session_summary.json"
            write_session_summary(summary_path, {"status": "ok", "selected_file_count": 2})
            parsed = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(parsed["status"], "ok")
            self.assertEqual(parsed["selected_file_count"], 2)


if __name__ == "__main__":
    unittest.main()
