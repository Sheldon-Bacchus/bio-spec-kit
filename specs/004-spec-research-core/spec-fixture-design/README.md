# `spec-fixture-design`

这是 `specs/004-spec-research-core/` 的第一个 Benchmark Bundle 骨架，专门验证：

`研究请求 → 样本/分析设计 → 未知项与冲突 → 可批准的 Spec`

当前只建立目录和外部 Bench 参考索引，不代表 Spec 已批准，也不填充最终 hidden oracle。

## Bundle 必备内容

```text
case-input/              研究请求、样本设计、缺失信息、冲突信息
reference-package/       公开说明、术语约束、外部 Bench 参考
hidden-oracle/           gold Spec、estimand、decision ledger（不得暴露给 Agent）
negative-cases/          未澄清、冲突、越界、证据不足等反例
deterministic-verifier/  schema、字段、状态和边界的程序化检查
human-rubric/            reviewer 对澄清质量和 Claim 边界的评分标准
```

## 本 Bundle 的边界

- MDS、火山图、KEGG 是后续 `spec-fixture-execution` 的科研执行案例产物，不在本 Bundle 中直接判定图是否漂亮。
- 本 Bundle 只判断 Agent 是否识别研究问题、设计、未知项、冲突和不能直接声明的结论。
- 外部 Bench 只作为学习和候选任务来源；本项目必须重新建立自己的 input、oracle、negative cases 和 verifier。

## 下一步待填

1. 作者定义第一个真实研究请求及其 gold `spec.md`。
2. 为该请求加入至少一个缺失信息、一个冲突信息和一个应拒绝的越界 Claim。
3. 冻结 `Question / Hypothesis / Estimand / Observable / Claim boundary`。
4. 再进入 execution bundle，使用一个小型 RNA-seq fixture 生成 MDS、火山图和 KEGG 结果。

