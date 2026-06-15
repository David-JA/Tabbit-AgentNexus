# Bounded Agent Dialogue Workflow

## 1. 目标

本文定义 AgentNexus 在多智能体 round-based 协作中的最小稳定协议。

本文解决的是：

- 多轮协作如何显式设定上限
- 每轮交接至少包含什么信息
- 共识与分歧如何结构化收口
- 什么时候必须停止并交给用户

本文不替代：

- 正式 runtime baseline
- 具体 scenario adapter 的实现细节
- 本地 policy 对读取、写入、命令执行的最终裁决

## 2. 核心行为

Given: 用户启动一个多智能体协作任务，并设置 `max_rounds=5`
When: `Web Agent` 与 `Browser Agent / Tabbit Agent` 在声明好的轮次上限内交换意见
Then: 系统最多执行 5 轮协作；若达成共识，输出 `Consensus Report`；若未达成共识，输出 `Disagreement Report` 和 `Human Confirmation Points`

Given: 某一轮协作需要更多上下文，但追加读取会触发策略或权限升级
When: 当前角色提出 read-more 请求
Then: 系统不得自动越权，而应显式记录风险、所需权限和停止原因

Given: `Web Agent` 与 `Browser Agent / Tabbit Agent` 出现冲突建议，或外部仓库执行证据与协商结论不一致
When: 本轮结束
Then: 冲突必须进入 `Disagreements` 小节，而不是被下一位角色静默覆盖

## 3. Round Handoff 格式

每轮至少应包含：

- `Task`
- `Current Round`
- `Context Used`
- `Executed Actions`
- `Findings`
- `Disagreements / Risks`
- `Recommended Next Actions for Browser Agent`
- `Recommended Repo Agent Instructions`
- `Stop / Continue Decision`

推荐 handoff 标题：

```markdown
# AgentNexus Web-Agent Handoff
```

或：

```markdown
# AgentNexus Tabbit Execution Feedback
```

## 4. Stop conditions

- 达成共识
- 达到 `max_rounds`
- 需要用户确认
- 需要更高权限
- 遇到安全边界
- 浏览器 / sandbox / 登录态失败
- 上下文不足且无法安全追加读取

## 5. Final Report 格式

```markdown
# AgentNexus Consensus Report

## Task
## Context Used
## Round Summary
## Agreed Findings
## Disagreements
## Risk / Uncertainty
## Human Confirmation Points
## Recommended Next Actions for Browser Agent
## Recommended Repo Agent Instructions
## Stop Reason
```

如果未达成共识，标题改为：

```markdown
# AgentNexus Disagreement Report
```

## 6. 维护原则

- 轮次上限必须先于“是否继续”被声明。
- “无人值守”只表示可在边界内自动推进，不表示可绕过权限、策略或人工确认。
- 报告必须区分已执行事实、推理判断和待确认事项。
