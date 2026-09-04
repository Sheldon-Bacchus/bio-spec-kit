---
lang: zh-CN
source: ../../reference-stack/02-deg/SKILL.md
translation-status: review-translation
---

# 差异表达分析（DEG）

本文件是 [英文 Skill 原件](../../reference-stack/02-deg/SKILL.md) 的中文审阅版。它负责
在 bulk RNA-seq 或微阵列表达数据上，对预先定义的两组或多组比较拟合差异表达模型；不适合
把单细胞、甲基化或非表达数据硬套进来。

## 输入、方法和边界

- 表达矩阵：基因在行、样本在列；样本 ID 必须和分组表一一对应。
- 分组/设计：包括 condition、batch、性别和其他预先声明的协变量；contrast 和参考组
  必须写入 Spec。
- raw counts 通常用 DESeq2/edgeR；已归一化连续表达可用 limma/voom；t-test/Wilcoxon
  只能作为探索或敏感性分析，不能与主模型混为一谈。
- 过滤、归一化、FDR 方法、LFC 阈值和随机种子应在看结果前冻结。

## 最小 CLI 形状

```bash
Rscript scripts/main.R \
  --input_file ./expression_matrix.csv \
  --group_file ./group_info.csv \
  --output_dir ./output/ \
  --diff_method limma \
  --p_threshold 0.05 \
  --logfc_threshold 0.1 \
  --seed 42
```

参数名称和默认值以英文原件及实际脚本为准；不要在 Spec 中只写“做 DEG”而不固定模型。

## 必须交付

1. 完整 DE 结果表：估计值、统计量、原始 p、调整后 p、丰度、基因 ID 和过滤/离群原因。
2. 派生的显著列表、排名向量、火山图/MA 图和热图。
3. 样本匹配、重复数、设计矩阵、contrast、软件/包版本和 session 信息。
4. 失败时的结构化错误（输入不存在、样本不匹配、过滤后无基因等），而不是静默继续。

## 统计提醒

调整后 p 值控制的是指定假设集合下的多重检验错误率；它不是效应大小、重复性或因果性。
“`padj < 0.05` 且 `|LFC| > 1`”是常见报告规则，但若要声称幅度本身受 FDR 控制，应使用
预先声明的 `lfcThreshold`/TREAT 等方法。

