"""Relay protocol constants for browser-mediated cross-space interaction.

These constants define the default thresholds, timeouts, and retry limits
for the N1 AgentNexus relay protocol.  They implement the hard constraints
defined in the spec:

- max_rounds: prevent unbounded autonomous loops
- per-step retry limits: prevent infinite tool-scheduling loops
- completeness thresholds: prevent half-output from being treated as complete
- user-intervention exit: relay_stuck after consecutive failures > threshold

All values are defaults; individual relay sessions may override them
via constructor parameters.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure repo root is importable for dual-purpose (CLI + library) usage.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ---------------------------------------------------------------------------
# Round / loop limits
# ---------------------------------------------------------------------------

# Maximum number of relay rounds before forced stop.
DEFAULT_MAX_ROUNDS = 5

# Maximum consecutive failures on any single step before triggering
# relay_stuck and requiring user intervention.
DEFAULT_MAX_CONSECUTIVE_FAILURES = 3

# ---------------------------------------------------------------------------
# Completeness detection
# ---------------------------------------------------------------------------

# Maximum number of polling retries when waiting for assistant response
# to complete (step 11: Detect response completion).
MAX_COMPLETION_POLL_RETRIES = 3

# Interval (seconds) between completion-poll attempts.
COMPLETION_POLL_INTERVAL_SECONDS = 3.0

# Maximum total wait time (seconds) for a single response completion.
# After this, the response is marked incomplete regardless of content.
MAX_RESPONSE_WAIT_SECONDS = 120.0

# ---------------------------------------------------------------------------
# Per-step retry defaults
# ---------------------------------------------------------------------------

# Default retry count for individual relay steps (except completion polling,
# which uses MAX_COMPLETION_POLL_RETRIES).
DEFAULT_STEP_MAX_RETRIES = 2

# ---------------------------------------------------------------------------
# Message size limits
# ---------------------------------------------------------------------------

# Maximum bytes for a single message payload sent through the relay.
MAX_PAYLOAD_BYTES = 2_000_000

# ---------------------------------------------------------------------------
# Relay step identifiers (14-step ledger)
# ---------------------------------------------------------------------------

STEP_LOCATE_CONVERSATION = "1_locate_conversation"
STEP_CAPTURE_URL = "2_capture_url"
STEP_CAPTURE_OUTPUT = "3_capture_assistant_output"
STEP_DETERMINE_COMPLETENESS = "4_determine_completeness"
STEP_PREPARE_PAYLOAD = "5_prepare_payload"
STEP_FOCUS_INPUT = "6_focus_input"
STEP_INSERT_MESSAGE = "7_insert_message"
STEP_VERIFY_TEXT = "8_verify_inserted_text"
STEP_SEND_MESSAGE = "9_send_message"
STEP_WAIT_RESPONSE = "10_wait_response"
STEP_DETECT_COMPLETION = "11_detect_completion"
STEP_CAPTURE_RESPONSE = "12_capture_final_response"
STEP_EMIT_LEDGER = "13_emit_ledger"
STEP_STOP_OR_CONTINUE = "14_stop_or_continue"

RELAY_STEPS: list[str] = [
    STEP_LOCATE_CONVERSATION,
    STEP_CAPTURE_URL,
    STEP_CAPTURE_OUTPUT,
    STEP_DETERMINE_COMPLETENESS,
    STEP_PREPARE_PAYLOAD,
    STEP_FOCUS_INPUT,
    STEP_INSERT_MESSAGE,
    STEP_VERIFY_TEXT,
    STEP_SEND_MESSAGE,
    STEP_WAIT_RESPONSE,
    STEP_DETECT_COMPLETION,
    STEP_CAPTURE_RESPONSE,
    STEP_EMIT_LEDGER,
    STEP_STOP_OR_CONTINUE,
]

# ---------------------------------------------------------------------------
# Stop reasons
# ---------------------------------------------------------------------------

STOP_MAX_ROUNDS = "max_rounds_reached"
STOP_CONSENSUS = "consensus_reached"
STOP_USER_ABORT = "user_abort"
STOP_RELAY_STUCK = "relay_stuck"
STOP_ERROR = "fatal_error"

# ---------------------------------------------------------------------------
# Envelope directions
# ---------------------------------------------------------------------------

DIRECTION_REPO_TO_WEB = "repo_to_web"
DIRECTION_WEB_TO_REPO = "web_to_repo"

# ---------------------------------------------------------------------------
# Payload roles
# ---------------------------------------------------------------------------

PAYLOAD_ROLE_CONTEXT_PACK = "context_pack"
PAYLOAD_ROLE_REVIEW_REQUEST = "review_request"
PAYLOAD_ROLE_ASSISTANT_REPLY = "assistant_reply"
PAYLOAD_ROLE_STOP_SIGNAL = "stop_signal"

# ---------------------------------------------------------------------------
# Static helpers
# ---------------------------------------------------------------------------

def all_step_ids() -> list[str]:
    """Return the 14 canonical relay step identifiers in order."""
    return list(RELAY_STEPS)


def is_valid_step_id(step_id: str) -> bool:
    """Check whether *step_id* is one of the 14 canonical steps."""
    return step_id in RELAY_STEPS


def stop_reason_valid(reason: str) -> bool:
    """Check whether *reason* is a known stop condition."""
    return reason in {
        STOP_MAX_ROUNDS,
        STOP_CONSENSUS,
        STOP_USER_ABORT,
        STOP_RELAY_STUCK,
        STOP_ERROR,
    }

# ---------------------------------------------------------------------------
# Completeness states
# ---------------------------------------------------------------------------

COMPLETENESS_COMPLETE = "complete"
COMPLETENESS_INCOMPLETE = "incomplete"
COMPLETENESS_UNKNOWN = "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print default relay protocol constants for N1 AgentNexus."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output constants as JSON instead of human-readable text.",
    )
    return parser.parse_args()


def main() -> int:
    import json

    args = parse_args()
    constants: dict[str, object] = {
        "DEFAULT_MAX_ROUNDS": DEFAULT_MAX_ROUNDS,
        "DEFAULT_MAX_CONSECUTIVE_FAILURES": DEFAULT_MAX_CONSECUTIVE_FAILURES,
        "MAX_COMPLETION_POLL_RETRIES": MAX_COMPLETION_POLL_RETRIES,
        "COMPLETION_POLL_INTERVAL_SECONDS": COMPLETION_POLL_INTERVAL_SECONDS,
        "MAX_RESPONSE_WAIT_SECONDS": MAX_RESPONSE_WAIT_SECONDS,
        "DEFAULT_STEP_MAX_RETRIES": DEFAULT_STEP_MAX_RETRIES,
        "MAX_PAYLOAD_BYTES": MAX_PAYLOAD_BYTES,
        "RELAY_STEPS": RELAY_STEPS,
        "STOP_REASONS": [
            STOP_MAX_ROUNDS,
            STOP_CONSENSUS,
            STOP_USER_ABORT,
            STOP_RELAY_STUCK,
            STOP_ERROR,
        ],
    }
    if args.json:
        print(json.dumps(constants, indent=2, ensure_ascii=False))
    else:
        for key, value in constants.items():
            print(f"{key} = {value!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
