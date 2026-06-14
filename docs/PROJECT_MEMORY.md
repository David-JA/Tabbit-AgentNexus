# PROJECT_MEMORY

这个文件只记录未来 agent 需要长期记住的项目级事实，不写一次性执行日志。

## Runtime Boundary Baseline

Tags: runtime, security, e2b, bridge

- 当前默认运行模型是 `E2B sandbox + mounted local folder + browser page automation`。
- 不把用户机器 shell、`Native Messaging` 或本机 `HTTP server` 视为默认桥接能力。
- bridge 的页面侧脚本只承担临时 harness 角色，不承担本地权限和长期策略。

Why it matters:
未来 agent 容易把“浏览器能控网页”误扩展成“能直接调用本机程序”，这里必须持续压住边界。

## MVP Strategy

Tags: roadmap, mvp, product

- 默认从 `M1 Repo Review Bridge` 开始，而不是一步做到自动写入或命令执行。
- `M2-M5` 是递进能力，不应提前假设已经启用。

Why it matters:
这个顺序直接影响风险、验证范围和 prompt/protocol 复杂度。

## Trust Model

Tags: trust, prompt-injection, policy

- 仓库内容是 `untrusted repository data`。
- 目标 AI 的回复是 `untrusted proposal`。
- 任何读取扩权、patch 应用、命令执行都必须经过本地策略层判断，不能只靠 prompt 约束。

Why it matters:
bridge 仓库天然容易把“模型建议”误当“可执行操作”，这是核心安全边界。

## Documentation Routing

Tags: docs, workflow, maintenance

- 正式架构落在 `docs/architecture/bridge_runtime_architecture.md`。
- 协作约定落在 `docs/workflows/agent_conventions.md`。
- accepted 阶段报告或设计/验证报告落在 `docs/reports/`。
- 非平凡实现前的执行 spec 落在 `discuss/`。
- repo-local workflow 入口放在 `.agent/skills/`。

Why it matters:
仓库正在从讨论期进入实现期，需要先把信息放对位置，避免后续持续漂移。
