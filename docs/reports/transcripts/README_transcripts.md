# Report Transcripts

本目录保存 `docs/reports/` 下正式 report 的配套 transcript、原始交互证据和结构化转写记录。

## 目标

本目录中的 `transcript` 与 `report` 不是一类文档。

- `report` 的目标是总结、判断、收口和给出 accepted 结论。
- `transcript` 的目标是尽可能完整地保留原始交互内容，并在不删减事实的前提下做结构化整理。

默认要求：

- transcript 不提前替代 report 做摘要收口。
- transcript 可以优化结构，但不应主动删减原始消息内容。
- 若已实际展开并复制，transcript 中的“执行步骤”“输出正文”“中间观察”“失败路径”等原始块都属于应保留内容。

## 适合放在这里的内容

- 多角色协作过程的结构化 transcript
- 验证报告背后的原始交互记录
- 被正式报告引用的 evidence record

## 不适合放在这里的内容

- 尚未接受的 discuss 草稿
- 仍在实施中的临时执行日志
- 最终结论型 report 正文

## 与 `docs/reports/` 根目录的分工

- `docs/reports/` 根目录：正式 report、阶段性 accepted 结论
- `docs/reports/transcripts/`：支撑这些结论的 transcript 与原始证据

## 命名建议

默认沿用对应 report 的主题 slug，并在文件名中显式包含 `transcript`，例如：

```text
20260615_tabbit_skill_architecture_probe_transcript.md
```

若当前记录尚未对应某一篇日期化 report，也应尽量避免过于随意的文件名；后续进入正式归档时，建议补齐日期和主题 slug。

## 转写原则

### 1. 保留原文，避免提前摘要

- 不要把原始消息压成几条概括性 bullet。
- 不要把多段原始内容改写成“整理后正文”“结论摘要”来替代原文。
- 原始消息内部若已经包含结论、表格、报告正文、失败信息或重复信息，默认保留。
- 若某些折叠区块在源对话中存在、但本次并未被展开复制，不要事后虚构该部分内容。

### 2. 允许的结构优化

允许做以下整理：

- 补充标题、状态、类型、用途说明
- 补充角色与空间图例
- 补充 Turn 索引和每轮元数据
- 将同一条原始回复按 `执行步骤`、`中间观察`、`输出正文` 等自然边界拆成多个小节
- 用代码块包裹原始消息，避免消息中的 Markdown 标题破坏仓库文档层级

### 3. 不建议的处理

- 不要把 transcript 改写成 report 风格的“结论优先”文档
- 不要为了“更干净”擅自去重、合并或删除原始块
- 不要补写原始对话里没有出现过的推断性结论
- 不要把 transcript 当成 durable rule 入口；长期规则仍应写入正式 workflow 或 memory

## 推荐结构

默认推荐使用以下结构：

1. 标题
2. 状态头
3. 阅读说明
4. 角色与空间图例
5. Turn 字段约定
6. 回合索引
7. 结构化转写记录

推荐头部元数据：

```text
> Status: accepted transcript record
> Type: <transcript type>
> Purpose: <why this transcript is kept>
```

推荐的 Turn 元数据表：

| Field | Value |
|---|---|
| `Speaker` | |
| `Receiver` | |
| `Relay` | |
| `Space` | |
| `Intent` | |

## Tabbit / Browser 类 transcript 的拆分建议

在 Tabbit / Browser 类对话里，`执行步骤` 通常是源对话中默认存在但可折叠的过程层；`输出正文` 则是最终对外文本，默认不包含这些执行步骤。

因此，当某一轮 `tabbit-agent` 或其他执行侧 agent 的回复同时包含“过程”和“最终对外输出”，且你已经展开并复制了过程层时，推荐拆成以下两个小节：

- `执行步骤与中间观察（原文）`
- `输出正文（原文）`

若本次没有展开或复制 `执行步骤`，可以只保留 `输出正文（原文）`，或使用单一的 `消息正文（原文）` 小节承载实际拿到的内容。

若同一轮还包含独立的失败路径、回滚记录、补充附件说明，也可以继续细分，但前提是不改写原始内容。

## 模板入口

可直接复制本目录模板：

```text
docs/reports/transcripts/TEMPLATE_transcript.md
```

该模板用于起稿；目录级规则仍以本文件为准。
