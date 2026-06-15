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

## 2026-06-15

- 项目总定位升级为 `Tabbit AgentNexus`，并将 `Bridge` 降级为内部 adapter / transport pattern。
- 新增 `docs/architecture/nexus_runtime_architecture.md` 与 `docs/workflows/bounded_agent_dialogue.md`，正式引入 capability planes、bounded unattended collaboration、scenario adapters 和共识/分歧汇报流程。
- 同步 `readme.md`、`AGENTS.md`、`docs/PROJECT_MEMORY.md`、`docs/README_docs.md`、`docs/workflows/README_workflows.md`，把真值入口、roadmap 和 workflow 命名迁移到 AgentNexus。
- 将 repo-local skills 重命名为 `nexus-spec-workflow`、`nexus-memory-maintenance`、`nexus-context-packager`、`nexus-multi-role-collaboration`，并新增 `nexus-bounded-dialogue`。
- 将 `package_bridge_repo_context.py` 迁移为 `package_nexus_context.py`，输出 zip、manifest title、README reading order 和 profile 默认名同步改为 AgentNexus。
- 将 `M1 Repo Review Bridge` 重新定位为 `N1 Local Workspace Review Adapter` 的 `repo-review` scenario，并在 active discuss 索引中标记历史名称。

- 补齐 `M1 Repo Review Bridge` 前置实现契约：`M1 Runtime Contract`、`Browser Adapter Minimal Contract`、`send-to-AI confirmation gate`、context caps 与核心验证矩阵。
- 落地首批可测试的 sandbox-side 核心：`config/default_policy.review_only.json`、`discover_repo.py`、`git_probe.py`、`policy.py`、`redact.py`、`context_packager.py`、`audit_log.py`。
- 新增对应 fixtures 与单元测试骨架，用于验证路径策略、secret redaction、context packaging、git graceful degradation 与 audit 落盘。
- 新增 4 角色协作 workflow：明确用户、网页 GPT、Tabbit agent、仓库代码 agent 的职责边界、默认任务路由和交接规则。（后于同日修正为双 Agent 核心协作环，见下条。）
- 修正 AgentNexus 默认协作模型：从“四角色并列协作”收敛为 `Web Agent ↔ Browser Agent / Tabbit Agent` 的核心双 Agent 协作环；`Repo / Code Agent` 调整为可选外部执行端，并新增正式报告做 supersession 收口。
- 同步项目基本定位：明确该仓库是在 AI 浏览器新架构下，为用户低成本调用网页端高性能 AI 而开发 bridge 中枢；当前主要网页端适配目标是 GPT，并要求实现同时考虑网页端 GPT 与 Tabbit agent 的需求和易用性。
- 修正 `bridge_repo_context` 的 `overview` 打包逻辑：默认纳入 `config/`、`scripts/`、`tests/`，确保网页 AI 评审包同时覆盖脚本、配置、测试和文档。
- 根据验收反馈完成 active 文档术语 cleanup，清掉 AgentNexus 定位迁移后的残留旧称。
- 将 `2026-06-15_agent-nexus-positioning-and-rename.md` 转入 `discuss/archive/`，作为定位迁移内容验收与正式收口记录保留。
- 新增 `scripts/n1_review_session.py`，把 N1 `repo-review` local dry run 收口为统一入口：创建 `context_pack.md`、`audit.jsonl`、`session_summary.json` 并默认停在 `ready_to_send`。
- 新增 `.agent/skills/nexus-local-workspace-review/`，明确 N1 local-only 执行顺序、review request 模板和 browser adapter handoff 边界。
- 新增 runner 级测试与 `tests/conftest.py`，覆盖 artifact fallback、no-git、denied-only、secret redaction 和 `no_write_repo`，同时修复裸跑 `pytest -q` 的导入稳定性。
- 将 sandbox-side 用户可见文案从 `M1 bridge` 收口为 `N1 Local Workspace Review` / `AgentNexus review-only`，并同步 discuss 索引与 active N1 spec 状态。
- 将两份 accepted Tabbit probe report 的稳定结论升级为 architecture boundary：补充 browser workspace / tab control 边界，并在 `nexus_runtime_architecture.md` 新增 Tabbit skill runtime and distribution plane。
- 同步 `docs/PROJECT_MEMORY.md`，沉淀 Tabbit skill 双运行时 / 双形态分发边界，以及 browser workspace 的真实 tab 寻址限制。
- 补充 architecture → report 的反向引用，并收紧 browser workspace report 中“已知 ID 标签页”表述；同时统一本轮涉及 Markdown 的换行风格，减少后续 diff 噪声。
