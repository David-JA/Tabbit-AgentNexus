from __future__ import annotations

import unittest
from pathlib import Path

from scripts.policy import decide_path, load_default


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_default()

    def test_allowlisted_docs_file_is_allowed(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        decision = decide_path(repo_root / "docs" / "guide.md", repo_root, self.policy)
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "allowed")

    def test_deny_glob_wins_for_env_file(self) -> None:
        repo_root = FIXTURES / "m1_repo_with_secrets"
        decision = decide_path(repo_root / ".env", repo_root, self.policy)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "denied_glob")

    def test_path_outside_repo_is_rejected(self) -> None:
        repo_root = FIXTURES / "m1_repo_basic"
        outside = FIXTURES / "m1_repo_with_secrets" / "docs" / "secrets.md"
        decision = decide_path(outside, repo_root, self.policy)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "outside_repo_root")


if __name__ == "__main__":
    unittest.main()
