# Stage Report Git Commit Trigger

> Status: Completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: nexus-default

## Summary

明确将阶段报告与 git 提交语义绑定，避免 agent 只遵循 commit message 规则、却漏掉阶段报告格式。

## Scope

### In scope

- 澄清阶段报告的默认触发时机
- 明确“可提交待确认”与“用户显式要求提交”两个场景下的 agent 输出要求
- 同步 workflow 入口说明，降低后续路由偏差

### Out of scope

- 修改 runtime boundary、权限模型或多角色主责分工
- 新增独立 workflow 文档或 repo-local skill
- 调整 commit message 模板本身

## Current Context

- 当前已知事实：`agent_conventions.md` 已定义阶段报告格式，但没有把触发条件明确绑定到 git 提交语义上。
- 相关正式入口：`AGENTS.md`、`docs/workflows/agent_conventions.md`、`docs/workflows/README_workflows.md`
- 相关讨论或参考：用户指出最近一次实际执行中，commit 风格被遵循，但阶段报告没有按约定给出。

## Requirements

- `R1`: 当 agent 判断当前工作已形成可提交变更集并准备征求是否提交时，应先按阶段报告格式给出总结。
- `R2`: 当用户显式要求 agent 执行 git 提交时，应将该动作视为阶段收口信号；提交完成后仍需按阶段报告格式汇报。
- `R3`: 规则应写在稳定 workflow 入口中，便于未来 agent 直接命中。

## Design

- `D1`: 在 `Stage Report Convention` 下新增“触发时机”小节，直接把阶段报告与 git 提交前后语义绑定。
- `D2`: 在 `README_workflows.md` 的 Agent Conventions 适用场景中补充一句，显式提示“进入可提交 / 请求提交 / 已提交语义时应输出阶段报告”。

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `docs/workflows/agent_conventions.md`
  - `docs/workflows/README_workflows.md`
  - `discuss/README_discuss.md`
  - 本 spec 文件
- 明确不会碰哪些部分：
  - `AGENTS.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/CHANGELOG.md`

## Execution Plan

- [x] `T1` 创建轻量 workflow spec，记录本次规则澄清
- [x] `T2` 更新 `agent_conventions.md`，明确阶段报告的 git 提交触发规则
- [x] `T3` 更新 workflow 入口与 discuss 索引

## Validation

- `V1`: 检查 `agent_conventions.md` 是否显式覆盖“可提交待确认”和“用户显式要求提交”两个触发场景
- `V2`: 检查 `README_workflows.md` 与 `discuss/README_discuss.md` 是否同步到位

## Implementation Report

### Completed

- 新增本次 workflow 澄清 spec
- 明确阶段报告与 git 提交语义绑定的规则
- 同步 workflow 入口与 discuss 索引

### Not completed

- 无

### Notes

- 此次调整是规则澄清，不是新增独立 workflow，也不改变 commit message 模板。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否
- 是否需要更新 `docs/PROJECT_MEMORY.md`：否
- 是否需要更新 `docs/CHANGELOG.md`：否
