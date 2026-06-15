"""Response completeness detection for browser-mediated relay.

Implements the completeness detection logic referenced in the 14-step
relay ledger (steps 4 and 11).  The core invariant is:

    A response that fails completeness detection MUST be recorded as
    "incomplete" and MUST NOT be written into review_report.md.

Detection strategies:
- Structural: checks for known end-of-response markers
- Size-based: flags unusually short or truncated outputs
- Time-based: enforces max wait before marking incomplete
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

# Ensure repo root is importable for dual-purpose (CLI + library) usage.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.relay_constants import (  # noqa: E402
    COMPLETENESS_COMPLETE,
    COMPLETENESS_INCOMPLETE,
    COMPLETENESS_UNKNOWN,
    COMPLETION_POLL_INTERVAL_SECONDS,
    MAX_COMPLETION_POLL_RETRIES,
    MAX_RESPONSE_WAIT_SECONDS,
)


@dataclass(frozen=True)
class CompletenessResult:
    """Result of a completeness check."""

    status: str  # complete | incomplete | unknown
    reason: str
    confidence: float = 1.0  # 0.0 - 1.0, only meaningful for complete/incomplete

    @property
    def is_complete(self) -> bool:
        return self.status == COMPLETENESS_COMPLETE

    @property
    def is_incomplete(self) -> bool:
        return self.status == COMPLETENESS_INCOMPLETE


# ---------------------------------------------------------------------------
# Structural markers (per-site extensible)
# ---------------------------------------------------------------------------

# Patterns that suggest a response is likely complete.
# These are heuristics, not guarantees; the unknown fallback is always safe.
_END_MARKERS: list[str] = [
    # Common closing patterns in AI assistant responses
    "\n---\n",
    "\n```\n\n",  # code block followed by double newline (end of message)
]

# Minimum character count to even consider a response "potentially complete".
_MIN_RESPONSE_CHARS = 50

# Responses shorter than this are almost certainly truncated.
_TRUNCATION_WARNING_CHARS = 20


def check_structural(text: str) -> CompletenessResult:
    """Check for structural markers indicating response completion."""
    if not text or not text.strip():
        return CompletenessResult(
            status=COMPLETENESS_INCOMPLETE,
            reason="empty_response",
            confidence=1.0,
        )

    if len(text) < _TRUNCATION_WARNING_CHARS:
        return CompletenessResult(
            status=COMPLETENESS_INCOMPLETE,
            reason="response_too_short",
            confidence=0.9,
        )

    # Check for end markers BEFORE the min-length check: a response with a
    # valid end marker is strong structural evidence, even if short.
    for marker in _END_MARKERS:
        if text.endswith(marker):
            return CompletenessResult(
                status=COMPLETENESS_COMPLETE,
                reason="end_marker_found",
                confidence=0.7,
            )
        # Also check if marker appears near the end (within trailing whitespace).
        stripped = text.rstrip()
        if stripped.endswith(marker.rstrip()):
            return CompletenessResult(
                status=COMPLETENESS_COMPLETE,
                reason="end_marker_found",
                confidence=0.6,
            )

    if len(text) < _MIN_RESPONSE_CHARS:
        return CompletenessResult(
            status=COMPLETENESS_UNKNOWN,
            reason="response_below_min_length",
            confidence=0.5,
        )

    # No structural evidence either way
    return CompletenessResult(
        status=COMPLETENESS_UNKNOWN,
        reason="no_structural_evidence",
        confidence=0.3,
    )


def check_size(text: str, max_bytes: int | None = None) -> CompletenessResult:
    """Check size-based heuristics for completeness."""
    byte_len = len(text.encode("utf-8"))

    if byte_len == 0:
        return CompletenessResult(
            status=COMPLETENESS_INCOMPLETE,
            reason="zero_byte_response",
            confidence=1.0,
        )

    if max_bytes is not None and byte_len > max_bytes:
        return CompletenessResult(
            status=COMPLETENESS_UNKNOWN,
            reason="response_exceeds_max_bytes",
            confidence=0.5,
        )

    return CompletenessResult(
        status=COMPLETENESS_UNKNOWN,
        reason="size_check_inconclusive",
        confidence=0.3,
    )


def evaluate_completeness(
    text: str,
    *,
    max_bytes: int | None = None,
) -> CompletenessResult:
    """Run all completeness checks and return the strongest signal.

    Priority: incomplete > complete > unknown.
    When multiple checks disagree, the most conservative result wins.
    """
    results = [
        check_structural(text),
        check_size(text, max_bytes=max_bytes),
    ]

    # If any check says incomplete, that wins.
    for r in results:
        if r.is_incomplete:
            return r

    # If any check says complete, that wins over unknown.
    for r in results:
        if r.is_complete:
            return r

    # Default to unknown.
    return CompletenessResult(
        status=COMPLETENESS_UNKNOWN,
        reason="all_checks_inconclusive",
        confidence=0.1,
    )


# ---------------------------------------------------------------------------
# Polling parameters (for step 11: Detect response completion)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PollingConfig:
    """Configuration for the completion-polling loop (step 11)."""

    max_retries: int = MAX_COMPLETION_POLL_RETRIES
    interval_seconds: float = COMPLETION_POLL_INTERVAL_SECONDS
    max_wait_seconds: float = MAX_RESPONSE_WAIT_SECONDS


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate response completeness for N1 relay."
    )
    parser.add_argument(
        "--text",
        help="Response text to evaluate (reads from stdin if omitted).",
    )
    parser.add_argument(
        "--text-file",
        type=argparse.FileType("r", encoding="utf-8"),
        help="File containing response text.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=None,
        help="Optional max byte limit for size check.",
    )
    return parser.parse_args()


def main() -> int:
    import sys

    args = parse_args()

    if args.text_file:
        text = args.text_file.read()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    result = evaluate_completeness(text, max_bytes=args.max_bytes)
    print(
        f"status={result.status} "
        f"reason={result.reason} "
        f"confidence={result.confidence:.2f}"
    )
    return 0 if result.is_complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
