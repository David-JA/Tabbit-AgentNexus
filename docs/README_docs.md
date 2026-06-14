# Docs Map

`docs/` 只放正式入口，不承接一次性讨论稿。

## 分层约定

| 内容类型 | 落点 |
|----------|------|
| 当前项目概览 | `../readme.md` |
| bridge 正式架构 | `architecture/bridge_runtime_architecture.md` |
| durable memory | `PROJECT_MEMORY.md` |
| 面向人的变更摘要 | `CHANGELOG.md` |
| workflow 说明 | `workflows/` |
| accepted 报告 | `reports/README_reports.md` |
| 方案草稿与执行 spec | `../discuss/` |

## 当前正式入口

- 架构入口：`architecture/bridge_runtime_architecture.md`
- workflow 入口：`workflows/README_workflows.md`
- 协作约定入口：`workflows/agent_conventions.md`
- 报告入口：`reports/README_reports.md`
- durable memory 入口：`PROJECT_MEMORY.md`

## 维护原则

- 正式入口保持短而稳，不把大段讨论稿原样搬过来。
- 可复用流程沉淀为 workflow 或 skill。
- 仍在争论中的内容继续留在 `discuss/`，不要提前写成 durable rule。
