---
name: bridge-spec-workflow
description: 为当前 Tabbit bridge 仓库的非平凡任务创建和维护单文件 discuss spec。适用于 protocol、policy、安全边界、browser/sandbox 职责划分、repo-local skill 或多文件实现方案变更。
compatibility: 需要能读取当前仓库中的 AGENTS.md、readme.md、docs/architecture/bridge_runtime_architecture.md、docs/workflows/agent_conventions.md、docs/workflows/discuss_spec_workflow.md、docs/workflows/discuss_spec_template.md 和 scripts/tools/new_discuss_spec.py。
---

# Bridge Spec Workflow

## 目标

这个 skill 只负责把“复杂任务先写成可执行 spec”这件事做规范。
它不替代正式架构文档，也不替代最终实现。

## 使用前必读

在采取动作前，先读取：

1. `AGENTS.md`
2. `readme.md`
3. `docs/architecture/bridge_runtime_architecture.md`
4. `docs/workflows/agent_conventions.md`
5. `docs/workflows/discuss_spec_workflow.md`
6. `docs/workflows/discuss_spec_template.md`

## 何时触发

出现以下任一情况时应触发：

- 非平凡多文件任务
- bridge protocol / session policy / trust model 变化
- browser-side harness 与 sandbox-side script 的职责重划
- `.agent/skills/` 新增或重构
- 需要明确记录 requirements、design、validation 和 durable sync

## 默认创建方式

```powershell
python scripts/tools/new_discuss_spec.py `
  --title "<task title>" `
  --slug "<short-slug>" `
  --type workflow `
  --profile bridge-default
```

## 填写规则

- 保留模板章节，不要删掉 `Validation`、`Implementation Report`、`Durable Sync`。
- 开始实现前先写 `Requirements` 和 `Design`。
- 实施过程中同步勾选 `Execution Plan`。
- 停止前回填实际验证和完成状态。

## 结束条件

只有在以下信息已回填时，这次 spec 才算完成：

- 完成项
- 未完成项
- 实际验证
- 已知限制
- 是否需要同步到 `AGENTS.md`、`docs/PROJECT_MEMORY.md`、`docs/CHANGELOG.md`
