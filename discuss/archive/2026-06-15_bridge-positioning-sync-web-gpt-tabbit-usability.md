# Bridge positioning sync for web GPT and Tabbit usability

> Status: completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: bridge-default

## Summary

把当前项目的基本定位明确写进仓库：这个项目是在 AI 浏览器新架构下，为用户低成本调用网页端高性能 AI 而开发一个中枢；当前网页端 AI 的主要适配目标是 GPT，而 Tabbit agent 既是中介也是副手，因此实现与 workflow 必须同时考虑网页端 GPT 和 Tabbit agent 的需求与易用性。

## Scope

### In scope

- 更新正式入口对项目目标的描述。
- 更新正式架构入口，明确网页端 GPT 与 Tabbit agent 都是设计对象。
- 更新 durable memory，记录“双端可用性”是当前默认产品定位。
- 按需更新协作 workflow，使其体现网页端 GPT 和 Tabbit agent 的易用性都应进入实现考量。
- 同步 discuss 索引与 changelog。

### Out of scope

- 不改变默认 runtime boundary。
- 不改变 M1-M5 路线。
- 不新增 browser adapter 或 sandbox runtime 能力。

## Current Context

- 当前已知事实：
  - 当前仓库已经明确了 4 角色协作模型，但对“为什么同时要服务网页端 GPT 与 Tabbit agent”仍缺少集中表述。
  - `readme.md` 当前强调的是 bridge skill 开发与安全边界，还没有把“低成本调用网页端高性能 AI”写成对外定位。
  - 正式架构入口已经说明页面交互通过浏览器 GUI 工具和临时 harness 完成，但尚未明确网页端 GPT 是当前主要适配目标，以及 Tabbit agent 是使用侧中介与副手。
- 相关正式入口：
  - `readme.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/multi_role_collaboration.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
  - `discuss/2026-06-15_bridge-multi-role-collaboration-workflow.md`

## Requirements

- `R1`: 正式入口必须明确本项目是在 AI 浏览器新架构下，为用户低成本调用网页端高性能 AI 而开发 bridge 中枢。
- `R2`: 正式架构必须明确当前网页端 AI 的主要适配目标是 GPT。
- `R3`: 正式文档必须明确 Tabbit agent 是桥接中的中介与副手，而不是可忽略的单纯执行器。
- `R4`: workflow 或 durable memory 必须明确：功能开发应同时考虑网页端 GPT 和 Tabbit agent 的需求与易用性。
- `R5`: 新表述不得削弱当前安全边界、用户确认和本地策略层职责。

## Design

- `D1`: 在 `readme.md` 中增加面向项目总目标的定位描述，强调“低成本调用网页端高性能 AI”。
- `D2`: 在正式架构入口中增加“产品定位与双端适配目标”小节，明确 GPT 是当前主要网页端适配目标，Tabbit agent 是中介与副手。
- `D3`: 在 `docs/PROJECT_MEMORY.md` 中增加 durable fact，说明“双端可用性”是当前默认产品约束。
- `D4`: 在 `docs/workflows/multi_role_collaboration.md` 中补一条实现原则，要求仓库实现同时考虑网页端 GPT 与 Tabbit agent 的易用性。

### Behavior Specs

```text
Given: 当前任务在设计 bridge 能力或交互流程
When: 仓库 agent、网页 GPT 或 Tabbit agent 提出方案
Then: 方案应同时考虑网页端 GPT 作为主要推理端的输入输出成本，以及 Tabbit agent 作为中介与副手的操作成本。
```

```text
Given: 某个实现只优化了网页端 GPT 的 prompt/上下文体验
When: 它明显增加了 Tabbit agent 的操作复杂度、失败率或维护成本
Then: 该实现不应被直接视为合格方案，而应继续收敛双端可用性。
```

```text
Given: 某个实现只优化了 Tabbit agent 的控制路径
When: 它显著降低了网页端 GPT 作为主要评审/推理目标的效果
Then: 该实现同样需要重新评估，而不是只看单端收益。
```

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `readme.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/multi_role_collaboration.md`
  - `discuss/README_discuss.md`
  - `docs/CHANGELOG.md`
- 明确不会碰哪些部分：
  - `AGENTS.md`
  - `scripts/`
  - `tests/`

## Execution Plan

- [x] `T1`: 创建并回填本次定位同步 spec。
- [x] `T2`: 更新 `readme.md`，明确项目总定位与 GPT/Tabbit 双端考量。
- [x] `T3`: 更新正式架构与 durable memory，沉淀双端适配目标。
- [x] `T4`: 更新协作 workflow、discuss 索引和 changelog。
- [x] `T5`: 运行关键字段检查并回填实施结果。

## Validation

- `V1`: `rg -n "网页端高性能 AI|主要适配目标是 GPT|中介与副手|双端可用性|网页端 GPT|Tabbit agent" <updated docs>`
- `V2`: `git diff --stat`

## Implementation Report

### Completed

- 更新 `readme.md`，把项目定位表述为 AI 浏览器新架构下的 bridge 中枢。
- 更新正式架构入口，明确网页端 GPT 是当前主要适配目标，Tabbit agent 是中介与副手。
- 更新 `docs/PROJECT_MEMORY.md` 和协作 workflow，加入双端可用性约束。
- 同步 discuss 索引和 changelog。

### Not completed

- 无。

### Notes

- 这次变更是定位同步与 workflow 收口，不涉及 runtime 能力扩展。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否。本次不新增 repo-wide 操作禁令。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：是。双端适配与双端可用性属于 durable 产品定位。
- 是否需要更新 `docs/CHANGELOG.md`：是。需要记录本次定位同步。
