# DEG 算法说明（中文审阅版）

英文原件：[references/algorithm.md](../../../reference-stack/02-deg/references/algorithm.md)。

## 方法定位

- **limma**：线性模型 + empirical Bayes 方差收缩，适合微阵列和已归一化/voom 表达；
  设计矩阵和 contrast 决定可解释的效应。
- **DESeq2**：负二项 GLM，适合 raw count；需要 size factor、离散度估计、独立过滤和
  Cook 距离等诊断。
- **edgeR**：负二项模型，常用于 raw count；TMM 等归一化和设计矩阵必须记录。
- **t-test/Wilcoxon**：不建模 RNA-seq count 的均值-方差结构；只能作为探索性或敏感性
  分析，并明确其限制。

## Spec 中要固定的假设

物种和基因 ID、输入是否为 raw counts、过滤规则、归一化、设计矩阵、contrast、协变量、
重复结构、检验统计量、多重检验方法、效应阈值、缺失/离群处理和软件版本。任何一个未
声明的选择都会让 no-skill 与 with-skill 比较失去可比性。

完整公式、R 代码和边界案例仍以英文原件为准。

