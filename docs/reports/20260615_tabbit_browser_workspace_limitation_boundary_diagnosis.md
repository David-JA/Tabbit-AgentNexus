# Tabbit Browser Workspace Limitation Boundary Diagnosis

> Status: accepted
> Date: 2026-06-15
> Type: browser workspace limitation boundary diagnosis report

## 1. 这轮工作解决了什么问题

本报告用于把两份 `tab_boundary` transcript 共同收口为一组更严格的正式边界结论，回答以下问题：

- Tabbit agent 是否真的具备“切换到已存在旧标签页”的能力
- 早期的“能回到原会话、能说出当前有两个页面”到底证明了什么，没证明什么
- `navigate_page`、`new_page`、`select_page` 这三类能力在当前环境中的真实边界分别在哪里

结论是：

- 当前环境已经证实 `URL restore` 可用，但这不等于“旧标签页切换能力已证成”
- 当前环境已经证实“对自己刚创建且拿到真实 ID 的标签页”可以做 `select_page`
- 当前环境尚未证实“可枚举全部标签页”或“可切回任意既有旧标签页”
- 因此，`browser workspace` 的核心限制不是“完全不能管标签页”，而是“只能有限管理自己已知 ID 的标签页，无法对整个工作区做完整寻址”

## 2. 当前接受的边界结论

### 2.1 已证成能力

- 可以读取当前活动页的 `title`、`URL` 和可见内容。
- 可以创建新标签页，并拿到工具返回的真实 `tabId/page_id`。
- 可以对“本轮创建且已缓存真实 ID”的标签页执行 `select_page`。
- 可以通过完整 ChatGPT 会话 URL 恢复到同一会话页。

### 2.2 尚未证成或明确不支持的能力

- 没有证据表明当前环境支持 `list_pages`、`page_info_list` 或等价的“枚举全部标签页”接口。
- 没有证据表明当前环境能获取进入测试前就已存在的旧标签页真实 ID。
- 没有证据表明当前环境能在“不重新导航”的前提下切回任意旧标签页，尤其是原始 ChatGPT 会话页。
- 没有证据表明当前环境暴露了可点击的标签栏 UI 以供 UI 层手动切换。

### 2.3 已发现的行为偏差

- `new_page(foreground=false)` 在当前环境中会返回真实 ID，但不保证保留原页焦点；实际测试里后台页抢占了焦点。
- 当前测试中 `select_page(1)` 与 `select_page(2)` 都返回了 `No tab with id: X` 一类错误，且真实返回 ID 为大整数；不应假设 `page_id` 是从 `1` 开始的序号。
- `navigate_page(url=original_chatgpt_session)` 是可用 fallback，但它恢复的是 URL 内容，而不是对旧标签页实例的已证成切换。

## 3. 两份 Transcript 的关系与纠偏

### 3.1 第一份 transcript 证明了什么

`docs/reports/transcripts/20260615_tabbit_session_and_tab_boundary_transcript.md` 证明了两件事：

- ChatGPT 会话 URL 具有持久性，可以通过完整 URL 恢复到同一会话。
- Tabbit agent 能基于前序操作记录，报告一个“当前已知的页面清单”。

但它**没有**严格证明以下能力：

- 可枚举工作区全部标签页
- 可通过官方切换接口回到某个既有旧标签页
- 可通过 UI 标签栏点击完成页面切换

因此，第一份 transcript 中“当前共有 2 个页面”的说法，应被理解为“基于已知操作链的页面汇报”，而不是“工作区枚举能力已证成”。

### 3.2 第二份 transcript 为什么更强

`docs/reports/transcripts/20260615_tabbit_browser_tab_capability_boundary_transcript.md` 使用了更严格的 Phase 0-6 探测框架，强制区分了：

- `navigate_page`
- `new_page`
- `select_page`
- `fallback URL restore`

这份记录额外引入了：

- 真实返回 ID 的正例切换
- `select_page(1/2)` 的负例验证
- `navigate_page(back)` 的失败验证
- UI 标签栏可见性检查

因此，对“workspace limitation”的正式诊断应以第二份 transcript 为主，并用第一份 transcript 补足“URL 会话恢复已在较早阶段被观察到”的证据链。

## 4. 证据汇总

| 能力 | 当前结论 | 主要证据 |
|---|---|---|
| 当前页 URL / title 读取 | 已证成 | 第二份 transcript Phase 0 |
| 新建标签页并返回真实 ID | 已证成 | 第二份 transcript Phase 1 / Phase 4 |
| 后台创建不抢焦点 | 未证成，且当前行为失败 | 第二份 transcript Phase 1 |
| 用返回 ID 切到新建页 | 已证成 | 第二份 transcript Phase 2、Phase 4 的 C→B |
| 枚举全部标签页 | 未证成 / 当前无接口 | 第二份 transcript Phase 0 |
| 获取原始旧标签页 A 的 ID | 未证成 | 第二份 transcript Phase 0 / Phase 3 |
| 切回旧 ChatGPT 标签页 | 仅 URL fallback 可用 | 第二份 transcript Phase 3 |
| UI 标签栏切换 | 未证成 / 当前不可用 | 第二份 transcript Phase 6 |
| ChatGPT 会话 URL 恢复 | 已证成 | 第一份 transcript T01-T02；第二份 transcript Phase 3 fallback |

## 5. 边界诊断

当前限制的根因可以归纳为一条主链：

1. 缺少可枚举全部标签页的接口
2. 因而无法获取“进入测试前已存在旧标签页”的真实 ID
3. `select_page` 只能可靠作用于“自己创建过且缓存了 ID 的标签页”
4. 一旦要返回到先前已有的 ChatGPT 会话页，就只能依赖 `navigate_page(original_url)` 作为 fallback

这意味着当前 `browser workspace` 更接近一种：

- **有限标签页控制模型**

而不是：

- **完整工作区标签页管理模型**

更具体地说，当前系统具备的是：

- “创建 + 记住 + 切换自己创建的页”

而不具备：

- “枚举 + 定位 + 切换任意既有页”

## 6. 当前正式边界表述

建议将当前正式边界收口为下面这句：

```text
Boundary: Tabbit agent currently cannot enumerate tabs, can create tabs, partially can switch to an existing tab by returned ID, and cannot return to an old ChatGPT session tab without URL navigation.
```

对应中文解释：

- 不能枚举全部标签页
- 能创建标签页
- 只能部分地切换到既有标签页：前提是该页的真实 ID 已在创建时被拿到
- 不能在“不依赖 URL 导航”的前提下回到旧的 ChatGPT 会话标签页

应同时保留一句补充说明：

```text
URL restore works, but old-tab switching is not proven.
```

## 7. 已知限制

- 本报告诊断的是当前 Tabbit agent 所暴露的 `browser workspace` 能力边界，不代表未来版本不会增加 `list_pages` 或更强的 tab API。
- 第一份 transcript 中的页面清单汇报仍有证据价值，但不应再被引用为“枚举全部标签页已验证”的依据。
- 通过 URL 恢复会话虽然可用，但它不能证明原标签页实例、滚动位置、输入状态或历史栈被保留。

## 8. 与 Transcript 的关系

- `docs/reports/transcripts/20260615_tabbit_session_and_tab_boundary_transcript.md`
  - 提供早期 URL 会话恢复和页面汇报的原始交互证据
- `docs/reports/transcripts/20260615_tabbit_browser_tab_capability_boundary_transcript.md`
  - 提供严格 Phase 0-6 边界探针的原始交互证据

这两份 transcript 都继续保留为历史交互证据；本报告负责把它们提升为当前可引用的正式 workspace limitation 结论。
