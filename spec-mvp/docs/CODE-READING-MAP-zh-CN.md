# 相关 Skills 代码阅读地图（中文）

本文件记录首轮对 MDS/PCA、DEG、火山图、GO/KEGG 相关代码的阅读结果。它不是新的
运行时 Skill，也不是 Spec 合同；它是学习和审计索引。

## 1. 你的学习方式叫什么

最准确的专业表述是：

> **分层递进式源代码阅读**（layered/progressive program comprehension）
> + **自底向上的调用链追踪**（bottom-up call-chain tracing）
> + **面向方法的包级审计**（method-centric package audit）
> + **端到端数据流/垂直切片追踪**（end-to-end dataflow / vertical-slice tracing）。

对应的层级不是重新学习 C/Python 语法，而是：

| 层级 | 你要看什么 | 生信对应问题 |
|---|---|---|
| 语言构造 | 赋值、条件、循环、异常、管道、对象 | 这一行怎样改变状态或数据 |
| 函数 | 输入、返回值、副作用、错误 | 这个函数的契约和失败条件是什么 |
| 模块 | 多个函数的职责和调用关系 | 一个方法模块怎样完成一项分析 |
| 包/API | 包函数、对象类、参数和版本 | 统计模型或数据库接口真正做了什么 |
| 脚本入口 | CLI、配置、日志、文件读写、流程编排 | 输入怎样经过整个分析并变成证据 |
| 垂直切片 | 从真实输入到最终表/图/Claim | 这条流程能否重算、验证、审计 |

因此你的重点应叫**方法中心的代码阅读**，而不是“从语法学到脚本”本身。语法只要能
读懂控制流即可；真正要分析的是包函数的估计对象（estimand）、数据尺度、统计假设、
返回对象、版本行为和失败恢复。

## 2. 总调用链

```text
输入矩阵 + 元数据 + Spec
        ↓
样本 QC（PCA/MDS）
        ↓
设计矩阵/contrast（决定 estimand 和 LFC 方向）
        ↓
DEG 模型（edgeR / limma / DESeq2）
        ↓
完整 DE 表（不要先删 NA/非显著行）
        ├── 火山图 / MA / 热图（表达层）
        └── GO / KEGG ORA 或 GSEA（解释层）
              ↓
        ID mapping + tested universe + DB snapshot
              ↓
        表、图、provenance、Claim 和验证评分
```

代码阅读时要沿着这条链追，而不是把每个 `.R`/`.py` 文件当成孤立教程。

## 3. 各节点的真实代码入口

### 3.1 DEG 脚本入口：编排层

[main.R](../skills/reference-stack/02-deg/scripts/main.R) 是 CLI 入口，主要做：

```text
optparse 解析参数
  → get_script_dir / source 函数文件
  → set.seed
  → check_files
  → run_diff_analysis
```

关键调用链：

```text
main.R
└── run_analysis.R::run_diff_analysis
    ├── functions.R::load_data
    │   ├── data.table::fread
    │   └── validate_groups
    ├── functions.R::run_diff_method
    │   ├── diff_limma
    │   ├── diff_deseq2
    │   ├── diff_edger
    │   └── diff_stat（t / Wilcoxon）
    ├── functions.R::filter_results
    └── generate_outputs
        ├── diff_visualization.R::generate_volcano
        └── diff_visualization.R::generate_heatmap
```

这个脚本是很好的“模块边界”教材，但它不是你最终的 PA-LUAD 主实现；它允许多种
方法通过 `switch()` 进入同一个结果接口，必须审计不同方法输出是否真的语义等价。

### 3.2 edgeR：当前项目最值得首先深读的统计包

项目适配器：[bulk-pa-luad/SKILL.md](../../.agents/skills/bulk-pa-luad/SKILL.md)

参考示例：[basic_workflow.R](../../.agents/skills/bulk-pa-luad/references/basic_workflow.R)

核心函数链：

```text
edgeR::DGEList
  → edgeR::filterByExpr
  → edgeR::normLibSizes / calcNormFactors
  → edgeR::estimateDisp
  → edgeR::glmQLFit
  → edgeR::glmQLFTest
  → edgeR::topTags / decideTests
```

每个函数都要按以下问题阅读：

| 函数 | 必须回答的问题 |
|---|---|
| `DGEList` | 输入是否真的是 raw integer counts；样本和基因怎样存储 |
| `filterByExpr` | 什么叫“可检验基因”；过滤依赖设计矩阵还是简单组别 |
| `normLibSizes` / `calcNormFactors` | 归一化校正的是库大小还是组成偏差；edgeR 版本差异是什么 |
| `estimateDisp` | common/trended/tagwise dispersion 如何估计；`robust=TRUE` 是否固定 |
| `glmQLFit` | 负二项均值-方差模型和 QL 过度离散怎样进入拟合 |
| `glmQLFTest` | contrast 对应什么 estimand；返回的统计量和 FDR 怎样解释 |
| `topTags` | 排序列、完整结果表和 tested-gene universe 是否保留 |

PA-LUAD 的配对设计还必须追踪：

```r
design <- model.matrix(~ subject + condition, metadata)
```

`subject` 吸收个体基线差异，`condition` 才是目标效应；不能为了代码短而退回无配对
检验。项目 Skill 已把它写入合同，但当前 `basic_workflow.R` 和 `contrasts.R` 主要是
简单 group 示例，尚未展示完整 subject-paired 的可执行切片，这就是一个需要补测试的边界。

### 3.3 参考 DEG 脚本中的审计点

[diff_methods.R](../skills/reference-stack/02-deg/scripts/diff_methods.R) 逐个实现了四类方法：

- `diff_limma`：`lmFit → contrasts.fit → eBayes → topTable`；
- `diff_deseq2`：`DESeqDataSetFromMatrix → DESeq → results`；
- `diff_edger`：`DGEList → cpm 过滤 → calcNormFactors → estimateDisp → glmFit → glmLRT`；
- `diff_stat`：逐基因 `t.test` 或 `wilcox.test`。

这里有几个不能被“脚本能跑”掩盖的事实：

1. 参考 `diff_edger` 使用 `glmFit + glmLRT`，而项目适配器合同要求现代 edgeR QL 路径
   `glmQLFit + glmQLFTest`；两者不能在报告中写成同一个方法。
2. 参考脚本用 `rowSums(cpm(dgelist) > 1) >= 2`，项目合同要求优先使用 `filterByExpr`；
   过滤后的 tested universe 会不同，no-skill/with-skill 比较必须固定其中一条。
3. `diff_deseq2` 对输入执行 `round(df)`。如果输入不是原始计数，这会把连续表达值伪装成
   count，属于数据尺度错误；Spec 应在入口拒绝而不是自动取整。
4. `diff_limma`、`diff_deseq2`、`diff_edger` 都直接 `na.omit()`；这会丢失 `padj=NA` 的
   诊断原因，和 `de-results` Skill 的要求冲突。
5. `main.R` 默认方法是 `limma`，但 PA-LUAD 项目主合同是 edgeR QL；默认值若不在项目
   入口覆盖，就会让“默认运行”偏离科研目标。
6. 简单脚本的 `design = ~ group` 没有 subject、batch、性别或其他协变量，不能直接作为
   paired PA-LUAD 的 oracle。

这些不是现在要立刻改掉的代码，而是阅读时要记录的“实现—合同差异”。

### 3.4 MDS/PCA：展示和诊断层，不是主要统计推断

参考示例：[embedding_phd.py](../skills/reference-stack/01-mds/examples/embedding_phd.py)

实际调用链是：

```text
scanpy.read_h5ad
  → scanpy.pp.normalize_total
  → scanpy.pp.log1p
  → scanpy.pp.highly_variable_genes
  → scanpy.pp.scale
  → scanpy.tl.pca
  → scanpy.pp.neighbors
  → scanpy.tl.umap / leiden
  → openTSNE.TSNE / phate.PHATE（补充投影）
```

值得读的包函数是 `scanpy` 的预处理和 PCA/邻居图接口，以及 `openTSNE`、`phate` 的
超参数和随机性。这里有一个必须明确的术语问题：这个示例实际做的是 **PCA、UMAP、
t-SNE、PHATE**，没有调用 classical MDS。若你的 Spec 写“MDS”，必须进一步决定是
`edgeR::plotMDS`/`limma::plotMDS` 的样本距离诊断，还是 `sklearn.manifold.MDS`；不能把
这些算法只用一个缩写混过去。

对 bulk RNA-seq，先读 PCA/MDS 的样本 QC；UMAP/t-SNE/PHATE 作为补充展示。二维距离、
点密度和簇间空隙不能直接变成生物学 Claim。

### 3.5 GO：统计富集函数层

项目示例：[go_enrichment_basic.R](../../.agents/skills/pathway-enrichment/references/go_enrichment_basic.R)

核心调用链：

```text
org.Hs.eg.db::keys
  → foreground + tested universe
  → clusterProfiler::enrichGO
  → as.data.frame
  → CSV
```

需要重点理解：

- `gene` 是 foreground，`universe` 是真正进入 DE 检验的 tested genes；二者必须同一 ID 空间；
- `ont='BP'/'MF'/'CC'` 必须显式设置，不能依赖默认值；
- `pAdjustMethod='BH'` 和 `qvalueCutoff` 是不同过滤层；
- `minGSSize`/`maxGSSize` 改变可测试通路集合；
- `readable=TRUE` 只是显示 ID，不改变富集统计本身。

当前 GO 示例为了离线可运行，使用 `head(all_entrez, 3000)` 和 `head(universe_ids, 200)`
造出 universe/foreground。这适合测试函数是否能运行，不适合当作科研真值或 benchmark oracle；
真正的 MVP 必须从执行过的 DE 表派生二者。

### 3.6 KEGG：数据库接口与可重复性层

项目示例：[kegg_enrichment.R](../../.agents/skills/pathway-enrichment/references/kegg_enrichment.R)

核心调用链：

```text
DE table
  → clusterProfiler::bitr（SYMBOL → ENTREZ）
  → enrichKEGG / enrichMKEGG（实时 KEGG REST）
  → gson_KEGG
  → gson::write.gson / read.gson
  → enricher(gson = snapshot)
```

这里最重要的不是画图，而是 join 和版本：

- 人/鼠通常进入 Entrez；细菌保留 locus tag；非模式物种可以走 KO；
- foreground 和 universe 必须走同一套 ID mapping，输出映射损失；
- `enrichKEGG`/`gseKEGG` 的实时查询会随 KEGG 更新漂移；
- `gson_KEGG()` 保存快照，`write.gson()`/`read.gson()` 才能让结果可复核；
- `use_internal_data=TRUE` 不是当前 KEGG 的版本固定方案；
- SPIA/graphite 还要额外理解有向、带符号的 KGML 拓扑，且主要适用于 signaling map。

KEGG 代码是本项目最值得做“数据库 join + 版本 provenance”审计的模块。

### 3.7 Enrichr Python：集成层，不是主统计 oracle

参考实现：[pathway_enricher.py](../skills/reference-stack/04-pathway-enricher/pathway_enricher.py)

核心调用链：

```text
argparse
  → parse_gene_file
  → requests.post(/addList)
  → requests.get(/enrich)
  → 解析 Enrichr 行
  → CSV / JSON / Markdown / PNG
```

最值得读的是 Python 的输入解析、异常处理、输出 schema 和复现包；`requests` 只是外部
API 传输。它没有把 DE tested universe 作为输入，也不拟合 edgeR/DESeq2 模型，因此不能
替代你的主 GO/KEGG Spec。它还会把基因符号发到公共 Enrichr API，必须在 Spec 中记录网络、
隐私和实时数据库依赖。

## 4. 推荐阅读优先级

### 第一优先级：决定科研结果的包

1. `edgeR`：`filterByExpr`、`normLibSizes`、`estimateDisp`、`glmQLFit`、`glmQLFTest`。
2. `limma`：`lmFit`、`contrasts.fit`、`eBayes`，重点看 paired/block 设计。
3. 设计矩阵和 contrast：`model.matrix`、`makeContrasts`、`~ subject + condition`。
4. `clusterProfiler`：`enrichGO`、`gseGO`、`enrichKEGG`、`gseKEGG`、`enrichMKEGG`、
   `enricher`、`simplify`、`pairwise_termsim`。
5. `org.Hs.eg.db`/其他 OrgDb：`keys`、`bitr`、keyType 和一对多映射。
6. `gson`/KEGG REST/SPIA/graphite：快照、实时版本和拓扑边界。

### 第二优先级：支撑可读性和诊断的包

`scanpy`、`sklearn`、`openTSNE`、`phate`、`ggplot2`、`ggrepel`、`pheatmap`。它们重要，
但不应先于 estimand、模型、universe 和数据库版本。

### 第三优先级：外部实现对照

Enrichr Python、报告生成、Markdown/PNG/CSV 格式和 reproducibility helper。它们用于
验证集成能力和失败闭环，不作为主科研结果的唯一依据。

## 5. 每读一个包函数都填这张表

| 字段 | 要回答的问题 |
|---|---|
| Representation | 输入是 raw counts、连续表达、gene list 还是 named ranking |
| Estimand | 这个函数究竟估计哪一个组间/通路效应 |
| Transformation | 在函数前后发生了什么变换、过滤和 ID 映射 |
| Assumptions | 分布、独立性、背景 universe、基因集大小和拓扑假设是什么 |
| API state | 参数默认值、对象 class、返回列和版本差异是什么 |
| Failure | 哪些错误会停止，哪些会静默返回空结果或丢行 |
| Evidence | 输出如何被下游火山图、GO/KEGG、Claim 和评分消费 |
| Provenance | 版本、seed、数据库日期、输入/输出 hash 如何保存 |

这张表就是从“代码阅读”进入“科研 Spec 审计”的桥梁。

## 6. 第一轮结论

当前最合理的学习顺序不是逐行翻译所有代码，而是：

```text
edgeR QL + paired design
  → 完整 DE 表与 tested universe
  → clusterProfiler GO/KEGG（ORA/GSEA 分叉）
  → KEGG ID/快照/SPIA 边界
  → MDS/PCA 与火山图等诊断表达
  → Enrichr 等外部适配器
```

这样读出来的不是“会调用几个包”，而是能解释：输入是什么、模型估计什么、结果为什么
可信、什么时候必须失败、下游如何继承证据，以及 no-skill/with-skill/no-Spec/with-Spec
比较时到底比较了哪一个状态。

