# AgentNexus Runtime Architecture

> Status: accepted baseline for current development repo
> Last updated: 2026-06-15
> Former entry: `docs/architecture/bridge_runtime_architecture.md`

## 1. Product positioning

这个仓库当前接受的产品定位是 `Tabbit AgentNexus`。

它是一个面向 Tabbit AI 浏览器的多智能体协作 skill 开发仓库，用于让网页端高性能 Agent 与 Tabbit 浏览器 Agent 构成核心协作环，并通过浏览器侧执行与中继能力连接：

- 网页端高性能 Agent
- 本地挂载工作区
- 网页搜索与页面观察
- 收藏夹等浏览器原生上下文源
- 富文本页面与文件产物

目标是在受控权限、审计记录和人工确认边界内，完成上下文打包、多轮讨论、交叉评审、共识形成、分歧汇报和后续受控执行。

约束：

- `Bridge` 是 AgentNexus 的内部 adapter / transport pattern，不再是项目总名。
- `repo-review` 是第一个优先落地的 scenario adapter，不是项目边界。
- 当前网页端高性能 Agent 的主要适配目标仍是 GPT，但设计不得预设只能服务单一站点。

## 2. Actor model

### 2.1 Core collaboration actors

#### User

负责：

- 定义目标、优先级和验收标准
- 确认非显然 tradeoff
- 对高风险动作做最终确认

边界：

- 用户是决策与验收中心，不是默认通信总线。
- 若 `Browser Agent / Tabbit Agent` 可以安全承担跨端转交，用户不应被写成日常 relay bus。

#### Web Agent

负责：

- 任务架构设计与多轮推进策略
- 阶段汇报、review、监督与风险说明
- 审阅 `Browser Agent / Tabbit Agent` 的观察结果与 `Repo / Code Agent` 的执行证据
- 在需要仓库修改时起草或审核精确的外部执行指令

不负责：

- 直接拥有本地执行权限
- 直接替代本地策略层做读取、写入或命令执行决策

#### Browser Agent / Tabbit Agent

负责：

- 浏览器页面导航、观察与交互
- 在受控条件下以浏览器用户身份读取、投递并回收网页端 Agent 对话，承担 `browser-mediated cross-space interaction` 原型
- 把上下文安全送入网页端 Agent
- 回收网页端结果、浏览器观察与产物状态
- 搜索、rich page interaction、E2B sandbox 执行和挂载目录操作
- 在受控策略下承担跨空间转交与产物整理

边界：

- `Browser Agent / Tabbit Agent` 功能强，但上下文成本高。
- 浏览器状态、网页快照、sandbox 日志和与 `Web Agent` 的多轮对话都会持续占用其上下文。
- `browser-mediated cross-space interaction` 已出现原型能力，但当前还不是默认稳定 transport；当链路过慢、卡在工具调度循环或缺少完整性判断时，用户仍可临时介入中转与纠偏。
- 不应让它长时间无人监督地执行仓库变更链；涉及仓库操作时，应保持 `Web Agent` 监督，并优先依赖 git 可审计证据。

### 2.2 External executors and adapters

#### Repo / Code Agent

`Repo / Code Agent` 不是 `Web Agent ↔ Browser Agent` 默认对话环的参与者。它是一个外部执行端，通过用户或 `Browser Agent / Tabbit Agent` 转交的明确指令接收任务，并返回可审计的仓库产物。

负责：

- 按明确指令修改仓库文件
- 运行测试与验证命令
- 返回 diff、测试结果、阶段报告和必要的提交证据

不负责：

- 直接参与 `Web Agent ↔ Browser Agent` 的默认多轮协商
- 拥有产品架构主责
- 把网页端自然语言直接视为已接受授权

#### Local Workspace Adapter

负责：

- 工作区发现
- policy 校验
- secret redaction
- context pack 生成
- audit log 与产物写入

边界：

- 它属于 capability / policy adapter，不是自治协作 actor。
- 它负责执行本地策略与产物处理，不负责替任一 agent 做产品决策。

## 3. Capability planes

### 3.1 Browser plane

- 页面导航
- 页面观察
- 表单/富文本/网页交互
- 网页端 Agent 对话页的读取、输入与消息投递
- 浏览器原生上下文源管理

### 3.2 Web-agent dialogue plane

- handoff prompt
- round-based discussion
- consensus / disagreement report
- stop / continue 决策

### 3.3 Local workspace plane

- mounted folder 读取
- policy gating
- redaction
- context packaging
- approved mutation and validation hooks

### 3.4 Artifact plane

- context pack
- review report
- consensus report
- disagreement report
- session summary
- audit trail

### 3.5 Policy / audit plane

- trust model
- deny-before-allow path policy
- action confirmation
- escalation checkpoints
- append-only audit records

### 3.6 Tabbit skill runtime and distribution plane

AgentNexus 当前接受 Tabbit skill 的双形态分工：

- 仓库中的源码版是 source of truth。
- Tabbit skill 的运行与分发单元是 `SKILL.md + .tar.gz bundle`。
- `browser-scripts/*.js` 在网页上下文执行。
- `scripts/*.py` 在 `E2B sandbox` 执行。
- Tabbit `.tar.gz` 是发行物，不替代仓库中的 repo-native 源码、测试和文档入口。

对应约束：

- Tabbit skill 不替代 repo-native 的测试、`git diff`、`git commit` 和本地仓库 agent。
- `allowed_tools` 只可视为声明性元数据，不应作为强安全边界。
- `url_patterns` 已证实会进入后端 metadata，但 UI 自动推荐 / 自动触发行为仍未完全证成。
- skill 删除后，DB 级失效可以成立，但 `E2B sandbox` 本地缓存不保证即时清空。
- confirmed size limit 仍是 `unknown`，因此 v0 bundle 应保持小型化，避免把未证成的大体积分发前提写进设计。

## 4. Trust model

### 4.1 Untrusted inputs

以下内容默认都属于不可信输入：

- 仓库文件内容
- 网页内容
- 收藏夹标题与说明
- 既有 artifact
- 网页端 Agent 回复

### 4.2 Enforcement rule

只有本地策略层可以决定：

- 是否允许追加读取
- 是否允许写入本地工作区
- 是否允许执行命令
- 是否需要用户确认

### 4.3 Default non-assumptions

当前默认不把以下能力当成运行前提：

- 用户机器 `PowerShell/cmd`
- `Native Messaging`
- 本机 `127.0.0.1` 服务
- 未挂载目录访问
- 从网页端自然语言直接解析并执行动作

## 5. Bounded unattended collaboration

AgentNexus 支持的不是无限轮无人值守，而是 `bounded unattended collaboration`。

默认必须显式设置：

- `max_rounds`
- 权限上限
- 失败上限
- 风险升级条件
- 人工确认点

### Stop conditions

- 达成共识
- 达到 `max_rounds`
- 需要用户确认
- 需要更高权限
- 遇到安全边界
- 浏览器 / sandbox / 登录态失败
- 上下文不足且无法安全追加读取

### Required reports

- 达成共识：输出 `Consensus Report`
- 未达成共识：输出 `Disagreement Report`
- 两者都必须包含 `Risk / Uncertainty` 与 `Human Confirmation Points`

## 6. Scenario adapters

当前接受的 scenario adapter 分层如下：

- `repo-review`
  - former name: `M1 Repo Review Bridge`
  - current roadmap slot: `N1 Local Workspace Review Adapter`
- `literature-reading`
- `knowledge-vault`
- `browser-research`
- `rich-document/report`

约束：

- 新 scenario 可以共用同一套运行边界与 policy / audit 基线
- 不应把单一 scenario 的临时实现反向提升为全项目默认边界

## 7. Roadmap

1. `N0 Runtime Boundary & Capability Baseline`
2. `N1 Local Workspace Review Adapter`
3. `N2 Bounded Read-More Dialogue`
4. `N3 Multi-Agent Consensus Loop`
5. `N4 Proposal Capture & Artifact Writer`
6. `N5 Approved Workspace Mutation`
7. `N6 Approved Validation Commands`
8. `N7 Multi-Scenario Browser Workspace`

## 8. Related entries

- Tabbit 浏览器 agent 行为边界：`tabbit_browser_agent_behavior_boundary.md`
- Tabbit skill 架构边界诊断报告：`../reports/20260615_tabbit_skill_architecture_boundary_diagnosis.md`
- 多角色协作 workflow：`../workflows/multi_role_collaboration.md`
- 多轮协作 workflow：`../workflows/bounded_agent_dialogue.md`
- bridge 兼容入口：`bridge_runtime_architecture.md`
