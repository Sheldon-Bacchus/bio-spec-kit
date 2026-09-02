# 表达结果到通路使用指南（中文审阅版）

英文原件：[reference-stack/04-pathway-workflow/usage-guide.md](../../reference-stack/04-pathway-workflow/usage-guide.md)。

## 四个常见入口

1. **ORA**：输入显著 DEG/模块列表，背景是实际可检验基因。
2. **GSEA**：输入全部可检验基因的 signed 排名；先固定排序统计量和随机种子。
3. **GO**：用合适的 OrgDb/keyType；必要时按基因长度使用 GOseq。
4. **KEGG**：使用正确 organism/keyType；保存实时查询的日期和快照。

## 最小交付

输出富集表、输入列表/排名、universe、ID 映射表、数据库版本、参数和冗余折叠后的图；
同时保留未折叠的原始结果，便于审计。无显著 term 时报告“未通过阈值”，不要改阈值直到
出现期望通路。

