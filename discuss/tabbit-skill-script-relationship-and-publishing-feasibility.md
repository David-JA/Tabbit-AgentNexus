# 妙招(Skill)与脚本的关系 & GPT Bridge 公开发布可行性分析

> **日期**: 2026-06-14  
> **基于**: Skill Creator (730008)、Browser Script Builder (730337)、网页广告一键净 (736463) 官方文档

---

## 目录

1. [核心结论](#1-核心结论)
2. [妙招(Skill)到底是什么？](#2-妙招skill到底是什么)
3. [Skill 与脚本的层级关系](#3-skill-与脚本的层级关系)
4. [Skill 如何"调用"脚本？](#4-skill-如何调用脚本)
5. [实际案例：已发布的带脚本妙招](#5-实际案例已发布的带脚本妙招)
6. [GPT Bridge 作为妙招发布的可行性评估](#6-gpt-bridge-作为妙招发布的可行性评估)
7. [推荐发布策略](#7-推荐发布策略)
8. [公开 vs 个人妙招的关键差异](#8-公开-vs-个人妙招的关键差异)

---

## 1. 核心结论

### ✅ 回答你的三个问题：

| 问题 | 答案 | 依据 |
|------|------|------|
| **现有架构足够吗？** | ✅ **基本够用，但需要适配** | Skill bundle结构天然支持我们设计的所有组件 |
| **妙招支持放入和调用脚本吗？** | ✅ **完全支持，且是官方一等公民能力** | `allowed_tools: ["evaluate_script"]` + `browser-scripts/` 目录 |
| **Skill和脚本的关系是什么？** | **Skill是容器/大脑，脚本是其可执行的手** | 见下方详细解释 |

### ⚠️ 需要注意的约束：

1. **Personal Skill ≠ Official Published Skill** — Skill Creator文档明确标注仅用于personal skill，official publishing有独立审核流程
2. **evaluate_script不能在Tabbit AI面板页面运行** — 只能在普通内容页（如ChatGPT）上注入
3. **本地文件夹访问需要用户显式授权** — 不能假设所有用户都挂载了本地仓库
4. **不支持本地stdio MCP** — 如果想对接外部服务，必须用HTTP-based remote MCP

---

## 2. 妙招(Skill)到底是什么？

### 官方定义（来自Skill Creator文档）

> **"Every generated skill must be more than a prompt. It should be a reusable runtime capability package that tells the Agent what to do, where to run each step, what files to use, what output to produce, and how to verify success."**

翻译：**妙招不是一个prompt，而是一个"可复用的运行时能力包"**。它告诉Agent：
- 做什么（workflow/SOP）
- 在哪里做每一步（browser? sandbox? MCP? web lookup?）
- 用哪些文件（scripts/templates/references）
- 输出什么（output contract）
- 怎么验证成功（verification standard）

### 妙招的Bundle结构（标准目录）

```
my-skill/
├── SKILL.md                  # 必需！行为规范/工作流/SOP（"大脑"）
├── browser-scripts/          # 可选。页面端JS脚本（通过evaluate_script注入）（"手"）
│   ├── bridge-harness.js     #   例：GPT Bridge的临时页面harness
│   └── response-capture.js   #   例：回复捕获脚本
├── scripts/                  # 可选。沙箱端处理脚本（E2B内运行）（"工具箱"）
│   ├── context-packager.py   #   例：仓库context打包器
│   └── secret-scanner.py     #   例：密钥扫描脱敏
├── references/               # 可选。领域知识/规则/示例（"知识库"）
│   ├── bridge-protocol.md    #   例：Tabbit-GPT协议规范
│   └── permission-templates.json  #   例：权限模板库
├── templates/                # 可选。输出模板（"格式标准"）
│   └── review-template.md    #   例：评审报告输出格式
└── assets/                   # 可选。静态资源
    └── cover.html            #   例：封面图
```

### 妒招的元数据（创建时声明）

```json
{
  "title": "GPT Repo Review Bridge",
  "description": "将本地仓库上下文桥接到Web端AI进行评审",
  "when_to_use": "当用户想让AI评审本地代码/文档仓库时触发",
  "source_type": "agent_create",        // 或 agent_update
  "url_patterns": ["*.chatgpt.com/*", "*.claude.ai/*"],  // 自动触发的URL模式
  "allowed_tools": ["evaluate_script"]   // 启用脚本能力！
}
```

---

## 3. Skill 与脚本的层级关系

### 一句话总结

> **Skill是"指挥官"，脚本是"士兵"。Skill的SKILL.md定义战略（何时调用哪个脚本、传什么参数、怎么处理返回值），脚本负责具体的战术执行。**

### 三种"脚本"在Skill中的角色

| 脚本类型 | 存放位置 | 运行环境 | 通过什么调用 | 典型用途 |
|----------|----------|----------|--------------|----------|
| **Browser Script** | `browser-scripts/*.js` | 用户浏览器页面（当前打开的网页） | `evaluate_script(script_path, args)` | DOM操作、UI交互、页面状态监听 |
| **Sandbox Script** | `scripts/*.py` / `scripts/*.sh` | E2B沙箱（隔离环境） | `e2b_bash("python script.py")` | 文件处理、数据转换、文本生成 |
| **External MCP Tool** | 不在bundle内，远程HTTP服务 | 外部服务器 | `mcp__<connector>__<tool>()` | GitHub API、Notion、数据库等 |

### 关键设计原则

来自Browser Script Builder文档的核心边界：

```
普通网页操作（90%场景）→ 用浏览器GUI工具：
  take_snapshot / click / type_text / scroll / navigate_page ...

需要脚本注入的场景（10%场景）→ 才用 evaluate_script：
  ✅ 批量DOM操作
  ✅ 大规模结构化数据提取
  ✅ 页面端自动化（非单次点击）
  ✅ 需要实时DOM事件监听（MutationObserver等）
  ✅ 需要访问页面内部运行时状态
  ❌ 不要用脚本替代单个正常GUI操作
```

---

## 4. Skill 如何"调用"脚本？

### 4.1 Browser Script 的调用方式

**在SKILL.md的工作流中这样写：**

```markdown
## Workflow

1. 确认当前页面为ChatGPT对话页面
2. 通过 `evaluate_script` 注入临时bridge harness：
   ```json
   {
     "script_path": "browser-scripts/bridge-harness.js",
     "args": { "session_id": "<动态生成>", "mode": "review_only" },
     "render_as_script_card": false
   }
   ```
3. 将本地context pack输入聊天框（使用 type_text）
4. 点击发送（使用 click）
5. 等待回复完成（使用 wait + take_snapshot 检测）
6. 通过 `evaluate_script` 读取最终回复：
   ```json
   {
     "script_path": "browser-scripts/response-capture.js",
     "args": { "session_id": "<同上>" },
     "render_as_script_card": false
   }
   ```
7. 清理 harness
```

**注意**：SKILL.md中写的是"指导性指令"，不是直接执行代码。未来的Tabbit Agent读取SKILL.md后，会按照这个SOP自行决定何时调用evaluate_script。

### 4.2 Sandbox Script 的调用方式

```markdown
## Workflow

1. 收集仓库文件列表
2. 使用sandbox脚本打包context pack：
   （Agent会在E2B中执行 `python scripts/context-packager.py --repo <path>`）
3. 对打包结果做secret scanning：
   （Agent会执行 `python scripts/secret-scanner.py <pack_file>`）
4. 继续后续步骤...
```

### 4.3 脚本之间的协作

```
SKILL.md (协调者)
    │
    ├─→ browser-scripts/bridge-harness.js  (页面端：监听GPT回复)
    │         │
    │         └─→ 返回 { ok: true, reply_text: "...", is_complete: bool }
    │
    ├─→ scripts/context-packager.py        (沙箱端：打包仓库文件)
    │         │
    │         └─→ 返回 context_pack markdown 文件路径
    │
    └─→ scripts/secret-scanner.py          (沙箱端：安全扫描)
              │
              └─→ 返回 sanitized 内容或 redaction 报告
```

---

## 5. 实际案例：已发布的带脚本妙招

### 案例：🧹 网页广告一键净 (Skill ID: 736463)

这是一个**已经在妙招市场公开发布的、使用evaluate_script的妙招**，完美展示了Skill+脚本的配合方式。

#### 它的Bundle结构：

```
baidu_ad_cleaner/
├── SKILL.md                        # 行为规范
├── browser-scripts/
│   └── baidu-ad-cleaner.js          # 核心清理脚本（~100行JS）
└── assets/
    └── cover.html                  # 封面图
```

#### 它的元数据声明：

```yaml
---
name: baidu_ad_cleaner
title: 🧹 百度搜索广告一键净
description: 一键清除百度搜索结果中的所有广告内容...
when_to_use: 当用户在百度搜索结果页面看到大量广告时...
---
```

#### 它的Runtime Requirements：

```markdown
- Browser login required: **no**
- Sandbox required: **no**
- Page script required: **yes** (需要 `evaluate_script` 注入)  ← 关键！
- User local folder required: **no**
```

#### 它的工作流（从SKILL.md原文）：

```markdown
1. 确认当前页面为百度搜索结果页 (`www.baidu.com/s?*`)
2. 通过 `evaluate_script` 注入 `browser-scripts/baidu-ad-cleaner.js`
3. 脚本自动执行以下清理操作：
   - 移除 `ec-tuiguang` 广告角标 SPAN 元素
   - 隐藏右侧 `EC_result` 推广卡片区域
   - ...
4. 返回清理统计报告（移除数量、类型明细）
5. 通过截图验证效果
```

#### 它的脚本契约（Script Contract）：

```javascript
// baidu-ad-cleaner.js 的标准形状
async function run(args) {
  return {
    ok: true,
    summary: "超保守清理完成：处理 N 个广告元素",
    changed_count: 11,
    data: { removed_nodes: [...] },
    warnings: []
  };
}
```

### 这个案例证明了什么？

| 证明点 | 证据 |
|--------|------|
| ✅ 已发布妙招可以使用evaluate_script | `Page script required: yes` |
| ✅ browser-scripts/ 是官方支持的目录 | `browser-scripts/baidu-ad-cleaner.js` |
| ✅ allowed_tools机制生效 | 该skill启用 `evaluate_script` |
| ✅ url_patterns自动触发可行 | `*.baidu.com/s*` |
| ✅ 脚本返回结构化JSON是标准实践 | `{ ok, summary, changed_count, data, warnings }` |
| ✅ 安全边界有先例 | "超保守策略"、"不触碰正常结果"、"display:none不删除DOM" |

---

## 6. GPT Bridge 作为妙招发布的可行性评估

### 6.1 架构映射：我们的设计 → Skill Bundle

| 我们讨论的组件 | 对应Skill Bundle位置 | 可行性 |
|---------------|----------------------|--------|
| Repo Context Packager | `scripts/context-packager.py` | ✅ E2B沙箱原生支持 |
| Secret Scanner | `scripts/secret-scanner.py` | ✅ 同上 |
| Bridge Harness (临时页面注入) | `browser-scripts/bridge-harness.js` | ✅ evaluate_script官方支持 |
| Response Capture | `browser-scripts/response-capture.js` | ✅ 同上 |
| Capability Policy Engine | `references/permission-templates.json` + SKILL.md逻辑 | ✅ SKILL.md作为策略层 |
| Bridge Protocol Spec | `references/bridge-protocol.md` | ✅ references目录 |
| Review Output Template | `templates/review-template.md` | ✅ templates目录 |
| User Approval UI逻辑 | SKILL.md工作流中的决策步骤 | ✅ Agent根据SKILL.md执行 |

### 6.2 ✅ 完全可行的部分

| 能力 | Skill机制 | 说明 |
|------|-----------|------|
| 读取本地仓库文件 | E2B `e2b_read` / `e2b_glob` | 用户挂载本地文件夹后可用 |
| 打包context pack | `scripts/` 中的Python脚本 | 沙箱内运行 |
| 注入页面脚本 | `evaluate_script` + `browser-scripts/` | 已有先例（广告一键净） |
| 操作ChatGPT等AI网站 | GUI工具 `type_text`/`click` + snapshot | 天然能力 |
| 捕获GPT回复 | `take_snapshot` + 可选 `evaluate_script` | 两种方式都支持 |
| 权限控制 | SKILL.md声明 + 运行时确认 | Agent层面实现 |
| URL自动触发 | `url_patterns: ["*.chatgpt.com/*"]` | 官方支持 |
| 版本迭代 | `source_type: "agent_update"` | 官方支持 |

### 6.3 ⚠️ 需要适配/注意的部分

| 问题 | 影响 | 解决方案 |
|------|------|----------|
| **本地文件夹不是所有用户都有** | 核心功能依赖本地文件访问 | SKILL.md中声明 `User local folder required: optional`；无本地文件夹时降级为"用户手动粘贴文件内容"模式 |
| **evaluate_script不能在AI面板运行** | Bridge harness必须在ChatGPT等目标页面注入 | 工作流第一步引导用户打开目标AI页面；或在SKILL中用 `new_page` 打开 |
| **Personal → Official 发布审核** | 当前Skill Creator只支持personal skill | 需要走官方publishing流程（可能有审核/质量门槛） |
| **多站点适配复杂度** | ChatGPT/Claude/Gemini的UI不同 | M1阶段先支持ChatGPT一种；后续版本逐步扩展 |
| **安全审核更严格** | 公开妙招涉及本地文件操作 | 需要在SKILL.md中极其明确地声明安全边界、权限模型、审计日志 |

### 6.4 ❌ 目前不可行/需要规避的部分

| 限制 | 说明 | 规避方案 |
|------|------|----------|
| 不支持本地stdio MCP | 不能要求用户 `npx xxx` 启动MCP server | 改用E2B内置脚本处理；或要求用户配置HTTP-based remote MCP |
| 不能在Skill中硬编码密钥/token | 安全红线 | 所有敏感信息走运行时用户输入或MCP OAuth |
| 不能假设特定本地路径 | 不同用户的仓库位置不同 | 设计为用户选择/输入repo路径 |
| NetworkProxy作为主路径风险高 | hacky且不稳定 | M1-M3完全不用NetworkProxy；MVP用DOM completion |

---

## 7. 推荐发布策略

### Phase 1: Personal Skill 先行验证（推荐立即开始）

```
你个人使用 → 收集反馈 → 迭代优化 → 再考虑公开发布
```

**理由**：
1. Skill Creator文档提供了完整的personal skill创建/上传流程
2. 可以快速验证M1-M3的实际体验
3. 不受官方审核周期限制
4. 可以自由实验不同的架构选择

**具体步骤**：
1. 用Skill Creator skill创建 `gpt-repo-review-bridge` personal skill
2. bundle包含：SKILL.md + browser-scripts/ + scripts/ + references/ + templates/
3. 上传到 `https://web.tabbit-ai.com/plaza/skills?view=my-skills`
4. 自己反复使用，收集问题

### Phase 2: Official Publishing（验证成熟后）

当personal skill经过充分验证后，考虑公开发布：

**发布前检查清单**：
- [ ] SKILL.md质量达标（含所有必需章节）
- [ ] 安全边界清晰（三层权限模型文档化）
- [ ] 错误处理完善（各种失败场景都有fallback）
- [ ] 至少在3个以上不同AI网站上测试过
- [ ] 有至少5个真实使用场景的成功记录
- [ ] README/cover/description对其他用户友好
- [ ] 不包含任何硬编码密钥/token/个人信息

---

## 8. 公开 vs 个人妙招的关键差异

| 维度 | Personal Skill | Official Published Skill |
|------|---------------|-------------------------|
| 创建方式 | Skill Creator skill (730008) | 官方审核流程（可能另有入口） |
| 可见范围 | 仅自己可见 | 妙招市场所有用户可见 |
| 审核要求 | 无（自用） | 有（质量/安全/合规审核） |
| allowed_tools | 任意组合 | 可能有限制（尤其evaluate_script） |
| 本地文件访问 | 用户自行挂载即可 | 需要更明确的授权提示 |
| url_patterns | 任意设置 | 可能需要审核 |
| 版本管理 | 自己控制 | 可能需要遵循semver |
| MCP依赖 | 自行配置 | 需要声明兼容性 |

---

## 附录A：GPT Bridge Skill 的推荐Bundle结构（草案）

```
gpt-repo-review-bridge/
├── SKILL.md                              # 主规范（~300行）
├── browser-scripts/
│   ├── bridge-harness.js                 # 临时注入：监听回复完成
│   └── response-extractor.js             # 提取assistant消息文本
├── scripts/
│   ├── context-packager.py               # 仓库→context pack
│   ├── secret-scanner.py                 # 密钥扫描+redaction
│   └── review-formatter.py               # 格式化评审输出
├── references/
│   ├── bridge-protocol-v01.md            # 协议规范
│   ├── permission-templates.json         # 5个预设权限模板
│   └── security-checklist.md             # 安全 Checklist
├── templates/
│   └── review-report.md                 # 评审报告输出模板
└── assets/
    └── cover.html                       # 封面
```

**SKILL.md 核心头信息（草案）**：

```yaml
---
name: gpt_repo_review_bridge
title: 🌉 GPT 仓库评审桥接器
description: 将本地代码/文档仓库的上下文桥接到Web端AI（ChatGPT/Claude/Gemini）进行智能评审
when_to_use: 当用户想让AI评审本地仓库、获取代码审查意见、文档改进建议时触发
---
```

**Runtime Requirements**：
```markdown
- Browser login required: yes (登录ChatGPT/Claude/Gemini)
- Sandbox required: yes (运行context packager和secret scanner)
- Page script required: yes (注入bridge harness捕获回复)
- User local folder required: optional (有则全自动读取; 无则手动粘贴)
- MCP required: no (纯内置能力)
```

---

*本文档基于 Tabbit 官方技能文档分析生成，供架构决策参考。*
