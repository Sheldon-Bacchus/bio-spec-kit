# 降维图使用指南（中文审阅版）

英文原件：[reference-stack/01-mds/usage-guide.md](../../reference-stack/01-mds/usage-guide.md)。

## 适用场景

- bulk 样本 QC：VST/log 后 PCA，显示 condition、batch、性别和方差解释率。
- 单细胞概览：PCA 后再 UMAP/t-SNE；明确邻居数、初始化和随机种子。
- 连续轨迹：PHATE 或扩散图，不能只凭 UMAP 空间的空隙宣称轨迹。
- 多组学：先说明联合表示（例如 MOFA 因子），再对联合空间降维。

## 最小提示模板

```text
请对已经明确变换方式的表达矩阵做样本层 PCA/MDS QC。报告输入、距离或变换、批次和
condition 标注、方差解释率、离群判断、软件版本与随机种子；不要把二维距离直接解释为
生物学距离，并输出可重算的坐标和参数。
```

需要运行命令、绘图代码和完整示例时，打开上面的英文原件；中文文件只做审阅和 Spec 绑定。

