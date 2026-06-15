from __future__ import annotations

import argparse
import json
from pathlib import Path


def discover_repo(repo_root: Path) -> dict[str, object]:
    resolved = repo_root.resolve(strict=False)
    return {
        "repo_root": str(repo_root),
        "resolved_repo_root": str(resolved),
        "exists": repo_root.exists(),
        "is_dir": repo_root.is_dir(),
        "git_dir_present": (repo_root / ".git").exists(),
        "path_parts": list(resolved.parts),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the mounted repo root for N1 local workspace review runs.")
    parser.add_argument("--repo-root", type=Path, required=True, help="Mounted repo root to inspect.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(discover_repo(args.repo_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
