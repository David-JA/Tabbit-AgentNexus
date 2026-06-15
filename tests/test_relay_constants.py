from __future__ import annotations

import unittest

from scripts.relay_constants import (
    DEFAULT_MAX_ROUNDS,
    DEFAULT_MAX_CONSECUTIVE_FAILURES,
    DEFAULT_STEP_MAX_RETRIES,
    MAX_COMPLETION_POLL_RETRIES,
    MAX_RESPONSE_WAIT_SECONDS,
    RELAY_STEPS,
    STOP_MAX_ROUNDS,
    STOP_CONSENSUS,
    STOP_USER_ABORT,
    STOP_RELAY_STUCK,
    STOP_ERROR,
    is_valid_step_id,
    all_step_ids,
    stop_reason_valid,
)


class RelayConstantsTests(unittest.TestCase):
    def test_default_max_rounds_is_positive(self) -> None:
        self.assertGreater(DEFAULT_MAX_ROUNDS, 0)

    def test_max_consecutive_failures_is_positive(self) -> None:
        self.assertGreater(DEFAULT_MAX_CONSECUTIVE_FAILURES, 0)

    def test_max_response_wait_seconds_is_positive(self) -> None:
        self.assertGreater(MAX_RESPONSE_WAIT_SECONDS, 0)

    def test_step_retries_not_exceed_completion_retries(self) -> None:
        # General step retries should not exceed completion poll retries,
        # because completion polling is the most retry-tolerant step.
        self.assertLessEqual(DEFAULT_STEP_MAX_RETRIES, MAX_COMPLETION_POLL_RETRIES)

    def test_relay_steps_has_fourteen_entries(self) -> None:
        self.assertEqual(len(RELAY_STEPS), 14)

    def test_all_step_ids_returns_fourteen(self) -> None:
        self.assertEqual(len(all_step_ids()), 14)

    def test_valid_step_ids_pass(self) -> None:
        for step_id in RELAY_STEPS:
            self.assertTrue(is_valid_step_id(step_id), f"step {step_id!r} should be valid")

    def test_invalid_step_id_fails(self) -> None:
        self.assertFalse(is_valid_step_id("99_fake_step"))

    def test_known_stop_reasons_are_valid(self) -> None:
        for reason in (STOP_MAX_ROUNDS, STOP_CONSENSUS, STOP_USER_ABORT,
                       STOP_RELAY_STUCK, STOP_ERROR):
            self.assertTrue(stop_reason_valid(reason), f"{reason!r} should be valid")

    def test_unknown_stop_reason_is_invalid(self) -> None:
        self.assertFalse(stop_reason_valid("some_random_reason"))


if __name__ == "__main__":
    unittest.main()
