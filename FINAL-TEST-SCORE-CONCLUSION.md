# Bio-Spec Kit：当前测试、评分与最终结论

**审计日期：** 2026-08-31  
**审计依据：** 后续分支线程 `01a04687-dd2c-7983-aece-cd377500801a` 与当前工作区实际文件、命令输出和真实 fixture 重跑。  
**本文件目的：** 只记录当前测试、评分、阻塞和最终结论；不把设计方案、历史结果或外部 benchmark 说明冒充为已通过的执行结果。

## 最终结论

当前项目可以开始自己的 Bio-Spec MVP，但还不能称为“完全自驾科研系统”。准确状态是：

> **局部技术执行闭环已经通过；Skill 源码合同测试已经通过；Spec × Skill 的 Agent 对照实验、完整科研方法验证、E2 独立复现和 E3 正交/实验验证尚未闭环。**

当前已经证明：

- MultiQC 有一个真实 CLI 执行并进行内容验证的 vertical slice；
- shared-integration 有一个真实 PA/LUAD DEG 表输入、确定性交集和方向分层 slice；
- Evidence Closure Kernel 的状态和失败规则测试通过；
- 上游 `bulk-rnaseq` 和 `experimental-design` 的脚本测试通过；
- 5 个项目 Skill 的 staging/discovery 副本和 hash 一致。

当前没有证明：

- Agent 在 `no-skill` 与 `with-skill` 之间的实际提升；
- Agent 在 `no-spec` 与 `with-spec` 之间的实际提升；
- Skill 与 Spec 的交互效应；
- DEG、KEGG 或 WGCNA 在本仓库中的完整可执行科学方法链；
- BixBench case 已经具有本项目自己的 hidden oracle 和 artifact verifier；
- E2 独立队列复现或 E3 正交/生物学验证；
- 官方 preset/extension/workflow/bundle 已经可以从干净项目安装并运行。

## 一、最终采用的实验架构

后续 benchmark 的 canonical 结构应是：

```text
一个共同的 BixBench-compatible 生信 case set
        ×
        ┌──────────────────────────────┐
        │ C00 no-spec    + no-skill   │
        │ C01 no-spec    + with-skill │
        │ C10 with-spec  + no-skill   │
        │ C11 with-spec  + with-skill │
        └──────────────────────────────┘
        ×
同一模型 / harness / 输入 / 工具预算 / verifier
        ↓
重复运行与 task-level 统计
```

四个 cell 使用同一科学结果 verifier。`no-spec` 不能因为没有 `spec.md` 就在共同科学结果分数中自动判零；Spec 合规度另行记录。

四个主要效果为：

```text
Skill effect without Spec = C01 - C00
Spec effect without Skill = C10 - C00
Skill effect with Spec    = C11 - C10
Spec effect with Skill    = C11 - C01
Interaction               = C11 - C10 - C01 + C00
```

旧文档中的 `spec-fixture-design`、`spec-fixture-execution`、`spec-fixture-claims` 应理解为三个生命周期测试视图，而不是三套互不相干的最终 benchmark 数据集。最终 benchmark 仍应是“共同 case set + 2×2 条件”。

## 二、已执行测试与结果

### 2.1 本地 MVP 测试

| 测试对象 | 执行方式 | 结果 | 结论边界 |
|---|---|---:|---|
| MultiQC vertical slice | `python -m unittest discover -s spec-mvp\\tests -p test_*.py -v` | **7/7 passed** | wrapper、内容检查、输入变化传播、缺少 executable 的 fail-closed 通过 |
| Evidence Closure Kernel | `python -m unittest discover -s spec-mvp\\research-evidence-kernel\\tests -p test_*.py -v` | **7/7 passed** | supported、not-supported、inconclusive、not-evaluable 和 provenance/输入失败状态通过 |
| 上游 `bulk-rnaseq` | 独立 Python 3.14 环境，pytest + pandas | **39 passed + 16 subtests** | 上游脚本合同行为通过；不是 Agent Skill lift，也不是完整 FASTQ→DEG 重跑 |
| 上游 `experimental-design` | 独立 Python 3.14 环境，pytest + numpy/pandas/pyDOE3 | **40 passed + 14 subtests** | 随机化、区组、DOE、seed 和设计行为通过；不是 Agent 科研设计推理 benchmark |
| Skill staging/discovery | catalog 读取、5 个目录存在、staging/discovery `SKILL.md` hash 对比 | **5/5 matched** | 5 个 Skill 的安装副本与审计副本一致 |
| Python 编译 | `python -m compileall -q extensions spec-mvp .agents\\skills` | **PASS** | 当前 Python 文件可编译 |
| YAML 解析 | 排除 `.git`、`.venv`、`vendor`、`.specstory` 后检查项目 YAML | **33/33 valid** | 不是 Spec Kit 语义验证，只是 YAML 可解析 |
| diff 检查 | `git diff --check` | **PASS** | 未发现 whitespace error |

合计：

```text
命名测试：93/93 passed
额外 subtests：30/30 passed
本地垂直切片和 ECK：14/14 passed
```

这里的 `100%` 只表示**已经执行的确定性测试全部通过**，不能被解释成整个科研系统的准确率或 benchmark 分数。

### 2.2 真实 fixture 重跑

#### MultiQC

使用当前工作区的 FastQC fixture 和 `.venv` 中的 MultiQC 1.35 重新执行：

```text
exit                  = 0
status                = completed
ok                    = true
release_ready         = true
input_file_count      = 1
multiqc               = 1.35
verification_errors   = []
```

它证明的是：

```text
FastQC fixture → MultiQC 1.35 → HTML/JSON/source map → 内容 verifier
```

它不证明 FastQC binary 从原始 FASTQ 开始运行，也不证明下游 DEG、KEGG 或生物学 QC 门限成立。

#### PA/LUAD shared integration

使用 `research-top` 中现有 PA/LUAD DEG 表重新执行 `run_shared_integration.py`，并显式使用 `max-abs-effect` duplicate policy：

```text
exit                  = 0
status                = completed
ok                    = true
shared_count          = 149
UpUp                  = 50
DownDown              = 17
UpDown                = 73
DownUp                = 9
partition_sum         = true
membership_union      = true
claim_status          = descriptive_only
release_ready         = false
```

它证明的是：

- 两个已有 DEG artifact 可以被 wrapper 消费；
- duplicate policy 被显式记录；
- 149 个 shared gene 及四类方向分层可确定性重算；
- 输入、输出和 provenance 可以形成技术记录；
- 结果只能发布为 descriptive overlap。

它不证明：

- PA/LUAD 上游 DEG 统计模型已经在当前仓库重跑并验证；
- shared genes 代表共同机制或因果关系；
- KEGG/WGCNA 已经运行；
- E2 独立队列复现或 E3 实验验证已经完成。

## 三、Spec Kit 当前实际状态

### 已通过

```text
specify check                         PASS
specify preset resolve spec-template PASS（core）
specify preset resolve plan-template PASS（core）
specify preset resolve tasks-template PASS（core）
git diff --check                      PASS
```

### 当前没有安装

```text
specify preset list     → No presets installed
specify extension list  → No extensions installed
specify workflow list   → 只有官方 Full SDD Cycle
```

因此，仓库里存在的 `presets/bio-research-mvp/`、`extensions/*` 和 `workflows/*` 目前只是工作区候选文件，尚未证明能够通过官方 CLI materialize、注册和运行。

### 明确失败

```text
specify bundle validate --path .\\bundles\\bioinformatics-core
```

失败原因是 bundle manifest 引用了当前 bundle、active catalog 或已安装组件中不存在的：

```text
6 个 extension
1 个 preset
1 个 workflow
共 8 个 unresolved references
```

这不是科研结果失败，而是 Spec Kit 组件解析/安装闭环尚未完成。当前不能宣称 `bioinformatics-core` 已经可以一键安装。

## 四、当前评分

### 4.1 已执行自动化测试分数

```text
93/93 命名测试通过 = 100%
30/30 subtests 通过 = 100%
5/5 Skill staging/discovery hash 对齐 = 100%
33/33 项目 YAML 可解析 = 100%
```

这些是**技术合同测试分数**，不是 Skill、Spec 或科研结论的最终评分。

### 4.2 仍不能给出数值的评分

| 目标 | 当前分数 | 原因 |
|---|---:|---|
| `no-skill` vs `with-skill` Agent pass rate | **N/A** | 尚未对同一 case、同一模型、同一 verifier 做 Agent 成对运行 |
| `no-spec` vs `with-spec` effect | **N/A** | 2×2 条件尚未执行 |
| Skill × Spec interaction | **N/A** | 没有 `C00/C01/C10/C11` 四个 cell 的结果 |
| DEG/KEGG/WGCNA 方法正确率 | **N/A / 部分** | 只有部分真实结果和设计材料，缺完整 fixture、oracle、verifier 与 clean rerun |
| E1 完整科研计算链 | **部分通过** | MultiQC 和 shared slice 有技术证据，但没有完整 DEG→pathway→Claim 闭环 |
| E2 独立数据/holdout | **未闭环** | 当前缺少可审计的独立运行和预先定义的 replication criterion |
| E3 正交/实验验证 | **未达到** | 当前只有候选路线或设计材料，没有完成相应实验验证 |
| 完全无人值守自驾 | **NO** | 官方组件未 materialize，Agent benchmark 和人工 release gate 未闭环 |

### 4.3 现在唯一可以正式写入报告的主结论

```text
Technical deterministic slice score: 100% on executed tests
Scientific release status: NOT RELEASE-READY
Agent Skill efficacy: NOT EVALUATED
Spec efficacy: NOT EVALUATED
Full autonomous operation: NOT ESTABLISHED
```

不能把这五行压成一个“系统总分”，否则会把已通过的技术测试错误地解释成科学有效性。

## 五、当前硬缺口

1. **官方组件 materialization 没闭环**：自定义 preset、extension、workflow 没安装，bundle 有 8 个 unresolved references。
2. **`spec-fixture-design` 仍是骨架**：目录和说明存在，但 hidden oracle、deterministic verifier、negative cases 和 human rubric 仍是 `.gitkeep`，不是可运行 benchmark。
3. **没有 Agent 行为测试**：上游 39/40 个脚本测试证明代码行为，不证明 Agent 会正确路由、澄清、阻塞或交付。
4. **没有真正的 2×2 评分结果**：目前没有 `C00/C01/C10/C11`，所以没有 Skill effect、Spec effect 或 interaction 数值。
5. **BixBench 只完成候选来源登记**：`bix-26-q3` 已保存 capsule 和复核点，但还没有转成本项目自己的 task package、hidden oracle 和 artifact verifier。
6. **科研方法 runtime 不完整**：当前仓库没有完整 raw counts→DEG→shared→KEGG 的统一执行链，也没有 WGCNA fixture/preservation verifier。
7. **release 状态语义需要拆分**：MultiQC 的技术 artifact 可以 `release_ready=true`，但 shared integration 仍是 `descriptive_only` 且 `release_ready=false`；技术状态、Claim 状态和人工发布状态不能共用一个布尔值。
8. **旧文档存在架构漂移**：旧 roadmap/evaluation matrix 仍把三个 bundle 写成主要结构；最终应统一解释为“一个共同 case set + 三个生命周期测试视图 + 2×2 条件”。

## 六、最终 MVP 判定

### 已完成的 MVP-0A

```text
FastQC fixture → MultiQC → 内容验证报告
```

状态：**技术 vertical slice 通过**。

### 已完成技术部分的 MVP-0B

```text
固定 PA/LUAD DEG 表
→ shared intersection
→ 四类 direction strata
→ manifest/provenance/claim
```

状态：**技术执行通过；Claim 仅为 descriptive_only；不具备 release-ready 科研结论资格**。

### 尚未完成的 Bio-SpecBench MVP

```text
共同 BixBench-compatible case
× no/with Spec
× no/with Skill
→ 同一 scientific verifier
→ 四 cell pass rate
→ Skill/Spec effect
→ interaction
```

状态：**尚未开始正式评分**。当前 `specs/004-spec-research-core/spec-fixture-design/` 只是设计骨架，不能算已通过 benchmark。

## 七、最终判断

```text
继续无限寻找新 benchmark       NO
现在开始自己的 MVP             YES
把当前结果称为完全自驾          NO
把 93/93 测试通过称为科学正确率  NO
把 shared 149 称为共同机制      NO
把 KEGG 富集称为独立验证         NO
把现有静态研究结果称为 E2/E3     NO
```

最终定位：

> **Bio-Spec Kit 当前是一个“官方 Spec Kit 兼容的、证据门控的科研自动化候选架构”，已经有局部可执行 vertical slice，但尚未成为完成 2×2 Agent benchmark、完整 E1/E2/E3 验证和人工发布闭环的自动科研系统。**

## 八、关键入口

- [总参考与历史决策](BIO-SPEC-KIT-REFERENCE.md)
- [当前项目 README](README.md)
- [评测矩阵](spec-mvp/docs/evaluation-matrix.md)
- [MultiQC vertical slice Spec](specs/002-multiqc-vertical-slice/spec.md)
- [Shared integration vertical slice Spec](specs/003-shared-integration-vertical-slice/spec.md)
- [Spec research design bundle 骨架](specs/004-spec-research-core/spec-fixture-design/README.md)
- [BixBench/SkillsBench 来源与适配说明](specs/004-spec-research-core/spec-fixture-design/reference-package/benchmark-source-map.md)
- [SkillsBench 对照协议](specs/004-spec-research-core/spec-fixture-design/reference-package/skillsbench-reference.md)
- [旧的路线摘要（需按本报告解释）](SPEC-RESEARCH-MVP-ROADMAP.md)

## 九、外部评测参考

- [SkillsBench 官方论文](https://www.skillsbench.ai/skillsbench.pdf)：task package、oracle、deterministic verifier、重复运行和 Skill paired evaluation。
- [SkillsBench 官方仓库](https://github.com/benchflow-ai/skillsbench)：当前 native task package 与 BenchFlow 运行入口。
- [Inspect AI](https://inspect.aisi.org.uk/)：Dataset、Solver、Scorer、Sandbox 和可分析 eval log 的科研评测抽象。
- [HELM](https://crfm.stanford.edu/helm/latest/)：多指标、透明和可复现的模型评测原则。
- [Langfuse Scores](https://langfuse.com/docs/evaluation/scores/overview)：trace/observation/session/dataset run 的评分记录层，不替代领域 verifier。

