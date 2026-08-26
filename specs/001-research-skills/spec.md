# 功能规格：科研与生信 Agent Skill 调研

**Feature Branch**：001-research-skills

**创建日期**：2026-08-26

**状态**：Draft（草稿）

**用户输入**：调研可复用的通用科研 Agent Skill 与生信 Agent Skill，
保持两类边界分开，并在安装前评估质量、认可度和 Agent 调用方式。

## 用户场景与测试（必需）

### 用户故事 1：分开两个科研领域（优先级：P1）

作为 bio-spec-kit 的维护者，我希望有一份“通用科研 Skill”目录和一份
“生信专用 Skill”目录，这样通用研究能力不会和生信执行能力混在一起。

**为什么是这个优先级**：两类 Skill 的用户、风险、证据标准和集成方式
不同。混在一起会导致后续选择 preset 时出现错误。

**独立测试**：检查目录标题和候选范围；每个候选只能属于一个目录，
通用科研目录中不能出现只服务于生信的 Skill。

**验收场景**：

1. **给定** 调研结果已经生成，**当** 审阅者打开目录，**那么** 必须看到
   两个且仅两个明确分区：通用科研 Skill、生信 Skill。
2. **给定** 某个候选主要处理 FASTQ、BAM、VCF、RNA-seq、单细胞、变异
   calling 或其他生信专用能力，**当** 对它分类，**那么** 它只能出现在
   生信目录。
3. **给定** 某个候选主要处理文献、写作、引用管理、实验设计、Notebook
   或开放科学，**当** 对它分类，**那么** 它只能出现在通用科研目录。

### 用户故事 2：带证据比较可被 Agent 调用的 Skill（优先级：P1）

作为科研人员，我希望每个候选都说明 Agent 如何调用它，以及有哪些证据
支持其质量，这样我能区分真正可用的 Skill、概念描述和科研原型。

**为什么是这个优先级**：Agent 调用方式是本项目的核心选择因素；GitHub
star 数量本身不能证明科学质量或运行质量。

**独立测试**：从任一目录任取 5 个候选，检查每个候选是否有来源 URL、
调用方式、维护信号、许可证状态、文档/测试信号、安全说明和评分；如果
没有评分，必须有明确的排除原因。

**验收场景**：

1. **给定** 候选提供 SKILL.md、CLI、MCP server、API、Notebook 或 workflow
   wrapper，**当** 记录它时，**那么** 必须写明调用类型以及所需输入/输出。
2. **给定** GitHub stars、forks、release 或 commit 活跃度无法核实，
   **当** 对候选评分时，**那么** 必须标记为“未核实”，不能自行估算。
3. **给定** 候选使用宽松许可证，但会执行代码或向外部服务发送数据，
   **当** 对它评估时，**那么** 这些风险必须和推荐结论放在一起。

### 用户故事 3：不绕过科研质量门选择候选（优先级：P1）

作为项目维护者，我希望有一套可重复的评分与准入规则，使进入 preset、
extension、bundle 或 adapter 的候选具备足够的质量、维护、安全和
Spec Kit 适配性。

**为什么是这个优先级**：本项目将被多个项目、团队和 Agent 重复使用；
没有记录的引入决定会形成供应链风险和科研质量风险。

**独立测试**：只根据候选证据记录重新评分，并得到相同的集成层级和推荐
结论，不依赖隐藏上下文。

**验收场景**：

1. **给定** 候选评分至少为 4.0/5，且没有关键许可证或数据处理失败项，
   **当** 审阅它时，**那么** 可以标记为受控试点首选。
2. **给定** 候选属于科研原型、许可证证据缺失，或没有可重复的调用合同，
   **当** 审阅它时，**那么** 必须标记为仅供参考或需要封装，而不能直接
   进入核心 bundle。
3. **给定** 候选会执行 pipeline 或写入外部服务，**当** 提议集成它时，
   **那么** 提案必须包含 QC、provenance 和人工审批边界。

### 用户故事 4：把调研结果映射到 Spec Kit 集成点（优先级：P2）

作为维护者，我希望每个推荐候选都映射到 preset、extension、bundle 或
外部 adapter，这样下一阶段可以直接制定实现计划，而不必复制整个上游
仓库。

**为什么是这个优先级**：调研只有转化为安全、边界清晰的复用路径才有价值。

**独立测试**：对于每个首选候选，审阅者都能判断它是可直接使用、需要
wrapper、仅供参考还是排除，并能找到下一步要创建的 Spec Kit 产物。

**验收场景**：

1. **给定** 某个候选被推荐，**当** 阅读集成映射时，**那么** 必须看到一个
   明确的集成目标和所需质量门。
2. **给定** 某候选不适合放进核心 bundle，**当** 阅读映射时，**那么** 必须
   说明原因是范围、许可证、安全、维护状态还是证据不足。

### 边界情况

- 某仓库 star 很高，但维护停滞、没有测试、许可证不清楚或执行边界不安全；
  star 不能作为唯一决定因素。
- 某项目同时包含通用科研和生信 Skill；必须按单个 Skill 或能力分类，
  不能把整个仓库一次性复制进来。
- 文档描述了 Agent 调用方式，但没有确定性的输入/输出合同；必须标记为
  wrapper-needed。
- 不同页面给出了不同的 star 或 release 数值；目录必须保留观察日期，
  并标记为需要复核。
- Skill 可能访问外部 API，或接收人类基因组/临床数据；在完成数据流和
  权限审查前，必须禁止默认执行。
- 候选没有可靠的许可证证据；即使科学价值很高，也不能进入默认 bundle。

## 需求（必需）

### 功能需求

- **FR-001**：调研产物必须包含两个互不重叠的候选目录：
  scientific-general 和 bioinformatics。
- **FR-002**：scientific-general 只能包含跨领域科研能力，例如文献、写作、
  引用管理、实验设计、统计推理、Notebook、知识管理和开放科学；必须排除
  生信专用执行 Skill。
- **FR-003**：bioinformatics 只能包含生信专用 Skill、生信 Agent library，
  或可以被约束为生信 Skill 的可执行能力。
- **FR-004**：每个候选记录必须包含 canonical source URL、范围、Agent 调用
  类型、所需输入、预期输出、许可证状态、维护信号、文档/测试信号、
  安全与隐私风险以及观察日期。
- **FR-005**：采用度信号必须区分已核实的 stars/forks/releases/commits 和
  未能核实的数值；缺失证据不得靠推测补齐。
- **FR-006**：评分必须使用 0-5 分制，并按以下权重可重复计算：Agent
  调用合同 20%、科研价值 20%、维护与采用度 15%、文档与测试 15%、
  许可证 10%、安全与隐私边界 10%、Spec Kit 适配性 10%。
- **FR-007**：每个候选必须被分到以下四个集成层级之一：
  preferred-pilot、wrapper-needed、reference-only、exclude。
- **FR-008**：当候选存在未解决的关键许可证问题、未披露的敏感数据传输、
  不安全的默认执行行为或不可重复的入口时，不得标记为 preferred-pilot。
- **FR-009**：每个 preferred-pilot 推荐必须指定一个边界清晰的 Spec Kit
  目标，并写明 QC、统计、provenance 和人工审阅门。
- **FR-010**：调研默认不得安装、执行第三方候选，也不得向候选上传项目
  数据；安装或执行必须作为之后单独批准的实现任务。
- **FR-011**：调研产物必须保留以下初始候选的来源链接并记录状态，不得
  静默删除：PaperQA2、AI4S Skills、Scientific Agent Skills、Zotero MCP、
  OpenAlex MCP、Quarto、Jupyter Book、AutoRA、OSF API、GPTomics/bioSkills、
  ClawBio、Hermes Agent bioinformatics skill、bioinformatics-agent-skills、
  nf-core/rnaseq、nf-core/sarek、nf-core/scrnaseq、nf-core/seqinspector、
  MultiQC、sc-best-practices 和 CellAgent。
- **FR-012**：调研产物必须包含简洁的决策摘要，说明第一批受控试点候选，
  以及核心 bundle 发布前必须补齐的证据缺口。

### 关键实体

- **Candidate Skill（候选 Skill）**：评估是否可复用的仓库、包、Skill 文件、
  服务或 workflow 能力。
- **Evidence Record（证据记录）**：来源链接、观察日期、版本或 commit、
  采用度信号、许可证状态、维护信号和质量证据。
- **Invocation Contract（调用合同）**：描述 Agent 如何调用能力，包括输入、
  输出、副作用、权限和失败行为。
- **Scoring Record（评分记录）**：加权评分、总分、置信度和集成层级。
- **Integration Recommendation（集成建议）**：映射到 Spec Kit preset、
  extension、bundle、adapter 或明确排除。

## 成功标准（必需）

### 可衡量结果

- **SC-001**：第一版调研快照至少包含 6 个通用科研候选和 8 个生信候选，
  且两人复核没有跨领域分类错误。
- **SC-002**：两个目录中保留的候选，100% 具有来源 URL、调用类型、许可证
  状态、维护状态、安全说明、评分和观察日期，或明确标记为证据不完整。
- **SC-003**：推荐进入受控试点的候选，100% 在安装前具有输入/输出合同，
  并明确 QC、provenance 和人工审阅边界。
- **SC-004**：至少 80% 的最高层级推荐评分达到 4.0/5 或以上，且没有未解决
  的关键准入失败项。
- **SC-005**：维护者只使用已记录的证据和评分规则，即可在 10 分钟内复现
  任一候选的分类和集成层级决定。
- **SC-006**：任何调研运行都不得在没有实现批准记录的情况下安装第三方
  Skill、执行未审查的外部命令或传输项目数据。

## 假设

- “高薪、高评分”按“高质量、高认可度和高维护信号”理解；GitHub stars
  不能替代科研价值判断。
- 第一版是截至 2026-08-26 的证据快照；安装前必须重新核实会变化的
  stars、releases 和 commit 活跃度。
- 同一仓库同时包含两类能力时，尽量按单个 Skill 或能力分别评估。
- 外部集成默认使用公共数据和只读操作。
- Spec Kit 负责协调、证据、质量门和 provenance；领域工具负责真正的
  生信或科研计算。

## 初始证据来源

### 通用科研 Skill

- [PaperQA2](https://github.com/Future-House/paper-qa)
- [AI4S Skills](https://github.com/ai4s-research/ai4s-skills)
- [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- [Zotero MCP](https://github.com/drxaibi/zotero-mcp)
- [OpenAlex MCP Server](https://github.com/cyanheads/openalex-mcp-server)
- [Quarto](https://github.com/quarto-dev/quarto)
- [Jupyter Book](https://github.com/jupyter-book/jupyter-book)
- [AutoRA](https://github.com/AutoResearch/autora)
- [OSF API](https://developer.osf.io/)

### 生信 Skill 与受约束的生信能力

- [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills)
- [ClawBio](https://github.com/ClawBio/ClawBio)
- [Hermes Agent bioinformatics skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/research/bioinformatics/SKILL.md)
- [bioinformatics-agent-skills](https://github.com/YuliaNuzhnenko/bioinformatics-agent-skills)
- [nf-core/rnaseq](https://github.com/nf-core/rnaseq)
- [nf-core/sarek](https://github.com/nf-core/sarek)
- [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq)
- [nf-core/seqinspector](https://github.com/nf-core/seqinspector)
- [MultiQC](https://github.com/MultiQC/MultiQC)
- [sc-best-practices](https://www.sc-best-practices.org/)
- [CellAgent](https://arxiv.org/abs/2407.09811)
