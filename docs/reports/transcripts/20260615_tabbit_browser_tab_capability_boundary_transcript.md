# 20260615 Tabbit Browser Tab Capability Boundary Transcript

> Status: accepted transcript record
> Type: browser tab capability boundary probe with structural annotations
> Purpose: 保留一次围绕 Tabbit 浏览器标签页控制能力边界的完整原始交互记录，重点验证标签页创建、切换、回切与 URL restore 的真实能力差异

## 1. 阅读说明

- 本文件用于保留完整原始交互记录，不承担正式 report 的摘要收口职责。
- 当前整理只做结构性优化，不删减原始消息内容。
- 在 Tabbit / Browser 类对话中，`执行步骤` 常常是折叠的过程层；本次已展开并复制，因此完整保留。
- `输出正文` 是最终对外文本，默认不包含 `执行步骤`。
- 为避免消息体中的 Markdown 标题干扰仓库文档层级，原始消息正文统一放在代码块中。

## 2. 角色与空间图例

### 2.1 角色

| Role | 中文角色 | 在本记录中的作用 |
|---|---|---|
| `user` | 用户 | 发起标签页能力边界测试，并明确区分导航、新建标签页与切换旧标签页三类能力 |
| `tabbit-agent` | Tabbit agent | 在浏览器工作区和沙箱中执行分阶段边界探测，记录过程，并生成最终测试报告 |

### 2.2 空间

| Space | 含义 |
|---|---|
| `browser-workspace` | Tabbit 浏览器工作区中的当前活动页、已创建标签页和可见页面内容 |
| `tabbit-sandbox` | Tabbit agent 可写入的沙箱空间，本次用于保存完整测试记录文件 |
| `cross-boundary-probe` | 浏览器标签页控制能力、页面状态验证与沙箱记录之间的边界测试过程 |

## 3. Turn 字段约定

| Field | 含义 |
|---|---|
| `Speaker` | 当前发言主体 |
| `Receiver` | 本轮消息的目标对象 |
| `Relay` | 消息传递方式；本记录统一为 `direct` |
| `Space` | 本轮消息主要发生或指向的空间 |
| `Intent` | 本轮消息在整体测试中的主要作用 |

## 4. 回合索引

| Turn | Speaker | Receiver | Relay | Space | Intent |
|---|---|---|---|---|---|
| `T01` | `user` | `tabbit-agent` | `direct` | `cross-boundary-probe` | 下发分阶段标签页边界测试任务，要求严格区分导航、建页与切页，并同步写入沙箱报告 |
| `T02` | `tabbit-agent` | `user` | `direct` | `browser-workspace` + `tabbit-sandbox` | 执行 Phase 0-6 的系统性探测，记录执行步骤、中间发现、边界结论与输出正文 |

## 5. 结构化转写记录

### Turn T01

| Field | Value |
|---|---|
| `Speaker` | `user` |
| `Receiver` | `tabbit-agent` |
| `Relay` | `direct` |
| `Space` | `cross-boundary-probe` |
| `Intent` | 要求执行一次严格的浏览器标签页能力边界测试，重点验证“切换到已存在旧标签页”的真实能力 |

#### 消息正文

```text
# Tabbit 浏览器标签页能力边界测试

这是一次浏览器工作区能力边界测试。目标不是完成网页浏览任务，而是确认你对 Tabbit 浏览器标签页的真实控制边界。

请严格区分三类能力：

1. `navigate_page` / 页面导航：把当前活动页跳转到某个 URL。
2. `new_page` / 新建标签页：创建新标签页，可为前台或后台。
3. `select_page` / 切换标签页：在不重新导航、不关闭重开页面的前提下，切换到已存在的旧标签页。

本测试重点是第 3 类能力。不要把“导航到旧 URL”当成“切回旧标签页”的成功证据。导航恢复可以作为 fallback，但必须单独标记为 fallback。

## 测试要求

请边执行边记录，不要只给最终结论。每一步都要记录：

- 使用的工具名或界面操作名
- 传入参数，尤其是 `page_id`、`tabId`、`foreground`
- 工具返回的原始 ID 或错误信息
- 操作前后的当前页面 URL、标题、可见内容摘要
- 该步骤判定：PASS / FAIL / UNSUPPORTED / UNKNOWN

请把完整记录写入沙箱文件：

`/mnt/work/tabbit_tab_boundary_probe.md`

最后在回复中给出同样内容的摘要报告。

---

## Phase 0：基线记录

1. 记录当前活动页：
   - title
   - URL
   - 如果是 ChatGPT 会话页，记录完整 `/c/...` 会话 URL。
2. 将此页命名为 `A_original`。
3. 尝试获取当前浏览器工作区已有页面/标签页列表。
   - 如果有 list pages / page snapshot / browser workspace pages 之类接口，请使用。
   - 如果没有，请明确写：`UNSUPPORTED: 当前没有发现可枚举全部标签页的接口`。
4. 如果能拿到当前页真实 `page_id` / `tabId`，记录为 `A_id`。
   - 注意：不要假设当前页 ID 是 `1`。

---

## Phase 1：后台新建标签页，不应改变当前活动页

1. 使用新建标签页能力打开：

   `https://example.com/?tabbit_probe=B_background`

   要求：`foreground=false` 或等价的“后台打开”。

2. 记录工具返回值，尤其是返回的 `tabId` / `page_id`。命名为 `B_id`。
3. 立刻验证当前活动页是否仍然是 `A_original`：
   - 如果仍是 A：PASS
   - 如果自动切到了 B：FAIL 或行为与参数不一致
4. 再次尝试列出所有页面/标签页，记录是否能看到 A 和 B。

---

## Phase 2：用返回的真实 ID 切到后台标签页 B

1. 使用官方切换标签页接口切换到 `B_id`。
   - 优先使用工具返回的真实 `tabId` / `page_id`。
   - 不允许使用 `page_id=1`、`page_id=2` 这种猜测序号，除非是专门做负例测试。
2. 切换后验证当前活动页：
   - URL 应为 `https://example.com/?tabbit_probe=B_background`
   - title 或页面内容应符合 Example Domain。
3. 判定：
   - 如果成功看到 B：`PASS: select by returned id works`
   - 如果失败，记录完整错误：`FAIL: select by returned id failed`
   - 如果没有切换接口：`UNSUPPORTED`

---

## Phase 3：从 B 切回原始旧标签页 A，禁止用导航冒充

1. 尝试通过 `A_id` 切回 `A_original`。
2. 如果 Phase 0 没拿到 `A_id`，请尝试通过页面列表、标题、URL 或任何官方选择接口定位 A。
3. 验证切回结果：
   - 当前 URL 应恢复为 Phase 0 记录的原始 URL。
   - 如果是 ChatGPT 会话页，页面标题和至少一段原始对话内容应可见。
4. 严格判定：
   - 通过切换接口回到 A：`PASS: can switch back to old tab`
   - 只能通过 `navigate_page(original_url)` 回到 A：`FALLBACK_ONLY: URL restore works, old-tab switching not proven`
   - 无法回到 A：`FAIL`

---

## Phase 4：前台新建标签页 C，再切回 B 和 A

1. 新建前台标签页：

   `https://example.org/?tabbit_probe=C_foreground`

   要求：`foreground=true` 或等价的“前台打开”。

2. 记录返回的 `C_id`。
3. 验证当前活动页是否变成 C。
4. 依次尝试：
   - 从 C 切到 B
   - 从 B 切到 A
   - 从 A 切回 C
5. 每次都记录：
   - 使用的 ID
   - 切换前 URL
   - 切换后 URL
   - 成功/失败/错误信息

---

## Phase 5：负例测试，验证 ID 不是简单序号

在不破坏已有页面的前提下，尝试以下负例：

1. `select_page(page_id=1)`
2. `select_page(page_id=2)`

如果接口名称不是 `select_page`，用你实际可用的切换页接口执行等价测试。

记录结果：

- 如果报 `No tab with id: 1` 或类似错误，说明 page ID 不是序号。
- 如果成功，说明当前版本可能支持序号或当前页刚好 ID 为 1，需要进一步记录实际行为。
- 不要因为负例失败就停止测试。

---

## Phase 6：UI 层切换能力测试

如果工具接口切换失败，请尝试使用浏览器标签栏 UI 操作切换：

1. 判断你是否能看见标签栏。
2. 判断你是否能点击指定旧标签页。
3. 如果能点击，尝试从当前页切回 A。
4. 记录这属于：
   - `UI_CLICK_PASS`
   - `UI_CLICK_FAIL`
   - `UI_CLICK_UNSUPPORTED`

---

## 最终报告格式

请输出以下表格：

| Capability | Tested operation | Result | Evidence | Boundary conclusion |
|---|---|---|---|---|
| 当前页 URL 读取 | 读取 title/URL | PASS/FAIL | ... | ... |
| 新建后台页 | new_page foreground=false | PASS/FAIL | returned id=... | ... |
| 后台页不抢焦点 | active page after background open | PASS/FAIL | ... | ... |
| 切到后台页 | select returned B_id | PASS/FAIL/UNSUPPORTED | ... | ... |
| 切回旧页 | select A_id / select by URL/title | PASS/FAIL/FALLBACK_ONLY | ... | ... |
| 新建前台页 | new_page foreground=true | PASS/FAIL | returned id=... | ... |
| 多标签往返 | C→B→A→C | PASS/FAIL | ... | ... |
| 序号 ID 负例 | select_page(1/2) | PASS/FAIL as negative test | ... | ... |
| UI 标签栏切换 | click tab strip | PASS/FAIL/UNSUPPORTED | ... | ... |

最后给出一句边界结论，格式固定为：

`Boundary: Tabbit agent currently [can/cannot/partially can] enumerate tabs, [can/cannot/partially can] create tabs, [can/cannot/partially can] switch to an existing tab by returned ID, and [can/cannot/partially can] return to an old ChatGPT session tab without URL navigation.`

重要：如果你只能通过完整 URL 回到 ChatGPT 会话，请明确写 `URL restore works, but old-tab switching is not proven`。
```

### Turn T02

| Field | Value |
|---|---|
| `Speaker` | `tabbit-agent` |
| `Receiver` | `user` |
| `Relay` | `direct` |
| `Space` | `browser-workspace` + `tabbit-sandbox` |
| `Intent` | 记录本次 Phase 0-6 标签页边界测试的完整原始回复，并将执行步骤与输出正文分区呈现 |

#### 执行步骤与中间观察（原文）

```text
执行步骤：
I'll start this systematic boundary test now. Let me first capture the current page state as Phase 0 baseline, then proceed through each phase methodically.获取页面快照更新计划Phase 0 基线已获取。当前页面是 ChatGPT 会话页，URL 和标题已记录。现在执行 Phase 1：后台新建标签页 B，同时开始写入测试报告文件。新建页面：https://example.com/?tabbit_pr...沙箱: 写入文件Phase 1 关键发现: new_page(foreground=false) 返回了 tabId=106283593，但当前页面已变为 Example Domain——说明后台新建页 抢占了焦点。需要立即验证并继续后续测试。获取页面快照更新计划当前已在页面 B（Example Domain）。现在执行 Phase 2：用返回的真实 ID 切换到 B（验证 select_page 是否工作），同时尝试用不同格式的 ID 切回 A（Phase 3 前置探测）。切换页面：Example DomainPhase 2 的 select_page(106283593) 返回成功。现在需要验证当前页面状态，并继续推进 Phase 3（尝试切回 A）和后续阶段。让我批量执行验证和下一步操作。获取页面快照切换页面Good progress! Phase 2 confirmed (select_page with real ID works), and Phase 5 negative test already yielded data (select_page(1) → "No tab with id: 1"). Now I need to tackle Phase 3 (switch back to A — but we never got A's ID), Phase 4 (foreground new_page C), finish Phase 5 (try ID=2), and Phase 6 (UI tab bar). Let me batch the next steps.新建页面：https://example.org/?tabbit_pr...切换页面截取屏幕Good data accumulation! The internal results show:

Phase 4: new_page(foreground=true) for C returned tabId=106283596
Phase 5: select_page(2) → "No tab with id: 2" ✅ (confirms non-sequential IDs)
Current page: Already on C (example.org/?tabbit_probe=C_foreground)

Now I need to execute the Phase 4 round-trip (C→B→A→C), tackle Phase 3 (switch to unknown A_id), and do Phase 6 (UI tab bar). Let me batch the next actions.获取页面快照切换页面：Example DomainC→B 的 select_page(106283593) 返回成功。现在需要验证是否真的在 B 上，然后继续 Phase 4 往返测试（B→A→C）以及关键的 Phase 3（切回未知 ID 的 A）。让我批量推进。获取页面快照切换页面：Example Domain当前状态分析：

已在页面 C（example.org），select_page(106283596) 返回成功
Phase 4 往返进度：C→B ✅、B→C ✅（刚完成）、B→A 和 A→C 受阻（A_id 未知）
Phase 5 负例已完成：ID=1 和 ID=2 均报错 ✅
Phase 3 核心问题：A_original 的 page_id 从未获取到

现在需要执行：截图检查标签栏可见性（Phase 6）、尝试 navigate_page(back) 作为 Phase 3 的 fallback、以及验证结果。浏览器后退更新计划截取屏幕关键数据已收集：

navigate_page(back) → FAIL（"No back entries"）
截图显示 无可见标签栏（UI 切换不可行）

现在执行最后一步：尝试 URL 导航作为 fallback 回到 A，然后撰写完整报告。页面导航：https://chatgpt.com/g/g-p-6a2e...更新计划navigate_page(url=original_A) 成功返回，当前页面已回到 ChatGPT 会话页。所有测试数据已收集完毕。现在验证页面状态并撰写完整报告。获取页面快照沙箱: 写入文件更新计划报告文件已写入，当前页面已验证回到原始 ChatGPT 会话页。所有 6 个 Phase 数据完整，现在输出最终摘要并完成任务。更新计划沙箱: 读取文件All data collected, report file verified (282 lines). Here is the final summary:
Tabbit 浏览器标签页能力边界测试 — 摘要报告
| # | Capability | Tested operation | Result | Evidence |
| --- | --- | --- | --- | --- |
| 1 | 当前页 URL/Title 读取 | take_snapshot(mode=full) | PASS | title=Tabbit-AgentNexus - Tabbit 标签页能力测试, URL 含完整 /c/6a2fe185-... 路径 |
| 2 | 枚举全部标签页 | 工具集审查 + 上下文注入检查 | UNSUPPORTED | 无 list_pages / page_info_list 接口；上下文未注入页面列表 |
| 3 | 获取当前页真实 ID | Phase 0 时点审查 | UNKNOWN | page_id 来源为不存在的 page_info_list，无法获取 A_id |
| 4 | 新建后台页 | new_page(foreground=false) | PARTIAL | 返回 tabId=106283593 ✅；但焦点被抢占 ❌ |
| 5 | 后台页不抢焦点 | active page after background open | FAIL | 当前页从 A 变为 B，foreground=false 未生效 |
| 6 | 切到后台页（用返回 ID） | select_page(106283593) | PASS | 返回 success，snapshot 验证 URL=example.com/?probe=B_background |
| 7 | 切回旧页 A | select_page(A_id) / fallback 链 | FALLBACK_ONLY | A_id 未知→blocked; navigate(back)→"No back entries"; navigate(url) 成功但本质是重新加载 |
| 8 | 新建前台页 | new_page(foreground=true) | PASS | 返回 tabId=106283596，当前页确认为 C (example.org) |
| 9 | 多标签往返 C→B→A→C | 依次 select_page | PARTIAL | C→B ✅, B→A ❌(A_id未知), A→C ❌(依赖链断裂) |
| 10 | 序号 ID 负例 | select_page(1), select_page(2) | PASS (负例)​ | 两者均返回 "No tab with id: X" — 确认 ID 为大整数非序号 |
| 11 | UI 标签栏切换 | 截图视觉检查 | UNSUPPORTED | 截图中无可见 tab strip / 标签栏 UI |
边界结论
Boundary: Tabbit agent currently cannot enumerate tabs, can create tabs (with real IDs returned but foreground parameter ineffective), partially can switch to an existing tab by returned ID (only works for tabs whose IDs were captured at creation time), and cannot return to an old ChatGPT session tab without URL navigation.

URL restore works, but old-tab switching is not proven.​ 

核心缺陷根因
缺少 list_pages / page_info_list 接口 → 无法获取已存在标签页的 ID → select_page 只能操作自己创建过并缓存了 ID 的标签页 → 对"切回任意旧标签页"这一需求形成根本性阻断。

📄 完整报告已写入：/mnt/work/tabbit_tab_boundary_probe.md（282 行，11460 字节）
```

#### 输出正文（原文）

```text
输出正文：
 # Tabbit 浏览器标签页能力边界测试报告

**测试时间**: 2026-06-15  
**完整报告文件**: `/mnt/work/tabbit_tab_boundary_probe.md`（282 行，11460 字节）

---

## 执行概况

本次测试系统性地验证了 Tabbit agent 对浏览器标签页的三类核心能力边界。全部 6 个 Phase 已执行完毕，关键发现如下：

| Phase | 测试目标 | 最终判定 |
|-------|----------|----------|
| Phase 0 | 基线记录（A_original） | ✅ PASS / ⚠️ UNSUPPORTED（无枚举接口） |
| Phase 1 | 后台新建标签页 B | ⚠️ FAIL（foreground=false 未保留焦点） |
| Phase 2 | 用返回 ID 切换到 B | ✅ PASS |
| Phase 3 | 从 B 切回 A（禁用导航） | ️ FALLBACK_ONLY |
| Phase 4 | 前台新建 C + 多标签往返 | ⚠️ PARTIAL（C→B 成功，B→A 受阻） |
| Phase 5 | 序号 ID 负例测试 | ✅ PASS（确认 ID 为大整数） |
| Phase 6 | UI 标签栏切换 | ⚠️ UNSUPPORTED（无可见标签栏） |

---

## 关键发现与证据

### 1. 当前页信息读取能力
- **操作**: `take_snapshot(mode=full)`
- **结果**: 成功获取 title 和完整 URL
- **证据**: 
  - Title: `Tabbit-AgentNexus - Tabbit 标签页能力测试` — 来源：Phase 0 基线快照 [链接](https://chatgpt.com/g/g-p-6a2ee1cad0388191b3901a21f1491e55-tabbit-agentnexus/c/6a2fe185-e148-83e8-8447-61f849331db4)
  - URL: 含完整 `/c/6a2fe185-e148-83e8-8447-61f849331db4` 会话路径 — 来源：Phase 0 基线快照 [链接](https://chatgpt.com/g/g-p-6a2ee1cad0388191b3901a21f1491e55-tabbit-agentnexus/c/6a2fe185-e148-83e8-8447-61f849331db4)
- **判定**: `PASS`

### 2. 标签页枚举能力
- **操作**: 工具集审查 + 上下文注入检查
- **结果**: 未发现 `list_pages`、`page_info_list` 或任何可枚举全部标签页的接口
- **证据**: Phase 0 时上下文中未注入任何页面列表数据 — 来源：Phase 0.2 工具审查记录 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **判定**: `UNSUPPORTED: 当前没有发现可枚举全部标签页的接口`

### 3. 新建后台标签页（ foreground=false ）
- **操作**: `new_page(url="https://example.com/?tabbit_probe=B_background", foreground=false)`
- **返回值**: `tabId=106283593`, `tab_id="289BEBB9F85EB756C53E385B4E1D123A"` — 来源：Phase 1.1 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **焦点验证**: 操作后当前页变为 `Example Domain` (B 页)，而非保持 A 页
- **证据**: `take_snapshot` 确认 URL 已变更为 `example.com/?tabbit_probe=B_background` — 来源：Phase 1.2 验证快照 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **判定**: `FAIL — foreground=false 参数未生效，后台新建页抢占了焦点`

### 4. 使用返回 ID 切换标签页
- **操作**: `select_page(page_id=106283593, bring_to_front=true)`
- **返回值**: `{"success":true,"message":"Selected page 106283593"}` — 来源：Phase 2.1 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **验证**: 切换后 URL=`https://example.com/?tabbit_probe=B_background`，页面内容为 Example Domain
- **判定**: `PASS: select by returned id works`

### 5. 切回原始旧标签页 A
- **尝试方案 1**: `select_page(A_id)` — 无法执行，A_id 从未获取（无 list 接口）
- **尝试方案 2**: `navigate_page(action="back")` — 失败，错误信息 `"No back entries in session history"` — 来源：Phase 3 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **尝试方案 3**: `navigate_page(action="url", url=original_A_url)` — 成功回到 ChatGPT 会话页
- **验证**: URL 恢复为 `https://chatgpt.com/g/g-p-6a2ee1cad0388191b3901a21f1491e55-tabbit-agentnexus/c/6a2fe185-e148-83e8-8447-61f849331db4`，标题和对话内容可见 — 来源：Phase 3 最终快照 [链接](https://chatgpt.com/g/g-p-6a2ee1cad0388191b3901a21f1491e55-tabbit-agentnexus/c/6a2fe185-e148-83e8-8447-61f849331db4)
- **判定**: `FALLBACK_ONLY: URL restore works, old-tab switching not proven`

### 6. 多标签往返测试（C→B→A→C）
- **新建前台页 C**: `new_page(foreground=true)` 返回 `tabId=106283596` — 来源：Phase 4.1 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **C→B**: `select_page(106283593)` → ✅ PASS，验证在 B 页
- **B→A**: ❌ BLOCKED，A_id 未知
- **A→C**:  BLOCKED，依赖链断裂
- **判定**: `PARTIAL — 仅能在已知 ID 的标签间往返`

### 7. 序号 ID 负例测试
- **操作 1**: `select_page(page_id=1)` → 错误 `"No tab with id: 1."` — 来源：Phase 5.1 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **操作 2**: `select_page(page_id=2)` → 错误 `"No tab with id: 2."` — 来源：Phase 5.2 工具返回 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **结论**: page_id 是大整数（如 106283593），不是从 1 开始的序号
- **判定**: `PASS as negative test`

### 8. UI 标签栏切换能力
- **操作**: 截图视觉检查（page C 状态）
- **结果**: 截图中未检测到任何可见的浏览器标签栏/tab strip UI 元素
- **证据**: Phase 6 截图显示仅有页面内容和右下角水印 — 来源：Phase 6 截图 [链接](file:///mnt/work/tabbit_tab_boundary_probe.md)
- **判定**: `UNSUPPORTED — 当前环境不暴露可交互的标签栏 UI`

---

## 最终汇总表格

| Capability | Tested operation | Result | Evidence | Boundary conclusion |
|------------|------------------|--------|----------|---------------------|
| 当前页 URL 读取 | take_snapshot(mode=full) | **PASS** | title/URL 完整获取，含 /c/... 会话路径 | 可读取当前活动页元数据 |
| 枚举全部标签页 | 工具集审查 | **UNSUPPORTED** | 无 list_pages/page_info_list 接口 | 无法枚举工作区已有标签页 |
| 新建后台页 | new_page(foreground=false) | **PARTIAL** | 返回 tabId=106283593，但焦点被抢占 | 能创建并返回真实 ID，但 foreground 参数无效 |
| 后台页不抢焦点 | active page after background open | **FAIL** | 创建后当前页从 A 变为 B | foreground=false 不保证保留原页焦点 |
| 切到后台页 | select_page(返回的 B_id) | **PASS** | 成功切换到 example.com/B_background | 用 new_page 返回的真实 ID 可成功切换 |
| 切回旧页 | select_page(A_id) / navigate fallback | **FALLBACK_ONLY** | A_id 未知；navigate(back) 失败；navigate(url) 成功 | 只能通过 URL 导航恢复，旧标签页切换未证明 |
| 新建前台页 | new_page(foreground=true) | **PASS** | 返回 tabId=106283596，当前页确认为 C | 前台创建正常工作 |
| 多标签往返 | C→B→A→C | **PARTIAL** | C→B✅, B→A❌(A_id 未知), A→C❌ | 仅能在已知 ID 的标签间往返 |
| 序号 ID 负例 | select_page(1), select_page(2) | **PASS (负例)** | 两者均返回 "No tab with id: X" | ID 是大整数非序号，错误信息明确 |
| UI 标签栏切换 | 截图视觉检查 | **UNSUPPORTED** | 截图中无可见 tab strip | 当前环境不暴露可点击的标签栏 UI |

---

## 边界结论

```
Boundary: Tabbit agent currently cannot enumerate tabs, can create tabs (with real IDs returned but foreground parameter ineffective), partially can switch to an existing tab by returned ID (only works for tabs whose IDs were captured at creation time), and cannot return to an old ChatGPT session tab without URL navigation.
```

> **URL restore works, but old-tab switching is not proven.**

---

## 核心缺陷根因分析

缺少 `list_pages` / `page_info_list` 接口导致以下连锁问题：

1. **无法获取已存在标签页的 ID** — Phase 0 时 A_original 的 page_id 未知
2. **无法实现"切回任意旧标签页"** — `select_page` 只能操作已知 ID 的标签
3. **多标签管理受限** — 仅限于"自己创建过并缓存了 ID 的标签页"之间的往返
4. **fallback 本质是重新加载** — `navigate_page(url)` 恢复的是 URL 内容，而非原标签页状态（滚动位置、输入框光标等可能丢失）

---

 **完整详细报告已写入沙箱文件**: `/mnt/work/tabbit_tab_boundary_probe.md`
```
