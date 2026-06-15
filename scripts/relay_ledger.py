"""14-step relay ledger for browser-mediated cross-space interaction.

Records every step of a relay round into an append-only JSONL ledger.
Each entry maps to one of the 14 canonical relay steps defined in the
N1 foundation/relay spec.

The ledger supports:
- Per-step recording with status / error / duration
- Round-level summaries
- Stop-condition tracking
- Replay via sequential JSONL reading
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure repo root is importable for dual-purpose (CLI + library) usage.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.relay_constants import (  # noqa: E402
    RELAY_STEPS,
    all_step_ids,
    is_valid_step_id,
    stop_reason_valid,
)

VALID_STEP_STATUSES = {"ok", "error", "skipped", "stuck"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Step-level entry
# ---------------------------------------------------------------------------

@dataclass
class LedgerStep:
    """A single step entry within a relay round."""

    round: int
    step_id: str
    status: str  # "ok" | "error" | "skipped" | "stuck"
    detail: str = ""
    error: str | None = None
    duration_ms: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "round": self.round,
            "step_id": self.step_id,
            "status": self.status,
        }
        if self.detail:
            d["detail"] = self.detail
        if self.error:
            d["error"] = self.error
        if self.duration_ms is not None:
            d["duration_ms"] = self.duration_ms
        if self.extra:
            d["extra"] = self.extra
        return d


# ---------------------------------------------------------------------------
# Round-level summary
# ---------------------------------------------------------------------------

@dataclass
class RelayRoundSummary:
    """Summary of a completed relay round."""

    round: int
    envelope: str = ""  # envelope_id reference, not full payload
    stop_reason: str | None = None
    steps_completed: int = 0
    steps_total: int = 14
    errors: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "round": self.round,
            "steps_completed": self.steps_completed,
            "steps_total": self.steps_total,
            "errors": self.errors,
        }
        if self.envelope:
            d["envelope"] = self.envelope
        if self.stop_reason:
            d["stop_reason"] = self.stop_reason
        if self.extra:
            d["extra"] = self.extra
        return d


# ---------------------------------------------------------------------------
# Ledger writer
# ---------------------------------------------------------------------------

class RelayLedger:
    """Append-only JSONL ledger for a single relay session.

    Usage:
        ledger = RelayLedger(log_path, session_id="n1-abc123")
        ledger.record_step(round=1, step_id="1_locate_conversation",
                           status="ok", detail="found active chat tab")
        ...
        ledger.write_round_summary(RelayRoundSummary(round=1, ...))
    """

    def __init__(self, log_path: Path, session_id: str) -> None:
        if not session_id:
            raise ValueError("session_id must be non-empty")
        self._log_path = log_path
        self._session_id = session_id
        log_path.parent.mkdir(parents=True, exist_ok=True)

    def record_step(
        self,
        round: int,
        step_id: str,
        status: str = "ok",
        detail: str = "",
        error: str | None = None,
        duration_ms: int | None = None,
        **extra: Any,
    ) -> LedgerStep:
        self._validate_step(
            round=round,
            step_id=step_id,
            status=status,
            duration_ms=duration_ms,
        )
        step = LedgerStep(
            round=round,
            step_id=step_id,
            status=status,
            detail=detail,
            error=error,
            duration_ms=duration_ms,
            extra=extra,
        )
        self._append(step.to_dict(), event="relay_step")
        return step

    def write_round_summary(self, summary: RelayRoundSummary) -> None:
        self._validate_summary(summary)
        payload = summary.to_dict()
        payload["session_id"] = self._session_id
        self._append(payload, event="relay_round_summary")

    def _append(self, payload: dict[str, Any], event: str) -> None:
        payload["ts"] = _now_iso()
        payload["session_id"] = self._session_id
        payload["event"] = event
        with self._log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    @property
    def log_path(self) -> Path:
        return self._log_path

    @staticmethod
    def _validate_step(
        *,
        round: int,
        step_id: str,
        status: str,
        duration_ms: int | None,
    ) -> None:
        if round < 1:
            raise ValueError("round must be >= 1")
        if not is_valid_step_id(step_id):
            raise ValueError(f"Unknown relay step id: {step_id!r}")
        if status not in VALID_STEP_STATUSES:
            raise ValueError(f"Unknown relay step status: {status!r}")
        if duration_ms is not None and duration_ms < 0:
            raise ValueError("duration_ms must be >= 0")

    @staticmethod
    def _validate_summary(summary: RelayRoundSummary) -> None:
        if summary.round < 1:
            raise ValueError("round must be >= 1")
        if summary.stop_reason is not None and not stop_reason_valid(summary.stop_reason):
            raise ValueError(f"Unknown stop reason: {summary.stop_reason!r}")
        if summary.steps_completed < 0:
            raise ValueError("steps_completed must be >= 0")
        if summary.steps_total < 0:
            raise ValueError("steps_total must be >= 0")
        if summary.steps_completed > summary.steps_total:
            raise ValueError("steps_completed must be <= steps_total")
        if summary.errors < 0:
            raise ValueError("errors must be >= 0")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record a relay ledger step for N1 AgentNexus."
    )
    parser.add_argument(
        "--log-path", type=Path, required=True, help="Ledger JSONL path."
    )
    parser.add_argument("--session-id", required=True, help="N1 session id.")
    parser.add_argument("--round", type=int, required=True, help="Relay round number.")
    parser.add_argument(
        "--step-id",
        required=True,
        choices=RELAY_STEPS,
        help="Canonical step identifier.",
    )
    parser.add_argument(
        "--status",
        default="ok",
        choices=["ok", "error", "skipped", "stuck"],
        help="Step execution status.",
    )
    parser.add_argument("--detail", default="", help="Human-readable step detail.")
    parser.add_argument("--error", default=None, help="Error message if status=error.")
    parser.add_argument(
        "--duration-ms", type=int, default=None, help="Step duration in milliseconds."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = RelayLedger(log_path=args.log_path, session_id=args.session_id)
    step = ledger.record_step(
        round=args.round,
        step_id=args.step_id,
        status=args.status,
        detail=args.detail,
        error=args.error,
        duration_ms=args.duration_ms,
    )
    print(json.dumps(step.to_dict(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
