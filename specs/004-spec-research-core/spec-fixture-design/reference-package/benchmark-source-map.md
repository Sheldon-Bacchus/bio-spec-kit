# Benchmark source map

更新时间：2026-08-31

本文件只记录“可以借鉴什么”和“不能直接拿来当什么”，不复制外部 Bench 的 hidden oracle。

## 1. SkillsBench：评测协议来源，不是生物数据来源

来源：

- https://www.skillsbench.ai/
- https://github.com/benchflow-ai/skillsbench
- https://raw.githubusercontent.com/benchflow-ai/skillsbench/main/registry.json

当前仓库的 v1.1 任务注册表是通用任务集合。已检查注册表，没有 `bio`、`rna`、`MDS`、`volcano` 或 `KEGG` 任务名/领域。

可借鉴：

- no-skill / curated-skill / self-generated-skill 的配对实验；
- 固定输入、oracle 和 deterministic verifier；
- `task.md + environment + oracle + verifier` 的任务封装；
- 先运行 oracle，再运行 Agent；
- 将 Skill lift、模型能力和 Agent 行为分开报告。

不直接借鉴：

- 不把 SkillsBench 的通用任务当成 bio benchmark；
- 不把它的 resolution rate 直接当作科研正确率；
- 不让外部 Skill 污染本项目的 Agent 对照条件。

## 2. BixBench：KEGG/DE 子任务来源

来源：

- https://github.com/FUture-House/BixBench
- https://huggingface.co/datasets/futurehouse/BixBench

当前数据集页面显示 205 个问题，来自真实发表的计算生物学 notebook/capsule。适合作为生物分析和多步骤推理的候选来源。

优先记录的候选任务：

- `bix-26-q3`：DESeq2 后，按绝对 log2 fold change 和 adjusted p-value 筛选，再计算 KEGG `ABC transporters` 中的贡献基因数；
- `bix-26-q4`：比较两个培养条件中显著下调基因的 KEGG 富集通路交集；
- `bix-26-q5`：找出只在铁缺乏条件显著富集、另一条件不显著的 KEGG 通路；
- `bix-32-q4`：比较三个 quorum-sensing mutant 中共同富集的 KEGG 通路。

这些任务能覆盖：阈值解析、DE → pathway enrichment、跨条件/跨菌株交集和方向一致性。

限制：BixBench 原生问题以开放答案或选择题为主，部分问题采用 LLM verifier 或字符串/范围 verifier；它不是 MDS、火山图、KEGG 三联图的完整 artifact benchmark。因此这里只作为 KEGG/DE 子任务候选，不直接作为本项目的最终 oracle。

## 3. BioAgent-Bench：可复现流程形状来源

来源：

- https://github.com/bioagent-bench/bioagent-bench
- https://github.com/bioagent-bench/bioagent-bench/tree/master/tasks/deseq
- https://github.com/bioagent-bench/bioagent-bench/tree/master/tasks/alzheimer-mouse

可借鉴：

- task 目录、Docker 环境、运行脚本和 reference/results 的组织方式；
- `deseq` 任务中的 QC、mapping、DESeq2 和结果文件链；
- `alzheimer-mouse` 任务中的多模型 DE 与 KEGG 通路比较思路。

限制：当前 `deseq` 任务的脚本最终输出上调基因表，并不提供 MDS、火山图、KEGG 三者的统一验收合同；项目 README 也提醒 truth/eval 不应默认视为绝对正确。因此不能原样作为本项目 hidden oracle。

## 4. UCDavis visualization workshop：三联案例构造来源

来源：

- https://ucdavis-bioinformatics-training.github.io/2025-August-Intermediate-Visualization-for-Bioinformatics/R/02-scatterplot

该教学案例明确使用四类数据：expression data、annotations、MDS coordinates 和 KEGG enrichment data，并包含火山图相关可视化内容。

用途：作为本项目第一个小型 execution fixture 的数据关系参考：

```text
expression/counts + sample annotations
        ├── MDS coordinates
        ├── differential-expression table → volcano plot
        └── gene identifiers → KEGG enrichment table/plot
```

限制：它是教学材料，不是 Agent benchmark；需要在本项目中重新冻结输入、参数、oracle、negative cases 和 verifier。

## 5. ggplotAgent：火山图视觉合同来源

来源：

- https://github.com/charlin90/ggplotAgent
- https://academic.oup.com/bioinformaticsadvances/article/6/1/vbaf332/8416062

仓库提供 `examples/volcano_example.csv` 和明确的火山图任务描述，包括 log2 fold change、-log10 FDR、上下调阈值、颜色和参考线；论文说明其 benchmark 包含 20 个可执行可视化任务。

用途：只借鉴火山图的输入字段和可验证视觉/语义要求，不把图像相似度当作科研 Claim 正确性。

## 当前选择结论

| 目标 | 首选来源 | 在本项目中的角色 |
|---|---|---|
| Skill 对照方法 | SkillsBench | 实验设计和任务封装参考 |
| KEGG/DE 真实问题 | BixBench | execution 子任务候选 |
| Bio workflow 目录形状 | BioAgent-Bench | 环境与流程参考 |
| MDS + expression + KEGG 数据关系 | UCDavis workshop | 本地 fixture 构造参考 |
| 火山图字段与视觉约束 | ggplotAgent | volcano artifact 合同参考 |

当前没有发现一个外部 Bench 同时提供 MDS、火山图、KEGG 三项的、带 hidden oracle 和 deterministic artifact verifier 的完整任务。因此本项目的首个三联案例必须自建，不能声称“直接复用了现成 BioBench 测试机”。

