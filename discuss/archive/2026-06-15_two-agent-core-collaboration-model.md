# Two-agent core collaboration model

> Status: completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: nexus-default

## Summary

把当前 AgentNexus 默认协作模型从“四角色并列常驻”修订为“Web Agent 与 Browser Agent / Tabbit Agent 构成核心双 Agent 协作环，Repo / Code Agent 作为可选外部执行端”。

## Scope

### In scope

- 修订正式入口中的默认协作模型表述。
- 同步 workflow、repo-local skills、durable memory 和 changelog。
- 新增一份 accepted report，作为本次架构修订的正式收口点。
- 同步 discuss 索引，说明旧四角色 workflow 仅保留为历史实现记录。

### Out of scope

- 不修改 runtime code、tests 或脚手架逻辑。
- 不修改 `N0-N7` roadmap。
- 不改变 `E2B sandbox + mounted local folder + browser page automation` baseline。
- 不改写 `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md` 正文。

## Current Context

- 当前已知事实：
  - 当前 checkout 为 `main@5a2eb28`，并已对齐 `origin/main`。
  - 当前正式入口仍把默认协作模型写成 4 个角色并列推进。
  - `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md` 已明确声明自己是交互记录，不替代正式真值。
  - 旧的四角色 workflow spec 已归档在 `discuss/archive/2026-06-15_bridge-multi-role-collaboration-workflow.md`。
- 相关正式入口：
  - `readme.md`
  - `docs/architecture/nexus_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/multi_role_collaboration.md`
  - `docs/workflows/bounded_agent_dialogue.md`
- 相关讨论或参考：
  - `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md`
  - `discuss/archive/2026-06-15_bridge-multi-role-collaboration-workflow.md`

## Requirements

- `R1`: 正式入口必须把默认协作模型改写为 `Web Agent ↔ Browser Agent / Tabbit Agent` 的核心双 Agent 协作环。
- `R2`: `Repo / Code Agent` 必须从默认对话环中移出，并明确为可选外部执行端。
- `R3`: workflow 和 repo-local skills 必须写清角色分工、任务路由、交接物和反模式。
- `R4`: transcript 继续保留为历史证据，但本次修订需要新增 accepted report 做正式收口。
- `R5`: 新表述不得削弱当前安全边界、用户授权要求或本地策略层职责。

## Design

- `D1`: 重写 `readme.md` 的“默认协作模型”段，并做最小必要的一致性补充。
- `D2`: 重构 `docs/architecture/nexus_runtime_architecture.md` 的 `Actor model`，区分核心协作 actor 与外部执行端 / adapter。
- `D3`: 用新的 durable memory 条目替换 `Multi-Role Collaboration Model`。
- `D4`: 把 `docs/workflows/multi_role_collaboration.md` 和 `docs/workflows/bounded_agent_dialogue.md` 统一改成双 Agent 核心模型。
- `D5`: 同步 `docs/workflows/README_workflows.md`、相关 skills、`docs/CHANGELOG.md`、`discuss/README_discuss.md` 和一份新 accepted report。

### Behavior Specs

```text
Given: 用户给出目标、优先级和授权边界
When: AgentNexus 进入默认协作流程
Then: 用户是决策与验收中心，而不是默认通信总线。
```

```text
Given: 任务需要架构设计、多轮推进策略、阶段汇报或监督
When: 协作进入高阶推理阶段
Then: Web Agent 默认承担主责，而不是仅作为外部 reviewer。
```

```text
Given: 任务需要真实浏览器操作、网页登录态上下文、E2B sandbox 执行、挂载目录操作或跨端转交
When: 协作进入执行与观察阶段
Then: Browser Agent / Tabbit Agent 默认承担主责，但涉及仓库操作时必须保持 Web Agent 监督与 git 可审计性。
```

```text
Given: 任务需要修改仓库、运行测试、整理 diff 或提交证据
When: 收到用户或 Browser Agent 转交的明确指令
Then: Repo / Code Agent 作为可选外部执行端参与，而不是默认对话环成员。
```

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `readme.md`
  - `docs/architecture/nexus_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/`
  - `.agent/skills/nexus-multi-role-collaboration/`
  - `.agent/skills/nexus-bounded-dialogue/`
  - `docs/reports/20260615_two_agent_core_collaboration_model.md`
  - `docs/CHANGELOG.md`
  - `discuss/README_discuss.md`
- 明确不会碰哪些部分：
  - `scripts/`
  - `tests/`
  - `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md`

## Execution Plan

- [x] `T1`：确认当前 checkout 与正式入口状态。
- [x] `T2`：创建本次 discuss spec，并写清 requirements、design 和 behavior specs。
- [x] `T3`：更新正式入口、workflow、repo-local skills 和 durable memory。
- [x] `T4`：新增 accepted report，并同步 changelog 与 discuss 索引。
- [x] `T5`：运行差异检查与新旧口径检查，并回填实施结果。

## Validation

- `V1`: `git status -sb`
- `V2`: `git rev-parse --abbrev-ref HEAD`
- `V3`: `git rev-parse --short HEAD`
- `V4`: `git diff --stat`
- `V5`: `git diff --check`
- `V6`: `rg -n "当前仓库默认按 4 个角色协作推进|默认存在的 4 个角色|用户、网页 GPT、Tabbit agent、仓库代码 agent 同时参与当前任务|When: Tabbit agent、Web Agent、仓库代码 agent 在任务中交换意见|Recommended Next Actions for Local Code Agent" readme.md docs .agent/skills -g "!docs/reports/transcripts/**"`
- `V7`: `rg -n "四角色|4 个角色|仓库代码 agent" docs/reports/transcripts discuss/archive`

## Implementation Report

### Completed

- 新建本次 discuss spec，并把它作为已接受默认协作模型的 superseding 修订记录。
- 把正式入口、workflow、repo-local skills 和 durable memory 改写为双 Agent 核心协作模型。
- 新增一份 accepted report，明确 transcript 是历史证据，正式真值看主入口文档。
- 同步 changelog 和 discuss 索引，避免旧四角色模型继续被读成当前默认状态。

### Not completed

- 无。

### Notes

- `AGENTS.md` 经检查未发现必须同步的新禁令或触发条件缺口，因此保持不改。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：是。默认协作模型属于长期有效事实。
- 是否需要更新 `docs/CHANGELOG.md`：是。需要给此次架构修订留下人类可读的变更摘要。
