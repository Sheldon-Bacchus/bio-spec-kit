# BixBench `bix-26-q3` 下载记录

## 来源

- 数据集：[futurehouse/BixBench](https://huggingface.co/datasets/futurehouse/BixBench)
- 版本：`main`，数据行的 `version` 为 `1.5`
- Question ID：`bix-26-q3`
- Capsule：`CapsuleFolder-0923d260-fe1b-4fb4-4398-79edf546e584.zip`
- Capsule SHA-256：`2885c81abf0cc4b9b5d5dede6d38db8a51d3aca3dc999d321675434a73773b21`

## 题目摘要

FeMinus（无铁葡萄糖）条件下，筛选显著上调基因并进行 KEGG 富集，问题询问 `ABC transporters` 通路中贡献了多少个基因。下载的 JSONL 记录中的 `ideal` 为 `11`，`eval_mode` 为 `str_verifier`。

这个答案只属于外部数据集记录，不能直接作为本项目 Agent 可见的 hidden oracle。若把该问题转成本项目 fixture，必须由 capsule 中的输入和分析过程独立重算，并把重算结果放在独立的 `hidden-oracle/` 中。

## Capsule 内容

```text
CapsuleFolder-0923d260-fe1b-4fb4-4398-79edf546e584.zip
├── CapsuleData-.../
│   ├── res_GluFevsGluFePlus.rds
│   └── res_SuccvsGluFePlus.rds
└── CapsuleNotebook-.../
    └── *_executed.ipynb
```

已额外把 executed notebook 平铺复制为 `notebook-executed.ipynb`，只是为绕过 Windows 长路径限制；原始 capsule 仍以 zip 文件为准。

## 重要复核点

notebook 的筛选代码对上调集合使用 `log2FoldChange > 1.5`，并在 `enrichKEGG` 中使用 `organism = "pau"`、`pvalueCutoff = 0.05`、`qvalueCutoff = 0.05`。题目文字还提到 adjusted p-value threshold `0.05`，但 notebook 的上调基因筛选段没有显式 `filter(padj < 0.05)`；这构成一个必须记录的输入/实现不一致，不能在本项目中默默替换。

因此它适合作为：

- KEGG/DE 语义与边界的外部参考；
- 一个“题目文字和执行 notebook 是否一致”的 negative case；
- 后续构造 `KEGG-001` 的候选来源。

它不是 MDS＋火山图＋KEGG 三联 fixture，也不是本项目最终的 deterministic oracle。

