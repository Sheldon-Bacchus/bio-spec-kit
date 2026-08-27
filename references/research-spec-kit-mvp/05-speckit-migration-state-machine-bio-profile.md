# 05 Spec Kit 机制迁移、状态机与 Bio Profile

> 用途：定义通用 Research Spec Kit、Bio Spec Kit 与具体 Skills 的分层，以及 Spec Kit 机制如何迁移。当前仅作为设计输入，不接入任何运行链路。

## 结论

现在确实容易把 Research Spec Kit 和 Bio Spec Kit 混在一起。建议明确成三层：

```text
Research Spec Kit = 通用科研母框架
Bio Spec Kit      = Research Spec Kit 的生物/生信 profile
Skills            = 某阶段内部真正执行 reasoning 或方法的能力模块
```

核心不是给 Spec Kit 加几个科研 Skill，而是把“意图 → 规格 → 设计 → 任务 → 执行 → 验证”的结构控制机制重新定义为：

```text
科研问题
  → 证据状态
  → 假设
  → 研究设计
  → 领域方法
  → 执行
  → 证据验证
  → 科学主张
  → 可复现记录
```

## 一、状态机

```text
Research Constitution
        ↓
Research Specification
        ↓
Evidence / Literature
        ↓
Research Design
        ↓
Domain Plan
        ↓
Research Tasks
        ↓
Execution
        ↓
Evidence Validation
        ↓
Scientific Claim
        ↓
Reproducibility / Communication
```

每个阶段都要有输入、输出、状态和 gate。下游不能悄悄跳过上游决策，也不能由领域 Skill 自行补齐关键科研假设。

## 二、Spec Kit 机制迁移

| 原 Spec Kit 机制 | Research 语义 | MVP 是否保留 |
|---|---|---|
| Constitution | 跨项目科研不变量、责任和发布规则 | 保留 |
| specify | 写清问题、事实、未知、gap、目标、假设、范围和判定 | 保留，改语义 |
| plan | 研究设计、estimand、方法候选、统计、验证和 provenance 计划 | 保留，改语义 |
| tasks | 按证据闭环拆解可执行任务 | 保留，改语义 |
| analyze | 跨 artifact 检查一致性、证据覆盖和风险 | 保留，改语义 |
| implement | 执行脚本、workflow、实验或外部工具 | 有条件保留 |
| converge | 对照 spec/plan/tasks 检查遗漏并追加任务 | 保留 |
| User Story | Scientific Question 的完整证据闭环 | 不机械保留 |
| Independent Test | Independent Validation / Evidence Gate | 改名改语义 |
| MVP first | 第一个能回答真实问题的最小证据闭环 | 保留底层思想 |

`implement` 不应默认等同于“自动做真实实验”；涉及真实样本、仪器、外部写入或危险操作时必须有人类批准和权限边界。

## 三、Research Spec Kit 通用层

通用层定义：

- question、hypothesis、estimand 和 scope；
- facts、unknowns、gaps、assumptions 和 clarifications；
- evidence、observable、validation、claim 的 ID 与关系；
- exploratory/confirmatory 区分；
- gate、状态、失败、waiver 和人工审批；
- run、artifact、hash、provenance 和 release；
- 不同 profile 的扩展和冲突优先级。

通用层不定义 FASTQ、DESeq2、显微镜参数、动物实验操作或某个模型包的默认值。

## 四、Bio Spec Kit profile

Bio Profile 负责把通用合同落到生物/生信场景：

- 样本 manifest、subject、condition、batch、replicate；
- FASTQ/BAM/CRAM/VCF/H5AD 等输入输出 schema；
- reference genome、annotation、gene ID namespace 和版本；
- QC 指标、阈值和失败动作；
- bulk RNA-seq、single-cell、spatial、variant、pathway 等方法；
- Nextflow、Scanpy、PyDESeq2、GSEA 等领域 Skill 路由；
- 生信特有的独立队列、细胞组成、n<<p、批次和伪重复规则。

Bio Profile 可以增加约束、增加字段、收紧 gate，但不能降低 Research Constitution 对证据、provenance、负结果和人工责任的要求。

## 五、Skills 的位置

Skill 不是上游研究设计器，而是某一阶段的可调用能力：

```text
Evidence stage       → paper-lookup / database-lookup
Design stage         → experimental-design / statistical-power
Domain Plan/Execute  → bulk-rnaseq / scanpy / scvi-tools / nextflow
Analysis/Validation  → pydeseq2 / statistical-analysis / pathway-enrichment
Communication        → scientific-writing / scientific-visualization
```

技能触发由上游 artifact 和 gate 决定。缺少 `Research Design Contract` 时，领域 Skill 应返回“研究设计不完整”，而不是自行选择主要终点、样本单位、统计模型或结论边界。

## 六、五类共性 artifact

不论是 wet-lab、bioinformatics、imaging 还是 ML，最小共性对象都是：

```text
ResearchQuestion
Evidence
Observable
Validation
Claim
Run / Provenance
Gate / State
```

这就是五个方向的共同底层。Constitution、设计、文献、统计和复现最终都要能引用这些对象，而不是各自建立一套互相无法连接的记录。

## 七、课题拆分与 spec-of-specs

一个完整课题不能当作一个 feature。建议分层：

```text
Project Spec
├── Q1：一个最小可回答的科学问题
├── Q2：新的机制或关联问题
├── Q3：新的空间/单细胞问题
├── Q4：新的实验验证问题
└── Communication：整合与发布
```

每个 Q 都有自己的 `spec → plan → tasks → execution → validation → claim` 生命周期；上层 project spec 只管理它们的关系、依赖和总体研究范围。Q1 的结果不能自动成为 Q2 的事实，只能作为带 evidence ID 的输入。

## 八、MVP 建议：先做 Evidence Closure Kernel

最小产品不建议一开始实现完整 Constitution、AutoRA、OSF、所有 profile 或全部命令。建议先实现一个可运行的 `Evidence Closure Kernel`：

```text
Question
  → Observable
  → Validation
  → Claim
  → Provenance
```

MVP 必须能：

1. 读取一份结构化研究问题；
2. 读取或生成 observable；
3. 运行一个确定性 validation；
4. 按 decision rule 生成 claim status；
5. 输出完整 ID 引用链和最小 provenance；
6. 在缺字段、失败或不确定时阻塞或降级，而不是编造结论；
7. 对一个真实 Q1 例子跑通 smoke test。

推荐最小文件：

```text
research-spec.yaml
observables.yaml
validations.yaml
claims.yaml
run-manifest.json
provenance.json
validation-verdict.json
```

## 九、第一刀的最小改造顺序

### 第 1 步：不动上游 Spec Kit

只在 Bio Spec Kit 的隔离范围内新增 Research MVP 参考和实验目录。上游模板、核心命令和既有 Bio baseline 先不改。

### 第 2 步：建立共性 schema

先定义 Question、Observable、Validation、Claim、Run、Gate 六类最小结构，暂不实现全部治理细节。

### 第 3 步：做一个确定性 Demo

用静态 fixture 模拟 Q1：PA 与 LUAD 两个效应向量 → 方向一致性和重叠指标 → 预设规则 → claim 状态。Demo 不需要真实下载数据，也不需要自动调用外部工具。

### 第 4 步：加失败分支

至少测试：缺少 question、缺少 observable、validation 失败、证据不足、provenance 不一致、探索性信号不能升级为 supported。

### 第 5 步：再接 Bio Profile

把 count matrix、sample manifest、QC、DEG、batch 和 reference 等 Bio-specific 约束接入同一共性 contract。这样生信是 profile，而不是把整个 Research Spec Kit 变成生信专用。

## 十、共性状态与 gate

```text
DRAFT
  → READY_FOR_DESIGN
  → READY_FOR_EXECUTION
  → RUNNING
  → RESULTS_UNVERIFIED
  → READY_FOR_REVIEW
  → RELEASED
```

任意关键输入不明时进入 `NEEDS_CLARIFICATION`；冲突进入 `ESCALATED`；运行失败进入 `FAILED_RETRYABLE` 或 `FAILED_TERMINAL`；验证不足时 claim 只能是 `INCONCLUSIVE` 或 `EXPLORATORY_ONLY`。

## 十一、MVP 不做什么

- 不做完整 OSF 自动注册；
- 不做全量文献数据库；
- 不做自动控制真实实验设备；
- 不做复杂多 agent 自我调度；
- 不把所有生信 Skill 一次性接入；
- 不把 `implement` 变成无人工批准的外部写操作；
- 不修改上游 Spec Kit 基线来“证明”架构成立。

