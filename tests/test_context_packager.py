from __future__ import annotations

import unittest
from pathlib import Path

from scripts.context_packager import build_context_pack
from scripts.policy import load_default


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class ContextPackagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_default()

    def test_builds_pack_and_redacts_secrets(self) -> None:
        repo_root = FIXTURES / "m1_repo_with_secrets"
        git_info = {"git_available": False, "repo_is_git": False}
        pack = build_context_pack(repo_root, self.policy, git_info)
        self.assertIn("# N1 Local Workspace Review Context Pack", pack.content)
        self.assertIn("[REDACTED_POSSIBLE_SECRET:openai_api_key]", pack.content)
        self.assertNotIn("sk-live-abcdefghijklmnopqrstuvwxyz", pack.content)
        self.assertGreater(pack.manifest["redaction_count"], 0)

    def test_skips_binary_and_oversized_files(self) -> None:
        repo_root = FIXTURES / "m1_repo_large_files"
        git_info = {"git_available": False, "repo_is_git": False}
        policy = dict(self.policy)
        policy["max_file_bytes"] = 128
        pack = build_context_pack(repo_root, policy, git_info)
        skipped = {item["path"]: item["reason"] for item in pack.manifest["skipped_files"]}
        self.assertEqual(skipped["docs/huge.txt"], "oversized")
        self.assertEqual(skipped["docs/sample.bin"], "binary")

    def test_raises_when_no_allowed_files(self) -> None:
        repo_root = FIXTURES / "m1_repo_denied_only"
        git_info = {"git_available": False, "repo_is_git": False}
        with self.assertRaisesRegex(ValueError, "no_allowed_files"):
            build_context_pack(repo_root, self.policy, git_info)


if __name__ == "__main__":
    unittest.main()
