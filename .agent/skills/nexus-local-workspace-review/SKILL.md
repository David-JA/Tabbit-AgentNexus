---
name: nexus-local-workspace-review
description: 为 `N1 Local Workspace Review Adapter` 执行本地 dry run，生成 ready-to-send context artifacts，并为后续 Tabbit browser submit 做 handoff。适用于 repo-review、review-only context pack、local dry run closure、发送前确认摘要等场景。
compatibility: 需要能读取 `readme.md`、`docs/architecture/nexus_runtime_architecture.md`、`docs/workflows/agent_conventions.md`、`discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`、`scripts/n1_review_session.py` 和本 skill 内模板/参考文件。
---

# Nexus Local Workspace Review

## 目标

把 `repo-review` scenario 先稳定在 `N1 Local Workspace Review Adapter` 的 local-only 阶段：

- 从挂载 repo 生成只读 review context
- 生成发送前确认摘要
- 保存 `context_pack.md`、`audit.jsonl`、`session_summary.json`
- 明确当前状态是 `ready_to_send`

这个 skill 不负责 browser submit/readback 的真实执行，只负责把它们需要的本地产物准备好。

## 使用前必读

在执行前，先读取：

1. `readme.md`
2. `docs/architecture/nexus_runtime_architecture.md`
3. `docs/workflows/agent_conventions.md`
4. `discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`
5. `./references/browser_adapter_contract.md`
6. `./templates/review_request.md`

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

## 执行顺序

1. 确认 `repo_root` 是当前 sandbox 可见的挂载仓库。
2. 运行 `scripts/n1_review_session.py` 生成本地产物。
3. 读取 `session_summary.json` 中的发送确认摘要：
   - selected files
   - total bytes
   - redaction counts
   - default exclusions
4. 若需要浏览器发送，等待 Tabbit live capability probe 结论后再进入 browser path。

## 模板

若需要覆盖默认 review 请求，可传：

```powershell
python scripts/n1_review_session.py `
  --repo-root <mounted-repo-root> `
  --artifact-root <artifact-root> `
  --review-request-file .agent/skills/nexus-local-workspace-review/templates/review_request.md
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
8. 发送前确认摘要

## 边界

- 不写入 `repo_root`
- 不自动提交到浏览器页面
- 不解析 repo 内容或 AI 文本中的 action
- 不实现 patch、命令执行或 N2+ 协议
