# discuss

这个目录保存草稿、spec、评审记录和仍在推进中的设计材料。

## Discuss Index

<!-- DISCUSS_SPEC_INDEX:START -->
| Date | Status | Type | Title | File | Notes |
|---|---|---|---|---|---|
| 2026-06-14 | Completed | workflow | Bridge repo conventions sync | [2026-06-14_bridge-repo-conventions-sync.md](2026-06-14_bridge-repo-conventions-sync.md) | conventions synced and first commit prepared |
| 2026-06-14 | Comprehensive reference | architecture | Tabbit GPT Bridge comprehensive architecture | [2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md](2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md) | merged reference from 3 docs; not formal source of truth |
| 2026-06-14 | M1 scaffold in progress | implementation | M1 Repo Review Bridge implement spec | [2026-06-14_m1-repo-review-bridge-implement-spec.md](2026-06-14_m1-repo-review-bridge-implement-spec.md) | runtime contract settled; sandbox-side testable core in progress |
| 2026-06-15 | Completed | workflow | 新增 bridge repo context packager skill | [2026-06-15_bridge-repo-context-packager-skill.md](2026-06-15_bridge-repo-context-packager-skill.md) | add a bridge-specific repo context packaging skill and script |
| 2026-06-15 | Completed | workflow | Bridge multi-role collaboration workflow | [2026-06-15_bridge-multi-role-collaboration-workflow.md](2026-06-15_bridge-multi-role-collaboration-workflow.md) | settled the 4-role collaboration model, task routing, and handoff rules |
| 2026-06-15 | Completed | workflow | Bridge positioning sync for web GPT and Tabbit usability | [2026-06-15_bridge-positioning-sync-web-gpt-tabbit-usability.md](2026-06-15_bridge-positioning-sync-web-gpt-tabbit-usability.md) | synced the core product positioning and dual-usability requirement into formal docs |
<!-- DISCUSS_SPEC_INDEX:END -->

## 放置规则

- 正式接受的结论不要长期只留在这里。
- 非平凡实现前的 spec、评审记录、方案草稿优先写在这里。
- 当某项结论已经进入 `docs/`、`AGENTS.md` 或 `docs/PROJECT_MEMORY.md` 后，应考虑把对应草稿标记为完成、参考或归档候选。

## 当前状态

- 三份原始 Tabbit 讨论材料已归档到 `archive/`，仅作为历史推导链保留；综合方案（`2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md`）作为合并后的背景参考；正式真值仍以 `readme.md`、`docs/architecture/bridge_runtime_architecture.md` 和 `docs/PROJECT_MEMORY.md` 为准。
- M1 实现前的收敛入口是 `2026-06-14_m1-repo-review-bridge-implement-spec.md`。
- `2026-06-14_bridge-repo-conventions-sync.md` 记录了当前仓库从骨架初始化继续收口到协作约定同步与首次提交的过程。

## Archive

旧讨论稿不再作为活跃入口：

- [tabbit-gpt-bridge-architecture-discussion.md](archive/tabbit-gpt-bridge-architecture-discussion.md)
- [tabbit-gpt-bridge-final-architecture-v4.md](archive/tabbit-gpt-bridge-final-architecture-v4.md)
- [tabbit-skill-script-relationship-and-publishing-feasibility.md](archive/tabbit-skill-script-relationship-and-publishing-feasibility.md)
