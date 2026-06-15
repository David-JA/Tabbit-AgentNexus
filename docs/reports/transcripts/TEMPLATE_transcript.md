# <Transcript Title>

> Status: accepted transcript record
> Type: <transcript type>
> Purpose: <why this transcript is kept>

## 1. 阅读说明

- 本文件用于保留完整原始交互记录，不承担正式 report 的摘要收口职责。
- 当前整理只做结构性优化，不删减原始消息内容。
- 在 Tabbit / Browser 类对话中，`执行步骤` 常常是折叠的过程层；若本次已展开并复制，默认完整保留。
- `输出正文` 是最终对外文本，默认不包含 `执行步骤`。
- 为避免消息体中的 Markdown 标题干扰仓库文档层级，原始消息正文可放入代码块。

## 2. 角色与空间图例

### 2.1 角色

| Role | 中文角色 | 在本记录中的作用 |
|---|---|---|
| `user` | 用户 | <role responsibility> |
| `<agent-id>` | <agent label> | <role responsibility> |

### 2.2 空间

| Space | 含义 |
|---|---|
| `<space-id>` | <space meaning> |
| `<space-id>` | <space meaning> |

## 3. Turn 字段约定

| Field | 含义 |
|---|---|
| `Speaker` | 当前发言主体 |
| `Receiver` | 本轮消息的目标对象 |
| `Relay` | 消息传递方式 |
| `Space` | 本轮消息主要发生或指向的空间 |
| `Intent` | 本轮消息在整体协作中的主要作用 |

## 4. 回合索引

| Turn | Speaker | Receiver | Relay | Space | Intent |
|---|---|---|---|---|---|
| `T01` | `user` | `<agent-id>` | `direct` | `<space-id>` | <intent> |
| `T02` | `<agent-id>` | `user` | `direct` | `<space-id>` | <intent> |

## 5. 结构化转写记录

### Turn T01

| Field | Value |
|---|---|
| `Speaker` | `user` |
| `Receiver` | `<agent-id>` |
| `Relay` | `direct` |
| `Space` | `<space-id>` |
| `Intent` | <intent> |

#### 消息正文

```text
<paste original user message here>
```

### Turn T02

| Field | Value |
|---|---|
| `Speaker` | `<agent-id>` |
| `Receiver` | `user` |
| `Relay` | `direct` |
| `Space` | `<space-id>` |
| `Intent` | <intent> |

#### 执行步骤与中间观察（原文，若已展开并复制）

```text
<paste original execution steps / intermediate observations here>
```

#### 输出正文（原文）

```text
<paste original final output body here>
```

### Turn T03

| Field | Value |
|---|---|
| `Speaker` | `user` |
| `Receiver` | `<agent-id>` |
| `Relay` | `direct` |
| `Space` | `<space-id>` |
| `Intent` | <intent> |

#### 消息正文

```text
<paste original user message here>
```

### Turn T04

| Field | Value |
|---|---|
| `Speaker` | `<agent-id>` |
| `Receiver` | `user` |
| `Relay` | `direct` |
| `Space` | `<space-id>` |
| `Intent` | <intent> |

#### 消息正文

```text
<paste original agent message here>
```

## 6. 可选补充

- 若 transcript 需要被某篇正式 report 引用，可在这里补 `Related report`。
- 若 transcript 中存在明显的 `执行步骤 / 输出正文` 双层结构，且过程层已被实际展开复制，优先拆分展示。
- 若本次没有展开复制 `执行步骤`，不要补写，可直接只保留 `输出正文（原文）` 或 `消息正文（原文）`。
- 若原始消息内部已包含重复段落，也默认保留，除非用户明确要求做对照版或清理版。
