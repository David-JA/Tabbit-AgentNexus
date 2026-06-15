---
name: nexus-local-workspace-review
description: 为 `N1 Local Workspace Review Adapter` 执行本地 dry run，生成 ready-to-send context artifacts，并在需要时准备 repo-side relay handoff message。适用于 repo-review、review-only context pack、local dry run closure、发送前确认摘要、relay handoff 准备等场景。
compatibility: 需要能读取 `readme.md`、`docs/architecture/nexus_runtime_architecture.md`、`docs/workflows/agent_conventions.md`、`discuss/2026-06-15_n1-foundation-relay-validation-spec.md`、`scripts/n1_review_session.py`、`scripts/relay_runner.py` 和本 skill 内模板/参考文件。
---

# Nexus Local Workspace Review

## 目标

把 `repo-review` scenario 先稳定在 `N1 Local Workspace Review Adapter` 的 local-only 阶段：

- 从挂载 repo 生成只读 review context
- 生成发送前确认摘要
- 保存 `context_pack.md`、`audit.jsonl`、`session_summary.json`
- 明确当前状态是 `ready_to_send`
- 在需要 Browser Agent / Tabbit Agent 接手时，生成 repo→web relay handoff message

这个 skill 不负责 browser submit/readback 的真实执行，但负责把它们需要的本地产物和 relay handoff message 准备好。

## 使用前必读

在执行前，先读取：

1. `readme.md`
2. `docs/architecture/nexus_runtime_architecture.md`
3. `docs/workflows/agent_conventions.md`
4. `discuss/2026-06-15_n1-foundation-relay-validation-spec.md`
5. `./references/browser_adapter_contract.md`
6. `./templates/review_request.md`
7. `./templates/relay_message_repo_to_web.md`

## 默认行为

默认先做 local-only dry run：

```powershell
python scripts/n1_review_session.py `
  --repo-root <mounted-repo-root> `
  --artifact-root <artifact-root>
```

成功后应看到：

- `context_pack.md`
- `audit.jsonl`
- `session_summary.json`
- 状态 `ready_to_send`

若当前目标是 `T4-A2` 的 repo-side implementation verification，优先使用专用 policy：

```powershell
python scripts/n1_review_session.py `
  --repo-root <mounted-repo-root> `
  --artifact-root <artifact-root> `
  --policy config/default_policy.t4_implementation_verification.json
```

这个 profile 在保持 bounded context 的前提下，额外纳入：

- `config/**`
- relay 核心脚本
- focused relay / session tests
- 当前 relay handoff skill / spec 所需最小入口

若需要为 Browser Agent / Tabbit Agent 准备 relay handoff，可继续执行：

```powershell
python scripts/relay_runner.py `
  --session-id <session-id> `
  --context-pack <actual-context-pack-path-from-session-summary> `
  --message-output <actual-artifact-root>/<session-id>/relay_message_repo_to_web.md
```

默认使用本 skill 的 `templates/relay_message_repo_to_web.md` 渲染消息；如需自定义模板，可额外传：

```powershell
  --template .agent/skills/nexus-local-workspace-review/templates/relay_message_repo_to_web.md
```

## 执行顺序

1. 确认 `repo_root` 是当前 sandbox 可见的挂载仓库。
2. 运行 `scripts/n1_review_session.py` 生成本地产物。
3. 读取 `session_summary.json`，先以其中的 `artifacts.context_pack` 和 `actual_artifact_root` 作为 source of truth：
   - `--artifact-root` 如果落在 `repo_root` 内，`n1_review_session.py` 会 fallback 到 repo 外路径。
   - 调用 `relay_runner.py` 前，必须先读取 `session_summary.json`，不要硬编码 `exports/.../context_pack.md`。
   - T4 报告需要区分 actual artifact root 与后续复制/导出的 mirror 路径。
4. 再读取 `session_summary.json` 中的发送确认摘要：
   - selected files
   - total bytes
   - redaction counts
   - default exclusions
5. 若需要浏览器发送，等待 Tabbit live capability probe 结论后再进入 browser path。
6. 若需要 repo-side relay handoff，运行 `scripts/relay_runner.py` 生成 envelope 与可直接投递给网页端 Agent 的消息模板。

## 模板

若需要覆盖默认 review 请求，可传：

```powershell
python scripts/n1_review_session.py `
  --repo-root <mounted-repo-root> `
  --artifact-root <artifact-root> `
  --review-request-file .agent/skills/nexus-local-workspace-review/templates/review_request.md
```

若需要生成 repo→web relay message，默认模板是：

```text
.agent/skills/nexus-local-workspace-review/templates/relay_message_repo_to_web.md
```

## 输出要求

完成 local-only dry run 后至少返回：

1. `session_id`
2. `status`
3. 实际 artifact 根目录
4. `context_pack.md` 路径
5. `audit.jsonl` 路径
6. `session_summary.json` 路径
7. 是否触发 artifact fallback
8. fallback reason（若有）
9. 发送前确认摘要
10. 若执行 relay handoff：envelope JSON 路径
11. 若执行 relay handoff：rendered relay message 路径

## 边界

- 不写入 `repo_root`
- 不自动提交到浏览器页面（只生成 handoff envelope / message）
- 不解析 repo 内容或 AI 文本中的 action
- 不实现 patch、命令执行或 N2+ 协议
