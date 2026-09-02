# KEGG 使用指南（中文审阅版）

英文原件：[reference-stack/05-kegg/usage-guide.md](../../reference-stack/05-kegg/usage-guide.md)。

## 推荐检查顺序

1. 确认物种和 KEGG organism code。
2. 确认输入是 gene list、全量 ranking 还是 signed fold-change + universe。
3. 把 query 和 universe 都转换到 KEGG 接受的 ID；输出未映射项。
4. 选择 ORA、GSEA 或 SPIA，并固定最小/最大基因集、FDR、seed。
5. 保存 KEGG 快照/访问日期、原始响应、结果表和 `pathview` 图源数据。

## 原核数据

细菌分析优先保留 locus tag；若物种不在 KEGG genome 列表，考虑 KO 映射。不能套用
人类 `OrgDb` 的 SYMBOL→ENTREZ 流程而不报告映射覆盖率。

## 解释

“某通路富集”只表示在当前数据库快照和背景下的统计关联；只有在预先定义的对照、方向、
复现和实验验证共同支持时，才可以提出机制性 Claim。

