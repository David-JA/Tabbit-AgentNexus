from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "exports" / "repo-context"
CONTEXT_DIR = Path("_context_pack")
EXCLUDED_PARTS = {".git", "__pycache__", "reference", "exports"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


@dataclass(frozen=True)
class Profile:
    name: str
    description: str
    include: tuple[str, ...]


PROFILES = {
    "minimal": Profile(
        name="minimal",
        description="正式入口 + 当前 N1 spec + repo-local skills 的轻量理解包。",
        include=(
            "readme.md",
            "AGENTS.md",
            ".gitignore",
            "docs/PROJECT_MEMORY.md",
            "docs/README_docs.md",
            "docs/architecture/nexus_runtime_architecture.md",
            "docs/architecture/bridge_runtime_architecture.md",
            "docs/architecture/tabbit_browser_agent_behavior_boundary.md",
            "docs/workflows/README_workflows.md",
            "docs/workflows/agent_conventions.md",
            "docs/workflows/discuss_spec_workflow.md",
            "docs/workflows/bounded_agent_dialogue.md",
            "docs/reports/README_reports.md",
            "discuss/README_discuss.md",
            "discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md",
            "discuss/2026-06-15_n1-adapter-scaffold-and-local-dry-run-closure.md",
            ".agent/skills",
            "scripts/n1_review_session.py",
            "scripts/tools/package_nexus_context.py",
            "scripts/tools/new_discuss_spec.py",
        ),
    ),
    "overview": Profile(
        name="overview",
        description="面向网页 AI 评审的完整理解包，默认包含正式入口、当前 discuss、repo-local skills、运行脚本、配置与测试夹具。",
        include=(
            "readme.md",
            "AGENTS.md",
            ".gitignore",
            "config",
            "docs",
            "discuss",
            ".agent/skills",
            "scripts",
            "tests",
        ),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package the current Tabbit AgentNexus repo into an AI-readable zip context pack."
    )
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="overview",
        help="Packaging profile to use.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated zip artifacts.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit zip path. Overrides --output-dir naming.",
    )
    parser.add_argument(
        "--git-commits",
        type=int,
        default=5,
        help="How many recent commits to summarize. Use 0 to skip git summary generation.",
    )
    return parser.parse_args()


def should_exclude(path: Path) -> bool:
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return True
    if len(path.parts) >= 2 and path.parts[0] == "discuss" and path.parts[1] == "archive":
        return True
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True
    return False


def expand_includes(entries: Iterable[str]) -> list[Path]:
    collected: set[Path] = set()
    for entry in entries:
        repo_path = REPO_ROOT / entry
        if not repo_path.exists():
            continue
        if repo_path.is_file():
            if not should_exclude(repo_path.relative_to(REPO_ROOT)):
                collected.add(repo_path)
            continue
        for child in repo_path.rglob("*"):
            if child.is_file():
                rel = child.relative_to(REPO_ROOT)
                if not should_exclude(rel):
                    collected.add(child)
    return sorted(collected)


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def build_git_summary(commit_count: int) -> tuple[str, str]:
    if commit_count <= 0:
        return "skipped", "# Git Recent Commits\n\nGit summary generation was skipped.\n"

    status = run_git(["status", "--short"])
    log = run_git(
        [
            "log",
            f"-n{commit_count}",
            "--pretty=format:%h %ad %s",
            "--date=short",
        ]
    )

    if status.returncode != 0 or log.returncode != 0:
        detail = status.stderr.strip() or log.stderr.strip() or "git unavailable"
        return "unavailable", f"# Git Recent Commits\n\nGit summary unavailable: {detail}\n"

    body = [
        "# Git Recent Commits",
        "",
        f"Generated at: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "",
        "## Working Tree Status",
        "",
        "```text",
        status.stdout.strip() or "clean",
        "```",
        "",
        "## Recent Commits",
        "",
        "```text",
        log.stdout.strip() or "no commits",
        "```",
        "",
    ]
    return "ready", "\n".join(body)


def build_context_readme(profile: Profile, files: list[Path], git_status: str) -> str:
    rel_files = [str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in files]
    preview = "\n".join(f"- `{item}`" for item in rel_files[:12])
    if len(rel_files) > 12:
        preview += f"\n- ... 另有 {len(rel_files) - 12} 个文件"

    lines = [
        "# Tabbit AgentNexus Context Pack",
        "",
        f"- Profile: `{profile.name}`",
        f"- Description: {profile.description}",
        f"- Generated at: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Git summary: {git_status}",
        "",
        "## Recommended Reading Order",
        "",
        "1. `_context_pack/README.md`",
        "2. `_context_pack/manifest.json`",
        "3. `_context_pack/GIT_RECENT_COMMITS.md`",
        "4. `readme.md`",
        "5. `AGENTS.md`",
        "6. `docs/architecture/nexus_runtime_architecture.md`",
        "7. `docs/architecture/tabbit_browser_agent_behavior_boundary.md`",
        "8. `docs/workflows/README_workflows.md`",
        "9. `docs/workflows/bounded_agent_dialogue.md`",
        "10. `config/` + `scripts/` + `tests/`",
        "",
        "## Included File Preview",
        "",
        preview,
        "",
        "## Default Exclusions",
        "",
        "- `.git/`",
        "- `reference/`",
        "- `exports/`",
        "- `discuss/archive/`",
        "- `__pycache__/`",
        "- `*.zip` / `*.pyc` / `*.pyo`",
        "",
    ]
    return "\n".join(lines)


def build_manifest(profile: Profile, files: list[Path], git_status: str, zip_path: Path) -> dict:
    included = []
    for path in files:
        rel = path.relative_to(REPO_ROOT)
        included.append(
            {
                "path": str(rel).replace("\\", "/"),
                "bytes": path.stat().st_size,
            }
        )

    return {
        "title": "Tabbit AgentNexus Context Pack",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "profile": profile.name,
        "description": profile.description,
        "repo_root": str(REPO_ROOT),
        "zip_path": str(zip_path),
        "git_summary_status": git_status,
        "default_exclusions": sorted(EXCLUDED_PARTS)
        + ["discuss/archive"]
        + sorted(EXCLUDED_SUFFIXES),
        "included_files": included,
    }


def resolve_output_path(output_dir: Path, explicit_output: Path | None, profile: Profile) -> Path:
    if explicit_output is not None:
        return explicit_output
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"agent_nexus_context_{profile.name}_{timestamp}.zip"


def package_repo(profile: Profile, output_path: Path, git_commits: int) -> dict:
    files = expand_includes(profile.include)
    git_status, git_summary = build_git_summary(git_commits)
    readme_text = build_context_readme(profile, files, git_status)
    manifest = build_manifest(profile, files, git_status, output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(str(CONTEXT_DIR / "README.md"), readme_text)
        zf.writestr(
            str(CONTEXT_DIR / "manifest.json"),
            json.dumps(manifest, ensure_ascii=False, indent=2),
        )
        zf.writestr(str(CONTEXT_DIR / "GIT_RECENT_COMMITS.md"), git_summary)
        for path in files:
            arcname = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            zf.write(path, arcname=arcname)

    return {
        "zip_path": output_path,
        "profile": profile.name,
        "description": profile.description,
        "file_count": len(files),
        "git_summary_status": git_status,
        "manifest_path": f"{CONTEXT_DIR.as_posix()}/manifest.json",
        "readme_path": f"{CONTEXT_DIR.as_posix()}/README.md",
        "git_summary_path": f"{CONTEXT_DIR.as_posix()}/GIT_RECENT_COMMITS.md",
        "excluded": [
            ".git/",
            "reference/",
            "exports/",
            "discuss/archive/",
            "__pycache__/",
            "*.zip",
            "*.pyc",
            "*.pyo",
        ],
    }


def print_summary(result: dict) -> None:
    excluded = " / ".join(result["excluded"])
    print("已生成 AgentNexus context pack:")
    print(f"- 路径: {result['zip_path']}")
    print(f"- 配置: {result['profile']}")
    print(f"- 描述: {result['description']}")
    print(f"- 文件数: {result['file_count']}")
    print(f"- README: {result['readme_path']}")
    print(f"- Manifest: {result['manifest_path']}")
    print(f"- Git 摘要: {result['git_summary_status']} ({result['git_summary_path']})")
    print(f"- 默认排除: {excluded}")


def main() -> int:
    args = parse_args()
    profile = PROFILES[args.profile]
    output_path = resolve_output_path(args.output_dir, args.output, profile)
    result = package_repo(profile, output_path, args.git_commits)
    print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
