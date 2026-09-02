# MDS → DEG → Volcano → GO / KEGG：实际执行顺序

## 结论

用户可以按 `MDS → DEG → 火山图 → GO → KEGG` 阅读，但正式执行时应写成：

```text
输入合同与原始 QC
    ↓
规范化后的样本关系诊断（MDS/PCA）
    ↓
DEG 模型与 contrast
    ↓
DE 结果诊断与结果表冻结
    ├── 火山图/MA/热图（可视化分支）
    └── GO 与 KEGG（并行的富集分支）
            ↓
      mapping / universe / DB snapshot 审计
            ↓
      跨数据集复现、provenance 与 Claim
```

## 各节点的底层关系

### 0. 输入合同和原始 QC

- 固定样本清单、metadata、物种、基因 ID、参考版本和 contrast。
- 有 FASTQ 时先做 FastQC/MultiQC；只有表达矩阵时至少检查样本数、缺失值、重复 ID、库规模/表达分布和元数据 join。
- 这一层失败，后面的 MDS、DEG 和富集结果都不应进入 release。

### 1. MDS/PCA：先做样本诊断

- counts 先经过适合可视化的变换（如 log-CPM、VST 或 rlog）；芯片数据使用规范化表达值。
- MDS/PCA 用来发现离群样本、样本交换、批次主导和条件/配对关系；不能自动把“看起来远”的样本删掉，删除规则必须预先声明并人工确认。
- MDS 坐标不是 DEG 的输入特征选择器，也不是通路证据。
- 若需要结果图，可以在模型拟合后再画一次；这是同一方法的第二个视图，不是新的统计步骤。

### 2. DEG：唯一的主要统计推断节点

- raw integer counts：edgeR/DESeq2；微阵列或连续表达值：limma；单细胞：按生物学样本做 pseudobulk 后再建模。
- 明确 design、contrast、过滤、归一化、FDR、效应阈值、方向和 tested-gene universe。
- 反向 contrast 必须反向 logFC；配对/阻断因素必须进入 design。
- 先冻结完整 DE 表，再生成下游图和富集输入。

### 3. 火山图：DEG 的可视化，不是下一种统计检验

- 必须使用已经冻结的 DE 表；不能从图反推基因列表。
- x 轴是明确的效应估计（RNA-seq 通常用 shrunken LFC），y 轴明确是 `-log10(p)` 还是 `-log10(padj)`。
- 阈值线、上下调方向、标签和显著基因计数必须来自同一张结果表。
- 验收底层数据和语义，不验收 PNG 像素相似度。

### 4. GO 与 KEGG：同一 DEG 结果的两个并行分支

- 先决定 ORA 还是 GSEA：阈值列表走 ORA，完整 signed ranking 才走 GSEA。
- 两者都要继承同一个已执行 DEG 的方向、ID mapping 和 tested-gene universe；不能自行发明 gene list。
- GO 需要明确 BP/MF/CC；KEGG 需要 organism、keyType、数据库快照/访问日期。
- 人宿主和细菌必须分开建模和注释。细菌通常用 locus tag/KO 和物种代码，不能套用人类 OrgDb。
- GO 结果不必先于 KEGG；正式流程中两者可以并行运行，最后再做比较或合并报告。

## 先看什么、后看什么

人工复核时按下面顺序最省事：

1. `01-mds/SKILL.md`：理解样本关系、变换和 MDS 的解释边界；
2. `02-deg/SKILL.md`：理解输入类型和模型路由；
3. `02-deg-results/SKILL.md`：理解 padj、FDR、方向、universe 和下游交接；
4. `03-de-visualization/SKILL.md`：理解 MDS/PCA、MA、p-value histogram 和热图的诊断位置；
5. `03-volcano/SKILL.md`：理解火山图的效应量、FDR 轴和标签合同；
6. `04-pathway-workflow/SKILL.md`：理解 ORA/GSEA 分叉和 ID 转换；
7. `05-kegg/SKILL.md`：理解 KEGG 的物种代码、细菌 locus tag、universe 和快照。

`04-pathway-enricher/` 是另一个外部实现参考，不是本项目推荐的唯一执行器；它的 Enrichr 结果不能替代本项目的 clusterProfiler/本地快照合同。

## 最容易犯的顺序错误

| 错误 | 为什么错 | 正确处理 |
|---|---|---|
| 先做 DEG，最后才看样本关系 | 可能把批次或离群样本当成生物效应 | 先做无偏 MDS/PCA 和样本距离检查 |
| 用 MDS 结果挑选“最像”的基因 | MDS 是样本关系，不是基因显著性检验 | MDS 只做 QC/结构诊断 |
| 火山图先于 DEG | 火山图没有独立的统计输入 | 先冻结 DE 表，再绘图 |
| GO 做完再把 GO 结果喂给 KEGG | 两者都应从同一 DEG 输入开始 | GO 与 KEGG 并行，分别记录数据库和参数 |
| 把 GO/KEGG 富集当成 DEG 验证 | 富集是同一 gene list 的派生解释 | 独立数据或正交实验才是验证 |
| 把人宿主和细菌基因直接求交集 | ID、基因组和注释体系不同 | 分支建模，在 pathway/ortholog 层预先定义比较规则 |
