---
name: nexus-bounded-dialogue
description: 为当前 Tabbit AgentNexus 仓库中的多轮协作任务建立 bounded dialogue 协议、round-based handoff 和 consensus/disagreement 收口格式。
compatibility: 需要能读取当前仓库中的 readme.md、docs/architecture/nexus_runtime_architecture.md、docs/workflows/bounded_agent_dialogue.md、docs/workflows/multi_role_collaboration.md 和 discuss/ 相关 spec。
---

# AgentNexus Bounded Dialogue

## 目标

这个 skill 用于回答“多轮协作如何设上限、每轮交什么、最后怎么收口”。

它不替代正式架构文档，也不替代具体 scenario spec。

## 使用前必读

在采取动作前，先读取：

1. `readme.md`
2. `docs/architecture/nexus_runtime_architecture.md`
3. `docs/workflows/bounded_agent_dialogue.md`
4. `docs/workflows/multi_role_collaboration.md`
5. 当前相关的 `discuss/` spec

## 何时触发

出现以下任一情况时应触发：

- 需要 2 轮及以上的多智能体协作
- 需要显式记录共识、分歧、风险或人工确认点
- 需要为网页端 Agent、Tabbit agent、仓库代码 agent 设计 round-based handoff

## 默认规则

- 显式声明 `current_round / max_rounds`
- 每轮至少交接 `Task`、`Context Used`、`Findings`、`Disagreements / Risks`、`Stop / Continue Decision`
- 达成共识时输出 `Consensus Report`
- 未达成共识时输出 `Disagreement Report` 与 `Human Confirmation Points`

## 结束条件

只有在以下信息清楚后，这次多轮协作收口才算完成：

- 停止原因
- 是否达成共识
- 尚未关闭的风险
- 是否需要用户确认
