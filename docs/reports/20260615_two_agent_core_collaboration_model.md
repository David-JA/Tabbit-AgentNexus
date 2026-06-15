# Two-agent core collaboration model

> Status: accepted
> Date: 2026-06-15
> Type: architecture correction report

## Summary

本报告用于正式收口 AgentNexus 默认协作模型的修订结果：当前接受的默认模型不是“四角色并列常驻协作”，而是 `Web Agent ↔ Browser Agent / Tabbit Agent` 的核心双 Agent 协作环，`Repo / Code Agent` 则作为可选外部执行端存在。

## Accepted Conclusion

- 用户负责目标、授权、优先级和最终验收。
- `Web Agent` 默认负责高阶推理、架构设计、多轮推进策略、阶段汇报、监督与 review。
- `Browser Agent / Tabbit Agent` 默认负责真实浏览器操作、网页登录态上下文、E2B sandbox 执行、挂载目录操作、产物整理与跨端转交。
- `Repo / Code Agent` 不属于 `Web Agent ↔ Browser Agent` 默认对话环；只有在收到明确指令后，才承担仓库修改、测试、diff 收口和提交证据返回。

## Relationship To Transcript

- `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md` 继续保留为历史交互证据。
- transcript 用于说明这次架构修订背后的探测、纠偏与讨论过程，但不替代正式架构真值。
- 当前正式真值入口如下：
  - `readme.md`
  - `docs/architecture/nexus_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`

## Verification

- 正式入口、workflow、repo-local skills 与 durable memory 已同步为双 Agent 核心协作口径。
- 历史 transcript 与 archive 保留旧说法，用于追溯当时的讨论链路，而不是描述当前 accepted state。

## Known Limits

- 本报告只修订默认协作模型与文档口径，不新增 runtime 能力，也不改变 `N0-N7` roadmap。
- 浏览器侧与仓库侧的具体协议实现仍需继续沿现有 scenario adapter 路线推进。
