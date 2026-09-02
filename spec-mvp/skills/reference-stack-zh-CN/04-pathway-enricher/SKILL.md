---
lang: zh-CN
source: ../../reference-stack/04-pathway-enricher/SKILL.md
translation-status: review-translation
---

# Pathway Enricher：Enrichr 基因集富集适配器

本文件是 [英文 Skill 原件](../../reference-stack/04-pathway-enricher/SKILL.md) 的中文审阅版。
它接收基因列表，调用 Enrichr 查询 KEGG、GO（BP/MF/CC）、Reactome 和 WikiPathways，
输出排序表、气泡图、条形图、Markdown 报告和可复现材料。

## 能做什么

- 解析并去重 HGNC 基因符号；
- 对多个预置数据库返回 term、p 值、调整后 p 值、z-score、combined score 和重叠基因；
- 生成 CSV、PNG、`report.md`、`result.json`、命令、环境和 checksum；
- 在结果为空或 API 失败时给出警告，而不是假装成功。

## 必须写入 Spec 的边界

- 这是**基因集富集适配器**，不做 DEG 拟合、变异检测或因果推断。
- Enrichr 的库名和版本是固定字符串；若库更新，结果会漂移，必须记录访问日期和响应哈希。
- 上游文档称“本地处理”，但实际会把基因符号 POST 到 `https://maayanlab.cloud/Enrichr`；
  因此不能宣称“数据完全不出机器”。在含敏感信息的项目中，应明确脱敏、联网许可和
  API 依赖，或改用本地 GO/KEGG 数据库。
- 富集 p 值是统计关联，不是疾病诊断或机制证明；输入规模过大、背景不当和 ID 错配都会
  造成假阴性/假阳性。

## 与本项目主链的关系

该适配器可作为 GO/KEGG 的外部交叉检查，但主 MVP 仍应以可固定版本的本地/快照流程为
主结果，并把 Enrichr 的实时联网结果标为辅助证据，不能和 DESeq2/edgeR 主模型混为一层。

