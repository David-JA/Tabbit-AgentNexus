from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_log import append_event, write_session_summary  # noqa: E402
from scripts.context_packager import DEFAULT_REVIEW_REQUEST, build_context_pack  # noqa: E402
from scripts.discover_repo import discover_repo  # noqa: E402
from scripts.git_probe import probe  # noqa: E402
from scripts.policy import create_session, load_default  # noqa: E402


def _is_within(candidate: Path, root: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
    except Exception:
        return False
    return True


def _resolve_artifact_session_dir(
    preferred_root: Path,
    repo_root: Path,
    session_id: str,
) -> tuple[Path, Path, bool, str | None]:
    preferred_root = preferred_root.resolve(strict=False)
    if _is_within(preferred_root, repo_root):
        fallback_root = Path(tempfile.gettempdir()) / "agentnexus-artifacts"
        session_dir = fallback_root / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir, fallback_root, True, "artifact_root_inside_repo"

    try:
        session_dir = preferred_root / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir, preferred_root, False, None
    except OSError:
        fallback_root = Path(tempfile.gettempdir()) / "agentnexus-artifacts"
        session_dir = fallback_root / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir, fallback_root, True, "artifact_root_unavailable"


def _build_confirmation_summary(manifest: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "selected_files": [item["path"] for item in manifest["selected_files"]],
        "selected_file_count": manifest["selected_file_count"],
        "bytes_total": manifest["bytes_total"],
        "redaction_count": manifest["redaction_count"],
        "default_exclusions": list(policy.get("deny_globs", [])),
        "confirmation_required": True,
        "confirmed": False,
    }


def run_session(
    repo_root: Path,
    artifact_root: Path,
    policy_path: Path | None = None,
    session_id: str | None = None,
    review_request: str | None = None,
) -> dict[str, Any]:
    policy = create_session(repo_root, load_default(policy_path), session_id=session_id)
    session_id = str(policy["session_id"])
    discovery = discover_repo(repo_root)
    session_dir, actual_root, fallback_used, fallback_reason = _resolve_artifact_session_dir(
        artifact_root,
        repo_root,
        session_id,
    )

    audit_path = session_dir / "audit.jsonl"
    context_pack_path = session_dir / "context_pack.md"
    summary_path = session_dir / "session_summary.json"

    append_event(
        audit_path,
        session_id=session_id,
        event="session_started",
        repo_root_alias=str(repo_root),
        preferred_artifact_root=str(artifact_root),
        actual_artifact_root=str(actual_root),
        fallback_used=fallback_used,
        failure_class=fallback_reason,
        detail={"mode": policy.get("mode", "review_only")},
    )

    git_info: dict[str, Any] = {
        "repo_root": str(repo_root.resolve(strict=False)),
        "git_available": False,
        "git_path": None,
        "repo_is_git": False,
        "branch": None,
        "status_short": "",
        "recent_commits": [],
        "error": "repo_unchecked",
    }
    summary: dict[str, Any] = {
        "session_id": session_id,
        "status": "failed",
        "mode": policy.get("mode", "review_only"),
        "repo_root": str(repo_root.resolve(strict=False)),
        "preferred_artifact_root": str(artifact_root),
        "actual_artifact_root": str(actual_root),
        "artifact_fallback_used": fallback_used,
        "artifact_fallback_reason": fallback_reason,
        "artifacts": {
            "context_pack": str(context_pack_path),
            "audit_log": str(audit_path),
            "session_summary": str(summary_path),
            "review_report": None,
        },
        "discovery": discovery,
        "git": git_info,
        "failure_class": None,
        "failures": [],
        "send_confirmation": None,
        "invariants": {
            "no_write_repo": not _is_within(actual_root, repo_root),
            "browser_submission_performed": False,
            "review_only": True,
        },
    }

    if fallback_reason == "artifact_root_inside_repo":
        summary["failures"].append("artifact_fallback_used")
        append_event(
            audit_path,
            session_id=session_id,
            event="artifact_fallback_used",
            status="warning",
            preferred_artifact_root=str(artifact_root),
            actual_artifact_root=str(actual_root),
            failure_class=fallback_reason,
        )
    elif fallback_reason == "artifact_root_unavailable":
        summary["failures"].append("artifact_fallback_used")
        append_event(
            audit_path,
            session_id=session_id,
            event="artifact_fallback_used",
            status="warning",
            preferred_artifact_root=str(artifact_root),
            actual_artifact_root=str(actual_root),
            failure_class=fallback_reason,
        )

    if not discovery["exists"]:
        summary["failure_class"] = "repo_root_missing"
        summary["failures"].append("repo_root_missing")
        append_event(
            audit_path,
            session_id=session_id,
            event="session_failed",
            status="error",
            failure_class="repo_root_missing",
        )
        write_session_summary(summary_path, summary)
        return summary

    if not discovery["is_dir"]:
        summary["failure_class"] = "repo_not_mounted"
        summary["failures"].append("repo_not_mounted")
        append_event(
            audit_path,
            session_id=session_id,
            event="session_failed",
            status="error",
            failure_class="repo_not_mounted",
        )
        write_session_summary(summary_path, summary)
        return summary

    git_info = probe(repo_root)
    summary["git"] = git_info

    try:
        pack = build_context_pack(
            repo_root=repo_root,
            policy=policy,
            git_info=git_info,
            review_request=(review_request or DEFAULT_REVIEW_REQUEST),
        )
    except ValueError as exc:
        failure_class = str(exc)
        summary["failure_class"] = failure_class
        summary["failures"].append(failure_class)
        append_event(
            audit_path,
            session_id=session_id,
            event="context_pack_failed",
            status="error",
            failure_class=failure_class,
            git_available=git_info.get("git_available", False),
        )
        write_session_summary(summary_path, summary)
        return summary

    context_pack_path.write_text(pack.content, encoding="utf-8")
    confirmation = _build_confirmation_summary(pack.manifest, policy)
    summary["status"] = "ready_to_send"
    summary["failure_class"] = None
    summary["send_confirmation"] = confirmation
    summary["manifest"] = pack.manifest
    if not summary["failures"]:
        summary["failures"] = []

    append_event(
        audit_path,
        session_id=session_id,
        event="context_pack_built",
        status="ok",
        repo_root_alias=str(repo_root),
        artifact_root=str(actual_root),
        bytes_total=pack.manifest["bytes_total"],
        selected_file_count=pack.manifest["selected_file_count"],
        redaction_count=pack.manifest["redaction_count"],
        git_available=git_info.get("git_available", False),
        failure_class=None,
        detail={
            "max_total_context_bytes": policy["max_total_context_bytes"],
            "max_file_bytes": policy["max_file_bytes"],
            "max_file_count": policy["max_file_count"],
        },
    )
    append_event(
        audit_path,
        session_id=session_id,
        event="ready_to_send",
        status="ok",
        selected_file_count=confirmation["selected_file_count"],
        bytes_total=confirmation["bytes_total"],
        redaction_count=confirmation["redaction_count"],
        confirmation_required=True,
    )
    write_session_summary(summary_path, summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the N1 local workspace review session and generate ready-to-send local artifacts."
    )
    parser.add_argument("--repo-root", type=Path, required=True, help="Mounted repo root to review.")
    parser.add_argument(
        "--artifact-root",
        type=Path,
        required=True,
        help="Preferred artifact output root. The runner falls back outside the repo when needed.",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        help="Optional policy JSON path. Defaults to config/default_policy.review_only.json.",
    )
    parser.add_argument("--session-id", help="Optional explicit N1 session id.")
    parser.add_argument(
        "--review-request-file",
        type=Path,
        help="Optional markdown/text file that overrides the default review request.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    review_request = None
    if args.review_request_file:
        review_request = args.review_request_file.read_text(encoding="utf-8")
    summary = run_session(
        repo_root=args.repo_root,
        artifact_root=args.artifact_root,
        policy_path=args.policy,
        session_id=args.session_id,
        review_request=review_request,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "ready_to_send" else 1


if __name__ == "__main__":
    raise SystemExit(main())
