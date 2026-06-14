from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "docs" / "workflows" / "discuss_spec_template.md"
DISCUSS_DIR = REPO_ROOT / "discuss"


def slugify(text: str) -> str:
    normalized = text.strip().lower()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"[\s_-]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized or "discuss-spec"


def build_output_path(slug: str) -> Path:
    date_prefix = dt.date.today().isoformat()
    return DISCUSS_DIR / f"{date_prefix}_{slug}.md"


def render_template(title: str, spec_type: str, profile: str) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": title,
        "{{DATE}}": dt.date.today().isoformat(),
        "{{TYPE}}": spec_type,
        "{{PROFILE}}": profile,
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new discuss spec from the repo template."
    )
    parser.add_argument("--title", required=True, help="Human-readable spec title.")
    parser.add_argument(
        "--slug",
        help="Optional file slug. Defaults to a slug derived from title.",
    )
    parser.add_argument(
        "--type",
        default="workflow",
        help="Spec type label written into the template.",
    )
    parser.add_argument(
        "--profile",
        default="bridge-default",
        help="Profile label written into the template.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the target file if it already exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slug = slugify(args.slug or args.title)
    output_path = build_output_path(slug)

    DISCUSS_DIR.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not args.force:
        raise SystemExit(
            f"Refusing to overwrite existing spec: {output_path}. Use --force to replace it."
        )

    content = render_template(args.title, args.type, args.profile)
    output_path.write_text(content, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
