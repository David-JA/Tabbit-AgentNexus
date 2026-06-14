# Discuss Spec Workflow

这个 workflow 用于在非平凡任务开始前，为当前仓库创建一个单文件 discuss spec。

## 何时必须使用

满足任一条件时，建议先创建 spec：

- 任务影响多个文件，并且有设计取舍
- 修改 bridge protocol、session policy、权限模型或信任边界
- 修改 browser-side harness 与 sandbox-side scripts 的职责切分
- 新增或重构 `.agent/skills/`
- 需要留下一份可评审、可回填、可交接的实施记录

## 可以跳过的情况

只有在以下条件同时满足时，才可以不走完整 spec：

- 单文件或边界极小
- 不改变既有行为契约
- 验证方式非常直接
- 不涉及策略、协议、安全边界或 workflow

## 文件命名

默认写入 `discuss/`，使用：

```text
YYYY-MM-DD_<slug>.md
```

建议 slug 简洁、稳定，避免把具体实现细节写进文件名。

## 创建方式

使用脚手架：

```powershell
python scripts/tools/new_discuss_spec.py `
  --title "<task title>" `
  --slug "<short-slug>"
```

如果不传 `--slug`，脚本会基于标题生成一个保守 slug。

## 建议模板结构

1. Summary
2. Scope
3. Requirements
4. Design
5. Execution Plan
6. Validation
7. Implementation Report
8. Durable Sync

模板文件见：

```text
docs/workflows/discuss_spec_template.md
```

## 执行规则

- 先补 `Current context`
- 再写 `Requirements` 和 `Design`
- 开始实施前写 `Expected diff shape`
- 执行中更新任务勾选状态
- 停止前回填 `Validation` 和 `Implementation Report`

## 回填要求

一个 spec 不应停留在“只开头不收尾”的状态。任务完成或中断前，至少回填：

- 已完成项
- 未完成项
- 实际验证命令
- 已知限制
- 是否需要同步到 durable memory
- 如果仓库存在 `discuss/README_discuss.md` 之类的索引入口，按需同步状态

## 与 repo-local skill 的关系

推荐通过 `.agent/skills/bridge-spec-workflow/` 触发本流程。
skill 负责提醒读取哪些正式入口；spec 文件负责记录这次任务本身。
