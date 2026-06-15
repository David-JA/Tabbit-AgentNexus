from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_event(
    log_path: Path,
    session_id: str,
    event: str,
    status: str = "ok",
    **fields: Any,
) -> dict[str, Any]:
    payload = {
        "ts": _now_iso(),
        "session_id": session_id,
        "event": event,
        "status": status,
        **fields,
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


def write_session_summary(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append a JSONL audit event for N1 local workspace review runs.")
    parser.add_argument("--log-path", type=Path, required=True, help="Audit log JSONL path.")
    parser.add_argument("--session-id", required=True, help="N1 session id.")
    parser.add_argument("--event", required=True, help="Audit event name.")
    parser.add_argument("--status", default="ok", help="Audit event status.")
    parser.add_argument(
        "--field",
        action="append",
        default=[],
        help="Extra key=value field to include. May be provided multiple times.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    extra_fields: dict[str, str] = {}
    for item in args.field:
        key, _, value = item.partition("=")
        extra_fields[key] = value
    payload = append_event(
        args.log_path,
        session_id=args.session_id,
        event=args.event,
        status=args.status,
        **extra_fields,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
