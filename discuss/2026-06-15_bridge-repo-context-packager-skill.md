# 新增 bridge repo context packager skill

> Status: completed
> Created: 2026-06-15
> Spec type: workflow
> Profile: bridge-default

## Summary

为当前 Tabbit bridge 开发仓库新增一个 repo-local context packager skill，用于把正式入口、关键 spec、repo-local skills 和必要脚本打包成适合外部 AI / 网页 AI 阅读的 zip。

## Scope

### In scope

- 新增一个针对当前 bridge 仓库的 repo-local skill
- 新增一个轻量打包脚本，输出带 manifest 的 zip context pack
- 为 skill 增加 profile 参考说明
- 同步 workflow 入口与 changelog
- 回填 discuss spec 和 discuss index

### Out of scope

- 不实现 M1 bridge runtime 代码
- 不引入 Native Messaging、本机服务或用户机器 shell 依赖
- 不做全量仓库备份器
- 不默认打包 `.git/`、`reference/` 或其他非关键大目录

## Current Context

- 当前已知事实：当前仓库只有 `scripts/tools/new_discuss_spec.py` 一个维护脚手架；尚无用于 handoff / repo context zip 的 repo-local skill 或脚本。
- 相关正式入口：`readme.md`、`docs/architecture/bridge_runtime_architecture.md`、`docs/architecture/tabbit_browser_agent_behavior_boundary.md`、`docs/workflows/README_workflows.md`
- 相关讨论或参考：`discuss/2026-06-14_m1-repo-review-bridge-implement-spec.md`、参考 skill `E:/project/pwa1483_1d_scan_stress/.agent/skills/repo-context-packager/`

## Requirements

- `R1`: 新 skill 必须明确面向“外部 AI 快速理解当前 bridge 仓库”，而不是全量归档。
- `R2`: 默认打包内容应优先覆盖正式入口、当前实现 spec、repo-local skills 和维护脚本。
- `R3`: 默认排除 `.git/`、`reference/`、`__pycache__/`、二进制大件和无关噪声。
- `R4`: 输出 zip 时应附带 `_context_pack/README.md` 与 `manifest.json` 之类的阅读入口。
- `R5`: 至少提供 `minimal` 和 `overview` 两种 profile。
- `R6`: 打包脚本在 git 不可用时不应失败。

## Design

- `D1`: 新增 `.agent/skills/bridge-repo-context-packager/`，结构跟现有 repo-local skills 保持一致：`SKILL.md` + `agents/openai.yaml` + `references/include-profiles.md`。
- `D2`: 新增 `scripts/tools/package_bridge_repo_context.py`，负责按 profile 收集文件、生成 manifest 和 zip。
- `D3`: `minimal` profile 聚焦正式入口；`overview` profile 在此基础上补充 `discuss/`、`docs/reports/`、`scripts/tools/` 等实现上下文。
- `D4`: 输出目录放在 `exports/repo-context/`，并更新 `.gitignore` 避免产物入库。

## Expected Diff Shape

- 预计会改哪些目录或文件：`.agent/skills/`、`scripts/tools/`、`docs/workflows/README_workflows.md`、`docs/CHANGELOG.md`、`.gitignore`、`discuss/README_discuss.md`
- 明确不会碰哪些部分：`docs/architecture/` 真值内容、M1 runtime 设计、`reference/` 原始参考材料

## Execution Plan

- [x] `T1` 设计 bridge 仓库专用 context pack 内容范围与 profiles
- [x] `T2` 实现打包脚本与 skill bundle
- [x] `T3` 同步 workflow / changelog / discuss index
- [x] `T4` 运行最小验证并回填结果

## Validation

- `V1`: `python -m py_compile scripts/tools/package_bridge_repo_context.py`
- `V2`: `python scripts/tools/package_bridge_repo_context.py --help`
- `V3`: `python scripts/tools/package_bridge_repo_context.py --profile minimal`
- `V4`: `git diff --stat`
- `V5`: `git status --short --branch`

## Implementation Report

### Completed

- 新增 `scripts/tools/package_bridge_repo_context.py`，支持 `minimal` / `overview` 两种打包 profile，并生成 zip、manifest、README 与 Git 摘要。
- 新增 `.agent/skills/bridge-repo-context-packager/`，包含 `SKILL.md`、`agents/openai.yaml` 和 `references/include-profiles.md`。
- 同步 `docs/workflows/README_workflows.md`、`docs/CHANGELOG.md`、`.gitignore` 与 `discuss/README_discuss.md`，把新 skill 接入当前仓库入口。
- 默认排除了 `.git/`、`reference/`、`exports/`、`discuss/archive/` 和缓存噪声，保持 handoff 包聚焦当前 bridge 仓库正式上下文。

### Not completed

- 无

### Notes

- 本任务同时涉及新增 `.agent/skills/` 与脚手架脚本，因此按 workflow 要求先创建 discuss spec。
- 当前脚本面向“外部 AI 理解包”，不是全量备份器；若未来需要包含 `reference/` 或历史 archive，应新增显式开关而不是改默认值。

## Durable Sync

- 是否需要更新 `AGENTS.md`：否
- 是否需要更新 `docs/PROJECT_MEMORY.md`：否
- 是否需要更新 `docs/CHANGELOG.md`：是
