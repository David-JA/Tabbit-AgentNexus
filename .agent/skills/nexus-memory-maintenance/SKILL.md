---
name: nexus-memory-maintenance
description: 为当前 Tabbit AgentNexus 仓库分流已接受的规则、durable decision 和变更摘要。适用于需要判断信息应写入 AGENTS、PROJECT_MEMORY、CHANGELOG、正式架构入口还是继续留在 discuss 的场景。
compatibility: 需要能读取当前仓库中的 AGENTS.md、readme.md、docs/README_docs.md、docs/PROJECT_MEMORY.md、docs/CHANGELOG.md 和 docs/architecture/nexus_runtime_architecture.md。
---

# Nexus Memory Maintenance

## 目标

这个 skill 解决“某条信息最终应该写到哪里”的问题。
目标是最小分流，而不是把同一段话复制到所有文件。

## 核心分流

| 信息类型 | 落点 |
|----------|------|
| 当前默认规则、禁令、协作边界 | `AGENTS.md` |
| 长期有效的接受结论 | `docs/PROJECT_MEMORY.md` |
| 面向人的变更摘要 | `docs/CHANGELOG.md` |
| 当前正式架构口径 | `docs/architecture/bridge_runtime_architecture.md` |
| 仍在讨论中的方案 | `discuss/` |
| 可复用 agent 流程 | `.agent/skills/` 或 `docs/workflows/` |

## 使用时机

- 某项 AgentNexus 结论已经被接受
- 某项 workflow 已经稳定
- 需要判断一个实现结果是否应升级为 durable memory
- 需要在任务完成后做收口

## 维护原则

- 未接受的内容不要提前写进 durable memory。
- `PROJECT_MEMORY` 只记长期有效事实，不写流水账。
- `CHANGELOG` 只写对人有意义的变化摘要。
- 如果行为边界变了，优先同步 `readme.md` 和正式架构入口。
