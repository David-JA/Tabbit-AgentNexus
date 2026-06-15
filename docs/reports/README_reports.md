# Reports

本目录保存当前仓库仍有活跃参考价值的 accepted 报告。

## 适合放在这里的内容

- accepted 阶段报告
- accepted 设计报告
- 协议或策略验证总结
- 某个 milestone 的收口说明

### 子目录约定

- 根目录优先放正式 report，即对外可引用的阶段性结论、设计结论或验证结论。
- `transcripts/` 用于保存已接受报告背后的 transcript、evidence record 或结构化交互记录。
- transcript 可以作为正式报告的证据附件长期保留，但不替代正式报告本身。

## 暂不适合放在这里的内容

- 尚未接受的方案草稿
- 一次性 review notes
- 单轮实施中的临时执行记录

这些内容优先留在 `discuss/`。

## 推荐命名

默认推荐：

```text
YYYY-MM-DD_<slug>.md
```

例如：

- `2026-06-14_m1_repo_review_bridge_baseline.md`
- `2026-06-20_session_policy_contract_review.md`

## 报告风格建议

accepted 报告正文可以按需要自由组织，但建议至少回答：

1. 这轮工作解决了什么问题
2. 当前接受的边界或结论是什么
3. 做了哪些验证
4. 已知限制是什么
5. 下一层正式入口在哪里

如果报告只是为一次实施任务服务，而不是 accepted 结论，优先写进 `discuss/` 并在收口后决定是否升级到 `docs/reports/`。
