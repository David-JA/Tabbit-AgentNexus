# CHANGELOG

## 2026-06-14

- 初始化当前仓库的轻量 agent harness。
- 新增正式入口：`readme.md`、`AGENTS.md`、`docs/architecture/bridge_runtime_architecture.md`。
- 新增记忆与 workflow 骨架：`docs/PROJECT_MEMORY.md`、`docs/workflows/`。
- 新增 repo-local skills：`bridge-spec-workflow`、`bridge-memory-maintenance`。
- 新增 `scripts/tools/new_discuss_spec.py`，用于快速创建 discuss spec。
- 同步一批跨项目也通用的轻量协作约定：`docs/workflows/agent_conventions.md`、`docs/reports/README_reports.md`、`discuss/README_discuss.md`。
- 补充仓库级 `.gitignore`，忽略常见 Python 缓存与噪声文件。
- 新增 `docs/architecture/tabbit_browser_agent_behavior_boundary.md`，沉淀 Tabbit 浏览器 agent 的能力矩阵、操作纪律、路径语义与已知限制。
- 补充 Git 提交相关的 accepted 运维经验：明确 `safe.directory` 归因、提交前 Git 身份检查，并新增一份 `docs/reports/` 报告沉淀完整诊断过程。
- 新增 `bridge-repo-context-packager` skill 与 `package_bridge_repo_context.py`，用于把当前 bridge 仓库打成面向外部 AI 的理解包 zip。
