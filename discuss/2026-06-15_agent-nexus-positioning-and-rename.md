# AgentNexus positioning and rename

> Status: completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: nexus-default

## Summary

把当前仓库从以 `Bridge / repo review` 为中心的正式定位，迁移为以 `AgentNexus / 多智能体协作枢纽` 为中心的正式定位，并同步入口文档、workflow、skills、脚本命名和 active discuss 说明。

## Scope

### In scope

- 更新 `readme.md`、`AGENTS.md`、`docs/PROJECT_MEMORY.md`、`docs/CHANGELOG.md` 和 `docs/README_docs.md`
- 新增 `docs/architecture/nexus_runtime_architecture.md`
- 新增 `docs/workflows/bounded_agent_dialogue.md`
- 更新 workflow 索引、multi-role workflow 和 discuss spec workflow
- 将 repo-local skills 和 context pack script 迁移到 `nexus-*` 命名
- 标注 `Bridge` 为内部 adapter，`M1 Repo Review Bridge` 为历史名称 / 迁移 scenario

### Out of scope

- 实现 browser adapter 端到端实测
- 扩展多站点自动化
- 引入自动 patch apply 或 validation command 执行

## Current Context

- 当前已知事实：
  - 仓库名已经是 `Tabbit-AgentNexus`，但 active docs / skills / scripts 仍大量使用 `Bridge` 命名。
  - 当前已接受的基础包括 runtime boundary、repo review context pack、secret redaction、policy、audit 和 4 角色协作。
  - 当前缺少把多轮协作、共识/分歧汇报和 bounded unattended collaboration 作为一等公民的正式文档入口。
- 相关正式入口：
  - `readme.md`
  - `AGENTS.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/README_workflows.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
  - `discuss/2026-06-15_bridge-multi-role-collaboration-workflow.md`
  - `discuss/2026-06-15_bridge-positioning-sync-web-gpt-tabbit-usability.md`

## Requirements

- `R1`: 项目总定位必须升级为 `Tabbit AgentNexus`，并明确 `Bridge` 只是内部 adapter / transport pattern。
- `R2`: 正式架构入口必须切换到 `docs/architecture/nexus_runtime_architecture.md`。
- `R3`: roadmap 必须从 `M1-M5` 迁移到 `N0-N7` 或等价的 AgentNexus 命名。
- `R4`: 必须新增 bounded multi-round dialogue 的正式 workflow，并定义共识、分歧、停止条件和人工确认点。
- `R5`: repo-local skills、spec 默认 profile 和 context pack script 的命名必须同步迁移到 `nexus-*`。

## Design

- `D1`: 保留 `docs/architecture/bridge_runtime_architecture.md` 作为兼容入口，但把真值迁移到新增的 `nexus_runtime_architecture.md`。
- `D2`: 把 `repo-review` 视为 AgentNexus 的第一个 scenario adapter，并在 active discuss 索引和 M1 spec 中标注 `Former name`。
- `D3`: 新增 `bounded_agent_dialogue.md`，把多轮协作的 round handoff、stop conditions 和最终报告格式固化下来。
- `D4`: skill 和脚手架采用 `nexus-*` 命名；对外文案统一改为 `AgentNexus context pack`。

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `readme.md`
  - `AGENTS.md`
  - `docs/architecture/`
  - `docs/workflows/`
  - `docs/PROJECT_MEMORY.md`
  - `docs/CHANGELOG.md`
  - `.agent/skills/`
  - `scripts/tools/`
  - `discuss/`
- 明确不会碰哪些部分：
  - `config/`、`tests/` 的业务行为逻辑
  - browser adapter 的实际运行实现
  - `reference/` 和 archive 中的历史材料正文

## Execution Plan

- [x] `T1`: 创建 discuss spec，并确认需要同步的正式入口、workflow、skills 和脚手架。
- [x] `T2`: 新增 AgentNexus 正式架构入口，并保留 bridge 兼容说明。
- [x] `T3`: 更新 readme、AGENTS、PROJECT_MEMORY、workflow 索引和 docs map。
- [x] `T4`: 新增 bounded dialogue workflow，并同步 multi-role collaboration 的 round-based 补充。
- [x] `T5`: 将 repo-local skills 和 context pack script 迁移到 `nexus-*` 命名。
- [x] `T6`: 更新 active discuss 索引和 M1 spec 的历史名称 / 迁移定位说明。
- [ ] `T7`: 运行帮助命令、编译、测试和 context pack 验证。

## Validation

- `V1`: `git diff --stat`
- `V2`: `python -m py_compile scripts/tools/new_discuss_spec.py scripts/tools/package_nexus_context.py`
- `V3`: `python scripts/tools/new_discuss_spec.py --help`
- `V4`: `python scripts/tools/package_nexus_context.py --help`
- `V5`: `python scripts/tools/package_nexus_context.py --profile overview`
- `V6`: `python -m pytest -q`

## Implementation Report

### Completed

- 创建并回填本次定位迁移 spec。
- 新增 `docs/architecture/nexus_runtime_architecture.md` 作为正式架构真值入口。
- 新增 `docs/workflows/bounded_agent_dialogue.md`，并更新 workflow / skills / docs map。
- 将 active skills 和 context pack 脚本迁移到 `nexus-*` 命名。
- 同步 readme、AGENTS、PROJECT_MEMORY、CHANGELOG 和 discuss 索引，使 `Bridge` 降级为内部 adapter，`repo-review` 降级为首个 scenario。

### Not completed

- browser adapter 的真实端到端实测仍未覆盖。
- 历史 archive 中的原始 bridge 讨论材料仅保留为历史参考，未做全文重写。

### Notes

- 这次迁移以“真值入口改向 + active workflow 改名 + 历史兼容说明”为主，没有重写测试核心或 sandbox 行为实现。
- 若后续要推进 N2/N3，应直接围绕 `bounded_agent_dialogue.md` 和 `nexus_runtime_architecture.md` 继续收敛，而不是回到 bridge-only 术语。

## Durable Sync

- 是否需要更新 `AGENTS.md`：是，已更新 trigger、真值入口和仓库目标。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：是，已同步 AgentNexus durable facts 和 bounded dialogue baseline。
- 是否需要更新 `docs/CHANGELOG.md`：是，已记录本次定位升级和命名迁移。
