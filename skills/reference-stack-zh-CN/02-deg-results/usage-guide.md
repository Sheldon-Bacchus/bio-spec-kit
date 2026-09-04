# DE 结果使用指南（中文审阅版）

英文原件：[reference-stack/02-deg-results/usage-guide.md](../../reference-stack/02-deg-results/usage-guide.md)。

## 常用任务

- **筛选**：先确认列名（`padj`、`adj.P.Val`、`FDR` 等），再按预先声明的阈值生成列表。
- **诊断**：统计 `padj=NA` 的原因，检查 p 值直方图、baseMean、离群样本和重复数。
- **注释**：记录原始 ID、目标 ID、映射数据库、映射损失和一对多映射处理。
- **导出**：同时导出完整 DE 表、显著表、GSEA 排名向量、ORA universe 和可读性注释表。

不要只交付“top 20 genes”或一张 Excel 截图；那无法重算，也不能支撑后续 GO/KEGG 审计。

