# Bridge Runtime Architecture

> Status: compatibility note
> Last updated: 2026-06-15
> Current formal entry: `nexus_runtime_architecture.md`

`Bridge Runtime Architecture` 不再是本仓库的正式最高架构入口。

当前接受的项目总定位已经升级为 `Tabbit AgentNexus`，其中：

- `Bridge` 仅表示 AgentNexus 的内部 adapter / transport pattern
- `repo-review` 是当前第一个 scenario adapter
- 正式 runtime baseline、actor model、capability planes、bounded unattended collaboration 和 roadmap 以 `docs/architecture/nexus_runtime_architecture.md` 为准

为了兼容旧引用，本文件暂时保留；未来 agent 若遇到本文件与其他入口冲突，应优先读取：

1. `../../readme.md`
2. `nexus_runtime_architecture.md`
3. `../PROJECT_MEMORY.md`
