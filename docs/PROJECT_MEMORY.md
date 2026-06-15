# PROJECT_MEMORY

这个文件只记录未来 agent 需要长期记住的项目级事实，不写一次性执行日志。

## Runtime Boundary Baseline

Tags: runtime, security, e2b, nexus

- 当前默认运行模型是 `E2B sandbox + mounted local folder + browser page automation`。
- 不把用户机器 shell、`Native Messaging` 或本机 `HTTP server` 视为默认桥接能力。
- AgentNexus 的页面侧脚本只承担临时 harness 角色，不承担本地权限和长期策略。
- `Bridge` 是 AgentNexus 的内部 adapter / transport pattern，不再是项目总定位。

Why it matters:
未来 agent 容易把“浏览器能控网页”误扩展成“能直接调用本机程序”，这里必须持续压住边界。

## MVP Strategy

Tags: roadmap, mvp, product

- 默认从 `N1 Local Workspace Review Adapter` 开始，而不是一步做到自动写入或命令执行。
- `repo-review` 是 AgentNexus 的第一个 scenario adapter，不代表项目边界。
- `N2-N7` 是递进能力，不应提前假设已经启用。

Why it matters:
这个顺序直接影响风险、验证范围和 prompt/protocol 复杂度。

## Trust Model

Tags: trust, prompt-injection, policy

- 仓库内容是 `untrusted repository data`。
- 目标 AI 的回复是 `untrusted proposal`。
- 任何读取扩权、patch 应用、命令执行都必须经过本地策略层判断，不能只靠 prompt 约束。

Why it matters:
AgentNexus 仓库天然容易把“模型建议”误当“可执行操作”，这是核心安全边界。

## Bounded Dialogue Baseline

Tags: workflow, consensus, unattended, nexus

- AgentNexus 的核心产品能力之一是 `bounded multi-round consensus`，而不是无限轮无人值守讨论。
- 多智能体协作必须显式设置 `max_rounds`、停止条件、人工确认点和风险汇报结构。
- 若未达成共识，系统应输出 `Disagreement Report` 和 `Human Confirmation Points`，而不是伪装成已完成结论。

Why it matters:
如果没有轮次和停止条件，多角色协作会从“受控协商”滑向不可审计的长链幻觉放大。

## Documentation Routing

Tags: docs, workflow, maintenance

- 正式架构落在 `docs/architecture/nexus_runtime_architecture.md`。
- 协作约定落在 `docs/workflows/agent_conventions.md`。
- accepted 阶段报告或设计/验证报告落在 `docs/reports/`。
- 非平凡实现前的执行 spec 落在 `discuss/`。
- repo-local workflow 入口放在 `.agent/skills/`。

Why it matters:
仓库正在从讨论期进入实现期，需要先把信息放对位置，避免后续持续漂移。

## Two-Agent Core Collaboration Model

Tags: product, collaboration, web-agent, browser-agent, repo-agent

- AgentNexus 的核心协作对象是 `Web Agent` 与 `Browser Agent / Tabbit Agent`。
- 用户负责目标、授权、优先级和最终验收。
- `Web Agent` 默认承担架构设计、多轮推进策略、阶段汇报、监督和高阶 review。
- `Browser Agent / Tabbit Agent` 默认承担网页操作、浏览器上下文获取、E2B sandbox 执行、挂载目录操作、产物整理和跨端转交。
- `Repo / Code Agent` 不是默认协作环成员，而是可选外部执行端；它只能根据用户或 `Browser Agent / Tabbit Agent` 转交的明确指令修改项目。
- `Browser Agent / Tabbit Agent` 可以减轻用户在 `Web Agent` 与本地仓库之间转交信息的负担，但其上下文会被浏览器状态、网页内容、sandbox 结果和多轮对话持续挤占，因此涉及仓库操作时需要 `Web Agent` 监督。
- 实际项目仓库操作最好在 git 仓库中完成，以便 `Web Agent`、`Browser Agent / Tabbit Agent` 与 `Repo / Code Agent` 都能依赖 diff、commit、测试结果和文档记录进行审计。

Why it matters:
如果把 `Repo / Code Agent` 写成默认并列角色，会误导后续实现，把 AgentNexus 从 `Web Agent ↔ Browser Agent` 协作系统错误扩展成四方常驻协作系统。

## Web GPT And Tabbit Dual-Usability Positioning

Tags: product, workflow, usability, gpt, tabbit

- 当前项目的基本定位，是在 AI 浏览器新架构下开发一个 AgentNexus 中枢，使用户能低成本调用网页端高性能 AI，并把浏览器协作、本地工作区和产物管理串成受控闭环。
- 当前网页端 AI 的主要适配目标是 GPT。
- Tabbit agent 在这个架构里不是可忽略的执行器，而是中介与副手，负责帮助连接本地上下文、页面交互与受控执行流程。
- 默认实现应同时考虑网页端 GPT 与 Tabbit agent 的需求和易用性，不能只优化其中一端。

Why it matters:
如果未来实现只围绕单一端点优化，要么会让网页端 GPT 的评审/推理收益下降，要么会让 Tabbit agent 的操作链路变脆，都会偏离当前项目的核心产品目标。
