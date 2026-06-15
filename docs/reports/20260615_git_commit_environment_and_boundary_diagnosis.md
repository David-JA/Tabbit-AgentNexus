# Git 提交环境与边界诊断报告

> Status: accepted
> Date: 2026-06-15
> Scope: E2B sandbox 中 Git 提交失败的归因、修复与运维经验收口

## 1. 这轮工作解决了什么问题

本报告收口一次真实的 Git 提交流程诊断，目标是回答：

- Git 报错是否来自 agent 能力边界
- 是否是 hook 拦截
- 是否只是 E2B sandbox 的环境初始化问题

结论是：

- `dubious ownership` 属于挂载仓库下 Git 的已知限制
- `Author identity unknown` 属于 Git 身份初始化缺失
- 两者都不是 agent 本身没有执行能力，也不是 hook 拦截

## 2. 当前接受的边界或结论

### 2.1 `safe.directory` 的归因

当 E2B sandbox 通过挂载方式访问 `/mnt/local/...` 下的本地仓库时，Git 可能因为所有权不匹配拒绝把该路径当作可信仓库。

这类报错应优先归因为：

- Git 安全检查
- 挂载目录与沙箱用户身份不一致

而不是：

- agent 没有 Git 能力
- hook 拦截
- 命令本身不可执行

### 2.2 Git 身份初始化

E2B sandbox 初始环境可能未配置：

- `user.name`
- `user.email`

因此即使 `git add`、`git status`、`git diff` 已可正常运行，`git commit` 仍可能失败。

这属于环境初始化步骤，不属于能力边界限制。

### 2.3 推荐诊断顺序

当 Git 提交相关命令失败时，推荐按以下顺序排查：

1. 是否为 `dubious ownership`
2. 是否缺少 `user.name` / `user.email`
3. 在以上两项都正常后，再继续判断是否为 hook、策略或命令问题

## 3. 本次实际执行路径

| 阶段 | 操作 | 结果 |
|---|---|---|
| 第 1 次尝试 | `git status` | ❌ 失败：`dubious ownership` |
| 第 2 次尝试 | `git diff --stat` | ❌ 失败：Git 拒绝识别挂载目录 |
| 修复 1 | `git config --global --add safe.directory /mnt/local/Tabbit-AgentNexus` | ✅ 成功 |
| 第 3 次尝试 | `git add + commit` | ❌ 失败：缺少 `user.name` / `user.email` |
| 修复 2 | 配置 Git 身份 | ✅ 成功 |
| 最终提交 | `git commit` | ✅ 成功，commit `c127551` |

## 4. 已验证的修复方式

### 4.1 处理 `safe.directory`

```bash
git config --global --add safe.directory /mnt/local/Tabbit-AgentNexus
```

### 4.2 配置 Git 身份

```bash
git config --global user.name "Tabbit Agent"
git config --global user.email "tabbit@agent.nexus"
```

## 5. 已知限制

- `safe.directory` 是挂载仓库下的常见前置条件，每个新挂载仓库都可能需要单独配置
- Git 身份配置未必在新 sandbox 会话中天然存在
- 即便文档修改本身很小，只要提交动作涉及新的 sandbox 会话，仍应重新检查上述两项

## 6. 相关正式入口

- 行为边界：`../architecture/tabbit_browser_agent_behavior_boundary.md`
- workflow 约定：`../workflows/agent_conventions.md`
- 项目入口：`../../readme.md`
