from __future__ import annotations

import unittest

from scripts.relay_completeness import (
    CompletenessResult,
    check_structural,
    check_size,
    evaluate_completeness,
)
from scripts.relay_constants import (
    COMPLETENESS_COMPLETE,
    COMPLETENESS_INCOMPLETE,
    COMPLETENESS_UNKNOWN,
)


class CompletenessStructuralTests(unittest.TestCase):
    def test_empty_text_is_incomplete(self) -> None:
        result = check_structural("")
        self.assertTrue(result.is_incomplete)
        self.assertEqual(result.reason, "empty_response")

    def test_whitespace_only_is_incomplete(self) -> None:
        result = check_structural("   \n  ")
        self.assertTrue(result.is_incomplete)

    def test_very_short_text_is_incomplete(self) -> None:
        result = check_structural("hi")
        self.assertTrue(result.is_incomplete)
        self.assertEqual(result.reason, "response_too_short")

    def test_short_but_not_truncated_is_unknown(self) -> None:
        # 30 chars: below _MIN_RESPONSE_CHARS (50) but above _TRUNCATION_WARNING_CHARS (20)
        result = check_structural("X" * 30)
        self.assertEqual(result.status, COMPLETENESS_UNKNOWN)

    def test_long_text_no_marker_is_unknown(self) -> None:
        result = check_structural("This is a long response without any end marker. " * 5)
        self.assertEqual(result.status, COMPLETENESS_UNKNOWN)

    def test_end_marker_detected(self) -> None:
        text = "A complete response with code block.\n```\n\n"
        result = check_structural(text)
        self.assertTrue(result.is_complete)


class CompletenessSizeTests(unittest.TestCase):
    def test_zero_bytes_is_incomplete(self) -> None:
        result = check_size("")
        self.assertTrue(result.is_incomplete)

    def test_under_max_bytes_is_unknown(self) -> None:
        result = check_size("hello", max_bytes=1000)
        self.assertEqual(result.status, COMPLETENESS_UNKNOWN)

    def test_over_max_bytes_is_unknown(self) -> None:
        result = check_size("x" * 100, max_bytes=10)
        self.assertEqual(result.status, COMPLETENESS_UNKNOWN)


class CompletenessEvaluateTests(unittest.TestCase):
    def test_empty_is_incomplete(self) -> None:
        result = evaluate_completeness("")
        self.assertTrue(result.is_incomplete)

    def test_long_text_is_unknown(self) -> None:
        result = evaluate_completeness("A reasonably long response. " * 10)
        self.assertEqual(result.status, COMPLETENESS_UNKNOWN)

    def test_structural_win_over_unknown(self) -> None:
        text = "Here is the complete analysis.\n```\n\n"
        result = evaluate_completeness(text)
        # structural says complete, size says unknown → complete wins
        self.assertTrue(result.is_complete)

    def test_incomplete_wins_over_complete(self) -> None:
        # Short text that happens to end with a marker should still be incomplete
        text = "ab\n```\n\n"
        result = evaluate_completeness(text)
        # structural says incomplete (too short), but marker check is inside
        # structural. Short-circuit: incomplete wins.
        self.assertTrue(result.is_incomplete)

    def test_confidence_range(self) -> None:
        result = evaluate_completeness("A" * 200)
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)


class CompletenessResultTests(unittest.TestCase):
    def test_is_complete_property(self) -> None:
        r = CompletenessResult(status=COMPLETENESS_COMPLETE, reason="test")
        self.assertTrue(r.is_complete)
        self.assertFalse(r.is_incomplete)

    def test_is_incomplete_property(self) -> None:
        r = CompletenessResult(status=COMPLETENESS_INCOMPLETE, reason="test")
        self.assertTrue(r.is_incomplete)
        self.assertFalse(r.is_complete)


if __name__ == "__main__":
    unittest.main()
