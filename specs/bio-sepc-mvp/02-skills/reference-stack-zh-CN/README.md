# 转录组首轮分析技能：中文审阅备份

本目录是 `spec-mvp/skills/reference-stack/` 的中文审阅镜像，服务于首轮
MDS/PCA → DEG → 火山图/MA → GO/KEGG 的 Spec 设计和测试。英文原件仍然是
审计基准，未被修改；本目录也不属于 `.agents/skills/`，不会被 Codex 运行时自动发现。

## 翻译策略

- 说明性内容用中文整理，保留关键英文术语、函数名、参数名、文件名、命令和 URL。
- 代码块、CLI 选项和输出文件名不翻译，避免复制到 VS Code 后失效。
- 每份中文文件都标出对应英文原件；需要逐段核对时以英文原件为准。
- 这是“可审阅、可定位”的备份，不把中文文件冒充成新的运行时 Skill，也不改变上游算法含义。

## 建议阅读顺序

```text
01-mds → 02-deg → 02-deg-results → 03-de-visualization / 03-volcano
       → 04-pathway-workflow → 05-kegg
```

真正执行时，MDS/PCA 是样本诊断；DEG 是主要统计推断；火山图/MA/热图是结果表达；
GO 与 KEGG 是下游富集分支。GO/KEGG 不是简单地“拿显著基因再跑一下”：必须先决定
ORA 还是 GSEA，定义可检验基因 universe，完成 ID 映射，并记录数据库版本和访问日期。

## 文件对应关系

| 中文审阅文件 | 英文原件 | 作用 |
|---|---|---|
| `01-mds/*` | `reference-stack/01-mds/*` | PCA、MDS、t-SNE、UMAP、PHATE 的选择、参数与局限 |
| `02-deg/*` | `reference-stack/02-deg/*` | limma/DESeq2/edgeR 及 CLI、算法、排错 |
| `02-deg-results/*` | `reference-stack/02-deg-results/*` | DE 表提取、`padj=NA`、FDR、注释和下游输入 |
| `03-de-visualization/*` | `reference-stack/03-de-visualization/*` | MA、火山图、热图、PCA 等表达规范 |
| `03-volcano/*` | `reference-stack/03-volcano/*` | 收缩后的 LFC、阈值和极端 p 值处理 |
| `04-pathway-enricher/*` | `reference-stack/04-pathway-enricher/*` | Enrichr 多数据库基因集富集适配器 |
| `04-pathway-workflow/*` | `reference-stack/04-pathway-workflow/*` | DE 到 GO/KEGG 的 ORA/GSEA 路由和证据边界 |
| `05-kegg/*` | `reference-stack/05-kegg/*` | KEGG ORA、GSEA、SPIA 拓扑分析和版本固定 |

## 与 MVP/SPEC 的关系

中文备份只帮助人工阅读。MVP 的可执行合同仍应引用项目适配器、输入/输出 schema、
固定软件环境、随机种子、数据库快照、验收阈值和 provenance。上游 Skill 的建议不能
自动变成项目结论；例如“富集显著”只能证明在指定 universe、方法和数据库版本下的
统计关联，不能直接证明疾病机制。

## 关键审计提醒

1. “MDS”在不同工具中可能指 classical MDS，也可能被口头用来指 PCA。Spec 必须把
   实际算法写明，不能仅写一个含糊缩写。
2. DEG 结果表必须冻结完整结果（包括未显著、`padj=NA` 和过滤原因），再派生显著列表、
   排名向量和作图表；不能只保存被筛选后的 CSV。
3. ORA 的 universe 是真正进入检验的基因，而不是全基因组；GSEA 要使用所有可排名基因。
4. KEGG 是实时数据库；公开结果必须记录访问日期并保存 `gson` 或等价快照。
5. Enrichr 适配器会把基因符号发到公共 API；“本地运行”不等于“数据完全不出机器”，
   因此隐私和联网依赖必须写入 Spec。

原始入口：[英文 reference-stack README](../reference-stack/README.md)。

