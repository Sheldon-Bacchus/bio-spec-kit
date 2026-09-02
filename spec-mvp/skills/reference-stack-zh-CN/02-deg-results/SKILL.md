---
lang: zh-CN
source: ../../reference-stack/02-deg-results/SKILL.md
translation-status: review-translation
---

# DE 结果提取、过滤、注释与导出

本文件是 [英文 Skill 原件](../../reference-stack/02-deg-results/SKILL.md) 的中文审阅版，
用于把 DESeq2/edgeR 的拟合结果转换成可复核的完整表、显著列表、GSEA 排名向量和 ORA 输入。

## 最重要的规则：`padj = NA` 不是普通缺失值

DESeq2 中至少要区分三种原因：

1. **独立过滤**：有有限的原始 `pvalue`，但丰度低于自动过滤阈值；它没有被检验结果“丢失”，
   只是没有进入 BH 调整。
2. **Cook 距离离群**：某个样本对该基因的影响过大，`pvalue` 和 `padj` 可能都为 `NA`；
   应诊断该样本，而不是无条件删除。
3. **某组全零/信息不足**：没有足够信息估计差异；通常在预处理阶段过滤或明确接受。

盲目 `na.omit()` 会静默丢掉可能有生物学意义的低丰度调控因子。每个 `NA` 的原因和处理
应进入结果表或诊断日志。

## 结果和下游输入

- 默认多重检验可用 BH；需要提高同一 FDR 下的检出力时可预先声明 IHW；需要“效应方向
  出错的概率”时可报告 lfsr/s-value。它们不是同一个指标。
- 若幅度是预先声明的假设，使用 TREAT 或 `lfcThreshold`；不要把事后 LFC 筛选包装成
  幅度假设已受 FDR 控制。
- GSEA 排名优先使用 DESeq2 的 `stat` 或等价的带精度信息的 signed statistic，不使用
  未收缩的 LFC 直接排序。ORA 背景必须是实际进入 DE 检验的全部可测试基因。
- 注释要记录 ID 类型、映射成功率、数据库版本和未映射基因；导出的完整表应保留未显著行。

## MVP 验收

输入结果对象、设计/contrast、过滤规则和软件版本可被第三方重建；派生出的显著列表、
排名向量和 universe 能由完整 DE 表重新计算；不同 FDR 方法或过滤策略的变化不会被覆盖。

