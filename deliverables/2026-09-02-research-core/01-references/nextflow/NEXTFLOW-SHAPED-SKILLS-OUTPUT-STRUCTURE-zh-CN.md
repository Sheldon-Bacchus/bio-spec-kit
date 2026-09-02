# Nextflow 形态的生信 Skills 输出结构设计（草案）

> 状态：design-only，供人工评审。本文不改写现有 Skill、不接管当前运行时，也不把
> Nextflow 假装成已经接入的执行器。
>
> 本文把用户口述中的 “Next Flower / Alex Flow” 按 Nextflow 理解。仓库中实际读取的
> 参照是 vendor/sources/bioSkills/workflow-management/nextflow-pipelines/ 和
> vendor/sources/nfcore-rnaseq/。

## 先看结论

这个方向是可行的，而且比继续逐个讨论每一个 Skill 更适合作为当前的总设计。
Nextflow 提供的不是一张更复杂的输入输出表，而是一套可组合的组件边界：

~~~text
process / module       一个可执行节点，声明输入、输出和命令
channel                节点之间的数据流，携带显式身份和数据形状
subworkflow            多个节点的有名组合，使用 take / main / emit
workflow               面向一次完整分析的入口和终端发布
profile / config       资源、容器、执行器和环境，不塞进方法代码
tests / provenance     运行证据、版本、哈希、快照和失败诊断
~~~

本项目应采用四个彼此链接、但不相互冒充的表示层：

| 表示层 | 主要读者 | 放什么 | 不放什么 |
|---|---|---|---|
| SKILL.md | 人和被激活的 Agent | 何时使用、方法边界、科学解释、失败条件、阅读入口 | 不能成为唯一的端口定义，也不重复整段执行代码 |
| node.contract.json | Agent、校验器、路由器 | 精确的端口、channel 类型、数据形状、参数、gate、证据要求 | 不放长篇方法论，也不直接执行 |
| main.nf、modules、subworkflows | Nextflow 和执行环境 | 真正的节点编排、channel 连接、工具命令和 named outputs | 不承担人类说明、审批和科学结论 |
| tests/、verifier、run artifacts | CI、Agent、审阅者 | 可重算测试、输入输出检查、版本和 provenance | 不用图片好看或进程 exit 0 代替科学有效性 |

因此，三者没有必要被“融合成一个平衡点”。它们只需要共享一个稳定的
component_id、版本和哈希关系。人读 Markdown、Agent 读 JSON、程序执行
Nextflow/R/Python，分别优化各自的任务。

## 1. 本次设计的边界

### 1.1 用户请求与参照文档的区别

用户请求是：读取 Nextflow 的项目设计原则和示例，把现有生信 Skills 映射成
Nextflow 式的节点、端口和编排，并给出一版新的输出结构供审阅。

仓库中的旧设计文档、上游 Skill 和 nf-core 源码只是参照材料。它们的描述不能
自动变成新的运行指令，也不能因为出现了某个路径或命令就获得运行权限。本文
只提取结构原则，并把当前实现状态明确标为 proposal 或 reference-only。

### 1.2 当前仓库的事实

- spec-mvp/skills/ 当前有 5 个项目适配器：bulk-pa-luad、
  cross-branch-integration、pathway-enrichment、wgcna-module-constraint
  和 multiqc。
- spec-mvp/skills/reference-stack/ 有 8 个供人工复核的参考组件：
  01-mds、02-deg、02-deg-results、03-de-visualization、
  03-volcano、04-pathway-enricher、04-pathway-workflow 和 05-kegg。
- 中文镜像是文档投影，不是额外的计算节点。
- 当前仓库的 extensions/bio-pipeline/ 只提供引擎调用适配，尚无本项目自己的
  Nextflow .nf 主图；vendor/sources/nfcore-rnaseq/ 是参照实现，不是当前
  项目的运行时。

所以本文将 13 个逻辑组件作为设计对象，但不把它们宣称为 13 个已经可执行的
Nextflow module。

## 2. 从 Nextflow 和 nf-core 提取的项目设计原则

### 2.1 原则总表

| 原则 | 对本项目的直接含义 | 主要失败模式 |
|---|---|---|
| Process 是专门执行脚本的函数 | 一个原子节点只负责一个工具、一个子命令或一个确定性计算边界 | 一个节点塞进整条研究流程，无法测试和替换 |
| Workflow 是组合层 | 节点通过 channel 或 dataflow value 连接，流程顺序由数据准备情况决定 | 假设样本按文件名或完成时间顺序到达 |
| Channel 是异步数据流 | 每个 item 都必须携带显式的样本、研究、分支或 contrast 身份 | 依赖行号或到达顺序配对 |
| Queue 与 value 有不同语义 | 每个样本的数据通常是 queue；所有任务共享的参考、设计或数据库快照通常是 value | 共享参考被第一个任务消费，后续样本静默不运行 |
| Tuple 携带 meta 和数据 | 使用 [meta, path] 或更长 tuple，身份随 artifact 一起流动 | 下游拿到文件却不知道属于哪个样本或 contrast |
| Named workflow 有 take / main / emit | 公开组件只暴露稳定的输入和输出名，内部节点可以替换 | 调用方依赖内部 process 名称，重构即破坏 |
| 配置和 profile 与方法分离 | executor、CPU、memory、container、conda、队列放在 config/profile | 把 SLURM 或本机路径写死进分析方法 |
| 缓存依赖任务身份 | 固定输入顺序、容器/环境、脚本和参数；关键输入要有哈希 | -resume 命中陈旧结果或因不稳定顺序全部重跑 |
| work 与终端发布分离 | 下游使用 process output channel；人看的目录是 publish/export 层 | 把 publish 目录当成缓存真相或上游输入 |
| 测试是组件的一部分 | 每个 module/subworkflow 有最小 fixture、stub、输出断言和稳定快照 | 只测进程 exit 0，不测输出语义 |
| 路由在 workflow 层显式表达 | ORA/GSEA、GO/KEGG、edgeR/limma 等由参数和 workflow 分支选择 | 让 LLM、文件名或隐式默认值偷偷改方法 |
| 进程成功不等于科学通过 | 运行状态、科学 verifier、人工 review 三种状态分开 | 生成了 HTML 就声称 QC 或研究结论成立 |

官方文档对这些边界的定义见
[Processes](https://docs.seqera.io/nextflow/process)、
[Workflows](https://docs.seqera.io/nextflow/workflow)、
[Modules](https://docs.seqera.io/nextflow/modules/) 和
[Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume)。

### 2.2 nf-core 的工程化补充

nf-core/rnaseq 把上述原则落实成了项目目录和贡献规则：

~~~text
modules/nf-core/       可复用的外部原子模块，按版本或 SHA 管理
modules/local/         只属于本项目的组件
subworkflows/nf-core/  可复用的多节点组合
subworkflows/local/    本项目特有的组合
conf/                  资源、profile、模块配置和参数默认值
meta.yml               组件输入、输出、工具和语义说明
tests/                 module/subworkflow/pipeline 级 nf-test
versions topic         独立记录软件版本，避免每条数据流重复携带
~~~

这对本项目最有用的不是照抄目录名，而是三条约束：

1. 复用的最小粒度是组件，而不是整篇 Skill。
2. 组件的输入输出文档和测试与代码同目录。
3. 项目特有逻辑放 local 层；上游可复用模块不直接在本项目里偷偷改写。

本地参照中的具体例子：

- vendor/sources/bioSkills/workflow-management/nextflow-pipelines/SKILL.md
  解释了 queue/value、tuple、.first()、collect()、-resume、profile
  和 fail-closed 的工程陷阱。
- vendor/sources/bioSkills/workflow-management/nextflow-pipelines/examples/rnaseq.nf
  展示了 FASTP → SALMON → MULTIQC 的 DSL2 连接、共享 index 的 value channel
  和 stub。
- vendor/sources/nfcore-rnaseq/modules/nf-core/multiqc/main.nf、
  meta.yml 和 tests/main.nf.test 展示了同一个组件如何分开写代码、输入输出
  语义和最小测试。
- vendor/sources/nfcore-rnaseq/workflows/rnaseq/main.nf 展示了复杂 pipeline
  如何通过 named outputs、join、mix、collect、条件分支和版本通道组合大量模块。

## 3. 建议的 Skill 包结构

这是目标结构，不是本次要一次性创建的所有文件：

~~~text
spec-mvp/skills/<component-id>/
├── SKILL.md                         # 人读：触发边界和科学语义
├── node.contract.json               # Agent 读：精确端口和 gate
├── main.nf                          # 公开入口：process 或 named workflow
├── meta.yml                         # 可选：nf-core 风格组件文档
├── modules/
│   ├── <atomic-node>/main.nf        # 一个工具/子命令/确定性计算
│   └── <atomic-node>/meta.yml
├── subworkflows/
│   └── <composition>/main.nf        # 多个原子节点的组合
├── scripts/                         # R/Python/CLI wrapper，负责数值计算
├── conf/
│   ├── base.config                  # 默认资源和通用策略
│   ├── test.config                  # 最小 fixture 和测试资源
│   └── profiles.config              # docker/conda/slurm 等环境
├── tests/
│   ├── main.nf.test                 # 组件级执行和输出断言
│   ├── fixtures/                    # 最小、可分发、可审计输入
│   └── snapshots/                   # 稳定文本或经过过滤的快照
├── examples/                        # 人类可复制的最小调用例
└── references/                      # 方法依据和限制，不是运行入口
~~~

运行时分层建议保持现有方向：

node.contract.json 不是 Nextflow 原生语法，
~~~text
.agents/skills/<component-id>/SKILL.md
    ↑ discovery projection，只放可激活的人读入口
spec-mvp/skills/<component-id>/
    ↑ 可审计的 Skill package，包括 contract、Nextflow、tests
pipelines/<pipeline-id>/main.nf
    ↑ 一次研究分析的总 workflow，调用多个 Skill component
workflows/bio-research-mvp/workflow.yml
    ↑ Spec Kit 生命周期和人工 gate，不是科学计算图
extensions/bio-pipeline/
    ↑ 引擎调用适配，不拥有分析方法本身
~~~
也不是把 nextflow_schema.json
改名。它是项目给 Agent 和 verifier 使用的桥接合同；Nextflow 的参数 schema
继续负责 pipeline CLI 参数，二者不应互相冒充。

## 4. 三种表示如何保持分离

### 4.1 SKILL.md：给人和被激活的 Agent

每个 SKILL.md 只保留以下内容：

~~~text
触发条件
不适用条件
本组件解决的科学问题和 estimand
方法选择规则和默认 preset
必须保留的身份、方向、universe、reference release
fail-closed 条件
按需阅读的 references
node.contract.json / main.nf / tests 的入口链接
~~~

它可以有一段很短的 contract 摘要，但精确端口、cardinality 和 tuple 形状
以 JSON 为准；否则每次改端口都要手工同步多份自然语言。

### 4.2 node.contract.json：给 Agent 和机器

建议的最小字段如下：

~~~json
{
  "schema_version": "0.1",
  "component_id": "bulk-pa-luad",
  "kind": "subworkflow",
  "status": "proposal",
  "entrypoint": {
    "script": "main.nf",
    "symbol": "BULK_PA_LUAD"
  },
  "identity": {
    "item_key": "meta.id",
    "required_meta": [
      "study_id",
      "reference_release"
    ]
  },
  "inputs": [
    {
      "port_id": "counts",
      "channel": "value",
      "shape": "path",
      "cardinality": "one",
      "artifact_type": "raw_integer_count_matrix",
      "required": true,
      "constraints": [
        "integer_counts",
        "feature_id_unique"
      ]
    },
    {
      "port_id": "sample_manifest",
      "channel": "value",
      "shape": "path",
      "cardinality": "one",
      "artifact_type": "sample_metadata",
      "required": true,
      "constraints": [
        "subject_and_condition_present",
        "stable_sample_id"
      ]
    },
    {
      "port_id": "contrast",
      "channel": "queue",
      "shape": "value",
      "cardinality": "many",
      "artifact_type": "declared_contrast",
      "required": true
    }
  ],
  "outputs": [
    {
      "port_id": "de_table",
      "channel": "queue",
      "shape": "tuple",
      "tuple": [
        "meta",
        "path"
      ],
      "artifact_type": "frozen_differential_expression_table",
      "required": true
    },
    {
      "port_id": "tested_universe",
      "channel": "queue",
      "shape": "tuple",
      "tuple": [
        "meta",
        "path"
      ],
      "artifact_type": "tested_gene_universe",
      "required": true
    },
    {
      "port_id": "verdict",
      "channel": "queue",
      "shape": "tuple",
      "tuple": [
        "meta",
        "path"
      ],
      "artifact_type": "machine_verdict",
      "required": true
    }
  ],
  "routes": {
    "method": {
      "type": "enum",
      "values": [
        "edgeR_QL",
        "paired_limma"
      ],
      "required": true
    }
  },
  "gates": [
    {
      "id": "pairing_complete",
      "stage": "precondition",
      "on_fail": "fail_closed",
      "verifier": "design-check"
    },
    {
      "id": "universe_present",
      "stage": "postcondition",
      "on_fail": "not_release_ready",
      "verifier": "artifact-check"
    }
  ],
  "execution": {
    "profiles": [
      "test",
      "docker",
      "slurm"
    ],
    "container_policy": "immutable_reference",
    "resume_policy": "inputs_and_environment_must_be_pinned"
  },
  "evidence": {
    "tests": [
      "tests/main.nf.test"
    ],
    "required_manifest_fields": [
      "input_hashes",
      "tool_versions",
      "parameters",
      "command",
      "exit_code"
    ]
  }
}
~~~

这里的 channel 是接口语义，不要求 Agent 直接解析 Groovy。最重要的新增
信息是：

- 输入/输出的 cardinality；
- queue 还是 value；
- path、value 还是 tuple；
- tuple 中身份字段和 artifact 的关系；
- 路由是显式枚举还是固定 preset；
- 哪些是执行前提、哪些是执行后验证、失败如何传播；
- 运行证据和测试在哪里。

### 4.3 Nextflow：只表达执行和连接

一个原子统计节点可以采用下面的形态。命令和容器只是示意，不能直接当作
当前项目的已完成实现：

~~~nextflow
process EDGER_QL {
    tag meta.id
    label 'process_high'
    container 'registry.example/edger-runner@sha256:PINNED_DIGEST'

    input:
    tuple val(meta), val(contrast)
    path counts
    path sample_manifest

    output:
    tuple val(meta), path('de-edger.tsv'), emit: de
    tuple val(meta), path('tested-universe.tsv'), emit: universe
    tuple val(meta), path('run-provenance.json'), emit: provenance

    script:
    """
    Rscript run_edger_ql.R --counts $counts --metadata $sample_manifest --contrast $contrast --out-table de-edger.tsv --out-universe tested-universe.tsv --out-provenance run-provenance.json
    """

    stub:
    """
    touch de-edger.tsv tested-universe.tsv run-provenance.json
    """
}
~~~

对应的公开 subworkflow 只负责组合节点和命名输出：

~~~nextflow
include { CHECK_DESIGN } from './modules/check-design'
include { EDGER_QL } from './modules/edger-ql'
include { LIMMA_PAIRED } from './modules/limma-paired'
include { FREEZE_DE } from './modules/freeze-de'

workflow BULK_PA_LUAD {
    take:
    counts
    sample_manifest
    contrasts
    options

    main:
    checked = CHECK_DESIGN(counts, sample_manifest, contrasts, options)

    if (options.method == 'edgeR_QL') {
        primary = EDGER_QL(checked.contrasts, counts, sample_manifest)
    } else if (options.method == 'paired_limma') {
        primary = LIMMA_PAIRED(checked.contrasts, counts, sample_manifest)
    } else {
        error 'Unsupported method'
    }

    frozen = FREEZE_DE(primary.de, primary.universe, primary.provenance)

    emit:
    de = frozen.de
    tested_universe = frozen.universe
    verdict = frozen.verdict
}
~~~

这里有三个硬约束：

1. 方法路由由 options.method 这样的显式值决定，不能由 Agent 根据文件名猜。
2. FREEZE_DE 接收已执行的结果和 universe；它不能重新计算或手工修改 p-value、
   FDR、logFC。
3. stub 只能证明 wiring 和文件形状，不能让 stub 结果进入 release。

### 4.4 channel 编排的通用模板

~~~text
queue channel       每个样本/contrast 一项，消费一次
value channel       一个参考/设计/数据库快照，所有任务复用
map                 纯变换身份或形状，不做外部副作用
join                依据稳定 key 对齐，必须保留 unmatched 审计
branch/filter       显式路由，不让隐式默认值选择科学方法
collect             将多项汇聚为一个聚合任务，例如 MultiQC
mix                 汇聚不同来源的同类 QC 文件，顺序不作为语义
emit                对外公开稳定的命名输出
publish/export      终端展示或交付，不作为上游计算合同
~~~

共享参考的典型写法是把 queue 转成 value：

~~~nextflow
reads_ch = Channel.fromFilePairs(params.reads, checkIfExists: true)
index_ch = Channel.fromPath(params.index, checkIfExists: true)

// 正确：一个 index 在每个样本任务中复用
ALIGN(reads_ch, index_ch.first())
~~~

不能把多样本 channel 的完成顺序当作样本顺序。所有需要关联的对象都要把
sample_id、subject_id、branch_id 或 contrast_id 放进 tuple/meta。

## 5. 新的输出结构

### 5.1 节点输出不是一个扁平目录

旧的输入输出合同仍然有用，但只适合作为摘要视图。Nextflow 形态的 public
interface 应该把数据流和证据分开命名：

~~~text
component.out
├── primary                 下游分析真正消费的主 artifact
├── diagnostics             QC、设计矩阵、mapping loss、稳定性等诊断
├── provenance              输入/参数/工具/容器/命令/版本/哈希
├── verdict                 机器可读的执行和科学检查结果
└── report                  给人打开的 HTML/Markdown/图，不作为唯一证据
~~~

规则是：

- primary、diagnostics、provenance、verdict 都可以进入下游 channel；
- report 是可审阅的视图，不能反向生成结果；
- verdict 至少区分 execution_status、scientific_status 和 release_ready；
- 人工审批另存为 review/approval.json 或 Spec Kit 的 gate artifact，不写入
  原始统计结果。

### 5.2 一次运行的建议目录

~~~text
.bio/runs/<run-id>/
├── run-manifest.json              # workflow、revision、profile、参数和时间
├── input-manifest.json            # 每个输入的路径、类型、reference、hash
├── results/
│   ├── bulk-pa-luad/
│   │   ├── data/
│   │   ├── diagnostics/
│   │   ├── provenance.json
│   │   └── verdict.json
│   ├── pathway-enrichment/
│   │   ├── data/
│   │   ├── reports/
│   │   ├── provenance.json
│   │   └── verdict.json
│   └── multiqc/
│       ├── multiqc_report.html
│       ├── multiqc_data/
│       ├── provenance.json
│       └── verdict.json
├── trace/
│   ├── trace.tsv
│   ├── report.html
│   └── timeline.html
└── review/
    ├── review.md
    └── approval.json
~~~

Nextflow 自己管理的 work/ 和 .nextflow/cache/ 不应被冒充成上面的发布结果。
work/ 保存任务执行现场，-resume 依赖任务缓存和工作目录；results/ 是人和
下游交付使用的稳定投影。终端发布可以使用当前版本支持的 workflow output
或 publish/export 机制，但不能改变 process output 的 dataflow 语义。

### 5.3 输出字段的最小机器合同

每个 verdict.json 应至少能回答：

~~~text
这是哪一个 component、哪一个 run、哪一个 item？
它实际接收了哪些输入，输入 hash 是什么？
实际使用了什么 method、preset、参数、reference release 和数据库版本？
实际运行了什么命令、什么容器/环境、什么 Nextflow revision？
进程是否成功？artifact 是否存在且内容来自输入？
科学前提是否通过？哪些项是 warning、failed 或 not evaluated？
是否允许进入下游？是否允许发布？是否仍需人工审批？
~~~

## 6. 13 个现有逻辑组件的 Nextflow 映射

### 6.1 映射表

| 当前组件 | 建议的 public kind | 内部节点或分支 | 设计判断 |
|---|---|---|---|
| 01-mds | process/module | MDS_QC、样本距离和结构诊断 | 一个可复用诊断节点；不能把 MDS 当成 DEG 或删样本决策 |
| 02-deg | subworkflow（reference-only） | DESEQ2、EDGER、LIMMA 方法族 | 方法参考集合，不另起一个与项目 adapter 冲突的 runtime |
| bulk-pa-luad | subworkflow | CHECK_DESIGN → EDGER_QL，可选 LIMMA_PAIRED → FREEZE_DE | 公开的是 paired bulk preset；内部可替换工具但不改变 estimand |
| 02-deg-results | process/module | FREEZE_DE、结果字段和 tested universe 审计 | 结果冻结是独立边界，不能被火山图或富集脚本隐式重写 |
| 03-de-visualization | subworkflow | MDS/PCA、MA、p-value、heatmap | 从冻结 DE 和诊断输入派生多个视图 |
| 03-volcano | module，由可视化 subworkflow 调用 | VOLCANO_PLOT | 和 DE visualization 有输入和输出重叠；保留独立 module 复用，不再作为平行大 Skill |
| cross-branch-integration | subworkflow | SAMPLE_MAP_CHECK → ID_HARMONIZE → INTERSECTION → DIRECTION_STRATA | 当前可由一个 deterministic process 实现；未来 joint model 必须是独立 route |
| pathway-enrichment | subworkflow | ID_MAP → ORA 或 GSEA，再并行 GO / KEGG → ENRICHMENT_VERIFY | 公开一个受约束入口；GO 与 KEGG 从同一已冻结输入并行 |
| 04-pathway-workflow | subworkflow/router | PATHWAY_ROUTE、方向分支、ORA/GSEA 选择 | 它是编排层，不是另一个富集算法 |
| 04-pathway-enricher | process/module（reference-only） | ENRICHR_QUERY | 外部服务 adapter，不能替代本地可复现的 pathway contract |
| 05-kegg | subworkflow（reference-only） | KEGG_ORA、可选 KEGG_SPIA、snapshot/check | KEGG 的 organism、keyType、release 和网络状态需要独立边界 |
| wgcna-module-constraint | subworkflow | SAMPLE_GENE_QC → SIGNED_NETWORK → MODULE_TRAIT → STABILITY_GATE → HANDOFF | 稳定性 gate 前只能是描述性模块，不能把共表达变成因果边 |
| multiqc | subworkflow façade | MULTIQC → VERIFY_MULTIQC | 当前唯一已接通 executable；报告生成和阈值/人工 gate 继续分离 |

### 6.2 合并、保留和不可替代

| 关系 | 处理方式 | 原因 |
|---|---|---|
| 03-de-visualization 与 03-volcano | 合成一个 DE visualization public subworkflow，火山图作为可复用 module | 两者都消费冻结 DE；合并入口可以减少重复触发，但不抹掉火山图的独立复用性 |
| 02-deg 与 bulk-pa-luad | 不直接合并；由 bulk-pa-luad 持有项目 paired preset，02-deg 做方法参考 | 上游方法知识和项目运行合同是两个所有权边界 |
| 04-pathway-workflow 与 04-pathway-enricher | 不合并；前者路由，后者外部实现 | 路由决策不能被某一个服务实现绑架 |
| 04-pathway-workflow 与 05-kegg | 不合并；KEGG 是有独特数据库和 ID 状态的 backend/subworkflow | GO/KEGG 可并行，但证据来源和版本边界不同 |
| multiqc 与 QC gate | 不合并 | MultiQC 负责汇总和报告；是否通过阈值属于 verifier/Spec gate |
| cross-branch-integration 与各上游 omics 分析 | 不合并 | 交集和方向分层不能替代每个分支的 normalization、model 或 QC |
| 中文/英文 Skill 镜像 | 合并为同一 component 的文档投影 | 翻译不是新的计算节点，也不应造成两个版本的端口漂移 |
| wgcna 与 pathway | 保留 handoff，不合并算法 | 模块基因可以成为 pathway foreground，但共表达和富集的 estimand 不同 |

## 7. 复杂 Skill 的通用编排方式

### 7.1 bulk paired DE

~~~text
counts + sample_manifest + explicit contrast
                │
                ▼
       CHECK_DESIGN / pairing audit
                │
        ┌───────┴────────┐
        ▼                ▼
    EDGER_QL       LIMMA_PAIRED
        └───────┬────────┘
                ▼
          FREEZE_DE
        ┌───────┼─────────┐
        ▼       ▼         ▼
      plots   pathway   cross-branch
~~~

只有 FREEZE_DE 后的表和 tested universe 才能流入下游。MDS/PCA 是上游诊断
和独立视图，不是从图反推基因列表的入口。

### 7.2 pathway enrichment

~~~text
frozen DE table / module genes + tested universe + ID namespace
                              │
                              ▼
                         ID_MAP_AUDIT
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
          GO branch                         KEGG branch
       ORA or full-rank GSEA              ORA or topology
             │                                 │
             └────────────────┬────────────────┘
                              ▼
                 mapping / DB / result verifier
~~~

GO 不需要先于 KEGG。两条分支共享输入合同，但各自保存 ontology、organism、
keyType、数据库版本或访问日期。

### 7.3 WGCNA constraint

~~~text
normalized bulk expression + traits + batch/subject metadata
                              │
                              ▼
                       SAMPLE_GENE_QC
                              │
                              ▼
                      SIGNED_NETWORK
                              │
                              ▼
                       MODULE_TRAIT
                              │
                              ▼
                     PRESERVATION / RESAMPLING
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
          constraint eligible       reference-only
                  │
                  ▼
          pathway handoff
~~~

稳定性没有执行或没有达到 preset 规则时，输出仍可以用于探索，但不能标记为
下游 constraint。

### 7.4 MultiQC

~~~text
upstream logs/metrics
        │
        ▼
bounded input manifest
        │
        ▼
MULTIQC process
        │
   ┌────┴──────────────┐
   ▼                   ▼
HTML/data          VERIFY_MULTIQC
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        machine verdict       human review
~~~

报告是视图，multiqc-verdict.json 是检查结果，Spec Kit 的 review gate 才是
发布授权。三者不互相替代。

## 8. Spec Kit 与 Nextflow 的连接点

建议把一次研究任务的生命周期写成下面的分层调用链：

~~~text
spec.md
  └─ 研究问题、estimand、限制、验收边界
       ↓
plan.md
  └─ component graph、method route、reference 和 preset
       ↓
tasks.md
  └─ 需要创建/修改/运行/复核的具体任务
       ↓
node.contract.json
  └─ Agent 可校验的端口、channel、gate 和证据要求
       ↓
main.nf / subworkflows / modules
  └─ Nextflow 的实际 dataflow 和工具执行
       ↓
R/Python/CLI + container
  └─ 真正的数值计算
       ↓
verifier + provenance + trace
  └─ 内容级检查、版本、哈希、失败原因
       ↓
review/approval.json
  └─ 人工判断和 release gate
~~~

所有权边界应固定为：

| 所有者 | 负责 | 不负责 |
|---|---|---|
| Spec Kit | 意图、计划、任务、人工 gate、用户可观察验收 | 不证明 R/CLI 真的计算过正确结果 |
| Skill | 方法语义、触发边界、preset、失败解释 | 不直接执行 shell，也不改写数值结果 |
| node.contract.json | 机器可读的接口和策略 | 不替代科学方法正文或运行证据 |
| Nextflow | 节点生命周期、channel、并行、缓存、重试和执行器抽象 | 不判定研究假设是否成立 |
| R/Python/CLI | 数值计算和确定性 artifact | 不决定上层研究问题和人工发布 |
| verifier | 内容、字段、hash、mapping、universe、版本等可复核检查 | 不把 warning 自动升级成结论 |
| 人工 reviewer | 对估计目标、限制和 release 的最终判断 | 不应手工编辑原始统计 artifact |

这也解释了为什么 Markdown、JSON 和代码不需要融合：它们在调用链中承担不同
的所有权。

## 9. 需要新增的缺口节点

如果把当前 5 个项目 adapter 真正迁移成 Nextflow 形态，缺的不是更多自然语言，
而是下面这些可复用基础组件：

| 缺口 | 建议 public component | 作用 |
|---|---|---|
| 输入合同验证 | INTAKE_VALIDATE | 检查文件类型、样本 roster、ID、物种、reference release 和必需字段 |
| 参考和数据库解析 | REFERENCE_RESOLVE | 把 genome/annotation/OrgDb/KEGG snapshot 解析成 pinned artifact |
| 设计和对齐验证 | DESIGN_CHECK、SAMPLE_MAP_CHECK | 在统计或交集之前失败闭合，禁止按行号配对 |
| artifact 内容验证 | ARTIFACT_VERIFY | 检查结果确实来自输入、字段齐全、空结果语义正确 |
| provenance 汇总 | PROVENANCE_COLLECT | 汇总输入、参数、工具、容器、命令、版本、hash 和 Nextflow trace |
| 研究 gate | REVIEW_GATE | 把 machine verdict 和人工批准分成两个状态；可由外层 workflow 实现 |
| 最小测试套件 | TEST_HARNESS | stub wiring、真实小 fixture、negative case、snapshot 稳定性 |
| 参数和端口 schema | CONTRACT_LINT | 检查 SKILL.md、JSON、Nextflow named outputs 是否发生漂移 |

其中 REVIEW_GATE 不应被伪装成 Nextflow 的普通 process：Nextflow 可以输出
待审阅 artifact，但“人是否批准”属于 Spec Kit/外层工作流状态。

## 10. 从旧输入输出表迁移到新合同

旧表不删除，先变成一个人类快速阅读的 summary projection：

~~~text
旧视图：
    inputs → outputs

新视图：
    component
      ├── semantic boundary
      ├── input ports
      │     ├── queue/value
      │     ├── cardinality
      │     ├── shape: path/value/tuple
      │     └── identity and constraints
      ├── explicit route / preset
      ├── process and subworkflow graph
      ├── output channels
      │     ├── primary
      │     ├── diagnostics
      │     ├── provenance
      │     └── verdict
      ├── tests and negative cases
      ├── cache / environment / executor policy
      └── terminal publish and human review
~~~

也就是说，Nextflow 结构是旧合同的包络和展开，不是一次推翻。人先看 summary
和 graph，Agent 查 JSON，执行器读 .nf，各自只加载自己需要的层。

## 11. 第一轮落地顺序

本轮只建议采用结构，不立即把 13 个组件全部改写：

1. 先给 multiqc 写一份 node.contract.json 和 Nextflow façade，复用现有
   wrapper、fixture、verdict 和 review 规则。
2. 把 bulk-pa-luad 作为第一个真正的 subworkflow，验证 value/queue、contrast
   fan-out、结果冻结和 tested universe 传递。
3. 把 pathway-enrichment 拆成 ID mapping、GO/KEGG 分支和统一 verifier，
   先做 offline fixture，再接外部数据库 snapshot。
4. 把 wgcna-module-constraint 和 cross-branch-integration 接到明确的
   stability/sample-map gate 后面。
5. 最后把 reference-stack 变成可复用 module 的来源映射，而不是直接把所有
   reference Skill 变成默认 runtime。

### 11.1 结构验收标准

一项 component 进入下一阶段前，应满足：

- 有唯一 component_id 和 interface version；
- SKILL.md、node.contract.json、main.nf 和测试的职责不混淆；
- 所有 public input/output 有明确 shape、cardinality、channel 和 identity；
- 能在最小 fixture 上执行或 stub 通过 wiring；
- 每个 output channel 都有断言，至少有 success、version 和 negative case；
- 运行结果有 input hash、参数、工具/容器版本、命令、exit code 和 provenance；
- -resume 的前提是输入顺序、环境、参考和参数稳定；
- process success、科学 verifier 和人工 release 三个状态不被合并；
- 现有扁平输入输出表仍能从合同生成，不出现两套互相矛盾的事实；
- 未经评审前，不修改当前 .agents/skills/ allowlist 和既有运行路径。

## 12. 当前建议固定的决策

为了让这份草案可以快速评审，我建议先固定以下五点：

1. **采用 Nextflow 作为执行结构参照**，不是要求每个 Skill 立刻变成一个完整
   pipeline。
2. **以 process/module 为原子单元，以 subworkflow 为 Skill public façade**；
   只有完整研究链才使用顶层 workflow。
3. **保留三种文件表示的分离**：SKILL.md、node.contract.json、
   main.nf/scripts。
4. **保留旧输入输出表作为 summary projection**，不把它当成唯一合同，也不
   删除现有结果和 verifier 语义。
5. **先做文档和一个 MultiQC proof，再决定是否迁移其余 Skill**；本文件本身
   不触发代码迁移。

需要人工确认、但不影响结构判断的细节只有：

- JSON 文件最终叫 node.contract.json 还是项目统一的其他名称；
- Nextflow 最低支持版本，以及是否启用 typed process/workflow；
- 终端发布采用新 workflow output 还是兼容旧版本的 publish/export adapter；
- pipelines/ 是否作为独立顶层目录，还是把第一次实现放在现有
  extensions/bio-pipeline/ 旁边。

## 13. 参照来源

### 本地已读来源

- [Nextflow authoring Skill](../../vendor/sources/bioSkills/workflow-management/nextflow-pipelines/SKILL.md)
- [Nextflow usage guide](../../vendor/sources/bioSkills/workflow-management/nextflow-pipelines/usage-guide.md)
- [RNA-seq DSL2 example](../../vendor/sources/bioSkills/workflow-management/nextflow-pipelines/examples/rnaseq.nf)
- [nf-core/rnaseq README](../../vendor/sources/nfcore-rnaseq/README.md)
- [nf-core/rnaseq contribution conventions](../../vendor/sources/nfcore-rnaseq/docs/CONTRIBUTING.md)
- [nf-core MultiQC module](../../vendor/sources/nfcore-rnaseq/modules/nf-core/multiqc/main.nf)
- [nf-core MultiQC metadata](../../vendor/sources/nfcore-rnaseq/modules/nf-core/multiqc/meta.yml)
- [nf-core MultiQC test](../../vendor/sources/nfcore-rnaseq/modules/nf-core/multiqc/tests/main.nf.test)
- [当前项目模块设计](module-design.md)
- [当前项目架构分析](architecture-analysis.md)
- [当前项目 Skill staging](../skills/README.md)

### 官方在线参考

- [Nextflow Processes](https://docs.seqera.io/nextflow/process)
- [Nextflow Workflows and dataflow](https://docs.seqera.io/nextflow/workflow)
- [Nextflow Modules](https://docs.seqera.io/nextflow/modules/)
- [Nextflow Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume)
- [Nextflow Configuration](https://www.nextflow.io/docs/latest/config.html)
- [nf-core component terminology](https://nf-co.re/docs/usage/getting_started/terminology)
- [nf-core subworkflow development](https://nf-co.re/docs/contributing/subworkflows)
- [nf-core component testing](https://nf-co.re/docs/specifications/components/subworkflows/testing)
