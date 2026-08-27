# 00 MVP 决策：先做 Evidence Closure Kernel

> 状态：讨论汇总与第一刀决策稿。
>
> 范围：只定义并实现一个隔离的 MVP，不修改上游 `spec-kit`、当前正式 Bio preset 或 `.agents` 运行时发现目录。

## 一、当前问题的核心判断

现在有两个容易混淆的层：

```text
Research Spec Kit = 通用科研母框架
Bio Spec Kit      = Research Spec Kit 的生物/生信 profile
```

更完整的分层应是：

```text
Research Spec Kit
  ├── 科研问题、证据、验证、claim、状态、gate、provenance
  └── 跨领域科研不变量

Bio Spec Kit profile
  ├── 样本、参考、批次、复制、QC、组学输入输出
  └── 生信方法的领域适用条件

Skills / Extensions
  ├── MultiQC、bulk RNA-seq、Scanpy、WGCNA、GSEA 等具体能力
  └── 确定性脚本、wrapper、workflow 和结果 artifact

Project / Feature Spec
  └── 某个具体课题或科学问题的实例
```

当前仓库已经有 Bio profile、Skill、extension、workflow 和 feature spec 的雏形，但通用 Research 层还没有独立的可运行内核。因此，如果现在直接改整个 Bio preset，会把治理规则、领域约束、工具方法和项目需求再次混在一起。

## 二、五个方向的共同底层

五个方向最终都要回答同一个问题：某个受约束的科学主张是否被指定的证据支持。

```text
Question
  → Observable
  → Validation
  → Claim
       ↓
    Provenance
       ↓
    State / Gate
```

共性对象：

| 对象 | MVP 职责 |
|---|---|
| Question | 定义问题、范围、比较和目标估计量 |
| Evidence | 记录来源或已产生的可引用证据 |
| Observable | 从输入中可计算、读取或核验的量 |
| Validation | 对 observable/claim 执行确定性检查 |
| Claim | 按规则生成的受限结论 |
| Run | 记录一次执行实例 |
| Provenance | 记录输入、参数、版本、输出和 hash |
| Gate / State | 决定是否能继续或升级 claim |

不放入共性内核的内容：FASTQ/H5AD、DESeq2/Scanpy、AutoRA、WGCNA、OSF、Nextflow、特定统计模型和复杂文献数据库。这些是 profile、adapter 或后续能力。

## 三、MVP 的准确定位

MVP 不是一个“完成科研”的系统，也不证明生物学真理。它只证明：

> 一个预先声明的 Question，能否由明确的 Observable、Validation、Decision Rule 和 Provenance 生成一个不会越界的 Claim 状态。

因此 MVP 命名为：

```text
Evidence Closure Kernel
```

第一版必须保持：

- 本地运行；
- 无外部网络依赖；
- 确定性；
- 输入和输出可 hash；
- 规则显式；
- 失败、阴性、不确定和探索性结果可区分；
- 不由 Agent 自由升级结论。

## 四、第一刀具体改什么

只在以下隔离范围新增：

```text
bio-spec-kit/spec-mvp/research-evidence-kernel/
```

建议结构：

```text
research-evidence-kernel/
├── README.md
├── kernel.py
├── schemas/
│   └── minimal-contract.md
├── fixtures/
│   ├── q1_supported/
│   ├── q1_not_supported/
│   ├── q1_inconclusive/
│   └── q1_invalid_provenance/
├── examples/
│   └── q1-minimal/
├── tests/
│   └── test_kernel.py
└── run_demo.py
```

第一版不建立数据库、不做 UI、不接 MCP、不做动态 Skill router，也不把已有五个方向强行串成一个大流程。

## 五、Q1 Demo

示例问题：

```text
在预先定义的 PA 与 LUAD 队列中，是否存在方向一致且超过预设效应阈值的共同转录响应？
```

Demo 使用固定的本地 effect vector，不下载真实数据：

```text
PA:   G1=2.0, G2=1.5, G3=-1.2, G4=0.4, G5=-2.0, G6=1.1
LUAD: G1=1.8, G2=1.2, G3=-1.5, G4=-0.8, G5=1.4, G7=2.2
```

固定规则：

```text
响应基因：abs(log2FC) >= 1.0
共同响应：两个向量都有该基因且都达到阈值
方向一致：sign(PA) == sign(LUAD)
minimum_overlap = 3
minimum_concordance = 0.8
independent_validation = required
```

交集为 G1、G2、G3、G5；其中 G5 方向冲突，一致性为 3/4 = 0.75。因此第一个 fixture 的结果应为 `not_supported`。把 LUAD 的 G5 改为 -1.4 后主分析通过，但若没有独立验证，claim 仍为 `inconclusive`，不能自动成为 `supported`。

## 六、MVP 状态与 gate

```text
DRAFT
  → READY_FOR_EXECUTION
  → RUNNING
  → RESULTS_UNVERIFIED
  → READY_FOR_REVIEW
  → RELEASED
```

异常状态：

```text
NEEDS_CLARIFICATION
FAILED_RETRYABLE
FAILED_TERMINAL
NOT_EVALUABLE
INCONCLUSIVE
EXPLORATORY_ONLY
ESCALATED
```

最低 gate：

1. Input Gate：Question、假设、范围、输入字段完整；
2. Design Gate：阈值、方向定义、背景集合和验证规则固定；
3. Execution Gate：Run 成功，输出存在，输入/输出 hash 可追溯；
4. Validation Gate：Observable 和验证结果满足 schema；
5. Claim Gate：状态只能按 Decision Rule 计算；
6. Release Gate：provenance 完整，并预留人工复核状态。

MVP 可以让本地 demo 输出 `release_candidate`，但没有人工批准时不能标为最终 `RELEASED`。

## 七、Research / Bio 的演进顺序

### 第一步：通用 Research Kernel

先做 Question、Evidence、Observable、Validation、Claim、Run、Provenance、Gate 的最小合同。

### 第二步：极薄 Bio profile

把现有 MultiQC vertical slice 作为第一个 Bio adapter：

```text
sample manifest
  → QC observable
  → provenance
  → validation verdict
```

### 第三步：具体 Skills

再按 allowlist 接入 bulk RNA-seq、pathway enrichment、WGCNA、single-cell、spatial 和其他领域能力。每个 Skill 只产生自己的 Observable/Run/Evidence，不重建全局状态机。

## 八、五个方向如何逐步体现

| 方向 | 在 MVP 中先体现什么 | 后续扩展 |
|---|---|---|
| Research Constitution | 不捏造、clarification、状态、gate、claim 限制 | 证据等级、人工审批、waiver、撤回 |
| Research Specification | Question、范围、estimand、decision rule | facts、unknowns、gaps、假设、预注册 |
| Research Design | 设计字段和 claim scope 的最小接口 | 实验设计、power、混杂、重复、统计模型 |
| Open Science | run、输入/输出 hash、参数、版本 | OSF、lockfile、容器、快照、报告 provenance |
| Spec Kit/Bio Profile | 隔离目录、profile 边界、状态迁移 | 候选 preset、命令、skill adapter、converge |

## 九、Smoke / E2E 验收标准

必须反复通过：

- happy path：生成完整 observable、validation、claim 和 provenance；
- 输入缺失：进入 `NEEDS_CLARIFICATION`，不输出正式结论；
- 方向冲突/阈值失败：产生 `not_supported`，不是异常崩溃；
- 主分析有信号但无独立验证：产生 `inconclusive` 或 `exploratory_only`；
- provenance/hash 不一致：`NOT_EVALUABLE`，阻断 release；
- 同一 fixture 重跑：规范化结果一致；
- 修改输入：input hash、observable 和 claim decision 按规则变化；
- 失败场景：失败 verdict 本身也持久化，不被伪装为成功。

测试比较规范化字段，不比较时间戳、临时路径和完整 HTML：

```text
status
claim_status
release_ready
error_code
input/output hashes
parsed observables
provenance completeness
interpretation mode
```

## 十、明确暂缓

- 不修改上游 `spec-kit`；
- 不修改正式 `presets/bioinformatics`；
- 不新增或改写 `.agents/skills`；
- 不接真实外部数据、OSF、PubMed、MCP；
- 不做完整 AutoRA、复杂 power、动态 router、多 agent runtime；
- 不强制串联 DE、GSEA、WGCNA、MultiQC；
- 不自动控制真实实验设备或执行外部写操作；
- 不把 `validation passed` 直接等同于 `claim supported`。

## 十一、决策

现在先做第一个 MVP 是正确的，而且最小正确对象不是“完整 Research Constitution”也不是“完整 Bio Spec Kit”，而是：

```text
一个通用 Evidence Closure Kernel
+ 一个极薄的 Bio/MultiQC vertical slice
+ 一组能反复通过的 Smoke/E2E 测试
```

完成这一层后，再逐步把五个方向的详细内容接入；每次扩展都必须证明没有破坏既有证据闭环。

