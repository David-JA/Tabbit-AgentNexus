from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


READ_ONLY_COMMANDS = (
    ["rev-parse", "--is-inside-work-tree"],
    ["branch", "--show-current"],
    ["status", "--short"],
)


def run_git_command(repo_root: Path, args: list[str], timeout_sec: float) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        check=False,
    )


def probe(repo_root: Path, timeout_sec: float = 2.0, recent_commits: int = 5) -> dict[str, Any]:
    git_path = shutil.which("git")
    result: dict[str, Any] = {
        "repo_root": str(repo_root.resolve(strict=False)),
        "git_available": bool(git_path),
        "git_path": git_path,
        "repo_is_git": False,
        "branch": None,
        "status_short": "",
        "recent_commits": [],
        "error": None,
    }
    if not git_path:
        result["error"] = "git_not_found"
        return result

    try:
        inside = run_git_command(repo_root, ["rev-parse", "--is-inside-work-tree"], timeout_sec)
    except subprocess.TimeoutExpired:
        result["error"] = "git_timeout"
        return result

    if inside.returncode != 0 or inside.stdout.strip().lower() != "true":
        result["error"] = "not_a_git_repo"
        return result

    result["repo_is_git"] = True

    for command in READ_ONLY_COMMANDS[1:]:
        try:
            proc = run_git_command(repo_root, command, timeout_sec)
        except subprocess.TimeoutExpired:
            result["error"] = "git_timeout"
            return result
        if proc.returncode != 0 and result["error"] is None:
            result["error"] = proc.stderr.strip() or "git_command_failed"
        if command[0] == "branch":
            result["branch"] = proc.stdout.strip() or None
        elif command[0] == "status":
            result["status_short"] = proc.stdout.strip()

    if recent_commits > 0:
        try:
            log_proc = run_git_command(
                repo_root,
                ["log", f"-n{recent_commits}", "--pretty=format:%h %ad %s", "--date=short"],
                timeout_sec,
            )
        except subprocess.TimeoutExpired:
            result["error"] = "git_timeout"
            return result
        if log_proc.returncode == 0:
            lines = [line for line in log_proc.stdout.splitlines() if line.strip()]
            result["recent_commits"] = lines
        elif result["error"] is None:
            result["error"] = log_proc.stderr.strip() or "git_log_failed"

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe git metadata for the N1 local workspace review adapter.")
    parser.add_argument("--repo-root", type=Path, required=True, help="Mounted repo root.")
    parser.add_argument("--timeout-sec", type=float, default=2.0, help="Timeout per git command.")
    parser.add_argument(
        "--recent-commits",
        type=int,
        default=5,
        help="How many recent commits to include when git is available.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(
        json.dumps(
            probe(args.repo_root, timeout_sec=args.timeout_sec, recent_commits=args.recent_commits),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
