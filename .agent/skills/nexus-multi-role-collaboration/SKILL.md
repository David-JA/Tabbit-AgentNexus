---
name: nexus-multi-role-collaboration
description: 为当前 Tabbit AgentNexus 仓库中的双 Agent 核心协作任务做职责划分、任务路由和交接收口。适用于需要明确用户授权、Web Agent、Browser Agent 与可选 Repo Agent 分工的场景。
compatibility: 需要能读取当前仓库中的 readme.md、docs/architecture/nexus_runtime_architecture.md、docs/PROJECT_MEMORY.md、docs/workflows/README_workflows.md、docs/workflows/multi_role_collaboration.md 和 discuss/ 相关 spec。
---

# AgentNexus Multi-Role Collaboration

## 目标

这个 skill 用于回答“当前任务由谁主责、谁反馈、何时调用外部仓库执行端、交接什么”。

它不替代正式架构文档，也不替代实现 spec。

## 使用前必读

在采取动作前，先读取：

1. `readme.md`
2. `docs/architecture/nexus_runtime_architecture.md`
3. `docs/PROJECT_MEMORY.md`
4. `docs/workflows/README_workflows.md`
5. `docs/workflows/multi_role_collaboration.md`
6. 当前相关的 `discuss/` spec

## 何时触发

出现以下任一情况时应触发：

- 需要明确 `Web Agent` 与 `Browser Agent / Tabbit Agent` 的默认分工
- 需要判断是否应调用可选 `Repo / Code Agent`
- 需要决定某类任务默认该交给哪个角色
- 需要收敛交接产物和反馈路径
- 需要避免“谁都在给建议，但没人真正负责落地”的推进混乱

## 默认路由原则

- 用户：目标、授权、优先级、最终验收
- `Web Agent`：架构设计、阶段汇报、监督、review
- `Browser Agent / Tabbit Agent`：浏览器执行、sandbox、挂载目录操作、跨端转交
- `Repo / Code Agent`：可选外部执行端，仅在明确委托后承担仓库修改、测试和提交证据返回

## 明确警告

- `Repo / Code Agent` 不是默认核心 actor。
- `Browser Agent / Tabbit Agent` 可以承担中继和挂载目录操作，但仓库变更应保持监督和可审计性。

## 结束条件

只有在以下信息清楚后，这次多角色协作收口才算完成：

- 当前阶段的主责角色
- 是否需要外部仓库执行端
- 交接物
- 是否需要用户重新确认
