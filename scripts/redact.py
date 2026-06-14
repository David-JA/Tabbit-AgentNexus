from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


PATTERNS = [
    ("openai_api_key", re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b")),
    ("github_token", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "private_key_block",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
]


@dataclass(frozen=True)
class RedactionResult:
    text: str
    counts: dict[str, int]

    @property
    def total(self) -> int:
        return sum(self.counts.values())


def redact_text(text: str) -> RedactionResult:
    counts = {name: 0 for name, _ in PATTERNS}
    sanitized = text
    for name, pattern in PATTERNS:
        sanitized, replace_count = pattern.subn(f"[REDACTED_POSSIBLE_SECRET:{name}]", sanitized)
        counts[name] = replace_count
    return RedactionResult(text=sanitized, counts=counts)


def is_binary_bytes(content: bytes) -> bool:
    if b"\x00" in content:
        return True
    sample = content[:1024]
    non_text = sum(byte < 9 or (13 < byte < 32) for byte in sample)
    return bool(sample) and (non_text / len(sample)) > 0.30


def scan_file(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if is_binary_bytes(raw):
        return {
            "path": str(path),
            "binary": True,
            "bytes": len(raw),
            "text": None,
            "redaction_count": 0,
            "counts": {},
        }

    text = raw.decode("utf-8", errors="replace")
    result = redact_text(text)
    return {
        "path": str(path),
        "binary": False,
        "bytes": len(raw),
        "text": result.text,
        "redaction_count": result.total,
        "counts": result.counts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redact likely secrets from a text file.")
    parser.add_argument("path", type=Path, help="File to scan and redact.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(scan_file(args.path), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
