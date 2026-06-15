from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.relay_runner import prepare_relay_handoff
from scripts.relay_constants import DIRECTION_REPO_TO_WEB, COMPLETENESS_UNKNOWN


class RelayRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_context_pack(self, content: str, suffix: str = "") -> Path:
        path = Path(self.temp_dir.name) / f"context_pack{suffix}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_prepare_handoff_creates_valid_envelope(self) -> None:
        pack_path = self._write_context_pack("# Context Pack\n\nTest content.")
        result = prepare_relay_handoff(
            session_id="n1-runner-test",
            context_pack_path=pack_path,
            round_number=1,
            target_url="https://chat.example.com/c/abc",
        )
        env = result["envelope"]
        self.assertEqual(env["session_id"], "n1-runner-test")
        self.assertEqual(env["round"], 1)
        self.assertEqual(env["direction"], DIRECTION_REPO_TO_WEB)
        self.assertEqual(env["payload_role"], "context_pack")
        self.assertTrue(env["untrusted_data"])

    def test_prepare_handoff_missing_file_raises(self) -> None:
        missing = Path(self.temp_dir.name) / "nonexistent.md"
        with self.assertRaises(FileNotFoundError):
            prepare_relay_handoff(
                session_id="n1-test",
                context_pack_path=missing,
            )

    def test_prepare_handoff_template_vars_present(self) -> None:
        pack_path = self._write_context_pack("payload")
        result = prepare_relay_handoff(
            session_id="n1-test",
            context_pack_path=pack_path,
            round_number=3,
            redaction_count=5,
        )
        tv = result["template_vars"]
        self.assertEqual(tv["session_id"], "n1-test")
        self.assertEqual(tv["round"], 3)
        self.assertEqual(tv["redaction_count"], 5)
        self.assertIn("payload", tv)
        self.assertIn("envelope_id", tv)

    def test_envelope_payload_digest_is_sha256(self) -> None:
        pack_path = self._write_context_pack("consistent payload")
        result = prepare_relay_handoff(
            session_id="n1-test",
            context_pack_path=pack_path,
        )
        digest = result["envelope"]["payload_digest"]
        self.assertEqual(len(digest), 64)  # SHA-256 hex

    def test_different_payloads_different_digests(self) -> None:
        path_a = self._write_context_pack("payload A", suffix="_a")
        path_b = self._write_context_pack("payload B", suffix="_b")
        result_a = prepare_relay_handoff(session_id="n1", context_pack_path=path_a)
        result_b = prepare_relay_handoff(session_id="n1", context_pack_path=path_b)
        self.assertNotEqual(
            result_a["envelope"]["payload_digest"],
            result_b["envelope"]["payload_digest"],
        )


if __name__ == "__main__":
    unittest.main()
