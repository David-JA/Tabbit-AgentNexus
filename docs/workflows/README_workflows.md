# Workflows

这里记录当前仓库已经接受的工程与 agent workflow。

## 当前可用流程

### 1. Agent Conventions

入口：

- `agent_conventions.md`

适用场景：

- 编写阶段报告
- 组织 Given-When-Then 行为约束
- 准备 commit message
- 维护 discuss 状态与文档命名
- 进行轻量 review 或 shell/sandbox 操作

### 2. Discuss Spec Workflow

入口：

- `discuss_spec_workflow.md`
- `discuss_spec_template.md`
- `../../scripts/tools/new_discuss_spec.py`
- `../../.agent/skills/nexus-spec-workflow/`

适用场景：

- 非平凡多文件改动
- AgentNexus protocol / policy / security boundary 变更
- browser script 与 sandbox script 职责边界变化
- skill/harness 结构升级

### 3. Repo Memory Maintenance

入口：

- `../../.agent/skills/nexus-memory-maintenance/`

适用场景：

- 某项结论已经被接受，需要分流到 `AGENTS.md`、`docs/PROJECT_MEMORY.md`、`docs/CHANGELOG.md`
- 需要判断某段信息该留在 `discuss/` 还是沉淀成正式入口

### 4. AgentNexus Context Packager

入口：

- `../../.agent/skills/nexus-context-packager/`
- `../../scripts/tools/package_nexus_context.py`

适用场景：

- 为外部 AI / 网页 AI 生成 AgentNexus 仓库理解包
- 做 handoff zip、repo overview bundle、外部评审上下文包
- 需要把正式入口、当前 spec、repo-local skills 和维护脚手架一起导出

### 5. Multi-Role Collaboration

入口：

- `multi_role_collaboration.md`
- `../../.agent/skills/nexus-multi-role-collaboration/`

适用场景：

- 用户、网页 GPT、Tabbit agent、仓库代码 agent 同时参与当前任务
- 需要明确谁主责需求、谁主责实现、谁负责反馈、谁做最终验收
- 需要为多角色协作建立默认任务路由和交接物

### 6. Bounded Agent Dialogue

入口：

- `bounded_agent_dialogue.md`
- `../../.agent/skills/nexus-bounded-dialogue/`

适用场景：

- 需要 round-based 多智能体协作
- 需要显式记录共识、分歧、风险和停止原因
- 需要把网页端高性能 Agent、Tabbit agent 和仓库代码 agent 的多轮交互收口成可执行报告

## 设计原则

- workflow 文档只描述稳定做法，不承接一次性任务细节。
- 讨论文档仍然写进 `discuss/`，不要直接把草稿塞进 `docs/workflows/`。
