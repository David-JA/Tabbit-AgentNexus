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

## Multi-Role Collaboration Model

Tags: workflow, collaboration, roles

- 当前 bridge 开发默认存在 4 个角色：用户、网页 GPT、Tabbit agent、仓库代码 agent。
- 用户负责需求确认、优先级和最终验收。
- 网页 GPT 负责架构建议、spec 收敛和实现过程中的 reviewer 反馈。
- Tabbit agent 负责目标使用方测试与行为反馈。
- 仓库代码 agent 负责仓库内的大部分实现、验证、文档同步和提交收口。

Why it matters:
多角色协作已经是当前仓库的常态，如果不把角色边界和默认任务路由写清，未来 agent 很容易重复评审、错配职责或把外部建议误当成已接受决策。

## Web GPT And Tabbit Dual-Usability Positioning

Tags: product, workflow, usability, gpt, tabbit

- 当前项目的基本定位，是在 AI 浏览器新架构下开发一个 bridge 中枢，使用户能低成本调用网页端高性能 AI。
- 当前网页端 AI 的主要适配目标是 GPT。
- Tabbit agent 在这个架构里不是可忽略的执行器，而是中介与副手，负责帮助连接本地上下文、页面交互与受控执行流程。
- 默认实现应同时考虑网页端 GPT 与 Tabbit agent 的需求和易用性，不能只优化其中一端。

Why it matters:
如果未来实现只围绕单一端点优化，要么会让网页端 GPT 的评审/推理收益下降，要么会让 Tabbit agent 的操作链路变脆，都会偏离当前项目的核心产品目标。
