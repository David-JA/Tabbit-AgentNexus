# Tabbit Bridge Skill Dev Repo

这个仓库用于开发面向 Tabbit AI 浏览器的 bridge skill，目标是让 Tabbit 在用户显式授权后，把本地仓库上下文安全地桥接到 Web 端 AI 页面，用于评审、补充读取、补丁提议与后续受控执行。

## 当前定位

- 当前优先级是先把 `M1 Repo Review Bridge` 做扎实。
- 架构默认基于 `E2B sandbox + mounted local folder + browser page automation`。
- 不把 `Native Messaging`、本机 `HTTP server`、用户机器 `PowerShell/cmd` 当成默认前提。

## 正式入口

- 架构真值入口：`docs/architecture/bridge_runtime_architecture.md`
- agent 协作规则：`AGENTS.md`
- 文档分层说明：`docs/README_docs.md`
- durable memory：`docs/PROJECT_MEMORY.md`
- workflow 入口：`docs/workflows/README_workflows.md`
- 报告目录入口：`docs/reports/README_reports.md`

## 目录约定

- `docs/`：正式文档、架构、workflow 说明
- `docs/reports/`：accepted 阶段报告、设计报告、验证总结
- `discuss/`：方案草稿、评审记录、实现 spec
- `reference/`：外部参考资料或长篇镜像材料
- `.agent/skills/`：repo-local 可复用 agent workflow
- `scripts/tools/`：维护仓库工作流的小工具

## 开发原则

- 先收敛行为边界，再写实现。
- 默认从只读评审模式出发，逐步升级能力。
- 仓库内容和 AI 回复都视为不可信输入。
- 所有高风险改动都应带验证路径与简明实现记录。

## 里程碑

1. `M1 Repo Review Bridge`：生成 context pack，送入目标 AI 页面，保存 review report
2. `M2 Read-more Bridge`：AI 请求额外文件，经过策略校验和确认后追加读取
3. `M3 Patch Proposal`：AI 输出 patch/diff，仅校验与保存
4. `M4 Apply with Approval`：用户确认后执行受控写入
5. `M5 Validation Commands`：用户确认后运行白名单验证命令
