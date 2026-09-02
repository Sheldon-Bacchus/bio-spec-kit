# Bio-Spec Kit 评测矩阵：Skill、科研方法与完整结果

版本：`0.1.0`  
状态：设计基线；不是已经全部通过的 benchmark 报告。  
范围：以已经做过的 PA/LUAD 分析、FastQC/MultiQC 以及当前五个项目 Skill 为基准。

## 1. 先把几个名称拆开

历史对话中的语音转写容易把几个不同对象合并。这里采用下面的解释：

| 用户提到的对象 | 本项目中对应的对象 | 它是什么 | 是否是同一个 Skill |
|---|---|---|---|
| KGG/KEGG 共分析 | `M04_GO_KEGG_annotation` | 对 DEG、shared direction 或模块候选做 GO/KEGG 富集和分支比较 | 主要对应 `pathway-enrichment` |
| 共分析/共同基因 | `M07_shared_149_direction` | PA/LUAD 结果的基因交集和 UpUp/DownDown/UpDown/DownUp 分层 | 对应 `cross-branch-integration` |
| DEG | `M03_PA_DE`、`M03_LUAD_DE_GSE75037` | 差异表达结果及其阈值、方向和 tested-gene universe | 对应 `bulk-pa-luad`；外部结构参考是 `bulk-rnaseq` |
| FastQC | FastQC log → MultiQC report | 上游质量报告生成和内容核对 | 对应 `multiqc` |

这里没有把“FastQC-DEG”当成一个方法。若它的意思是“FastQC 之后进入 DEG”，那是两个相邻节点：

```text
FastQC/MultiQC（输入质量证据）
        ↓
DEG（统计推断）
        ↓
共同基因/方向整合
        ↓
GO/KEGG（功能解释）
        ↓
独立复现或实验验证
```

每个箭头都必须有输入输出合同。FastQC 报告不能证明 DEG 正确；KEGG 富集也不能反过来证明 DEG 或因果机制。

## 2. 三个完全不同的评测对象

### 2.1 单一 Skill 测试：Skill 有没有被正确使用

它问的是：

> 加载这个 Skill 后，Agent 的选择、澄清、约束遵守和交付行为是否变好？

它不问“这个科学结论是否已经被实验验证”。

单 Skill 测试至少包括：

| 测试层 | 要测试什么 | 主要证据 |
|---|---|---|
| 结构 | frontmatter、职责、触发条件、禁用范围、引用路径是否完整 | `SKILL.md`、结构检查器 |
| 路由 | 该用时能否触发，不该用时能否不触发 | 正例、负例、相邻 Skill 竞争 |
| 输入合同 | 是否要求正确的数据、ID、单位、参考版本、阈值和设计信息 | 输入检查记录 |
| 指令遵守 | 是否执行 Skill 的关键决策和停止条件 | Agent trajectory、工具调用日志 |
| 失败闭环 | 缺失、冲突、工具错误时是否停机、澄清或降级 | `NEEDS_INPUT`、`BLOCKED`、`ESCALATE` |
| 输出合同 | 是否产生规定的 artifact、字段、版本和限制说明 | schema、artifact manifest |
| 确定性脚本 | Skill 附带的脚本是否对已知输入给出正确结果 | unit test、golden fixture |
| 来源完整性 | 上游 Skill 是否被静默改写 | commit、原始 hash、规范化 hash、manifest |
| 边际收益 | 有 Skill 和无 Skill 是否有可重复差异 | paired with/without runs |

### 2.2 单一科研方法测试：方法本身是否正确

它问的是：

> 即使没有 Agent，按照这个方法和参数，统计或计算过程是否成立？

重点是已知答案模拟、阴性对照、前置条件、敏感性分析、替代实现和结果语义。

### 2.3 完整科研结果测试：从输入到 Claim 是否可信

它问的是：

> 这次实验从数据身份、QC、统计、整合、解释到最终结论，是否形成了可复现且不过度宣称的证据链？

这必须另外经过三个大测试：

1. 计算重现：同一锁定输入能否重新得到同一结果；
2. 独立复现：新的队列、样本或独立数据能否支持同一方向/效应；
3. 正交或生物学验证：不同测量或干预是否支持研究 Claim。

这三个测试不能用一次成功的 Skill 调用替代。

## 3. Skill benchmark 应该怎样演

### 3.1 最重要的实验设计：成对干预

Skill 的效果不能用“有 Skill 的一次结果”判断。最小设计是固定其他条件，只改变 Skill：

```text
同一模型
同一任务
同一输入
同一工具和预算
同一 verifier
        ├── no-skill baseline
        ├── curated-skill condition
        └── self-generated-skill condition（可选）
```

核心量是：

```text
Skill gain = Pass(with Skill) - Pass(without Skill)
```

还要报告：

- `improved`：有 Skill 成功、无 Skill 失败；
- `unchanged`：两者相同；
- `harmed`：有 Skill 反而失败或违反约束；
- `both-failed`：两者都失败。

如果只测 with-skill，很容易把模型自身能力、工具能力或 fixture 简单度误认为 Skill 的贡献。

### 3.2 一个 benchmark case 不只是 prompt

每个 case 应保存一份 Agent 看不到的评测合同：

```text
case/
├── case.yml                 # 用户输入、场景和允许范围
├── inputs/                  # fixture 或脱敏输入
├── oracle.yml               # 允许方案、禁止错误、预期状态
├── verifier/                # 确定性检查器
├── reference/               # reference artifact 或数值容差
└── README.md                # 人工复核说明
```

`oracle.yml` 至少声明：

- 期望触发的 Skill 和允许的替代 Skill；
- 必须发现的 blocker；
- 可接受的方法集合；
- 禁止的科学错误；
- 必须生成的输出文件和字段；
- 关键数值及容差；
- 必须记录的版本、参数和 hash；
- 预期是 `READY`、`NEEDS_INPUT`、`BLOCKED` 还是 `ESCALATE`；
- 哪些输出只能是 exploratory，不能进入 release。

### 3.3 外部 benchmark 在这里各自负责什么

之前讨论过的项目不能混成一个总 benchmark：

| 项目 | 它真正测什么 | 对本项目的用法 | 不能替代什么 |
|---|---|---|---|
| SkillsBench | with-skill/without-skill 的 Skill 边际收益 | 借用成对实验、重复运行、trajectory 和成本记录 | 不能替代生信科学正确性 |
| PromptBio-Bench | Agent 是否能拿真实生物数据、调用工具并交付文件 | 借用任务合同、输入文件、reference artifact 和 verifier 形态 | 不能证明统计设计或生物机制 |
| `spec-kit-verify` | Spec、Plan、Tasks 与实现的追溯和覆盖 | 做 Spec-to-artifact compliance grader | 不能证明分析实际运行或科学正确 |
| `spec-kit-verify-tasks` | `[X]` 任务是否有真实完成证据，避免空实现 | 做“完成声明可信度”检查 | 不能测 Skill 增益或生物学有效性 |
| `tiny-spec` rubric | SDD 框架的经验性能、严谨性、审计性、流程开销 | 借用框架质量 rubric | 不是成熟科研 benchmark |
| LAB-Bench / ScienceAgentBench | 生物学知识、数据库、protocol 或程序任务 | 借用领域 case 类型和专家 rubric | 不等于本项目完整实验结果 |
| PaperBench | 完整科研复现和层级化 rubric | 借用“多条合法路径 + 独立重跑 + 分层评分” | 不直接评估某一个 Bio Skill |

结论是：目前没有一个已经被社区统一认可、同时覆盖 Bio Skill、Spec、统计方法、完整科研 Claim 和实验验证的单一 benchmark。我们需要组合这些思想，建立自己的小型、固定、可审计 case 集。

相关入口： [SkillsBench](https://github.com/benchflow-ai/skillsbench)、[PromptBio-Bench](https://github.com/PromptBio/promptbio-bench)、[spec-kit-verify](https://github.com/ismaelJimenez/spec-kit-verify)、[spec-kit-verify-tasks](https://github.com/datastone-inc/spec-kit-verify-tasks)、[PaperBench](https://openai.com/index/paperbench/)。

## 4. 当前四类 Skill 的单独测试

### 4.1 `multiqc`：FastQC/MultiQC Skill

#### Skill 层

- 正例：输入目录含预期 FastQC log，能选择 `multiqc` Skill 和正确 preset；
- 负例：只有 BAM、VCF 或未知日志时，不应假装完成 FastQC QC；
- 缺失：输入目录、配置、可执行文件或预期样本缺失时应 fail closed；
- 内容：HTML、JSON、source mapping、log 都必须包含 fixture 派生证据；
- 边界：报告生成成功不等于 QC threshold 通过；
- 安全：敏感数据不能自动进入网络摘要模式；
- provenance：记录 MultiQC 版本、wrapper 版本、命令、输入输出 hash。

#### 当前已完成

当前本地已有真实 MultiQC vertical slice：

- 输入是最小 FastQC fixture；
- 调用真实 MultiQC 1.35 CLI；
- 验证 HTML、JSON、source mapping 和 fixture marker；
- fixture 改变时 artifact 内容随之改变；
- executable 缺失时失败闭环。

这证明的是 `multiqc` 的执行闭环，不证明 FastQC 生物学 QC 门限，也不证明下游 DEG。

#### 仍缺

- no-skill/with-skill 的 Agent 触发对照；
- malformed FastQC、错误样本 roster、重复样本和无目标 module；
- 把 QC 结果安全地传给 DEG 的输入合同；
- 人工 review 记录和 release gate。

### 4.2 `bulk-pa-luad`：DEG/edgeR/limma Skill

#### Skill 层

- 正例：用户明确给出 count matrix、metadata、subject/pairing、condition、contrast 和 estimand；
- 负例：输入是 TPM/CPM/VST 却要求 edgeR count model 时必须拒绝；
- 路由：paired bulk 与 single-cell、unpaired bulk、workflow engine 任务要正确区分；
- 方法约束：必须先 `filterByExpr`，使用明确的 normalization 和 edgeR QL；
- 设计约束：配对数据必须进入设计矩阵，不能为了简单改成 unpaired；
- 输出约束：结果必须带 signed statistic、tested-gene universe、版本、参数和 hash；
- 失败：非整数 counts、metadata join 不完整、design singular、包缺失时 fail closed；
- 结果语义：无显著 DEG 可以是有效阴性结果，不能改成空的“成功”或虚构阳性。

#### 方法层最小 case

1. 已知效应的合成 count 数据：已知若干基因上调/下调，检查方向、效应排序和 FDR 行为；
2. 全零效应阴性数据：检查假阳性率和空结果语义；
3. paired 与 unpaired 成对数据：改变 pairing 条件后设计矩阵和结果必须改变；
4. metadata 缺失、重复 subject、condition 不完整：都应阻塞；
5. 非整数输入、TPM 冒充 counts：应拒绝；
6. contrast 反向：结果 logFC 方向应反向，不能只改标签；
7. duplicate gene IDs：去重规则必须显式记录，不能静默覆盖；
8. 同一输入重跑：结果在声明的数值容差内一致。

#### 与已有 PA/LUAD 结果的关系

`M03_PA_DE` 和 `M03_LUAD_DE_GSE75037` 是已经产生的研究结果，可作为 reference artifact 和真实 case 背景；但它们不是自动等于当前 `bulk-pa-luad` Skill 已经在本仓库中重新执行通过。要升级为“本 Skill 已验证”，还需锁定原始输入、设计、脚本、软件环境、输出 hash 并完成独立重跑。

### 4.3 `cross-branch-integration`：共同基因/方向共分析 Skill

#### Skill 层

- 正例：两个分支有明确 branch label、stable subject/sample map、ID namespace、方向约定和整合问题；
- 负例：只有两个结果表但没有样本对应关系，却要求做 joint model 时必须拒绝；
- 不得按行号把两个表配对；
- ID、assembly、namespace 不一致时必须阻塞或报告无法匹配；
- 必须保留 unmatched records，不能只输出交集；
- 方向定义必须来自 signed effect/statistic，并记录 cutoff；
- 直接交集只能称为 descriptive overlap，不能自动升级为共同因果机制；
- joint model 若没有 held-out validation，只能作为未验证候选，不能 release。

#### 方法层最小 case

使用一个 4–8 个基因的 toy table，预先知道四类结果：

```text
Up / Up
Down / Down
Up / Down
Down / Up
```

逐项改变：

1. 行顺序：结果应不变；
2. gene symbol 大小写或 alias：若规则允许，应规范化并记录；
3. 重复 ID：按预先声明的规则处理；
4. 一个分支缺失：保留 unmatched，不生成伪交集；
5. 一侧改变阈值：交集数量和方向分层必须随之改变；
6. 一侧反转 contrast：方向 strata 应相应改变；
7. 混入不同 assembly/namespace：应失败或进入 `NEEDS_INPUT`；
8. 随机打乱两侧 row order：不得影响结果。

#### 已有研究结果

当前真实结果是 shared 149：`UpUp 50`、`DownDown 17`、`UpDown 73`、`DownUp 9`。它适合作为 reference output 和检验数据连接的真实 case；它本身仍是共同变化描述层，不是独立验证，也不是因果证明。

### 4.4 `pathway-enrichment`：GO/KEGG Skill

#### Skill 层

- 输入必须来自已经执行的 DEG 或 module 结果，Skill 不能自己发明 gene list；
- thresholded list 走 ORA，完整 ranked list 才能走 GSEA；
- ORA 必须使用 tested-gene universe，不能默认用全基因组；
- foreground 和 universe 必须经过同一 ID mapping 路径；
- mapping loss、duplicate、unmapped 数量必须报告；
- up/down 方向需要分开时不能合成一组；
- KEGG 必须记录 organism、keyType、数据库 access date 或 frozen snapshot；
- 无显著通路是有效结果；不能编辑结果表使其通过 cutoff；
- pathway enrichment 是解释性/假设生成证据，不是同一 DEG 结果的独立验证。

#### 方法层最小 case

1. 合成 gene set + 明确 universe：已知一个 pathway 被富集，检查 ORA 方向、overlap 和 BH 调整；
2. 改变 universe：结果必须改变，证明背景不是隐藏默认值；
3. 混用 SYMBOL/ENSEMBL/Entrez：应失败或显式报告 mapping loss；
4. ORA 输入没有 universe：必须 fail closed；
5. GSEA 只给显著 gene list、没有全量 ranking：必须拒绝；
6. 上下调列表分开：结果不得被方向混淆；
7. KEGG organism/keyType 错误：必须阻塞，不得返回貌似正常的零结果；
8. live KEGG 与 frozen snapshot：必须记录版本/日期并能解释差异；
9. 同一 snapshot 重跑：结果在声明容差内一致；
10. pathway redundancy：必须注明 collapse 或未 collapse，不能把重复术语当独立机制证据。

#### 已有研究结果

`M04_GO_KEGG_annotation` 当前状态是 `COMPLETED_WITH_BOUNDARY`。其中已有 GO/KEGG 表、mapping counts、universe 和方法报告，因此可以作为真实 benchmark case；但它不能自动被当成独立生物学验证。尤其 KEGG 的 live database 状态必须冻结，不能只保留结果表。

### 4.5 `wgcna-module-constraint`：WGCNA 模块约束 Skill

WGCNA 不应被当成 DEG 或 KEGG 的“自动下一步”。它是一个对表达矩阵、样本量、批次、trait 和网络参数都有额外前置条件的模块发现/约束方法。

#### Skill 层

- 正例：输入是方向明确的 normalized bulk expression、完整 sample trait、batch/subject 信息和预先声明的最小样本规则；
- 负例：raw single-cell dropout 矩阵、样本数过少、要求把共表达直接解释成因果调控，或没有验证队列却声称 module preservation；
- 设计约束：network type、soft power、outlier 规则、module cut 参数和 trait 必须显式记录；
- 语义约束：grey module 不能被当成生物学模块，co-expression 不能被写成 causal regulation；
- 冲突约束：sample/trait 数量不匹配、batch 与 biological condition 完全混淆、验证队列 namespace 不一致时应阻塞或降级；
- 输出约束：模块标签、eigengene、module-trait statistics、kME/hub、stability/preservation 和参数 provenance 必须可追溯。

#### 方法层最小 case

1. 合成表达矩阵中植入一个已知 trait-associated module，检查模块与 trait 的关系方向；
2. 无信号阴性矩阵，检查是否产生虚假模块故事；
3. 打乱 sample/gene 顺序，结果在 label permutation 后应等价；
4. 加入轻微噪声或移除异常样本，检查稳定性指标按规则变化；
5. batch 完全等于 biology 时进入高风险或阻塞；
6. 样本数低于 preset 时拒绝把结果提升为主要证据；
7. 把 grey module 标成 biological module 时 verifier 必须失败；
8. 没有独立验证队列时，`preservation` 只能是未达到或候选状态。

#### 已有研究结果

`research-top` 已有 WGCNA comparison、module preservation 相关记录和 candidate module，但当前 `bio-spec-kit` 还没有固定 expression fixture、golden module oracle、可执行 runtime、preservation verifier、batch-confounding case 或 with/without Skill 对照。因此它目前属于研究候选/方法设计层，不是已经 benchmark 通过的 Skill。

## 5. 单一科研方法测试的共同模板

每个方法都应有下面八类检查，不依赖 Agent 是否参与：

| 方法检查 | 问题 |
|---|---|
| 适用性 | 输入数据和科学问题是否真的适合该方法？ |
| 已知答案 | 合成数据或小型 toy case 的预期方向/数值能否恢复？ |
| 阴性对照 | 没有效应时是否保持合理的假阳性和空结果语义？ |
| 前置条件 | 输入类型、重复、配对、ID、universe、scale 和参考版本是否满足？ |
| 参数敏感性 | 改变一个参数后，结果是否按预期改变，而不是完全不变或不稳定？ |
| 替代方法 | 用合理的第二实现或敏感性分析检查主要结论是否稳健？ |
| 结果语义 | effect、direction、interval、FDR、overlap 和限制是否解释正确？ |
| 重现性 | 同一环境重跑、清洁环境重跑、输入 hash 和软件版本是否匹配？ |

重要原则：

- 一个方法在 toy data 上通过，只说明实现和局部统计行为可接受；
- 一个方法在真实数据上生成表，只说明产生了结果文件；
- 只有前置条件、统计行为、provenance 和独立复现都通过，才可支持更强 Claim。

## 6. 完整科研结果的三个测试

### E1：计算重现测试

目的：证明“这次结果确实由声明的输入、脚本、参数和版本产生”。

对 PA/LUAD 主线，最小链条应是：

```text
冻结输入与 manifest
  → PA/LUAD DEG
  → shared intersection/direction
  → GO/KEGG interpretation
  → run manifest / provenance / claim record
```

验收证据：

- 输入文件、脚本、工具、数据库和参数都有版本或 hash；
- 每个下游表能追溯到上游 artifact；
- 清洁目录重跑成功；
- 关键行数、方向、统计量和结果文件在容差内一致；
- 修改输入后，受影响的下游 artifact 发生可解释变化；
- 不允许使用手工编辑后的中间表冒充运行结果。

E1 不能证明生物学真理，只能证明计算链可信。

### E2：独立数据/holdout 复现测试

目的：检验结果是否只适用于发现数据。

验收要求：

- 独立队列、独立样本或预先留出的 patient-level 数据不能参与发现阈值；
- gene ID、reference、assay 和样本单位一致或差异被显式处理；
- 复现的目标必须预先定义，例如方向、效应区间、患者级分层或 pathway-level signal；
- 不应要求每个基因逐个显著，必须事先声明 replication criterion；
- 失败或不一致要保留为 negative/inconclusive，不通过调整阈值强行修复。

现有 `research-top` 中已经有患者级复现、外部复现审计等材料，但它们需要逐个检查数据独立性、是否真正运行、是否有 leakage 和最终状态，不能仅因文件存在就判定 E2 通过。

### E3：正交/生物学验证测试

目的：检验“计算候选”是否得到不同测量或干预的支持。

可接受的证据类型取决于 Claim：

- qPCR、蛋白、免疫染色或 FISH 等正交测量；
- 细胞或动物中的扰动、抑制、rescue 或 target engagement；
- 对 PA Claim 的直接证据，如原始测序、PathSeq/Kraken2、16S、FISH 或 qPCR；
- 空间/患者级证据只能支持相应层级的定位或关联，不自动成为感染因果证据。

必须保持以下边界：

```text
DEG ≠ pathway proof
pathway enrichment ≠ causal target
shared 149 ≠ shared mechanism
scRNA/ST compatible state ≠ PA-positive
expression association ≠ infection causality
```

E3 没有完成时，最终状态最多是候选、关联或待验证，不能发布为已证实机制。

### 6.1 与现有 `research-top` 证据逐项对账

下面这张表把“已经有研究记录”与“已经通过完整验证”分开。它是当前判断自动化成熟度的依据，而不是把旧结果重新包装成通过。

| 现有证据 | 已观察到的状态 | 它能证明什么 | 仍不能证明什么 |
|---|---|---|---|
| LUAD paired limma reproduction | `PASS`；166 samples、83 pairs；重跑与参考结果的相关性/recall/direction 为 1，最大绝对差约 `1.2e-14` | 这一条声明的计算重现链在固定环境下高度一致 | 不等于独立患者队列 E2，也不等于生物学 E3 |
| PA/LUAD 主线的 WGCNA/交集/KEGG 执行 | 技术执行通过、design audit `15/15`，但总体仍为 `AGENT_VERIFIED / NEEDS_HUMAN_REVIEW`，不是 `FINAL_VERIFIED` | 运行产物和部分设计检查存在 | 不足以证明完整 scientific release，尤其不能替代 KEGG snapshot、E2、E3 |
| promotion asset/hash validation | 资产 hash 检查有 `PASS`，但整体 technical validation 曾因旧 graphics 路径缺失、README/tasks hash 不一致而 `FAILED` | 说明发布资产完整性本身也需要单独 gate | 不能因为部分 hash 通过就宣布整条研究链通过 |
| `M03_PA_DE`、`M03_LUAD_DE_GSE75037`、`M07_shared_149_direction`、`M04_GO_KEGG_annotation` | 有真实结果、Run ID、artifact hash、数量 QA 和边界声明 | 结果归档可追溯，部分算术/结构关系成立 | 不是每个方法都已有独立 fixture、oracle、反事实测试和 clean rerun |
| “independent candidate” 比较 | 两个候选集约为 `174 vs 149`，重叠 `142`，Jaccard 约 `0.7845` | 可以作为候选集 concordance 线索 | 不是 patient-level 独立复现，来源、处理、leakage 和 holdout 尚未闭环 |
| patient-level validation / scRNA-ST 路线 | patient-level rerun 因输入缺失而 `BLOCKED`；scRNA/ST 仍为 `STAGING_UNCONFIRMED`；qPCR 主要是设计，蛋白/FISH/扰动等未达到 | 明确知道验证路线和阻塞位置 | 还没有 E2 的独立数据结论，也没有 E3 的实验/正交结论 |

因此，当前项目的真实状态是：

```text
归档与部分计算重现：有实证
单方法独立 benchmark：尚未完成
E1 整链 release gate：部分完成
E2 独立队列/holdout：未闭环，部分 blocked
E3 正交/实验验证：未达到
完全无人值守自动驾驶：不成立
```

## 7. 当前项目到底还缺什么

| 层次 | 当前已有 | 当前缺口 | 判断 |
|---|---|---|---|
| Spec Core | `specs/002` 有完整 spec/plan/tasks；有官方流程候选 | `bio-research-mvp` 的安装、materialization、workflow/gate 还未完整验证 | 部分完成 |
| Skill 结构 | 5 个 Skill 已有 staging 和 discovery 目录；结构校验通过 | 没有统一 case registry、with/without harness、Skill gain 报告 | 只完成结构层 |
| MultiQC/FastQC | 已有真实 CLI、fixture、HTML/JSON、3 个 E2E 测试 | 还没有接到 DEG 输入合同，也没有完整 QC gate | 第一个执行 MVP 已完成 |
| DEG | `research-top` 有 M03 真实结果和方法报告 | 当前 repo 没有 `bulk-pa-luad` 的完整 R runtime、fixture、verifier 和重跑记录 | 研究结果有，Skill runtime 未完成 |
| 共同基因/方向 | `research-top` 有 shared 149 和四类方向表 | 当前 repo 没有确定性 integration wrapper 和 toy/golden tests | 真实结果有，Skill runtime 未完成 |
| GO/KEGG | `research-top` 有 M04 结果、mapping/universe 字段和方法报告 | 当前 repo 的 KEGG/GO runtime pending；live DB pin 和独立 verifier 尚未闭环 | 结果有边界，运行链未完成 |
| 科研验证 | 有 ECK 的 supported/not-supported/inconclusive/not-evaluable 状态 | validation 目前较接近 fixture declaration；缺 Evidence Registry 和真正独立验证 provider | 语义 MVP 部分完成 |
| WGCNA | 有 method reference、comparison 和 candidate module 记录 | 没有 fixture、golden module、stability/preservation verifier、batch-confounding 和 sample-size rejection case | 研究候选层 |
| 完整实验结果 | 已有真实 PA/LUAD 研究工程和候选实验路线；局部 LUAD E1 reproduction 可通过 | 主线仍是 `NEEDS_HUMAN_REVIEW`；E1/E2/E3 没有统一 release gate 和最终 evidence package | 未完成 |
| Benchmark | 已分析 SkillsBench、PromptBio-Bench、Spec verify、PaperBench 等 | 尚无自己的固定 Bio cases、隐藏 oracle、重复运行统计和报告 | 尚未开始执行 |
| 人工控制 | 已定义 `explain-only`、`propose-only`、`apply-approved` | 还未把审批、waiver、release 记录全部接入运行链 | 设计完成，工程未闭环 |

所以当前不是“完全自动化”。准确说法是：

> 已有一个可以真实执行和验证的 MultiQC 最小切片，以及一个可以计算证据状态的 ECK；其余真实科研方法仍处于适配器、研究结果参考或待接入 runtime 状态。

## 8. 建议现在开始的自己的 MVP

不建议马上把 FastQC、原始 counts、DEG、WGCNA、KEGG、scRNA/ST、实验验证全部串成一个巨大 MVP。当前最小且有科研价值的垂直切片应是：

### Bio-Research Validation MVP-1

```text
两个已冻结的 DEG result tables
        ↓
确定性 shared intersection + direction strata
        ↓
本地冻结 gene-set 的 ORA/解释性结果
        ↓
Evidence/Provenance/Claim record
        ↓
E1 计算重现 gate
```

具体范围：

1. 暂不重跑完整 raw-count DEG；先把已有 PA/LUAD DEG 表作为有 provenance 的输入 fixture；
2. 实现 `cross-branch-integration` 的确定性 wrapper；
3. 用 toy fixture 和真实 shared 149 case 同时测试；
4. 先使用本地冻结 gene-set/GMT 做可复现的 pathway slice；KEGG live REST 作为显式后置例外；
5. 输出 intersection table、四类 direction table、mapping audit、pathway table、manifest、verdict 和 limitation report；
6. 把这些输出接入 ECK 的 Observable/Validation/Claim；
7. 加入 no-skill/with-skill 的 Skill 评测入口，但不让 Skill 直接写科学结果；
8. 以 E1 为 MVP 的 release gate，E2/E3 只记录为 `not_reached` 或 `pending`，不伪装成通过。

### 为什么 FastQC 不和这个 MVP 强行合并

FastQC/MultiQC 是输入质量与报告生成切片，已经有独立的真实执行证明。把它和 DEG/KEGG 首次接入时同时合并，会让失败原因难以区分：究竟是 QC、统计设计、ID mapping、KEGG 版本还是 Claim 状态出了问题。

因此建议保留两条可组合的 MVP：

```text
MVP-0A：FastQC fixture → MultiQC → 内容验证报告       已有
MVP-0B：固定 DEG → shared 149 → pathway → ECK         下一步
MVP-1 ：raw counts → DEG → shared → pathway → ECK      后续
MVP-2 ：E1 + 独立 cohort/holdout 的 E2                再后续
MVP-3 ：E3 正交/扰动/直接 PA 证据                     实验阶段
```

## 9. 进入 MVP 前的硬性判定

一个 case 只有同时满足以下条件，才能说“这一层通过”：

```text
正确路由
∧ 输入合同满足
∧ 方法前置条件满足
∧ 确定性 verifier 通过
∧ provenance 完整
∧ 失败 case 能正确停机
∧ 重跑在声明容差内一致
∧ 没有越过 Claim boundary
```

任何以下情况直接 hard fail：

- 把不存在的样本、版本、结果或文献写进报告；
- 把 unknown 或 conflict 静默变成事实；
- 把 shared overlap 写成因果机制；
- 把 KEGG/GO 富集写成独立验证；
- 把技术重复当成生物学重复；
- 只有静态结果文件，没有真实执行证据；
- provenance 与结果不匹配仍然输出 supported/release；
- 在关键设计信息缺失时继续运行；
- 用人工编辑结果代替 wrapper 产物。

本文件是当前 Bio-Spec Kit 的评测和 MVP 入口；它不把现有研究结果重新判定为已验证，也不替代后续实际运行和人工科研审查。
