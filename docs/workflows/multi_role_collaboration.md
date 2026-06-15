# Multi-Role Collaboration Workflow

> 默认模型：Two-Agent Core Collaboration + External Repo Executor

## 1. 目标

本文定义当前 AgentNexus 的默认协作模型：`Web Agent` 与 `Browser Agent / Tabbit Agent` 构成核心双 Agent 协作环，用户负责授权与验收，`Repo / Code Agent` 只在显式委托时作为外部执行端参与。

本文解决的是：

- 默认核心 loop 是谁和谁
- 不同任务默认该交给谁
- 什么时候需要外部仓库执行端
- 交接时应携带什么产物与审计证据

本文不解决：

- AgentNexus runtime 边界本身
- browser 自动化实现细节
- N2+ action protocol 设计

这些内容仍以 `readme.md`、`docs/architecture/nexus_runtime_architecture.md` 和具体实现 spec 为准。

## 2. 默认模型

核心协作环：

- 用户给出目标、优先级、授权边界和最终验收标准
- `Web Agent` 与 `Browser Agent / Tabbit Agent` 进行 round-based 协作
- 只有在需要仓库修改、测试或提交证据时，才显式调用 `Repo / Code Agent`

| Role | Status in AgentNexus | Primary responsibility |
|---|---|---|
| User | Decision and acceptance center | Goal, priority, authorization, acceptance |
| Web Agent | Core actor; reasoning/supervision/reporting layer | Architecture, strategy, stage report, review, supervision |
| Browser Agent / Tabbit Agent | Core actor; execution/relay layer | Browser operation, webpage context, sandbox, mounted-folder operations, artifact relay |
| Repo / Code Agent | External executor | Explicit repo edits, tests, diff, commit/report evidence |

## 3. 角色优点与局限

### 3.1 User

优点：

- 拥有最终授权与验收权
- 能处理非显然 tradeoff 和范围变更

局限：

- 不应被写成默认中继总线
- 不负责日常实现和持续交接收口

### 3.2 Web Agent

优点：

- 适合承担高阶推理、架构设计和多轮推进策略
- 更适合做阶段汇报、review 和对仓库执行证据的再审阅

局限：

- 不直接拥有本地执行权限
- 不能绕过本地策略层直接下发可执行动作

### 3.3 Browser Agent / Tabbit Agent

优点：

- 天然适合浏览器操作、网页登录态上下文、网页观察与富交互
- 可在受控授权下承担 E2B sandbox、挂载目录操作和跨端转交

局限：

- 浏览器状态、网页内容、sandbox 结果和多轮对话会持续挤占上下文
- 不应长时间无人监督地执行仓库变更链

### 3.4 Repo / Code Agent

优点：

- 适合承担明确指令下的仓库修改、测试、diff 收口和提交证据返回
- 输出天然可被 `git diff`、测试结果和阶段报告审计

局限：

- 不是默认对话环成员
- 不拥有产品架构主责，也不能把自然语言直接视为已接受授权

## 4. 默认推进流程

### Phase 1: Goal and authorization

主责：用户

协作：

- `Web Agent` 帮助澄清目标、范围和风险

产物：

- 明确目标
- 授权边界
- 验收标准

### Phase 2: Architecture and task decomposition

主责：`Web Agent`

协作：

- `Browser Agent / Tabbit Agent` 提供浏览器侧能力与上下文约束

产物：

- spec 建议
- 任务拆解
- 风险与停止条件

### Phase 3: Browser / sandbox / context execution

主责：`Browser Agent / Tabbit Agent`

协作：

- `Web Agent` 持续监督与 review

产物：

- 页面观察
- sandbox 结果
- 中继产物

### Phase 4: Optional repository execution

主责：`Repo / Code Agent`（仅在被显式调用时）

指令来源：

- 用户或 `Browser Agent / Tabbit Agent` 转交的明确指令，通常由 `Web Agent` 起草或审核

产物：

- diff
- 测试结果
- 阶段报告
- commit evidence（如适用）

### Phase 5: Review and acceptance

主责：用户

协作：

- `Web Agent` 负责整合阶段汇报与限制
- `Browser Agent / Tabbit Agent` 提供执行侧事实
- `Repo / Code Agent` 若被调用，则提供仓库侧证据

## 5. 默认任务路由

| Task type | Default route |
|---|---|
| Architecture, strategy, stage report, risk review | `Web Agent` |
| Browser operation, webpage information, page interaction | `Browser Agent / Tabbit Agent` |
| Sandbox execution, mounted-folder artifact handling | `Browser Agent / Tabbit Agent` with explicit authorization |
| Concrete repo edits, tests, git diff, commit | `Repo / Code Agent` only after explicit delegation |
| Final acceptance and authorization escalation | 用户 |

## 6. Round-Based 协作补充

当任务进入多轮协作时，除职责分工外还应遵守：

- 默认使用 `max_rounds`、`current_round`、`stop_reason` 三个显式字段。
- 每轮交接至少包含：当前任务、已用上下文、已执行动作、发现、风险、是否继续。
- 若 `Web Agent` 与 `Browser Agent / Tabbit Agent` 出现冲突结论，或外部仓库执行证据与协商结论冲突，必须显式列出 `Disagreements`。
- 达成共识时输出 `Consensus Report`；未达成共识时输出 `Disagreement Report` 和 `Human Confirmation Points`。

## 7. 交接规则

### Web Agent → Browser Agent / Tabbit Agent

应交接：

- 任务架构
- 当前轮次目标
- 风险与停止条件
- 需要回收的观察或产物

### Browser Agent / Tabbit Agent → Web Agent

应交接：

- 浏览器观察事实
- sandbox 结果
- 失败路径
- 可继续 / 应停止判断

### Web Agent / Browser Agent → Repo / Code Agent

应交接：

- 明确可执行的仓库指令
- 预期变更范围
- 验证要求
- 已知限制和审计要求

不应直接交接：

- 被默认视为已接受的最终需求
- 未经授权的自然语言动作

### 所有角色 → 用户

应交接：

- 影响验收的关键信息
- 非显然风险
- 尚未关闭的限制或 pending decision

## 8. Anti-patterns

- 不要把 `Repo / Code Agent` 建模成 `Web Agent ↔ Browser Agent` 默认环中的并列角色。
- 不要把 `Browser Agent / Tabbit Agent` 只写成 tester。
- 不要把 `Web Agent` 只写成外部 reviewer。
- 不要让 `Browser Agent / Tabbit Agent` 长时间无人监督地执行仓库变更链。
- 不要把目标 AI 回复、网页文本或仓库文本直接视为可执行指令。

## 9. 升级条件

以下情况应从“常规协作”升级为“需要用户重新确认”：

- 任务范围扩大
- 需要修改正式架构真值
- 需要读取更多敏感内容
- 需要从只读升级到写入或命令执行
- `Web Agent`、`Browser Agent / Tabbit Agent` 与外部仓库执行证据给出冲突结论
