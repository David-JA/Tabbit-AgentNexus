# discuss

这个目录保存草稿、spec、评审记录和仍在推进中的设计材料。

## Discuss Index

<!-- DISCUSS_SPEC_INDEX:START -->
| Date | Status | Type | Title | File | Notes |
|---|---|---|---|---|---|
| 2026-06-15 | Phase 1 done / Phase 2+ pending | workflow | N1 AgentNexus Foundation, Relay, and Validation Spec | [2026-06-15_n1-foundation-relay-validation-spec.md](2026-06-15_n1-foundation-relay-validation-spec.md) | current active spec; covers repo foundation + browser-mediated relay + supervised four-role workflow |
| 2026-06-14 | legacy / superseded | implementation | N1 Local Workspace Review Adapter implement spec | [2026-06-14_m1-repo-review-bridge-implement-spec.md](2026-06-14_m1-repo-review-bridge-implement-spec.md) | superseded by 2026-06-15 successor; body retained as historical implementation evidence |
<!-- DISCUSS_SPEC_INDEX:END -->

## 放置规则

- 正式接受的结论不要长期只留在这里。
- 非平凡实现前的 spec、评审记录、方案草稿优先写在这里。
- 当某项结论已经进入 `docs/`、`AGENTS.md` 或 `docs/PROJECT_MEMORY.md` 后，应考虑把对应草稿标记为完成、参考或归档候选。

## 当前状态

- 当前活跃 discuss 入口是 `2026-06-15_n1-foundation-relay-validation-spec.md`，作为 N1 AgentNexus foundation + browser-mediated relay + supervised four-role development 的当前阶段 active spec。
- `2026-06-14_m1-repo-review-bridge-implement-spec.md` 已转为 legacy / superseded，只在顶部指向 successor；正文保留作为历史实施证据，不再作为当前主入口。
- 已完成的 workflow、实现收口记录和 bridge 阶段背景材料已统一转入 `archive/`，避免与当前活跃 spec 混放。
- `2026-06-15_two-agent-core-collaboration-model.md` 已完成正式收口，并通过 accepted report 固化为当前默认协作模型的 supersession 记录。
- `2026-06-15_bridge-multi-role-collaboration-workflow.md` 只保留为历史实现记录，不再代表当前默认协作模型。
- 当前正式真值仍以 `readme.md`、`docs/architecture/nexus_runtime_architecture.md` 和 `docs/PROJECT_MEMORY.md` 为准。

## Archive

旧讨论稿不再作为活跃入口：

- [2026-06-14_bridge-repo-conventions-sync.md](archive/2026-06-14_bridge-repo-conventions-sync.md)
- [2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md](archive/2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md)
- [2026-06-15_agent-nexus-positioning-and-rename.md](archive/2026-06-15_agent-nexus-positioning-and-rename.md)
- [2026-06-15_bridge-multi-role-collaboration-workflow.md](archive/2026-06-15_bridge-multi-role-collaboration-workflow.md)
- [2026-06-15_bridge-positioning-sync-web-gpt-tabbit-usability.md](archive/2026-06-15_bridge-positioning-sync-web-gpt-tabbit-usability.md)
- [2026-06-15_bridge-repo-context-packager-skill.md](archive/2026-06-15_bridge-repo-context-packager-skill.md)
- [2026-06-15_two-agent-core-collaboration-model.md](archive/2026-06-15_two-agent-core-collaboration-model.md)
- [2026-06-15_n1-adapter-scaffold-and-local-dry-run-closure.md](archive/2026-06-15_n1-adapter-scaffold-and-local-dry-run-closure.md)
- [2026-06-15_stage-report-git-commit-trigger.md](archive/2026-06-15_stage-report-git-commit-trigger.md)
- [tabbit-gpt-bridge-architecture-discussion.md](archive/tabbit-gpt-bridge-architecture-discussion.md)
- [tabbit-gpt-bridge-final-architecture-v4.md](archive/tabbit-gpt-bridge-final-architecture-v4.md)
- [tabbit-skill-script-relationship-and-publishing-feasibility.md](archive/tabbit-skill-script-relationship-and-publishing-feasibility.md)
