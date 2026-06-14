from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


DEFAULT_POLICY_PATH = (
    Path(__file__).resolve().parents[1] / "config" / "default_policy.review_only.json"
)


@dataclass(frozen=True)
class PathDecision:
    allowed: bool
    reason: str
    rel_path: str | None


def load_default(path: Path | None = None) -> dict[str, Any]:
    policy_path = path or DEFAULT_POLICY_PATH
    with policy_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def create_session(
    repo_root: Path,
    policy: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    base = dict(policy or load_default())
    base["repo_root"] = str(repo_root.resolve())
    base["session_id"] = session_id or f"m1-{uuid.uuid4().hex[:12]}"
    return base


def _resolve_within_repo(candidate: Path, repo_root: Path) -> tuple[Path | None, str | None]:
    try:
        repo_real = repo_root.resolve()
        candidate_real = candidate.resolve(strict=False)
        rel = candidate_real.relative_to(repo_real)
    except Exception:
        return None, None
    return candidate_real, rel.as_posix()


def _matches_any(rel_path: str, patterns: list[str]) -> bool:
    return any(fnmatch(rel_path, pattern) for pattern in patterns)


def decide_path(candidate: Path, repo_root: Path, policy: dict[str, Any]) -> PathDecision:
    _, rel_path = _resolve_within_repo(candidate, repo_root)
    if rel_path is None:
        return PathDecision(False, "outside_repo_root", None)

    deny_globs = list(policy.get("deny_globs", []))
    if _matches_any(rel_path, deny_globs):
        return PathDecision(False, "denied_glob", rel_path)

    allow_globs = list(policy.get("allow_globs", []))
    if allow_globs and not _matches_any(rel_path, allow_globs):
        return PathDecision(False, "not_allowlisted", rel_path)

    return PathDecision(True, "allowed", rel_path)


def is_path_allowed(candidate: Path, repo_root: Path, policy: dict[str, Any]) -> bool:
    return decide_path(candidate, repo_root, policy).allowed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate whether paths are allowed by M1 policy.")
    parser.add_argument("--repo-root", type=Path, required=True, help="Mounted repo root.")
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY_PATH,
        help="Policy JSON path.",
    )
    parser.add_argument("paths", nargs="+", help="Candidate file paths to check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    policy = load_default(args.policy)
    repo_root = args.repo_root.resolve()
    results = []
    for raw_path in args.paths:
        decision = decide_path(Path(raw_path), repo_root, policy)
        results.append(
            {
                "path": raw_path,
                "allowed": decision.allowed,
                "reason": decision.reason,
                "rel_path": decision.rel_path,
            }
        )
    print(json.dumps({"repo_root": str(repo_root), "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
