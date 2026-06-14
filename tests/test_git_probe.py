from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.git_probe import probe


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class GitProbeTests(unittest.TestCase):
    def test_reports_git_unavailable(self) -> None:
        with patch("scripts.git_probe.shutil.which", return_value=None):
            info = probe(FIXTURES / "m1_repo_basic")
        self.assertFalse(info["git_available"])
        self.assertEqual(info["error"], "git_not_found")

    def test_reports_non_git_repo_gracefully(self) -> None:
        with patch("scripts.git_probe.shutil.which", return_value="/usr/bin/git"):
            with patch("scripts.git_probe.run_git_command") as mock_run:
                mock_run.return_value = subprocess.CompletedProcess(
                    args=["git", "rev-parse"],
                    returncode=128,
                    stdout="false\n",
                    stderr="fatal: not a git repository",
                )
                info = probe(FIXTURES / "m1_repo_basic")
        self.assertTrue(info["git_available"])
        self.assertFalse(info["repo_is_git"])
        self.assertEqual(info["error"], "not_a_git_repo")

    def test_reports_git_timeout(self) -> None:
        with patch("scripts.git_probe.shutil.which", return_value="/usr/bin/git"):
            with patch("scripts.git_probe.run_git_command", side_effect=subprocess.TimeoutExpired("git", 2)):
                info = probe(FIXTURES / "m1_repo_basic")
        self.assertEqual(info["error"], "git_timeout")


if __name__ == "__main__":
    unittest.main()
