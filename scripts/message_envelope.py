"""Message envelope for browser-mediated cross-space relay.

Implements the message envelope schema defined in the N1 foundation/relay
spec.  Every envelope:

- Carries an explicit `untrusted_data: true` flag.
- Stores only a SHA-256 digest of the payload -- never the raw payload.
- Never includes secret plaintext.
- Declares its completeness status and direction.

Downstream consumers MUST treat every envelope's payload as untrusted and
MUST NOT interpret natural-language content as executable instructions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import string
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure repo root is importable for dual-purpose (CLI + library) usage.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.relay_constants import (  # noqa: E402
    COMPLETENESS_COMPLETE,
    COMPLETENESS_INCOMPLETE,
    COMPLETENESS_UNKNOWN,
    DIRECTION_REPO_TO_WEB,
    DIRECTION_WEB_TO_REPO,
    PAYLOAD_ROLE_ASSISTANT_REPLY,
    PAYLOAD_ROLE_CONTEXT_PACK,
    PAYLOAD_ROLE_REVIEW_REQUEST,
    PAYLOAD_ROLE_STOP_SIGNAL,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_sha256_hex(value: str) -> bool:
    return len(value) == 64 and all(ch in string.hexdigits for ch in value)


@dataclass(frozen=True)
class MessageEnvelope:
    """A single cross-space relay message envelope.

    All fields are immutable.  The envelope carries metadata about a
    payload but never stores the payload itself.
    """

    envelope_id: str
    session_id: str
    round: int
    direction: str
    target_conversation_url: str
    payload_role: str
    payload_digest: str
    payload_bytes: int
    redaction_count: int = 0
    untrusted_data: bool = True
    completeness: str = COMPLETENESS_UNKNOWN
    ts: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "session_id": self.session_id,
            "round": self.round,
            "direction": self.direction,
            "target_conversation_url": self.target_conversation_url,
            "payload_role": self.payload_role,
            "payload_digest": self.payload_digest,
            "payload_bytes": self.payload_bytes,
            "redaction_count": self.redaction_count,
            "untrusted_data": self.untrusted_data,
            "completeness": self.completeness,
            "ts": self.ts,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def build_envelope(
    *,
    session_id: str,
    direction: str,
    target_conversation_url: str,
    payload_role: str,
    payload: bytes | str,
    round_number: int,
    redaction_count: int = 0,
    completeness: str = COMPLETENESS_UNKNOWN,
    envelope_id: str | None = None,
) -> MessageEnvelope:
    """Build a MessageEnvelope from its constituent parts.

    The payload is digested (SHA-256) but never stored in the envelope.
    """
    if isinstance(payload, str):
        payload = payload.encode("utf-8")

    return MessageEnvelope(
        envelope_id=envelope_id or uuid.uuid4().hex,
        session_id=session_id,
        round=round_number,
        direction=direction,
        target_conversation_url=target_conversation_url,
        payload_role=payload_role,
        payload_digest=_sha256_hex(payload),
        payload_bytes=len(payload),
        redaction_count=redaction_count,
        untrusted_data=True,
        completeness=completeness,
    )


def validate_envelope(envelope: MessageEnvelope) -> list[str]:
    """Validate an envelope and return a list of issues (empty = valid).

    Checks:
    - untrusted_data must be True (hard constraint).
    - direction must be one of the known values.
    - payload_role must be one of the known values.
    - round must be >= 1.
    - envelope_id and session_id must be non-empty.
    - payload_digest must be a 64-character SHA-256 hex string.
    - payload_bytes and redaction_count must be >= 0.
    - completeness must be complete | incomplete | unknown.
    """
    issues: list[str] = []

    if not envelope.untrusted_data:
        issues.append("untrusted_data must be True")

    if envelope.direction not in (DIRECTION_REPO_TO_WEB, DIRECTION_WEB_TO_REPO):
        issues.append(
            f"Unknown direction: {envelope.direction!r}"
        )

    valid_roles = {
        PAYLOAD_ROLE_CONTEXT_PACK,
        PAYLOAD_ROLE_REVIEW_REQUEST,
        PAYLOAD_ROLE_ASSISTANT_REPLY,
        PAYLOAD_ROLE_STOP_SIGNAL,
    }
    if envelope.payload_role not in valid_roles:
        issues.append(
            f"Unknown payload_role: {envelope.payload_role!r}"
        )

    if envelope.round < 1:
        issues.append("round must be >= 1")

    if not envelope.envelope_id:
        issues.append("envelope_id must be non-empty")

    if not envelope.session_id:
        issues.append("session_id must be non-empty")

    if not _is_sha256_hex(envelope.payload_digest):
        issues.append("payload_digest must be a 64-character SHA-256 hex string")

    if envelope.payload_bytes < 0:
        issues.append("payload_bytes must be >= 0")

    if envelope.redaction_count < 0:
        issues.append("redaction_count must be >= 0")

    valid_completeness = {
        COMPLETENESS_COMPLETE,
        COMPLETENESS_INCOMPLETE,
        COMPLETENESS_UNKNOWN,
    }
    if envelope.completeness not in valid_completeness:
        issues.append(
            "completeness must be one of: complete, incomplete, unknown"
        )

    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and print a relay message envelope."
    )
    parser.add_argument("--session-id", required=True, help="N1 session id.")
    parser.add_argument(
        "--direction",
        required=True,
        choices=[DIRECTION_REPO_TO_WEB, "web_to_repo"],
        help="Envelope direction.",
    )
    parser.add_argument(
        "--target-url",
        required=True,
        help="Target conversation URL (or alias).",
    )
    parser.add_argument(
        "--payload-role",
        required=True,
        choices=[
            PAYLOAD_ROLE_CONTEXT_PACK,
            "review_request",
            "assistant_reply",
            "stop_signal",
        ],
        help="Role of the payload.",
    )
    parser.add_argument(
        "--payload-file",
        type=argparse.FileType("rb"),
        help="File whose content is the payload (reads from stdin if omitted).",
    )
    parser.add_argument("--round", type=int, required=True, help="Relay round number.")
    parser.add_argument(
        "--redaction-count", type=int, default=0, help="Number of redacted items."
    )
    parser.add_argument(
        "--completeness",
        default=COMPLETENESS_UNKNOWN,
        choices=["complete", "incomplete", "unknown"],
        help="Completeness status of the payload.",
    )
    return parser.parse_args()


def main() -> int:
    import sys

    args = parse_args()
    payload_bytes = (
        args.payload_file.read()
        if args.payload_file
        else sys.stdin.buffer.read()
    )

    envelope = build_envelope(
        session_id=args.session_id,
        direction=args.direction,
        target_conversation_url=args.target_url,
        payload_role=args.payload_role,
        payload=payload_bytes,
        round_number=args.round,
        redaction_count=args.redaction_count,
        completeness=args.completeness,
    )

    issues = validate_envelope(envelope)
    if issues:
        for issue in issues:
            print(f"VALIDATION ERROR: {issue}", file=sys.stderr)
        return 1

    print(envelope.to_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
