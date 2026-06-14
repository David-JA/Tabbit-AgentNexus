from __future__ import annotations

import unittest
from pathlib import Path

from scripts.redact import redact_text, scan_file


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class RedactTests(unittest.TestCase):
    def test_redacts_known_secret_patterns(self) -> None:
        result = redact_text("OPENAI=sk-abcdefghijklmnopqrstuvwxyz\nTOKEN=ghp_abcdefghijklmnopqrstuvwxyz1234\n")
        self.assertIn("[REDACTED_POSSIBLE_SECRET:openai_api_key]", result.text)
        self.assertIn("[REDACTED_POSSIBLE_SECRET:github_token]", result.text)
        self.assertGreaterEqual(result.total, 2)

    def test_does_not_over_redact_normal_code(self) -> None:
        result = redact_text("def slugify(value: str) -> str:\n    return value.lower()\n")
        self.assertEqual(result.total, 0)

    def test_scan_file_flags_binary(self) -> None:
        binary_path = FIXTURES / "m1_repo_large_files" / "docs" / "sample.bin"
        report = scan_file(binary_path)
        self.assertTrue(report["binary"])
        self.assertEqual(report["redaction_count"], 0)


if __name__ == "__main__":
    unittest.main()
