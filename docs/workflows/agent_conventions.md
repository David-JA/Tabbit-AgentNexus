# Agent Conventions

## 1. Scope

本文档承接低频但稳定的 agent 协作细则，避免把 `AGENTS.md` 膨胀成一本操作手册。

本文覆盖：

- 阶段报告风格
- BDD / Given-When-Then 书写
- commit message 风格
- 文档放置与命名
- discuss 文档状态维护
- 代码风格与注释
- PowerShell / sandbox 使用习惯
- 轻量 review checklist

本文不承担：

- bridge 架构真值
- 运行边界定义
- session policy 设计本身

这些内容仍以 `AGENTS.md` 和 `docs/architecture/bridge_runtime_architecture.md` 为准。

## 2. Stage Report Convention

完成一轮可交付工作后，默认按以下格式提供阶段报告；不适用项明确写 `无`：

- `已实现：`
- `已自动验证：`
- `需要用户验证：`
- `已知限制：`
- `下一步：`

约束：

- `已自动验证` 只写本轮真实跑过的自动检查。
- `需要用户验证` 只写必须依赖用户、浏览器状态或外部环境的确认。
- 不要把自动验证、人工验证和未来计划混成一段。

## 3. Behavior First / BDD Convention

非平凡行为修改默认先写 Given-When-Then，再实现。

格式：

```text
Given: 当前 repo / session / page / policy 处于什么状态
When: agent、skill、script 或用户执行什么动作
Then: 系统应允许、拒绝、记录、提示或产出什么结果
```

适用建议：

- bug fix：最少写出失败行为和预期结果
- workflow / policy / protocol 修改：至少写 2-4 条核心 GWT
- 高风险任务：把 GWT 写进 discuss spec，而不是只留在脑中

## 4. Commit Convention

### 提交边界

当范围清晰、验证完成、没有明显无关改动时，agent 可以直接提交。
若提交范围或验收标准不清晰，先和用户对齐。

### Commit message 风格

默认采用下面的结构；标题和条目内容默认使用简体中文，固定小节名 `Validation:` 与 `Limitations:` 可保留英文：

```text
<scope>: <用动词概括本次变更>

- <关键实现 1>
- <关键实现 2>
- <关键实现 3>

Validation:
- <自动验证 1>
- <自动验证 2>

Limitations:
- <与本提交直接相关的限制，可省略整节>
```

不要把以下内容写进 commit message：

- `Needs user validation`
- `Next step`
- 当前工作区状态
- 完整阶段报告原文

## 5. Documentation Placement and Naming

### 放置规则

- 正式接受的内容写入 `docs/`
- accepted 报告写入 `docs/reports/`
- 草稿、spec、审计、评审记录写入 `discuss/`
- durable 结论不要只留在 `discuss/`

### 命名规则

- 根目录正式入口保留为小写 `readme.md`
- 子目录入口优先使用 `README_<scope>.md`
- discuss spec 默认使用 `YYYY-MM-DD_<slug>.md`
- Python 代码默认使用：
  - 函数/变量：`snake_case`
  - 类：`PascalCase`
  - 常量：`UPPER_SNAKE_CASE`

## 6. Discuss Maintenance

如果 `discuss/` 下的文档包含可执行计划，建议维护：

- `Status`
- `Execution Plan`
- `Validation`
- `Implementation Report`

如果存在目录级索引文件，例如 `discuss/README_discuss.md`，应同步更新状态，不要让索引和正文长期漂移。

推荐的执行状态总览格式：

```markdown
> **执行状态总览**（截至 YYYY-MM-DD）
>
> | 阶段 | 状态 |
> |---|---|
> | Phase 1 | ✅ 已完成 |
> | Phase 2 | ⚠️ 进行中 |
```

## 7. Code Style and Comments

- 优先遵循周围文件现有风格。
- 不要为了“整洁”做大规模无关格式 churn。
- 注释优先解释为什么这么做，而不是复述代码表面行为。
- Markdown 和规则文档默认使用简体中文；代码注释可跟随文件现有语言。

## 8. PowerShell / Sandbox Notes

- 在 Windows PowerShell 环境下，先区分仓库问题和沙箱问题。
- 简单只读命令优先保持简单，不要堆过多 shell 技巧。
- 若并行命令出现环境噪声或失败，优先退回顺序执行。
- 若关键命令确实被沙箱限制，应请求提权，而不是发明奇怪 workaround。

## 9. Lightweight Review Checklist

做实现复核时，优先检查：

1. 行为边界是否更清晰了，而不是更模糊了。
2. 正式入口和草稿入口是否放对地方了。
3. 新约定是否能被未来 agent 直接复用。
4. 自动验证是否匹配本次真实改动。
5. 文档是否和代码/脚手架保持一致。
