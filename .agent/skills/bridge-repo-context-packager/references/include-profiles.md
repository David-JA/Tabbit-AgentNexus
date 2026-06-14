# Bridge Repo Context Pack Profiles

## `minimal`

适合：

- 用户只想把当前 bridge 仓库的正式入口和当前实现方向交给外部 AI
- 希望 zip 尽量小
- 不需要完整 reports 和全部 discuss 材料

包含：

- `readme.md`
- `AGENTS.md`
- `.gitignore`
- `docs/PROJECT_MEMORY.md`
- `docs/README_docs.md`
- `docs/architecture/*.md`
- `docs/workflows/*.md`
- `docs/reports/README_reports.md`
- `discuss/README_discuss.md`
- `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
- `.agent/skills/`
- `scripts/tools/package_bridge_repo_context.py`
- `scripts/tools/new_discuss_spec.py`

不包含：

- `docs/reports/*.md`
- `discuss/archive/`
- `reference/`
- `exports/`

## `overview`

适合：

- 用户要把当前 bridge 仓库完整交给外部 AI 快速理解
- 需要正式入口、reports、当前 discuss 和维护脚手架
- 需要看到 repo-local skills 的完整结构

包含：

- `readme.md`
- `AGENTS.md`
- `.gitignore`
- `docs/`
- `discuss/`
- `.agent/skills/`
- `scripts/tools/`

仍默认排除：

- `.git/`
- `reference/`
- `exports/`
- `__pycache__/`
- `*.zip` / `*.pyc` / `*.pyo`
- `discuss/archive/` 不会被自动特殊挑出；若后续需要纳入，应单独扩展脚本
