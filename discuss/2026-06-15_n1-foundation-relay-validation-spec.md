# N1 AgentNexus Foundation, Relay, and Validation Spec

> Status: Phase 1-4 repo-side done / Phase 3 browser-side pending
> Created: 2026-06-15
> Spec type: workflow
> Profile: nexus-default
> Supersedes: `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md` for current planning
> Depends on:
> - `docs/architecture/nexus_runtime_architecture.md`
> - `docs/architecture/tabbit_browser_agent_behavior_boundary.md`
> - `docs/PROJECT_MEMORY.md`
> - `docs/reports/20260615_tabbit_skill_architecture_boundary_diagnosis.md`
> - `docs/reports/20260615_tabbit_browser_workspace_limitation_boundary_diagnosis.md`

## Summary

把上一版“单纯 N1 Local Workspace Review Adapter”升级为：

```text
N1 AgentNexus foundation + browser-mediated relay prototype + repo execution governance + validation
```

也就是说，本 spec 不再只设计“本地仓库 review adapter”，而是把 Tabbit agent 已经能以浏览器用户身份与网页 GPT 交互这条原型链路正式纳入第一阶段开发对象，并显式承认当前仓库推进采用 supervised four-role development model。三条线并行收口：

```text
A. Repo-side foundation
   本地仓库读取、policy、redaction、context pack、audit、测试

B. Browser-mediated relay foundation
   Tabbit agent 读取网页 GPT 输出、输入消息、点击发送、等待完整输出、回收结果

C. Supervised four-role development workflow
   User + Web Agent + Browser Agent / Tabbit Agent + Repo / Code Agent 在有人监督下推进实现、测试和验收
```

## Scope

### In scope

- 显式化 two-layer actor model：product target runtime model（`Web Agent ↔ Browser Agent` 核心双 Agent 协作环）与 current repository development model（supervised four-role）。
- Repo-side foundation 的能力盘点与缺口表格化（policy / redaction / context pack / audit / runner），并把后续 Phase 2/4 的 repo-side relay 实现与本 spec 对齐。
- Browser-mediated cross-space interaction 作为开发对象（而非仅“发现”）：14 步 relay ledger、message envelope、completeness 判断、retry / fallback / 用户介入出口规则。
- Repo / Code Agent execution governance：明确其在当前仓库阶段是主要 implementation executor，但只接明确指令、必须返回 diff / tests / commit evidence。
- Supervised four-role development workflow 的阶段化测试流程。
- 四层测试矩阵：repo-side unit、repo-side integration dry run、browser-mediated relay supervised test、multi-agent agreement test。
- 旧 M1 Repo Review Bridge spec 标记 legacy / superseded 的迁移路径。

### Out of scope

- 把 `browser-mediated cross-space interaction` 当作稳定 transport layer。它当前仍是原型，速度、工具调度卡顿、输出完整性判断和异常恢复仍需治理。
- 无人值守闭环（unbounded autonomous loop）。当前必须带轮次上限、权限上限、失败上限和人工确认出口。
- 双 agent 自运行（assume `Web Agent ↔ Browser Agent` 可在不监督下自跑）。
- N2+ 能力：action parsing、patch proposal、repo write / apply、command execution、official publishing、multi-site 通用适配。
- 假设可枚举全部标签页、可切回任意旧标签页实例、或旧实例的滚动位置 / 输入状态 / 历史栈被保留。
- 本轮不修改正式 architecture 文档。边界已在前序 commit（`b01ec38` 等）固化，本轮只是执行 spec。
- 本 spec 的创建阶段不直接实现 relay / foundation 代码；后续 Phase 2/4 已按本 spec 落地 repo-side relay protocol modules。Browser-side live relay 仍不在 Repo Agent 可单独完成范围内。

## Current Context

- 当前已知事实：
  - `docs/reports/20260615_tabbit_skill_architecture_boundary_diagnosis.md` 已确认 T02-T04 是 `browser-mediated cross-space interaction`，不是 `user-relay`；用户从 T05 才开始显式介入，原因是链路偏慢、工具调度卡顿、缺少稳定完整性判断，而不是此前轮次没有自动跨空间交互能力。
  - Tabbit agent 已出现原型能力：可以以浏览器用户身份读取网页 GPT 输出、定位输入区、发送消息、回收后续响应。该能力已被 `readme.md`、`nexus_runtime_architecture.md` §2.1、`tabbit_browser_agent_behavior_boundary.md` §4.3.2 和 `PROJECT_MEMORY.md` 的 `Browser-Mediated Cross-Space Interaction Prototype` 条目吸收。
  - 该能力当前仍只是原型，不得写成稳定 transport。每份涉及文档都保留“prototype only / not stable contract”限定词。
  - 当前产品目标模型是 `Web Agent ↔ Browser Agent / Tabbit Agent` 核心双 Agent 协作环；`Repo / Code Agent` 是外部执行端，只在收到明确指令后承担仓库修改、测试、diff 收口与提交证据返回。
  - Tabbit browser workspace 是有限标签页控制模型：不能枚举全部标签页、不能切回任意未掌握真实 ID 的旧标签页、URL restore 可用但不保留旧实例状态。
- 相关正式入口：
  - `readme.md`
  - `AGENTS.md`
  - `docs/architecture/nexus_runtime_architecture.md`
  - `docs/architecture/tabbit_browser_agent_behavior_boundary.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/agent_conventions.md`
  - `docs/workflows/discuss_spec_workflow.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`（predecessor，本轮标记 legacy / superseded）
  - `docs/reports/20260615_tabbit_skill_architecture_boundary_diagnosis.md`
  - `docs/reports/20260615_tabbit_browser_workspace_limitation_boundary_diagnosis.md`
  - `docs/reports/transcripts/20260615_tabbit_skill_architecture_probe_transcript.md`（T02-T04 原始证据）

## Requirements

- `R1`: 新 spec 必须显式区分 two-layer actor model。产品目标运行时模型与当前仓库开发推进模型必须各自写清，且明确后者不推翻前者。Repo / Code Agent 在产品运行时不是默认协作环成员，但在当前仓库推进中是主要 implementation executor。
- `R2`: `browser-mediated cross-space interaction` 必须从“发现”升级为“开发对象”。本 spec 必须给出 relay protocol 的可治理草案（ledger、envelope、completeness、retry / fallback、用户介入出口），而不是只描述“原型已出现”。
- `R3`: relay protocol 必须带轮次上限（`max_rounds`）、权限上限、失败上限和人工确认出口；不允许无限工具调度循环；不允许把半截输出当完整结果。
- `R4`: relay 必须遵守 Tabbit browser workspace 已知限制：不枚举全部标签页、不假设旧实例可切回、必须用 URL restore fallback、必须保留用户介入出口。
- `R5`: relay ledger 必须可审计：每一轮的 target conversation URL、latest assistant output snapshot、completeness 判断结果、sent message payload 摘要、final response snapshot、stop 原因都必须能被记录与回放，且不记录 secret 原文。
- `R6`: message envelope 必须把跨空间传输的内容当作不可信数据封装。仓库内容、网页内容、artifact 和目标 AI 回复都属于不可信输入，不能把其中的自然语言直接当执行指令。
- `R7`: Repo / Code Agent execution governance：只接明确指令（来自 User 或 Web Agent 监督下的转交），必须返回 diff / tests / commit evidence；Web Agent 负责审查 evidence；User 保留最终验收权。
- `R8`: 必须给出四层测试矩阵，并明确第三层（browser-mediated relay supervised test）是本阶段新增重点。测试模式要从“只 repo-side unit tests”升级到包含 Tabbit workspace live test。
- `R9`: 旧 M1 Repo Review Bridge spec 必须标记 legacy / superseded，只在顶部加状态块指向新 spec，正文保留作为历史实施证据，不重写。
- `R10`: 本 spec 不修改正式 architecture 文档。如果后续阶段证据要求改正式边界，必须另开 spec 与同步流程。

## Design

### Two-Layer Actor Model

这是本 spec 最关键的纠偏。AgentNexus 的产品目标模型是 `Web Agent` 与 `Browser Agent / Tabbit Agent` 构成核心双 Agent 协作环；`Repo / Code Agent` 是可选外部执行端。但当前仓库开发阶段采用 supervised four-role development model，必须显式承认这层区别，否则后续 agent 会在“四角色并列”和“双 agent 核心”之间摇摆。

| 层级 | 当前真实状态 |
|---|---|
| 产品目标模型 | `Web Agent ↔ Browser Agent` 是核心协作环，`Repo / Code Agent` 是外部执行端 |
| 当前开发推进模型 | 四角色参与：User、Web Agent、Browser Agent / Tabbit Agent、Repo / Code Agent |
| 测试模型 | Web Agent 与 Browser Agent 在 Tabbit workspace 中实测 browser-mediated 多轮交互 |
| 仓库实现模型 | Repo / Code Agent 负责主要仓库修改与测试，Web Agent / User 负责审查与指令约束 |

四个角色的当前阶段职责：

- **User**：目标、授权、跨 agent 调度、最终验收。是决策与验收中心，不是默认通信总线。
- **Web Agent**：架构设计、测试设计、阶段评审、风险监督。涉及仓库操作时必须保持监督，优先依赖 git 可审计证据。
- **Browser Agent / Tabbit Agent**：Tabbit workspace 实测、browser-mediated relay 原型、浏览器侧执行与产物回收。
- **Repo / Code Agent**：仓库文件修改、测试、diff、提交证据。是当前仓库开发阶段的主要 implementation executor，但不是产品运行时的自治决策者。

```text
Given: 后续 agent 读到本仓库的架构文档
When: 它看到 "Repo / Code Agent 是外部执行端" 与 "当前仓库推进主要靠 Repo Agent 实现" 两层表述
Then: 两层不冲突：前者是产品运行时模型，后者是当前仓库开发推进模型；必须在各自语境下理解，不能混用。
```

```text
Given: Web Agent 与 Browser Agent 在 Tabbit workspace 中进行 browser-mediated 多轮交互
When: 链路偏慢、卡在工具调度循环或缺少完整性判断
Then: 用户可临时介入中转与纠偏；这不代表 browser-mediated 能力不存在，只代表当前仍需监督与可靠性治理。
```

```text
Given: Repo / Code Agent 完成一批仓库修改
When: 提交结果给 Web Agent
Then: 必须附带 diff、测试结果和 commit evidence；Web Agent 审查后才能进入下一轮或交付用户验收。
```

### Foundation Architecture

#### Repo-side foundation

下表盘点 Phase 1（2026-06-15）时的当前基线。所有 sandbox 脚本都是 dual-purpose：既能作为 argparse CLI（带 `--help`），也暴露可被单元测试直接导入的 library 函数。基线已通过 `python -m pytest -q`（22 passed）与两个 CLI 的 `--help` 验证。

状态标记：✅ = 已落地且有测试覆盖；🟡 = 已落地但测试覆盖有缺口；⚪ = 配置/脚手架文件，靠下游间接覆盖。

| Component | Path | Current status | Responsibility | Test coverage | Gap | Next phase |
|---|---|---|---|---|---|---|
| Repo discovery | `scripts/discover_repo.py` | ✅ dual-purpose | `discover_repo(repo_root)` 返回 exists / is_dir / git_dir_present / resolved path | `test_discover_repo.py`（1 test） | 无实质缺口 | T3+ relay 不依赖此模块 |
| Git probe | `scripts/git_probe.py` | ✅ dual-purpose | 只读 git 元数据：`probe()` 返回 branch / status / recent_commits，git 不可用时优雅降级 | `test_git_probe.py`（3 tests：unavailable / not-a-repo / timeout） | 无实质缺口 | T3+ relay 不依赖此模块 |
| Path policy | `scripts/policy.py` | ✅ dual-purpose | `load_default` + `decide_path` 实现 deny-before-allow + realpath containment | `test_policy.py`（3 tests：allow / deny-glob-wins / outside-repo） | 仅测了 `decide_path`/`load_default`，`create_session` 未直接测 | 低优先级 |
| Secret redaction | `scripts/redact.py` | ✅ dual-purpose | `redact_text` + `scan_file`：4 类 secret pattern + 二进制检测 | `test_redact.py`（3 tests） | pattern 集较保守，可能漏新型 secret | 留待 evidence 驱动扩展，不在本轮 |
| Context packager | `scripts/context_packager.py` | ✅ dual-purpose | `build_context_pack` 组装 markdown，强制 caps、跳过 binary/oversized、套 untrusted banner | `test_context_packager.py`（3 tests） | 无实质缺口 | T3+ relay envelope 可复用其 manifest 结构 |
| Audit log | `scripts/audit_log.py` | ✅ dual-purpose | `append_event`（JSONL）+ `write_session_summary`（JSON） | `test_audit_log.py`（2 tests） | 无实质缺口 | T3+ relay ledger 复用 append_event 落盘 |
| Session runner | `scripts/n1_review_session.py` | ✅ dual-purpose | composition root：串联 6 个模块，生成 `context_pack.md` + `audit.jsonl` + `session_summary.json`，停在 `ready_to_send` | `test_n1_review_session.py`（7 tests：success / denied-only / redaction / no-git / artifact-fallback / no-write / summary round-trip） | 仅 local-only 路径；browser submit / capture 未实现（符合 N1 边界） | T4 browser-backed dry run |
| Review-only policy | `config/default_policy.review_only.json` | ⚪ data | 单一 policy 源：`review_only`、caps、allow/deny globs | 间接（经 `load_default` 被三个 test 文件覆盖） | 无直接测试，但作为数据文件可接受 | 低优先级 |
| Repo-context exporter | `scripts/tools/package_nexus_context.py` | 🟡 dual-purpose | 独立工具：打 zip 给外部 AI 评审，不导入 N1 sandbox 模块 | **无测试** | 完全未覆盖（CLI 与 library 路径都未测） | 建议在独立 phase 补 smoke test，不阻塞 relay |
| N1 skill scaffold | `.agent/skills/nexus-local-workspace-review/` | ⚪ scaffold | 4 文件：`SKILL.md` + `agents/openai.yaml` + `references/browser_adapter_contract.md` + `templates/review_request.md` | 无（非可执行代码） | browser adapter contract 仅为 reference，未落到可执行 harness | T4 实现时落地 |
| Test suite | `tests/` | ✅ green | 8 个 test 文件 + `conftest.py`（sys.path 引导）+ 4 个 fixture repo | `pytest -q` → 22 passed | CLI `main`/`parse_args` 路径未测；仅测 library 入口 | 低优先级，CLI 已用 `--help` 手测 |

**基线不变式（Phase 1 确认仍成立）**：`no_write_repo`、`redaction_before_send`、`no_action_execution`、`path_containment`、`deny-before-allow`、`explicit context caps`（`max_total_context_bytes=2_000_000` / `max_file_bytes=200_000` / `max_file_count=64`）。

**本轮结论**：repo-side foundation 的 6 个 sandbox 脚本 + session runner + test suite 已构成可审计、可复现的 local-only 基线，`ready_to_send` closure 成立。唯一测试覆盖缺口是 `scripts/tools/package_nexus_context.py`（独立 export 工具，不属于 review-only runtime，不阻塞 relay，建议单独 phase 补 smoke test）。browser submit / capture、relay ledger、agreement test 仍属后续 phase，符合 Out of scope。

#### Tabbit skill / browser-side foundation

- Tabbit skill 是统一 bundle 模型（`SKILL.md` + `.tar.gz` 发行版），不是“提示词 / 脚本 / 任务”三种独立类型。
- Tabbit skill 不只是浏览器内脚本打包物，它还是 `Web Agent ↔ Browser Agent` 协作中的浏览器侧 relay / orchestration layer。
- 它不替代本地仓库 agent 承担真实 repo 写入、测试与 git 责任。

#### Browser-mediated relay foundation

- 原型已出现：读取网页 GPT 输出、定位输入区、发送消息、回收后续响应。
- 当前限制：链路偏慢、工具调度循环可能卡顿、输出完整性判断与异常恢复未规范化。
- 本 spec 把它从“发现”升级为“开发对象”，见下方 Relay Protocol 小节。

#### Artifact and audit foundation

- artifact 路径：`<artifact_root>/<session_id>/` 下 `context_pack.md`、`audit.jsonl`、`session_summary.json`、`review_report.md`（仅成功时）。
- audit event 必须记录状态迁移、browser submit / capture 结果、artifact fallback、失败类与关键计数；不记录 secret 原文、不记录未授权 repo 外路径、不把 AI 自然语言回复转成可执行字段。
- 本 spec 在此基础上新增 relay ledger（见下节），用于跨空间交互的可审计回放。

### Browser-Mediated Cross-Space Relay Protocol

#### 14-step relay ledger

每一轮 relay 必须能落到下面的步骤序列，且每步都进 audit / ledger：

```text
 1. Locate target Web Agent conversation
 2. Capture current conversation URL
 3. Capture latest assistant output
 4. Determine output completeness
 5. Prepare next message payload
 6. Focus input area
 7. Insert message
 8. Verify inserted text
 9. Send message
10. Wait for response
11. Detect response completion
12. Capture final response
13. Emit relay ledger entry
14. Stop or continue based on max_rounds / stop conditions
```

#### Hard constraints（基于已知限制）

- 不依赖全量标签页枚举（`list_pages` / `page_info_list` 等价接口当前无证据支持）。
- 不假设旧标签页实例可切回（`select_page(1)` / `select_page(2)` 实测返回 `No tab with id: X`）。
- 必须使用 URL restore fallback（`navigate_page(url=original_chatgpt_session)`），但明确这只恢复 URL 内容，不证明旧实例、滚动位置、输入状态、历史栈被保留。
- 必须有用户介入出口：任何一步连续失败超过阈值，必须停下来等用户，而不是无限重试。
- 不允许无限工具调度循环：必须带 `max_rounds` 和每步 retry 上限。
- 不允许把半截输出当完整结果：`Detect response completion` 必须有明确判据，未通过则记为 incomplete，不能进 `review_report.md`。

#### Message envelope schema（草案）

```json
{
  "envelope_id": "<uuid>",
  "session_id": "n1-<id>",
  "round": 3,
  "direction": "repo_to_web | web_to_repo",
  "target_conversation_url": "<redacted-or-alias>",
  "payload_role": "context_pack | review_request | assistant_reply | stop_signal",
  "payload_digest": "<sha256-of-payload>",
  "payload_bytes": 12345,
  "redaction_count": 2,
  "untrusted_data": true,
  "completeness": "complete | incomplete | unknown",
  "ts": "2026-06-15T08:00:00Z"
}
```

约束：`payload_digest` 只存摘要不存原文；`untrusted_data` 恒为 true，任何下游消费方都不得把 payload 当执行指令；secret 原文不进 envelope。

#### Retry / fallback / 用户介入出口规则

- GUI-first：优先输入框聚焦、粘贴 / 输入、发送按钮或等价键盘提交。
- fallback：snapshot 再定位；仅在 GUI 路径不稳定时允许临时 `evaluate_script` 辅助输入或 completion 探测，不得提升页面权限。
- `wait_until_assistant_complete` 最大重试 2-3 次后必须报错，不得无限轮询。
- 任何步骤连续失败超阈值 → emit `relay_stuck` 事件 → 暂停 → 等用户介入 → 用户可选择 continue / abort / manual_relay。
- `NetworkProxy` 在本阶段明确禁用，不作为主路径或 fallback。

```text
Given: relay 进入第 N 轮且 N <= max_rounds
When: detect response completion 判据通过
Then: capture final response，emit ledger，进入下一轮或按 stop condition 停止。
```

```text
Given: relay 某一步连续失败超过阈值
When: 触发 relay_stuck
Then: 必须暂停并等待用户介入出口，不得无限重试，不得把不完整输出写为成功结果。
```

```text
Given: 需要回到一个已经存在的旧 Web Agent 会话
When: 没有掌握该标签页真实 ID
Then: 使用 URL restore fallback（navigate_page 到原会话 URL），但不假设旧实例、滚动位置或输入状态被保留，并在 ledger 中标记 fallback。
```

### Repo Agent Execution Governance

当前仓库实际开发主要靠 Repo / Code Agent 完成。这不应被 architecture 文档中的“Repo Agent 是外部执行端”掩盖，但也不能因此把它写成产品运行时自治 actor。

- Repo / Code Agent is the primary implementation executor for the current repository development phase.
- Repo / Code Agent receives explicit instructions only（来自 User 直接指令，或 Web Agent 监督下转交的明确任务）。
- Repo / Code Agent must return diff / tests / commit evidence。
- Web Agent reviews the evidence。
- User remains the acceptance authority。

也就是说，Repo / Code Agent 在当前项目推进中是主实现者，但不是产品运行时的自治决策者。

```text
Given: Repo / Code Agent 收到一批仓库修改任务
When: 完成修改
Then: 必须返回 diff、测试结果和 commit evidence；未附带 evidence 的结果不能进入 Web Agent review。
```

```text
Given: Web Agent 审查 Repo / Code Agent 的 evidence
When: 发现未覆盖测试、越界改动或与正式边界冲突
Then: 退回 Repo / Code Agent 修正，不直接交付用户验收。
```

### Supervised Test Workflow

四角色在 Tabbit workspace 中的 supervised 测试流程：

1. Web Agent 设计测试任务与 stop condition。
2. Browser Agent / Tabbit Agent 在 Tabbit workspace 中实际执行（读取、投递、回收）。
3. 用户监督，并在卡住时通过用户介入出口介入。
4. 保存 transcript / relay ledger / report。
5. Web Agent 与 Repo / Code Agent 根据 evidence 总结稳定性问题与缺口。
6. 稳定结论升级到 `docs/reports` 或 `docs/workflows`；未稳定结论留在 `discuss/`。

本阶段不追求无人值守，先追求可审计、可复现。

```text
Given: Web Agent 与 Browser Agent 在 Tabbit workspace 中进行多轮 browser-mediated 交互
When: 达成 stop condition（共识或分歧）
Then: 输出 agreement 或 disagreement report，连同 relay ledger 一起保存，供用户验收。
```

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - 新建本 spec：`discuss/2026-06-15_n1-foundation-relay-validation-spec.md`。
  - 旧 spec 顶部状态块改为 legacy / superseded：`discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`（只改顶部，不重写正文）。
  - 更新 discuss 索引：`discuss/README_discuss.md`（新增行 + 旧行 status 更新 + 当前状态小节同步）。
  - relay repo-side 已在后续 phase 落地：`scripts/relay_constants.py`、`scripts/message_envelope.py`、`scripts/relay_ledger.py`、`scripts/relay_completeness.py`、`scripts/relay_runner.py` 与 relay 模板；browser-side harness 与 live test 仍待 T4。
- 明确不会碰哪些部分：
  - 不修改正式 architecture 文档（`docs/architecture/**`）。
  - 不修改 `AGENTS.md`、`docs/PROJECT_MEMORY.md`（本轮未改 repo-wide rules 或 durable architecture decision）。
  - 不在 Repo Agent 侧实现 browser live relay 执行。
  - 不进入 N2+ action / patch / write / command。
  - 不假设全量标签页枚举或旧实例切换。

## Execution Plan

- [x] `T1` Phase 0 文档重置：新建本 spec、旧 M1 spec 标记 legacy / superseded、更新 `discuss/README_discuss.md` 索引与当前状态。
- [x] `T2` Phase 1 Repo-side foundation consolidation：梳理现有 `scripts/`、`tests/`、`.agent/skills/`，确认 N1 runner 当前能力，把已完成项与缺口表格化。重点不是重写代码，而是把当前 foundation 状态表格化。
- [x] `T3` Phase 2 Relay protocol 设计：设计 browser-mediated relay ledger schema、message envelope、response completeness 判断、retry / fallback / 用户介入出口规则。已落地为 `scripts/relay_constants.py`、`scripts/message_envelope.py`、`scripts/relay_ledger.py`、`scripts/relay_completeness.py` 四个 dual-purpose 模块 + 对应单元测试。
- [ ] `T4` Phase 3 Tabbit workspace supervised test：由 Web Agent 设计测试任务，Browser Agent 在 Tabbit workspace 中实际执行，用户监督并在卡住时介入，保存 transcript / relay ledger / report，总结稳定性问题。不追求无人值守，先追求可审计、可复现。
  - `T4-A2` repo-side evidence-quality fix：使用 `config/default_policy.t4_implementation_verification.json` 收窄 implementation-verification context，同时要求调用方从 `session_summary.json` 读取 `actual_artifact_root` 与 `artifacts.context_pack`，不要把 `exports/...` mirror 路径当 source of truth。
- [x] `T5` Phase 4 Repo Agent implementation：Repo / Code Agent 根据新 spec 修改仓库，增加模板、协议、ledger schema、测试。已落地 `scripts/relay_runner.py`（relay 集成入口）、`templates/relay_message_repo_to_web.md`（跨空间 relay 模板）+ 5 个新测试文件（44+5=49 个 relay 相关测试用例，全量 71 passed）。
- [ ] `T6` Phase 5 闭环验收：Web Agent 评审 Repo Agent 结果，Browser Agent 做 Tabbit workspace 实测，用户验收，稳定结论升级到 `docs/reports` 或 `docs/workflows`。

## Validation

测试矩阵分四层（第三层是本阶段新增重点）：

- `V1`: Repo-side unit tests — 验证 policy、redaction、context pack、audit、runner（继承 predecessor spec 的 V1-V13）。
- `V2`: Repo-side integration dry run — 验证 N1 review session 能生成完整 handoff artifact（`context_pack.md` + `audit.jsonl` + `session_summary.json`，`ready_to_send` 状态）。
- `V3`: Browser-mediated relay supervised test — 验证 Tabbit agent 能把 Web Agent 输出读出、投递下一轮、回收结果；relay ledger 14 步可被记录与回放；`relay_stuck` 用户介入出口可用。
- `V4`: Multi-agent agreement test — 验证 Web Agent 与 Browser Agent 能在有限轮次（`max_rounds`）内达成共识或输出分歧报告。

标准工程验证（每个非平凡改动都要带）：

- `V5`: `python -m py_compile <edited_python_files>`（若改了 Python）。
- `V6`: `python <script> --help`（若改了 CLI）。
- `V7`: `git diff --stat` 确认只动了预期文件。
- `V8`: 新 spec 章节齐全（10 个 `##` + 状态块 4 字段 + Supersedes / Depends on）。
- `V9`: 新 spec 引用的 5 个 dependency 文件路径全部存在。
- `V10`: 旧 M1 spec 正文未被重写（`git diff` 只显示顶部状态块改动）。

## Implementation Report

### Completed

- 创建本 spec，把上一版“单纯 N1 Local Workspace Review Adapter”升级为“N1 AgentNexus foundation + browser-mediated relay prototype + repo execution governance + validation”。
- 显式化 two-layer actor model：产品目标运行时模型（`Web Agent ↔ Browser Agent` 核心双 Agent 协作环 + Repo 外部执行端）与当前仓库开发推进模型（supervised four-role: User + Web Agent + Browser Agent + Repo Agent）。
- 把 `browser-mediated cross-space interaction` 从“发现”升级为“开发对象”，给出 14 步 relay ledger、message envelope schema 草案、retry / fallback / 用户介入出口规则。
- 明确 Repo / Code Agent execution governance：当前阶段主实现者，但只接明确指令、必须返回 evidence、Web Agent review、User 验收。
- 给出四层测试矩阵，并标注第三层（browser-mediated relay supervised test）为本阶段新增重点。
- 指明旧 M1 Repo Review Bridge spec 的迁移路径（标记 legacy / superseded，不重写正文）。
- Phase 1 Repo-side foundation consolidation：在 `Foundation Architecture / Repo-side foundation` 下落地 foundation status table（11 行组件，覆盖 6 个 sandbox 脚本、session runner、policy 配置、repo-context exporter、skill scaffold、test suite），确认基线不变式仍成立，记录唯一测试覆盖缺口（`scripts/tools/package_nexus_context.py` 无测试，属独立 export 工具不阻塞 relay）。
- Phase 2 Relay protocol 设计落地：将 spec 草案的 14 步 relay ledger、message envelope schema、completeness 检测、retry/fallback 规则落地为 4 个 dual-purpose Python 模块（`relay_constants.py`、`message_envelope.py`、`relay_ledger.py`、`relay_completeness.py`） + 44 个单元测试用例，全部通过。
- Phase 4 Repo Agent implementation：新增 `scripts/relay_runner.py`（N1 session → relay handoff 集成入口）、`templates/relay_message_repo_to_web.md`（跨空间 relay 模板） + 5 个 runner 测试用例。全量测试：71 passed。
- Phase 2/4 minor hardening（2026-06-16）：修正 active spec 中“已实现 / 不实现”并存的残留表述；为 `message_envelope.py` 补齐 SHA-256 / 非负数 / completeness / `session_id` 校验；为 `relay_ledger.py` 的 library 入口补齐 round / step / status / duration 强校验；为 `relay_runner.py` 增加模板渲染输出（`--template` / `--message-output`）并同步 `nexus-local-workspace-review` skill 的 relay handoff 用法。

### Not completed

- Phase 3 Tabbit workspace supervised test 尚未执行（依赖 Browser Agent 在 Tabbit workspace 中实际执行 browser-mediated 交互，Repo Agent 无法单独完成）。
- Phase 5 闭环验收尚未执行（依赖 Web Agent 评审 + Browser Agent 实测 + User 验收）。

### Notes

#### Phase 1 Validation（2026-06-15）

本轮实际跑过的自动验证：

- `python -m pytest -q` → `22 passed`（8 个 test 文件覆盖 6 个 sandbox 脚本 + session runner；cache 写入警告与本轮无关，是 `.pytest_cache` 写权限，不影响结果）。
- `python scripts/n1_review_session.py --help` → 正常输出 6 个参数（`--repo-root` / `--artifact-root` / `--policy` / `--session-id` / `--review-request-file` / `-h`）。
- `python scripts/tools/package_nexus_context.py --help` → 正常输出 4 个参数（`--profile` / `--output-dir` / `--output` / `--git-commits`）。
- `git diff --stat` → 本轮只动 `discuss/2026-06-15_n1-foundation-relay-validation-spec.md`（status table + Execution Plan + Implementation Report）。

本轮盘点确认的关键事实：

- 6 个 sandbox 脚本都是 dual-purpose（argparse CLI + library 函数），都有对应单元测试。
- `n1_review_session.py` 是 composition root，串联全部 6 个模块，7 个 runner 测试覆盖 success / denied-only / redaction / no-git / artifact-fallback / no-write / summary round-trip。
- `package_nexus_context.py` 是独立 export 工具，不导入 N1 sandbox 模块，**无测试**——这是唯一测试覆盖缺口，但不阻塞 relay（它不属于 review-only runtime）。
- 基线不变式（`no_write_repo` / `redaction_before_send` / `no_action_execution` / `path_containment` / `deny-before-allow` / explicit caps）在当前测试集下仍成立。

#### Phase 2 & 4 Validation（2026-06-15）

本轮 Repo Agent 实现的自动验证：

- `python -m pytest -q` → `71 passed`（22 original + 49 relay/runner tests，0 failures）
- `python scripts/relay_constants.py --help` → 正常输出（`--json` flag）
- `python scripts/message_envelope.py --help` → 正常输出（8 个参数）
- `python scripts/relay_ledger.py --help` → 正常输出（8 个参数 + 14 canonical step choices）
- `python scripts/relay_completeness.py --help` → 正常输出（3 个参数）
- `python scripts/relay_runner.py --help` → 正常输出（8 个参数）

#### Phase 2/4 Hardening Validation（2026-06-16）

本轮小修实际跑过的自动验证：

- `python -m pytest -q`
- `python -m py_compile scripts/message_envelope.py scripts/relay_ledger.py scripts/relay_runner.py`
- `python scripts/message_envelope.py --help`
- `python scripts/relay_ledger.py --help`
- `python scripts/relay_runner.py --help`
- `git diff --stat`

#### T4-A2 Evidence-Quality Note（2026-06-16）

- 为 T4 supervised retest 增加 bounded review profile：`config/default_policy.t4_implementation_verification.json`。它显式纳入 `config/**`、focused relay tests、core relay scripts 与当前 handoff skill/spec 所需最小入口，避免继续沿用过宽或过窄的默认 review-only context。
- `n1_review_session.py` 的 artifact fallback 语义保持不变：若请求的 `artifact_root` 位于 `repo_root` 内，则 session artifacts 会落到 repo 外 fallback root。后续 `relay_runner.py` 或报告脚本必须先读取 `session_summary.json`，以 `actual_artifact_root` 与 `artifacts.context_pack` 为准。
- T4 报告需要区分 actual artifact root 与复制/导出的 mirror 路径；mirror 只用于展示或归档，不应被误当成 live handoff 的 source path。

新增模块清单：

| Module | Tests | Purpose |
|---|---|---|
| `scripts/relay_constants.py` | 10 | 14-step IDs, thresholds, stop reasons, validators |
| `scripts/message_envelope.py` | 10 | Envelope build/validate, SHA-256 digest, untrusted flag |
| `scripts/relay_ledger.py` | 8 | Append-only JSONL ledger, step/round recording |
| `scripts/relay_completeness.py` | 16 | Structural + size-based completeness detection |
| `scripts/relay_runner.py` | 5 | N1 session → relay handoff integration |
| `templates/relay_message_repo_to_web.md` | — | Relay message template for cross-space handoff |

关键设计决策记录：

- All 4 relay modules follow the same dual-purpose pattern as existing sandbox scripts (argparse CLI + importable library).
- `message_envelope.py` enforces `untrusted_data=True` invariant; envelope carries only SHA-256 digest, never raw payload.
- `relay_completeness.py` checks end markers BEFORE minimum length (structural evidence is stronger than size heuristics).
- `relay_runner.py` is a composition root that ties N1 session output to relay envelope; it does NOT perform browser actions (those belong to Browser Agent/Tabbit).
- T4 (Phase 3 Tabbit workspace supervised test) explicitly blocked: requires Browser Agent in Tabbit workspace; Repo Agent cannot execute browser-mediated interactions.
- T6 (Phase 5 closed-loop acceptance) depends on T4 + Web Agent review.

#### Migration From Legacy M1 Bridge Spec

旧文档 `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md` 不再作为当前主入口，但只做顶部状态标注：

```text
> Status: legacy / superseded for current planning
> Successor: discuss/2026-06-15_n1-foundation-relay-validation-spec.md
> Note: 本文档记录原始 N1 Repo Review Bridge 实施计划。当前开发已推进到 AgentNexus N1 foundation + browser-mediated relay + supervised four-role development workflow。历史正文保留以供追溯，不再作为当前主入口。
```

不全量重写旧文档。它的 Execution Plan、Validation、Implementation Report 的历史勾选状态是重要的实施证据，必须保留。predecessor spec 仍是本 spec 的历史脉络来源，不是被否定的对象。

#### Open Questions

- relay ledger schema 的字段最小集是否足够？是否需要在 envelope 中加入 `parent_envelope_id` 用于多轮串联回放？
- response completeness 的判断阈值（轮询间隔、最大等待时长、completion 信号来源）如何确定？是否需要 per-site 的 completion 判据？
- multi-agent agreement test 的“共识”标准是什么？文本相似度、结构化字段匹配，还是人工判定？分歧报告的最小 schema 是什么？
- ~~Phase 1 的 foundation 状态表格应该写在本 spec 的后续修订，还是单独开一份 `docs/reports/` 诊断？~~ **已解决（Phase 1）**：写在 `Foundation Architecture / Repo-side foundation` 下，作为本 spec 的状态基线段落，不另开 report。
- 当前 supervised four-role development model 何时、以什么证据可以收敛回 product target runtime model？收敛条件是否应该写进 durable memory？

## Durable Sync

- 是否需要更新 `AGENTS.md`：否。本次没有改变 repo-wide agent rules。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：否。相关 durable 边界（browser-mediated 原型、two-agent-core、tab control 限制）已在前序 commit 固化；本 spec 只是执行规划，未新增 durable architecture decision。
- 是否需要更新 `docs/CHANGELOG.md`：是。需记录新 active spec 创建与旧 M1 spec 状态变更。
