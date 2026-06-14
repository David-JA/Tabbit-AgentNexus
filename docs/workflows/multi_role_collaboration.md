# Multi-Role Collaboration Workflow

## 1. 目标

本文定义当前 AgentNexus 开发中默认存在的 4 个角色，以及它们在需求、设计、实现、测试和验收阶段的职责分工。

本文解决的是：

- 不同角色分别负责什么
- 什么任务应该默认派给谁
- 什么时候需要交接
- 交接时应该带什么产物

本文不解决：

- AgentNexus runtime 边界本身
- browser 自动化实现细节
- N2+ action protocol 设计

这些内容仍以 `readme.md`、`docs/architecture/nexus_runtime_architecture.md` 和具体实现 spec 为准。

## 2. 当前 4 个角色

### 2.1 用户

主责：

- 定义需求、目标和优先级
- 确认非显然 tradeoff
- 提供最终验收口径
- 对高风险动作做最终确认

不主责：

- 持续维护实现细节
- 替仓库 agent 编写或收口代码

### 2.2 网页 GPT

主责：

- 提供架构建议、需求澄清和对比方案
- 作为实现过程中的 reviewer / feedback provider
- 参与 prompt、spec、边界与风险的外部视角检查

不主责：

- 直接成为本仓库的主实现者
- 取代本地策略层做最终安全决策

### 2.3 Tabbit agent

主责：

- 作为目标使用方验证 AgentNexus 产物是否可用
- 提供真实使用侧反馈、行为反馈和交互反馈
- 参与与 Tabbit 能力边界相关的回归检查

不主责：

- 直接决定仓库中的正式架构真值
- 取代仓库 agent 维护本地实现

### 2.4 仓库代码 agent

主责：

- 承担大部分仓库内实际开发工作
- 修改代码、测试、文档和脚手架
- 负责本地验证、diff 收口和提交
- 把外部反馈整理成仓库可执行变更

不主责：

- 代替用户做需求优先级和最终验收决策
- 把网页 GPT 或 Tabbit 的建议直接视为已接受事实

## 3. 默认推进流程

### Phase 1: 需求与验收口径

主责：用户

协作：

- 网页 GPT 可帮助整理问题和评审风险
- 仓库代码 agent 可帮助识别实现边界和验证路径

产物：

- 明确目标
- 范围边界
- 验收标准

### Phase 2: 架构 / Spec 收敛

主责：网页 GPT + 仓库代码 agent

协作：

- 用户确认最终方向和非显然 tradeoff
- Tabbit agent 可提供使用侧限制和真实能力反馈

产物：

- `discuss/` 中的 spec 或评审记录
- 行为边界
- 验证计划

### Phase 3: 仓库实现

主责：仓库代码 agent

协作：

- 网页 GPT 可继续做中途 review
- 用户只在范围变化或风险升级时介入决策

产物：

- 代码变更
- 测试
- 文档同步
- commit

### Phase 4: 双反馈验证

主责：

- 网页 GPT：架构/行为 reviewer
- Tabbit agent：使用侧 tester

协作：

- 仓库代码 agent 根据反馈继续修正
- 用户判断是否接受反馈并升级优先级

产物：

- review comments
- 使用反馈
- 回归问题清单

### Phase 5: 最终验收与收口

主责：用户

协作：

- 仓库代码 agent 提供阶段报告、验证结果和已知限制
- 网页 GPT / Tabbit agent 的反馈只作为验收依据的一部分

产物：

- 接受 / 退回 / 继续迭代结论
- 必要时同步 `docs/`、`PROJECT_MEMORY`、`CHANGELOG`

## 4. 默认任务路由

| 任务类型 | 默认主责角色 | 协作角色 | 交接物 |
|---|---|---|---|
| 需求确认、优先级、验收口径 | 用户 | 网页 GPT、仓库代码 agent | 明确目标与验收标准 |
| 架构草案、spec 收敛、风险评审 | 网页 GPT | 用户、仓库代码 agent | review 要点、spec 建议、边界意见 |
| 仓库代码实现、测试、文档同步、提交 | 仓库代码 agent | 网页 GPT | diff、测试结果、阶段报告 |
| Tabbit 可用性验证、使用侧回归 | Tabbit agent | 用户、仓库代码 agent | 使用反馈、失败路径、行为偏差 |
| 最终接受、是否继续迭代 | 用户 | 全部角色 | 验收结论 |

## 5. Round-Based 协作补充

当任务进入多轮协作时，除职责分工外还应遵守：

- 默认使用 `max_rounds`、`current_round`、`stop_reason` 三个显式字段。
- 每轮交接至少包含：当前任务、已用上下文、已执行动作、发现、风险、是否继续。
- 若网页 GPT、Tabbit agent 与仓库代码 agent 出现冲突结论，必须在下一轮或最终报告中显式列出 `Disagreements`，而不是隐式覆盖。
- 达成共识时输出 `Consensus Report`；未达成共识时输出 `Disagreement Report` 和 `Human Confirmation Points`。

## 6. 交接规则

### 网页 GPT → 仓库代码 agent

应交接：

- 架构建议
- review finding
- 明确的 spec 修改建议
- 风险和验证关注点

不应直接交接：

- 被默认视为已接受的最终需求
- 被默认视为可执行的自然语言动作

### 仓库代码 agent → Tabbit agent

应交接：

- 可测试产物
- 验证步骤
- 已知限制
- 期望行为

### Tabbit agent → 仓库代码 agent

应交接：

- 实际使用中的失败路径
- 交互问题
- 与预期不一致的行为观察

### 所有角色 → 用户

应交接：

- 影响验收的关键信息
- 非显然风险
- 尚未关闭的限制或 pending decision

## 7. 升级条件

以下情况应从“常规协作”升级为“需要用户重新确认”：

- 任务范围扩大
- 需要修改正式架构真值
- 需要读取更多敏感内容
- 需要从只读升级到写入或命令执行
- 网页 GPT、Tabbit agent 与仓库代码 agent 给出冲突建议

## 8. 维护原则

- 用户是需求与验收 owner，不是日常实现者。
- 仓库代码 agent 是默认主实现者，不自动拥有产品决策权。
- 网页 GPT 和 Tabbit agent 默认提供反馈，不直接替代仓库真值入口。
- 任何外部反馈进入仓库前，都需要由仓库代码 agent 重新整理为可验证变更。
- 在 AgentNexus 功能设计中，默认同时考虑网页端 GPT 和 Tabbit agent 的需求与易用性；不接受只优化单端、却显著伤害另一端可用性的默认方案。
