# Analysis stack reference skills

这是给本项目人工复核用的 upstream Skill 副本，不是运行时 Skill allowlist。
它们被放在 `spec-mvp/skills/reference-stack/`，不会被 Codex 从
`.agents/skills/` 自动发现，也没有改写上游 `SKILL.md`。

## 建议阅读顺序

```text
00（先读项目 adapter 的输入合同）
01-mds/                    样本关系与降维（先做无偏 QC）
02-deg/                    bulk RNA-seq / microarray 的 DEG 主分析
02-deg-results/            DEG 结果、FDR、tested universe 与下游交接
03-de-visualization/      DE 诊断面板（MA、p-value、MDS/PCA、热图）
03-volcano/                火山图字段、shrunken LFC、阈值和标签合同
04-pathway-workflow/      DEG → ORA/GSEA 的流程路由
04-pathway-enricher/       Enrichr 参考实现（仅作外部实现对照）
05-kegg/                   KEGG organism、ID、universe、快照与拓扑边界
```

严格的执行关系不是一条机械直线：MDS 是 DEG 前的样本/批次诊断，火山图必须在
DEG 结果之后，GO 与 KEGG 是同一 DEG 结果的两个并行下游分支，不存在“先 GO
才能 KEGG”的方法要求。完整说明见同目录的 `analysis-order.md`。

## 与项目 Skill 的关系

| 分析节点 | 项目运行时适配器 | 本目录的参考 Skill |
|---|---|---|
| MDS / 样本 QC | 尚未注册专门适配器 | `01-mds`、`03-de-visualization` |
| DEG | `bulk-pa-luad` | `02-deg`、`02-deg-results` |
| 火山图 | 尚未注册专门适配器 | `03-volcano`、`03-de-visualization` |
| GO / KEGG | `pathway-enrichment` | `04-pathway-workflow`、`04-pathway-enricher`、`05-kegg` |

## 使用边界

1. 参考副本只用于阅读、字段设计、negative case 和 verifier 设计；不直接把外部脚本结果当作本项目 oracle。
2. RNA-seq 原始整数 counts 才能进入 edgeR/DESeq2；FPKM/RPKM/TPM 或芯片强度应走适合的 limma/表达模型路径。
3. MDS 和火山图是从上游数据派生的 artifact，不是独立的生物学结论；验收应检查底层数据和语义，不比较图片像素。
4. GO/KEGG 必须继承已经执行的 DEG 表、方向、tested-gene universe、ID mapping 和数据库版本/访问日期。
5. 细菌与人类宿主必须分开建模和注释；不要把 bacterial locus tag、KO 或 KEGG organism code 与人类 SYMBOL/ENSEMBL 直接混接。
6. 运行时仍只允许使用 `.agents/skills/` 和 `spec-mvp/skills/` 中已经登记的项目适配器；本目录不会改变当前 allowlist。

## 来源

副本来自当前主机的 `C:/Users/ldc/.codex/skills/`，保留原目录中的 `SKILL.md`、参考文档、示例和测试文件。复制日期由版本控制记录确定；若上游更新，必须重新复制并重新审计，不能静默覆盖已冻结的 benchmark 参考。
