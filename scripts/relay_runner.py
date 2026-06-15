"""Relay runner: ties N1 local review session output to the relay protocol.

This module is the composition root for browser-mediated relay: it takes the
output of `n1_review_session.py` (context_pack.md + audit artifacts) and
prepares a MessageEnvelope for handoff to the Browser Agent.

It does NOT perform browser interactions itself — those belong to the
Browser Agent / Tabbit Agent in a Tabbit workspace.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Ensure repo root is importable for dual-purpose (CLI + library) usage.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.message_envelope import build_envelope, validate_envelope  # noqa: E402
from scripts.relay_constants import (  # noqa: E402
    COMPLETENESS_UNKNOWN,
    DEFAULT_MAX_ROUNDS,
    DIRECTION_REPO_TO_WEB,
    PAYLOAD_ROLE_CONTEXT_PACK,
)

DEFAULT_RELAY_TEMPLATE_PATH = (
    _REPO_ROOT
    / ".agent"
    / "skills"
    / "nexus-local-workspace-review"
    / "templates"
    / "relay_message_repo_to_web.md"
)


def prepare_relay_handoff(
    *,
    session_id: str,
    context_pack_path: Path,
    round_number: int = 1,
    target_url: str = "",
    redaction_count: int = 0,
    max_rounds: int = DEFAULT_MAX_ROUNDS,
) -> dict:
    """Prepare a relay handoff from a completed N1 review session.

    Returns a dict with the envelope and template variables ready for
    the Browser Agent to use.
    """
    if not context_pack_path.exists():
        raise FileNotFoundError(f"context_pack not found: {context_pack_path}")

    payload = context_pack_path.read_text(encoding="utf-8")

    envelope = build_envelope(
        session_id=session_id,
        direction=DIRECTION_REPO_TO_WEB,
        target_conversation_url=target_url,
        payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
        payload=payload,
        round_number=round_number,
        redaction_count=redaction_count,
    )

    issues = validate_envelope(envelope)
    if issues:
        raise ValueError(f"Envelope validation failed: {issues}")

    return {
        "envelope": envelope.to_dict(),
        "template_vars": {
            "session_id": session_id,
            "round": round_number,
            "max_rounds": max_rounds,
            "envelope_id": envelope.envelope_id,
            "redaction_count": redaction_count,
            "payload": payload,
        },
    }


def render_relay_message(
    *,
    template_path: Path,
    template_vars: dict[str, Any],
) -> str:
    """Render a relay handoff message from a markdown template."""
    if not template_path.exists():
        raise FileNotFoundError(f"relay template not found: {template_path}")

    template_text = template_path.read_text(encoding="utf-8")
    try:
        return template_text.format(**template_vars)
    except KeyError as exc:
        missing = exc.args[0]
        raise ValueError(
            f"relay template placeholder missing from template_vars: {missing}"
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a relay handoff envelope from N1 review artifacts."
    )
    parser.add_argument(
        "--session-id", required=True, help="N1 session id."
    )
    parser.add_argument(
        "--context-pack", type=Path, required=True,
        help="Path to context_pack.md from n1_review_session.",
    )
    parser.add_argument(
        "--target-url", default="",
        help="Target Web Agent conversation URL.",
    )
    parser.add_argument(
        "--round", type=int, default=1,
        help="Relay round number (default: 1).",
    )
    parser.add_argument(
        "--redaction-count", type=int, default=0,
        help="Number of redacted items in the context pack.",
    )
    parser.add_argument(
        "--output", type=Path,
        help="Write envelope JSON to file instead of stdout.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        help="Template path for rendering a repo-to-web relay message.",
    )
    parser.add_argument(
        "--message-output",
        type=Path,
        help="Write a rendered relay message to this file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = prepare_relay_handoff(
            session_id=args.session_id,
            context_pack_path=args.context_pack,
            round_number=args.round,
            target_url=args.target_url,
            redaction_count=args.redaction_count,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.template and not args.message_output:
        print(
            "ERROR: --template requires --message-output",
            file=sys.stderr,
        )
        return 1

    rendered_message: str | None = None
    if args.message_output:
        template_path = args.template or DEFAULT_RELAY_TEMPLATE_PATH
        try:
            rendered_message = render_relay_message(
                template_path=template_path,
                template_vars=result["template_vars"],
            )
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    envelope_json = json.dumps(result["envelope"], indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(envelope_json, encoding="utf-8")
        print(f"Envelope written to {args.output}")
    else:
        print(envelope_json)

    if rendered_message is not None:
        args.message_output.parent.mkdir(parents=True, exist_ok=True)
        args.message_output.write_text(rendered_message, encoding="utf-8")
        print(f"Relay message written to {args.message_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
