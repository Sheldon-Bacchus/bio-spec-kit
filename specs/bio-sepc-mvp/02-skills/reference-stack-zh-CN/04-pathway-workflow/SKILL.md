---
lang: zh-CN
source: ../../reference-stack/04-pathway-workflow/SKILL.md
translation-status: review-translation
---

# 从表达结果到通路：GO/KEGG 工作流

本文件是 [英文 Skill 原件](../../reference-stack/04-pathway-workflow/SKILL.md) 的中文审阅版。
它负责把 DE 结果路由到 ORA 或 GSEA、准备 ID 和 universe、调用 GO/KEGG 等数据库，并在解释
前处理冗余；它不替代每个数据库或每种统计方法的专门 Skill。

## 第一决定：ORA 还是 GSEA

这是由输入决定的，不是个人偏好：

- 如果几乎所有可检验基因都有可靠的 signed statistic（例如 DESeq2 Wald `stat`），使用
  **GSEA**，输入是按降序排列的命名向量，不设任意显著性截断。
- 如果只有预先选出的 gene list（显著 DEG、共表达模块、GWAS hits），使用 **ORA**，并
  明确可检验的 **background universe**。

把有完整排名的数据先二值化会丢失弱而协调的信号；把 ORA 的背景写成“全基因组”会把
表达/检测偏差误报成富集。

## 共同契约

记录基因 ID 类型、物种、映射数据库、成功/失败映射、universe、方法（ORA/GSEA）、
多重检验、最小/最大基因集大小、随机种子、数据库版本/访问日期、冗余折叠规则和原始
响应。GO 通常可使用本地 OrgDb/GO.db；KEGG 查询常为实时 REST，必须固定快照。

## 解释边界

富集结果是“在指定 universe、统计方法和数据库版本下，某些基因集出现统计关联”。
它不能单独证明通路方向、细胞机制、疾病因果或实验复现。`compareCluster` 等并排比较应
使用同一个模型和同一套规则，不应直接比较不同运行的原始 p 值。

