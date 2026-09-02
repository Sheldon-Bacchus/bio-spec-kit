# R 与伪代码优先的跨语言代码学习法

## 1. 这套方法的专业叫法

这不是只有一个统一名称的教学流派。对当前项目，最准确的组合表述是：

> **语言无关、算法优先的渐进式精化**
>（language-agnostic, algorithm-first stepwise refinement）
> + **伪代码驱动的跨语言概念迁移**
>（pseudocode-driven cross-language transfer）
> + **契约优先的包级源代码审计**
>（contract-first package-level source audit）。

软件工程中的 `stepwise refinement` 是从高层目标逐步精化成数据、控制流、模块、函数和
可执行代码。你的路线还要从真实包函数反向追踪它如何实现高层算法，因此也是
**双向可追溯的程序理解**。

## 2. 伪代码不是一种统一语言

伪代码没有全球统一语法，而是一组与具体语言无关的算法记号。按保留的信息量，可以分为：

| 形式 | 保留什么 | 生信例子 |
|---|---|---|
| 叙述式伪代码 | 人的意图和动作 | 读取计数，检查样本，删除低表达基因 |
| 结构化伪代码 | `IF/ELSE/FOR/WHILE` 与顺序 | `IF 样本不匹配 THEN 停止` |
| 数据流伪代码 | 对象经过哪些节点 | `counts → filter → normalize → fit → test` |
| 契约式伪代码 | 前置、后置、不变量、失败条件 | `REQUIRE raw integer counts` |
| 统计伪代码 | estimand、模型、零假设、统计量 | `fit NB-QL model; test condition contrast` |
| 领域伪代码 | 领域固定动作词 | `map IDs → define universe → run ORA/GSEA` |

流程图、形式规格（例如 TLA+）和可执行 DSL 可以辅助伪代码，但不是同一个东西：
伪代码描述“想怎样算”，Spec/契约描述“允许什么行为以及必须满足什么条件”，代码才是
真正执行的实现。

## 3. “删除符号”可以做，但不能删除语义骨架

第一遍可以暂时抹掉括号、逗号、赋值箭头和包前缀，只保留动作和对象。但以下信息不能删除：

1. **数据表示**：向量、矩阵、表、列表、因子和缺失值；
2. **形状**：行数、列数、行名和列名；
3. **数据尺度**：raw counts、log/VST、TPM/FPKM、gene list 或 ranking；
4. **绑定关系**：哪个名字保存哪个对象；
5. **顺序**：过滤先于模型拟合，ID mapping 先于富集；
6. **分支和循环**：何时停止、跳过或重复处理；
7. **函数契约**：输入、输出、副作用和错误；
8. **统计语义**：估计对象、零假设、universe、FDR 和方向；
9. **外部效果**：文件、网络、随机数、数据库版本和缓存。

应删除的是**表面语法噪声**，保留的是**语义不变量**。

## 4. 所有语言的共同核心和差异

几乎所有语言都能抽象成：数据、名字与绑定、表达式求值、顺序、条件、重复、函数/模块、
输入输出、错误和状态。但“必须先声明所有东西”不是所有语言的共同规则。

| 范式 | 代表语言 | 声明和控制流特点 |
|---|---|---|
| 过程式/命令式 | C、Python、R script | 逐步改变状态；C 类型显式，R/Python 多为动态绑定 |
| 静态类型编译式 | C、C++、Rust、Go、Java | 类型、接口和编译期检查重要 |
| 动态/解释式 | Python、R、JavaScript | 名字在运行时绑定；导入模块不等于声明每个函数类型 |
| 函数式 | Haskell、Lisp、部分 Python/R | 函数组合、递归和不可变数据突出 |
| 声明式/集合式 | SQL | 描述结果集合，不逐项写执行循环 |
| 数据流/工作流 | Shell、Nextflow、Snakemake | 节点和数据依赖比变量顺序更重要 |
| 逻辑式 | Prolog | 写事实、规则和查询，而不是传统循环 |

因此应学习共同的“数据—变换—控制—接口—错误—证据”，再学习某种语言如何表达它。

## 5. R 的最小语法骨架

第一阶段只学这些，不先学完整 R 生态：

```r
# 注释
x <- 3                         # 赋值：名字 x 绑定到对象 3
v <- c(1, 2, 3)                # 向量
lst <- list(a = 1, b = "x")    # 可放不同类型对象的列表
df <- data.frame(id = v, g = c("A", "B", "A"))
m <- matrix(1:6, nrow = 2)     # 矩阵；R 的索引从 1 开始

f(x, arg = value)              # 函数调用；命名参数用 name = value
pkg::fun(x)                     # 显式调用某个包的函数
x[1]                            # 向量/列表取元素
m[1, 2]                         # 矩阵取行列
df$g                            # 表中取列
df[["g"]]                       # 按名字取出列对象

if (condition) { ... } else { ... }
for (i in seq_along(v)) { ... }
while (condition) { ... }

f <- function(arg) {            # 定义函数
  result <- arg + 1
  result                         # 最后一行是返回值
}

library(edgeR)                   # 加载包，不是声明所有函数类型
```

尽早认识 `TRUE/FALSE`、`NULL`、`NA`、`factor`、`names`、`class`、`str`、`dim` 和
`length`。它们比记住某个科研包的函数名更基础。

### `fit` 和 `name` 不是魔法关键词

```r
fit <- glmQLFit(y, design)
res <- results(dds, name = "condition_treated_vs_control")
```

- `fit` 通常只是变量名，表示把拟合模型对象保存到这个名字；换成 `model1` 也可以。
- `name` 是 `results()` 的参数名，字符串用于选择某个系数；它不是神奇的编程关键词。
- 阅读时先检查 `class(fit)`、`str(fit)`、`names(fit)`，再研究包如何解释对象。

## 6. 同一段科研逻辑的四种表示

### 人话

读取 raw counts 和样本信息，检查样本匹配；去掉低表达基因；按实验设计建模；估计离散度；
测试处理组相对对照组的差异；保存完整结果和诊断。

### 结构化伪代码

```text
INPUT counts, metadata, subject, condition
REQUIRE counts are non-negative integers
REQUIRE sample IDs in counts equal sample IDs in metadata
REQUIRE every subject has required condition levels
CREATE count-model object
FILTER genes by expression rule
NORMALIZE library/composition factors
BUILD design subject + condition
ESTIMATE dispersion
FIT negative-binomial quasi-likelihood model
TEST the declared condition contrast
EXPORT complete DE table, tested universe, diagnostics and provenance
IF any contract check fails THEN stop with a machine-readable error
```

### R 表达

```r
library(edgeR)
y <- DGEList(counts = counts)
keep <- filterByExpr(y, design = design)
y <- y[keep, , keep.lib.sizes = FALSE]
y <- normLibSizes(y)
y <- estimateDisp(y, design, robust = TRUE)
fit <- glmQLFit(y, design, robust = TRUE)
test <- glmQLFTest(fit, contrast = contrast)
res <- topTags(test, n = Inf)$table
```

### 包语义

```text
DGEList       组织计数与样本信息
filterByExpr  定义哪些基因有资格进入检验
normLibSizes  校正库大小/组成偏差
estimateDisp  估计负二项离散度
glmQLFit      拟合带准似然的计数模型
glmQLFTest    对声明的 contrast 做检验
topTags       导出统计量、p 值和 FDR
```

四层必须一一对应；如果 R 代码和伪代码顺序不一致，先检查实现是否错误，不要强行背诵。

## 7. 本项目的代码阅读顺序

### 阶段 A：R 核心语法

只覆盖赋值、对象、向量/矩阵/表/列表、索引、函数、条件、循环、包和错误。每个概念
用一个 5–20 行的小例子验证，不进入 DE 分析。

### 阶段 B：科研数据表示

先理解 `counts`、`metadata`、`design`、`contrast`、`DGEList` 和 `DESeqDataSet` 的
形状、class、行列名和生命周期，重点看对象状态怎样改变。

### 阶段 C：单包、单方法

先只读 edgeR QL：

```text
DGEList
→ filterByExpr
→ normLibSizes
→ estimateDisp
→ glmQLFit
→ glmQLFTest
→ topTags
```

随后读配对设计和 contrast，再读 limma/DESeq2 的对应实现。

### 阶段 D：小脚本

阅读 `main.R → run_analysis.R → functions.R → diff_methods.R` 的控制流，明确哪些代码
是编排层，哪些代码真正调用统计包，哪些代码只负责写文件和画图。

### 阶段 E：下游包

```text
完整 DE 表
→ clusterProfiler::enrichGO / gseGO
→ clusterProfiler::enrichKEGG / gseKEGG
→ OrgDb::bitr / keys
→ gson 快照 / SPIA / graphite
```

先理解 `gene`、`universe`、ranking 和 ID mapping，再看 dotplot 或报告格式。

### 阶段 F：Spec 和测试

最后把伪代码中的 `REQUIRE/ENSURE/IF FAIL` 变成 Spec、验证器和测试。Spec 不是用来替代
R 基础，而是把已经理解的语义固定成可执行合同。

## 8. 每个函数的固定阅读模板

| 问题 | 要记录的内容 |
|---|---|
| 输入 | 类型、形状、单位、行列名、允许缺失值 |
| 绑定 | 函数返回什么对象，赋给哪个名字 |
| 变换 | 发生了什么过滤、归一化、映射或排序 |
| 算法 | 数学模型、estimand、零假设、统计量 |
| 默认值 | 哪些参数如果不写会改变结果 |
| 输出 | class、列名、维度、下游消费者 |
| 失败 | error、warning、空结果还是静默删行 |
| 外部效果 | 文件、网络、随机数、数据库版本 |
| 测试 | 能验证哪个不变量，negative case 是什么 |

## 9. 需要改进的地方

1. **不要同时深学多种语言的完整语法**：先用同一套伪代码，再分别学习每种语言表达这
   套语义所需的最小语法。
2. **不要把函数名当知识单位**：知识单位应是“对象状态变化 + 方法假设 + 输出证据”。
3. **不要抹掉类型和形状**：跨语言抽象不是把所有东西说成“处理数据”；`matrix`、
   `data.frame`、`factor` 和 `DGEList` 的差别直接影响科研结果。
4. **不要把包 API 当算法本身**：先写统计伪代码和 estimand，再看包如何实现；否则会把
   默认参数误当成科学定律。
5. **加入反例驱动学习**：非整数 counts、样本错配、缺少 universe、错误 ID、空结果、
   设计矩阵奇异都要有小例子。
6. **把每个学习单元做成微型垂直切片**：一个输入、一个核心函数、一个输出、一个断言、
   一个失败样例；不要一开始跑整条大流程。

## 10. 当前第一学习单元

下一轮先不讲 GO/KEGG，也不讲复杂画图，只完成：

```text
R 基础对象和函数调用
→ 读取 counts / metadata
→ 检查类型、维度、ID 和配对
→ 写出 subject + condition 设计
→ 逐个理解 edgeR QL 函数
→ 导出一个完整 DE 表
```

完成这个单元后，再把同一套伪代码分别映射到 limma、DESeq2、Python/pandas 和 workflow
语言。这样学到的是可迁移的编程和科研计算结构，而不是一组孤立的英语函数名。
