# Bridge multi-role collaboration workflow

> Status: completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: bridge-default

## Summary

把当前 bridge 开发中实际存在的 4 个角色沉淀成明确协作模型，说明每个角色的职责边界、默认任务分配、交接产物与推进节奏，减少多 agent 场景下的职责漂移与重复劳动。

## Scope

### In scope

- 明确 4 个角色在当前仓库语境下的职责边界：
  - 用户
  - 网页 GPT
  - Tabbit agent
  - 仓库代码 agent
- 为需求收敛、架构/spec、仓库实现、测试反馈、最终验收建立默认推进流程。
- 为不同类型任务建立默认路由与交接物。
- 把稳定结论同步到正式入口、workflow 入口与 repo-local skill。

### Out of scope

- 不改变既有 runtime boundary、权限模型或 M1-M5 路线。
- 不把网页 GPT 或 Tabbit agent 升级为本地代码写入者。
- 不讨论浏览器自动化细节、selector 策略或新的 bridge protocol。

## Current Context

- 当前已知事实：
  - 仓库已经收敛到 `E2B sandbox + mounted local folder + browser page automation` 基线。
  - `M1 Repo Review Bridge` 已补齐前置契约，并已落地第一批 sandbox-side 可测试核心。
  - 实际开发过程中已经稳定出现 4 个协作角色，但当前正式文档尚未把这些角色的职责和任务分配写清。
- 相关正式入口：
  - `readme.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/README_workflows.md`
  - `docs/workflows/agent_conventions.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
  - `docs/architecture/tabbit_browser_agent_behavior_boundary.md`

## Requirements

- `R1`: 正式文档必须明确 4 个角色的职责边界、主责任务和非职责范围。
- `R2`: workflow 必须明确不同阶段由哪个角色主责推进，哪些角色提供反馈或验收。
- `R3`: 对于常见任务类型，仓库内必须有一份可直接复用的默认任务路由表。
- `R4`: 新约定必须保持当前真值层级，不把一次性执行细节写成长期规则。
- `R5`: 若新增稳定 workflow，必须同步 `docs/workflows/README_workflows.md` 与对应 `.agent/skills/` 入口。

## Design

- `D1`: 在 `readme.md` 和正式架构入口中只保留简洁的角色模型与推进原则，避免把操作手册塞进总入口。
- `D2`: 在 `docs/workflows/` 新增一份专门的多角色协作文档，写清阶段流、任务路由、交接物和升级条件。
- `D3`: 在 `.agent/skills/` 增加对应 workflow skill，让未来 agent 在遇到多角色协作问题时能先读到这一套路由。
- `D4`: 在 `docs/PROJECT_MEMORY.md` 沉淀“4 角色协作模型是当前默认推进方式”这一 durable decision。
- `D5`: 在 `discuss/` spec 中保留本次实施记录，并同步索引状态。

### Behavior Specs

```text
Given: 用户提出一个 bridge 开发任务
When: 任务进入需求和验收定义阶段
Then: 用户负责确认目标、边界、优先级和最终验收口径，而不是把这些决策默认转交给网页 GPT 或仓库 agent。
```

```text
Given: 需要产出架构建议、spec 收敛或中途 review 反馈
When: 网页 GPT 参与当前任务
Then: 它默认承担架构 reviewer / feedback provider 角色，而不是本仓库的主实现者。
```

```text
Given: 需要验证 bridge 产物在 Tabbit 侧是否可用
When: 任务进入使用侧验证阶段
Then: Tabbit agent 默认承担使用者测试与行为反馈角色，而不是正式真值文档的唯一制定者。
```

```text
Given: 任务需要修改仓库文件、脚本、测试或正式文档
When: 进入实际实现阶段
Then: 仓库代码 agent 默认承担主实现责任，并负责把实现、验证和提交收口到仓库内。
```

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `readme.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/README_workflows.md`
  - new workflow doc under `docs/workflows/`
  - new repo-local skill under `.agent/skills/`
  - `discuss/README_discuss.md`
  - `docs/CHANGELOG.md`
- 明确不会碰哪些部分：
  - 不改 sandbox 脚本行为
  - 不改 browser adapter 契约
  - 不改变 M1 scope 本身

## Execution Plan

- [x] `T1`: 创建并回填本次多角色协作 workflow spec。
- [x] `T2`: 更新正式入口，加入 4 角色协作模型与推进原则。
- [x] `T3`: 新增 workflow 文档，明确任务路由、阶段分工、交接产物和升级条件。
- [x] `T4`: 新增 repo-local skill 入口，并同步 workflow 索引。
- [x] `T5`: 更新 changelog、discuss 索引和 durable memory。
- [x] `T6`: 运行最小验证并记录实施结果。

## Validation

- `V1`: `python -m py_compile <edited_python_files>`，若新增或修改 repo-local 脚手架脚本。
- `V2`: `git diff --stat` 确认只修改预期文档与 skill 入口。
- `V3`: `Get-Content` 或 `rg` spot-check 关键入口是否都出现新的角色模型与路由说明。

## Implementation Report

### Completed

- 创建本次 discuss spec，并收敛为多角色协作 workflow 变更。
- 更新 `readme.md`、正式架构入口和 `PROJECT_MEMORY`，把 4 角色协作模型升级为正式口径。
- 新增 `docs/workflows/multi_role_collaboration.md` 与 `.agent/skills/bridge-multi-role-collaboration/`。
- 同步 workflow 索引、discuss 索引和 changelog。
- 通过关键字段命中检查与 diff/stat 检查，确认入口之间已联通。

### Not completed

- 无。

### Notes

- 这次变更的目标是让角色分工可复用、可追踪，不是增加新的运行时能力。
- 任务路由是默认协作模型；若未来角色发生变化，应优先更新 workflow 文档和正式架构入口。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否。当前是 bridge 协作模型收口，不是 repo-wide 强制新禁令。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：是。4 角色协作模型属于 durable workflow fact。
- 是否需要更新 `docs/CHANGELOG.md`：是。需要记录新的协作 workflow 与任务路由约定。
