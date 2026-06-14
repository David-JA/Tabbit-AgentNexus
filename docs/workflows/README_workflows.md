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
- `../../.agent/skills/bridge-spec-workflow/`

适用场景：

- 非平凡多文件改动
- bridge protocol / policy / security boundary 变更
- browser script 与 sandbox script 职责边界变化
- skill/harness 结构升级

### 3. Repo Memory Maintenance

入口：

- `../../.agent/skills/bridge-memory-maintenance/`

适用场景：

- 某项结论已经被接受，需要分流到 `AGENTS.md`、`docs/PROJECT_MEMORY.md`、`docs/CHANGELOG.md`
- 需要判断某段信息该留在 `discuss/` 还是沉淀成正式入口

## 设计原则

- workflow 文档只描述稳定做法，不承接一次性任务细节。
- 讨论文档仍然写进 `discuss/`，不要直接把草稿塞进 `docs/workflows/`。
