# Tabbit Skill Architecture Boundary Diagnosis

> Status: accepted
> Date: 2026-06-15
> Type: skill architecture boundary diagnosis report

## 1. 这轮工作解决了什么问题

本报告用于把 `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md` 中已经完成的多轮架构取证，收口为一组可以正式引用的结论，回答以下问题：

- Tabbit agent 侧的 skill 到底是什么结构
- 它与仓库里的 `SKILL.md` / 脚本型 skill 是否兼容
- AgentNexus 后续应采用什么集成形态
- 哪些结论已经确认，哪些仍应保守表述

结论是：

- Tabbit agent 侧 skill 已证实是统一 bundle 模型，而不是“提示词 / 脚本 / 任务”三种彼此独立的底层类型。
- `SKILL.md` 是 bundle 的必需入口，agent 侧真实打包格式是 `.tar.gz`。
- skill 已证实具备双运行时：`browser-scripts/*.js` 在网页上下文执行，`scripts/*.py` 在 E2B sandbox 执行。
- T02-T04 已证实一条原型级 `browser-mediated cross-space interaction`：Tabbit agent 能以浏览器用户身份读取网页 GPT 输出、投递修正消息并继续回收后续测试指令，用户不是这些轮次的物理中介。
- AgentNexus 的推荐集成形态不是“把本地仓库 agent 全部塞进浏览器 skill”，而是“仓库源码版 + Tabbit 发行版”的双形态协同。

## 2. 当前接受的边界或结论

### 2.1 已确认的 skill contract

- Tabbit skill 是统一 bundle 模型。
- `SKILL.md` 是唯一必需入口。
- agent 侧上传 / 分发的真实格式是 `.tar.gz`。
- `browser-scripts/*.js` 可通过 `evaluate_script` 在网页上下文执行。
- `scripts/*.py` 可在 E2B sandbox 中执行。
- skill 的创建、上传、加载、更新、删除链路已经跑通。
- `PUT update` 语义已验证稳定：`skill_id` / `share_code` 稳定，`version` 递增，bundle 完全替换。
- skill 删除后 DB 级失效，但 E2B 本地缓存不会立即自动清除。

### 2.2 已确认的 browser-mediated cross-space interaction 原型

- transcript 的 T02-T04 不是 `user-relay`，而是 `browser-mediated`。
- 这些轮次的物理传输由 Tabbit agent 自己通过浏览器控制工具完成，包括读取网页输出、滚动/快照观察、定位输入区、发送消息和回收后续测试指令。
- 这证明当前能力边界不只是“两个 agent 通过用户转述协作”，而是已经出现了“Tabbit agent 以浏览器用户身份读取和操控网页 GPT 对话”的原型能力。
- 用户从 T05 才开始显式介入，原因是这条自动化链路当时仍偏慢、容易卡在工具调度循环，且缺少稳定的完整性判断和恢复规范，而不是因为此前轮次没有自动跨空间交互能力。

### 2.3 推荐的 AgentNexus 集成形态

当前接受的集成形态是双形态：

```text
repo source of truth
└── tabbit-agentnexus-skill/
    ├── SKILL.md
    ├── browser-scripts/
    ├── scripts/
    ├── references/
    ├── examples/
    └── assets/

build output
└── dist/
    └── tabbit-agentnexus-<version>.tar.gz
```

对应职责分工：

- Tabbit skill：浏览器侧 orchestration layer，负责网页 DOM 读取、页面交互、轻量数据处理、handoff 协议执行和浏览器内分发。
- 本地仓库 agent：负责本地文件读写、测试、`git diff`、`git commit` 和正式文档同步。
- 仓库源码版：承担长期版本控制和 source of truth。
- Tabbit 发行版：承担用户侧加载与运行。

这套分工还应补上一条关键含义：

- Tabbit skill 不只是“浏览器内脚本打包物”，它还可以成为 `Web Agent ↔ Browser Agent` 协作中的浏览器侧 relay / orchestration layer。

### 2.4 应保守表述的边界

- `allowed_tools` 很可能是声明性元数据，而不是强安全边界；由于未创建 `allowed_tools=[]` 的独立 skill 做隔离测试，该结论应视为 `high-confidence inferred`，工程上不得依赖它作为安全隔离机制。
- `url_patterns` 已证实会写入后端元数据，但 UI 层自动推荐 / 自动触发行为仍未完全证成。
- Tabbit skill 的 confirmed size limit 仍是 `unknown`；packager 与 upload script 中未发现硬编码限制，底层对象存储限制不能直接写成 Tabbit confirmed limit。
- `browser-mediated cross-space interaction` 当前只可视为原型级能力，不应提前写成“稳定、快速、低误判的默认 transport layer”。

## 3. 本次实际验证覆盖了什么

| 验证面 | 结果 |
|---|---|
| T02-T04 非 user-relay，而是 browser-mediated cross-space interaction | ✅ 已确认到原型级 |
| 统一 bundle 结构 | ✅ 已确认 |
| `SKILL.md` 必需性 | ✅ 已确认 |
| `.tar.gz` 打包与上传 | ✅ 已确认 |
| browser JS 运行时 | ✅ 已确认 |
| E2B Python 运行时 | ✅ 已确认 |
| skill 更新语义 | ✅ 已确认 |
| 删除与清理行为 | ✅ 已确认到 DB 级失效 / 缓存残留 |
| `url_patterns` 写入后端 | ✅ 已确认 |
| `allowed_tools` 强隔离语义 | ⚠️ 未完全确认 |
| 实际大小限制阈值 | ⚠️ 未确认 |
| share_code 删除后的跨账号行为 | ⚠️ 未确认 |
| 用户侧 UI 是否接受 zip/md/json | ⚠️ 未确认 |

## 4. 对 AgentNexus 的正式影响

### 4.1 可以接受的设计前提

- AgentNexus 可以把 Tabbit skill 当作正式浏览器侧入口来设计。
- 浏览器端 JS 与 E2B Python 的组合足以覆盖 v0 所需的网页上下文抽取、轻量处理与 artifact 生成。
- `Web Agent ↔ Browser Agent` 之间已经出现一条可工作的 `browser-mediated cross-space interaction` 原型，因此“浏览器代理直接读取和操控网页 GPT 对话页”可以作为正式设计输入，而不必再退回到“默认只能靠用户逐轮转述”。
- 仓库中仍应保留 repo-native 的源码结构和测试入口，而不是把 Tabbit skill 当作唯一 source of truth。

### 4.2 不应误用的设计前提

- 不应把 E2B Python 等同于用户本地仓库 Python。
- 不应让 Tabbit skill 替代本地仓库 agent 承担真实 repo 写入、测试与 git 责任。
- 不应把“原型级 browser-mediated cross-space interaction 已出现”误写成“这条自动化链路已经稳定、快速、可无人治理”。
- 不应把 `allowed_tools` 当成强权限边界。
- 不应把“删除 skill”误写成“所有沙箱缓存立即清除”。

## 5. 当前建议的最小文件结构

```text
tabbit-agentnexus-skill/
├── SKILL.md
├── browser-scripts/
│   └── nexus_orchestrator.js
├── scripts/
│   └── data_processor.py
├── references/
│   └── handoff_protocol.md
└── examples/
    └── sample_workflow.md
```

这个最小结构表达的不是最终目录冻结，而是当前已被验证支撑的最小闭环：

- `SKILL.md`：任务边界、调用时机、workflow、能力路由
- `browser-scripts/`：网页上下文读取、DOM 交互、handoff 执行
- `scripts/`：E2B sandbox 内的轻量数据处理与 artifact 生成
- `references/`：跨 agent 协议与 contract
- `examples/`：典型任务样例

## 6. 已知限制

- 本报告只收口 Tabbit skill 架构边界和 AgentNexus 的推荐集成形态，不代表 v0 设计本身已经完成。
- `browser-mediated cross-space interaction` 的关键发现是“能力已出现”，不是“稳定性问题已解决”；速度、调度卡顿、输出完整性判断和恢复策略仍需后续治理。
- transcript 中包含一段历史性的“四角色两空间纠偏”过程，但当前默认协作模型的正式真值仍以后续报告和正式 workflow 为准。
- 用户侧 UI 的上传格式、自动推荐细节和部分权限边界仍需后续针对性验证。

## 7. 与 Transcript 的关系

- `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md`
  - 保留了从初始误判、端到端 probe、外部 review，到最终纠偏与收口建议的完整原始过程。
  - 其中 `Relay` 字段和 `3.2 关键说明` 已明确 T02-T04 属于 `browser-mediated`，T05 才转入用户显式中介。

本报告负责把 transcript 中已经足够稳定的部分提升为 accepted 结论；transcript 继续作为历史证据保留，但不替代正式架构和正式 workflow 入口。
