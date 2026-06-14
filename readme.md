# Tabbit AgentNexus

这个仓库用于开发面向 Tabbit AI 浏览器的多智能体协作 skill。`AgentNexus` 的目标不是做单一站点的仓库桥接器，而是以 Tabbit 浏览器 Agent 为协作中枢，连接网页端高性能 Agent、本地挂载工作区、网页搜索、收藏夹、富文本页面和文件产物，在受控权限、审计记录和人工确认边界内完成上下文打包、多轮讨论、交叉评审、共识形成、分歧汇报和后续受控执行。

其中：

- `Bridge` 是 AgentNexus 的一种内部 adapter / transport pattern
- `repo-review` 是 AgentNexus 当前第一个优先落地的 scenario adapter
- 当前主要网页端推理适配目标仍是 GPT，但设计不应被单一站点锁死

## 当前定位

- 当前优先级是先把 `N1 Local Workspace Review Adapter` 做扎实。
- 架构默认基于 `E2B sandbox + mounted local folder + browser page automation`。
- 不把 `Native Messaging`、本机 `HTTP server`、用户机器 `PowerShell/cmd` 当成默认前提。
- 当前实现与 workflow 需要同时考虑网页端 GPT 和 Tabbit agent 的需求与易用性，而不是只优化其中一端。
- 无人值守能力默认采用 `bounded unattended collaboration`，必须带轮次上限、权限上限、失败上限和人工确认出口。

## 正式入口

- 架构真值入口：`docs/architecture/nexus_runtime_architecture.md`
- Tabbit 浏览器 agent 行为边界：`docs/architecture/tabbit_browser_agent_behavior_boundary.md`
- agent 协作规则：`AGENTS.md`
- 文档分层说明：`docs/README_docs.md`
- durable memory：`docs/PROJECT_MEMORY.md`
- workflow 入口：`docs/workflows/README_workflows.md`
- 报告目录入口：`docs/reports/README_reports.md`

## 目录约定

- `config/`：M1 / M2+ runtime policy 与 config templates
- `docs/`：正式文档、架构、workflow 说明
- `docs/reports/`：accepted 阶段报告、设计报告、验证总结
- `discuss/`：方案草稿、评审记录、实现 spec
- `reference/`：外部参考资料或长篇镜像材料
- `.agent/skills/`：repo-local 可复用 agent workflow
- `scripts/`：sandbox-side bridge runtime scripts
- `scripts/tools/`：维护仓库工作流与打包脚手架
- `tests/`：sandbox-side unit tests and fixtures

## 开发原则

- 先收敛行为边界，再写实现。
- 默认从只读评审模式出发，逐步升级能力。
- 仓库内容和 AI 回复都视为不可信输入。
- 所有高风险改动都应带验证路径与简明实现记录。

## 默认协作模型

当前仓库默认按 4 个角色协作推进：

- 用户：负责需求确认、优先级和最终验收
- 网页 GPT：负责架构建议、spec 评审与实现过程中的外部反馈
- Tabbit agent：负责目标使用侧测试与行为反馈
- 仓库代码 agent：负责大部分实际开发、验证、文档同步和提交

详细任务路由见 `docs/workflows/multi_role_collaboration.md`。

## 里程碑

1. `N0 Runtime Boundary & Capability Baseline`：冻结运行边界、能力平面、信任模型和默认禁区
2. `N1 Local Workspace Review Adapter`：生成 context pack，送入目标 AI 页面，保存 review report
3. `N2 Bounded Read-More Dialogue`：在策略和上限内支持追加上下文读取
4. `N3 Multi-Agent Consensus Loop`：支持多轮协作、共识/分歧汇报和停止条件
5. `N4 Proposal Capture & Artifact Writer`：结构化保存建议、草案和报告产物
6. `N5 Approved Workspace Mutation`：用户确认后执行受控写入
7. `N6 Approved Validation Commands`：用户确认后运行白名单验证命令
8. `N7 Multi-Scenario Browser Workspace`：扩展到 literature-reading、knowledge-vault、browser-research、rich-document/report 等 scenario
