# N1 Browser Adapter Contract Reference

当前 skill 只负责 local-only dry run，但后续若要接 Tabbit browser path，应遵循现有 N1 spec 中冻结的最小 contract：

- `open_or_confirm_target_page()`
- `submit_text_to_chat(text)`
- `wait_until_assistant_complete(timeout)`
- `read_last_assistant_message()`
- `cleanup_page_harness()`

## 当前要求

- 优先 `GUI-first`
- 允许 `snapshot` 辅助判断
- 只有 live probe 证明 GUI 路径不稳定时，才引入最小 `evaluate_script` fallback
- N1 不得使用 `NetworkProxy`

## 与本 skill 的关系

本 skill 的输出 `session_summary.json` 已包含：

- selected files
- bytes total
- redaction count
- default exclusions
- `ready_to_send` 状态

后续 browser adapter 应消费这些产物，而不是重做 sandbox-side file selection、policy 或 redaction。
