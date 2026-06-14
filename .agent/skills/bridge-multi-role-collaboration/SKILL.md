---
name: bridge-multi-role-collaboration
description: 为当前 Tabbit bridge 仓库中的多角色协作任务做职责划分、任务路由和交接收口。适用于用户、网页 GPT、Tabbit agent、仓库代码 agent 同时参与的需求收敛、spec 评审、实现推进和验收分工场景。
compatibility: 需要能读取当前仓库中的 readme.md、docs/architecture/bridge_runtime_architecture.md、docs/PROJECT_MEMORY.md、docs/workflows/README_workflows.md、docs/workflows/multi_role_collaboration.md 和 discuss/ 相关 spec。
---

# Bridge Multi-Role Collaboration

## 目标

这个 skill 用于回答“当前任务应该由谁主责、谁反馈、何时交接、交接什么”。

它不替代正式架构文档，也不替代实现 spec。

## 使用前必读

在采取动作前，先读取：

1. `readme.md`
2. `docs/architecture/bridge_runtime_architecture.md`
3. `docs/PROJECT_MEMORY.md`
4. `docs/workflows/README_workflows.md`
5. `docs/workflows/multi_role_collaboration.md`
6. 当前相关的 `discuss/` spec

## 何时触发

出现以下任一情况时应触发：

- 用户、网页 GPT、Tabbit agent、仓库代码 agent 同时参与当前任务
- 需要决定某类任务默认该交给哪个角色
- 需要收敛交接产物和反馈路径
- 需要避免“谁都在给建议，但没人真正负责落地”的推进混乱

## 默认路由原则

- 需求、优先级、最终验收：用户主责
- 架构建议、spec 收敛、外部 review：网页 GPT 主责反馈
- 仓库代码实现、测试、提交、文档同步：仓库代码 agent 主责
- Tabbit 可用性验证、使用侧反馈：Tabbit agent 主责

## 结束条件

只有在以下信息清楚后，这次多角色协作收口才算完成：

- 当前阶段的主责角色
- 协作角色
- 交接物
- 是否需要用户重新确认
