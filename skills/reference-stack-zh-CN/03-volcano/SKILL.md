---
lang: zh-CN
source: ../../reference-stack/03-volcano/SKILL.md
translation-status: review-translation
---

# 火山图与 MA 图

本文件是 [英文 Skill 原件](../../reference-stack/03-volcano/SKILL.md) 的中文审阅版，
专门处理收缩 LFC、显著性阈值、极端 p 值、标签和可读性。

## 核心规则

- 火山图的 x 轴应为明确的（最好是收缩后的）`log2FoldChange`，y 轴为
  `-log10(pvalue)` 或 `-log10(padj)`，图注必须说明是哪一个。
- 收缩 LFC 用于稳定效应大小和排序展示；它不会改变原始 p 值。显著性颜色应由冻结的
  DE 结果列决定，而不是由看图后临时选点决定。
- `padj=NA`、`pvalue=0`、无穷大的 `-log10(p)` 和低丰度基因要有明确显示/截断策略，
  不能静默替换成任意数字。
- MA 图是对低表达依赖、归一化和均值-方差关系的诊断；它不是火山图的装饰版本。
- 标签数量、优先级和重叠处理要可复现；不要只标记“最符合预期”的基因。

## 结论边界

火山图只能支持“哪些基因在指定 contrast 下具有某种效应和统计证据”。它不能单独证明
通路、疾病因果或实验重复性；后续 GO/KEGG 必须从完整 DE 表重新构建输入。

