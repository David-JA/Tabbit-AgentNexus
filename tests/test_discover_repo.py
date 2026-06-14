from __future__ import annotations

import unittest
from pathlib import Path

from scripts.discover_repo import discover_repo


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class DiscoverRepoTests(unittest.TestCase):
    def test_reports_basic_repo_shape(self) -> None:
        info = discover_repo(FIXTURES / "m1_repo_basic")
        self.assertTrue(info["exists"])
        self.assertTrue(info["is_dir"])
        self.assertFalse(info["git_dir_present"])


if __name__ == "__main__":
    unittest.main()
