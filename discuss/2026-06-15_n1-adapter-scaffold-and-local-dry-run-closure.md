# N1 adapter scaffold and local dry run closure

> Status: implemented
> Created: 2026-06-15
> Spec type: implementation
> Profile: nexus-default

## Summary

把 `N1 Local Workspace Review Adapter` 从“已有零件”推进到“可本地一键 dry run 生成可发送 artifacts”，同时补齐 repo-local skill scaffold、runner、测试与最小文档收口。

## Scope

### In scope

- 新增一个统一的 N1 local-only session runner。
- 新增面向 `repo-review` scenario 的 repo-local skill scaffold。
- 把 sandbox-side 用户可见命名从 `M1 bridge` 收口到 `N1 / AgentNexus review-only`。
- 补齐 local dry run 的测试、`pytest` 导入稳定性和最小文档同步。

### Out of scope

- 不实现 browser submit/readback。
- 不实现 patch、命令执行、N2+ action protocol。
- 不改 runtime boundary、trust model 或默认权限模型。
- 不处理 Tabbit live capability probe 本身。

## Current Context

- 当前已知事实：
  - `discover_repo.py`、`git_probe.py`、`policy.py`、`redact.py`、`context_packager.py`、`audit_log.py` 已可独立测试。
  - 缺的不是底层零件，而是可复现的 session 编排入口和 N1 执行 skill。
  - `pytest -q` 的导入稳定性在解压环境里还不够稳，需要补一个仓库内修复。
- 相关正式入口：
  - `readme.md`
  - `docs/architecture/nexus_runtime_architecture.md`
  - `docs/workflows/agent_conventions.md`
  - `docs/PROJECT_MEMORY.md`
- 相关讨论或参考：
  - `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
  - `discuss/README_discuss.md`

## Requirements

- `R1`: local dry run 必须能通过单一 CLI 入口创建 `session_id`、`context_pack.md`、`audit.jsonl` 和 `session_summary.json`。
- `R2`: 默认状态必须是 `ready_to_send`，且明确尚未提交到浏览器页面。
- `R3`: 若 `artifact_root` 不可写或位于 `repo_root` 内，runner 必须自动切到 repo 外 fallback 并记录降级。
- `R4`: dry run 必须保持 `no_write_repo`，实现上不允许把产物落回 repo。
- `R5`: skill scaffold 只编排已有脚本，不重复实现 sandbox 逻辑。
- `R6`: 当前实现必须把用户可见的 `M1 bridge` 命名收口为 `N1 Local Workspace Review`。

## Design

- `D1`: 新增 `scripts/n1_review_session.py` 作为统一入口，内部串联 discovery、policy session、git probe、context build、audit 和 summary。
- `D2`: 把 artifact root 解析做成显式步骤，优先用用户指定目录，失败时退到系统临时目录下的 `agentnexus-artifacts/<session_id>/`。
- `D3`: `session_summary.json` 输出机器可读的发送确认摘要、artifact 路径、失败类和 invariants，供后续 browser adapter 复用。
- `D4`: 新增 `.agent/skills/nexus-local-workspace-review/`，明确先跑 local-only dry run，再等待 Tabbit live capability probe 结果决定 browser path。
- `D5`: 用 runner 级测试覆盖成功、`no_git`、`denied_only`、secret redaction、artifact fallback 和 `no_write_repo`。

## Expected Diff Shape

- 预计会改哪些目录或文件：
  - `scripts/`
  - `tests/`
  - `.agent/skills/`
  - `discuss/`
  - `docs/CHANGELOG.md`
- 明确不会碰哪些部分：
  - `docs/architecture/` 真值边界
  - N2-N7 协议和执行能力
  - browser-side live probe 报告

## Execution Plan

- [x] `T1`: 新建本次实现 spec，冻结 local-only closure 范围。
- [x] `T2`: 新增 N1 repo-local adapter skill scaffold。
- [x] `T3`: 新增统一 session runner，串联已有 sandbox-side 零件。
- [x] `T4`: 收口用户可见命名与 CLI 描述到 N1 / AgentNexus。
- [x] `T5`: 补 runner 级测试与 `pytest` 导入稳定性。
- [x] `T6`: 完成 local-only dry run 的自动验证与文档回填。

## Validation

- `V1`: `python -m py_compile scripts/n1_review_session.py scripts/*.py`
- `V2`: `python -m pytest -q`
- `V3`: `pytest -q`
- `V4`: `python scripts/n1_review_session.py --help`
- `V5`: `git diff --stat`

## Implementation Report

### Completed

- 新增 N1 local-only session runner，并把默认 session id 前缀收口为 `n1-`。
- 新增 `nexus-local-workspace-review` skill、review request 模板和 browser contract 参考。
- 新增 runner 级测试，覆盖 fallback、no-git、denied-only、redaction 与 `no_write_repo`。
- 补上 `tests/conftest.py`，让裸跑 `pytest -q` 也能稳定导入 `scripts`。
- 更新 discuss 索引与 changelog，使当前 active backlog 更聚焦在 N1 闭环。

### Not completed

- 未做 Tabbit live capability probe。
- 未实现 browser submit/readback。
- 未生成真实 `review_report.md`。

### Notes

- 本次故意把“发送前确认”停在 artifact 和 summary 层，不提前引入 browser harness 复杂度。
- 若后续 live probe 证明 GUI-first 路径不稳定，应基于本 runner 的 summary/audit 接口补最小 browser adapter，而不是回头重写 sandbox 逻辑。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否
- 是否需要更新 `docs/PROJECT_MEMORY.md`：否
- 是否需要更新 `docs/CHANGELOG.md`：是
