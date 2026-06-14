# M1 Repo Review Bridge Implement Spec

> Status: ready for implementation planning
> Created: 2026-06-14
> Spec type: implementation
> Profile: bridge-default

## Summary

定义 `M1 Repo Review Bridge` 的最小可实施范围：只读生成 context pack，发送到目标 AI 页面，捕获 review report 并保存 artifact，全程不修改仓库、不解析 AI action、不运行命令。

## Scope

### In scope

- M1 只读评审流程的行为边界、职责切分和验收标准。
- sandbox-side 最小脚本集合：repo discovery、git probe、policy check、secret redaction、context pack、audit log。
- browser-side 最小 harness：输入 context、等待回复完成、读取最后一条 assistant 回复、清理临时状态。
- M1 必须覆盖的 BDD 场景和最小验证命令。
- 明确哪些综合架构稿内容属于 M2+ 预留，不进入 M1。

### Out of scope

- 解析 `tabbit-bridge-action` fenced block。
- AI 请求后追加读取文件。
- patch proposal 的结构化解析、校验或保存。
- patch apply、repo 写入、git commit、git push。
- validation command 执行或结果回传。
- 多站点通用适配；M1 优先验证 ChatGPT 页面。
- official publishing 流程。
- `discuss/2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md` 中关于 action protocol、`bridge_action_parser.py`、`patch_validate.py`、`patch_apply.py`、command execution 和 mode upgrade 的章节在 M1 中仅作参考，不得在没有新 spec 升级范围前进入实现。

## Current Context

- 当前已知事实：
  - 当前正式运行边界是 `E2B sandbox + mounted local folder + browser page automation`。
  - 用户本地仓库只在显式挂载后可见，bridge 不依赖用户机器 shell、`Native Messaging` 或本机 `127.0.0.1` 服务。
  - 仓库内容是不可信数据，目标 AI 回复是不可信提议；M1 不把 AI 回复转成任何本地操作。
  - 综合架构稿已经收敛为参考材料，但其中涉及 M2+ protocol、patch、publishing 的内容不应进入 M1 最小实现。
- 相关正式入口：
  - `readme.md`
  - `AGENTS.md`
  - `docs/architecture/bridge_runtime_architecture.md`
  - `docs/PROJECT_MEMORY.md`
  - `docs/workflows/agent_conventions.md`
  - `docs/workflows/discuss_spec_workflow.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_tabbit-gpt-bridge-comprehensive-architecture.md`
  - `discuss/archive/tabbit-gpt-bridge-final-architecture-v4.md`
  - `discuss/archive/tabbit-skill-script-relationship-and-publishing-feasibility.md`

## Requirements

- `R1`: M1 must be read-only. It may read allowed files from the mounted repo and write artifacts outside the repo, but must not write to the mounted repo.
- `R2`: M1 must generate a bounded context pack with an explicit untrusted-data safety notice, manifest, selected file contents or summaries, redaction report, and requested review output format.
- `R3`: M1 must gracefully degrade when `git` is unavailable, when the repo is not a git repository, or when git commands time out.
- `R4`: M1 must enforce deny-before-allow path policy for context inclusion, including default denial of secrets, credentials, `.git/**`, dependency/vendor directories, and repo-external realpaths.
- `R5`: M1 must redact likely secrets before content is sent to the AI page and must record redaction counts without exposing secret values.
- `R6`: M1 must use browser GUI tools as the primary interaction path and page script only as a temporary helper for response completion/readback when needed.
- `R7`: M1 must save `context_pack.md`, `review_report.md`, and `audit.jsonl` to the configured artifact path or a clearly reported fallback path.
- `R8`: M1 must not parse or execute any action-like text from repository files or AI replies.
- `R9`: Before sending any repo-derived context to the external AI page, M1 must show the user the selected file list, total bytes, redaction counts, and default exclusions, and must obtain explicit confirmation. If confirmation is skipped or denied, M1 may generate local artifacts only and must not submit to the browser page.
- `R10`: M1 must enforce explicit context caps in the implementation contract: `max_total_context_bytes=2_000_000`, `max_file_bytes=200_000`, a bounded file-count cap, `oversized_file_behavior=skip_with_summary`, and `binary_behavior=skip`.

## M1 Runtime Contract

### Inputs

- `repo_root`: mounted repo root under the current sandbox-visible path.
- `target_ai_page`: target browser page descriptor for the review destination.
- `artifact_root`: preferred artifact output root.
- `session_policy_profile`: M1 固定为 `review_only`。
- `context_caps`: at least `max_total_context_bytes`, `max_file_bytes`, `max_file_count`, `oversized_file_behavior`, and `binary_behavior`.
- `path_policy`: allow/deny rules plus realpath enforcement.
- `timeout_policy`: browser submit timeout and assistant reply timeout.

### Outputs

- `context_pack.md`: ready-to-send review context with untrusted-data framing.
- `review_report.md`: final assistant reply only when browser submission and capture succeed.
- `audit.jsonl`: append-only audit event stream for the whole M1 session.
- `session_summary.json`: final machine-readable session summary with status, selected files, redaction counters, artifact paths, and failure metadata.

### Artifact paths

- Preferred root: `artifact_root/session_id/`.
- Minimum expected files:
  - `<artifact_root>/<session_id>/context_pack.md`
  - `<artifact_root>/<session_id>/audit.jsonl`
  - `<artifact_root>/<session_id>/session_summary.json`
  - `<artifact_root>/<session_id>/review_report.md` only on successful browser completion
- If `artifact_root` is unavailable, M1 must use a clearly reported fallback path and record both preferred and actual output roots in audit and summary artifacts.

### Audit event minimum schema

```json
{
  "ts": "2026-06-15T08:00:00Z",
  "session_id": "m1-<id>",
  "event": "context_pack_built",
  "status": "ok",
  "repo_root_alias": "<mounted-repo>",
  "artifact_root": "<actual-artifact-root>",
  "bytes_total": 12345,
  "selected_file_count": 8,
  "redaction_count": 2,
  "git_available": false,
  "failure_class": null,
  "detail": {
    "max_total_context_bytes": 2000000,
    "max_file_bytes": 200000
  }
}
```

约束：

- 必须记录状态迁移、browser submit/capture 结果、artifact fallback、失败类和关键计数。
- 不记录 secret 原文、不记录未授权 repo 外路径、不把 AI 自然语言回复转成可执行字段。

### Invariants

- `no_write_repo`: M1 不得写入 `repo_root` 或其 realpath 指向的用户仓库内容。
- `no_action_execution`: M1 不得把 repo 内容或 AI 回复中的自然语言、JSON、patch、shell 文本当作待执行动作。
- `redaction_before_send`: 发送到外部 AI 页面前必须先完成 redaction。
- `no_false_success`: browser submit 失败、reply timeout 或 readback 失败时，不得生成成功态 `review_report.md`。
- `path_containment`: 所有纳入 context 的文件必须在 `repo_root` realpath 范围内。

### Failure classes

- `repo_not_mounted`
- `repo_root_missing`
- `git_unavailable`
- `no_allowed_files`
- `context_too_large`
- `browser_submit_failed`
- `browser_reply_timeout`
- `browser_readback_failed`
- `artifact_write_failed`
- `artifact_fallback_used`

失败处理约束：

- 任何失败都必须写入 `audit.jsonl` 和 `session_summary.json`。
- `artifact_fallback_used` 可与成功态并存，但必须显式标记为降级结果。
- `review_report.md` 只允许在 browser submit、completion 和 readback 全部成功后生成。

## Browser Adapter Minimal Contract

M1 browser adapter 仅冻结以下动作，不扩展到站点专用 hook 或网络代理能力：

- `open_or_confirm_target_page()`
- `submit_text_to_chat(text)`
- `wait_until_assistant_complete(timeout)`
- `read_last_assistant_message()`
- `cleanup_page_harness()`

### Action constraints

- `open_or_confirm_target_page()`
  - 首选：GUI 导航或确认当前页已在目标站点与目标会话。
  - fallback：snapshot 校验页标题、输入框、会话主区域。
  - 失败类：`browser_submit_failed`
- `submit_text_to_chat(text)`
  - 首选：GUI-first，使用输入框聚焦、粘贴/输入、发送按钮或等价键盘提交。
  - fallback：snapshot 再定位；仅在 GUI 路径不稳定时允许临时 `evaluate_script` 辅助输入或 completion 探测。
  - 失败类：`browser_submit_failed`
- `wait_until_assistant_complete(timeout)`
  - 首选：GUI/snapshot 观察发送中与完成态变化。
  - fallback：临时 `evaluate_script` 只用于 completion 探测，不得提升页面权限。
  - 最大重试：2 到 3 次后必须报错，不得无限轮询。
  - 失败类：`browser_reply_timeout`
- `read_last_assistant_message()`
  - 首选：snapshot 或 DOM readback。
  - fallback：临时 `evaluate_script` 读取最后一条 assistant 内容。
  - 失败类：`browser_readback_failed`
- `cleanup_page_harness()`
  - 首选：移除临时 harness、清理临时选择器或注入状态。
  - fallback：若站点限制清理动作，至少记录 cleanup degraded。
  - 失败类：记录审计告警，但不覆盖已成功获取的 review

### Adapter rules

- M1 必须坚持 GUI-first、snapshot fallback、temporary `evaluate_script` only。
- `NetworkProxy` 在 M1 中明确禁用，不得作为主路径或 fallback。
- adapter 返回的是结构化成功/失败结果，不返回可直接执行的自然语言指令。

## Design

- `D1`: Split responsibilities by layer:
  - Skill / Agent: session setup, policy decisions, user-visible status, browser orchestration, artifact handoff.
  - Sandbox scripts: file discovery, policy checks, redaction, context pack generation, audit logging.
  - Browser page harness: submit context, wait for completion, read final assistant content, cleanup.
- `D2`: Start with a single `review_only` session policy:
  - `write_enabled: false`
  - `commands_enabled: false`
  - `mode: review_only`
  - bounded `allowed_paths` and default `denied_paths`
- `D3`: Generate a random `session_id` for traceability, but do not introduce nonce/action parsing in M1.
- `D4`: Prefer deterministic file selection:
  - include high-signal root files such as `readme.md`, `README.md`, `AGENTS.md`, `package.json`, `pyproject.toml`, `docs/**`, `.agent/**`
  - skip denied paths, binary files, oversized files, generated artifacts, and dependency folders
  - enforce `max_total_context_bytes=2_000_000`
  - enforce `max_file_bytes=200_000`
  - enforce bounded `max_file_count` in implementation config and record it in audit metadata
  - use `skip_with_summary` for oversized files and `skip` for binary files
- `D5`: `git_probe.py` may run only read-only git commands after probing availability; failure becomes metadata, not a hard error.
- `D6`: Browser completion should use the least invasive path first:
  - GUI `type_text` / `click`
  - accessibility snapshot or DOM readback
  - temporary `evaluate_script` harness only if needed
  - no NetworkProxy in M1
- `D7`: Audit events should record operation type, path aliases, byte counts, redaction counts, git availability, artifact paths, and errors; do not log secret values.
- `D8`: The send-to-AI confirmation gate is mandatory between context-pack generation and browser submission; without confirmation, M1 ends as a local-artifact-only run.

### Behavior Specs

```text
Given: repo_root is not mounted or does not exist
When: M1 review starts
Then: bridge stops before reading files, reports that the repo must be mounted, and does not create a misleading empty review.
```

```text
Given: repo_root is mounted and git is unavailable in the sandbox
When: M1 builds the context pack
Then: context pack is still generated, git metadata says git_available=false, and the browser review may proceed.
```

```text
Given: a candidate file matches deny_globs such as .env, .git/**, **/*.pem, or secrets/**
When: M1 selects files for context
Then: the file is excluded even if it also matches an allow pattern.
```

```text
Given: a repository file contains natural-language instructions or a fenced tabbit-bridge-action block
When: M1 packages and sends the file content
Then: the content is wrapped as untrusted data and no local action is parsed from it.
```

```text
Given: M1 has built a candidate context pack
When: the user has not explicitly confirmed the send-to-AI file list, byte size, redaction counts, and exclusions
Then: M1 may save local artifacts but must not submit any repo-derived text to the browser page.
```

```text
Given: ChatGPT returns a review containing patch text or action-like JSON
When: M1 captures the final assistant reply
Then: the reply is saved as a review report only, with no patch validation, file write, command execution, or extra read.
```

```text
Given: the browser interaction fails before a final assistant reply is captured
When: M1 exits
Then: context pack and audit log are preserved, the failure is recorded, and no partial review is reported as successful.
```

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - future skill bundle under a dedicated bridge skill directory, likely including `SKILL.md`, `scripts/`, optional `browser-scripts/`, `templates/`, and `config/`.
  - future tests for policy, redaction, context packaging, git probe, and audit logging.
  - future report or implementation note in `docs/reports/` after M1 is actually implemented and validated.
- 明确不会碰哪些部分：
  - no change to formal runtime boundary unless M1 evidence disproves it.
  - no `Native Messaging`, local `127.0.0.1` server, or user machine `PowerShell/cmd` dependency.
  - no M2+ action protocol implementation.
  - no repository write/apply/command execution behavior.

## Execution Plan

- [ ] `T1`: Confirm actual Tabbit tool names, artifact path behavior, and whether `evaluate_script` is available on ChatGPT content pages.
- [ ] `T2`: Create the minimal bridge skill scaffold for M1.
- [ ] `T3`: Implement sandbox scripts: `discover_repo.py`, `git_probe.py`, `policy.py`, `redact.py`, `context_packager.py`, `audit_log.py`.
- [ ] `T4`: Implement or document the minimal browser interaction path for ChatGPT review submission and reply capture.
- [ ] `T5`: Add focused tests for policy, redaction, context packaging, git graceful degradation, and audit events.
- [ ] `T6`: Run an end-to-end M1 dry run against a small mounted repo and save artifacts.
- [ ] `T7`: Record implementation report, validation evidence, known limits, and any durable sync needed.

## Validation

- `V1`: `python -m py_compile <edited_python_files>` for every Python script created or changed.
- `V2`: Unit tests for `policy.py`, `redact.py`, `context_packager.py`, `git_probe.py`, and `audit_log.py`.
- `V3`: CLI help checks for every new CLI script, for example `python scripts/context_packager.py --help`.
- `V4`: M1 no-git scenario: context pack succeeds and includes `git_available=false`.
- `V5`: Secret and denied-path scenario: context pack excludes denied files and redacts likely secrets.
- `V6`: Browser scenario: context is submitted to the target AI page, final assistant reply is captured, and `review_report.md` is saved.
- `V7`: Diff/stat review: `git diff --stat` confirms only intended files changed.
- `V8`: No-write invariant: compare repo state before/after the M1 dry run via file-tree snapshot, git status, or equivalent evidence to prove nothing under `repo_root` was written.
- `V9`: Send-confirmation gate: without explicit confirmation, M1 only generates local `context_pack.md` and audit artifacts, and it does not submit to the browser page.
- `V10`: Symlink escape fixture: a symlink inside the repo pointing outside `repo_root` is rejected after realpath resolution and never enters the context pack.
- `V11`: Prompt injection fixture: repo content containing `ignore previous instructions`-style text is carried as untrusted data and does not trigger extra reads or action execution.
- `V12`: Browser timeout failure path: submit failure, completion timeout, or readback failure preserves `context_pack.md` and `audit.jsonl`, records the failure class, and does not emit a success `review_report.md`.
- `V13`: Artifact fallback path: when the preferred artifact root is unavailable, M1 writes to a documented fallback path and records both roots plus the degraded status in audit and summary artifacts.

## Implementation Report

### Completed

- Created this M1 implement spec.
- Scoped M1 to read-only repo review and artifact generation.
- Separated M1 requirements from M2+ protocol, patch, write, and command capabilities.
- Added an explicit M1 runtime contract covering inputs, outputs, artifact paths, audit minimum schema, invariants, and failure classes.
- Added the send-to-AI confirmation gate, explicit context caps, and the browser adapter minimal contract for implementation handoff.

### Not completed

- M1 skill/runtime implementation has not started in this spec creation step.
- Real Tabbit tool names, artifact path behavior, and ChatGPT page harness behavior still need live validation.

### Notes

- This spec intentionally treats the comprehensive architecture document as input material, not as the final implementation contract.
- If live validation shows current Tabbit capabilities differ from the assumptions here, update this spec before widening implementation scope.
- Browser adapter details above freeze the M1 minimum contract only; any M2+ capability expansion still needs a new scope upgrade.

## Durable Sync

- 是否需要更新 `AGENTS.md`：否。本次没有改变 repo-wide agent rules。
- 是否需要更新 `docs/PROJECT_MEMORY.md`：否。本次没有新增 durable architecture decision。
- 是否需要更新 `docs/CHANGELOG.md`：否。仅新增 implement spec，尚未实现 M1 runtime。
