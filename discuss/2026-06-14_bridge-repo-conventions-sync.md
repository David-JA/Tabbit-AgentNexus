# Bridge repo conventions sync

> Status: completed
> Created: 2026-06-14
> Spec type: workflow
> Profile: bridge-default

## Summary

把参考科研仓库中跨项目也通用的协作约定，轻量同步到当前 Tabbit bridge 开发仓库，并完成第一次提交。

## Scope

### In scope

- 提炼 BDD / Given-When-Then 约定
- 提炼阶段报告与 commit message 风格
- 提炼文档放置、命名、discuss 维护等轻量 convention
- 以 bridge 仓库为目标，新增最小正式入口并完成首个 commit

### Out of scope

- 不同步科研仓库中的科学真值链、实验命名和数据处理规则
- 不在本任务中实现 M1 bridge 脚本

## Current Context

- 当前已知事实：当前仓库已完成第一轮轻量 harness 初始化，但还缺少 `agent_conventions`、`reports`、`discuss index` 这些更偏协作层的通用约定。
- 相关正式入口：`AGENTS.md`、`readme.md`、`docs/architecture/bridge_runtime_architecture.md`、`docs/workflows/README_workflows.md`
- 相关讨论或参考：`discuss/archive/tabbit-gpt-bridge-final-architecture-v4.md`、参考仓库 `docs/workflows/agent_conventions.md`

## Requirements

- `R1`: 只同步跨项目也成立的 convention，不把科研专用口径照搬进来。
- `R2`: 新增的 convention 必须有正式入口，并能被未来 agent 直接复用。
- `R3`: 本轮完成后仓库应具备可接受的首个提交边界。

## Design

- `D1`: 新增 `docs/workflows/agent_conventions.md` 作为低频稳定操作细则入口。
- `D2`: 新增 `docs/reports/README_reports.md` 与 `discuss/README_discuss.md`，把报告层和草稿层补齐。
- `D3`: 只对现有入口做最小同步，不扩展到实现代码层。

## Expected Diff Shape

- 预计会改哪些目录或文件：`AGENTS.md`、`readme.md`、`docs/`、`discuss/`、`.gitignore`
- 明确不会碰哪些部分：`reference/` 原始参考材料，不新增 bridge 运行时代码

## Execution Plan

- [x] `T1` 读取参考 convention 与相关入口，提炼可迁移部分
- [x] `T2` 新增轻量 `agent_conventions`、`reports`、`discuss` 入口
- [x] `T3` 同步现有正式入口与 memory/changelog
- [x] `T4` 验证并完成首个提交

## Validation

- `V1`: `python -m py_compile scripts/tools/new_discuss_spec.py`
- `V2`: `python scripts/tools/new_discuss_spec.py --help`
- `V3`: `git status --short --branch`

## Implementation Report

### Completed

- 新增 `docs/workflows/agent_conventions.md`，把阶段报告、BDD、commit、命名、PowerShell/sandbox 约定集中为一个稳定入口。
- 新增 `docs/reports/README_reports.md` 与 `discuss/README_discuss.md`，补齐 accepted 报告层和 discuss 索引入口。
- 更新 `AGENTS.md`、`readme.md`、`docs/README_docs.md`、`docs/workflows/README_workflows.md`、`docs/PROJECT_MEMORY.md`、`docs/CHANGELOG.md`，把新入口接入现有 harness。
- 新增 `.gitignore`，避免 Python 缓存噪声进入首次提交。

### Not completed

- 无

### Notes

- 本轮只同步“vibe coding 普适性”较强的 convention，未引入科研仓库中的项目真值链和归档治理复杂度。

## Durable Sync

- 是否需要更新 `AGENTS.md`：是，已更新
- 是否需要更新 `docs/PROJECT_MEMORY.md`：是，已更新
- 是否需要更新 `docs/CHANGELOG.md`：是，已更新
