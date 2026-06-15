from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.n1_review_session import run_session


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def snapshot_files(root: Path) -> set[str]:
    return {
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.rglob("*")
        if path.is_file()
    }


class N1ReviewSessionTests(unittest.TestCase):
    def test_local_only_success_path(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
            self.assertEqual(summary["status"], "ready_to_send")
            self.assertFalse(summary["artifact_fallback_used"])
            self.assertTrue(Path(summary["artifacts"]["context_pack"]).exists())
            self.assertTrue(Path(summary["artifacts"]["audit_log"]).exists())
            self.assertTrue(Path(summary["artifacts"]["session_summary"]).exists())
            self.assertIsNone(summary["artifacts"]["review_report"])
            self.assertFalse(summary["invariants"]["browser_submission_performed"])

    def test_denied_only_repo_fails_cleanly(self) -> None:
        repo_root = FIXTURES / "m1_repo_denied_only"
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
            self.assertEqual(summary["status"], "failed")
            self.assertEqual(summary["failure_class"], "no_allowed_files")
            self.assertTrue(Path(summary["artifacts"]["audit_log"]).exists())
            self.assertTrue(Path(summary["artifacts"]["session_summary"]).exists())

    def test_secret_redaction_survives_through_summary_and_artifact(self) -> None:
        repo_root = FIXTURES / "m1_repo_with_secrets"
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
            self.assertEqual(summary["status"], "ready_to_send")
            self.assertGreater(summary["manifest"]["redaction_count"], 0)
            context_pack = Path(summary["artifacts"]["context_pack"]).read_text(encoding="utf-8")
            self.assertIn("[REDACTED_POSSIBLE_SECRET:openai_api_key]", context_pack)
            self.assertNotIn("sk-live-abcdefghijklmnopqrstuvwxyz", context_pack)

    def test_no_git_path_still_reaches_ready_to_send(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("scripts.n1_review_session.probe") as mock_probe:
                mock_probe.return_value = {
                    "repo_root": str(repo_root.resolve()),
                    "git_available": False,
                    "git_path": None,
                    "repo_is_git": False,
                    "branch": None,
                    "status_short": "",
                    "recent_commits": [],
                    "error": "git_not_found",
                }
                summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
            self.assertEqual(summary["status"], "ready_to_send")
            self.assertFalse(summary["git"]["git_available"])

    def test_artifact_root_inside_repo_uses_fallback(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        artifact_root = repo_root / "artifacts"
        summary = run_session(repo_root=repo_root, artifact_root=artifact_root)
        self.assertEqual(summary["status"], "ready_to_send")
        self.assertTrue(summary["artifact_fallback_used"])
        self.assertEqual(summary["artifact_fallback_reason"], "artifact_root_inside_repo")
        self.assertFalse(str(summary["actual_artifact_root"]).startswith(str(repo_root.resolve())))

    def test_no_write_repo_invariant(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        before = snapshot_files(repo_root)
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
        after = snapshot_files(repo_root)
        self.assertEqual(summary["status"], "ready_to_send")
        self.assertEqual(before, after)

    def test_summary_file_matches_return_payload(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_session(repo_root=repo_root, artifact_root=Path(temp_dir))
            summary_path = Path(summary["artifacts"]["session_summary"])
            loaded = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["session_id"], summary["session_id"])
            self.assertEqual(loaded["status"], "ready_to_send")


if __name__ == "__main__":
    unittest.main()
