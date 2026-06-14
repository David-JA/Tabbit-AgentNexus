# Bridge Runtime Architecture

> Status: accepted baseline for current development repo
> Last updated: 2026-06-15
> Derived from: `discuss/archive/tabbit-gpt-bridge-final-architecture-v4.md`

## 1. 目标

这个仓库当前接受的目标是开发一个 Tabbit bridge skill，并把它收敛为 AI 浏览器新架构下的一个 bridge 中枢：在用户显式授权挂载本地仓库后，以较低操作成本把受控上下文发送到网页端高性能 AI 完成评审与后续协作。当前网页端 AI 的主要适配目标是 GPT，而 Tabbit agent 负责承担中介与副手角色，把本地上下文处理、页面交互和后续受控流程串起来。

## 1.1 双端适配目标

当前产品定位要求同时考虑两端：

- 网页端 GPT：
  - 是当前主要的网页端推理、评审和反馈目标
  - 需要高质量、低噪声、边界清晰的上下文与交互输入
- Tabbit agent：
  - 是 bridge 的中介与副手，而不是可忽略的旁路组件
  - 需要可控、低摩擦、易验证的上下文打包、页面编排和结果回传路径

因此，bridge 设计不应只优化单端体验；凡是进入默认实现的方案，都应同时评估网页端 GPT 的效果和 Tabbit agent 的可用性成本。

## 2. 默认运行边界

当前默认边界如下：

- bridge 运行在 `E2B Linux sandbox`
- 用户本地仓库只在显式挂载后可见
- 文件操作基于挂载目录进行
- 页面交互通过浏览器 GUI 工具和按需注入脚本完成
- 持久化产物走 artifact 路径，而不是依赖用户本机服务

明确不作为默认前提的能力：

- 用户机器 `PowerShell/cmd`
- `Native Messaging`
- 本机 `127.0.0.1` 服务
- 未挂载目录访问

## 3. 分层职责

### Skill / Agent Layer

负责：

- session 建立
- 策略判断
- 上下文选择与打包
- 用户确认
- 审计与结果落盘

不负责：

- 把页面脚本当作长期常驻代理
- 把 prompt 当安全边界

### Sandbox Script Layer

负责：

- repo 发现
- git 探测
- policy 校验
- secret redaction
- context pack 生成
- patch 校验与后续受控处理

### Browser Page Layer

负责：

- 输入 prompt/context
- 监听回复完成
- 读取最终 assistant 内容
- 任务结束后清理临时 harness

不负责：

- 本地文件权限
- 受控写入决策
- 长期状态保存

## 4. 当前推荐里程碑

1. `M1 Repo Review Bridge`
   - 生成 context pack
   - 发送到目标 AI 页面
   - 捕获 review
   - 保存报告
   - 不修改仓库
2. `M2 Read-more Bridge`
   - 解析结构化 `read_files` 请求
   - 策略校验后追加读取
3. `M3 Patch Proposal`
   - 校验并保存 patch
   - 仍不写入仓库
4. `M4 Apply with Approval`
   - 需要用户明确确认
   - 记录 before/after
5. `M5 Validation Commands`
   - 仅允许白名单验证命令

## 5. 安全基线

### Trust model

- 仓库内容是不可信数据
- AI 回复是不可信提议
- 只有本地策略层可以决定是否读取、写入或执行

### Policy model

当前采用三层思路：

1. 静态默认规则
2. session 级实际策略
3. 单次操作确认

### 默认禁区

在进入更具体实现前，默认应拒绝或强限制：

- `.env`、密钥、证书、凭据类文件
- `.git` 内部实现细节
- 未授权的 repo 外路径
- 自动执行危险命令
- 未确认的 patch 应用

## 6. 当前实现哲学

- 任务式 bridge 优于常驻式脚本
- DOM completion 主路径优于 hacky network hook
- 先只读评审，后追加能力
- 优先沉淀 repo-local workflow，而不是先追求全站点适配

## 7. 默认协作角色

当前仓库默认按以下 4 个角色推进 bridge 开发：

1. 用户
   - 负责需求、优先级、风险确认和最终验收
2. 网页 GPT
   - 负责架构建议、spec 收敛和实现过程中的 reviewer 反馈
3. Tabbit agent
   - 负责目标使用方视角的测试、回归观察和行为反馈
4. 仓库代码 agent
   - 负责仓库内的大部分实际开发、测试、文档同步和提交

约束：

- 网页 GPT 和 Tabbit agent 默认提供建议或反馈，不直接替代仓库真值入口。
- 仓库代码 agent 负责把外部反馈整理成仓库内可验证变更。
- 用户始终保留需求和验收的最终决定权。

## 8. 相关材料

- Tabbit 浏览器 agent 行为边界：`tabbit_browser_agent_behavior_boundary.md`
- 多角色协作 workflow：`../workflows/multi_role_collaboration.md`
- 讨论稿：`discuss/archive/tabbit-gpt-bridge-architecture-discussion.md`
- 最终讨论版：`discuss/archive/tabbit-gpt-bridge-final-architecture-v4.md`
- skill 与发布可行性：`discuss/archive/tabbit-skill-script-relationship-and-publishing-feasibility.md`
