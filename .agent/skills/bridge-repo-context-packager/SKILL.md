---
name: bridge-repo-context-packager
description: 为当前 Tabbit bridge 开发仓库生成面向外部 AI / 网页 AI 的 context pack zip。适用于 handoff、外部评审、Web AI 上下文包、repo overview bundle 等场景。
compatibility: 需要能读取当前仓库中的正式入口、`.agent/skills/` 与 `scripts/tools/package_bridge_repo_context.py`，并具备 Python 执行权限。
---

# Bridge Repo Context Packager

## 目标

把当前 bridge 开发仓库打成一个**适合外部 AI 快速理解的 zip context pack**。

这个包不是全量备份，而是：

- 保留仓库正式入口与实现上下文
- 优先包含架构、workflow、当前实现 spec、repo-local skills、关键运行脚本、配置和测试夹具
- 默认排除 `.git/`、`reference/`、`exports/` 和缓存噪声

## 何时使用

当用户提到以下意图时，优先使用本 skill：

- “把这个 bridge repo 打包给网页版 AI / Web AI / 外部 AI”
- “做一个 handoff 包 / context pack / repo overview zip”
- “把正式文档、当前 spec 和技能一起导出，方便别人快速理解”

## 使用前必读

在执行前，先读取：

1. `readme.md`
2. `docs/architecture/bridge_runtime_architecture.md`
3. `docs/architecture/tabbit_browser_agent_behavior_boundary.md`
4. `docs/workflows/README_workflows.md`
5. `./references/include-profiles.md`

## 默认行为

默认运行：

```powershell
python scripts/tools/package_bridge_repo_context.py --profile overview
```

脚本会输出：

- 一个 zip 文件
- `_context_pack/README.md`
- `_context_pack/manifest.json`
- `_context_pack/GIT_RECENT_COMMITS.md`

## 轻重级别

先看 [include-profiles.md](./references/include-profiles.md)。

### 更轻量

```powershell
python scripts/tools/package_bridge_repo_context.py --profile minimal
```

### 默认

```powershell
python scripts/tools/package_bridge_repo_context.py --profile overview
```

### 控制 git 摘要条数

```powershell
python scripts/tools/package_bridge_repo_context.py --profile overview --git-commits 9
```

### 跳过 git 摘要

```powershell
python scripts/tools/package_bridge_repo_context.py --profile overview --git-commits 0
```

## 默认打包重点

相较于参考仓库中的通用科研包，本 skill 更偏向当前 bridge 仓库的“正式入口 + 当前收敛 spec + repo-local workflow + 可评审实现核心”：

- `readme.md`
- `AGENTS.md`
- `config/`
- `docs/architecture/`
- `docs/workflows/`
- `docs/reports/`
- 当前 `discuss/` 材料
- `.agent/skills/`
- `scripts/`
- `tests/`

## 输出要求

完成后必须返回：

1. zip 的绝对路径
2. 使用的 profile
3. 文件数
4. `_context_pack/README.md` 路径
5. `_context_pack/manifest.json` 路径
6. `_context_pack/GIT_RECENT_COMMITS.md` 状态
7. 明确说明默认排除了什么

推荐输出格式：

```text
已生成 bridge repo context pack:
- 路径: <绝对路径>
- 配置: overview
- 文件数: N
- README: _context_pack/README.md
- Manifest: _context_pack/manifest.json
- Git 摘要: ready / skipped / unavailable
- 默认排除: .git / reference / exports / __pycache__ / *.zip / *.pyc
```

## 边界

- 这是给外部 AI 快速理解当前 bridge repo 的包，不是全量归档
- 默认不打包 `.git/`
- 默认不打包 `reference/`
- 默认不打包 `exports/`
- 若用户需要历史归档材料，应明确说明当前 `overview` 也不会自动包含 `discuss/archive/`
